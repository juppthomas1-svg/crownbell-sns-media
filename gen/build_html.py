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
#pulse{position:absolute;inset:0;opacity:0;pointer-events:none;background:radial-gradient(70% 55% at 50% 45%,rgba(227,196,124,.0) 30%,rgba(227,196,124,.55) 100%)}
.light #pulse{background:radial-gradient(70% 55% at 50% 45%,rgba(15,42,92,0) 35%,rgba(15,42,92,.35) 100%)}
.beams{display:none}.power .beams{display:block}
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

/* 焦らせるタイマー */
.ring{position:relative;width:200px;height:200px;flex:none}
.ring svg{position:absolute;inset:0;transform:rotate(-90deg)}
.ring .rbg{fill:none;stroke:rgba(201,168,92,.22);stroke-width:12}
.ring #rfg{fill:none;stroke:#e3c47c;stroke-width:12;stroke-linecap:round;stroke-dasharray:540.4;filter:drop-shadow(0 0 10px rgba(227,196,124,.7))}
.ring .cnum{position:absolute;inset:0;width:auto;display:flex;align-items:center;justify-content:center;text-align:center;font-size:112px}
.light .ring #rfg{stroke:#b0883a;filter:drop-shadow(0 0 8px rgba(176,136,58,.5))}
.light .ring .rbg{stroke:rgba(15,42,92,.12)}
.bignum{position:absolute;left:0;right:0;top:420px;text-align:center;font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:1100px;line-height:1;color:rgba(227,196,124,.07);pointer-events:none}
.light .bignum{color:rgba(15,42,92,.06)}
.safe .ring{width:160px;height:160px}.safe .ring .cnum{font-size:88px}
.safe .bignum{font-size:900px;top:360px;left:-90px}
.timer{gap:30px}

