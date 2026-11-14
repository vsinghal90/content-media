// Naad Katha reel cover, final style (option B, owner 15 Nov 2026).
// Usage: node make-cover.js <background.jpg|png> "<series>" "<bhag e.g. भाग 2>" "<big word>" "<question>" <out.jpg> [style]
// style (optional): 1-navy-gold (default), 2-violet, 3-gold-band, 4-diya-saffron, 5-white-green.
// Series lock: every part of a series uses the style of its भाग 1 cover.
// Needs Playwright (require('playwright')) and internet for Google Fonts (Yatra One).
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const [bg,series,bhag,word,q,out,style]=process.argv.slice(2);
if(!out){console.error('usage: node make-cover.js bg series bhag word question out.jpg');process.exit(1)}
const tplFile=(!style||style==='1-navy-gold')?path.join(__dirname,'cover.template.html'):path.join(__dirname,'colour-variants','_var_'+style+'.html');
if(!fs.existsSync(tplFile)){console.error('unknown style '+style);process.exit(1)}
const tpl=fs.readFileSync(tplFile,'utf8');
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
const html=tpl.replace('{{BG}}','file://'+path.resolve(bg)).replace('{{PILL}}','').replace('{{SERIES}}',esc(series)).replace('{{BHAG}}',esc(bhag)).replace('{{TITLE}}',esc(word)).replace('{{SUB}}',esc(q));
(async()=>{const tmp=path.join(require('os').tmpdir(),'nk-cover-'+Date.now()+'.html');fs.writeFileSync(tmp,html);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+tmp);await p.waitForSelector('body[data-ready]',{timeout:30000});await p.waitForTimeout(200);
await p.screenshot({path:out,type:'jpeg',quality:90});await b.close();fs.unlinkSync(tmp);console.log('saved',out)})();
