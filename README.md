## **Resident Evil (1996) Browser Port**

**Android edition:** https://github.com/RE4LeonMeow/ResidentEvil1996Android

**Play in your browser:** https://re4leonmeow.github.io/ResidentEvil1996Browser/

Hey! This is my unofficial browser port of Resident Evil 1 for PC and phones,
based on
[ecruells/resident-evil-pc-decomp](https://github.com/ecruells/resident-evil-pc-decomp).
Huge thanks to ecruells and everyone who worked on the decompilation. This
port uses their engine and adds the browser launcher, local file loading,
touch controls and other features below.

You bring your own GOG PC files, select the folder and play. **No game files
are included in this repo, the website or the browser ZIP.**

## What it has

- Keyboard, controller and touch controls for PC and phones.
- Arrows or a joystick, automatic arrows in menus, movable/resizable touch
  buttons, opacity settings and Hold/Toggle options.
- Optional 16:9 mode, including rearranged inventory, item box and pickup
  screens that keep text and items in proportion.
- Quick turn, fullscreen, a togglable FPS counter and optional loading filenames.
- Experimental **More FPS** mode. It adds extra rendered frames without
  speeding up the game, but it does not guarantee 60 FPS.
- An experimental Cheats tab with infinite health/ammo, healing, ammo refill,
  item box access and saving without an ink ribbon.
- Optional browser storage for remembering your selected game files.

## What you need

- A modern browser with WebAssembly, WebGL and folder selection support.
  Chrome or Edge are good starting points on PC and Android.
- Your own installed/extracted **USA GOG PC version of Resident Evil 1**.
- Enough browser storage if you want it to remember the game files.

Other browsers and iPhones can have different file-picker, storage and
fullscreen restrictions, so compatibility depends on the browser and device.

## How to play

### Online

1. Open the browser edition using the page link at the top of this README.
2. Click **Select game folder** and choose your complete installed GOG game
   folder, or its `USA` folder.
3. Click **Launch game** and enjoy!

On a phone, keep the extracted game folder in local storage and rotate your
phone sideways. The browser might call the folder selection an "upload",
but **the port reads your files locally and does not upload them**.

Keep `Data`, `Stage1` and the other stage folders, `Sound`, `Voice`, `Movie`
and the remaining game folders together. Select the extracted folder, not a
ZIP, installer `.exe` or disc image.

### Locally on a PC

1. Download the browser ZIP from this repo's **Releases** page.
2. Extract it and keep all the extracted files together.
3. Open **index.html** in your browser.
4. Select your game folder and launch.

For a more reliable local save location, open a terminal in the extracted
folder and run:

```sh
python3 serve.py
```

On Windows, use `python serve.py` if needed. Open **http://localhost:8000**.
Python 3 is only needed for this optional local server. It serves the launcher;
your selected game files are still read locally by the browser.

## Controls

### Keyboard

| Key | What it does |
| --- | --- |
| Arrow keys | Move using the original tank controls |
| C / Enter | Interact or confirm |
| Ctrl / V | Run or cancel |
| X | Aim; use confirm while aiming to fire |
| Z | Open inventory |
| P | Open in-game options |
| Q | Quick 180-degree turn during normal movement |
| F2 | Open or close launcher settings |

In-game remapping can change these actions. For Yes/No prompts, use the
arrows to choose and confirm with C or Enter.

### Touch and controllers

Phones show touch controls by default. Open the gear button for
**Controls & settings**, then choose arrows or a joystick. **Edit touch
layout** lets you move and resize controls. **Touch button behavior** offers
Hold or Toggle for each button; toggles glow amber while active.

Touch buttons are ACTION, RUN, AIM, ITEMS, PAUSE and TURN. Use ACTION while
aiming to fire. **Use arrows in menus** switches the joystick to arrows for
menu navigation.

For controllers, pair through your device settings, then press a controller
button so the browser can detect it. Button bindings and the stick dead zone
can be adjusted in launcher settings. Controller support depends on your
browser and device.

## Saves and remembered files

**Remember game files in this browser** stores a local browser-managed copy
for later launches. If storage is full, you can leave it off and select your
folder again next time.

**Forget imported files** removes that imported copy while keeping saves and
control settings. It does not delete your original game folder.

**Saves belong to the browser profile and site where you played.** Switching
browser, moving to another website or using the Android APK does not transfer
them automatically. Clearing site data, private browsing or browser storage
cleanup can remove saves.

To back them up, save in the game first, return to the launcher and open
**Save backups -> Export saves**. Keep the downloaded `.saves.zip` file.
Use **Import saves** in either edition to restore it or move to another browser,
site or phone. Import asks before replacing matching slots; other slots,
settings and game files stay as they are. Close other game tabs first. The
backup contains existing save slots, not an unsaved moment in the game.

Original USA GOG saves work too: ZIP your `savedat1.dat` through
`savedat8.dat` files and use **Import saves**. Files can be at the ZIP's root
or inside `SAVE/`. To use an exported ZIP with the PC game, extract the `.dat`
files into its `SAVE` folder, backing up existing files first.

## FAQ

### Does this include the game?

No, you need your own legally obtained game files. This is the engine and
launcher for loading them.

### Can I play offline?

Yes, use the extracted browser ZIP on your PC. The website itself is not an
installable offline app, so use the local package if you want offline access.

### Why does it need my game folder?

The engine needs the original backgrounds, models, audio and other game data.
It reads them from your local selection. The Windows executable is not run.

### Can I use mods?

**Mod support is in the works.** For now, use the original USA GOG files.

### Why isn't everything 16:9?

Gameplay and supported menus have widescreen layouts. Movies, scripted
cutscenes, save screens and game options keep their complete original image.

### Does More FPS make the game run faster?

No, game speed and timers stay the same. It adds interpolated render frames
in supported scenes. It can increase heat and GPU load, and the result depends
on your device.

### I get a black screen or the game won't launch. What should I try?

Check that your game folder is complete and update your browser. Try
**Test graphics & sound**, then **OpenGL ES 2 - compatibility** in settings
and relaunch. **Skip movies** is also available for troubleshooting. There
is no Vulkan renderer.

If it still fails, open **Logs -> Copy report** and include it with your
browser, device and what you were doing when the problem happened.

### Why can't I select a folder or use fullscreen on my phone?

These features depend on the browser. Try an up-to-date Chrome or Edge on
Android. Fullscreen and orientation locking may still be restricted by the
device. The game can also be played without fullscreen.

### Are cheats safe to use?

They are experimental and can break progression or saves. Use a separate save
slot. Turning cheats off does not undo changes you already saved.

## Credits

Playtesters:

- Kali Kyle
- Vhmed_hosny
- khoilinux

thank you to everyone who tested the port and helped find bugs <3

## Links

- [Discord](https://discord.gg/5PVsXAgvM2)
- [X / Twitter](https://x.com/4wu4_)
- [GitHub](https://github.com/RE4LeonMeow)

There is also an optional **Donation** button in the launcher.

## Source and licensing

The original engine and decompilation are by
[ecruells and contributors](https://github.com/ecruells/resident-evil-pc-decomp).
Widescreen code adapts work from
[ResidentEvilClassicTrilogy.FusionFix](https://github.com/Fusion-Fix/ResidentEvilClassicTrilogy.FusionFix).

Code is distributed under [GPL-3.0](LICENSE), with GPL-3.0-or-later notices
for the adapted FusionFix code. Emscripten, SDL2, FFmpeg, zlib and social
icons have their own bundled notices. Keep the copyright and license notices
when sharing builds or source. Build instructions are in `docs/WEB.md` in
the source tree.

Resident Evil belongs to Capcom. Game assets, launcher artwork and trademarks
are not covered by the code license. This is an unofficial fan project,
unaffiliated with Capcom or GOG. Original game data is not included in this
repo or the downloads.
