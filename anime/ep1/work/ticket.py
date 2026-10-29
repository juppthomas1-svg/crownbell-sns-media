import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC='/root/.claude/uploads/210bf86c-99a6-5384-bb82-ae2771382964/30286a52-Hands_holding_blank_ticket_1b861e07.mp4'
tr=np.load('track.npy').astype(float)
# smooth center
cx=(tr[:,0]+tr[:,2]/2);cy=(tr[:,1]+tr[:,3]/2)
k=np.ones(9)/9;cx=np.convolve(np.pad(cx,4,mode='edge'),k,'valid');cy=np.convolve(np.pad(cy,4,mode='edge'),k,'valid')
S=3  # supersample: work at 2160x3840? use 1080x1920 output
W,H=1080,1920;sc=W/720
BK='/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc';SB='/usr/share/fonts/opentype/noto/NotoSerifCJK-SemiBold.ttc'
def txtimg():
    w,h=560,240;im=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(im)
    f1=ImageFont.truetype(SB,22,index=0);f2=ImageFont.truetype(BK,54,index=0);f3=ImageFont.truetype(SB,18,index=0)
    ink=(40,30,12,255)
    def ctext(y,s,f,fill,sp=0):
        if sp:
            ws=[d.textlength(c,font=f) for c in s];tw=sum(ws)+sp*(len(s)-1);x=(w-tw)/2
            for c,cw in zip(s,ws): d.text((x,y),c,font=f,fill=fill);x+=cw+sp
        else:
            tw=d.textlength(s,font=f);d.text(((w-tw)/2,y),s,font=f,fill=fill)
    ctext(30,'BUSINESS  ENGLISH',f1,(90,62,20,235),sp=6)
    d.line([(150,72),(410,72)],fill=(110,80,30,200),width=2)
    ctext(88,'ビジネス英語実務検定',f2,ink)
    d.line([(150,168),(410,168)],fill=(110,80,30,200),width=2)
    ctext(180,'国際ビジネス言語認定協会',f3,(90,62,20,235),sp=3)
    return im
T=txtimg()
# big title card
def card():
    w,h=W,330;im=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rectangle([0,40,w,h-40],fill=(9,20,48,200))
    gold=(201,168,92,255)
    d.line([(110,40),(w-240,40)],fill=gold,width=3);d.line([(110,h-40),(w-240,h-40)],fill=gold,width=3)
    f=ImageFont.truetype(BK,74,index=0);s='ビジネス英語実務検定'
    tw=d.textlength(s,font=f);x=110+((w-350)-tw)/2
    d.text((x+3,112+3),s,font=f,fill=(0,0,0,140));d.text((x,112),s,font=f,fill=(227,196,124,255))
    return im
C=card()
cap=cv2.VideoCapture(SRC);fps=24;out=cv2.VideoWriter('s3_text.mp4',cv2.VideoWriter_fourcc(*'mp4v'),fps,(W,H))
REV0,REV1,DON=0.6,1.5,1.6
i=0
while True:
    ok,f=cap.read()
    if not ok:break
    t=i/fps
    fr=Image.fromarray(cv2.cvtColor(cv2.resize(f,(W,H),interpolation=cv2.INTER_LANCZOS4),cv2.COLOR_BGR2RGB)).convert('RGBA')
    # text on ticket
    if t>=REV0:
        p=min(1,(t-REV0)/(REV1-REV0))
        s=1.0
        if t>=DON: s=1+0.10*np.exp(-(t-DON)*9)
        tw,th=int(T.width*0.68*sc*s),int(T.height*0.68*sc*s)
        tt=T.resize((tw,th),Image.LANCZOS)
        # reveal mask left->right with soft edge
        m=np.zeros((th,tw),np.float32);edge=p*(tw+120)-60
        xs=np.arange(tw);m[:]=np.clip((edge-xs)/60+0.5,0,1)
        a=np.array(tt);a[...,3]=(a[...,3]*m).astype(np.uint8);tt=Image.fromarray(a)
        x=int(cx[i]*sc-tw/2);y=int(cy[i]*sc-th/2)
        fr.alpha_composite(tt,(x,y))
        # sweep glow
        if p<1:
            g=Image.new('RGBA',(W,H),(0,0,0,0));gd=ImageDraw.Draw(g);gx=x+edge
            gd.ellipse([gx-40,y+th*0.2,gx+40,y+th*0.8],fill=(255,230,160,170));g=g.filter(ImageFilter.GaussianBlur(25));fr.alpha_composite(g)
    if t>=DON:
        # flash
        fl=max(0,1-(t-DON)*4)
        if fl>0:
            g=Image.new('RGBA',(W,H),(255,236,190,int(60*fl)));fr.alpha_composite(g)
        # card slides/fades in
        q=min(1,(t-DON)/0.25);cc=C.copy();ca=np.array(cc);ca[...,3]=(ca[...,3]*q).astype(np.uint8)
        fr.alpha_composite(Image.fromarray(ca),(0,int(1110+40*(1-q))))
    out.write(cv2.cvtColor(np.array(fr.convert('RGB')),cv2.COLOR_RGB2BGR));i+=1
out.release();print(i)
