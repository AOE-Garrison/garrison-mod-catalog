# Garrison mod catalog

Public mod catalog for Garrison. Players can browse and download without a GitHub account. Maintainers publish mod ZIPs through GitHub Releases; ZIPs and SGA files never belong in Git history.

Each release ZIP contains `garrison.json`, its referenced archives and an optional cover beside the manifest. The manifest supplies release details. `catalog.config.json` selects the version and browsing category for each mod ID; `catalog.json` and `covers/` are generated.

## Publish a mod

1. In Blender, fill the Package details and press **Package for Garrison**.
2. From this repository, run `python scripts/publish_mod.py path/to/<id>-<version>.zip --category games-scenarios`.
3. Review, commit and push the updated `catalog.config.json`.
4. Check the **Build mod catalog** workflow, then Sync in Garrison.

The publisher validates archive paths, hashes, manifest details and covers before creating `<id>-v<version>` with asset `<id>-<version>.zip`. Existing releases are never overwritten. Raise the semantic version for every update, and keep bundle and member keys stable.

Choose `civilizations`, `games-scenarios`, `enhancements` or `maps`. New and
unclassified mods require `--category`; updates retain their existing category
when it is omitted. Categories describe purpose, separately from Map / Tuning /
Mode component badges. Category-only edits need no new ZIP or release.

Publish the matching client before activating packages requiring it. Garrison
0.1.8 reads `catalog-v2.json`; `catalog.json` remains a filtered 0.1.7 feed.
Older clients reject new fields before evaluating minimum versions.

## Connect Garrison

Open **Mods > Catalog > Sync**. The default source is:

```text
https://raw.githubusercontent.com/AOE-Garrison/garrison-mod-catalog/main/catalog-v2.json
```

Sync refreshes the catalog. Installing or updating a selected mod verifies its ZIP size and SHA-256. Enabling a mod does not choose its map, Game Mode or Tuning Pack in the lobby; follow that mod's launch instructions.

The Garrison product repository and product distribution are separate from this public catalog.

[Author instructions](docs/ADDING_MODS.md) include the transition from older catalog releases.

For independent civilizations, read the [maintainer and AI handoff](docs/CIVILIZATION_MAINTAINER_HANDOFF.md),
[card preset](docs/CIVILIZATION_CARDS.md) and [0.1.8 release checklist](docs/RELEASE_0.1.8.md).
