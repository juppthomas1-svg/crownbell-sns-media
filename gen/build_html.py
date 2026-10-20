# 10秒の縦型動画（1080x1920）の HTML を作る。
# 使い方: python3 -I build_html.py content.json outdir
# content.json は [{id, kind:"quiz"|"promo", platform:"tt"|"ig", ...}] の配列
import json, sys, os, html, base64, shutil

E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://crownbell-kentei.netlify.app/practice"

CSS = r'''
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#050d22}
body{font-family:"Inter","Noto Sans CJK JP",sans-serif;color:#f4efe2;-webkit-font-smoothing:antialiased;
 background:radial-gradient(90% 55% at 50% 8%,#2a4a86 0%,#132b5e 38%,#091a3d 70%,#050d22 100%)}
canvas{position:absolute;inset:0}
.vig{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 50%,transparent 60%,rgba(0,0,0,.35) 100%)}
.frame{position:absolute;inset:40px;border:1.5px solid rgba(201,168,92,.42)}
.frame:after{content:"";position:absolute;inset:12px;border:1px solid rgba(201,168,92,.18)}
.sc{position:absolute;left:0;right:0;top:0;bottom:0;opacity:0}
.a{opacity:0}
.serif{font-family:"Noto Serif CJK JP",serif}
.gold{color:#e3c47c}
.brand{display:flex;align-items:center;gap:26px}
.brand img{width:118px;height:118px;border-radius:50%;box-shadow:0 0 0 3px rgba(227,196,124,.35),0 0 40px rgba(227,196,124,.25)}
.brand .n{font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:50px;letter-spacing:.04em;line-height:1.2}
.brand .n small{display:block;font-family:"Noto Sans CJK JP";font-weight:700;font-size:30px;letter-spacing:.06em;color:#e3c47c;margin-top:8px}
.kicker{display:flex;align-items:center;gap:22px;font-family:"Noto Serif CJK JP",serif;font-size:36px;letter-spacing:.32em;color:#e3c47c}
.kicker:before{content:"";width:70px;height:1.5px;background:#c9a85c}
.hook{position:absolute;left:96px;right:80px;top:560px}
.hook .kicker{margin:56px 0 44px}
.hook h1{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:96px;line-height:1.38;letter-spacing:.01em;text-shadow:0 6px 30px rgba(0,0,0,.35)}
.hook h1 em{font-style:normal;color:#e3c47c}
.mini{position:absolute;top:150px;left:96px;right:96px;display:flex;justify-content:space-between;align-items:center;font-family:"Noto Serif CJK JP",serif;font-size:30px;letter-spacing:.28em;color:#c9a85c;border-bottom:1px solid rgba(201,168,92,.4);padding-bottom:26px}
.mini b{font-weight:400;font-family:"Inter";letter-spacing:.34em;font-size:28px}
.qwrap{position:absolute;left:96px;right:96px;top:300px}
.band{display:inline-flex;align-items:stretch;background:linear-gradient(90deg,#c9a85c,#e8cd8a);color:#0a1a3d;font-weight:900;font-size:36px;letter-spacing:.06em;margin-bottom:54px}
.band span{padding:14px 26px}
.band span+span{border-left:1.5px solid rgba(10,26,61,.35);font-weight:700;font-size:30px;display:flex;align-items:center}
.qlabel{font-family:"Inter";font-weight:600;font-size:28px;letter-spacing:.4em;color:#c9a85c;margin-bottom:22px}
.qtext{font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:58px;line-height:1.5;margin-bottom:56px}
.qtext .en{display:block;font-family:"Inter";font-weight:700;color:#e3c47c;font-size:64px;line-height:1.3;margin:12px 0 6px}
.opt{position:relative;display:flex;align-items:center;gap:34px;background:rgba(255,255,255,.045);border:1.5px solid rgba(201,168,92,.42);padding:38px 40px;margin-bottom:28px;font-size:46px;font-weight:600;line-height:1.3}
.opt b{flex:none;width:78px;height:78px;border:1.5px solid #c9a85c;color:#e3c47c;display:flex;align-items:center;justify-content:center;font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:42px}
.opt.ok{background:linear-gradient(90deg,#c9a85c,#ead08f);color:#0a1a3d;border-color:#ead08f;box-shadow:0 0 60px rgba(227,196,124,.45)}
.opt.ok b{background:#0a1a3d;color:#e3c47c;border-color:#0a1a3d}
.opt.ng{opacity:.28}
.timer{display:flex;align-items:center;gap:36px;margin-top:40px}
.bar{flex:1;height:8px;background:rgba(255,255,255,.12);position:relative}
.bar i{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,#b8954a,#ead08f);box-shadow:0 0 18px rgba(227,196,124,.6)}
.cnum{width:110px;text-align:right;font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:120px;line-height:1;color:#e3c47c}
.tlab{font-family:"Inter";font-size:24px;letter-spacing:.4em;color:rgba(201,168,92,.8);margin-top:18px}
.anslab{font-family:"Inter";font-weight:600;font-size:30px;letter-spacing:.4em;color:#c9a85c;margin-bottom:30px}
.ex{margin-top:44px;font-size:40px;line-height:1.6;border-left:5px solid #c9a85c;padding:6px 0 6px 34px}
.ex b{color:#e3c47c}
.prob{position:absolute;left:96px;right:96px;top:560px}
.prob .kicker{margin:56px 0 50px}
.pline{display:flex;align-items:center;gap:30px;font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:56px;line-height:1.3;padding:30px 0;border-bottom:1px solid rgba(201,168,92,.3)}
.pline i{flex:none;width:58px;height:58px;border:2px solid #c9a85c;position:relative}
.pline i:after{content:"";position:absolute;left:14px;top:2px;width:18px;height:36px;border-right:6px solid #e3c47c;border-bottom:6px solid #e3c47c;transform:rotate(45deg)}
.sol{position:absolute;left:96px;right:96px;top:600px}
.sol h2{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:96px;line-height:1.38;margin:40px 0 30px}
.sol h2 em{font-style:normal;color:#e3c47c}
.sol .note{font-size:32px;color:rgba(244,239,226,.7);margin-bottom:56px}
.facts{display:flex;gap:18px}
.fact{flex:1;border:1.5px solid rgba(201,168,92,.5);background:rgba(255,255,255,.04);padding:30px 18px;text-align:center}
.fact .k{font-family:"Inter";font-size:22px;letter-spacing:.3em;color:#c9a85c}
.fact .v{font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:44px;line-height:1.3;margin-top:14px}
.fact .v small{display:block;font-size:28px;font-weight:400;font-family:"Noto Sans CJK JP";color:rgba(244,239,226,.75);margin-top:6px}
.end{position:absolute;left:80px;right:80px;top:250px;display:flex;flex-direction:column;align-items:center;text-align:center}
.end .brand{margin-bottom:50px}
.end .lead{font-family:"Noto Serif CJK JP",serif;font-size:42px;line-height:1.6;margin-bottom:34px}
.end .now{font-family:"Inter";font-weight:600;font-size:28px;letter-spacing:.5em;color:#c9a85c}
.end h3{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:120px;line-height:1.22;margin:16px 0 30px}
.end h3 em{font-style:normal;color:#e3c47c}
.chips{display:flex;gap:16px;margin-bottom:44px}
.chips span{border:1.5px solid #c9a85c;color:#f4efe2;font-weight:700;font-size:34px;padding:10px 22px}
.card{display:flex;align-items:center;gap:40px;background:#fbf8f0;color:#0a1a3d;padding:36px 44px;text-align:left;box-shadow:0 30px 80px rgba(0,0,0,.45)}
.card img{width:300px;height:300px;image-rendering:pixelated}
.card .t{white-space:nowrap;font-size:34px;line-height:1.6;font-weight:700}
.card .t b{color:#9a7428}
.card .t .url{display:inline-block;margin-top:14px;font-family:'Inter';font-weight:700;font-size:30px;color:#0a1a3d;border-top:1.5px solid #c9a85c;padding-top:12px}
.card .t .s{font-size:30px;font-weight:500;color:#33405e}
.btn{border:2px solid #e3c47c;padding:30px 70px;font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:52px;letter-spacing:.06em;margin-bottom:28px;background:rgba(227,196,124,.08)}
.srch{font-size:36px;color:rgba(244,239,226,.85)}
.srch b{color:#e3c47c}
.fine{margin-top:44px;font-size:26px;line-height:1.75;color:rgba(244,239,226,.62)}
.foot{position:absolute;left:96px;right:96px;bottom:92px;display:flex;justify-content:space-between;font-family:"Inter";font-size:24px;letter-spacing:.32em;color:rgba(201,168,92,.75);border-top:1px solid rgba(201,168,92,.35);padding-top:24px}

.ad1{position:absolute;left:96px;right:96px;top:520px}
.ad1 .kicker{margin:56px 0 30px}
.ad1 h2{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:76px;line-height:1.4;margin-bottom:36px}
.mid{position:absolute;left:96px;right:96px;top:640px}
.mid h2{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:88px;line-height:1.42;margin:36px 0 40px}
.mid h2 em{font-style:normal;color:#e3c47c}
.mid .sub{font-size:40px;line-height:1.7;color:rgba(244,239,226,.85)}
.feat{display:flex;gap:34px;align-items:center;border-bottom:1px solid rgba(201,168,92,.35);padding:40px 0}
.feat .k{font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:64px;color:#e3c47c;min-width:110px}
.feat .v{font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:54px;line-height:1.35}
.feat .v small{display:block;font-family:"Noto Sans CJK JP";font-weight:500;font-size:34px;color:rgba(244,239,226,.75);margin-top:8px}
.cert{position:relative;margin:30px auto 0;width:820px;height:600px;background:linear-gradient(160deg,#fdfaf1,#f3ecd9);color:#0a1a3d;box-shadow:0 40px 90px rgba(0,0,0,.5);padding:38px}
.cert .b1{position:absolute;inset:22px;border:3px solid #b8954a}
.cert .b2{position:absolute;inset:32px;border:1px solid #c9a85c}
.cert .in{position:relative;height:100%;display:flex;flex-direction:column;align-items:center;text-align:center;padding-top:30px}
.cert .en{font-family:"Inter";font-size:20px;letter-spacing:.5em;color:#9a7428}
.cert h4{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:76px;letter-spacing:.4em;margin:14px 0 10px;padding-left:.4em}
.cert .lv{font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:34px;margin-bottom:20px}
.cert .nm{font-family:"Noto Serif CJK JP",serif;font-size:30px;border-bottom:1.5px solid #0a1a3d;padding:0 60px 6px;margin-bottom:18px}
.cert .tx{font-family:"Noto Serif CJK JP",serif;font-size:22px;line-height:1.7;color:#33405e}
.cert .no{position:absolute;left:30px;bottom:24px;font-family:"Inter";font-size:18px;color:#5a6684;letter-spacing:.06em}
.cert .org{position:absolute;right:120px;bottom:30px;font-family:"Noto Serif CJK JP",serif;font-size:22px;font-weight:700}
.cert img{position:absolute;right:16px;bottom:10px;width:96px;height:96px;border-radius:50%}
.cert .mihon{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-18deg);font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:170px;letter-spacing:.2em;color:rgba(160,120,40,.22);border:8px solid rgba(160,120,40,.22);padding:0 30px}
.ev{position:absolute;left:96px;right:96px;top:330px}
.ev h2{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:68px;line-height:1.45;margin:30px 0 10px}
.ev h2 em{font-style:normal;color:#e3c47c}
.ev .cap{margin-top:40px;font-size:30px;color:rgba(244,239,226,.65);text-align:center}
.btn2{border:2px solid #e3c47c;padding:30px 60px;font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:48px;background:rgba(227,196,124,.1)}

.figwrap{position:absolute;left:170px;right:170px;bottom:150px}
.figwrap svg{width:100%;display:block}
.figp .prob{top:250px}.figp .sol{top:250px}
.figp .prob .pline{font-size:52px;padding:22px 0}
.cert-mini{position:absolute;right:90px;bottom:330px;width:300px;height:220px;background:linear-gradient(160deg,#fdfaf1,#efe6cf);box-shadow:0 20px 60px rgba(0,0,0,.5);transform:rotate(-6deg)}
.cert-mini:before{content:"";position:absolute;inset:10px;border:2px solid #b8954a}
.cert-mini b{position:absolute;left:0;right:0;top:60px;text-align:center;font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:44px;letter-spacing:.3em;color:#0a1a3d}
.cert-mini i{position:absolute;left:40px;right:40px;top:130px;height:2px;background:#c9a85c;box-shadow:0 18px 0 #d8c69a,0 36px 0 #d8c69a}

.story .figwrap{left:220px;right:220px;bottom:345px}
.story .figp .prob{top:300px}.story .figp .sol{top:300px}.story .sol h2{margin:24px 0 18px;font-size:88px}.story .sol .note{margin-bottom:30px}
.story .end{top:300px}
.story .mini{display:none}

/* TikTok/Instagram の画面に重なる場所（上の検索バー・右のボタン・下の投稿文）を避ける */
.safe .mini{display:none}
.safe .hook{left:80px;right:190px;top:430px}
.safe .hook h1{font-size:86px}
.safe .qwrap{left:70px;right:190px;top:220px}
.safe .band{font-size:30px;margin-bottom:34px}.safe .band span+span{font-size:26px}
.safe .qtext{font-size:48px;margin-bottom:30px}.safe .qtext .en{font-size:54px}
.safe .opt{font-size:40px;padding:24px 28px;margin-bottom:18px;gap:24px}
.safe .opt b{width:62px;height:62px;font-size:34px}
.safe .timer{margin-top:22px}.safe .cnum{font-size:96px}
.safe .ex{margin-top:26px;font-size:36px}
.safe .prob{left:70px;right:190px;top:300px}
.safe .pline{font-size:46px;padding:22px 0}
.safe .pline i{width:48px;height:48px}.safe .pline i:after{left:11px;top:1px;width:15px;height:30px}
.safe .sol{left:70px;right:190px;top:260px}
.safe .sol h2{font-size:80px}
.safe .sol .note{font-size:28px;margin-bottom:30px}
.safe .facts{gap:12px}.safe .fact{padding:22px 8px}.safe .fact .v{font-size:36px}.safe .fact .v small{font-size:24px}.safe .fact .k{font-size:18px}
.safe .end{left:60px;right:180px;top:200px}
.safe .end .brand{margin-bottom:26px}.safe .brand img{width:96px;height:96px}.safe .brand .n{font-size:42px}.safe .brand .n small{font-size:26px}
.safe .end .lead{font-size:34px;margin-bottom:16px}
.safe .end h3{font-size:96px;margin:8px 0 20px}
.safe .chips{gap:10px;margin-bottom:26px}.safe .chips span{font-size:28px;padding:8px 14px}
.safe .card{padding:24px 26px;gap:24px}.safe .card img{width:220px;height:220px}
.safe .card .t{font-size:28px}.safe .card .t .s{font-size:24px}.safe .card .t .url{font-size:22px}
.safe .btn{font-size:42px;padding:24px 40px}.safe .srch{font-size:30px}
.safe .fine{margin-top:24px;font-size:22px}
.safe .figwrap{left:130px;right:290px;bottom:470px}
.safe .figp .prob,.safe .figp .sol{top:230px}
.safe .foot{display:none}
.tgt{display:inline-block;margin-top:44px;background:linear-gradient(90deg,#c9a85c,#ead08f);color:#0a1a3d;font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:64px;letter-spacing:.12em;padding:14px 34px}
.tgt+.kicker{margin-top:30px!important}
.qfig{left:320px;right:320px;bottom:330px}
.safe .qfig{left:260px;right:340px;bottom:480px}
.figp .hook{top:300px}

/* 明るい配色（アイボリー × 紺 × 金） */
.light{color:#0f2a5c;background:radial-gradient(110% 70% at 70% 20%,#ffffff 0%,#fbf8f1 45%,#f1ead9 100%)}
.light .vig{background:radial-gradient(120% 80% at 50% 50%,transparent 70%,rgba(150,120,60,.12) 100%)}
.light .frame{border-color:rgba(184,149,74,.7)}.light .frame:after{border-color:rgba(184,149,74,.35)}
.light .gold,.light h1 em,.light .sol h2 em,.light .end h3 em,.light .mid h2 em,.light .ev h2 em{color:#b0883a}
.light .brand .n{color:#0f2a5c}.light .brand .n small{color:#a07c34}
.light .brand img{box-shadow:0 0 0 3px rgba(184,149,74,.45),0 8px 24px rgba(15,42,92,.18)}
.light .kicker{color:#a07c34}.light .kicker:before{background:#b8954a}
.light .hook h1,.light .sol h2,.light .end h3{text-shadow:none}
.light .mini{color:#a07c34;border-color:rgba(184,149,74,.5)}
.light .qlabel,.light .anslab,.light .tlab{color:#a07c34}
.light .qtext .en{color:#b0883a}
.light .opt{background:#0f2a5c;border-color:#b8954a;color:#f7f1e1;box-shadow:0 8px 20px rgba(15,42,92,.15)}
.light .opt b{border-color:#c9a85c;color:#e3c47c}
.light .opt.ok{background:linear-gradient(90deg,#c9a85c,#ead08f);color:#0f2a5c}
.light .opt.ok b{background:#0f2a5c;color:#e3c47c}
.light .opt.ng{opacity:.35}
.light .bar{background:rgba(15,42,92,.12)}.light .cnum{color:#b0883a}
.light .ex{border-color:#b8954a;color:#0f2a5c}.light .ex b{color:#a07c34}
.light .pline{border-color:rgba(184,149,74,.45);color:#0f2a5c}
.light .pline i{background:#0f2a5c;border-color:#0f2a5c}.light .pline i:after{border-color:#e3c47c}
.light .sol .note,.light .mid .sub{color:rgba(15,42,92,.7)}
.light .fact{background:#0f2a5c;border-color:#b8954a;color:#f7f1e1}.light .fact .k{color:#c9a85c}.light .fact .v small{color:rgba(247,241,225,.75)}
.light .end .lead,.light .srch{color:#0f2a5c}.light .srch b{color:#a07c34}
.light .now{color:#a07c34}
.light .chips span{background:#0f2a5c;border-color:#0f2a5c;color:#f7f1e1}
.light .btn,.light .btn2{background:#0f2a5c;border-color:#b8954a;color:#f7f1e1}
.light .card{background:#ffffff;border:1.5px solid #b8954a;box-shadow:0 14px 40px rgba(15,42,92,.15)}
.light .fine{color:rgba(15,42,92,.6)}
.light .foot{color:#a07c34;border-color:rgba(184,149,74,.5)}
.light .tgt{background:#c8102e;color:#fff}
.light .band{background:#0f2a5c;color:#f7f1e1}.light .band span+span{border-color:rgba(247,241,225,.3)}

/* リール広告：下のボタン・投稿文（約640px）と右のボタンを避ける。さらに明るく */
.reelad .figwrap{left:250px;right:400px;bottom:600px}
.reelad .figp .prob,.reelad .figp .sol{top:170px}
.reelad .tgt{margin-top:28px;font-size:56px;padding:10px 28px}
.reelad .tgt+.kicker{margin-top:20px!important;margin-bottom:20px!important}
.reelad .pline{font-size:42px;padding:13px 0}
.reelad .sol h2{font-size:76px;margin:24px 0 16px}
.reelad .end{top:170px}
.reelad .end h3{font-size:88px}
.reelad .fine{font-size:20px;margin-top:16px}
.reelad.light{background:radial-gradient(120% 80% at 70% 15%,#ffffff 0%,#fffdf8 50%,#f7f1e4 100%)}
.reelad.light .vig{display:none}

/* 人物を大きく・文字を太く（2026/10/20） */
body{font-weight:700}
.kicker{font-weight:700}
.fine,.cert .tx{font-weight:600}
.sol .note,.mid .sub,.ex,.srch,.end .lead,.card .t .s,.fact .v small,.feat .v small{font-weight:700}
.figwrap{left:110px;right:110px;bottom:120px}
.safe .figwrap{left:120px;right:295px;bottom:380px}
.reelad .figwrap{left:200px;right:330px;bottom:560px}
.story .figwrap{left:160px;right:160px;bottom:330px}
.qfig{left:250px;right:250px;bottom:260px}
.safe .qfig{left:210px;right:300px;bottom:450px}
'''

