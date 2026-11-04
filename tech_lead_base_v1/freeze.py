"""Create base candidates from existing saved sheets; never generate new artwork."""
from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parent
SOURCES={
'down':'exec-6c62a6a1-09a2-40dd-b613-d8eaa9d21418.png',
'up':'exec-46109d51-0c7a-40fc-8853-bf4a0d764ed0.png',
'left':'exec-63ec4c1b-eb6c-43aa-b545-43cde93e01de.png',
'right':'exec-5af300a7-8108-493f-9a54-4992e573547b.png',
}
if (ROOT/'manifest.json').exists():
 raise SystemExit('Base already frozen. Create a new version explicitly; do not overwrite v1.')
manifest={'version':1,'status':'candidate_for_visual_review','cell_size':[384,512],
'provenance':'First frame of previously generated saved idle sheets; not the original user-uploaded sheet.',
'processing':'Exact first cell, no resampling, no recoloring or quantization. Only magenta background converted to binary alpha.',
'views':{}}
for direction,filename in SOURCES.items():
 source=Path('/workspace/generated_images')/filename
 with Image.open(source) as im:
  assert im.size==(1536,1024)
  cell=im.convert('RGBA').crop((0,0,384,512))
 original=cell.copy()
 pixels=cell.load()
 for y in range(512):
  for x in range(384):
   r,g,b,a=pixels[x,y]
   if r>180 and b>170 and g<80:
    pixels[x,y]=(0,0,0,0)
 cell.save(ROOT/(direction+'.png'))
 # Check all retained pixels are literally the same as the source cell.
 for a,b in zip(cell.getdata(),original.getdata()):
  if a[3]: assert a==b
 bounds=cell.getbbox()
 manifest['views'][direction]={
  'file':direction+'.png','sha256':hashlib.sha256((ROOT/(direction+'.png')).read_bytes()).hexdigest(),
  'source_file':filename,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
  'source_frame':1,'source_cell':[0,0,384,512],'visible_bounds':list(bounds),
  'feet_y':bounds[3]-1,'anchor':[192,bounds[3]-1],
  'visible_colors':len({p[:3] for p in cell.getdata() if p[3]})}
 (ROOT/('source_'+direction+'.png')).write_bytes(source.read_bytes())
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Frozen four existing views. Visible source pixels retained exactly.')
