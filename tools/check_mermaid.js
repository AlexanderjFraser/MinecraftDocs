#!/usr/bin/env node
/*
 * Every mermaid diagram on every page must parse under the mermaid the site ships.
 *
 * The live site shows a "Syntax error in text / mermaid version 11.6.0" box
 * wherever the browser's mermaid rejects a diagram, and nothing between the
 * markdown and the browser checks for that. This does: it builds the book
 * (mdbook + mdbook-mermaid from ~/.cargo/bin), walks every .html under book/,
 * takes each `<pre class="mermaid">` block exactly the way mermaid's own run()
 * does in the browser (innerHTML -> entity decode -> dedent -> trim), and feeds
 * that text to the same mermaid.min.js (repo root, listed in book.toml's
 * additional-js) loaded in a jsdom window. The verdict is the browser's
 * verdict, not a guess from the markdown: the HTML parser sees the text first,
 * so a stray `<` may already be gone by the time mermaid does.
 *
 * Usage (from the repo root; needs `npm install` in tools/ once, for jsdom):
 *     node tools/check_mermaid.js              # mdbook build, then check
 *     node tools/check_mermaid.js --no-build   # check the existing book/
 *     node tools/check_mermaid.js --verbose    # full mermaid error per failure
 * Prints one line per failing diagram:
 *     src/<page>.md:<line>: <error>
 * where <line> is the diagram's first line in the markdown, and the error
 * carries mermaid's own line number mapped back to the file (approximate: jison
 * reports an error at an end-of-line one line late), then a summary
 * `N diagrams checked, M failed`. Exit 1 if any failed, 0 if clean, 2 if the
 * tool itself could not run. book/print.html (every page again) and
 * book/index.html (the first page again) are skipped so each diagram counts once.
 *
 * One non-parse failure is also reported: a `#` in sequence-diagram text, which
 * mermaid reads as a comment and silently drops along with the rest of the line.
 * The escapes that survive both checks are mermaid's entity codes, `#59;` for
 * `;` and `#35;` for `#` (a `;` otherwise ends the statement mid-sentence).
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const BOOK_DIR = path.join(ROOT, 'book');
const MERMAID_JS = path.join(ROOT, 'mermaid.min.js');
// Root pages mdbook writes that only repeat other pages (or, for 404, have none).
const REPEAT_PAGES = new Set(['print.html', 'index.html', '404.html']);
// mermaid's default maxTextSize: a longer diagram never errors, it silently
// renders the "Maximum text size in diagram exceeded" placeholder instead.
const MAX_TEXT_SIZE = 50000;

function usage() {
  console.error([
    'usage: node tools/check_mermaid.js [--no-build] [--verbose]',
    '  --no-build   check the existing book/ instead of running mdbook build first',
    '  --verbose    print the full mermaid error under each failure line',
  ].join('\n'));
}

function parseArgs(argv) {
  const opts = { build: true, verbose: false };
  for (const a of argv) {
    if (a === '--no-build') opts.build = false;
    else if (a === '--build') opts.build = true;
    else if (a === '--verbose' || a === '-v') opts.verbose = true;
    else if (a === '--help' || a === '-h') { usage(); process.exit(0); }
    else { console.error(`unknown argument: ${a}`); usage(); process.exit(2); }
  }
  return opts;
}

// `mdbook build` from ~/.cargo/bin, with ~/.cargo/bin on the child's PATH so
// mdbook can find the mdbook-mermaid preprocessor book.toml names.
function buildBook() {
  const cargoBin = path.join(os.homedir(), '.cargo', 'bin');
  let mdbook = path.join(cargoBin, process.platform === 'win32' ? 'mdbook.exe' : 'mdbook');
  if (!fs.existsSync(mdbook)) mdbook = 'mdbook';
  const env = { ...process.env };
  const pathKey = Object.keys(env).find((k) => k.toUpperCase() === 'PATH') || 'PATH';
  env[pathKey] = cargoBin + path.delimiter + (env[pathKey] || '');
  console.error(`building book/ with ${mdbook} build`);
  const r = spawnSync(mdbook, ['build'], { cwd: ROOT, stdio: 'inherit', env });
  if (r.error || r.status !== 0) {
    console.error(`mdbook build failed${r.error ? ': ' + r.error.message : ` (exit ${r.status})`}`);
    process.exit(2);
  }
}

function relPosix(p) {
  return path.relative(ROOT, p).split(path.sep).join('/');
}

function listHtml(dir, out = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
  for (const ent of entries) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) listHtml(p, out);
    else if (ent.isFile() && ent.name.endsWith('.html')) out.push(p);
  }
  return out;
}

// Load mermaid.min.js into a jsdom window as a classic script (a vm.Script in
// the window's context, like a <script> tag). A window.eval would not do: the
// bundle is strict-mode, and a strict indirect eval keeps its top-level `var`
// to itself, so the IIFE's result never reaches globalThis.
function loadMermaid(JSDOM) {
  const dom = new JSDOM('<!DOCTYPE html><html><head></head><body></body></html>', {
    runScripts: 'outside-only',
    pretendToBeVisual: true,
    url: 'https://minecraftdocs.dev/',
  });
  const w = dom.window;
  if (typeof w.matchMedia !== 'function') {
    w.matchMedia = () => ({
      matches: false, media: '', onchange: null,
      addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {},
      dispatchEvent() { return false; },
    });
  }
  const src = fs.readFileSync(MERMAID_JS, 'utf8');
  new vm.Script(src, { filename: 'mermaid.min.js' }).runInContext(dom.getInternalVMContext());
  if (!w.mermaid || typeof w.mermaid.parse !== 'function') {
    throw new Error('mermaid.min.js did not define window.mermaid.parse');
  }
  // What mermaid-init.js does in the browser, minus startOnLoad (we call parse ourselves).
  w.mermaid.initialize({ startOnLoad: false, theme: 'default' });
  return { window: w, mermaid: w.mermaid };
}

// --- the text mermaid sees: a copy of what its run() does to each element ----

// mermaid's utils.entityDecode: innerHTML in, text out, through a scratch <div>.
function entityDecode(document, html) {
  const div = document.createElement('div');
  html = escape(html).replace(/%26/g, '&').replace(/%23/g, '#').replace(/%3B/g, ';');
  div.innerHTML = html;
  return unescape(div.textContent);
}

// ts-dedent for a single string, as mermaid calls it.
function dedent(str) {
  str = str.replace(/\r?\n([\t ]*)$/, '');
  const matches = str.match(/\n([\t ]+|(?!\s).)/g);
  if (matches) {
    const min = Math.min(...matches.map((m) => (m.match(/[\t ]/g) || []).length));
    if (min > 0) str = str.replace(new RegExp(`\n[\t ]{${min}}`, 'g'), '\n');
  }
  return str.replace(/^\r?\n/, '');
}

function diagramText(element, document) {
  return dedent(entityDecode(document, element.innerHTML)).trim().replace(/<br\s*\/?>/gi, '<br/>');
}

// --- mapping a block back to the markdown ------------------------------------

// The ```mermaid fences of one markdown file: { line: 1-based line of the
// opening fence, body: the text between the fences }.
function mermaidFences(md) {
  const lines = md.replace(/\r\n?/g, '\n').split('\n');
  const fences = [];
  let open = null;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (open === null) {
      const m = /^\s*(`{3,}|~{3,})\s*mermaid\s*$/.exec(l);
      if (m) open = { line: i + 1, marker: m[1], body: [] };
    } else {
      const m = /^\s*(`{3,}|~{3,})\s*$/.exec(l);
      if (m && m[1][0] === open.marker[0] && m[1].length >= open.marker.length) {
        fences.push({ line: open.line, body: open.body.join('\n') });
        open = null;
      } else {
        open.body.push(l);
      }
    }
  }
  return fences;
}

const norm = (s) => s.replace(/\r/g, '').split('\n').map((l) => l.trimEnd()).join('\n').trim();

// mermaid counts error lines against the text after its own preprocessing
// (leading blank lines gone, YAML front matter cut, `%%` comment lines and the
// blank lines before them removed), so "line n" is mapped back through the
// same steps.
function markdownLine(fence, n) {
  const lines = fence.body.split('\n');
  let kept = lines.map((text, i) => ({ text, md: fence.line + 1 + i }));
  while (kept.length && kept[0].text.trim() === '') kept.shift();
  if (kept.length && kept[0].text.trim() === '---') {
    const end = kept.findIndex((l, i) => i > 0 && l.text.trim() === '---');
    if (end > 0) kept = kept.slice(end + 1);
  }
  const out = [];
  for (const l of kept) {
    if (/^\s*%%(?!\{)/.test(l.text)) {
      while (out.length && out[out.length - 1].text.trim() === '') out.pop();
      continue;
    }
    out.push(l);
  }
  while (out.length && out[0].text.trim() === '') out.shift();
  const hit = out[n - 1];
  return hit ? hit.md : null;
}

// In a sequence diagram a `#` outside an entity code (`#59;` for `;`, `#35;`
// for `#` itself) opens a legacy comment: no error, the rest of the line just
// never renders. A parse verdict cannot see that, so it is checked here.
function droppedByHashComment(text) {
  const lines = text.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^\s*(%%|#)/.test(line)) continue; // a whole-line comment is deliberate
    const stripped = line.replace(/#\w+;/g, '');
    const at = stripped.indexOf('#');
    if (at >= 0) return { line: i + 1, text: stripped.slice(at, at + 40).trim() };
  }
  return null;
}

function oneLine(err, fence) {
  const msg = String((err && err.message) || err).replace(/\r/g, '');
  const lines = msg.split('\n');
  let first = lines[0].trim();
  if (first.length > 240) first = first.slice(0, 237) + '...';
  first = first.replace(/:\s*$/, '');
  const m = /line (\d+)/i.exec(first);
  if (m && fence) {
    const md = markdownLine(fence, Number(m[1]));
    if (md) first += ` (≈ file line ${md})`;
  }
  const expecting = lines.find((l) => /^Expecting /.test(l.trim()));
  return expecting ? `${first}; ${expecting.trim()}` : first;
}

// --- main -----------------------------------------------------------------------

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  let JSDOM, VirtualConsole;
  try {
    ({ JSDOM, VirtualConsole } = require('jsdom'));
  } catch (e) {
    console.error('jsdom is not installed: run `npm install` in tools/ once (tools/package.json lists it)');
    process.exit(2);
  }
  if (opts.build) buildBook();
  if (!fs.existsSync(BOOK_DIR)) {
    console.error('no book/ directory: drop --no-build, or run `mdbook build` first');
    process.exit(2);
  }

  const { window, mermaid } = loadMermaid(JSDOM);
  const scratchDocument = window.document;
  const quiet = new VirtualConsole(); // page DOMs: no jsdom CSS-parse chatter
  let checked = 0;
  let failed = 0;

  for (const html of listHtml(BOOK_DIR)) {
    const rel = relPosix(html);
    const inBook = rel.slice('book/'.length);
    if (REPEAT_PAGES.has(inBook)) continue;
    const pageDom = new JSDOM(fs.readFileSync(html, 'utf8'), { virtualConsole: quiet });
    const nodes = Array.from(pageDom.window.document.querySelectorAll('.mermaid'));
    if (nodes.length === 0) continue;

    let mdRel = 'src/' + inBook.replace(/\.html$/, '.md');
    let mdPath = path.join(ROOT, mdRel);
    if (!fs.existsSync(mdPath) && inBook.endsWith('/index.html')) {
      // mdBook renders a part's README.md as index.html (pass-3 landing pages).
      mdRel = 'src/' + inBook.replace(/index\.html$/, 'README.md');
      mdPath = path.join(ROOT, mdRel);
    }
    let fences = null;
    if (fs.existsSync(mdPath)) fences = mermaidFences(fs.readFileSync(mdPath, 'utf8'));
    else console.error(`warning: ${rel} has diagrams but there is no ${mdRel}; reporting HTML positions`);

    for (let i = 0; i < nodes.length; i++) {
      const text = diagramText(nodes[i], scratchDocument);
      let fence = null;
      if (fences) fence = fences.find((f) => norm(f.body) === norm(text)) || fences[i] || null;
      const where = fence ? `${mdRel}:${fence.line + 1}` : `${rel}:#${i + 1}`;
      checked++;
      let err = null;
      if (text.length > MAX_TEXT_SIZE) {
        err = new Error(`diagram is ${text.length} characters, over mermaid's maxTextSize of ${MAX_TEXT_SIZE}: it renders as the "Maximum text size in diagram exceeded" placeholder`);
      } else {
        try {
          const result = await mermaid.parse(text, { suppressErrors: false });
          if (result && result.diagramType === 'sequence') {
            const dropped = droppedByHashComment(text);
            if (dropped) {
              err = new Error(`"#" starts a comment in sequence diagrams, so mermaid silently drops "${dropped.text}" and the rest of line ${dropped.line}`);
            }
          }
        } catch (e) {
          err = e;
        }
      }
      if (err) {
        failed++;
        console.log(`${where}: ${oneLine(err, fence)}`);
        if (opts.verbose) {
          const full = String((err && err.message) || err).replace(/\r/g, '');
          console.log(full.split('\n').map((l) => '    ' + l).join('\n'));
        }
      }
    }
  }

  console.log(`${checked} diagrams checked, ${failed} failed`);
  process.exit(failed ? 1 : 0);
}

main().catch((e) => {
  console.error((e && e.stack) || e);
  process.exit(2);
});
