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

Card metadata does not change in-game text. Update ArmyBP/RaceBP/Codex and their
private localization explicitly when those surfaces need a change.
