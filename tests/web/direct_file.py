"""Extracted-package file:// regression; synthetic files only.

Requires Playwright's Chromium (system Chromium policies may block file://).
Run after tools/web/package.py with the browser executable installed by
python3 -m playwright install chromium.
"""
import pathlib
import zipfile
import io
import struct
import tempfile
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
WEB = ROOT / 'build/browser'
BOOT = ['fontus.tim','font03t.tim','optkey03.tim','status.tim','statface.tim','blue.tim','staitem.tim','kage.tim']
TIM = (struct.pack('<II',16,9) + struct.pack('<I4H',524,0,0,256,1)
       + struct.pack('<256H',*([0,31,992,31744]+[0]*252))
       + struct.pack('<I4H',65548,0,0,128,256) + bytes([1])*65536)

with tempfile.TemporaryDirectory(prefix='re1-file-fixtures-') as temp, sync_playwright() as p:
    game = pathlib.Path(temp)/'USA'
    for name,data in ({'Data/'+n:TIM for n in BOOT}
                      | {'Data/item_all.pix':bytes(91200),'Stage1/ROOM1000.RDT':b'fixture'}).items():
        file = game/name
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_bytes(data)
    browser = p.chromium.launch(headless=True,args=['--no-sandbox','--enable-unsafe-swiftshader'])
    page = browser.new_page()
    errors,requests = [],[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url))
    page.goto((WEB/'index.html').as_uri())
    page.wait_for_function('()=>!document.querySelector("#folder").disabled')
    assert page.locator('[id^=hd-]').count()==0
    assert page.evaluate('typeof RE1HDPack')=='undefined'
    assert '| HD:' not in page.evaluate('RE1Diag.report()')
    pages=len(page.context.pages)
    page.locator('#launcher-credits').click()
    assert page.locator('#credits').evaluate('(d)=>d.open')
    assert page.locator('#credits-text').text_content()==(ROOT/'web/plain.txt').read_text()
    assert len(page.context.pages)==pages
    page.locator('#close-credits').click()
    page.evaluate('async()=>RE1SaveData.write([{name:"savedat1.dat",contents:new Uint8Array(0xa82).fill(71)}])')
    page.locator('#launcher-saves').click()
    with page.expect_download() as exported:page.locator('#saves-export').click()
    saved_backup=pathlib.Path(temp)/'local.saves.zip';exported.value.save_as(saved_backup)
    page.evaluate('async()=>RE1SaveData.write([{name:"savedat1.dat",contents:new Uint8Array(0xa82).fill(9)}])')
    with page.expect_file_chooser() as selected:page.locator('#saves-import').click()
    selected.value.set_files(saved_backup)
    page.wait_for_function('()=>!RE1SaveData.busy()');page.locator('#saves-confirm').click();page.wait_for_function('()=>!RE1SaveData.busy()')
    assert page.evaluate('async()=>Array.from((await RE1SaveData.read())[0].contents)')==[71]*0xa82
    gog=bytes((i*37+11)&255 for i in range(0x800))
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as archive:archive.writestr('SAVE/SAVEDAT2.DAT',gog)
    with page.expect_file_chooser() as selected:page.locator('#saves-import').click()
    selected.value.set_files({'name':'gog.zip','mimeType':'application/zip','buffer':buffer.getvalue()})
    page.wait_for_function('()=>!RE1SaveData.busy()');page.locator('#saves-confirm').click();page.wait_for_function('()=>!RE1SaveData.busy()')
    with page.expect_download() as exported:page.locator('#saves-export').click()
    gog_zip=pathlib.Path(temp)/'local-gog.zip';exported.value.save_as(gog_zip)
    with zipfile.ZipFile(gog_zip) as archive:
        assert archive.testzip() is None and archive.read('savedat2.dat')==gog
        assert archive.read('savedat1.dat')==bytes([71])*0xa82
    page.locator('#saves-close').click()
    page.locator('#browser-remember').uncheck()
    page.locator('#browser-folder-input').set_input_files(str(game))
    page.wait_for_function('()=>RE1BrowserStorage.ready()')
    page.evaluate('()=>{window.re1Ready=()=>{window.engineReady=true;};}')
    page.locator('#launch').click()
    page.wait_for_function('()=>window.engineReady===true',timeout=60000)
    assert page.evaluate("Module.FS.readFile('/game/USA/Data/fontus.tim').length")==len(TIM)
    page.evaluate("Module.FS.writeFile('/persist/SAVE/local-test.dat',new Uint8Array([12,128,255]));re1Sync();")
    page.wait_for_function('()=>!window.re1SyncBusy')
    page.reload()
    page.locator('#graphics-test').click()
    page.wait_for_function('()=>RE1Diag.graphicsPassed',timeout=60000)
    assert page.evaluate("Array.from(Module.FS.readFile('/persist/SAVE/local-test.dat'))")==[12,128,255]
    assert not errors,errors
    assert not any(url.split('?')[0].endswith('/residentevil.wasm') for url in requests)
    assert all(url.startswith(('file:','blob:','data:')) for url in requests),requests
    print('PASS: direct index.html save export/import, embedded wasm, folder reads, durable saves/reload, actual graphics/audio; no HTTP or wasm fetch')
    browser.close()