FIG = r'''<svg id="fig" viewBox="0 0 600 640" style="overflow:visible" xmlns="http://www.w3.org/2000/svg">
<defs>
 <linearGradient id="suit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c3768"/><stop offset="1" stop-color="#0a1a3d"/></linearGradient>
 <linearGradient id="skin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6d3b3"/><stop offset="1" stop-color="#e2ad86"/></linearGradient>
 <radialGradient id="glow" cx=".5" cy=".42" r=".55"><stop offset="0" stop-color="#e3c47c" stop-opacity=".34"/><stop offset="1" stop-color="#e3c47c" stop-opacity="0"/></radialGradient>
 <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset=".74" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
 <mask id="m" maskUnits="userSpaceOnUse" x="-300" y="-300" width="1200" height="940"><rect x="-300" y="-300" width="1200" height="940" fill="url(#fade)"/></mask>
</defs>
<ellipse id="figglow" cx="300" cy="300" rx="430" ry="430" fill="url(#glow)" opacity="0"/>
<g id="qs" fill="#c9a85c" font-family="Noto Serif CJK JP" font-weight="700">
 <text id="q1" x="150" y="120" font-size="64">?</text><text id="q2" x="430" y="90" font-size="48">?</text><text id="q3" x="470" y="200" font-size="36">?</text>
</g>
<g mask="url(#m)" stroke="#d9b866" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round">
 <g id="body">
  <path d="M40 640 C46 520 92 452 190 424 L248 404 L300 470 L352 404 L410 424 C508 452 554 520 560 640 Z" fill="url(#suit)"/>
  <path d="M248 404 L300 470 L352 404 L340 392 L300 412 L260 392 Z" fill="#e9e1cc" stroke-width="1.6"/>
  <path d="M262 420 L300 470 L338 420 L320 560 L300 600 L280 560 Z" fill="#e9e1cc" stroke="none"/>
  <path d="M290 418 L310 418 L316 440 L326 580 L300 612 L274 580 L284 440 Z" fill="#0a1a3d" stroke-width="1.8"/>
  <path d="M290 418 L310 418 L316 440 L284 440 Z" fill="#132b5e" stroke-width="1.8"/>
  <path d="M248 404 L226 430 L262 470 L238 500 L300 600" fill="none"/>
  <path d="M352 404 L374 430 L338 470 L362 500 L300 600" fill="none"/>
  <path d="M410 505 L452 500 L455 512 L413 517 Z" fill="#c9a85c" stroke-width="1.4"/>
  <path d="M266 330 L266 392 L300 412 L334 392 L334 330" fill="url(#skin)" stroke="#b9805c"/>
 </g>
 <g id="head">
  <path d="M300 92 C356 92 392 136 392 200 C392 270 352 336 300 340 C248 336 208 270 208 200 C208 136 244 92 300 92 Z" fill="url(#skin)" stroke="#b9805c"/>
  <path d="M206 206 C196 128 240 70 306 72 C372 74 410 124 398 206 C390 170 372 146 348 136 C320 150 270 152 238 140 C222 156 212 178 206 206 Z" fill="#1f1712" stroke="#1f1712"/>
  <path d="M210 196 C196 194 194 236 214 240" fill="url(#skin)" stroke="#b9805c" stroke-width="1.8"/>
  <path d="M390 196 C404 194 406 236 386 240" fill="url(#skin)" stroke="#b9805c" stroke-width="1.8"/>
  <g fill="none" stroke="#4a3022" stroke-width="5">
   <path id="bl"/><path id="br"/><path id="mo" stroke="#9a4e42" stroke-width="4.5"/>
  </g>
  <ellipse id="el" cx="264" cy="236" rx="7" ry="3" fill="#2a1a12" stroke="none"/>
  <ellipse id="er" cx="336" cy="236" rx="7" ry="3" fill="#2a1a12" stroke="none"/>
 </g>
 <g id="cert" opacity="0"><g transform="translate(0 -108) translate(300 527) scale(1.32) translate(-300 -527)">
  <rect x="196" y="452" width="208" height="150" fill="#fbf7ec" stroke="#b8954a" stroke-width="3"/>
  <rect x="206" y="462" width="188" height="130" fill="none" stroke="#c9a85c" stroke-width="1.2"/>
  <text x="300" y="512" text-anchor="middle" font-family="Noto Serif CJK JP" font-weight="900" font-size="34" fill="#0a1a3d" stroke="none" letter-spacing="6">合格証</text>
  <text id="ctext" x="300" y="546" text-anchor="middle" font-family="Noto Serif CJK JP" font-weight="700" font-size="17" fill="#0a1a3d" stroke="none" letter-spacing="1"></text><rect id="ccur" x="0" y="531" width="2" height="19" fill="#9a7428" stroke="none" opacity="0"/><path d="M232 564 H368 M232 578 H330" stroke="#d8c69a" stroke-width="2"/>
  <circle cx="372" cy="575" r="12" fill="#c9a85c" stroke="none"/>
  <ellipse cx="200" cy="590" rx="26" ry="20" fill="url(#skin)" stroke="#b9805c"/><ellipse cx="400" cy="590" rx="26" ry="20" fill="url(#skin)" stroke="#b9805c"/></g>
 </g>
</g>
</svg>'''

