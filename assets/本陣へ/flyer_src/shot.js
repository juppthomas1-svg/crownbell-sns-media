const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1240,height:1754},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/flyer.html');await p.waitForTimeout(600);
await p.screenshot({path:'flyer_A4_300dpi_raw.png'});
await p.pdf({path:'flyer_A4.pdf',width:'210mm',height:'297mm',printBackground:true,pageRanges:'1'});
await b.close();})();
