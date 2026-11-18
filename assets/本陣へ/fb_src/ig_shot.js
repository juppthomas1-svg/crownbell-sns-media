const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();
for(const [f,w,h] of [['ig_1350',1080,1350],['ig_story',1080,1920]]){
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
 await p.goto('file://'+process.cwd()+'/'+f+'.html');await p.waitForTimeout(600);
 await p.screenshot({path:f+'.png'});}
await b.close();})();