/* ランキング */
.rk-head{position:absolute;left:130px;right:130px;top:190px;text-align:center}
.rk-head .who{display:inline-block;background:#0f2a5c;color:#f7f1e1;font-weight:900;font-size:40px;padding:8px 22px;letter-spacing:.04em}
.rk-head h1{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:76px;line-height:1.25;margin-top:16px}
.rk-head h1 em{font-style:normal;color:#b0883a}
.rk-note{margin-top:10px;font-size:22px;color:rgba(15,42,92,.6)}
.rk-list{position:absolute;left:130px;right:130px;top:540px}
.rk-row{display:flex;align-items:center;gap:20px;height:118px;margin-bottom:14px}
.rk-no{flex:none;width:118px;height:118px;display:flex;align-items:center;justify-content:center;font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:54px;color:#fff;background:#0f2a5c}
.rk-no small{font-size:26px;margin-left:2px}
.rk-row.top .rk-no{background:linear-gradient(135deg,#c9a85c,#ead08f);color:#0f2a5c;font-size:64px}
.rk-slot{flex:1;height:118px;background:#fff;border:2px solid rgba(184,149,74,.55);display:flex;align-items:center;padding:0 24px;font-weight:900;font-size:38px;color:#0f2a5c;overflow:hidden;box-shadow:0 6px 18px rgba(15,42,92,.08)}
.rk-row.top .rk-slot{border:3px solid #c9a85c;background:linear-gradient(90deg,#fffaf0,#fff)}
.rk-slot span{display:block;opacity:0}
.rk-slot .q{font-family:"Noto Serif CJK JP",serif;font-size:60px;color:rgba(15,42,92,.2)}
.rk-row.top .rk-slot span.win{font-family:"Noto Serif CJK JP",serif;font-size:48px;color:#0f2a5c}
.rk-desc{position:absolute;left:130px;right:400px;top:1260px;height:190px}
.rk-desc>div{position:absolute;inset:0;opacity:0;border-left:6px solid #b8954a;padding:6px 0 6px 22px;font-size:31px;line-height:1.55;font-weight:700;color:#0f2a5c}
.rk-desc b{color:#a07c34}
.rk-fig{position:absolute;left:665px;width:240px;top:1170px}
.rk-fig svg{width:100%;display:block}

.rk2 .rk-row{height:120px;margin-bottom:12px}
.rk2 .rk-no{width:120px;height:120px}
.rk2 .rk-slot{height:120px}
.rk2 .rk-desc{top:1080px;height:360px;right:150px}
.rk2 .rk-desc>div{font-size:29px;line-height:1.6}
.rk2 .rk-desc .g{display:block;color:#a07c34;margin-bottom:6px}
.rk2 .rk-desc .x{display:block;color:#0f2a5c}
.rk2 .rk-desc .x i{font-style:normal;display:inline-block;width:34px;height:34px;line-height:34px;text-align:center;background:#0f2a5c;color:#fff;font-size:22px;margin-right:10px;vertical-align:2px}
.rk2 .rk-desc .g i{font-style:normal;display:inline-block;width:34px;height:34px;line-height:34px;text-align:center;background:linear-gradient(135deg,#c9a85c,#ead08f);color:#0f2a5c;font-size:22px;margin-right:10px;vertical-align:2px}
.rk2 .rk-fig{display:none}
.rk-crit{position:absolute;left:130px;right:130px;top:1455px;font-size:19px;line-height:1.5;color:rgba(15,42,92,.55);text-align:center}

.rk2 .rk-head h1{font-size:58px;line-height:1.3;margin-top:14px}
.rk2 .rk-list{top:530px}
.rk2 .rk-desc{top:1070px;height:370px}
.rk2 .rk-desc>div{font-size:37px;line-height:1.55;padding-left:24px}
.rk2 .rk-desc .x i,.rk2 .rk-desc .g i{width:42px;height:42px;line-height:42px;font-size:26px}
.rk2 .rk-crit{top:auto;position:static;margin-top:8px;font-size:19px;color:rgba(15,42,92,.55)}
.rk2 .rk-note{display:none}

/* 就活系TikTok風（今回だけの特別デザイン） */
.jk{background:linear-gradient(180deg,#dfe8f1 0%,#eef2f6 40%,#d9dee5 100%)}
.jk .vig,.jk .frame,.jk .foot,.jk #pulse{display:none}
.jk-bg{position:absolute;inset:0;overflow:hidden}
.jk-bg i{position:absolute;top:0;bottom:900px;width:150px;background:linear-gradient(180deg,rgba(255,255,255,.95),rgba(255,255,255,.55));filter:blur(18px)}
.jk-bg b{position:absolute;left:0;right:0;top:1020px;bottom:0;background:linear-gradient(180deg,#c8cfd8,#b9c1cc);filter:blur(2px)}
.jk-bg u{position:absolute;left:-40px;right:-40px;top:980px;height:70px;background:#9aa6b4;filter:blur(14px);opacity:.6}
.jk-title{position:absolute;left:60px;top:175px;background:#1d6fd1;color:#fff;font-family:"Noto Sans CJK JP";font-weight:900;font-size:66px;letter-spacing:.02em;padding:10px 26px;box-shadow:0 8px 0 #0f4c97}
.jk-sub{position:absolute;left:60px;top:300px;background:#fff;color:#1d3557;font-weight:900;font-size:34px;padding:6px 18px}
.jk-list{position:absolute;left:40px;top:400px;width:330px}
.jk-row{display:flex;align-items:center;gap:10px;height:122px;margin-bottom:12px}
.jk-no{width:64px;text-align:center;font-family:"Noto Sans CJK JP";font-weight:900;font-size:76px;-webkit-text-stroke:5px #fff;paint-order:stroke fill}
.jk-slot{flex:1;height:122px;background:#fff;box-shadow:0 6px 16px rgba(0,0,0,.12);display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;font-size:30px;line-height:1.2;color:#1d3557;padding:0 10px}
.jk-slot span{opacity:0}
.jk-fig{position:absolute;left:330px;width:560px;top:520px}
.jk-fig svg{width:100%;display:block;overflow:visible}
.jk-pop{position:absolute;left:400px;width:440px;top:900px;height:190px;background:#fff;box-shadow:0 14px 34px rgba(0,0,0,.2);display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;font-size:50px;line-height:1.2;color:#1d3557;opacity:0}
.jk-cap{position:absolute;left:60px;right:190px;top:1300px;height:140px;text-align:center}
.jk-cap div{position:absolute;left:0;right:0;opacity:0;font-family:"Noto Sans CJK JP";font-weight:900;font-size:50px;line-height:1.3;color:#fff;-webkit-text-stroke:10px #111;paint-order:stroke fill}
.jk-cap div.y{color:#ffe14d}
.jk-note{position:absolute;left:60px;right:190px;top:1205px;font-size:19px;line-height:1.45;color:rgba(20,30,50,.6);font-weight:700}

/* 気合いの入る配色（power） */
.power{color:#fff;background:radial-gradient(90% 60% at 50% 30%,#163a86 0%,#0b1f4d 45%,#040b1f 100%)}
.power .vig{background:radial-gradient(120% 80% at 50% 50%,transparent 55%,rgba(0,0,0,.55) 100%)}
.power .beams{position:absolute;inset:-200px;pointer-events:none;background:
 linear-gradient(115deg,transparent 38%,rgba(242,193,78,.16) 40%,transparent 44%),
 linear-gradient(115deg,transparent 52%,rgba(242,193,78,.10) 53%,transparent 56%),
 linear-gradient(115deg,transparent 64%,rgba(255,255,255,.06) 65%,transparent 67%)}
.power .frame{border-color:rgba(242,193,78,.6)}
.power .brand img{width:78px;height:78px}
.power .brand .n{font-size:32px;color:rgba(255,255,255,.85)}
.power .brand .n small{font-size:20px;color:#f2c14e}
.power .hook{top:330px}
.power .hook .kicker{display:block;margin:44px 0 40px;background:linear-gradient(90deg,#f2c14e,#ffe08a);color:#071330;font-family:"Noto Sans CJK JP";font-weight:900;font-size:54px;line-height:1.3;letter-spacing:.02em;padding:18px 28px;box-shadow:0 10px 30px rgba(242,193,78,.35)}
.power .hook .kicker:before{display:none}
.power .hook h1{font-family:"Noto Sans CJK JP";font-weight:900;font-size:100px;line-height:1.25;color:#fff;text-shadow:0 6px 30px rgba(0,0,0,.5)}
.power .hook h1 em{color:#f2c14e}
.power .opt{background:rgba(255,255,255,.06);border-color:#f2c14e}
.power .opt b{border-color:#f2c14e;color:#f2c14e}
.power .opt.ok{background:linear-gradient(90deg,#f2c14e,#ffe08a);color:#071330}
.power .qtext .en,.power .cnum,.power .gold,.power .ex b{color:#f2c14e}
.power .band{background:linear-gradient(90deg,#f2c14e,#ffe08a)}
.power .ring #rfg{stroke:#f2c14e}
.power .end h3 em,.power .sol h2 em{color:#f2c14e}

/* NYスカイライン（power） */
.sky{position:absolute;left:0;right:0;bottom:0;width:1080px;height:760px;opacity:.7;-webkit-mask-image:linear-gradient(180deg,#000 60%,rgba(0,0,0,.35) 100%)}
.power #qfw{filter:drop-shadow(0 0 1.5px rgba(255,255,255,.55))}
.lap{display:none}.power .lap{display:block}
.sky .w{fill:#f2c14e}
.power .qfig{left:250px;right:250px;bottom:150px}
.power .safe .qfig{left:230px;right:300px}
/* カウントダウン：右下の赤い数字がドクンドクン */
#pulse,.bignum{display:none!important}
.cnum{color:#e53935!important;text-shadow:0 0 24px rgba(229,57,53,.45)}
.ring #rfg{stroke:#e53935!important;filter:drop-shadow(0 0 8px rgba(229,57,53,.5))!important}
'''

LAP = r'''<svg class="lap" viewBox="0 0 600 640" style="position:absolute;left:0;top:0;width:100%;overflow:visible">
<defs><linearGradient id="skinL" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6d3b3"/><stop offset="1" stop-color="#e2ad86"/></linearGradient>
<linearGradient id="lid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfd5de"/><stop offset="1" stop-color="#9aa3b0"/></linearGradient></defs>
<path d="M150 470 L450 470 L470 610 L130 610 Z" fill="url(#lid)" stroke="#6b7482" stroke-width="2.4"/>
<path d="M100 610 L500 610 L520 628 L80 628 Z" fill="#8a93a0" stroke="#6b7482" stroke-width="2"/>
<circle cx="300" cy="538" r="22" fill="none" stroke="#f2c14e" stroke-width="3"/><path d="M280 538 H320 M300 518 V558 M286 526 Q300 538 286 550 M314 526 Q300 538 314 550" stroke="#f2c14e" stroke-width="2" fill="none"/>
<g id="hl"><path d="M120 640 Q140 604 170 600 L200 604 Q206 614 196 620 L150 640 Z" fill="#14254f" stroke="#d9b866" stroke-width="2"/><ellipse cx="200" cy="608" rx="30" ry="16" fill="url(#skinL)" stroke="#b9805c" stroke-width="2.2"/></g><g id="hr"><path d="M480 640 Q460 604 430 600 L400 604 Q394 614 404 620 L450 640 Z" fill="#14254f" stroke="#d9b866" stroke-width="2"/><ellipse cx="400" cy="608" rx="30" ry="16" fill="url(#skinL)" stroke="#b9805c" stroke-width="2.2"/></g></svg>'''

SKY = r'''<svg class="sky" viewBox="0 0 1080 760" preserveAspectRatio="xMidYMax slice"><defs><linearGradient id="bld" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#132a5e"/><stop offset="1" stop-color="#050d24"/></linearGradient><linearGradient id="bld2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a3672"/><stop offset="1" stop-color="#06102a"/></linearGradient></defs><rect x="-20" y="463" width="101" height="297" fill="url(#bld)"/><rect x="-20" y="463" width="101" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="-10" y="481" width="8" height="12" opacity="0.28" data-p="5.16"/><rect class="w" x="8" y="481" width="8" height="12" opacity="0.63" data-p="5.71"/><rect class="w" x="26" y="481" width="8" height="12" opacity="0.31" data-p="2.63"/><rect class="w" x="44" y="481" width="8" height="12" opacity="0.61" data-p="0.37"/><rect class="w" x="44" y="507" width="8" height="12" opacity="0.63" data-p="0.31"/><rect class="w" x="62" y="507" width="8" height="12" opacity="0.61" data-p="0.84"/><rect class="w" x="-10" y="533" width="8" height="12" opacity="0.6" data-p="3.59"/><rect class="w" x="44" y="533" width="8" height="12" opacity="0.62" data-p="1.18"/><rect class="w" x="62" y="533" width="8" height="12" opacity="0.71" data-p="3.54"/><rect class="w" x="8" y="585" width="8" height="12" opacity="0.41" data-p="1.13"/><rect class="w" x="44" y="585" width="8" height="12" opacity="0.45" data-p="3.11"/><rect class="w" x="62" y="585" width="8" height="12" opacity="0.54" data-p="3.82"/><rect class="w" x="-10" y="611" width="8" height="12" opacity="0.58" data-p="1.04"/><rect class="w" x="8" y="611" width="8" height="12" opacity="0.86" data-p="2.65"/><rect class="w" x="44" y="611" width="8" height="12" opacity="0.61" data-p="4.96"/><rect class="w" x="-10" y="637" width="8" height="12" opacity="0.48" data-p="3.12"/><rect class="w" x="26" y="637" width="8" height="12" opacity="0.31" data-p="1.70"/><rect class="w" x="62" y="637" width="8" height="12" opacity="0.73" data-p="1.94"/><rect class="w" x="26" y="663" width="8" height="12" opacity="0.72" data-p="5.57"/><rect class="w" x="44" y="663" width="8" height="12" opacity="0.86" data-p="2.23"/><rect class="w" x="8" y="689" width="8" height="12" opacity="0.44" data-p="4.64"/><rect class="w" x="26" y="689" width="8" height="12" opacity="0.85" data-p="3.12"/><rect class="w" x="44" y="689" width="8" height="12" opacity="0.51" data-p="1.74"/><rect class="w" x="62" y="689" width="8" height="12" opacity="0.53" data-p="3.46"/><rect class="w" x="44" y="715" width="8" height="12" opacity="0.4" data-p="0.52"/><rect class="w" x="62" y="715" width="8" height="12" opacity="0.68" data-p="0.08"/><rect class="w" x="8" y="741" width="8" height="12" opacity="0.43" data-p="0.91"/><rect class="w" x="62" y="741" width="8" height="12" opacity="0.33" data-p="5.40"/><rect x="94" y="307" width="66" height="453" fill="url(#bld)"/><rect x="94" y="307" width="66" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="122" y="351" width="8" height="12" opacity="0.51" data-p="0.65"/><rect class="w" x="104" y="377" width="8" height="12" opacity="0.29" data-p="1.31"/><rect class="w" x="122" y="377" width="8" height="12" opacity="0.47" data-p="0.33"/><rect class="w" x="140" y="377" width="8" height="12" opacity="0.35" data-p="0.64"/><rect class="w" x="104" y="403" width="8" height="12" opacity="0.27" data-p="5.49"/><rect class="w" x="140" y="403" width="8" height="12" opacity="0.41" data-p="2.18"/><rect class="w" x="104" y="429" width="8" height="12" opacity="0.33" data-p="5.33"/><rect class="w" x="122" y="455" width="8" height="12" opacity="0.32" data-p="2.15"/><rect class="w" x="140" y="455" width="8" height="12" opacity="0.79" data-p="1.01"/><rect class="w" x="104" y="481" width="8" height="12" opacity="0.87" data-p="3.32"/><rect class="w" x="122" y="481" width="8" height="12" opacity="0.6" data-p="0.17"/><rect class="w" x="104" y="533" width="8" height="12" opacity="0.49" data-p="1.05"/><rect class="w" x="122" y="559" width="8" height="12" opacity="0.39" data-p="5.10"/><rect class="w" x="122" y="611" width="8" height="12" opacity="0.59" data-p="2.23"/><rect class="w" x="140" y="611" width="8" height="12" opacity="0.27" data-p="1.75"/><rect class="w" x="104" y="637" width="8" height="12" opacity="0.7" data-p="6.01"/><rect class="w" x="122" y="637" width="8" height="12" opacity="0.86" data-p="6.20"/><rect class="w" x="104" y="663" width="8" height="12" opacity="0.39" data-p="1.42"/><rect class="w" x="122" y="663" width="8" height="12" opacity="0.38" data-p="3.92"/><rect class="w" x="122" y="715" width="8" height="12" opacity="0.68" data-p="5.71"/><rect class="w" x="140" y="741" width="8" height="12" opacity="0.76" data-p="2.09"/><rect x="170" y="335" width="119" height="425" fill="url(#bld)"/><rect x="170" y="335" width="119" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="198" y="353" width="8" height="12" opacity="0.35" data-p="6.24"/><rect class="w" x="216" y="353" width="8" height="12" opacity="0.63" data-p="2.92"/><rect class="w" x="216" y="379" width="8" height="12" opacity="0.61" data-p="0.13"/><rect class="w" x="270" y="379" width="8" height="12" opacity="0.74" data-p="0.87"/><rect class="w" x="198" y="405" width="8" height="12" opacity="0.82" data-p="0.18"/><rect class="w" x="216" y="405" width="8" height="12" opacity="0.58" data-p="4.80"/><rect class="w" x="234" y="405" width="8" height="12" opacity="0.6" data-p="5.24"/><rect class="w" x="252" y="405" width="8" height="12" opacity="0.73" data-p="5.64"/><rect class="w" x="252" y="431" width="8" height="12" opacity="0.35" data-p="3.21"/><rect class="w" x="234" y="457" width="8" height="12" opacity="0.34" data-p="3.89"/><rect class="w" x="252" y="457" width="8" height="12" opacity="0.29" data-p="4.29"/><rect class="w" x="234" y="483" width="8" height="12" opacity="0.37" data-p="0.27"/><rect class="w" x="252" y="483" width="8" height="12" opacity="0.54" data-p="0.17"/><rect class="w" x="180" y="509" width="8" height="12" opacity="0.46" data-p="6.11"/><rect class="w" x="216" y="509" width="8" height="12" opacity="0.43" data-p="3.19"/><rect class="w" x="270" y="509" width="8" height="12" opacity="0.59" data-p="5.50"/><rect class="w" x="234" y="535" width="8" height="12" opacity="0.54" data-p="2.62"/><rect class="w" x="252" y="535" width="8" height="12" opacity="0.46" data-p="4.21"/><rect class="w" x="270" y="535" width="8" height="12" opacity="0.39" data-p="1.90"/><rect class="w" x="180" y="561" width="8" height="12" opacity="0.76" data-p="5.90"/><rect class="w" x="216" y="561" width="8" height="12" opacity="0.41" data-p="0.86"/><rect class="w" x="270" y="561" width="8" height="12" opacity="0.83" data-p="1.02"/><rect class="w" x="198" y="587" width="8" height="12" opacity="0.71" data-p="6.24"/><rect class="w" x="216" y="587" width="8" height="12" opacity="0.52" data-p="2.24"/><rect class="w" x="234" y="587" width="8" height="12" opacity="0.49" data-p="2.12"/><rect class="w" x="180" y="613" width="8" height="12" opacity="0.59" data-p="1.86"/><rect class="w" x="216" y="613" width="8" height="12" opacity="0.85" data-p="1.44"/><rect class="w" x="252" y="613" width="8" height="12" opacity="0.43" data-p="5.69"/><rect class="w" x="270" y="613" width="8" height="12" opacity="0.74" data-p="5.15"/><rect class="w" x="234" y="639" width="8" height="12" opacity="0.6" data-p="3.23"/><rect class="w" x="270" y="639" width="8" height="12" opacity="0.43" data-p="5.02"/><rect class="w" x="180" y="665" width="8" height="12" opacity="0.83" data-p="1.69"/><rect class="w" x="198" y="665" width="8" height="12" opacity="0.31" data-p="1.64"/><rect class="w" x="234" y="665" width="8" height="12" opacity="0.42" data-p="0.76"/><rect class="w" x="252" y="665" width="8" height="12" opacity="0.9" data-p="2.62"/><rect class="w" x="198" y="691" width="8" height="12" opacity="0.71" data-p="5.89"/><rect class="w" x="234" y="691" width="8" height="12" opacity="0.37" data-p="5.85"/><rect class="w" x="180" y="717" width="8" height="12" opacity="0.54" data-p="4.22"/><rect class="w" x="198" y="717" width="8" height="12" opacity="0.77" data-p="6.25"/><rect class="w" x="216" y="717" width="8" height="12" opacity="0.26" data-p="3.18"/><rect class="w" x="270" y="717" width="8" height="12" opacity="0.54" data-p="4.13"/><rect class="w" x="270" y="743" width="8" height="12" opacity="0.39" data-p="1.44"/><rect x="296" y="333" width="77" height="427" fill="url(#bld)"/><rect x="296" y="333" width="77" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="360" y="351" width="8" height="12" opacity="0.66" data-p="5.53"/><rect class="w" x="306" y="377" width="8" height="12" opacity="0.29" data-p="4.18"/><rect class="w" x="324" y="377" width="8" height="12" opacity="0.58" data-p="6.10"/><rect class="w" x="306" y="403" width="8" height="12" opacity="0.37" data-p="1.69"/><rect class="w" x="324" y="403" width="8" height="12" opacity="0.49" data-p="2.07"/><rect class="w" x="360" y="403" width="8" height="12" opacity="0.27" data-p="5.54"/><rect class="w" x="306" y="429" width="8" height="12" opacity="0.37" data-p="2.11"/><rect class="w" x="324" y="429" width="8" height="12" opacity="0.43" data-p="4.12"/><rect class="w" x="342" y="429" width="8" height="12" opacity="0.75" data-p="0.57"/><rect class="w" x="306" y="455" width="8" height="12" opacity="0.63" data-p="2.47"/><rect class="w" x="324" y="455" width="8" height="12" opacity="0.66" data-p="0.53"/><rect class="w" x="306" y="481" width="8" height="12" opacity="0.83" data-p="4.92"/><rect class="w" x="324" y="507" width="8" height="12" opacity="0.65" data-p="0.91"/><rect class="w" x="324" y="533" width="8" height="12" opacity="0.71" data-p="3.17"/><rect class="w" x="342" y="559" width="8" height="12" opacity="0.7" data-p="5.01"/><rect class="w" x="342" y="585" width="8" height="12" opacity="0.28" data-p="4.00"/><rect class="w" x="306" y="611" width="8" height="12" opacity="0.54" data-p="0.32"/><rect class="w" x="324" y="611" width="8" height="12" opacity="0.6" data-p="1.54"/><rect class="w" x="342" y="611" width="8" height="12" opacity="0.55" data-p="0.44"/><rect class="w" x="324" y="637" width="8" height="12" opacity="0.59" data-p="4.68"/><rect class="w" x="324" y="663" width="8" height="12" opacity="0.74" data-p="1.45"/><rect class="w" x="324" y="689" width="8" height="12" opacity="0.84" data-p="1.80"/><rect class="w" x="342" y="689" width="8" height="12" opacity="0.66" data-p="1.25"/><rect class="w" x="306" y="715" width="8" height="12" opacity="0.67" data-p="4.35"/><rect class="w" x="342" y="715" width="8" height="12" opacity="0.56" data-p="3.05"/><rect class="w" x="306" y="741" width="8" height="12" opacity="0.39" data-p="3.07"/><rect class="w" x="342" y="741" width="8" height="12" opacity="0.55" data-p="4.82"/><rect x="385" y="381" width="85" height="379" fill="url(#bld)"/><rect x="385" y="381" width="85" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="431" y="399" width="8" height="12" opacity="0.55" data-p="5.15"/><rect class="w" x="395" y="425" width="8" height="12" opacity="0.42" data-p="1.32"/><rect class="w" x="431" y="425" width="8" height="12" opacity="0.63" data-p="0.89"/><rect class="w" x="413" y="451" width="8" height="12" opacity="0.78" data-p="3.19"/><rect class="w" x="395" y="477" width="8" height="12" opacity="0.83" data-p="3.05"/><rect class="w" x="413" y="477" width="8" height="12" opacity="0.25" data-p="3.09"/><rect class="w" x="449" y="477" width="8" height="12" opacity="0.34" data-p="2.16"/><rect class="w" x="395" y="503" width="8" height="12" opacity="0.8" data-p="0.01"/><rect class="w" x="449" y="503" width="8" height="12" opacity="0.85" data-p="4.48"/><rect class="w" x="413" y="529" width="8" height="12" opacity="0.49" data-p="2.47"/><rect class="w" x="395" y="555" width="8" height="12" opacity="0.53" data-p="1.73"/><rect class="w" x="413" y="555" width="8" height="12" opacity="0.32" data-p="5.24"/><rect class="w" x="431" y="555" width="8" height="12" opacity="0.86" data-p="1.57"/><rect class="w" x="449" y="555" width="8" height="12" opacity="0.58" data-p="1.19"/><rect class="w" x="395" y="581" width="8" height="12" opacity="0.87" data-p="5.55"/><rect class="w" x="449" y="607" width="8" height="12" opacity="0.73" data-p="2.83"/><rect class="w" x="431" y="633" width="8" height="12" opacity="0.28" data-p="5.82"/><rect class="w" x="449" y="633" width="8" height="12" opacity="0.56" data-p="2.16"/><rect class="w" x="395" y="659" width="8" height="12" opacity="0.73" data-p="6.13"/><rect class="w" x="413" y="659" width="8" height="12" opacity="0.68" data-p="1.89"/><rect class="w" x="449" y="659" width="8" height="12" opacity="0.36" data-p="1.02"/><rect class="w" x="395" y="685" width="8" height="12" opacity="0.84" data-p="3.12"/><rect class="w" x="413" y="685" width="8" height="12" opacity="0.84" data-p="6.26"/><rect class="w" x="431" y="685" width="8" height="12" opacity="0.34" data-p="1.21"/><rect class="w" x="449" y="685" width="8" height="12" opacity="0.47" data-p="0.57"/><rect class="w" x="395" y="711" width="8" height="12" opacity="0.42" data-p="3.58"/><rect class="w" x="449" y="711" width="8" height="12" opacity="0.52" data-p="3.29"/><rect class="w" x="395" y="737" width="8" height="12" opacity="0.47" data-p="0.39"/><rect class="w" x="413" y="737" width="8" height="12" opacity="0.88" data-p="0.79"/><rect x="477" y="402" width="71" height="358" fill="url(#bld)"/><rect x="477" y="402" width="71" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="505" y="420" width="8" height="12" opacity="0.67" data-p="2.71"/><rect class="w" x="523" y="420" width="8" height="12" opacity="0.78" data-p="6.08"/><rect class="w" x="487" y="446" width="8" height="12" opacity="0.53" data-p="4.80"/><rect class="w" x="505" y="472" width="8" height="12" opacity="0.85" data-p="5.83"/><rect class="w" x="505" y="498" width="8" height="12" opacity="0.76" data-p="1.41"/><rect class="w" x="523" y="498" width="8" height="12" opacity="0.88" data-p="0.68"/><rect class="w" x="505" y="550" width="8" height="12" opacity="0.75" data-p="0.01"/><rect class="w" x="523" y="550" width="8" height="12" opacity="0.62" data-p="0.24"/><rect class="w" x="505" y="602" width="8" height="12" opacity="0.75" data-p="0.62"/><rect class="w" x="523" y="602" width="8" height="12" opacity="0.86" data-p="1.20"/><rect class="w" x="487" y="628" width="8" height="12" opacity="0.76" data-p="0.01"/><rect class="w" x="487" y="654" width="8" height="12" opacity="0.46" data-p="5.27"/><rect class="w" x="505" y="654" width="8" height="12" opacity="0.59" data-p="3.44"/><rect class="w" x="523" y="654" width="8" height="12" opacity="0.52" data-p="4.08"/><rect class="w" x="487" y="680" width="8" height="12" opacity="0.38" data-p="5.56"/><rect class="w" x="523" y="680" width="8" height="12" opacity="0.4" data-p="2.66"/><rect class="w" x="487" y="706" width="8" height="12" opacity="0.57" data-p="4.37"/><rect class="w" x="523" y="706" width="8" height="12" opacity="0.51" data-p="0.04"/><rect class="w" x="487" y="732" width="8" height="12" opacity="0.8" data-p="0.42"/><rect class="w" x="523" y="732" width="8" height="12" opacity="0.75" data-p="1.22"/><rect x="559" y="405" width="88" height="355" fill="url(#bld)"/><rect x="559" y="405" width="88" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="587" y="423" width="8" height="12" opacity="0.87" data-p="3.11"/><rect class="w" x="605" y="423" width="8" height="12" opacity="0.4" data-p="2.62"/><rect class="w" x="587" y="449" width="8" height="12" opacity="0.51" data-p="1.34"/><rect class="w" x="623" y="449" width="8" height="12" opacity="0.28" data-p="0.38"/><rect class="w" x="569" y="475" width="8" height="12" opacity="0.83" data-p="5.55"/><rect class="w" x="569" y="501" width="8" height="12" opacity="0.37" data-p="5.88"/><rect class="w" x="605" y="501" width="8" height="12" opacity="0.68" data-p="2.38"/><rect class="w" x="623" y="501" width="8" height="12" opacity="0.47" data-p="1.06"/><rect class="w" x="569" y="527" width="8" height="12" opacity="0.43" data-p="2.21"/><rect class="w" x="605" y="527" width="8" height="12" opacity="0.88" data-p="1.30"/><rect class="w" x="623" y="527" width="8" height="12" opacity="0.78" data-p="5.16"/><rect class="w" x="569" y="553" width="8" height="12" opacity="0.28" data-p="2.97"/><rect class="w" x="587" y="553" width="8" height="12" opacity="0.85" data-p="1.21"/><rect class="w" x="605" y="553" width="8" height="12" opacity="0.83" data-p="0.19"/><rect class="w" x="623" y="553" width="8" height="12" opacity="0.78" data-p="4.81"/><rect class="w" x="569" y="579" width="8" height="12" opacity="0.27" data-p="0.39"/><rect class="w" x="605" y="579" width="8" height="12" opacity="0.74" data-p="5.64"/><rect class="w" x="623" y="579" width="8" height="12" opacity="0.43" data-p="6.01"/><rect class="w" x="587" y="605" width="8" height="12" opacity="0.72" data-p="1.99"/><rect class="w" x="605" y="605" width="8" height="12" opacity="0.25" data-p="4.75"/><rect class="w" x="605" y="631" width="8" height="12" opacity="0.4" data-p="2.98"/><rect class="w" x="587" y="657" width="8" height="12" opacity="0.41" data-p="2.70"/><rect class="w" x="569" y="683" width="8" height="12" opacity="0.77" data-p="4.64"/><rect class="w" x="569" y="709" width="8" height="12" opacity="0.46" data-p="2.27"/><rect class="w" x="605" y="709" width="8" height="12" opacity="0.38" data-p="4.73"/><rect class="w" x="623" y="709" width="8" height="12" opacity="0.29" data-p="0.21"/><rect class="w" x="587" y="735" width="8" height="12" opacity="0.89" data-p="5.55"/><rect class="w" x="623" y="735" width="8" height="12" opacity="0.3" data-p="0.61"/><rect x="658" y="452" width="117" height="308" fill="url(#bld)"/><rect x="658" y="452" width="117" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="668" y="470" width="8" height="12" opacity="0.52" data-p="3.90"/><rect class="w" x="758" y="470" width="8" height="12" opacity="0.8" data-p="1.84"/><rect class="w" x="686" y="496" width="8" height="12" opacity="0.73" data-p="1.25"/><rect class="w" x="704" y="496" width="8" height="12" opacity="0.41" data-p="0.96"/><rect class="w" x="758" y="496" width="8" height="12" opacity="0.51" data-p="6.23"/><rect class="w" x="686" y="522" width="8" height="12" opacity="0.78" data-p="4.10"/><rect class="w" x="722" y="522" width="8" height="12" opacity="0.56" data-p="5.14"/><rect class="w" x="668" y="548" width="8" height="12" opacity="0.44" data-p="0.75"/><rect class="w" x="686" y="548" width="8" height="12" opacity="0.88" data-p="3.66"/><rect class="w" x="722" y="548" width="8" height="12" opacity="0.81" data-p="2.82"/><rect class="w" x="740" y="548" width="8" height="12" opacity="0.76" data-p="5.94"/><rect class="w" x="758" y="548" width="8" height="12" opacity="0.64" data-p="3.89"/><rect class="w" x="668" y="574" width="8" height="12" opacity="0.49" data-p="0.89"/><rect class="w" x="686" y="574" width="8" height="12" opacity="0.42" data-p="3.76"/><rect class="w" x="722" y="574" width="8" height="12" opacity="0.26" data-p="2.06"/><rect class="w" x="758" y="574" width="8" height="12" opacity="0.45" data-p="1.28"/><rect class="w" x="704" y="600" width="8" height="12" opacity="0.32" data-p="2.48"/><rect class="w" x="758" y="600" width="8" height="12" opacity="0.36" data-p="4.37"/><rect class="w" x="668" y="626" width="8" height="12" opacity="0.43" data-p="1.93"/><rect class="w" x="704" y="626" width="8" height="12" opacity="0.62" data-p="2.24"/><rect class="w" x="722" y="626" width="8" height="12" opacity="0.81" data-p="6.26"/><rect class="w" x="740" y="626" width="8" height="12" opacity="0.38" data-p="4.57"/><rect class="w" x="758" y="626" width="8" height="12" opacity="0.25" data-p="5.66"/><rect class="w" x="668" y="652" width="8" height="12" opacity="0.78" data-p="2.55"/><rect class="w" x="722" y="652" width="8" height="12" opacity="0.26" data-p="3.46"/><rect class="w" x="668" y="678" width="8" height="12" opacity="0.65" data-p="2.33"/><rect class="w" x="704" y="678" width="8" height="12" opacity="0.43" data-p="3.27"/><rect class="w" x="740" y="678" width="8" height="12" opacity="0.57" data-p="5.05"/><rect class="w" x="668" y="704" width="8" height="12" opacity="0.33" data-p="5.92"/><rect class="w" x="722" y="704" width="8" height="12" opacity="0.85" data-p="2.44"/><rect class="w" x="686" y="730" width="8" height="12" opacity="0.76" data-p="1.39"/><rect class="w" x="704" y="730" width="8" height="12" opacity="0.8" data-p="5.21"/><rect class="w" x="722" y="730" width="8" height="12" opacity="0.39" data-p="2.51"/><rect class="w" x="758" y="730" width="8" height="12" opacity="0.33" data-p="1.55"/><rect x="782" y="253" width="65" height="507" fill="url(#bld)"/><rect x="782" y="253" width="65" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="792" y="297" width="8" height="12" opacity="0.5" data-p="2.86"/><rect class="w" x="810" y="323" width="8" height="12" opacity="0.41" data-p="2.44"/><rect class="w" x="828" y="323" width="8" height="12" opacity="0.58" data-p="1.12"/><rect class="w" x="792" y="349" width="8" height="12" opacity="0.89" data-p="2.92"/><rect class="w" x="810" y="349" width="8" height="12" opacity="0.65" data-p="5.14"/><rect class="w" x="810" y="375" width="8" height="12" opacity="0.29" data-p="2.25"/><rect class="w" x="828" y="375" width="8" height="12" opacity="0.77" data-p="3.17"/><rect class="w" x="810" y="401" width="8" height="12" opacity="0.33" data-p="5.79"/><rect class="w" x="828" y="401" width="8" height="12" opacity="0.72" data-p="0.50"/><rect class="w" x="810" y="453" width="8" height="12" opacity="0.29" data-p="3.86"/><rect class="w" x="792" y="479" width="8" height="12" opacity="0.34" data-p="5.56"/><rect class="w" x="810" y="479" width="8" height="12" opacity="0.78" data-p="4.99"/><rect class="w" x="810" y="505" width="8" height="12" opacity="0.79" data-p="3.83"/><rect class="w" x="828" y="505" width="8" height="12" opacity="0.46" data-p="3.85"/><rect class="w" x="828" y="531" width="8" height="12" opacity="0.88" data-p="3.02"/><rect class="w" x="828" y="557" width="8" height="12" opacity="0.49" data-p="1.25"/><rect class="w" x="792" y="583" width="8" height="12" opacity="0.66" data-p="1.75"/><rect class="w" x="810" y="583" width="8" height="12" opacity="0.49" data-p="4.97"/><rect class="w" x="828" y="583" width="8" height="12" opacity="0.75" data-p="0.31"/><rect class="w" x="792" y="661" width="8" height="12" opacity="0.6" data-p="5.38"/><rect class="w" x="828" y="661" width="8" height="12" opacity="0.49" data-p="2.32"/><rect class="w" x="792" y="687" width="8" height="12" opacity="0.47" data-p="0.51"/><rect class="w" x="810" y="687" width="8" height="12" opacity="0.65" data-p="6.02"/><rect class="w" x="828" y="687" width="8" height="12" opacity="0.59" data-p="1.95"/><rect x="854" y="392" width="79" height="368" fill="url(#bld)"/><rect x="854" y="392" width="79" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="882" y="410" width="8" height="12" opacity="0.58" data-p="5.62"/><rect class="w" x="900" y="410" width="8" height="12" opacity="0.4" data-p="4.10"/><rect class="w" x="918" y="410" width="8" height="12" opacity="0.25" data-p="2.23"/><rect class="w" x="864" y="436" width="8" height="12" opacity="0.48" data-p="1.41"/><rect class="w" x="918" y="436" width="8" height="12" opacity="0.66" data-p="2.98"/><rect class="w" x="864" y="462" width="8" height="12" opacity="0.86" data-p="1.53"/><rect class="w" x="882" y="462" width="8" height="12" opacity="0.31" data-p="4.01"/><rect class="w" x="864" y="488" width="8" height="12" opacity="0.42" data-p="0.07"/><rect class="w" x="918" y="488" width="8" height="12" opacity="0.67" data-p="2.79"/><rect class="w" x="900" y="514" width="8" height="12" opacity="0.84" data-p="0.28"/><rect class="w" x="864" y="540" width="8" height="12" opacity="0.4" data-p="0.37"/><rect class="w" x="900" y="540" width="8" height="12" opacity="0.61" data-p="5.91"/><rect class="w" x="918" y="540" width="8" height="12" opacity="0.38" data-p="3.82"/><rect class="w" x="918" y="566" width="8" height="12" opacity="0.45" data-p="1.89"/><rect class="w" x="864" y="592" width="8" height="12" opacity="0.83" data-p="4.92"/><rect class="w" x="900" y="592" width="8" height="12" opacity="0.8" data-p="4.68"/><rect class="w" x="900" y="618" width="8" height="12" opacity="0.32" data-p="1.46"/><rect class="w" x="918" y="618" width="8" height="12" opacity="0.47" data-p="4.71"/><rect class="w" x="918" y="644" width="8" height="12" opacity="0.61" data-p="2.74"/><rect class="w" x="900" y="670" width="8" height="12" opacity="0.67" data-p="6.06"/><rect class="w" x="918" y="670" width="8" height="12" opacity="0.82" data-p="0.10"/><rect class="w" x="864" y="696" width="8" height="12" opacity="0.4" data-p="4.67"/><rect class="w" x="918" y="696" width="8" height="12" opacity="0.82" data-p="2.06"/><rect class="w" x="864" y="722" width="8" height="12" opacity="0.84" data-p="3.96"/><rect x="943" y="248" width="89" height="512" fill="url(#bld)"/><rect x="943" y="248" width="89" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="989" y="266" width="8" height="12" opacity="0.63" data-p="3.55"/><rect class="w" x="1007" y="266" width="8" height="12" opacity="0.27" data-p="0.70"/><rect class="w" x="971" y="292" width="8" height="12" opacity="0.89" data-p="4.40"/><rect class="w" x="989" y="292" width="8" height="12" opacity="0.34" data-p="4.04"/><rect class="w" x="1007" y="292" width="8" height="12" opacity="0.29" data-p="0.29"/><rect class="w" x="989" y="318" width="8" height="12" opacity="0.87" data-p="3.35"/><rect class="w" x="1007" y="344" width="8" height="12" opacity="0.41" data-p="1.28"/><rect class="w" x="953" y="370" width="8" height="12" opacity="0.87" data-p="5.72"/><rect class="w" x="989" y="370" width="8" height="12" opacity="0.74" data-p="3.97"/><rect class="w" x="953" y="396" width="8" height="12" opacity="0.76" data-p="4.06"/><rect class="w" x="971" y="396" width="8" height="12" opacity="0.47" data-p="1.64"/><rect class="w" x="989" y="396" width="8" height="12" opacity="0.85" data-p="0.30"/><rect class="w" x="953" y="448" width="8" height="12" opacity="0.73" data-p="4.96"/><rect class="w" x="971" y="448" width="8" height="12" opacity="0.59" data-p="0.62"/><rect class="w" x="1007" y="448" width="8" height="12" opacity="0.62" data-p="4.49"/><rect class="w" x="989" y="474" width="8" height="12" opacity="0.53" data-p="3.29"/><rect class="w" x="1007" y="474" width="8" height="12" opacity="0.74" data-p="0.34"/><rect class="w" x="953" y="500" width="8" height="12" opacity="0.31" data-p="4.37"/><rect class="w" x="1007" y="526" width="8" height="12" opacity="0.78" data-p="5.89"/><rect class="w" x="953" y="552" width="8" height="12" opacity="0.36" data-p="5.90"/><rect class="w" x="971" y="578" width="8" height="12" opacity="0.46" data-p="0.60"/><rect class="w" x="971" y="604" width="8" height="12" opacity="0.67" data-p="2.34"/><rect class="w" x="989" y="604" width="8" height="12" opacity="0.53" data-p="3.42"/><rect class="w" x="1007" y="604" width="8" height="12" opacity="0.89" data-p="3.96"/><rect class="w" x="971" y="630" width="8" height="12" opacity="0.64" data-p="4.33"/><rect class="w" x="1007" y="630" width="8" height="12" opacity="0.63" data-p="3.28"/><rect class="w" x="1007" y="656" width="8" height="12" opacity="0.55" data-p="4.33"/><rect class="w" x="953" y="682" width="8" height="12" opacity="0.4" data-p="2.10"/><rect class="w" x="953" y="708" width="8" height="12" opacity="0.74" data-p="5.19"/><rect class="w" x="989" y="734" width="8" height="12" opacity="0.4" data-p="6.00"/><rect class="w" x="1007" y="734" width="8" height="12" opacity="0.87" data-p="6.25"/><rect x="1038" y="440" width="73" height="320" fill="url(#bld)"/><rect x="1038" y="440" width="73" height="3" fill="rgba(242,193,78,.55)"/><rect class="w" x="1048" y="458" width="8" height="12" opacity="0.89" data-p="4.99"/><rect class="w" x="1084" y="458" width="8" height="12" opacity="0.38" data-p="4.01"/><rect class="w" x="1048" y="484" width="8" height="12" opacity="0.38" data-p="2.44"/><rect class="w" x="1066" y="484" width="8" height="12" opacity="0.51" data-p="4.97"/><rect class="w" x="1048" y="536" width="8" height="12" opacity="0.64" data-p="2.54"/><rect class="w" x="1048" y="562" width="8" height="12" opacity="0.62" data-p="4.70"/><rect class="w" x="1066" y="562" width="8" height="12" opacity="0.4" data-p="4.54"/><rect class="w" x="1048" y="640" width="8" height="12" opacity="0.66" data-p="0.61"/><rect class="w" x="1066" y="640" width="8" height="12" opacity="0.76" data-p="4.48"/><rect class="w" x="1048" y="666" width="8" height="12" opacity="0.53" data-p="2.86"/><rect class="w" x="1084" y="666" width="8" height="12" opacity="0.69" data-p="5.84"/><rect class="w" x="1048" y="692" width="8" height="12" opacity="0.68" data-p="4.89"/><rect class="w" x="1066" y="692" width="8" height="12" opacity="0.57" data-p="6.12"/><rect class="w" x="1084" y="692" width="8" height="12" opacity="0.6" data-p="1.01"/><rect class="w" x="1048" y="744" width="8" height="12" opacity="0.62" data-p="3.40"/><rect x="110" y="140" width="140" height="620" fill="url(#bld2)"/><rect class="w" x="138" y="158" width="8" height="12" opacity="0.47" data-p="4.66"/><rect class="w" x="192" y="158" width="8" height="12" opacity="0.58" data-p="5.86"/><rect class="w" x="138" y="184" width="8" height="12" opacity="0.5" data-p="0.39"/><rect class="w" x="156" y="184" width="8" height="12" opacity="0.85" data-p="3.95"/><rect class="w" x="210" y="184" width="8" height="12" opacity="0.45" data-p="2.51"/><rect class="w" x="192" y="210" width="8" height="12" opacity="0.85" data-p="0.43"/><rect class="w" x="228" y="210" width="8" height="12" opacity="0.67" data-p="4.53"/><rect class="w" x="138" y="236" width="8" height="12" opacity="0.68" data-p="5.22"/><rect class="w" x="174" y="236" width="8" height="12" opacity="0.9" data-p="4.77"/><rect class="w" x="138" y="262" width="8" height="12" opacity="0.71" data-p="4.32"/><rect class="w" x="120" y="288" width="8" height="12" opacity="0.68" data-p="2.01"/><rect class="w" x="174" y="288" width="8" height="12" opacity="0.83" data-p="0.96"/><rect class="w" x="192" y="288" width="8" height="12" opacity="0.5" data-p="0.54"/><rect class="w" x="228" y="288" width="8" height="12" opacity="0.86" data-p="3.33"/><rect class="w" x="120" y="314" width="8" height="12" opacity="0.63" data-p="4.13"/><rect class="w" x="138" y="314" width="8" height="12" opacity="0.3" data-p="1.84"/><rect class="w" x="210" y="314" width="8" height="12" opacity="0.54" data-p="4.93"/><rect class="w" x="228" y="314" width="8" height="12" opacity="0.51" data-p="3.36"/><rect class="w" x="174" y="340" width="8" height="12" opacity="0.84" data-p="3.44"/><rect class="w" x="210" y="340" width="8" height="12" opacity="0.57" data-p="1.34"/><rect class="w" x="228" y="340" width="8" height="12" opacity="0.8" data-p="4.22"/><rect class="w" x="120" y="366" width="8" height="12" opacity="0.33" data-p="2.63"/><rect class="w" x="120" y="392" width="8" height="12" opacity="0.36" data-p="3.77"/><rect class="w" x="156" y="392" width="8" height="12" opacity="0.46" data-p="4.37"/><rect class="w" x="192" y="392" width="8" height="12" opacity="0.55" data-p="2.67"/><rect class="w" x="120" y="418" width="8" height="12" opacity="0.48" data-p="4.06"/><rect class="w" x="138" y="418" width="8" height="12" opacity="0.28" data-p="4.63"/><rect class="w" x="192" y="418" width="8" height="12" opacity="0.56" data-p="4.76"/><rect class="w" x="210" y="418" width="8" height="12" opacity="0.39" data-p="2.61"/><rect class="w" x="228" y="418" width="8" height="12" opacity="0.31" data-p="4.14"/><rect class="w" x="120" y="444" width="8" height="12" opacity="0.76" data-p="3.48"/><rect class="w" x="156" y="444" width="8" height="12" opacity="0.47" data-p="1.58"/><rect class="w" x="174" y="444" width="8" height="12" opacity="0.44" data-p="2.23"/><rect class="w" x="210" y="444" width="8" height="12" opacity="0.89" data-p="5.48"/><rect class="w" x="228" y="444" width="8" height="12" opacity="0.38" data-p="3.09"/><rect class="w" x="120" y="470" width="8" height="12" opacity="0.38" data-p="4.48"/><rect class="w" x="138" y="470" width="8" height="12" opacity="0.88" data-p="0.55"/><rect class="w" x="174" y="470" width="8" height="12" opacity="0.61" data-p="2.55"/><rect class="w" x="210" y="470" width="8" height="12" opacity="0.32" data-p="0.29"/><rect class="w" x="156" y="496" width="8" height="12" opacity="0.58" data-p="3.41"/><rect class="w" x="174" y="496" width="8" height="12" opacity="0.35" data-p="4.23"/><rect class="w" x="228" y="496" width="8" height="12" opacity="0.28" data-p="3.98"/><rect class="w" x="138" y="522" width="8" height="12" opacity="0.68" data-p="5.46"/><rect class="w" x="156" y="522" width="8" height="12" opacity="0.32" data-p="5.84"/><rect class="w" x="174" y="522" width="8" height="12" opacity="0.82" data-p="0.87"/><rect class="w" x="192" y="522" width="8" height="12" opacity="0.71" data-p="5.42"/><rect class="w" x="210" y="522" width="8" height="12" opacity="0.27" data-p="0.13"/><rect class="w" x="228" y="548" width="8" height="12" opacity="0.7" data-p="2.54"/><rect class="w" x="120" y="574" width="8" height="12" opacity="0.69" data-p="3.73"/><rect class="w" x="174" y="574" width="8" height="12" opacity="0.75" data-p="3.45"/><rect class="w" x="192" y="574" width="8" height="12" opacity="0.56" data-p="5.63"/><rect class="w" x="228" y="574" width="8" height="12" opacity="0.26" data-p="4.20"/><rect class="w" x="156" y="600" width="8" height="12" opacity="0.33" data-p="2.97"/><rect class="w" x="174" y="600" width="8" height="12" opacity="0.62" data-p="2.83"/><rect class="w" x="228" y="600" width="8" height="12" opacity="0.74" data-p="4.36"/><rect class="w" x="120" y="626" width="8" height="12" opacity="0.74" data-p="1.84"/><rect class="w" x="228" y="626" width="8" height="12" opacity="0.27" data-p="0.38"/><rect class="w" x="174" y="652" width="8" height="12" opacity="0.45" data-p="3.77"/><rect class="w" x="120" y="678" width="8" height="12" opacity="0.87" data-p="4.57"/><rect class="w" x="156" y="678" width="8" height="12" opacity="0.88" data-p="0.73"/><rect class="w" x="192" y="678" width="8" height="12" opacity="0.77" data-p="3.00"/><rect class="w" x="120" y="704" width="8" height="12" opacity="0.74" data-p="2.10"/><rect class="w" x="138" y="704" width="8" height="12" opacity="0.65" data-p="4.09"/><rect class="w" x="228" y="704" width="8" height="12" opacity="0.35" data-p="5.23"/><rect class="w" x="156" y="730" width="8" height="12" opacity="0.5" data-p="2.36"/><rect class="w" x="192" y="730" width="8" height="12" opacity="0.54" data-p="4.32"/><rect class="w" x="210" y="730" width="8" height="12" opacity="0.42" data-p="0.99"/><rect x="135" y="60" width="90" height="80" fill="url(#bld2)"/><rect class="w" x="181" y="78" width="8" height="12" opacity="0.34" data-p="5.59"/><rect class="w" x="145" y="104" width="8" height="12" opacity="0.88" data-p="5.01"/><rect x="155" y="0" width="50" height="60" fill="url(#bld2)"/><rect class="w" x="183" y="44" width="8" height="12" opacity="0.76" data-p="4.54"/><rect x="177" y="-100" width="6" height="100" fill="#f2c14e" opacity=".8"/><rect x="790" y="190" width="140" height="570" fill="url(#bld2)"/><rect class="w" x="818" y="208" width="8" height="12" opacity="0.29" data-p="2.48"/><rect class="w" x="890" y="208" width="8" height="12" opacity="0.5" data-p="3.39"/><rect class="w" x="800" y="234" width="8" height="12" opacity="0.29" data-p="2.50"/><rect class="w" x="836" y="234" width="8" height="12" opacity="0.79" data-p="2.02"/><rect class="w" x="872" y="234" width="8" height="12" opacity="0.39" data-p="0.58"/><rect class="w" x="908" y="234" width="8" height="12" opacity="0.63" data-p="2.25"/><rect class="w" x="836" y="260" width="8" height="12" opacity="0.85" data-p="3.10"/><rect class="w" x="872" y="260" width="8" height="12" opacity="0.55" data-p="0.51"/><rect class="w" x="890" y="260" width="8" height="12" opacity="0.27" data-p="1.76"/><rect class="w" x="800" y="286" width="8" height="12" opacity="0.38" data-p="5.47"/><rect class="w" x="854" y="286" width="8" height="12" opacity="0.85" data-p="1.76"/><rect class="w" x="872" y="286" width="8" height="12" opacity="0.54" data-p="3.72"/><rect class="w" x="908" y="286" width="8" height="12" opacity="0.8" data-p="2.13"/><rect class="w" x="818" y="312" width="8" height="12" opacity="0.27" data-p="0.22"/><rect class="w" x="836" y="312" width="8" height="12" opacity="0.71" data-p="3.06"/><rect class="w" x="836" y="338" width="8" height="12" opacity="0.46" data-p="1.46"/><rect class="w" x="854" y="338" width="8" height="12" opacity="0.85" data-p="3.18"/><rect class="w" x="872" y="338" width="8" height="12" opacity="0.8" data-p="2.33"/><rect class="w" x="890" y="338" width="8" height="12" opacity="0.72" data-p="1.08"/><rect class="w" x="818" y="364" width="8" height="12" opacity="0.61" data-p="0.17"/><rect class="w" x="854" y="364" width="8" height="12" opacity="0.58" data-p="4.64"/><rect class="w" x="908" y="364" width="8" height="12" opacity="0.46" data-p="0.04"/><rect class="w" x="800" y="390" width="8" height="12" opacity="0.74" data-p="3.70"/><rect class="w" x="818" y="390" width="8" height="12" opacity="0.67" data-p="2.96"/><rect class="w" x="836" y="390" width="8" height="12" opacity="0.5" data-p="2.35"/><rect class="w" x="854" y="390" width="8" height="12" opacity="0.54" data-p="5.07"/><rect class="w" x="836" y="416" width="8" height="12" opacity="0.79" data-p="0.49"/><rect class="w" x="872" y="416" width="8" height="12" opacity="0.74" data-p="4.89"/><rect class="w" x="800" y="442" width="8" height="12" opacity="0.26" data-p="0.47"/><rect class="w" x="836" y="442" width="8" height="12" opacity="0.4" data-p="0.73"/><rect class="w" x="854" y="442" width="8" height="12" opacity="0.47" data-p="4.62"/><rect class="w" x="872" y="442" width="8" height="12" opacity="0.54" data-p="5.58"/><rect class="w" x="890" y="442" width="8" height="12" opacity="0.35" data-p="2.63"/><rect class="w" x="908" y="442" width="8" height="12" opacity="0.27" data-p="3.59"/><rect class="w" x="800" y="468" width="8" height="12" opacity="0.77" data-p="1.64"/><rect class="w" x="818" y="468" width="8" height="12" opacity="0.55" data-p="3.03"/><rect class="w" x="836" y="468" width="8" height="12" opacity="0.58" data-p="3.96"/><rect class="w" x="800" y="494" width="8" height="12" opacity="0.74" data-p="6.10"/><rect class="w" x="818" y="494" width="8" height="12" opacity="0.42" data-p="1.50"/><rect class="w" x="836" y="494" width="8" height="12" opacity="0.5" data-p="2.61"/><rect class="w" x="854" y="494" width="8" height="12" opacity="0.79" data-p="6.15"/><rect class="w" x="872" y="494" width="8" height="12" opacity="0.67" data-p="2.78"/><rect class="w" x="800" y="520" width="8" height="12" opacity="0.76" data-p="5.93"/><rect class="w" x="818" y="520" width="8" height="12" opacity="0.48" data-p="0.25"/><rect class="w" x="836" y="520" width="8" height="12" opacity="0.43" data-p="1.13"/><rect class="w" x="890" y="520" width="8" height="12" opacity="0.36" data-p="3.77"/><rect class="w" x="854" y="546" width="8" height="12" opacity="0.34" data-p="4.21"/><rect class="w" x="890" y="546" width="8" height="12" opacity="0.45" data-p="0.06"/><rect class="w" x="872" y="572" width="8" height="12" opacity="0.43" data-p="4.01"/><rect class="w" x="908" y="572" width="8" height="12" opacity="0.52" data-p="4.79"/><rect class="w" x="800" y="598" width="8" height="12" opacity="0.68" data-p="1.56"/><rect class="w" x="854" y="598" width="8" height="12" opacity="0.71" data-p="3.61"/><rect class="w" x="890" y="598" width="8" height="12" opacity="0.86" data-p="6.08"/><rect class="w" x="908" y="598" width="8" height="12" opacity="0.48" data-p="1.54"/><rect class="w" x="908" y="624" width="8" height="12" opacity="0.32" data-p="4.59"/><rect class="w" x="800" y="650" width="8" height="12" opacity="0.27" data-p="5.05"/><rect class="w" x="818" y="650" width="8" height="12" opacity="0.41" data-p="0.56"/><rect class="w" x="854" y="650" width="8" height="12" opacity="0.45" data-p="3.49"/><rect class="w" x="890" y="650" width="8" height="12" opacity="0.85" data-p="4.64"/><rect class="w" x="908" y="650" width="8" height="12" opacity="0.79" data-p="4.00"/><rect class="w" x="818" y="676" width="8" height="12" opacity="0.54" data-p="2.20"/><rect class="w" x="836" y="676" width="8" height="12" opacity="0.37" data-p="1.71"/><rect class="w" x="908" y="676" width="8" height="12" opacity="0.33" data-p="5.55"/><rect class="w" x="818" y="702" width="8" height="12" opacity="0.4" data-p="4.20"/><rect class="w" x="854" y="702" width="8" height="12" opacity="0.87" data-p="0.12"/><rect class="w" x="818" y="728" width="8" height="12" opacity="0.88" data-p="0.33"/><rect class="w" x="836" y="728" width="8" height="12" opacity="0.51" data-p="5.27"/><rect x="815" y="110" width="90" height="80" fill="url(#bld2)"/><rect class="w" x="825" y="128" width="8" height="12" opacity="0.51" data-p="3.52"/><rect class="w" x="843" y="128" width="8" height="12" opacity="0.35" data-p="4.27"/><rect class="w" x="861" y="128" width="8" height="12" opacity="0.82" data-p="4.16"/><rect class="w" x="879" y="128" width="8" height="12" opacity="0.32" data-p="1.18"/><rect class="w" x="825" y="154" width="8" height="12" opacity="0.38" data-p="4.20"/><rect class="w" x="843" y="154" width="8" height="12" opacity="0.52" data-p="2.49"/><rect x="835" y="50" width="50" height="60" fill="url(#bld2)"/><rect class="w" x="845" y="68" width="8" height="12" opacity="0.89" data-p="6.11"/><rect class="w" x="863" y="68" width="8" height="12" opacity="0.81" data-p="3.90"/><rect x="857" y="-50" width="6" height="100" fill="#f2c14e" opacity=".8"/></svg>'''

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
  <path d="M410 505 L452 500 L455 512 L413 517 Z" fill="#c9a85c" stroke-width="1.4"/><path d="M416 503 L426 486 L436 502 L446 488 L452 500 Z" fill="#f2c14e" stroke-width="1.2"/><circle cx="238" cy="470" r="6" fill="#f2c14e" stroke="#fff3c4" stroke-width="1.5"/>
  <path d="M266 330 L266 392 L300 412 L334 392 L334 330" fill="url(#skin)" stroke="#b9805c"/>
 </g>
 <g id="head">
  <path d="M300 92 C356 92 392 136 392 200 C392 270 352 336 300 340 C248 336 208 270 208 200 C208 136 244 92 300 92 Z" fill="url(#skin)" stroke="#b9805c"/>
  <path d="M206 206 C196 128 240 70 306 72 C372 74 410 124 398 206 C390 170 372 146 348 136 C320 150 270 152 238 140 C222 156 212 178 206 206 Z" fill="#1f1712" stroke="#1f1712"/>
  <path d="M250 110 C290 86 350 92 384 140" fill="none" stroke="#5a4a3e" stroke-width="5" opacity=".7"/>
  <path d="M210 196 C196 194 194 236 214 240" fill="url(#skin)" stroke="#b9805c" stroke-width="1.8"/>
  <path d="M390 196 C404 194 406 236 386 240" fill="url(#skin)" stroke="#b9805c" stroke-width="1.8"/>
  <g fill="none" stroke="#4a3022" stroke-width="5">
   <path id="bl"/><path id="br"/><path id="mo" stroke="#9a4e42" stroke-width="4.5"/>
  </g>
  <ellipse id="el" cx="264" cy="236" rx="7" ry="3" fill="#2a1a12" stroke="none"/>
  <ellipse id="er" cx="336" cy="236" rx="7" ry="3" fill="#2a1a12" stroke="none"/>
  <g id="gl" style="display:none" fill="rgba(255,255,255,.08)" stroke="#111" stroke-width="7"><rect x="232" y="214" width="62" height="44" rx="12"/><rect x="306" y="214" width="62" height="44" rx="12"/><path d="M294 232 Q300 226 306 232" fill="none" stroke-width="5"/><path d="M232 230 L212 222 M368 230 L388 222" stroke-width="5"/></g>
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
    hook = (f'<div class="sc" data-in="-1000" data-out="{T_Q}" data-d="250">' + (SKY if v.get("theme")=="power" else '') + '<div class="hook">'
            f'<div class="a" data-in="-1000">{brand()}</div>'
            f'<div class="kicker a" data-in="-1000">{v.get("kicker_html") or E(v["kicker"])}</div>'
            f'<h1 class="a" data-in="-1000">{v["hook"]}</h1></div></div>')
    opts_q = ''.join(f'<div class="opt a" data-in="{T_Q+200+j*110}"><b>{L[j]}</b><span>{E(o)}</span></div>' for j, o in enumerate(v["opts"]))
    q = (f'<div class="sc" data-in="{T_Q}" data-out="{T_E}" data-d="300"><div id="bignum" class="bignum"></div>'
         f'<div class="mini"><span>ビジネス英語実務検定</span><b>QUESTION</b></div><div class="qwrap">'
         f'<div class="band a" data-in="{T_Q}"><span>無料お試し 実施中</span><span>登録なし・10問・約5分</span></div>'
         f'<div class="qtext a" data-in="{T_Q+80}">{v["q"]}</div>'
         f'<div id="opts">{opts_q}</div>'
         f'<div id="tm" data-in="{T_Q+450}" data-out="{T_A}" data-d="250"><div class="timer"><div class="bar"><i id="bar"></i></div><div class="ring"><svg viewBox="0 0 200 200"><circle class="rbg" cx="100" cy="100" r="86"/><circle id="rfg" cx="100" cy="100" r="86"/></svg><div class="cnum" id="cn">3</div></div></div>'
         f'<div class="tlab">TIME LIMIT ― 回答まで</div></div>'
         f'<div class="ex a" data-in="{T_A+350}">{v["ex"]}</div></div></div>')
    hooks = (f'window.HOOKS=function(t){{const tb=document.getElementById("bar");tb.style.width=(100*(1-cl((t-{T_Q+500})/3000)))+"%";'
             f'document.getElementById("cn").textContent=t<{T_Q+1500}?"3":t<{T_Q+2500}?"2":"1";const tt=t-{T_Q+500},f=((tt%1000)+1000)%1000/1000,on=tt>=0&&t<{T_A},last=tt>=2000;const cn=document.getElementById("cn");const hb=f<.12?Math.sin(f/.12*Math.PI):(f>.22&&f<.34?.6*Math.sin((f-.22)/.12*Math.PI):0);cn.style.transform=on?`scale(${{1+(last?.6:.42)*hb}})`:"none";cn.style.transformOrigin="50% 50%";const qw=document.querySelector(".qwrap");qw.style.transform="none";const pl=document.getElementById("pulse");if(pl)pl.style.opacity=on?Math.min(1,.18+.5*cl(tt/3000)+(last?.4:.22)*Math.pow(1-f,2)):0;const rf=document.getElementById("rfg");if(rf){{rf.style.strokeDashoffset=540.4*cl(tt/3000);rf.style.strokeWidth=last?16:12;}}const bn=document.getElementById("bignum");if(bn){{bn.textContent=on?cn.textContent:"";bn.style.transform=on?`scale(${{1.18-.18*ease(f)}})`:"none";bn.style.opacity=on?(last?1.8:1)*(.6+.4*Math.pow(1-f,2)):0;}}tb.style.boxShadow=on?`0 0 ${{14+26*Math.pow(1-f,2)}}px rgba(227,196,124,${{.5+.4*Math.pow(1-f,2)}})`:"none";'
             f'const os=document.querySelectorAll("#opts .opt");os.forEach((o,j)=>{{o.classList.toggle("ok",t>={T_A}&&j=={v["ans"]});o.classList.toggle("ng",t>={T_A}&&j!={v["ans"]});}});'
             f'if(t>={T_A}&&!window.BURST){{const r=os[{v["ans"]}].getBoundingClientRect();window.BURST={{t:{T_A},x:r.left+r.width/2,y:r.top+r.height/2}};}}}};')
    lead = "書類選考で苦戦していませんか？<br>資格欄、空白のままになっていませんか？"
    if v.get("figure"):
        fig = f'<div class="figwrap qfig" id="qfw" style="position:absolute">{FIG}' + (LAP if v.get("theme")=="power" else '') + '</div>'
        isx = 'true' if v["platform"] == "x" else 'false'
        hooks += ("(function(){const H=window.HOOKS;window.HOOKS=function(t){H(t);const $=i=>document.getElementById(i);if(!$('fig'))return;"
                  "const TQ=%d,TA=%d,TE=%d,X=%s,w=$('qfw');"
                  "let op=0,pose=0;if(t<TQ){op=cl((TQ-t)/250);pose=0;}else if(X&&t>=TA+250&&t<TE){op=ease(cl((t-TA-250)/400))*cl((TE-t)/250);pose=1;}"
                  "w.style.opacity=op;"
                  "if(pose==1){const k=ease(cl((t-TA-250)/500));w.style.transformOrigin='50%% 100%%';w.style.transform=`translate(270px,${-150+(1-k)*50}px) scale(.42)`;}else{w.style.transform='none';}"
                  "document.querySelectorAll('.sky .w').forEach(w=>{const p=+w.dataset.p;w.style.opacity=.35+.6*(.5+.5*Math.sin(t/700+p));});"
                  "if(pose==0&&document.body.classList.contains('power')){$('fig').style.filter='none';$('figglow').setAttribute('opacity',0);$('gl').style.display='block';"
                  "const ty=k=>Math.max(0,Math.sin(t/(k)))*10;if($('hl')){$('hl').setAttribute('transform',`translate(0 ${-ty(52)})`);$('hr').setAttribute('transform',`translate(0 ${-ty(41+7)})`);}"
                  "const bob=Math.sin(t/600)*2;$('head').setAttribute('transform',`translate(-6 ${-4+bob}) rotate(${-5+Math.sin(t/900)*1} 300 330)`);$('body').setAttribute('transform',`translate(0 ${-4+bob*.5}) scale(1.03 1.02)`);"
                  "const sh='translate(-16 0)';['bl','br','mo','el','er','gl'].forEach(i=>$(i).setAttribute('transform',sh));"
                  "$('bl').setAttribute('d','M240 192 L264 194 L286 202');$('br').setAttribute('d','M360 192 L336 194 L314 202');"
                  "$('mo').setAttribute('d','M284 292 Q300 296 320 285');$('mo').setAttribute('fill','none');"
                  "const bk=((t+500)%%1600)<110?.6:4.2;$('el').setAttribute('ry',bk);$('er').setAttribute('ry',bk);"
                  "['q1','q2','q3'].forEach(q=>$(q).setAttribute('opacity',0));}"
                  "else if(pose==0){const sw=Math.sin(t/330),bob=Math.sin(t/260)*4;"
                  "$('fig').style.filter='saturate(.75)';$('figglow').setAttribute('opacity',0);"
                  "$('head').setAttribute('transform',`translate(0 ${12+bob}) rotate(${sw*9} 300 330)`);"
                  "$('body').setAttribute('transform',`translate(0 ${bob*0.5})`);"
                  "const up=(Math.sin(t/420)+1)/2;"
                  "$('bl').setAttribute('d',`M246 ${206-up*6} Q266 ${197-up*8} 284 ${192-up*4}`);$('br').setAttribute('d',`M354 ${200-up*3} Q334 ${196-up*3} 316 ${198-up*2}`);"
                  "$('mo').setAttribute('d','M284 292 Q300 290 316 288');"
                  "const bl=((t+500)%%1100)<110?.6:5.5;$('el').setAttribute('ry',bl);$('er').setAttribute('ry',bl);"
                  "['q1','q2','q3'].forEach((q,i)=>{const e=$(q),st=i==0?-300:120+i*280,k=cl((t-st)/260),sc=k<1?(1-Math.pow(1-k,3))*1.25-(k>.7?(k-.7)*.8:0):1;"
                  "e.setAttribute('opacity',k>0?.85:0);const bx=[180,445,488][i],by=[100,72,182][i];e.setAttribute('transform',`translate(${bx} ${by+Math.sin(t/450+i*2)*8}) scale(${Math.max(0,sc)}) translate(${-bx} ${-by})`)});}"
                  "else if(pose==1){$('fig').style.filter='none';$('figglow').setAttribute('opacity',document.body.classList.contains('power')?0:.9);if(document.body.classList.contains('power'))$('gl').style.display='block';if(document.body.classList.contains('power')){['bl','br','mo','el','er','gl'].forEach(i=>$(i).setAttribute('transform','translate(-16 0)'));}"
                  "$('head').setAttribute('transform','translate(0 -6) rotate(0 300 330)');$('body').setAttribute('transform','none');"
                  "$('bl').setAttribute('d','M246 198 Q266 186 284 196');$('br').setAttribute('d','M354 198 Q334 186 316 196');"
                  "$('mo').setAttribute('d','M280 286 Q300 306 320 286');$('el').setAttribute('ry',6.5);$('er').setAttribute('ry',6.5);"
                  "['q1','q2','q3'].forEach(q=>$(q).setAttribute('opacity',0));}"
                  "}})();") % (T_Q, T_A, T_E, isx)
        return '<div class="figp">' + hook + '</div>' + q + fig + end_screen(v["platform"], T_E, lead), hooks
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

def rank(v):
    items = v["items"]            # 下位から順に [(名前, 説明), ...]。最後が1位
    n = len(items)
    T0, STEP = v.get("t0", 1200), v.get("step", 1800)
    T1 = T0 + STEP*(n-1) - STEP + v.get("drum_gap", 1800)   # 1位のドラムロール開始
    T1R, T_E = T1 + 900, v.get("end_at", 12000)
    times = [T0 + i*STEP for i in range(n-1)] + [T1R]
    rows = ''
    for r in range(1, n+1):           # 1位が上
        idx = n - r
        name, _ = items[idx]
        cls = ' top' if r == 1 else ''
        win = ' class="win"' if r == 1 else ''
        rows += (f'<div class="rk-row{cls}"><div class="rk-no">{r}<small>位</small></div>'
                 f'<div class="rk-slot"><span class="q" id="rq{r}">？</span><span id="rs{r}"{win}>{name}</span></div></div>')
    desc = ''
    for i, (name, d) in enumerate(items):
        out = times[i+1] if i+1 < n else T_E
        desc += f'<div data-in="{times[i]+150}" data-out="{out}" data-d="300">{d}</div>'
    body = (f'<div class="sc {v.get("cls","")}" data-in="-1000" data-out="{T_E}" data-d="250">'
            f'<div class="rk-head"><div class="who">{E(v["target"])}</div><h1>{v["title"]}</h1><div class="rk-note">※国際ビジネス言語認定協会の公式アカウントです</div>' + (f'<div class="rk-crit">{v["crit"]}</div>' if v.get("crit") else '') + '</div>'
            f'<div class="rk-list">{rows}</div><div class="rk-desc">{desc}</div>' +
            f'<div class="rk-fig">{FIG}</div></div>')
    js = ("window.HOOKS=function(t){const $=i=>document.getElementById(i);const T=%s,N=%d,T1=%d;"
          "for(let r=1;r<=N;r++){const i=N-r,k=ease(cl((t-T[i])/350)),s=$('rs'+r),q=$('rq'+r);"
          "if(r==1&&t>=T1&&t<T[i]){q.style.opacity=.2+.8*Math.abs(Math.sin((t-T1)/70));q.style.display='block';}"
          "s.style.opacity=k;s.style.transform=`translateX(${(1-k)*60}px) scale(${r==1?1+.25*Math.pow(1-k,2):1})`;"
          "q.style.display=k>0?'none':'block';if(k<=0)q.style.opacity=1;}"
          "if(t>=T[N-1]&&!window.BURST){const b=$('rs1').getBoundingClientRect();window.BURST={t:T[N-1],x:b.left+b.width/2,y:b.top+b.height/2};}"
          "const p=ease(cl((t-T[N-1])/900)),L=(a,b)=>a+(b-a)*p;if(!$('fig'))return;"
          "$('figglow').setAttribute('opacity',p);$('fig').style.filter='saturate('+L(.7,1)+')';"
          "const sw=(1-p)*Math.sin(t/330)*8;$('head').setAttribute('transform',`translate(0 ${L(14,-8)}) rotate(${sw} 300 330)`);"
          "$('bl').setAttribute('d',`M246 ${L(206,198)} Q266 ${L(198,186)} 284 ${L(192,196)}`);$('br').setAttribute('d',`M354 ${L(200,198)} Q334 ${L(196,186)} 316 ${L(198,196)}`);"
          "$('mo').setAttribute('d',`M280 ${L(292,286)} Q300 ${L(288,306)} 320 ${L(290,286)}`);$('el').setAttribute('ry',L(5,6.5));$('er').setAttribute('ry',L(5,6.5));"
          "['q1','q2','q3'].forEach((q,i)=>{const e=$(q);e.setAttribute('opacity',(1-p)*.8);e.setAttribute('transform',`translate(0 ${Math.sin(t/450+i*2)*8})`)});"
          "const c=ease(cl((t-T[N-1]-200)/600));$('cert').setAttribute('opacity',c);$('cert').setAttribute('transform',`translate(0 ${(1-c)*200})`);"
          "const TX='ビジネス英語実務検定',n=Math.max(0,Math.min(TX.length,Math.floor((t-T[N-1]-700)/70)));$('ctext').textContent=TX.slice(0,n);};") % (times, n, T1)
    lead = "内定に向けて、<br>まずは資格欄から。"
    return body + end_screen(v["platform"], T_E, lead), js

def rankjk(v):
    items = v["items"]; n = len(items)
    T0, STEP = v.get("t0", 1500), v.get("step", 3300)
    T1 = T0 + STEP*(n-1); T1R = T1 + 900; T_E = v.get("end_at", 16500)
    times = [T0 + i*STEP for i in range(n-1)] + [T1R]
    cols = ['#e53935', '#1d6fd1', '#f5a623', '#2e9e5b', '#7e57c2']
    rows = ''.join(f'<div class="jk-row"><div class="jk-no" style="color:{cols[r-1]}">{r}</div><div class="jk-slot"><span id="js{r}">{items[n-r][0]}</span></div></div>' for r in range(1, n+1))
    caps = ''; pops = ''
    for i, (name, pts) in enumerate(items):
        end = times[i+1] if i+1 < n else T_E
        pops += f'<div class="jk-pop" id="jp{i}">{name}</div>'
        seg = (end - times[i] - 300) / max(1, len(pts))
        for j, (kind, txt) in enumerate(pts):
            a = int(times[i] + 300 + j*seg); b = int(a + seg)
            caps += f'<div class="{"y" if kind=="g" else ""}" data-in="{a}" data-out="{b}" data-d="120">{txt}</div>'
    if n:
        caps += f'<div class="y" data-in="{T1}" data-out="{T1R}" data-d="120">そして第1位は…</div>'
    body = (f'<div class="sc" data-in="-1000" data-out="{T_E}" data-d="250"><div class="jk-bg">'
            + ''.join(f'<i style="left:{x}px"></i>' for x in (40, 260, 480, 700, 920)) + '<u></u><b></b></div>'
            f'<div class="jk-fig">{FIG}</div>'
            f'<div class="jk-title">{E(v["title"])}</div><div class="jk-sub">{E(v["sub"])}</div>'
            f'<div class="jk-list">{rows}</div>{pops}'
            f'<div class="jk-note">{v["crit"]}</div><div class="jk-cap">{caps}</div></div>')
    js = ("window.HOOKS=function(t){const $=i=>document.getElementById(i);const T=%s,N=%d,T1=%d,TE=%d;"
          "for(let i=0;i<N;i++){const r=N-i,k=ease(cl((t-T[i]-650)/350));$('js'+r).style.opacity=k;"
          "const p=$('jp'+i),a=cl((t-T[i])/220),b=cl((t-T[i]-500)/250);p.style.opacity=a*(1-b);p.style.transform=`scale(${.6+.5*ease(a)-.4*b}) translate(${-b*260}px,${-b*300}px)`;}"
          "if(t>=T[N-1]&&!window.BURST){const b=$('js1').getBoundingClientRect();window.BURST={t:T[N-1]+650,x:b.left+b.width/2,y:b.top+b.height/2};}"
          "if(!$('fig'))return;const talk=t>T[0]&&t<TE&&!(t>T1-100&&t<T[N-1]);const m=talk?(Math.abs(Math.sin(t/95))*.7+Math.abs(Math.sin(t/57))*.3):0;"
          "$('mo').setAttribute('d',`M284 290 Q300 ${292+m*16} 316 290`);$('mo').setAttribute('fill',m>.15?'#7a2e2a':'none');"
          "$('bl').setAttribute('d','M246 200 Q266 190 284 194');$('br').setAttribute('d','M354 200 Q334 190 316 194');"
          "const bl=((t+300)%%2300)<120?.6:6;$('el').setAttribute('ry',bl);$('er').setAttribute('ry',bl);"
          "$('head').setAttribute('transform',`translate(0 ${Math.sin(t/700)*3}) rotate(${Math.sin(t/900)*2.5} 300 330)`);"
          "['q1','q2','q3'].forEach(q=>$(q).setAttribute('opacity',0));$('figglow').setAttribute('opacity',0);"
          "const c=ease(cl((t-T[N-1]-300)/600));$('cert').setAttribute('opacity',c);$('cert').setAttribute('transform',`translate(0 ${(1-c)*200})`);"
          "const TX='ビジネス英語実務検定',n=Math.max(0,Math.min(TX.length,Math.floor((t-T[N-1]-800)/70)));$('ctext').textContent=TX.slice(0,n);};") % (times, n, T1, T_E)
    return body + end_screen(v["platform"], T_E, "まずは、無料お試しから。"), js

def build(v, outdir):
    body, hooks = quiz(v) if v["kind"] == "quiz" else ad(v) if v["kind"] == "ad" else rank(v) if v["kind"] == "rank" else rankjk(v) if v["kind"] == "rankjk" else promo(v)
    seed = sum(ord(c) for c in v["id"]) % 9000 + 11
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{"story" if v["platform"]=="igad" else "safe reelad" if v["platform"]=="igreel" else "safe" if v["platform"] in ("tt","ig") else ""}{" light" if v.get("theme")=="light" else ""}{" jk" if v["kind"]=="rankjk" else ""}{" power" if v.get("theme")=="power" else ""}">'
           f'<canvas id="cv"></canvas><div class="beams"></div><div class="vig"></div><div id="pulse"></div><div class="frame"></div>{body}'
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
