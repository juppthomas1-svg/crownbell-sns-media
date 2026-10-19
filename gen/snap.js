const {chromium}=require('playwright');const path=require('path');
(async()=>{const [dir,id,...ts]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(dir,id+'.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
for(const t of ts){await p.evaluate(ms=>window.render(ms),+t);await p.screenshot({path:`${dir}/snap_${id}_${t}.png`});}await b.close();})();
