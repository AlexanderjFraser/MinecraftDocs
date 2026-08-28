#!/usr/bin/env bash
# Verify names, build the book, deploy to Cloudflare Pages (project `minecraftdocs`, minecraftdocs.dev).
#   tools/deploy.sh            -> production (branch main)
#   tools/deploy.sh preview    -> a preview deployment on branch "preview"
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.cargo/bin:$PATH"
export CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN:-$(tr -d '"\r\n ' < ~/.cloudflare/pvpmod.token)}"
python tools/verify_names.py --index
mdbook build
python tools/llms_full.py   # book/llms-full.txt: the whole corpus in one file for agents
wrangler pages deploy book --project-name=minecraftdocs --branch="${1:-main}" --commit-dirty=true
