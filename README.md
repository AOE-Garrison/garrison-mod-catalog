# Garrison mod catalog

Public mod catalog for Garrison. Players can browse and download without a GitHub account. Maintainers publish mod ZIPs through GitHub Releases; ZIPs and SGA files never belong in Git history.

Each release ZIP contains `garrison.json`, its referenced archives and an optional cover beside the manifest. The manifest supplies all card details. `catalog.config.json` selects the version to list for each mod ID; `catalog.json` and `covers/` are generated.

## Publish a mod

1. In Blender, fill the Package details and press **Package for Garrison**.
2. From this repository, run `python scripts/publish_mod.py path/to/<id>-<version>.zip`.
3. Review, commit and push the updated `catalog.config.json`.
4. Check the **Build mod catalog** workflow, then Sync in Garrison.

The publisher validates archive paths, hashes, manifest details and covers before creating `<id>-v<version>` with asset `<id>-<version>.zip`. Existing releases are never overwritten. Raise the semantic version for every update, and keep bundle and member keys stable.

## Connect Garrison

Open **Mods > Catalog > Sync**. The default source is:

```text
https://raw.githubusercontent.com/AOE-Garrison/garrison-mod-catalog/main/catalog.json
```

Sync refreshes the catalog. Installing or updating a selected mod verifies its ZIP size and SHA-256. Enabling a mod does not choose its map, Game Mode or Tuning Pack in the lobby; follow that mod's launch instructions.

The Garrison product repository and product distribution are separate from this public catalog.

[Author instructions](docs/ADDING_MODS.md) include the transition from older catalog releases.
