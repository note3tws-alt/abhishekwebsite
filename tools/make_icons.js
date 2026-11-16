// Regenerates favicon/app-icon PNGs from src/brand/mark.svg and mark-square.svg.
// Needs Node + Playwright: npm i -D playwright && npx playwright install chromium && node tools/make_icons.js
const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{const b=await chromium.launch();const D=require('path').join(__dirname,'..','src','brand')+'/';
const jobs=[['mark.svg',32,'favicon-32.png'],['mark-square.svg',180,'apple-touch-icon.png'],['mark-square.svg',192,'icon-192.png'],['mark-square.svg',512,'icon-512.png']];
for (const [src,size,out] of jobs){const p=await b.newPage({viewport:{width:size,height:size}});
const svg=fs.readFileSync(D+src,'utf8');
await p.setContent('<html><body style="margin:0;background:transparent">'+svg.replace('<svg ','<svg width="'+size+'" height="'+size+'" style="display:block" ')+'</body></html>');
await p.screenshot({path:D+out,omitBackground:true,clip:{x:0,y:0,width:size,height:size}});await p.close();}
await b.close();})()
