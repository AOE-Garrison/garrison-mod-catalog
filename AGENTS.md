# Catalog maintenance

This is the private AOE-Garrison mod catalog, separate from product source.
Keep one labelled `mod.toml` and an optional cover in each `mods/<stable-id>/`.
See README.md and docs/ADDING_MODS.md for the author workflow.
Write repository documentation and contributor instructions in English.

Keep package ZIPs in Releases. Never commit SGA files, Blender scenes, secrets,
tokens, proprietary source assets or machine-specific paths. Do not change
repository visibility or publish to another destination without user direction.

Keep IDs and bundle/member keys stable. Use new semantic versions, release tags
and asset names for updates. Do not overwrite existing release assets. Validate
archive paths, hashes and package roles before generating catalog.json. Publish
the generated index only after the entire catalog validates; preserve the prior
index on failure. Do not hand-edit hashes or sizes.

Shared catalog scripts originate in aoe4-modding-kit/tools/catalog; carry fixes
back there and test the changed boundary. The private route uses GitHub API
URLs and existing GitHub CLI authentication. Never put credentials in URLs,
catalog metadata, logs or committed files. No script executes mod contents.
