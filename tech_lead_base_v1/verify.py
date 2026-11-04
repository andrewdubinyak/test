"""Read-only integrity checks for the frozen four-view character base."""
from pathlib import Path
from PIL import Image
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_text())
for direction,info in manifest['views'].items():
 p=root/info['file']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==info['sha256'],direction+': base changed'
 with Image.open(p) as im:
  assert list(im.size)==manifest['cell_size']
  assert im.mode=='RGBA'
  assert set(im.getchannel('A').getdata())<={0,255}
  source=root/('source_'+direction+'.png')
  assert hashlib.sha256(source.read_bytes()).hexdigest()==info['source_sha256']
  with Image.open(source) as src:
   src=src.convert('RGBA').crop(tuple(info['source_cell']))
   for a,b in zip(im.getdata(),src.getdata()):
    if a[3]: assert a==b,direction+': visible pixel changed'
 print(direction+': unchanged, visible source pixels exact')
print('PASS: frozen base v1 intact; no generation, rescaling, recoloring, or quantization.')