JS = r'''
const W=1080,H=1920,cv=document.getElementById('cv'),cx=cv.getContext('2d');cv.width=W;cv.height=H;
function rnd(s){return function(){s=(s*16807)%2147483647;return (s-1)/2147483646}}
const R=rnd(SEED);const dust=[...Array(70)].map(()=>({x:R()*W,y:R()*H,r:.8+R()*2.2,s:8+R()*26,p:R()*6.28,f:.5+R()}));
const RB=rnd(SEED+7);const burst=[...Array(110)].map(()=>{const a=RB()*6.283,v=300+RB()*900;return {vx:Math.cos(a)*v,vy:Math.sin(a)*v-350,r:2+RB()*5,l:.9+RB()*.9,tw:RB()*6}});
const cl=x=>Math.max(0,Math.min(1,x)),ease=x=>1-Math.pow(1-x,3);
function vis(el,t){const i=+el.dataset.in,o=el.dataset.out?+el.dataset.out:1e9,d=+(el.dataset.d||450);
 const a=ease(cl((t-i)/d)),b=cl((o-t)/280);const v=Math.min(a,b);el.style.opacity=v;
 if(el.classList.contains('a'))el.style.transform=`translateY(${(1-a)*34}px)`;}
window.render=function(ms){const t=ms;document.querySelectorAll('[data-in]').forEach(e=>vis(e,t));
 cx.clearRect(0,0,W,H);
 for(const d of dust){const y=((d.y-t/1000*d.s)%H+H)%H,o=.18+.32*(.5+.5*Math.sin(t/1000*d.f*2+d.p));
  cx.beginPath();cx.arc(d.x+Math.sin(t/1500+d.p)*8,y,d.r,0,6.283);cx.fillStyle=document.body.classList.contains('light')?`rgba(184,149,74,${o*.8})`:`rgba(232,205,138,${o})`;cx.fill();}
 if(window.BURST){const dt=(t-BURST.t)/1000;if(dt>0&&dt<2){for(const p of burst){if(dt>p.l)continue;
  const x=BURST.x+p.vx*dt*Math.exp(-dt*1.6),y=BURST.y+p.vy*dt*Math.exp(-dt*1.6)+260*dt*dt,o=(1-dt/p.l)*(.6+.4*Math.sin(dt*30+p.tw));
  const g=cx.createRadialGradient(x,y,0,x,y,p.r*3);g.addColorStop(0,`rgba(255,240,190,${o})`);g.addColorStop(.4,`rgba(232,200,120,${o*.8})`);g.addColorStop(1,'rgba(232,200,120,0)');
  cx.fillStyle=g;cx.beginPath();cx.arc(x,y,p.r*3,0,6.283);cx.fill();}}}
 if(window.HOOKS)HOOKS(t);};
'''

