# Abhishek Prakash — personal website

Source for https://abhishekreally.com.

## Build
```
python3 build.py
```
Output goes to `out/`:
- `out/abhishek-really-site/` — the website (deploy this)
- `out/abhishek-really-netlify.zip` — same, zipped for Netlify drag-and-drop
- `out/abhishek-really.html` — single-file preview

## Preview
```
cd out/abhishek-really-site && python3 -m http.server 8000
```
Then open http://localhost:8000

## Deploy
Netlify → your site → Deploys → drag in `out/abhishek-really-netlify.zip`.
Or connect this folder's Git repo to Netlify; `netlify.toml` runs the build for you.

See **CLAUDE.md** for the full project guide, content facts and design rules.
