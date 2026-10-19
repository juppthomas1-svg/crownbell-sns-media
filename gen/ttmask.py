import sys
from PIL import Image, ImageDraw
# TikTok の画面に重なる場所を赤でぬる（上 160px・右 170px・下 470px）
out=sys.argv[1]; ims=[Image.open(f).convert('RGB') for f in sys.argv[2:]]
for im in ims:
    d=ImageDraw.Draw(im,'RGBA'); d.rectangle([0,0,1080,160],fill=(255,0,0,70)); d.rectangle([1080-170,0,1080,1920],fill=(255,0,0,70)); d.rectangle([0,1920-470,1080,1920],fill=(255,0,0,70))
W=Image.new('RGB',(1080*len(ims),1920)); [W.paste(im,(i*1080,0)) for i,im in enumerate(ims)]
W.resize((360*len(ims),640)).save(out)
