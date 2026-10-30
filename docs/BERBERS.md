# Berbers 0.1.1

Berbers by **hosein81 and marcokistan** is an independent civilization in the
Civilizations category. Install and enable it in Garrison **0.1.9 or newer**,
launch through Garrison, then select **Berbers / Standard / Tuning Pack: None**.
Disable the old replacement Berber package. The author's pilot used a human
Dark Age start with a stock opponent.

- [Catalog release](https://github.com/AOE-Garrison/garrison-mod-catalog/releases/tag/berbers-v0.1.1)
- [Original project and editable sources](https://github.com/hoseinm1381/aoe4-berbers)
- [Upstream 0.1.0 release](https://github.com/hoseinm1381/aoe4-berbers/releases/tag/v0.1.0)
- [Original credits](https://github.com/hoseinm1381/aoe4-berbers/blob/main/CREDITS.md)

## Catalog edition

Catalog version 0.1.1 adds the card's historical period, three-star difficulty,
gameplay themes and six bonus rows, plus player instructions, full original
credits and provenance. The SGA and original flag cover are byte-identical to
upstream 0.1.0. This is a presentation and documentation release; it contains no
gameplay, model, texture, script or audio changes.

Period, themes and bonus text come from the packaged English localization,
IDs 5002, 5003 and 5010–5021. Difficulty comes from the packaged ArmyBP. The
card description follows those authored mechanics. The existing bundle/member
key `berbers` and native owner `5fe8767cca3a4e649e20c9527cf014ec` are retained.
Category `civilizations` is assigned in catalog.config.json. The release is
listed in catalog-v2.json and excluded from the legacy 0.1.7 feed.

## Independent package review — October 30, 2026

| Check | Result |
| --- | --- |
| Upstream ZIP SHA-256 | `b8c016ecfba0c4fab3a210bd4b4a58eed6a088fbbe8dac759f65a35c19e9f7dd` |
| Catalog ZIP SHA-256 | `dba912f5a0b3082af27e4f090b3e7fe34b57063e4129285d09284e654f4db13e` |
| Catalog ZIP size | 615,106,849 bytes |
| Unchanged SGA SHA-256 | `78d4f0f3878f26aae3ff122ca92a9809c4dbdf430b647ebafccf2bce47061482` |
| SGA size | 771,517,836 bytes |
| Archive readback | All 2,849 members decoded; CRC32 and SHA1 block checks passed |
| Native declaration | Owner/header agreement, additive Boolean false root, one flat RaceBP and final root/race/dispatcher hashes passed |
| Native classification | Civilization; no bundled map or Game Mode; audio present |
| Blueprint graph | 293 definitions; 276 distinct private typed references resolved |
| Stock dependencies | 574 distinct typed references matched uniquely in the installed stock attribute inventory |
| Prematch roster | All 67 private entity and 52 private squad definitions included, plus 79 resolvable stock entities |
| SCAR identity audit | 25 scripts; no foreign private-owner literals or unresolved own blueprint-name literals |
| Catalog package | Strict manifest/role/details validation, archive SHA-256 and ZIP CRC checks passed |

The native reader checked the manifest, archive identity and civilization
declaration directly. A trial library import was refused because AoE IV was
running; no import, staging or gameplay test was completed by this review.
The current game session and installed mod library were preserved. Mod scripts
were inspected as data, not executed.

These checks establish package integrity and static integration, not in-game
appearance or complete gameplay behavior. Stock-reference inventory checks do
not simulate opaque resource loading or script-generated references.

## Runtime acceptance boundary

The [author's release notes](https://github.com/hoseinm1381/aoe4-berbers/blob/main/docs/RELEASE_NOTES.md)
report that trial.3 loaded and worked. Upstream 0.1.0 preserves that gameplay
but changes native flag presentation; that flag layout still needs a fresh
in-game visual check. This catalog edition retains the same boundary.

Detailed age-up, training and ability coverage, AI, alternate starts, repeated
matches, save/load, replays and performance remain separate acceptance gates.
Multiplayer support is not claimed. A successful catalog build or archive
readback does not qualify those routes.

## Attribution and updates

Original Future Kingdoms credits: **hossein81** and **marcokistan** (lead
developers), **Karyu** and **lammet** (media), and **ForsakenCryz** (original
idea, early development and civilization QA). The original wording and spelling
are retained in CREDITS.txt and UPSTREAM-START-HERE.txt inside the ZIP.

Keep the upstream project as the source of gameplay and assets. Preserve the
bundle/member keys and owner when publishing updates, assign a new immutable
version, and keep ZIPs in Releases. To stop using the mod, close AoE IV and
disable Berbers in Garrison. Keep an accepted previous package for rollback.
