#!/usr/bin/env bash
# Verify names, build the book, deploy to Cloudflare Pages (project `minecraftdocs`, minecraftdocs.dev).
#   tools/deploy.sh            -> production (branch main)
#   tools/deploy.sh preview    -> a preview deployment on branch "preview"
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.cargo/bin:$PATH"
export CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN:-$(tr -d '"\r\n ' < ~/.cloudflare/pvpmod.token)}"
python tools/map_source.py      # the atlas: src/generated/ (tables and SVG figures) from the decompile
python tools/gen_reference.py all   # the eleven Reference views, re-read off the decompile
python tools/pass5_coverage.py --write   # the thirteen coverage phrases, src/generated/coverage-<dir>.md, from the same PARTS mapping the size phrases use (pass-6 planning session)
python tools/check_deps.py --write-figure   # the parts-dependency figure and its table, src/generated/parts-dependency.*, from the landing pages (pass 7, session N)
python tools/verify_names.py --index
python tools/check_lanes.py --strict --index --unused   # every lane on every page means what the key says (corpus-wide since pass-3 session P); src/reference/lanes.md regenerated; key rows no page declares reported, not failed (pass 7, session O)
python tools/check_figure_names.py --strict   # every name inside a mermaid block resolves (sixth gate: report-only from pass 7's planning session, --strict from its close)
python tools/check_deps.py --quiet   # the landing pages, the lecture table and the parts-dependency figure agree (fourth gate, pass-4 session A)
python tools/check_links.py --quiet  # every internal link, anchor, include, SUMMARY entry and redirect resolves (fifth gate, pass-5 planning session)
mdbook build
node tools/check_mermaid.js --no-build   # every diagram parses under the site's own mermaid (needs `npm install` in tools/ once)
python tools/llms_full.py   # book/llms-full.txt: the whole corpus in one file for agents
python tools/site_index.py   # book/sitemap.xml (for search engines; src/robots.txt points at it) and book/llms.txt (the index form, one line per page)
wrangler pages deploy book --project-name=minecraftdocs --branch="${1:-main}" --commit-dirty=true
