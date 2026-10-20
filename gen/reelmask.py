import sys
from PIL import Image, ImageDraw
# リール広告で隠れる場所を赤でぬる（上150・右170・下640）
out=sys.argv[1]; ims=[Image.open(f).convert('RGB') for f in sys.argv[2:]]
for im in ims:
    d=ImageDraw.Draw(im,'RGBA'); d.rectangle([0,0,1080,150],fill=(255,0,0,60)); d.rectangle([1080-170,0,1080,1920],fill=(255,0,0,60)); d.rectangle([0,1920-640,1080,1920],fill=(255,0,0,60))
W=Image.new('RGB',(1080*len(ims),1920)); [W.paste(im,(i*1080,0)) for i,im in enumerate(ims)]
W.resize((360*len(ims),640)).save(out)
