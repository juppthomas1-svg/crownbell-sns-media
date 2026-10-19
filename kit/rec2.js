const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const files=fs.readdirSync('.').filter(f=>f.endsWith('.html'));const off={};
for(const f of files){const t0=Date.now();
 const ctx=await b.newContext({viewport:{width:1080,height:1920},recordVideo:{dir:'r2_'+f.replace('.html',''),size:{width:1080,height:1920}}});
 const p=await ctx.newPage();await p.goto('file://'+process.cwd()+'/'+encodeURIComponent(f));await p.waitForTimeout(700);
 const T=await p.evaluate(()=>{startAnim();return TOTAL});off[f]=(Date.now()-t0)/1000;await p.waitForTimeout(T+400);await ctx.close();}
fs.writeFileSync('off.json',JSON.stringify(off));await b.close();})();
