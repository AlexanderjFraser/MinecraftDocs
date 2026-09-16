#!/usr/bin/env node
/*
 * Every figure as the reader sees it: rendered in a real browser at the column width,
 * screenshotted, and measured.
 *
 * check_mermaid.js proves a diagram parses; nothing before pass 7 ever looked at one
 * rendered. This does: it serves the built book/ over a local port, opens every page that
 * has a figure in the Chrome (or Edge) already installed on the machine — the same engine
 * the site's readers use — waits for mermaid to render, and for each `pre.mermaid` and each
 * generated `figure.map` SVG it writes a PNG of exactly what the column shows and a record
 * of its geometry:
 *
 *   size       the SVG's natural size (its viewBox), the size it is displayed at, and the
 *              scale between them — mermaid shrinks a diagram wider than the column, so a
 *              2,400px flowchart is shown at 0.45 and its 16px labels at 7px
 *   type       the smallest and median effective font size on screen, and how many labels
 *              are under 11px and under 9px
 *   texts      every label with its role (node, edge label, message, note, participant,
 *              cluster, block label), its screen box, and whether it lies outside the box
 *              that is supposed to hold it (a note whose text runs past its rectangle)
 *   overlaps   label boxes that overlap each other, and labels that lie over a shape that
 *              is not their own (an edge label across a node, a note over a message)
 *   edges      edges routed through a node they do not connect, and edge crossings
 *   clipping   anything drawn outside the SVG's own frame, which the browser cuts off
 *   counts     nodes, edges, clusters, participants, messages, notes, blocks, activations
 *
 * The verdict is the browser's: Chrome lays the text out with the site's own CSS and font,
 * so a label that overflows here overflows for a reader. The screenshot is what an agent
 * looks at; the JSON is what pass7_figures.py turns into flags and tables.
 *
 * Usage (from the repo root; needs `npm install` in tools/ once, for playwright-core, and
 * Chrome or Edge installed — playwright-core drives the installed browser and downloads
 * nothing; set FIGURES_BROWSER to an executable to use another Chromium):
 *     node tools/render_figures.js                    # mdbook build, then render everything to render/
 *     node tools/render_figures.js --no-build         # render the existing book/
 *     node tools/render_figures.js --pages systems/world --pages client/the-client-loop
 *     node tools/render_figures.js --theme navy       # the dark palette (light · rust · navy · coal · ayu)
 *     node tools/render_figures.js --width 820        # a narrower column (default 1440: the desktop column)
 *     node tools/render_figures.js --init-js FILE     # try a candidate mermaid-init.js in place of the site's
 *     node tools/render_figures.js --css FILE         # append a candidate stylesheet to custom.css
 *     node tools/render_figures.js --svg              # also save each rendered SVG
 *     node tools/render_figures.js --html FILE        # render one standalone page instead of the book (a gallery of
 *                                                     #   candidate diagrams: tools/pass7/gallery.html); it loads
 *                                                     #   /__root/mermaid.min.js, /__root/mermaid-init.js and
 *                                                     #   /__root/custom.css, so --init-js and --css apply to it too
 *     node tools/render_figures.js --probe            # prove the measurements on synthetic diagrams
 * Writes render/<page>--f<n>.png (mermaid figures, in page order) and render/<page>--m<n>.png
 * (generated SVGs), plus render/index.json with one record per figure: the page, the markdown
 * line of its fence, its diagram type, and every measurement above. render/ is gitignored.
 * Exit 1 if a page failed to render, 2 if the tool could not run.
 */
'use strict';

const fs = require('fs');
const http = require('http');
const path = require('path');
const cm = require('./check_mermaid.js');

const ROOT = cm.ROOT;
const BOOK_DIR = cm.BOOK_DIR;
const DEFAULT_OUT = path.join(ROOT, 'render');
const THEMES = { light: 'light', rust: 'light', navy: 'dark', coal: 'dark', ayu: 'dark' };
const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.woff': 'font/woff', '.woff2': 'font/woff2',
  '.json': 'application/json', '.txt': 'text/plain', '.xml': 'application/xml', '.ico': 'image/x-icon',
};

function usage() {
  console.error([
    'usage: node tools/render_figures.js [--no-build] [--out DIR] [--pages P ...] [--width N] [--scale N]',
    '                                    [--theme light|rust|navy|coal|ayu] [--init-js FILE] [--css FILE]',
    '                                    [--svg] [--quiet] [--probe]',
  ].join('\n'));
}