def brand(sub="24時間いつでもオンライン受験"):
    return f'<div class="brand"><img src="logo.png"><div class="n">ビジネス英語実務検定<small>{E(sub)}</small></div></div>'

def end_screen(platform, t0, lead):
    fine = ('本番は合格すれば合格証を最短で受験当日に発行｜3級 3,500円〜（税込）<br>'
            '※お試し問題は本番とは異なり、合格証は発行されません<br>'
            '※国際ビジネス言語認定協会が認定する民間資格です')
    if platform == "tt":
        how = ('<div class="card a" data-in="%d"><img src="qr.png"><div class="t">無料お試しは<br>'
               '<b>「ビジネス英語実務検定」</b><br>で検索<br><span class="s">またはQRをスクショ → 長押し</span><br>'
               '<span class="url">crownbell-kentei.netlify.app/tiktok</span></div></div>') % (t0 + 450)
    elif platform in ("igad", "igreel"):
        how = ('<div class="a" data-in="%d"><div class="btn">下の「詳しくはこちら」から</div>'
               '<div class="srch">または <b>「ビジネス英語実務検定」</b> で検索</div></div>') % (t0 + 450)
    elif platform == "x":
        how = ('<div class="a" data-in="%d"><div class="btn">プロフィールのリンクから</div>'
               '<div class="srch">または <b>この投稿への返信</b> のリンクから</div></div>') % (t0 + 450)
    else:
        how = ('<div class="a" data-in="%d"><div class="btn">プロフィールのリンクから</div>'
               '<div class="srch">または <b>「ビジネス英語実務検定」</b> で検索</div></div>') % (t0 + 450)
    return (f'<div class="sc" data-in="{t0}" data-d="350"><div class="end">'
            f'<div class="a" data-in="{t0}">{brand()}</div>'
            f'<div class="lead a" data-in="{t0+100}">{lead}</div>'
            f'<div class="now a" data-in="{t0+200}">NOW OPEN</div>'
            f'<h3 class="a" data-in="{t0+250}">無料お試し<br><em>実施中</em></h3>'
            f'<div class="chips a" data-in="{t0+350}"><span>登録なし</span><span>10問</span><span>約5分</span><span>スマホでOK</span></div>'
            f'{how}<div class="fine a" data-in="{t0+600}">{fine}</div></div></div>')

