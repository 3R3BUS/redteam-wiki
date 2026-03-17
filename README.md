# Vantablack Wiki — Static Site

Comprehensive red team & offensive security reference. 69+ articles, 24 categories.

## Deploy to Cloudflare Pages

### Option A — Drag & Drop (instant)
1. Run `python3 build.py` to generate `index.html`
2. Go to [Cloudflare Pages](https://pages.cloudflare.com) → Create a project → Direct Upload
3. Drag `index.html`, `_headers`, `_redirects` into the upload zone
4. Done — live in seconds

### Option B — Git integration (auto-deploy on push)
1. Push this directory to a GitHub/GitLab repo
2. Cloudflare Pages → New project → Connect Git repo
3. Build settings:
   - **Build command**: `python3 build.py`
   - **Output directory**: `/` (same dir as build.py)
   - **Root directory**: `wiki/` (if monorepo)
4. Every push auto-rebuilds and deploys

### Option C — Wrangler CLI
```bash
npm install -g wrangler
python3 build.py
wrangler pages deploy . --project-name vantablack-wiki
```

## Local development
```bash
python3 build.py
python3 -m http.server 8080
# open http://localhost:8080
```

## Regenerate after wiki updates
```bash
cd /home/erebus/wiki
python3 build.py
```
The `build.py` script reads all markdown from `../custom-c2/server/docs/` and embeds them into a self-contained `index.html`.
