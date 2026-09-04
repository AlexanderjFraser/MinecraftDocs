#!/usr/bin/env bash
# Verify names, build the book, deploy to Cloudflare Pages (project `minecraftdocs`, minecraftdocs.dev).
#   tools/deploy.sh            -> production (branch main)
#   tools/deploy.sh preview    -> a preview deployment on branch "preview"
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.cargo/bin:$PATH"
export CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN:-$(tr -d '"\r\n ' < ~/.cloudflare/pvpmod.token)}"
python tools/map_source.py      # the atlas: src/generated/ (tables and SVG figures) from the decompile
python tools/gen_reference.py all   # the eight Reference views, re-read off the decompile
python tools/verify_names.py --index
python tools/check_lanes.py --strict --index   # every lane on every page means what the key says (corpus-wide since pass-3 session P); src/reference/lanes.md regenerated
python tools/check_deps.py --quiet   # the landing pages, the lecture table and the parts-dependency figure agree (fourth gate, pass-4 session A)
mdbook build
node tools/check_mermaid.js --no-build   # every diagram parses under the site's own mermaid (needs `npm install` in tools/ once)
python tools/llms_full.py   # book/llms-full.txt: the whole corpus in one file for agents
wrangler pages deploy book --project-name=minecraftdocs --branch="${1:-main}" --commit-dirty=true