def quiz(v):
    T_Q, T_A, T_E = 2100, 5600, 7700
    L = "ABC"
    hook = (f'<div class="sc" data-in="-1000" data-out="{T_Q}" data-d="250"><div class="hook">'
            f'<div class="a" data-in="-1000">{brand()}</div>'
            f'<div class="kicker a" data-in="-1000">{E(v["kicker"])}</div>'
            f'<h1 class="a" data-in="-1000">{v["hook"]}</h1></div></div>')
    opts_q = ''.join(f'<div class="opt a" data-in="{T_Q+200+j*110}"><b>{L[j]}</b><span>{E(o)}</span></div>' for j, o in enumerate(v["opts"]))
    q = (f'<div class="sc" data-in="{T_Q}" data-out="{T_E}" data-d="300">'
         f'<div class="mini"><span>ビジネス英語実務検定</span><b>QUESTION</b></div><div class="qwrap">'
         f'<div class="band a" data-in="{T_Q}"><span>無料お試し 実施中</span><span>登録なし・10問・約5分</span></div>'
         f'<div class="qtext a" data-in="{T_Q+80}">{v["q"]}</div>'
         f'<div id="opts">{opts_q}</div>'
         f'<div id="tm" data-in="{T_Q+450}" data-out="{T_A}" data-d="250"><div class="timer"><div class="bar"><i id="bar"></i></div><div class="cnum" id="cn">3</div></div>'
         f'<div class="tlab">TIME LIMIT ― 回答まで</div></div>'
         f'<div class="ex a" data-in="{T_A+350}">{v["ex"]}</div></div></div>')
    hooks = (f'window.HOOKS=function(t){{const tb=document.getElementById("bar");tb.style.width=(100*(1-cl((t-{T_Q+500})/3000)))+"%";'
             f'document.getElementById("cn").textContent=t<{T_Q+1500}?"3":t<{T_Q+2500}?"2":"1";'
             f'const os=document.querySelectorAll("#opts .opt");os.forEach((o,j)=>{{o.classList.toggle("ok",t>={T_A}&&j=={v["ans"]});o.classList.toggle("ng",t>={T_A}&&j!={v["ans"]});}});'
             f'if(t>={T_A}&&!window.BURST){{const r=os[{v["ans"]}].getBoundingClientRect();window.BURST={{t:{T_A},x:r.left+r.width/2,y:r.top+r.height/2}};}}}};')
    lead = "書類選考で苦戦していませんか？<br>資格欄、空白のままになっていませんか？"
    if v.get("figure"):
        fig = f'<div class="figwrap qfig" data-in="-1000" data-out="{T_Q}" data-d="250">{FIG}</div>'
        hooks += ("(function(){const H=window.HOOKS;window.HOOKS=function(t){H(t);const $=i=>document.getElementById(i);if(!$('fig'))return;"
                  "const sw=Math.sin(t/600);$('fig').style.filter='saturate(.7) brightness(.95)';"
                  "$('head').setAttribute('transform',`translate(0 14) rotate(${-8+sw*3} 300 330)`);"
                  "$('bl').setAttribute('d','M246 206 Q266 198 284 192');$('br').setAttribute('d','M354 200 Q334 196 316 198');"
                  "$('mo').setAttribute('d','M284 292 Q300 290 316 288');$('el').setAttribute('ry',5);$('er').setAttribute('ry',5);"
                  "['q1','q2','q3'].forEach((q,i)=>{const e=$(q);e.setAttribute('opacity',.75);e.setAttribute('transform',`translate(0 ${Math.sin(t/450+i*2)*10})`)});}})();")
        return '<div class="figp">' + hook + fig + '</div>' + q + end_screen(v["platform"], T_E, lead), hooks
    return hook + q + end_screen(v["platform"], T_E, lead), hooks

