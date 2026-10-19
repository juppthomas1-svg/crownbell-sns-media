import json,html
E_=html.escape
CSS='''
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;font-family:"Noto Sans CJK JP",sans-serif;color:#f5f1e6;
background:radial-gradient(120% 70% at 50% 0%,#1d3d7a 0%,#0b2150 45%,#06142f 100%)}
.frame{position:absolute;inset:36px;border:2px solid rgba(201,168,92,.55);pointer-events:none}
.frame:after{content:"";position:absolute;inset:10px;border:1px solid rgba(201,168,92,.25)}
.top{position:absolute;top:84px;left:84px;right:84px;display:flex;align-items:center;gap:22px}
.top img{width:92px;height:92px;border-radius:50%;background:#fff}
.top .n{font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:38px;letter-spacing:.06em;line-height:1.25}
.top .n small{display:block;font-family:"Noto Sans CJK JP";font-weight:400;font-size:22px;letter-spacing:.2em;color:#c9a85c}
.top .off{margin-left:auto;font-size:24px;letter-spacing:.2em;color:#c9a85c;border:1.5px solid #c9a85c;padding:8px 18px}
.bot{position:absolute;bottom:80px;left:84px;right:84px;display:flex;justify-content:space-between;font-size:24px;letter-spacing:.12em;color:rgba(245,241,230,.6);border-top:1px solid rgba(201,168,92,.35);padding-top:22px}
.s{position:absolute;left:96px;right:96px;top:300px;bottom:200px;display:flex;flex-direction:column;justify-content:center;opacity:0;transition:opacity .45s}
.s.on{opacity:1}
.a{opacity:0;transform:translateY(36px);transition:opacity .55s ease,transform .55s cubic-bezier(.2,.8,.2,1)}
.on .a{opacity:1;transform:none}
.on .d1{transition-delay:.15s}.on .d2{transition-delay:.4s}.on .d3{transition-delay:.65s}.on .d4{transition-delay:.9s}.on .d5{transition-delay:1.15s}.on .d6{transition-delay:1.4s}
.kicker{font-size:34px;letter-spacing:.3em;color:#c9a85c;margin-bottom:34px;display:flex;align-items:center;gap:20px}
.kicker:before{content:"";width:64px;height:2px;background:#c9a85c}
h1{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:84px;line-height:1.35;letter-spacing:.02em}
h1 em{font-style:normal;color:#e6c77a}
.lead{font-size:44px;line-height:1.6;margin-top:40px;color:rgba(245,241,230,.85)}
.q{font-size:52px;line-height:1.55;font-weight:700;margin-bottom:56px}
.q .en{display:block;font-family:"Noto Sans",sans-serif;color:#e6c77a;font-size:54px;margin-top:14px}
.opt{display:flex;align-items:center;gap:30px;background:rgba(255,255,255,.06);border:1.5px solid rgba(201,168,92,.45);padding:40px 42px;margin-bottom:30px;font-size:52px;font-weight:600;font-family:"Noto Sans","Noto Sans CJK JP",sans-serif;line-height:1.3;transition:all .5s}
.opt b{flex:none;width:76px;height:76px;border:2px solid #c9a85c;color:#e6c77a;display:flex;align-items:center;justify-content:center;font-family:"Noto Serif CJK JP",serif;font-size:42px}
.opt.ok{background:linear-gradient(90deg,#c9a85c,#e6c77a);color:#0b2150;border-color:#e6c77a}
.opt.ok b{background:#0b2150;color:#e6c77a;border-color:#0b2150}
.opt.ng{opacity:.32}
.timer{margin-top:40px;height:10px;background:rgba(255,255,255,.12);position:relative}
.timer i{position:absolute;left:0;top:0;bottom:0;width:100%;background:#c9a85c;transition:width 3s linear}
.timer.go i{width:0}
.cnum{font-family:"Noto Serif CJK JP",serif;font-size:120px;color:#e6c77a;text-align:right;margin-top:10px;height:150px}
.ans{font-size:34px;letter-spacing:.3em;color:#c9a85c;margin-bottom:28px}
.ex{margin-top:26px;font-size:44px;line-height:1.65;border-left:6px solid #c9a85c;padding:8px 0 8px 34px;color:rgba(245,241,230,.92)}
.ex b{color:#e6c77a}
.row{display:flex;gap:30px;align-items:baseline;border-bottom:1px solid rgba(201,168,92,.35);padding:34px 0}
.row .k{font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:56px;color:#e6c77a;min-width:150px}
.row .v{font-size:44px;line-height:1.5}
.row .v .en{display:block;font-family:"Noto Sans",sans-serif;font-weight:700;font-size:56px;color:#f5f1e6}
.row .v .ja{font-size:40px;color:rgba(245,241,230,.75)}
.lab{font-size:34px;letter-spacing:.2em;margin:24px 0 16px}
.bad{border:1.5px solid rgba(230,120,120,.7);background:rgba(160,40,50,.25);padding:38px 42px;font-size:54px;font-weight:700;font-family:"Noto Sans",sans-serif;text-decoration:line-through;text-decoration-color:rgba(255,140,140,.8)}
.good{border:1.5px solid #e6c77a;background:linear-gradient(90deg,rgba(201,168,92,.3),rgba(201,168,92,.08));padding:38px 42px;font-size:54px;font-weight:700;font-family:"Noto Sans",sans-serif}
.cta{align-items:center;text-align:center}
.cta img{width:400px;height:400px;border-radius:50%;background:#fff;box-shadow:0 0 0 10px rgba(201,168,92,.25),0 30px 80px rgba(0,0,0,.45);transform:scale(.85);opacity:0;transition:all .9s cubic-bezier(.2,.8,.2,1)}
.cta.on img{transform:none;opacity:1}
.cta .t{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:70px;line-height:1.4;margin-top:64px}
.cta .sub{font-size:38px;letter-spacing:.12em;color:#e6c77a;margin-top:30px}
.cta .btn{margin-top:56px;border:2px solid #e6c77a;padding:26px 56px;font-size:40px;letter-spacing:.1em}
.cta .note{margin-top:40px;font-size:26px;color:rgba(245,241,230,.55)}
'''
def wrap(inner,js):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="frame"></div><div class="top"><img src="logo-seal.png"><div class="n">ビジネス英語実務検定<small>BUSINESS ENGLISH CERTIFICATION</small></div><span class="off">公式</span></div>{inner}<div class="bot"><span>国際ビジネス言語認定協会</span><span>24時間オンライン受験</span></div><script>{js}</script></body></html>'
def build(v):
    S=[];T=[];t=0
    def at(ms,code): T.append((ms,code))
    for i,s in enumerate(v['scenes']):
        sid=f's{i}';k=s['type']
        if k=='hook':
            S.append(f'<div class="s" id="{sid}"><div class="kicker a d1">{E_(s["tag"])}</div><h1 class="a d1">{s["h"]}</h1></div>'); at(t,f"show('{sid}')"); t+=s.get('d',3400)
        elif k=='quiz':
            L='ABC'
            S.append(f'<div class="s" id="{sid}"><div class="q a d1">{s["q"]}</div>'+''.join(f'<div class="opt a d{j+2}"><b>{L[j]}</b>{E_(o)}</div>' for j,o in enumerate(s['opts']))+f'<div class="timer a d5" id="tm{sid}"><i></i></div><div class="cnum" id="cn{sid}"></div></div>')
            S.append(f'<div class="s" id="{sid}r"><div class="ans a d1">ANSWER ― 正解</div>'+''.join(f'<div class="opt {"ok" if j==s["ans"] else "ng"}"><b>{L[j]}</b>{E_(o)}</div>' for j,o in enumerate(s['opts']))+f'<div class="ex a d3">{s["ex"]}</div></div>')
            at(t,f"show('{sid}')"); at(t+2400,f"document.getElementById('tm{sid}').classList.add('go')")
            for n,c in enumerate('321'): at(t+2400+n*1000,f"document.getElementById('cn{sid}').textContent='{c}'")
            t+=5500; at(t,f"show('{sid}r')"); t+=s.get('d',6000)
        elif k=='list':
            S.append(f'<div class="s" id="{sid}"><div class="kicker a d1">{s["title"]}</div>'+''.join(f'<div class="row a d{j+2}"><span class="k">{j+1:02d}</span><span class="v"><span class="en">{E_(en)}</span><span class="ja">{E_(ja)}</span></span></div>' for j,(en,ja) in enumerate(s['items']))+'</div>')
            at(t,f"show('{sid}')"); t+=600+len(s['items'])*1800+3500
        elif k=='bullets':
            S.append(f'<div class="s" id="{sid}"><div class="kicker a d1">{s["title"]}</div>'+''.join(f'<div class="row a d{j+2}"><span class="k">{j+1:02d}</span><span class="v">{b}</span></div>' for j,b in enumerate(s['items']))+(f'<div class="lead a d6" style="font-size:28px">{s["note"]}</div>' if s.get('note') else '')+'</div>')
            at(t,f"show('{sid}')"); t+=600+len(s['items'])*1300+3200
        elif k=='ngok':
            S.append(f'<div class="s" id="{sid}"><div class="q a d1">{s["q"]}</div><div class="lab a d2" style="color:#f0a0a0">✕ 失礼に聞こえることも</div><div class="bad a d2">{E_(s["ng"])}</div><div id="{sid}o" class="a"><div class="lab" style="color:#e6c77a">◎ 丁寧な言い方</div><div class="good">{E_(s["ok"])}</div><div class="ex">{s["ex"]}</div></div></div>')
            at(t,f"show('{sid}')"); at(t+3200,f"document.getElementById('{sid}o').style.opacity=1;document.getElementById('{sid}o').style.transform='none'"); t+=9800
        elif k=='cta':
            S.append(f'<div class="s cta" id="{sid}"><img src="logo-seal.png"><div class="t a d2">{s.get("big","あなたの<br>ビジネス英語力を、<br>証明しよう。")}</div><div class="sub a d3">3級・2級・1級｜24時間オンライン受験</div><div class="btn a d4">プロフィールのリンクから</div><div class="note a d5">国際ビジネス言語認定協会が認定する民間資格です</div></div>')
            at(t,f"show('{sid}')"); t+=4300
    js='const show=id=>{document.querySelectorAll(".s").forEach(e=>e.classList.remove("on"));document.getElementById(id).classList.add("on")};window.startAnim=()=>{'+''.join(f'setTimeout(()=>{{{c}}},{ms});' for ms,c in T)+'};window.TOTAL='+str(t)+';'
    return wrap(''.join(S),js),t
