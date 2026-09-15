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
    'usage: node tools/check_mermaid.js [--no-build] [--verbose] [--probe]',
    '  --no-build   check the existing book/ instead of running mdbook build first',
    '  --verbose    print the full mermaid error under each failure line',
    '  --probe      prove the caption rule fails on the construct it should, then exit',
  ].join('\n'));
}

function parseArgs(argv) {
  const opts = { build: true, verbose: false, probe: false };
  for (const a of argv) {
    if (a === '--no-build') opts.build = false;
    else if (a === '--build') opts.build = true;
    else if (a === '--verbose' || a === '-v') opts.verbose = true;
    else if (a === '--probe') opts.probe = true;
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
  // Three diagram types (pie, packet-beta, radar-beta) call structuredClone, which Node has and a
  // jsdom window does not; without it they fail to parse here and render fine in the browser.
  if (typeof w.structuredClone !== 'function' && typeof structuredClone === 'function') {
    w.structuredClone = structuredClone;
  }
  // block-beta's parser prints its lexer trace through console.log; keep the report clean.
  for (const k of ['log', 'info', 'debug', 'trace']) w.console[k] = () => {};
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

const norm = (s) => {
  const ls = s.replace(/\r/g, '').split('\n').map((l) => l.trimEnd());
  const indents = ls.filter((l) => l.trim()).map((l) => l.match(/^ */)[0].length);
  const cut = indents.length ? Math.min(...indents) : 0;
  return ls.map((l) => l.slice(cut)).join('\n').trim();
};

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

// Mermaid runs a markdown tokenizer over flowchart and state-diagram labels and
// renders only what it understands (text, strong, em, paragraph, space, html,
// escape); anything else becomes the literal string `Unsupported markdown: <type>`
// in the node, and the *label is gone*. A label line that begins `1. `, `- `, `* `,
// `> ` or a rule is a markdown block, so it is erased — the diagram parses, the
// markdown looks right, and only the render shows it. Sequence-diagram messages do
// not go through this path; measured on both, in Chrome, at the reading column.
// (pass 7, session F — nine labels were live: four on one page's lead figure and
// five of the six nodes on another's.)
const LABEL_BLOCK = /^(\d+[.)]\s|[-*+]\s|>\s|#{1,6}\s)/;
const LABEL_RULE = /^(-{3,}|\*{3,}|_{3,})$/;
function erasedLabels(text, diagramType) {
  if (!/^(flowchart|graph|state)/i.test(String(diagramType || ''))) return [];
  const isState = /^state/i.test(String(diagramType || ''));
  const out = [];
  const lines = text.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^\s*%%/.test(line)) continue;
    const labels = [...line.matchAll(/"([^"]*)"/g)].map((m) => m[1]);
    if (isState) {
      const m = /:\s*(.+)$/.exec(line);
      if (m) labels.push(m[1]);
    }
    for (const label of labels) {
      for (const seg of label.split(/<br\s*\/?>/i)) {
        const t = seg.trim();
        if (LABEL_BLOCK.test(t) || LABEL_RULE.test(t)) out.push({ line: i + 1, text: t.slice(0, 48) });
      }
    }
  }
  return out;
}

