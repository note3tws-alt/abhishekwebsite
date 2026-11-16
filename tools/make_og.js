// Regenerates the social share card src/brand/og-image.jpg (1200x630) used for og:image / twitter:image.
// Needs Node + Playwright: npm i -D playwright && npx playwright install chromium && node tools/make_og.js
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const D = path.join(__dirname, '..', 'src');
  const face = 'data:image/webp;base64,' + fs.readFileSync(path.join(D, 'photos', 'abhishek-headshot.webp')).toString('base64');
  const mark = fs.readFileSync(path.join(D, 'brand', 'mark.svg'), 'utf8').replace('<svg ', '<svg width="64" height="64" ');
  const html = `<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#0b0b0d;color:#fff;font-family:'Plus Jakarta Sans',sans-serif;position:relative;overflow:hidden}
.frame{position:absolute;inset:28px;border:1px solid rgba(255,255,255,.12);border-radius:4px}
.txt{position:absolute;left:84px;top:80px;width:640px}
.brand{display:flex;align-items:center;gap:16px;font-weight:700;font-size:22px;color:rgba(255,255,255,.75)}
h1{font-size:76px;line-height:1;letter-spacing:-.045em;font-weight:800;margin-top:56px}
p{font-size:28px;line-height:1.35;color:rgba(255,255,255,.72);margin-top:26px;font-weight:500}
.pill{display:inline-block;margin-top:40px;background:#dfff4f;color:#0e0e10;font-weight:700;font-size:22px;padding:12px 22px;border-radius:999px}
.arch{position:absolute;right:84px;bottom:28px;width:380px;height:470px;border-radius:190px 190px 0 0;background:#1a1a1d;overflow:hidden}
.arch img{position:absolute;left:50%;bottom:0;transform:translateX(-50%);width:100%;height:auto}
</style></head><body><div class="frame"></div>
<div class="txt"><div class="brand">${mark}abhishekreally.com</div>
<h1>Abhishek<br>Prakash</h1>
<p>Digital Marketing Specialist in Dubai. Meta Ads, performance marketing &amp; content strategy.</p>
<span class="pill">7+ years · UAE &amp; India</span></div>
<div class="arch"><img src="${face}" alt=""></div></body></html>`;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.setContent(html, { waitUntil: 'networkidle' });
  await p.screenshot({ path: path.join(D, 'brand', 'og-image.jpg'), type: 'jpeg', quality: 86 });
  await b.close();
})();
