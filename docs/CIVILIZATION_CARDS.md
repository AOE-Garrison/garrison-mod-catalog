# Civilization card preset

Set the catalog category to `civilizations` in `catalog.config.json` or the
publisher's `--category`. This is browsing metadata, separate from the archive
role and `details.content_types`. Use the template in
`templates/civilization-details.json` as the `details` object of `garrison.json`.
Replace every example value; never publish its example ID or pretend hash.

Use the civilization's flag as `details.cover`, placed beside `garrison.json`.
It is also the small header flag and the subdued card background. Supply an
ordinary PNG, JPEG or WebP, at most 4 MiB, with a plain filename of at most
64 characters. Do not ship game fonts; Garrison supplies typography/fallbacks.
Native in-game flags require separate cooked assets described in the handoff.

| Field | Editorial preset |
| --- | --- |
| `name` | Public civilization name, without version or marketing prefix |
| `summary` | One useful sentence, at most 180 characters |
| `description` | Approximately 300–340 characters for the card; plain prose, no status filler |
| `author` | Actual author names, at most 100 characters; no integration credits appended |
| `updated` | Real publication date, `YYYY-MM-DD` |
| `version` | Immutable semantic release version |
| `min_garrison` | At least `0.1.8` for independent civilizations |
| `civilization.period` | Historical period, not the release date |
| `civilization.difficulty` | 1, 2 or 3; omit when unknown |
| `civilization.tagline` | Short gameplay themes |
| `civilization.bonuses` | Specific, verified mechanics in separate rows; up to 24 |

Cards span two ordinary grid columns including the intervening gap. Keep paired
introductions comparable in length. Detailed bonuses belong behind the `i`
button, not in a long scrollable card introduction. Enabled state comes from
Garrison, so do not add "Ready for your next game" to metadata. The category
subtitle uses project counts and catalog groups sort newest update date first.

## Garrison 0.1.10 presentation

The Catalog overview shows only the five newest civilizations in one overlapping
row. Hover briefly to reveal a card, click to keep it open, and click outside or
press Escape to collapse it. **View all** opens the complete Civilizations
category; additional entries never create another overview row. Installed and
the complete category retain their ordinary grids.

Every overlap state uses the full card layout. Text keeps its expanded wrapping
while neighboring cards and the right-edge gradient cover it. Do not prepare a
second collapsed description, insert manual line breaks to fit a visible strip,
or draw text, a fade or buttons into the flag image. Garrison owns the fade,
animation, clipping and responsive layout.

The footer sits inside the flag artwork: author on the left, version and update
date together, then the activation switch and action icons on the right. Narrow
windows stack these controls. Installed and uninstalled neighbors share a
height. Garrison supplies Enabled, details, install/update and removal controls;
metadata must not imitate them. Keep the real author credit intact rather than
shortening names to make space for controls.

These are client-side changes. Existing accepted packages and flag images do
not need a new version or a recook. Raise the package version only when its
actual contents or metadata change. The new layout does not change the existing
`civilization` role or the package's minimum version requirement.

Card metadata does not change in-game text. Update ArmyBP/RaceBP/Codex and their
private localization explicitly when those surfaces need a change.
