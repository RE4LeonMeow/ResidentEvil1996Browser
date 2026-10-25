# Building the browser edition

The repository root is the ready-to-host browser site. web/ holds editable
launcher sources; src/ holds the C++ engine. No Android app or APK is included
or required. Keep .nojekyll at the root for GitHub Pages.

Use Linux/WSL2, Emscripten 3.1.69, CMake, Ninja, Make and Python 3. The matching
FFmpeg/SDL/Emscripten runtime sources are bundled in dependency-sources/.

```sh
# Activate your Emscripten installation first.
mkdir -p build/dependency-source/ffmpeg
tar -xzf dependency-sources/ffmpeg-n7.1.1-source.tar.gz --strip-components=1 -C build/dependency-source/ffmpeg
export RE1_FFMPEG_SOURCE="$PWD/build/dependency-source/ffmpeg"
bash tools/web/build.sh
python3 tools/web/package.py
```

The packager updates the site files at the repository root and writes
build/resident-evil-browser-1.00.zip. Commit the changed root site files after
rebuilding; GitHub Pages can deploy main / (root). web/residentevil.js and its
.wasm input are ignored build intermediates; root residentevil.js contains the
matching engine/WASM for direct-file and hosted use. No game data is needed.

Checks: node --test tests/web/unit/*.test.js,
python3 tests/web/browser.py and python3 tests/web/direct_file.py. Browser
checks need Python Playwright/Chromium. Technical notes: docs/WEB.md.
