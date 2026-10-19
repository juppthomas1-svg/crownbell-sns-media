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
'''

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
  cx.beginPath();cx.arc(d.x+Math.sin(t/1500+d.p)*8,y,d.r,0,6.283);cx.fillStyle=`rgba(232,205,138,${o})`;cx.fill();}
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
    hook = (f'<div class="sc" data-in="0" data-out="{T_Q}" data-d="250"><div class="hook">'
            f'<div class="a" data-in="0" data-d="300">{brand()}</div>'
            f'<div class="kicker a" data-in="120">{E(v["kicker"])}</div>'
            f'<h1 class="a" data-in="220" data-d="500">{v["hook"]}</h1></div></div>')
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
    return hook + q + end_screen(v["platform"], T_E, lead), hooks

def promo(v):
    T_S, T_E = 3000, 6800
    lines = ''.join(f'<div class="pline a" data-in="{350+j*550}"><i></i><span>{E(p)}</span></div>' for j, p in enumerate(v["problems"]))
    prob = (f'<div class="sc" data-in="0" data-out="{T_S}" data-d="250"><div class="prob">'
            f'<div class="a" data-in="0" data-d="300">{brand()}</div>'
            f'<div class="kicker a" data-in="120">{E(v["kicker"])}</div>{lines}</div></div>')
    facts = ''.join(f'<div class="fact a" data-in="{T_S+900+j*150}"><div class="k">{k}</div><div class="v">{val}</div></div>' for j, (k, val) in enumerate(v["facts"]))
    sol = (f'<div class="sc" data-in="{T_S}" data-out="{T_E}" data-d="300"><div class="mini"><span>ビジネス英語実務検定</span><b>SOLUTION</b></div><div class="sol">'
           f'<div class="kicker a" data-in="{T_S+50}">{E(v["sol_kicker"])}</div>'
           f'<h2 class="a" data-in="{T_S+150}" data-d="550">{v["sol"]}</h2>'
           f'<div class="note a" data-in="{T_S+500}">{v["sol_note"]}</div><div class="facts">{facts}</div></div></div>')
    return prob + sol + end_screen(v["platform"], T_E, v.get("end_lead", "あなたのビジネス英語力を、<br>確かな資格に。")), ''

def build(v, outdir):
    body, hooks = quiz(v) if v["kind"] == "quiz" else promo(v)
    seed = sum(ord(c) for c in v["id"]) % 9000 + 11
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
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