// A caption is the italic paragraph after a figure, and `custom.css` styles it
// with `p:has(> em:only-child)` — one <em> and nothing else. An author who closes
// the italics to set a name and reopens them writes *two* <em> children, so the
// rule stops matching: the paragraph loses its styling and its figure number,
// silently, in the built page only. The markdown looks right, mermaid parses
// fine, and nothing but the render ever showed it. (pass 7, session D — thirteen
// of these were live, three of them shipped in Part III.)
function brokenCaption(p) {
  const html = (p.innerHTML || '').trim();
  if (!html.startsWith('<em>') || !html.endsWith('</em>')) return null;
  const body = html.slice(4, -5);
  if (!/<\/?em>/.test(body)) return null;
  const text = (p.textContent || '').replace(/\s+/g, ' ').trim();
  return text.length > 60 ? text.slice(0, 60) + '…' : text;
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

// Prove the caption rule fails on the construct it should and passes the ones it
// should not: the paragraphs below are the shapes a page actually writes.
function runProbe(JSDOM) {
  const cases = [
    ['a caption that closes its italics part-way', '<p><em>The four values of</em> <code>FullChunkStatus</code><em>, and nothing else.</em></p>', true],
    ['a caption that closes its italics around a plain word', '<p><em>the only way back to</em> Free <em>is a behaviour letting go.</em></p>', true],
    ['one italic run with a code span inside it', '<p><em>The shaded band is <code>MinecraftServer.tickChildren</code>, and the rest is bookkeeping.</em></p>', false],
    ['one italic run with a link inside it', '<p><em>Nothing here is light (<a href="x.html">lighting</a>).</em></p>', false],
    ['a plain paragraph after a figure', '<p>Follow the two arrows into <em>the network</em>: they are the whole of it.</p>', false],
    ['a paragraph that is not a caption at all', '<p>Every section below walks one stretch of that diagram.</p>', false],
  ];
  // The erased-label rule, measured in Chrome before it was written: a flowchart or
  // state-diagram label that begins a markdown block is replaced by "Unsupported
  // markdown", a sequence message is not, and a digit-dot that is not at the start
  // of the label is ordinary text.
  const labelCases = [
    ['a flowchart node label numbered "1. "', ['flowchart TD', ' A["1. forgetOutdatedMemories runs first"] --> B["b"]'], 'flowchart-v2', true],
    ['a flowchart node label bulleted "- "', ['flowchart TD', ' A["- one candidate per face"] --> B["b"]'], 'flowchart-v2', true],
    ['a flowchart edge label numbered "1. "', ['flowchart TD', ' A["a"] -- "1. the first answer" --> B["b"]'], 'flowchart-v2', true],
    ['a state transition numbered "1. "', ['stateDiagram-v2', ' S1 --> S2 : 1. the first step'], 'stateDiagram', true],
    ['a second line of a label numbered "2. "', ['flowchart TD', ' A["the phases<br/>2. tickSensors"] --> B["b"]'], 'flowchart-v2', true],
    ['a sequence message numbered "1. "', ['sequenceDiagram', ' A->>B: 1. tryStart, then the duration roll'], 'sequence', false],
    ['a digit-dot with no space after it', ['flowchart TD', ' A["1.forgetOutdatedMemories runs first"] --> B["b"]'], 'flowchart-v2', false],
    ['a digit-dot that is not at the start', ['flowchart TD', ' A["Phase 1. forgetOutdatedMemories"] --> B["b"]'], 'flowchart-v2', false],
    ['an ordinary hyphenated label', ['flowchart TD', ' A["coast-or-interpolate, then applyInput"] --> B["b"]'], 'flowchart-v2', false],
  ];
  let ok = true;
  for (const [what, lines, kind, shouldFail] of labelCases) {
    const got = erasedLabels(lines.join('\n'), kind).length > 0;
    const passed = got === shouldFail;
    ok = ok && passed;
    console.log(`${passed ? 'pass' : 'FAIL'}  ${what} \u2014 ${shouldFail ? 'is' : 'is not'} erased by mermaid`);
  }
  for (const [what, html, shouldFail] of cases) {
    const dom = new JSDOM(`<body><pre class="mermaid">flowchart TD
 A --> B</pre>${html}</body>`);
    const fig = dom.window.document.querySelector('.mermaid');
    const got = brokenCaption(fig.nextElementSibling) !== null;
    const passed = got === shouldFail;
    ok = ok && passed;
    console.log(`${passed ? 'pass' : 'FAIL'}  ${what} — ${shouldFail ? 'is' : 'is not'} a lost caption`);
  }
  console.log(ok ? 'probe passed' : 'PROBE FAILED');
  process.exit(ok ? 0 : 1);
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  let JSDOM, VirtualConsole;
  try {
    ({ JSDOM, VirtualConsole } = require('jsdom'));
  } catch (e) {
    console.error('jsdom is not installed: run `npm install` in tools/ once (tools/package.json lists it)');
    process.exit(2);
  }
  if (opts.probe) return runProbe(JSDOM);
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

    let mdRel = 'src/' + inBook.replace(/\.html$/, '.md');
    let mdPath = path.join(ROOT, mdRel);
    if (!fs.existsSync(mdPath) && inBook.endsWith('/index.html')) {
      // mdBook renders a part's README.md as index.html (pass-3 landing pages).
      mdRel = 'src/' + inBook.replace(/index\.html$/, 'README.md');
      mdPath = path.join(ROOT, mdRel);
    }
    let fences = null;
    if (fs.existsSync(mdPath)) fences = mermaidFences(fs.readFileSync(mdPath, 'utf8'));
    else if (nodes.length) console.error(`warning: ${rel} has diagrams but there is no ${mdRel}; reporting HTML positions`);
    // A mermaid fence inside a *tight* HTML block never converts: it publishes as literal
    // backticks, and a gate that reads only the converted nodes never sees it. An include can
    // add nodes a page has no fence for, so only a shortfall is a failure. (session O)
    if (fences && fences.length > nodes.length) {
      const rendered = nodes.map((n) => norm(diagramText(n, scratchDocument)));
      const short = fences.length - nodes.length;
      const missing = fences.filter((f) => !rendered.includes(norm(f.body)));
      const blame = missing.length === short ? missing : fences.slice(nodes.length);
      for (const f of blame) {
        checked++;
        failed++;
        console.log(`${mdRel}:${f.line + 1}: this \`\`\`mermaid fence did not become a diagram — it publishes as literal backticks. An HTML block ends at a blank line, so a fence inside <figure> or <details> needs a blank line around it.`);
      }
    }
    // Captions: every figure on the page, mermaid blocks and generated SVGs alike.
    const figures = Array.from(pageDom.window.document.querySelectorAll('.mermaid, figure.map'));
    for (const fig of figures) {
      const next = fig.nextElementSibling;
      if (!next || next.tagName !== 'P') continue;
      const lost = brokenCaption(next);
      if (lost) {
        failed++;
        console.log(`${mdRel}: this caption closes its italics part-way through, so it is not styled or numbered as a caption — one italic run, with any name in backticks inside it: “${lost}”`);
      }
    }

    if (nodes.length === 0) continue;

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
          const erased = result ? erasedLabels(text, result.diagramType) : [];
          if (!err && erased.length) {
            const one = erased[0];
            err = new Error(`line ${one.line} is a markdown block, so mermaid replaces the whole label with "Unsupported markdown": “${one.text}”${erased.length > 1 ? ` (and ${erased.length - 1} more in this diagram)` : ''}`);
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

module.exports = { buildBook, listHtml, mermaidFences, norm, entityDecode, dedent, diagramText, markdownLine, relPosix, REPEAT_PAGES, ROOT, BOOK_DIR, MERMAID_JS };

if (require.main === module) {
  main().catch((e) => {
    console.error((e && e.stack) || e);
    process.exit(2);
  });
}