def promo(v):
    T_S, T_E = 3000, 6800
    lines = ''.join(f'<div class="pline a" data-in="-1000"><i></i><span>{E(p)}</span></div>' for j, p in enumerate(v["problems"]))
    prob = (f'<div class="sc" data-in="-1000" data-out="{T_S}" data-d="250"><div class="prob">'
            f'<div class="a" data-in="-1000">{brand()}</div>'
            + (f'<div class="tgt a" data-in="-1000">{E(v["target"])}</div>' if v.get("target") else '') +
            f'<div class="kicker a" data-in="-1000">{E(v["kicker"])}</div>{lines}</div></div>')
    facts = ''.join(f'<div class="fact a" data-in="{T_S+900+j*150}"><div class="k">{k}</div><div class="v">{val}</div></div>' for j, (k, val) in enumerate(v["facts"]))
    sol = (f'<div class="sc" data-in="{T_S}" data-out="{T_E}" data-d="300"><div class="mini"><span>ビジネス英語実務検定</span><b>SOLUTION</b></div><div class="sol">'
           f'<div class="kicker a" data-in="{T_S+50}">{E(v["sol_kicker"])}</div>'
           f'<h2 class="a" data-in="{T_S+150}" data-d="550">{v["sol"]}</h2>'
           f'<div class="note a" data-in="{T_S+500}">{v["sol_note"]}</div><div class="facts">{facts}</div></div></div>')
    if v.get("figure"):
        fig = (f'<div class="figwrap" data-in="-1000" data-out="{T_E}" data-d="300">{FIG}</div>'
               '')
        hooks = ("window.HOOKS=function(t){const p=ease(cl((t-%d)/900)),L=(a,b)=>a+(b-a)*p,$=i=>document.getElementById(i);"
                 "if(!$('fig'))return;"
                 "$('figglow').setAttribute('opacity',p);$('fig').style.filter='saturate('+L(.55,1)+') brightness('+L(.9,1.03)+')';"
                 "$('head').setAttribute('transform',`translate(0 ${L(26,-8)}) rotate(${L(-7,0)} 300 330)`);"
                 "$('body').setAttribute('transform',`translate(0 ${L(10,-6)}) scale(1 ${L(.975,1.01)})`);"
                 "$('bl').setAttribute('d',`M246 ${L(212,198)} Q266 ${L(204,186)} 284 ${L(196,196)}`);"
                 "$('br').setAttribute('d',`M354 ${L(212,198)} Q334 ${L(204,186)} 316 ${L(196,196)}`);"
                 "$('mo').setAttribute('d',`M280 ${L(292,286)} Q300 ${L(280,304)} 320 ${L(292,286)}`);"
                 "$('el').setAttribute('ry',L(2.5,6.5));$('er').setAttribute('ry',L(2.5,6.5));"
                 "const w=Math.sin(t/400);['q1','q2','q3'].forEach((q,i)=>{const e=$(q);e.setAttribute('opacity',(1-p)*(.55+.2*Math.sin(t/300+i)));e.setAttribute('transform',`translate(0 ${Math.sin(t/500+i*2)*8})`)});"
                 "const c=ease(cl((t-%d)/700));$('cert').setAttribute('opacity',c);$('cert').setAttribute('transform',`translate(0 ${(1-c)*260})`);"
                 "const TX='ビジネス英語実務検定',n=Math.max(0,Math.min(TX.length,Math.floor((t-%d)/85)));$('ctext').textContent=TX.slice(0,n);$('ccur').setAttribute('opacity',(t>%d&&n<TX.length&&Math.floor(t/250)%%2)?1:0);if(n>0){const bb=$('ctext').getBBox();$('ccur').setAttribute('x',bb.x+bb.width+2);}"
                 "if(t>=%d&&!window.BURST){const r=$('cert').getBoundingClientRect();window.BURST={t:%d,x:r.left+r.width/2,y:r.top+r.height/3};}};") % (T_S+250, T_S, T_S+750, T_S+700, T_S+650, T_S+650)
        return '<div class="figp">' + prob + sol + fig + '</div>' + end_screen(v["platform"], T_E, v.get("end_lead", "あなたのビジネス英語力を、<br>確かな資格に。")), hooks
    return prob + sol + end_screen(v["platform"], T_E, v.get("end_lead", "あなたのビジネス英語力を、<br>確かな資格に。")), ''


