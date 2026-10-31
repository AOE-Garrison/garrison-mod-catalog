# In-game player colors

`player_colors` 0.1.0 by overbait requires the complete Garrison 0.1.10 player
distribution and AoE IV 17.0.12182. It belongs to `enhancements`, with member
role and content type `player-colors`. Only `catalog-v3.json` lists it.

The SGA contains one declaration, `garrison/player-colors.json`:

```json
{"schema":"garrison.player-colors-package/v1"}
```

The package carries no game assets, shader bytecode, executables or personal
palettes. The client owns the interactive card and guarded runtime. A client
layout or runtime fix does not require another version of this unchanged mod.
If the declaration or release metadata changes, publish a new immutable version
and validate the entire package normally.

The card spans two ordinary columns and uses a text heading with inline author
credit instead of a cover. It supplies a segmented color wheel, per-player
markers, lightness/chroma/hue sliders, harmony and variant menus, team sectors,
pinning and Enabled. Selecting a marker scopes sliders to that player;
deselecting it edits the whole palette. Formats include 1v1 through 4v4 and
eight-player FFA. Marker 1 follows the local player regardless of lobby order.
Standard details, update and removal actions use the normal mod library.

Use a local single-player match launched through Garrison with unique lobby
colors. No Tuning Pack selection is needed. The runtime synchronizes models,
health bars, names, occlusion silhouettes, minimap marks and tribute names.
Disabling restores original colors; removing/updating preserves the saved
palette. In-game UI Colors remains a separate compatible enhancement.
Player Colors has not been qualified for multiplayer.

Publish only metadata, documentation and required package declarations here.
Never add palette preferences, process dumps or game-derived shader captures to
the catalog repository or release ZIP.