V=json.load(open('videos.json'))
# polish copy for professional tone
for v in V:
    for s in v['scenes']:
        if s['type']=='hook' and v['file'].startswith('01'):
            s['tag']='はじめまして'; s['h']='仕事で使う英語を、<br><em>確かな資格</em>に。'
        if s['type']=='cta' and v['file'].startswith('01'): s['big']='毎日1問、<br>ビジネス英語を。'
        if s['type']=='hook' and v['file'].startswith('02'): s['tag']='1日1問ビジネス英語'; s['h']='「お先に失礼します」<br>英語で<br><em>言えますか？</em>'
        if s['type']=='hook' and v['file'].startswith('03'): s['tag']='その英語、大丈夫？'; s['h']='上司への<br><em>“I want…”</em><br>失礼に<br>聞こえていませんか？'
        if s['type']=='hook' and v['file'].startswith('04'): s['tag']='英語面接対策'; s['h']='<em>“What are your<br>strengths?”</em><br>どう答えますか？'
        if s['type']=='hook' and v['file'].startswith('05'): s['tag']='保存版'; s['h']='オンライン会議で<br>使える英語<br><em>3選</em>'
        if s['type']=='hook' and v['file'].startswith('06'): s['tag']='1日1問ビジネス英語'; s['h']='<em>look</em> の後の1語で、<br>意味がまったく<br>変わります。'
        if s['type']=='hook' and v['file'].startswith('07'): s['tag']='ビジネス英語実務検定'; s['h']='あなたに合うのは、<br><em>何級</em>ですか？'
        if s['type']=='cta' and v['file'].startswith('07'): s['big']='迷ったら、<br>3級から。'
        if s['type']=='bullets': s['items']=['3級・2級・1級の<br>3つのレベル','24時間いつでも、<br>PC・スマホで受験','合格証（PDF）は<br>最短で受験当日に発行','履歴書の資格欄に<br>記載できます']; s['title']='ABOUT ― 検定について'
        if s['type']=='list' and v['file'].startswith('07'): s['title']='LEVELS ― 級の目安'
        if s['type']=='list' and v['file'].startswith('05'): s['title']='PHRASES ― 会議の英語'
for v in V:
    h,t=build(v); open(v['file']+'.html','w').write(h); print(v['file'],t)
