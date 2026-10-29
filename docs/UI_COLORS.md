# Publishing In-game UI Colors

This is an optional enhancement package for Garrison 0.1.8 or later. Its stable
bundle and member key is `ui_colors`; its role and content type are `ui-colors`.
The catalog category is `enhancements`. Credit `overbait`.

The ZIP contains the normal `garrison.json`, `ui_colors.sga`, cover and player
instructions. The SGA has one `data` TOC: `garrison/ui-colors.json` plus the
fixed inventory of 29 palettes, three compiled UI shaders each. The declaration
uses `garrison.ui-colors/v1` and binds each shader by SHA-256. The client rejects
unknown presets, missing/extra members, invalid containers and changed hashes.

Renderer executables are part of the qualified Garrison player distribution.
Never put a DLL, ASI, addon binary, executable path or a machine-local graphics
manifest in this mod. A package cannot select an executable for the client to
load. No files are installed into the Steam game directory.

Build from a reviewed local palette inventory with the shared product tool
`tools/ui_colors/package_presets.py`. It verifies shader hashes, compiles the
SGA and reads back every member before producing the release ZIP. Use a new
output directory and an immutable release version. Run the catalog package
validator and test installation in a separate clean Garrison state directory.

The card deliberately omits version/date text to make room for palette controls;
both fields remain required in metadata and govern catalog updates. It uses
ordinary card dimensions and an Enabled toggle. Clicking the selected palette
restores standard colors; disabling retains the last choice. Live palette
switching and archive install/remove have different lifecycle boundaries.

Check clean installation, offline selection persistence, cache repair, updates,
removal and renderer acknowledgement. A successful archive readback is not
evidence that a palette was applied to a running game.
