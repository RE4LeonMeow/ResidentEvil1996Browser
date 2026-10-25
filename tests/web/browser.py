"""Standalone static-browser checks with generated files, no game assets.
Run tools/web/package.py first. Requires Playwright and system Chromium.
"""
import http.server
import pathlib
import struct
import tempfile
import threading
from playwright.sync_api import sync_playwright

ROOT=pathlib.Path(__file__).resolve().parents[2]
WEB=ROOT/'build/browser'
BOOT=['fontus.tim','font03t.tim','optkey03.tim','status.tim','statface.tim','blue.tim','staitem.tim','kage.tim']
palette=struct.pack('<256H',*([0,31,992,31744,1023]+[0]*251))
pixels=bytes(1+(x//128)+(y//128)*2 for y in range(256) for x in range(256))
TIM=struct.pack('<II',16,9)+struct.pack('<I4H',524,0,0,256,1)+palette+struct.pack('<I4H',65548,0,0,128,256)+pixels
MOVIE=bytes((n*37+11)%256 for n in range(1535452))

class Server(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(WEB),**kw)
    def log_message(self,*a):pass
    def translate_path(self,path):
        # Verify that the package also works below a static host's subpath.
        if path.startswith('/preview/'):path=path[len('/preview'):]
        return super().translate_path(path)

server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Server)
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/preview/'

try:
    with tempfile.TemporaryDirectory(prefix='re1-browser-fixtures-') as temp,sync_playwright() as p:
        game=pathlib.Path(temp)/'USA'
        files={'Data/'+n:TIM for n in BOOT}
        files.update({'Data/item_all.pix':bytes(91200),'Data/test.bin':bytes(range(256))*2300,'Movie/capcom.avi':MOVIE,'Stage1/ROOM1000.RDT':b'fixture'})
        for name,data in files.items():
            path=game/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--enable-unsafe-swiftshader'])
        page=browser.new_page(viewport={'width':1280,'height':720})
        requests=[];failures=[]
        page.on('request',lambda r:requests.append((r.method,r.url)))
        page.on('pageerror',lambda e:failures.append(str(e)))
        page.goto(url);page.wait_for_function('()=>!document.querySelector("#folder").disabled')
        assert page.locator('.intro p').inner_text()=='Made by 4wu4_'
        assert 'Output:' in page.evaluate('RE1Diag.report()')
        assert 'Recent frame gap:' in page.evaluate('RE1Diag.report()')
        page.locator('#launcher-credits').click()
        page.wait_for_function('()=>document.querySelector("#credits-text").textContent.includes("khoilinux")')
        assert page.locator('#credits').evaluate('(d)=>d.open')
        page.locator('#close-credits').click()
        # Editing the text file takes effect on the next opening, and remains
        # literal text rather than HTML or executable credits markup.
        edited='Playtesters:\nAnother tester\n<b>literal text</b>'
        page.route('**/plain.txt',lambda route:route.fulfill(body=edited,content_type='text/plain'))
        page.locator('#launcher-credits').click()
        page.wait_for_function('(text)=>document.querySelector("#credits-text").textContent===text',arg=edited)
        assert page.locator('#credits-text b').count()==0
        page.locator('#close-credits').click();page.unroute('**/plain.txt')
        assert page.evaluate('RE1Input.settings.hidden') is True
        assert page.locator('#launch').is_disabled()
        page.locator('#browser-folder-input').set_input_files(str(game))
        page.wait_for_function('()=>RE1BrowserStorage.ready()')
        assert 'remembered' in page.evaluate('RE1BrowserStorage.status()')
        assert page.evaluate('typeof AndroidLauncher')=='undefined'
        page.evaluate('''()=>{
          window.re1Ready=()=>{window.testReady=true;};window.re1Exit=()=>{window.testExited=true;};
        }''')
        page.locator('#launch').click();page.wait_for_function('()=>window.testReady===true',timeout=90000)
        page.evaluate('''()=>{
          const fs=Module.FS,all=fs.readFile('/game/USA/Data/test.bin');
          if(all.length!==588800||all.some((n,i)=>n!==i%256))throw Error('Local file bytes differ');
          const tail=new Uint8Array(224732),s=fs.open('/game/USA/Movie/capcom.avi','r');
          if(fs.read(s,tail,0,tail.length,1310720)!==tail.length)throw Error('Movie tail length');
          if(tail.some((n,i)=>n!==(((i+1310720)*37+11)%256)))throw Error('Movie tail bytes');
          if(fs.read(s,tail,0,1,1535452)!==0)throw Error('Movie EOF');fs.close(s);
          for(const [offset,length] of [[-1,1],[0,262145],[1535452,1]]){
            let rejected=false;try{RE1BrowserStorage.read('Movie/capcom.avi',offset,length);}catch(e){rejected=true;}
            if(!rejected)throw Error('Invalid read accepted');
          }
          fs.writeFile('/persist/SAVE/browser-test.dat',new Uint8Array([0,128,255]));
          window.re1Sync();
        }''')
        page.wait_for_function('()=>!window.re1SyncBusy')
        page.evaluate("()=>Module.callMain(['--capture','/persist/browser-boot.cap','4'])")
        page.wait_for_function('()=>window.testExited===true',timeout=30000)
        assert page.evaluate("()=>Module.FS.analyzePath('/persist/browser-boot.cap').exists")
        # The remembered browser copy must not depend on the original folder.
        moved=pathlib.Path(temp)/'moved-USA';game.rename(moved);game=moved
        page.reload();page.wait_for_function('()=>RE1BrowserStorage.ready()')
        assert 'restored' in page.evaluate('RE1BrowserStorage.status()')
        page.evaluate('()=>{window.re1Ready=()=>{window.testReady=true;};}')
        page.locator('#launch').click();page.wait_for_function('()=>window.testReady===true',timeout=90000)
        assert page.evaluate("()=>Array.from(Module.FS.readFile('/persist/SAVE/browser-test.dat'))")==[0,128,255]
        assert page.evaluate("()=>Array.from(Module.FS.readFile('/game/USA/Data/test.bin').slice(-4))")==[252,253,254,255]
        page.reload();page.wait_for_function('()=>RE1BrowserStorage.ready()')
        page.locator('#browser-forget').click();page.wait_for_function('()=>!RE1BrowserStorage.busy()&&!RE1BrowserStorage.ready()')
        assert 'Saves and control settings are kept' in page.evaluate('RE1BrowserStorage.status()')
        page.reload();page.wait_for_function('()=>!document.querySelector("#folder").disabled')
        assert not page.evaluate('RE1BrowserStorage.ready()')
        assert all(method=='GET' for method,address in requests)
        assert not any('/manifest' in address or '/data/' in address for method,address in requests)
        assert not failures,failures
        print('PASS: static subpath; native folder input; exact local binary/tail/EOF reads; wasm boot; remembered files survive source rename/reload; saves persist; forget is separate; no file uploads or data endpoints')
        page.close()

        # Real engine render/audio with desktop keyboard shortcuts and settings.
        desktop=browser.new_page(viewport={'width':1280,'height':720})
        desktop.goto(url);desktop.locator('#graphics-test').click()
        desktop.wait_for_function('()=>RE1Diag.frames>=3',timeout=90000)
        desktop.evaluate('Module._re1_web_suspend(1)')
        assert desktop.locator('#touch').is_hidden()
        desktop.locator('#canvas').focus()
        desktop.keyboard.down('ArrowUp');desktop.keyboard.down('x')
        assert desktop.evaluate('RE1Input.mask()')==1025
        desktop.keyboard.up('ArrowUp');assert desktop.evaluate('RE1Input.mask()')==1024
        desktop.keyboard.up('x');assert desktop.evaluate('RE1Input.mask()')==0
        desktop.keyboard.down('ControlLeft');assert desktop.evaluate('RE1Input.mask()')==512
        desktop.keyboard.down('ArrowLeft');assert desktop.evaluate('RE1Input.mask()')==(512|4)
        desktop.keyboard.up('ArrowLeft');assert desktop.evaluate('RE1Input.mask()')==512
        desktop.keyboard.up('ControlLeft');assert desktop.evaluate('RE1Input.mask()')==0
        desktop.keyboard.down('ControlRight');desktop.keyboard.down('ArrowUp')
        assert desktop.evaluate('RE1Input.mask()')==(512|1)
        desktop.keyboard.up('ControlRight');assert desktop.evaluate('RE1Input.mask()')==1
        desktop.keyboard.up('ArrowUp');assert desktop.evaluate('RE1Input.mask()')==0
        desktop.evaluate('()=>{window.turnCalls=0;Module._re1_web_quick_turn=()=>{window.turnCalls++;return 0;};}')
        desktop.keyboard.press('q');assert desktop.evaluate('window.turnCalls')==1
        desktop.keyboard.down('ArrowLeft');assert desktop.evaluate('RE1Input.mask()')==4
        desktop.keyboard.press('F2');assert desktop.locator('#settings').evaluate('d=>d.open')
        desktop.keyboard.up('ArrowLeft');assert desktop.evaluate('RE1Input.mask()')==0
        desktop.locator('#browser-fullscreen').click();desktop.wait_for_function('()=>!!document.fullscreenElement')
        desktop.locator('#open-logs').click();assert desktop.locator('#diagnostics').evaluate('d=>d.open')
        desktop.keyboard.press('F2');assert not desktop.locator('#settings').evaluate('d=>d.open')
        assert desktop.evaluate('document.activeElement.id')=='canvas'
        desktop.keyboard.down('ArrowRight');assert desktop.evaluate('RE1Input.mask()')==8
        desktop.keyboard.up('ArrowRight');assert desktop.evaluate('RE1Input.mask()')==0
        desktop.wait_for_function('()=>document.querySelector("#error").open',timeout=30000)
        assert desktop.evaluate('RE1Diag.graphicsPassed')
        print('PASS: desktop keyboard chords/releases, Q, F2/settings, fullscreen, Logs, engine graphics/audio and return dialog')
        desktop.close()

        mobile=browser.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
        mobile.goto(url);mobile.wait_for_function('()=>!document.querySelector("#folder").disabled')
        assert mobile.evaluate('RE1Input.settings.hidden') is False
        assert mobile.locator('.launch-card').bounding_box()['width']>330
        mobile.locator('#browser-remember').uncheck();mobile.locator('#browser-folder-input').set_input_files(str(game))
        mobile.wait_for_function('()=>RE1BrowserStorage.ready()')
        mobile.locator('#launcher-settings').click();mobile.locator('#movement').select_option('joystick')
        mobile.locator('#browser-auto-fullscreen').uncheck();mobile.locator('#close-settings').click()
        mobile.set_viewport_size({'width':960,'height':540})
        mobile.locator('#graphics-test').click();mobile.wait_for_function('()=>RE1Diag.frames>=3',timeout=90000)
        mobile.evaluate('Module._re1_web_suspend(1)')
        mobile.evaluate('re1TouchContext(false)');assert mobile.locator('#joystick').is_visible()
        mobile.evaluate('re1TouchContext(true)');assert mobile.locator('#touch-up').is_visible()
        mobile.evaluate("RE1BrowserStorage.io('Data/fontus.tim')");assert mobile.locator('#browser-loading-file').is_visible()
        mobile.locator('#gear').click();mobile.locator('#show-loading-files').uncheck()
        assert mobile.locator('#browser-loading-file').is_hidden()
        mobile.locator('#edit-layout').click();mobile.locator('#layout-control').select_option('joystick')
        mobile.locator('#layout-size').fill('130');mobile.locator('#layout-size').dispatch_event('input')
        assert mobile.evaluate('RE1Input.settings.sizes.joystick')==1.3
        mobile.locator('#save-layout').click();mobile.locator('#close-settings').click()
        mobile.wait_for_function('()=>document.querySelector("#error").open',timeout=30000)
        assert mobile.evaluate('RE1Diag.graphicsPassed')
        with mobile.expect_navigation(wait_until='load'):
            mobile.locator('#reload').click()
        mobile.wait_for_function('()=>!!window.RE1Input&&!!window.RE1BrowserStorage&&!document.querySelector("#folder").disabled')
        assert not mobile.evaluate('RE1BrowserStorage.ready()')
        assert mobile.evaluate('RE1Input.settings.sizes.joystick')==1.3
        print('PASS: phone portrait/landscape layout, local import without retention, joystick/menu arrows, resizing, filename toggle, real graphics/audio, reload/settings persistence')
        mobile.close();browser.close()
finally:server.shutdown()
