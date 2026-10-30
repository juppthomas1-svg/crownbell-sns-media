import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
def build(out,CW,CH,L,T,s0=0.85,K=3):
    src=Image.open('/tmp/crownbell_work/igpin/ken_cert5_src.png').convert('RGBA');W,H=src.size
    s=s0*K;L*=K;T*=K
    yy=np.arange(H)[:,None];xx=np.arange(W)[None,:]
    left=np.clip(xx/60,0,1)*np.ones((H,1));left[530:885,:]=1
    a=left*np.clip((W-1-xx)/20,0,1)*np.clip((yy-30)/60,0,1)*np.clip((1040-yy)/90,0,1)
    b=np.array(src);b[...,3]=(a*255).astype(np.uint8)
    big=Image.fromarray(b).resize((int(W*s),int(H*s)),Image.LANCZOS)
    rgb=big.convert('RGB').filter(ImageFilter.UnsharpMask(radius=2,percent=60,threshold=2));big=Image.merge('RGBA',(*rgb.split(),big.split()[3]))
    P=Image.new('RGBA',(CW*K,CH*K),(0,0,0,0));P.alpha_composite(big,(int(L),int(T)))
    x0=L+s*30;x1=L+s*623;y0=T+s*540;f=s/(0.85*K)
    d=ImageDraw.Draw(P)
    BK='/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc';SB='/usr/share/fonts/opentype/noto/NotoSerifCJK-SemiBold.ttc'
    cx=(x0+x1)/2;navy=(12,26,62,255);gold=(165,125,55,255);U=K*f
    def ct(y,t,fo,fill,sp=0,x=None):
        ws=[d.textlength(c,font=fo) for c in t];tw=sum(ws)+sp*(len(t)-1);q=(x if x is not None else cx)-tw/2
        for c,w in zip(t,ws): d.text((q,y),c,font=fo,fill=fill);q+=w+sp
    Y=lambda v:y0+v*U
    ct(Y(28),'CERTIFICATE',ImageFont.truetype(SB,int(16*U),index=0),gold,sp=7*U)
    d.line([(cx-130*U,Y(56)),(cx+130*U,Y(56))],fill=gold,width=int(2*U))
    ct(Y(66),'ビジネス英語実務検定',ImageFont.truetype(BK,int(47*U),index=0),navy)
    d.line([(cx-130*U,Y(140)),(cx+130*U,Y(140))],fill=gold,width=int(2*U))
    ct(Y(150),'BUSINESS ENGLISH PRACTICAL PROFICIENCY',ImageFont.truetype(SB,int(12*U),index=0),gold,sp=3*U)
    ct(Y(210),'国際ビジネス言語認定協会',ImageFont.truetype(SB,int(18*U),index=0),(60,50,35,255),sp=1*U,x=cx-40*U)
    logo=Image.open('/home/claude/crownbell-sns-media/kit/logo-seal.png').convert('RGBA').resize((int(56*U),int(56*U)),Image.LANCZOS)
    P.alpha_composite(logo,(int(cx+125*U),int(Y(192))))
    P.save(out)
if __name__=='__main__':
    a=sys.argv;build(a[1],int(a[2]),int(a[3]),float(a[4]),float(a[5]),float(a[6]) if len(a)>6 else 0.85)
