"""Deterministic pixel animation pilot. Pillow only; no image generation."""
from pathlib import Path
from PIL import Image, ImageDraw
import io, json, zipfile
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
OUT.mkdir(exist_ok=True)
SIZE = (96, 128)
MAGENTA = (255, 0, 255, 255)
master = Image.open(ROOT / 'master.png').convert('RGBA')

def masked(poly):
    mask = Image.new('L', SIZE)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    a = np.asarray(master).copy()
    a[:, :, 3] = np.minimum(a[:, :, 3], np.asarray(mask))
    return Image.fromarray(a)

# Explicit non-overlapping masks in native pixel coordinates.
polygons = {
 'head': [(0,0),(95,0),(95,64),(0,64)],
 'left_arm': [(0,65),(30,65),(34,72),(34,80),(36,86),(35,94),(0,94)],
 'right_arm': [(66,65),(95,65),(95,94),(61,94),(61,86),(62,80),(62,73)],
 'left_leg': [(0,88),(47,88),(47,127),(0,127)],
 'right_leg': [(48,88),(95,88),(95,127),(48,127)],
}
layers = {k: masked(v) for k,v in polygons.items()}
used = np.zeros((128,96), dtype=bool)
for layer in layers.values(): used |= np.asarray(layer)[:,:,3] > 0
body = np.asarray(master).copy()
body[used,3] = 0
layers['body'] = Image.fromarray(body)
for name,layer in layers.items(): layer.save(OUT / (name + '.png'))

def shifted(layer, dx=0, dy=0):
    out = Image.new('RGBA',SIZE)
    out.alpha_composite(layer,(dx,dy))
    return out

def leg_pose(layer, extension, swing):
    # Preserve original sneaker pixels; adjust trouser length above ankle.
    upper = layer.crop((0,88,96,101))
    shoe = layer.crop((0,101,96,110))
    length = 13 + extension
    upper = upper.resize((96,length),Image.Resampling.NEAREST)
    out = Image.new('RGBA',SIZE)
    out.alpha_composite(upper,(swing,88))
    out.alpha_composite(shoe,(swing,88+length))
    return out

def compose(left, right, la, ra, bob=0, blink=False):
    frame = Image.new('RGBA',SIZE)
    # Fill the shoulder joints behind moving arms using an existing hoodie color.
    joint = ImageDraw.Draw(frame)
    cloth = master.getpixel((38,76))
    joint.polygon([(29,70+bob),(35,70+bob),(36,86+bob),(29,85+bob)],fill=cloth)
    joint.polygon([(61,70+bob),(67,70+bob),(67,85+bob),(60,86+bob)],fill=cloth)
    # Rear foot first; the closer foot remains visibly in front at the pelvis.
    ordered = [right,left] if left.getbbox() and left.getbbox()[3] > right.getbbox()[3] else [left,right]
    for layer in ordered: frame.alpha_composite(layer)
    for name in ['body','head']: frame.alpha_composite(shifted(layers[name],0,bob))
    frame.alpha_composite(la)
    frame.alpha_composite(ra)
    if blink:
        # Eye patches use only palette colors already present on the master.
        d = ImageDraw.Draw(frame)
        skin = master.getpixel((46,53))
        ink = master.getpixel((35,51))
        for x1,x2 in [(34,42),(52,59)]:
            d.rectangle((x1,53+bob,x2,58+bob),fill=skin)
            d.line((x1,56+bob,x2,56+bob),fill=ink,width=1)
    return frame

walk = []
# Opposite phase legs. F1 and F5 explicitly swap extension and shoe positions.
extensions = [(2,-3),(1,-2),(0,0),(-2,1),(-3,2),(-2,1),(0,0),(1,-2)]
for i,(le,re) in enumerate(extensions):
    bob = [0,1,-1,0,0,1,-1,0][i]
    swing = [1,1,0,-1,-1,-1,0,1][i]
    left = leg_pose(layers['left_leg'],le,swing)
    right = leg_pose(layers['right_leg'],re,-swing)
    # Opposite arm swing, with the hand pixels retained exactly.
    la = shifted(layers['left_arm'],-swing,-le//2+bob)
    ra = shifted(layers['right_arm'],swing,-re//2+bob)
    walk.append(compose(left,right,la,ra,bob))

idle=[]
for i in range(8):
    bob = [0,-1,-1,0,0,0,0,0][i]
    idle.append(compose(layers['left_leg'],layers['right_leg'],
        shifted(layers['left_arm'],0,bob),shifted(layers['right_arm'],0,bob),bob,blink=i==5))

def export(name,frames):
    sheet=Image.new('RGBA',(1536,1024),MAGENTA)
    gifs=[]
    for i,f in enumerate(frames):
        large=f.resize((384,512),Image.Resampling.NEAREST)
        sheet.alpha_composite(large,((i%4)*384,(i//4)*512))
        bg=Image.new('RGBA',(384,512),MAGENTA)
        bg.alpha_composite(large)
        gifs.append(bg.convert('RGB'))
    sheet.convert('RGB').save(OUT/(name+'.png'))
    # Shared palette prevents palette flicker between GIF frames.
    palette=Image.new('RGB',(96*8,128))
    for i,f in enumerate(frames):
        bg=Image.new('RGBA',SIZE,MAGENTA); bg.alpha_composite(f)
        palette.paste(bg.convert('RGB'),(i*96,0))
    palette=palette.quantize(colors=128,dither=Image.Dither.NONE)
    indexed=[g.quantize(palette=palette,dither=Image.Dither.NONE) for g in gifs]
    indexed[0].save(OUT/(name+'.gif'),save_all=True,append_images=indexed[1:],duration=140,loop=0,optimize=False,disposal=2)
    return sheet

for name,frames in [('walk_down',walk),('idle_down',idle)]: export(name,frames)
# Editable OpenRaster master: separate original sprite parts, no baked background.
import xml.etree.ElementTree as ET
root=ET.Element('image',w='96',h='128',name='Tech Lead pixel master',version='0.0.3')
stack=ET.SubElement(root,'stack')
with zipfile.ZipFile(OUT/'master.ora','w') as z:
    z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
    for name in ['head','body','left_arm','right_arm','left_leg','right_leg']:
        src='data/'+name+'.png'
        ET.SubElement(stack,'layer',name=name,src=src,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
        b=io.BytesIO();layers[name].save(b,format='PNG');z.writestr(src,b.getvalue())
    z.writestr('stack.xml',ET.tostring(root))
    b=io.BytesIO();master.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())

# Useful invariants: exact chroma key, binary alpha, shared palette, fixed head.
master_colors=set(map(tuple,np.asarray(master).reshape(-1,4)))
for f in walk+idle:
    a=np.asarray(f)
    assert set(np.unique(a[:,:,3])) <= {0,255}
    assert set(map(tuple,a[a[:,:,3]>0])) <= master_colors
for i,f in enumerate(walk):
    bob=[0,1,-1,0,0,1,-1,0][i]
    reference=np.asarray(master)[18:64,20:77]
    actual=np.asarray(f)[18+bob:64+bob,20:77]
    assert np.array_equal(actual[reference[:,:,3]>0],reference[reference[:,:,3]>0])
assert not np.array_equal(np.asarray(walk[0]),np.asarray(walk[4]))
for n in ['walk_down','idle_down']:
    with Image.open(OUT/(n+'.png')) as im:
        assert im.size==(1536,1024)
        assert im.getpixel((0,0))==(255,0,255)
print('PASS: fixed master palette; binary alpha; unchanged head in walk; distinct F1/F5; 1536x1024 sheets; exact #FF00FF.')
