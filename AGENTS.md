# Catalog maintenance

This is the public AOE-Garrison mod catalog, separate from private product source. Write repository documentation and contributor instructions in English.

Use `catalog.config.json` to select mod IDs and versions. All metadata comes from release ZIPs containing `garrison.json`; `details.id` must equal the bundle key. `catalog.json` and `covers/` are generated. See README.md and docs/ADDING_MODS.md.

Keep package ZIPs in Releases. Never commit SGA files, Blender scenes, secrets, tokens, proprietary source assets or machine-specific paths. Do not change repository visibility or publish to another destination without user direction.

Keep bundle and member keys stable. Use new semantic versions, release tags and asset names for updates. Never overwrite existing releases. Validate paths, hashes, details and roles before publishing the index; preserve the prior index on validation failure. Do not hand-edit hashes or sizes.

Shared catalog scripts originate in aoe4-modding-kit/tools/catalog. Carry shared fixes upstream and test the changed boundary. Do not execute mod contents. Never put credentials in URLs, metadata, logs or committed files. Packaging validation does not establish gameplay or multiplayer compatibility.