def ad(v):
    T1, T2, T3, T4 = 3600, 6600, 10600, 14600
    lines = ''.join(f'<div class="pline a" data-in="-1000"><i></i><span>{E(p)}</span></div>' for p in v["problems"])
    s1 = (f'<div class="sc" data-in="-1000" data-out="{T1}" data-d="250"><div class="ad1">'
          f'<div class="a" data-in="-1000">{brand()}</div>'
          f'<div class="kicker a" data-in="-1000">就職活動中の皆さまへ</div>'
          f'<h2 class="a" data-in="-1000">こんなお悩みは<br>ありませんか。</h2>{lines}</div></div>')
    s2 = (f'<div class="sc" data-in="{T1}" data-out="{T2}" data-d="300"><div class="mini"><span>ビジネス英語実務検定</span><b>SOLUTION</b></div><div class="mid" style="top:740px">'
          f'<div class="kicker a" data-in="{T1+50}">そんな方のための</div>'
          f'<h2 class="a" data-in="{T1+150}" data-d="600">ビジネス英語<br><em>実務検定。</em></h2>'
          f'<div class="sub a" data-in="{T1+600}">仕事で使う英語の力を測る、<br>オンラインの検定です。</div></div></div>')
    feats = [("01","実務の場面から出題","メール・会議・電話"),("02","24時間いつでも受験","PC・スマホでオンライン"),("03","3級・2級・1級","3つのレベル")]
    fh = ''.join(f'<div class="feat a" data-in="{T2+250+j*450}"><span class="k">{k}</span><span class="v">{a}<small>{b}</small></span></div>' for j,(k,a,b) in enumerate(feats))
    s3 = (f'<div class="sc" data-in="{T2}" data-out="{T3}" data-d="300"><div class="mini"><span>ビジネス英語実務検定</span><b>FEATURES</b></div><div class="mid" style="top:660px">'
          f'<div class="kicker a" data-in="{T2+50}">3つの特長</div>{fh}</div></div>')
    cert = ('<div class="cert"><div class="b1"></div><div class="b2"></div><div class="in">'
            '<div class="en">CERTIFICATE OF ACHIEVEMENT</div><h4>合格証</h4>'
            '<div class="lv">ビジネス英語実務検定　3級</div><div class="nm">氏名　○○ ○○</div>'
            '<div class="tx">あなたは本検定に合格したことを<br>ここに証します</div></div>'
            '<div class="no">認定番号 No. 000000</div><div class="org">国際ビジネス言語認定協会</div><img src="logo.png">'
            '<div class="mihon">見本</div></div>')
    s4 = (f'<div class="sc" data-in="{T3}" data-out="{T4}" data-d="300"><div class="mini"><span>ビジネス英語実務検定</span><b>CERTIFICATE</b></div><div class="ev">'
          f'<div class="kicker a" data-in="{T3+50}">認定番号つきの合格証</div>'
          f'<h2 class="a" data-in="{T3+150}">合格すれば、<br><em>最短で受験当日</em>に<br>PDFで発行。</h2>'
          f'<div class="a" data-in="{T3+500}" data-d="700">{cert}</div>'
          f'<div class="cap a" data-in="{T3+700}">※画像は見本です</div></div></div>')
    fine = ('3級 3,500円〜（税込）<br>※お試し問題は本番とは異なり、合格証は発行されません<br>'
            '※国際ビジネス言語認定協会が認定する民間資格です')
    s5 = (f'<div class="sc" data-in="{T4}" data-d="350"><div class="end" style="top:330px">'
          f'<div class="a" data-in="{T4}">{brand()}</div>'
          f'<div class="now a" data-in="{T4+150}" style="margin-top:30px">FREE TRIAL</div>'
          f'<h3 class="a" data-in="{T4+250}" style="font-size:104px">まずは、<br><em>無料体験版</em>から。</h3>'
          f'<div class="chips a" data-in="{T4+400}"><span>登録不要</span><span>10問</span><span>約5分</span><span>スマホでOK</span></div>'
          f'<div class="btn2 a" data-in="{T4+550}">画面下のボタンから</div>'
          f'<div class="fine a" data-in="{T4+700}">{fine}</div></div></div>')
    return s1+s2+s3+s4+s5, ''

