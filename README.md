# sleepaqua.github.io

Static portfolio page served straight from `main` by GitHub Pages. No framework and no
build step at deploy time: `index.html` is the whole site, with its CSS inline and no
JavaScript.

To change the page, edit `tools/index.template.html` and rebuild:

    python3 tools/build.py

That script also generates the two chart figures (mahjong-mc and GapFiller) as inline SVG
from the numbers in the tool output, so the charts cannot drift from what the tools print.
Chart data and the commands behind it are documented at the top of `tools/build.py`.

`demos/pacepulse/` is a prebuilt copy of the PacePulse web app, with its asset and
service-worker paths made relative so it runs under a subpath and keeps its own offline
cache scope.
