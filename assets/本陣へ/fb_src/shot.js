const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [f,w,h] of [['fb_1080',1080,1080],['fb_1200x630',1200,630]]){
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:2});
 await p.goto('file://'+process.cwd()+'/'+f+'.html');await p.waitForTimeout(500);
 await p.screenshot({path:f+'@2x.png'});
 const p1=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
 await p1.goto('file://'+process.cwd()+'/'+f+'.html');await p1.waitForTimeout(500);
 await p1.screenshot({path:f+'.png'});}
await b.close();})();