function parseArgs(argv) {
  const o = { build: true, out: DEFAULT_OUT, pages: [], width: 1440, height: 900, scale: 2, theme: 'light',
              initJs: null, css: null, svg: false, quiet: false, probe: false, html: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => { if (i + 1 >= argv.length) { console.error(`${a} needs a value`); usage(); process.exit(2); } return argv[++i]; };
    if (a === '--no-build') o.build = false;
    else if (a === '--build') o.build = true;
    else if (a === '--out') o.out = path.resolve(next());
    else if (a === '--pages') o.pages.push(next().replace(/\\/g, '/'));
    else if (a === '--width') o.width = Number(next());
    else if (a === '--height') o.height = Number(next());
    else if (a === '--scale') o.scale = Number(next());
    else if (a === '--theme') o.theme = next();
    else if (a === '--init-js') o.initJs = path.resolve(next());
    else if (a === '--css') o.css = path.resolve(next());
    else if (a === '--svg') o.svg = true;
    else if (a === '--quiet' || a === '-q') o.quiet = true;
    else if (a === '--probe') o.probe = true;
    else if (a === '--html') o.html = path.resolve(next());
    else if (a === '--help' || a === '-h') { usage(); process.exit(0); }
    else { console.error(`unknown argument: ${a}`); usage(); process.exit(2); }
  }
  if (!(o.theme in THEMES)) { console.error(`unknown theme ${o.theme}`); process.exit(2); }
  return o;
}

// --- a static server over book/ (plus the repo root's mermaid.min.js and a probe directory) --

function serve(roots) {
  const server = http.createServer((req, res) => {
    let url = decodeURIComponent(req.url.split('?')[0]);
    if (url.endsWith('/')) url += 'index.html';
    for (const { prefix, dir } of roots) {
      if (!url.startsWith(prefix)) continue;
      const file = path.join(dir, url.slice(prefix.length));
      if (!file.startsWith(dir) || !fs.existsSync(file) || !fs.statSync(file).isFile()) continue;
      res.writeHead(200, { 'Content-Type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
      return;
    }
    res.writeHead(404); res.end('not found');
  });
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve({ server, port: server.address().port })));
}

// --- the source text of each block in a built page, in DOM order ---------------------------

function decode(html) {
  return html.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'").replace(/&amp;/g, '&');
}

function blocksInHtml(html) {
  const out = [];
  const re = /<pre class="mermaid">([\s\S]*?)<\/pre>/g;
  let m;
  while ((m = re.exec(html))) out.push(decode(m[1]));
  return out;
}

function mdFor(inBook) {
  let mdRel = 'src/' + inBook.replace(/\.html$/, '.md');
  if (!fs.existsSync(path.join(ROOT, mdRel)) && inBook.endsWith('/index.html')) {
    mdRel = 'src/' + inBook.replace(/index\.html$/, 'README.md');
  }
  return fs.existsSync(path.join(ROOT, mdRel)) ? mdRel : null;
}

