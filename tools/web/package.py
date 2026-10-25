#!/usr/bin/env python3
"""Build the browser site/ZIP from this repository only; no Android checkout."""
import base64,hashlib,html,pathlib,re,shutil,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[2]
WEB=ROOT/'web';OUT=ROOT/'build/browser';VERSION='1.00'
files='index.html app.js plain.txt cheats.js runtime.js input.js presentation.js diagnostics.js movie-audio.js saves.js style.css browser.css browser.js browser-storage.js launcher-art.png icon.png residentevil.js residentevil.wasm'.split()
for name in files:
    if not (WEB/name).is_file():raise SystemExit('Missing '+name+'; run bash tools/web/build.sh first')
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for name in files:shutil.copyfile(WEB/name,OUT/name)
binary=base64.b64encode((OUT/'residentevil.wasm').read_bytes()).decode('ascii')
engine=OUT/'residentevil.js'
engine.write_text("(function(){const raw=atob('"+binary+"');const bytes=new Uint8Array(raw.length);for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);globalThis.Module.wasmBinary=bytes;})();\n"+engine.read_text())
(OUT/'residentevil.wasm').unlink()
revision=hashlib.sha256(engine.read_bytes()).hexdigest()[:16]
p=OUT/'browser.js';p.write_text(re.sub(r"engineScript:'residentevil\.js(?:\?v=[^']+)?'","engineScript:'residentevil.js?v="+revision+"'",p.read_text()))
shutil.copytree(ROOT/'licenses',OUT/'licenses')
shutil.copyfile(ROOT/'LICENSE',OUT/'LICENSE')
shutil.copyfile(ROOT/'docs/WEB.md',OUT/'README-WEB.md')
shutil.copyfile(ROOT/'serve.py',OUT/'serve.py')
(OUT/'.nojekyll').write_text('')
p=OUT/'index.html';text=p.read_text()
text=re.sub(r'<template id="bundled-credits">.*?</template>',lambda m:'<template id="bundled-credits">'+html.escape((WEB/'plain.txt').read_text())+'</template>',text,flags=re.S)
text=re.sub(r'((?:src|href)="[^"?]+)\?v=[^" ]+',r'\1',text)
text=re.sub(r'(?:src|href)="([^"?#]+\.(?:js|css))"',lambda m:m[0][:-1]+'?v='+hashlib.sha256((OUT/m[1]).read_bytes()).hexdigest()[:16]+'"',text)
p.write_text(text)
# Keep the repository root ready for GitHub Pages (main / root).
for file in OUT.rglob('*'):
    if file.is_file():
        dest=ROOT/file.relative_to(OUT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(file,dest)
archive=ROOT/'build'/f'resident-evil-browser-{VERSION}.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for file in sorted(OUT.rglob('*')):
        if file.is_file():z.write(file,f'resident-evil-browser-{VERSION}/'+str(file.relative_to(OUT)))
print('Browser ZIP:',archive)
print('GitHub Pages files updated at:',ROOT)