def build(v, outdir):
    body, hooks = quiz(v) if v["kind"] == "quiz" else ad(v) if v["kind"] == "ad" else promo(v)
    seed = sum(ord(c) for c in v["id"]) % 9000 + 11
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{"story" if v["platform"]=="igad" else "safe reelad" if v["platform"]=="igreel" else "safe" if v["platform"] in ("tt","ig") else ""}{" light" if v.get("theme")=="light" else ""}">'
           f'<canvas id="cv"></canvas><div class="vig"></div><div class="frame"></div>{body}'
           f'<div class="foot"><span>国際ビジネス言語認定協会</span><span>ONLINE EXAMINATION</span></div>'
           f'<script>const SEED={seed};{JS}{hooks}</script></body></html>')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, v["id"] + ".html")
    open(p, "w").write(doc)
    return p

if __name__ == "__main__":
    items = json.load(open(sys.argv[1])); out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    shutil.copy(os.path.join(HERE, "..", "kit", "logo-seal.png"), os.path.join(out, "logo.png"))
    import cv2
    q = cv2.QRCodeEncoder.create().encode(SITE)
    cv2.imwrite(os.path.join(out, "qr.png"), cv2.resize(q, (q.shape[1]*10, q.shape[0]*10), interpolation=cv2.INTER_NEAREST))
    for v in items:
        print(build(v, out))
