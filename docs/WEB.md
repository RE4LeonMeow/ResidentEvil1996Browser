# Resident Evil 1.00 — browser package

Made by **4wu4_**, based on
[ecruells/resident-evil-pc-decomp](https://github.com/ecruells/resident-evil-pc-decomp).
The upstream decompilation remains credited to its own contributors.

This ZIP is a standalone static package for PC and phone browsers. It contains
the engine and launcher, with no game data. It is provided as a download; no
website is deployed by the packaging scripts.

## Run locally on a PC

1. Extract `resident-evil-browser-1.00.zip`.
2. Double-click **index.html** in the extracted folder to open the launcher.
   Keep all extracted files together. The matching WebAssembly is included in
   the engine script, so direct local opening needs no separate wasm fetch.
3. Use a modern browser with WebGL and folder selection support.
4. Choose **Select game folder** and select your complete installed/extracted
   USA GOG game folder, or its `USA` directory. Keep Data, Stage, Movie, Sound,
   Voice and other game folders together. Extract installers/archives first.
5. Tap **Launch game**.

For a stable local save origin, open a terminal in the extracted folder and
run `python3 serve.py` (`python serve.py` on Windows), then open
**http://localhost:8000**. Python 3 is needed only for this optional local server.
Selected game files are read directly by the browser; they are not sent to
that server or bundled with the package. Direct-file saves depend on the
browser's local-file storage permissions; use localhost for a stable save origin.

## Use in another repository or on a phone

Copy the extracted package's **contents** into your chosen site's static
directory. Serve it over **HTTPS** with `.wasm` files as `application/wasm`.
It works in a subdirectory and needs no `/manifest` or `/data` server endpoints,
backend process, cross-origin isolation or CDN dependencies. Keep the bundled
license notices and credit to upstream.

On phones, open that HTTPS page in a modern browser with folder selection and
WebGL support, then choose the locally installed game folder. Android Chrome
and Edge are the initial phone targets. The browser's picker may use the word
"upload" for folder selection; this application keeps the files on the device.
Other browsers, including iOS Safari, need device testing, particularly folder
selection, local Blob reads, storage quota, audio and fullscreen behavior.

Touch controls appear by default on touch devices. Desktop browsers default to
hidden touch controls; change **Hide touch controls** in settings to show them.
Rotate a phone sideways for more space. Fullscreen on launch defaults on for
touch devices and can be changed in settings; **Fullscreen** also provides a
manual toggle. Browsers may restrict fullscreen and orientation locking.

## Controls and settings

**Touch button behavior** offers Hold or Toggle for each touch button. Active
toggles glow amber. Settings, menu transitions, hidden controls and app focus
changes release them. Menus use normal taps; keyboard/gamepad input and joystick
movement remain held, and TURN stays a one-shot action.

**Experimental · More FPS** inserts geometry render frames while keeping
original game simulation/timers at approximately 30 Hz. It starts off and
returns to original frames for movies, doors, menus, changed scenes/geometry or
slow frames. Resolution, textures and filtering are preserved. Extra GPU work
can increase heat or latency, and 60 FPS is not guaranteed. The FPS overlay
counts rendered frames; diagnostics include the interpolated-frame count.
Slow frames trigger about two seconds of original rendering before retrying.
Delays detected after submitting a generated frame trigger a longer five-second
backoff, covering GPU/compositor stalls that a CPU-only budget can miss.

Version 1.00 includes **Controls & settings → Cheats**. Accept the experimental
warning to access infinite health/ammo, heal, refill carried weapons, open the
item box, or open the ordinary save-slot picker without an ink ribbon. Actions
require normal player control. Cheats reset on return to the launcher, but changes
already saved remain in that slot. Use a separate slot. Infinite health keeps HP
full; scripted instant deaths may still occur.


- **PC:** arrows move, **C / Enter** confirms, **Ctrl / V** runs/cancels, **X** aims,
  **Z** opens inventory, **P** requests game options, **Q** quick-turns and **F2**
  opens/closes launcher settings. Choose Yes/No with arrows, then confirm.
  These shortcuts use the same game actions as the touch controls.
- **Phones:** D-pad or joystick, automatic menu arrows, editable positions and
  individual sizes, opacity, ACTION/RUN/AIM/ITEMS/PAUSE and TURN.
- **Controllers:** standard browser gamepads use the left stick/D-pad and
  configurable button mappings/dead zone. Pair through the device's settings.
  Physical controller coverage still needs testing.
- Original **4:3** or optional **16:9**. Inventory and pickup screens are rearranged
  across the wider viewport, keeping text, icons and models proportional. The
  item preview stays centered in its expanded frame. Item boxes use a separate
  wide arrangement, with their lid animation retaining the world framing.
  Map/file selectors share the wide menu frame, zoomed maps keep their markers
  aligned, and document pages keep proportional lettering in a centered layout.
  Save screens and options retain their complete original layout. The same door/grab framing as the
  Android port, FPS toggle, transparent loading filenames, Logs, renderer
  compatibility selection and graphics/sound test.
- **Launcher** flushes saves and returns to the launcher. Browser reload after
  a failure is also available. Changing renderer applies on the next launch.
- **Donation** opens the maintainer’s message first, with Cancel/OK. Crypto
  addresses appear only after OK. **X**, **Discord** and **GitHub** open in a separate tab.
- **Credits** opens a menu dialog, including direct `index.html` launches.
  Localhost/hosted builds read the included `plain.txt` on every open. Direct
  launches use a bundled text snapshot because browsers restrict reading local
  files: edit the source `android/app/src/main/assets/web/plain.txt` and rebuild
  the ZIP, or run `serve.py` to read edits to an extracted `plain.txt` directly.

Original image resolution, textures, filtering and game timing are preserved.
The 0.9.1 rendering and timer optimizations are included.

## Local files and saves

**Remember game files in this browser** stores an optional browser-managed copy
of the selected files so they can be restored after reloading. Allow enough
storage for the full game directory. If the copy exceeds browser quota, the
current selection still works; select it again after reloading, or leave the
option unchecked. **Forget imported files** removes this game's imported copy
and keeps saves and control settings. It does not delete the original folder.

The engine reads files in bounded chunks with a 16 MiB cache; it does not load
the whole game into WebAssembly memory. Progress saves and `config.ini` use
separate browser IndexedDB storage; controls use localStorage. Saves belong to
this browser profile and this site's origin. Moving to another site, another
browser or the Android APK does not automatically transfer saves. Clearing site
data/private browsing can delete them.

Return to the launcher after saving in-game and open **Save backups**.
**Export saves** downloads a `.saves.zip` file containing the original saved-slot `.dat` files.
**Import saves** validates a backup and asks before replacing its matching
slots. Other slots, settings and imported game files stay intact. Android and
browser editions share the format, so backups can be moved between them or
to another browser/site. Close other game tabs first. The backup contains
saved progress, not a snapshot of unsaved gameplay. These controls also work
when opening `index.html` directly.

ZIPs of original USA GOG `savedat1.dat` through `savedat8.dat` files also
work. Put the files at the ZIP root or inside `SAVE/`. Slot names are
case-insensitive; both 2048-byte compact and 2690-byte extended saves are
supported. Stored and ordinary Deflate ZIPs are accepted; compressed ZIPs need
a browser/WebView with `DecompressionStream` support for `deflate-raw`.
Exported ZIPs hold unchanged `.dat` files for the PC game's `SAVE` folder.
Back up existing PC saves before replacing them. ZIP backups are limited to
128 KiB and at most eight slots; encrypted and split archives are unsupported.

## Mod support

**Mod support is in the works.** Version 1.00 targets original USA game data;
a general mod/replacement-texture loader is not available in this release.

## Build and validation

Build the shared engine with `tools/web/build.sh`, then run
`python3 tools/web/package.py`. The static files are written to `build/browser`
and the standalone ZIP to `build/resident-evil-browser-1.00.zip`. The package
script uses an explicit application-file allowlist and includes no selected
game files, saves, testing captures, server-side game directory or signing keys.

The browser uses the same wasm32 engine, SDL/WebAudio, FFmpeg movie decoder and
WebGL 1/2 renderer as the Android APK. Movie soundtracks use a scheduled
WebAudio source and a shared audio/video clock; game sound effects and music
retain the SDL mixer. Local file reads use short-lived Blob URLs, not game-file
requests to the website. If a host supplies its own Content
Security Policy, allow `connect-src 'self' blob:` and WebAssembly compilation
(`script-src 'self' 'wasm-unsafe-eval'`); the supplied HTML already defines this.

PC/mobile Chromium checks and local private-data smoke tests are documented in
the repository's Android/browser development notes. These do not establish
complete playthrough coverage or support on every physical phone/browser.

Code uses GPL-3.0, with GPL-3.0-or-later notices for adapted FusionFix widescreen
code. Runtime/dependency notices are in `licenses/`. The supplied logo,
background and icon are separately owned artwork and are not relicensed by the
code license. This independent project is unaffiliated with Capcom or GOG.