function slugOf(mdRel) {
  return mdRel.replace(/^src\//, '').replace(/^systems\//, '').replace(/\.md$/, '').replace(/\//g, '--');
}

// --- what runs inside the page --------------------------------------------------------------

// Everything below is evaluated in the browser. It returns, per figure, the geometry in screen
// pixels (what the reader sees at this viewport) and the derived flags.
function measureAll() {
  const rectOf = (el) => { const r = el.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; };
  const area = (b) => b.w * b.h;
  const inter = (a, b) => {
    const x = Math.max(a.x, b.x), y = Math.max(a.y, b.y);
    const X = Math.min(a.x + a.w, b.x + b.w), Y = Math.min(a.y + a.h, b.y + b.h);
    return X > x && Y > y ? (X - x) * (Y - y) : 0;
  };
  const contains = (a, b, tol) => b.x >= a.x - tol && b.y >= a.y - tol && b.x + b.w <= a.x + a.w + tol && b.y + b.h <= a.y + a.h + tol;
  const inside = (b, p, inset) => p.x > b.x + inset && p.x < b.x + b.w - inset && p.y > b.y + inset && p.y < b.y + b.h - inset;
  const near = (p, q, d) => Math.abs(p.x - q.x) <= d && Math.abs(p.y - q.y) <= d;
  const clean = (s) => (s || '').replace(/\s+/g, ' ').trim().slice(0, 160);
  const segCross = (p1, p2, p3, p4) => {
    const d = (p2.x - p1.x) * (p4.y - p3.y) - (p2.y - p1.y) * (p4.x - p3.x);
    if (Math.abs(d) < 1e-9) return null;
    const t = ((p3.x - p1.x) * (p4.y - p3.y) - (p3.y - p1.y) * (p4.x - p3.x)) / d;
    const u = ((p3.x - p1.x) * (p2.y - p1.y) - (p3.y - p1.y) * (p2.x - p1.x)) / d;
    if (t <= 0 || t >= 1 || u <= 0 || u >= 1) return null;
    return { x: p1.x + t * (p2.x - p1.x), y: p1.y + t * (p2.y - p1.y) };
  };

  function roleOf(el) {
    const c = el.getAttribute('class') || '';
    if (/messageText/.test(c)) return 'message';
    if (/noteText/.test(c)) return 'note';
    if (/loopText|labelText/.test(c)) return 'block';
    if (/sequenceNumber/.test(c)) return 'seqnum';
    if (/\bactor\b/.test(c)) return 'participant';
    if (el.closest('g.edgeLabel, g.edgeLabels')) return 'edgeLabel';
    if (el.closest('g.cluster')) return 'cluster';
    if (el.closest('g.node')) return 'node';
    if (el.closest('g.stateGroup')) return 'state';
    if (/\btitle\b|titleText/.test(c)) return 'title';
    return 'text';
  }

  // The box a label is supposed to sit inside, if any: its node's shape, its note's rect, the
  // participant's box, a loop's label polygon.
  function containerOf(el, role) {
    let g = null;
    if (role === 'node' || role === 'edgeLabel' || role === 'cluster' || role === 'state') {
      g = el.closest('g.node, g.edgeLabel, g.cluster, g.stateGroup');
      if (!g) return null;
      const shape = g.querySelector(':scope > rect, :scope > polygon, :scope > circle, :scope > ellipse, :scope > path, :scope > g > rect, :scope > g > polygon, :scope > g > path, :scope > g > circle');
      return shape ? { el: shape, box: rectOf(shape) } : null;
    }
    if (role === 'note') {
      const p = el.parentElement;
      const r = p && p.querySelector('rect.note');
      return r ? { el: r, box: rectOf(r) } : null;
    }
    if (role === 'participant') {
      const p = el.parentElement;
      const r = p && (p.querySelector('rect.actor, rect.actor-top, rect.actor-bottom') || p.querySelector('rect'));
      return r ? { el: r, box: rectOf(r) } : null;
    }
    if (role === 'block') {
      // the label box polygon is the previous sibling of the loop label text
      let s = el.previousElementSibling;
      while (s && !(s.tagName.toLowerCase() === 'polygon' && /labelBox/.test(s.getAttribute('class') || ''))) s = s.previousElementSibling;
      return s ? { el: s, box: rectOf(s) } : null;
    }
    return null;
  }

  function fontOf(el) {
    let probe = el;
    if (el.tagName.toLowerCase() === 'foreignobject') {
      probe = el.querySelector('p, span, div') || el;
      // the innermost element with its own text decides the size
      const deep = el.querySelector('p') || el.querySelector('span.nodeLabel, span.edgeLabel, span') || probe;
      probe = deep;
    } else {
      const ts = el.querySelector('tspan');
      if (ts) probe = ts;
    }
    return parseFloat(getComputedStyle(probe).fontSize) || 16;
  }

  function samplePath(svg, el) {
    let L = 0;
    try { L = el.getTotalLength(); } catch (e) { return []; }
    if (!L || !isFinite(L)) return [];
    const n = Math.max(8, Math.min(240, Math.ceil(L / 5)));
    const ctm = el.getScreenCTM();
    const pts = [];
    for (let k = 0; k <= n; k++) {
      const p = el.getPointAtLength((L * k) / n);
      const q = svg.createSVGPoint(); q.x = p.x; q.y = p.y;
      const s = ctm ? q.matrixTransform(ctm) : q;
      pts.push({ x: s.x, y: s.y });
    }
    return pts;
  }

  function measureSvg(svg, kind, index) {
    const R = rectOf(svg);
    const vb = svg.viewBox && svg.viewBox.baseVal;
    let natural = vb && vb.width ? { w: vb.width, h: vb.height } : null;
    if (!natural) { try { const b = svg.getBBox(); natural = { w: b.width, h: b.height }; } catch (e) { natural = { w: R.w, h: R.h }; } }
    const scale = natural.w ? R.w / natural.w : 1;
    const diagram = svg.getAttribute('aria-roledescription') || (kind === 'map' ? 'map' : 'unknown');

    // --- labels ---
    const textEls = [];
    svg.querySelectorAll('text').forEach((t) => { if (t.closest('foreignObject')) return; if (clean(t.textContent)) textEls.push(t); });
    svg.querySelectorAll('foreignObject').forEach((fo) => { if (clean(fo.textContent)) textEls.push(fo); });
    const texts = textEls.map((el) => {
      const role = roleOf(el);
      const font = fontOf(el);
      const cont = containerOf(el, role);
      const box = rectOf(el);
      const group = el.closest('g.node, g.edgeLabel, g.cluster, g.stateGroup') || (role === 'note' || role === 'participant' ? el.parentElement : null);
      return { el, role, text: clean(el.textContent), box, font, eff: font * scale, group,
               // a loop/alt/par/opt label is drawn by mermaid across its own frame's edge on every figure
               // that has one, so it is the device's layout, not a label escaping its box (pass 7, O)
               container: cont, outside: cont && role !== 'block' ? !contains(cont.box, box, 2) : false };
    });

    // --- shapes ---
    const nodes = [];
    svg.querySelectorAll('g.node').forEach((g) => {
      const shape = g.querySelector(':scope > rect, :scope > polygon, :scope > circle, :scope > ellipse, :scope > path, :scope > g > rect, :scope > g > polygon, :scope > g > path, :scope > g > circle') || g;
      nodes.push({ el: g, id: g.id || '', box: rectOf(shape), label: clean(g.textContent) });
    });
    const clusters = [...svg.querySelectorAll('g.cluster')].map((g) => ({ el: g, box: rectOf(g.querySelector('rect') || g), label: clean(g.querySelector('.cluster-label, text') ? g.querySelector('.cluster-label, text').textContent : '') }));
    const actorRects = [...svg.querySelectorAll('rect.actor, rect.actor-top, rect.actor-bottom')];
    const noteRects = [...svg.querySelectorAll('rect.note')];
    const activations = [...svg.querySelectorAll('rect[class*="activation"]')];
    const labelBoxes = [...svg.querySelectorAll('polygon.labelBox')];
    const lifelines = [...svg.querySelectorAll('line.actor-line')];
    const messages = [...svg.querySelectorAll('line[class*="messageLine"], path[class*="messageLine"]')];
    const participants = new Set([...svg.querySelectorAll('text.actor, text[class*="actor"]')].map((t) => clean(t.textContent)).filter(Boolean));
    const edgeEls = [...new Set([...svg.querySelectorAll('path.flowchart-link, path.transition, g.edgePaths path, g.edgePath path, path.edge-thickness-normal, path.edge-thickness-thick, path[class*="edge-pattern"]')])];
    const edges = edgeEls.map((el, i) => ({ el, i, pts: samplePath(svg, el), id: el.id || '' }));

    // shapes a label may wrongly sit over: nodes, participants, notes, block labels (not clusters, which contain nodes by design)
    const obstacles = [
      ...nodes.map((n) => ({ el: n.el, box: n.box, kind: 'node', label: n.label })),
      ...actorRects.map((r) => ({ el: r, box: rectOf(r), kind: 'participant', label: '' })),
      ...noteRects.map((r) => ({ el: r, box: rectOf(r), kind: 'note', label: '' })),
      ...labelBoxes.map((r) => ({ el: r, box: rectOf(r), kind: 'block', label: '' })),
    ];
    const activationBoxes = activations.map((r) => ({ el: r, box: rectOf(r) }));

    // --- flags ---
    const textOverlaps = [];
    for (let i = 0; i < texts.length; i++) {
      for (let j = i + 1; j < texts.length; j++) {
        const a = texts[i], b = texts[j];
        if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
        if (a.group && a.group === b.group) continue;
        const ov = inter(a.box, b.box);
        if (ov > 0.1 * Math.min(area(a.box), area(b.box)) && ov > 4) {
          textOverlaps.push({ a: a.text, ra: a.role, b: b.text, rb: b.role, area: Math.round(ov) });
        }
      }
    }
    const textOverShape = [];
    const textOverActivation = [];
    for (const t of texts) {
      for (const o of obstacles) {
        if (t.container && t.container.el === o.el) continue;
        if (o.el.contains(t.el) || (t.group && (t.group === o.el || t.group.contains(o.el) || o.el.contains(t.group)))) continue;
        if (t.role === 'note' && o.kind === 'note' && t.el.parentElement && t.el.parentElement.contains(o.el)) continue;
        if (t.role === 'participant' && o.kind === 'participant' && t.el.parentElement && t.el.parentElement.contains(o.el)) continue;
        const ov = inter(t.box, o.box);
        if (ov > 0.1 * area(t.box) && ov > 4) textOverShape.push({ text: t.text, role: t.role, over: o.kind, label: o.label, area: Math.round(ov) });
      }
      if (t.role === 'message' || t.role === 'note' || t.role === 'block') {
        for (const a of activationBoxes) {
          const ov = inter(t.box, a.box);
          if (ov > 4) textOverActivation.push({ text: t.text, role: t.role, area: Math.round(ov) });
        }
      }
    }
    // a lifeline through a message label: mermaid draws it under the text, so it is a count, not a defect
    let lifelinesThroughText = 0;
    if (lifelines.length) {
      const xs = lifelines.map((l) => rectOf(l).x);
      for (const t of texts) if (t.role === 'message') for (const x of xs) if (x > t.box.x + 2 && x < t.box.x + t.box.w - 2) lifelinesThroughText++;
    }

    const edgeThroughNode = [];
    let crossings = 0;
    const crossingPairs = [];
    if (edges.length && nodes.length) {
      for (const e of edges) {
        if (e.pts.length < 2) continue;
        const first = e.pts[0], last = e.pts[e.pts.length - 1];
        const ends = nodes.filter((n) => inside(n.box, first, -6) || inside(n.box, last, -6));
        for (const n of nodes) {
          if (ends.includes(n)) continue;
          if (e.pts.some((p) => inside(n.box, p, 3))) { edgeThroughNode.push({ edge: e.id || String(e.i), node: n.label.slice(0, 60) }); break; }
        }
      }
    }
    if (edges.length > 1) {
      for (let i = 0; i < edges.length; i++) {
        for (let j = i + 1; j < edges.length; j++) {
          const A = edges[i].pts, B = edges[j].pts;
          if (A.length < 2 || B.length < 2) continue;
          let found = null;
          outer: for (let a = 0; a + 1 < A.length; a++) {
            for (let b = 0; b + 1 < B.length; b++) {
              const x = segCross(A[a], A[a + 1], B[b], B[b + 1]);
              if (!x) continue;
              const endsA = near(x, A[0], 6) || near(x, A[A.length - 1], 6);
              const endsB = near(x, B[0], 6) || near(x, B[B.length - 1], 6);
              if (endsA || endsB) continue;   // two edges meeting at a node, not a crossing
              found = x; break outer;
            }
          }
          if (found) { crossings++; if (crossingPairs.length < 20) crossingPairs.push([edges[i].id || String(i), edges[j].id || String(j)]); }
        }
      }
    }

    // anything outside the SVG's own frame is cut off by the browser
    const clipped = [];
    const frame = { x: R.x, y: R.y, w: R.w, h: R.h };
    for (const t of texts) if (!contains(frame, t.box, 1.5)) clipped.push({ what: 'label', role: t.role, text: t.text });
    for (const o of obstacles) if (!contains(frame, o.box, 1.5)) clipped.push({ what: o.kind, text: o.label.slice(0, 60) });

    const effs = texts.map((t) => t.eff).sort((a, b) => a - b);
    const median = effs.length ? effs[Math.floor(effs.length / 2)] : null;
    const longest = texts.reduce((m, t) => (t.text.length > m ? t.text.length : m), 0);

    return {
      kind, index, diagram,
      natural: { w: Math.round(natural.w), h: Math.round(natural.h) },
      display: { w: Math.round(R.w), h: Math.round(R.h) },
      scale: Math.round(scale * 1000) / 1000,
      fonts: { min: effs.length ? Math.round(effs[0] * 10) / 10 : null, median: median != null ? Math.round(median * 10) / 10 : null,
               under11: effs.filter((e) => e < 11).length, under9: effs.filter((e) => e < 9).length, labels: effs.length },
      counts: { nodes: nodes.length, edges: edges.length, clusters: clusters.length, participants: participants.size,
                messages: messages.length, notes: noteRects.length, blocks: labelBoxes.length, activations: activations.length,
                labels: texts.length, longestLabel: longest },
      flags: {
        textOverlaps, textOverShape, textOverActivation, lifelinesThroughText,
        textOutsideContainer: texts.filter((t) => t.outside).map((t) => ({ role: t.role, text: t.text })),
        edgeThroughNode, crossings, crossingPairs, clipped,
      },
      texts: texts.slice(0, 400).map((t) => ({ role: t.role, text: t.text, eff: Math.round(t.eff * 10) / 10,
                                                 box: { x: Math.round(t.box.x - R.x), y: Math.round(t.box.y - R.y), w: Math.round(t.box.w), h: Math.round(t.box.h) } })),
    };
  }

  const main = document.querySelector('.content main') || document.querySelector('main') || document.body;
  const out = { column: main.clientWidth, figures: [] };
  document.querySelectorAll('pre.mermaid').forEach((pre, i) => {
    const svg = pre.querySelector('svg');
    if (!svg) { out.figures.push({ kind: 'mermaid', index: i, error: clean(pre.textContent).slice(0, 200) || 'no svg rendered' }); return; }
    const err = svg.querySelector('.error-text, .error-icon');
    if (err) { out.figures.push({ kind: 'mermaid', index: i, error: clean(svg.textContent).slice(0, 200) }); return; }
    out.figures.push(measureSvg(svg, 'mermaid', i));
  });
  document.querySelectorAll('figure.map svg').forEach((svg, i) => out.figures.push(measureSvg(svg, 'map', i)));
  return out;
}

// --- driving the browser --------------------------------------------------------------------

async function launch() {
  let chromium;
  try { ({ chromium } = require('playwright-core')); }
  catch (e) { console.error('playwright-core is not installed: run `npm install` in tools/ once (tools/package.json lists it)'); process.exit(2); }
  const tries = [];
  if (process.env.FIGURES_BROWSER) tries.push({ executablePath: process.env.FIGURES_BROWSER });
  tries.push({ channel: 'chrome' }, { channel: 'msedge' }, { channel: 'chromium' });
  let lastErr = null;
  for (const t of tries) {
    try { return await chromium.launch({ headless: true, ...t }); } catch (e) { lastErr = e; }
  }
  console.error('no Chrome, Edge or Chromium found to drive (set FIGURES_BROWSER to an executable): ' + (lastErr && lastErr.message));
  process.exit(2);
}

// mdBook's sticky menu bar and its page-turn chevrons are fixed to the viewport, so an element
// screenshot of a figure taller than the window would carry them across the picture. Hidden,
// not removed: the layout must stay what the reader gets.
const HIDE_CHROME = '#mdbook-menu-bar, #menu-bar, .menu-bar, .nav-chapters, .nav-wrapper, .nav-wide-wrapper, .sidebar-resize-handle { visibility: hidden !important; }';

async function renderPage(page, url, opts) {
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  await page.waitForFunction(
    () => [...document.querySelectorAll('pre.mermaid')].every((p) => p.getAttribute('data-processed') === 'true'),
    null, { timeout: 45000 });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.addStyleTag({ content: HIDE_CHROME });
  await page.waitForTimeout(80);
  const data = await page.evaluate(measureAll);
  const svgs = await page.$$('pre.mermaid svg');
  const maps = await page.$$('figure.map svg');
  return { data, svgs, maps };
}

function setupContext(browser, opts) {
  return browser.newContext({
    viewport: { width: opts.width, height: opts.height },
    deviceScaleFactor: opts.scale,
    colorScheme: THEMES[opts.theme] === 'dark' ? 'dark' : 'light',
  }).then(async (ctx) => {
    await ctx.addInitScript((theme) => {
      try { localStorage.setItem('mdbook-theme', theme); localStorage.setItem('mdbook-sidebar', 'visible'); } catch (e) { /* private mode */ }
    }, opts.theme);
    if (opts.initJs) {
      const body = fs.readFileSync(opts.initJs, 'utf8');
      await ctx.route(/mermaid-init(-[0-9a-f]+)?\.js$/, (route) => route.fulfill({ contentType: 'application/javascript', body }));
    }
    if (opts.css) {
      const extra = fs.readFileSync(opts.css, 'utf8');
      await ctx.route(/custom(-[0-9a-f]+)?\.css$/, async (route) => {
        const resp = await route.fetch();
        const body = (await resp.text()) + '\n/* --css candidate */\n' + extra;
        route.fulfill({ contentType: 'text/css', body });
      });
    }
    return ctx;
  });
}

// One standalone HTML page (a gallery of candidate diagrams) rendered the way a book page is:
// its mermaid blocks screenshotted and measured into <out>/<stem>--f<n>.png and <stem>.json.
async function renderHtml(opts) {
  const dir = path.dirname(opts.html);
  const base = path.basename(opts.html);
  const stem = base.replace(/\.html?$/, '');
  fs.mkdirSync(opts.out, { recursive: true });
  const { server, port } = await serve([{ prefix: '/__root/', dir: ROOT }, { prefix: '/__probe/', dir }]);
  const browser = await launch();
  const ctx = await setupContext(browser, opts);
  const page = await ctx.newPage();
  page.on('pageerror', (e) => console.error(`  page error: ${e.message.split('\n')[0]}`));
  const { data, svgs } = await renderPage(page, `http://127.0.0.1:${port}/__probe/${base}`, opts);
  const sources = blocksInHtml(fs.readFileSync(opts.html, 'utf8'));
  const records = [];
  let fi = 0;
  for (const fig of data.figures) {
    if (fig.kind !== 'mermaid') continue;
    const png = path.join(opts.out, `${stem}--f${fig.index + 1}.png`);
    const handle = svgs[fi++];
    if (handle && !fig.error) await handle.screenshot({ path: png, type: 'png' });
    const src = sources[fig.index] || '';
    records.push({ id: `${stem}--f${fig.index + 1}`, first_line: (src.split('\n').find((l) => l.trim()) || '').trim().slice(0, 80),
                   png: fig.error ? null : cm.relPosix(png), ...fig });
    console.log(`${fig.error ? 'FAIL' : 'ok  '}  f${fig.index + 1}  ${fig.diagram || ''}  ${fig.error || `${fig.natural.w}x${fig.natural.h} scale ${fig.scale} min type ${fig.fonts.min}px`}`);
  }
  await browser.close();
  server.close();
  fs.writeFileSync(path.join(opts.out, `${stem}.json`), JSON.stringify({ html: cm.relPosix(opts.html), records }, null, 1), 'utf8');
  console.log(`${records.length} figures rendered to ${cm.relPosix(opts.out)}/`);
  process.exit(records.some((r) => r.error) ? 1 : 0);
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.probe) return probe(opts);
  if (opts.html) return renderHtml(opts);
  if (opts.build) cm.buildBook();
  if (!fs.existsSync(BOOK_DIR)) { console.error('no book/ directory: drop --no-build, or run `mdbook build` first'); process.exit(2); }
  fs.mkdirSync(opts.out, { recursive: true });

  const { server, port } = await serve([{ prefix: '/__root/', dir: ROOT }, { prefix: '/', dir: BOOK_DIR }]);
  const browser = await launch();
  const ctx = await setupContext(browser, opts);
  const page = await ctx.newPage();
  page.on('pageerror', (e) => { if (!opts.quiet) console.error(`  page error: ${e.message.split('\n')[0]}`); });

  const records = [];
  let pagesDone = 0, failed = 0, figures = 0;
  const t0 = Date.now();
  for (const html of cm.listHtml(BOOK_DIR)) {
    const inBook = cm.relPosix(html).slice('book/'.length);
    if (cm.REPEAT_PAGES.has(inBook)) continue;
    const raw = fs.readFileSync(html, 'utf8');
    if (!/class="mermaid"|<figure class="map"/.test(raw)) continue;
    const mdRel = mdFor(inBook);
    const label = mdRel || `book/${inBook}`;
    if (opts.pages.length && !opts.pages.some((p) => label.includes(p))) continue;
    const slug = mdRel ? slugOf(mdRel) : inBook.replace(/\.html$/, '').replace(/\//g, '--');
    const fences = mdRel ? cm.mermaidFences(fs.readFileSync(path.join(ROOT, mdRel), 'utf8')) : [];
    const sources = blocksInHtml(raw);

    let result;
    try {
      result = await renderPage(page, `http://127.0.0.1:${port}/${inBook}`, opts);
    } catch (e) {
      failed++;
      console.log(`FAIL ${label}: ${e.message.split('\n')[0]}`);
      continue;
    }
    const { data, svgs, maps } = result;
    let fi = 0, mi = 0;
    for (const fig of data.figures) {
      let rec;
      if (fig.kind === 'mermaid') {
        const src = sources[fig.index] || '';
        const fence = fences.find((f) => cm.norm(f.body) === cm.norm(src)) || fences[fig.index] || null;
        const png = path.join(opts.out, `${slug}--f${fig.index + 1}.png`);
        const handle = svgs[fi++];
        if (handle && !fig.error) {
          try { await handle.screenshot({ path: png, type: 'png' }); } catch (e) { fig.screenshotError = e.message.split('\n')[0]; }
        }
        rec = { page: mdRel, slug, n: fig.index + 1, id: `${slug}--f${fig.index + 1}`, fence_line: fence ? fence.line : null,
                source_first_line: (src.split('\n').find((l) => l.trim()) || '').trim().slice(0, 60),
                png: fig.error ? null : cm.relPosix(png), ...fig };
        if (opts.svg && handle && !fig.error) {
          const svgPath = png.replace(/\.png$/, '.svg');
          fs.writeFileSync(svgPath, await handle.evaluate((el) => el.outerHTML), 'utf8');
          rec.svg = cm.relPosix(svgPath);
        }
      } else {
        const png = path.join(opts.out, `${slug}--m${fig.index + 1}.png`);
        const handle = maps[mi++];
        if (handle) { try { await handle.screenshot({ path: png, type: 'png' }); } catch (e) { fig.screenshotError = e.message.split('\n')[0]; } }
        rec = { page: mdRel, slug, n: fig.index + 1, id: `${slug}--m${fig.index + 1}`, fence_line: null, png: cm.relPosix(png), ...fig };
      }
      delete rec.el;
      records.push(rec);
      figures++;
    }
    pagesDone++;
    if (!opts.quiet) {
      const bad = data.figures.filter((f) => f.error).length;
      const warn = data.figures.filter((f) => f.flags && (f.flags.textOverlaps.length || f.flags.textOutsideContainer.length || f.flags.clipped.length || f.flags.edgeThroughNode.length)).length;
      console.log(`${String(data.figures.length).padStart(2)} figures${bad ? `  ${bad} FAILED` : ''}${warn ? `  ${warn} flagged` : ''}  column ${data.column}px  ${label}`);
    }
  }
  await browser.close();
  server.close();

  const index = { generated: new Date().toISOString(), width: opts.width, scale: opts.scale, theme: opts.theme,
                  initJs: opts.initJs, css: opts.css, pages: pagesDone, figures: records.length, records };
  fs.writeFileSync(path.join(opts.out, 'index.json'), JSON.stringify(index, null, 1), 'utf8');
  const secs = Math.round((Date.now() - t0) / 100) / 10;
  console.log(`${records.length} figures on ${pagesDone} pages rendered to ${cm.relPosix(opts.out)}/ in ${secs}s` +
              (failed ? `; ${failed} pages FAILED to render` : ''));
  process.exit(failed ? 1 : 0);
}

// --- the probe --------------------------------------------------------------------------------

const PROBE_HTML = `<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{margin:0;padding:20px;font-family:sans-serif} .content main{width:1100px} pre.mermaid{max-width:100%}</style>
</head><body><div class="content"><main>
<p>1. a note whose text runs out of its box, and a message label across an activation</p>
<pre class="mermaid">sequenceDiagram
    participant A as Alpha
    participant B as Beta
    participant C as Gamma
    A->>B: first
    activate B
    A->>C: a message that crosses the middle lane while it is active
    Note over A,B: a note whose text is far too long for the box mermaid draws for it because notes do not wrap and this one keeps going well past the right-hand edge of the two lanes it sits over
    deactivate B
</pre>
<p>2. four edges that must cross once (K2,2)</p>
<pre class="mermaid">flowchart TD
    A["A"] --> C["C"]
    A --> D["D"]
    B["B"] --> C
    B --> D
</pre>
<p>3. a chain too wide for the column, so its labels shrink</p>
<pre class="mermaid">flowchart LR
    N1["a long step label"] --> N2["a long step label"] --> N3["a long step label"] --> N4["a long step label"] --> N5["a long step label"] --> N6["a long step label"] --> N7["a long step label"] --> N8["a long step label"] --> N9["a long step label"] --> N10["a long step label"] --> N11["a long step label"] --> N12["a long step label"] --> N13["a long step label"] --> N14["a long step label"]
</pre>
<p>4. clean</p>
<pre class="mermaid">flowchart TD
    A["one"] --> B["two"]
    B --> C{"three?"}
</pre>
<p>5. an edge routed through a node it does not connect</p>
<pre class="mermaid">flowchart LR
    A["A"] --> B["B"] --> C["C"]
    A --> C
</pre>
</main></div>
<script src="/__root/mermaid.min.js"></script>
<script>mermaid.initialize({ startOnLoad: true, theme: 'default' });</script>
</body></html>`;

async function probe(opts) {
  const dir = path.join(opts.out, '_probe');
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'probe.html'), PROBE_HTML, 'utf8');
  const { server, port } = await serve([{ prefix: '/__root/', dir: ROOT }, { prefix: '/__probe/', dir }]);
  const browser = await launch();
  const ctx = await setupContext(browser, { ...opts, initJs: null, css: null });
  const page = await ctx.newPage();
  const { data, svgs } = await renderPage(page, `http://127.0.0.1:${port}/__probe/probe.html`, opts);
  for (let i = 0; i < svgs.length; i++) await svgs[i].screenshot({ path: path.join(dir, `probe--f${i + 1}.png`) });
  await browser.close();
  server.close();
  const f = data.figures;
  const checks = [
    ['1: the long note is flagged as text outside its box', f[0] && f[0].flags && f[0].flags.textOutsideContainer.some((t) => t.role === 'note')],
    ['1: the message across the active lane is flagged over an activation', f[0] && f[0].flags && f[0].flags.textOverActivation.length > 0],
    ['2: K2,2 has one crossing', f[1] && f[1].flags && f[1].flags.crossings === 1],
    ['3: the wide chain is shrunk below 0.7 and its smallest label is under 11px', f[2] && f[2].scale < 0.7 && f[2].fonts.min < 11],
    ['4: the clean figure has no overlap, no crossing, no clipping, no small text', f[3] && f[3].flags && f[3].flags.textOverlaps.length === 0 && f[3].flags.crossings === 0 && f[3].flags.clipped.length === 0 && f[3].flags.textOutsideContainer.length === 0 && f[3].fonts.min >= 11],
    ['5: the A→C edge is either routed through B or counted as a crossing/through-node (mermaid routes around it, so this checks the detector runs)', f[4] && f[4].flags && Array.isArray(f[4].flags.edgeThroughNode)],
    ['every figure got a diagram type from the browser', f.every((x) => x.diagram && x.diagram !== 'unknown')],
  ];
  let ok = true;
  for (const [what, pass] of checks) { console.log(`${pass ? 'pass' : 'FAIL'}  ${what}`); if (!pass) ok = false; }
  fs.writeFileSync(path.join(dir, 'probe.json'), JSON.stringify(data, null, 1), 'utf8');
  console.log(ok ? `probe passed; screenshots and probe.json in ${cm.relPosix(dir)}/` : 'PROBE FAILED');
  process.exit(ok ? 0 : 1);
}

if (require.main === module) {
  main().catch((e) => { console.error((e && e.stack) || e); process.exit(2); });
}
