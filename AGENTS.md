# Catalog maintenance

This is the public AOE-Garrison mod catalog, separate from private product source. Write repository documentation and contributor instructions in English.

Use `catalog.config.json` to select mod IDs, versions and browsing categories. Release metadata comes from ZIPs containing `garrison.json`; `details.id` must equal the bundle key. Categories are separate publisher assignments, not package component types. Use the publisher's `--category` for new or unclassified mods. Generate `catalog-v2.json` for 0.1.8 and the filtered `catalog.json` for 0.1.7 in one build, with `covers/`. See README.md and docs/ADDING_MODS.md.

Keep package ZIPs in Releases. Never commit SGA files, Blender scenes, secrets, tokens, proprietary source assets or machine-specific paths. Do not change repository visibility or publish to another destination without user direction.

Keep bundle and member keys stable. Use new semantic versions, release tags and asset names for updates. Never overwrite existing releases. Validate paths, hashes, details and roles before publishing the index; preserve the prior index on validation failure. Do not hand-edit hashes or sizes.

Shared catalog scripts originate in aoe4-modding-kit/tools/catalog. Carry shared fixes upstream and test the changed boundary. Do not execute mod contents. Never put credentials in URLs, metadata, logs or committed files. Packaging validation does not establish gameplay or multiplayer compatibility.
