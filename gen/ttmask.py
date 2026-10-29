import sys
from PIL import Image, ImageDraw
# TikTok の画面に重なる場所を赤でぬる（縦長スマホ基準：上 220px・左 100px・右 230px・下 520px。2026-10-29 更新）
out=sys.argv[1]; ims=[Image.open(f).convert('RGB') for f in sys.argv[2:]]
for im in ims:
    d=ImageDraw.Draw(im,'RGBA'); d.rectangle([0,0,1080,220],fill=(255,0,0,70)); d.rectangle([0,220,100,1400],fill=(255,0,0,70)); d.rectangle([1080-230,220,1080,1400],fill=(255,0,0,70)); d.rectangle([0,1920-520,1080,1920],fill=(255,0,0,70))
W=Image.new('RGB',(1080*len(ims),1920)); [W.paste(im,(i*1080,0)) for i,im in enumerate(ims)]
W.resize((360*len(ims),640)).save(out)
