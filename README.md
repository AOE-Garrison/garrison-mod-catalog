# Garrison mod catalog

Private catalog for [Garrison](https://github.com/AOE-Garrison/aoe4-modding-kit).
Organization owners already have administrator access; no separate invitation is needed.

```text
mods/
  overfootball/      mod.toml + cover.jpg
  ram-napkin-race/   mod.toml + cover.jpg
templates/mod.toml  labelled form for the next mod
scripts/            create, prepare, publish and validate
catalog.json        generated index; do not edit by hand
```

## Add a mod

1. Install Python 3.11+ and GitHub CLI. Run `gh auth login` with a repository member account.
2. Run `python scripts/new_mod.py my-mod --name "My Mod" --author "Author"`.
3. Fill `mods/my-mod/mod.toml`. Put `cover.jpg` or `cover.png` alongside it and set `cover = "cover.jpg"`. No filename prefix is required. Use 1600×600, up to 4 MiB.
4. Commit and push the metadata and cover to `main`.
5. Publish the prepared bundle: `python scripts/publish_mod.py my-mod path/to/bundle.zip`.
6. Check the **Build mod catalog** Actions run. It verifies every archive/hash and commits the new index. A failed build keeps the previous index intact.

The source ZIP must contain exactly one `mod.bundle.json` and its referenced SGA files. The script inserts the matching description and cover. ZIPs belong in GitHub Releases, never in Git history.

For updates, keep the folder, `details.id`, bundle key and member keys stable. Increase `version`, `release_tag` and `asset`; update the date and changelog. Published releases are immutable: do not replace a ZIP under the same version. Use a new version to correct it.

A metadata push before its release exists can fail validation; publishing the release triggers another run. Alternatively publish after preparing the metadata locally and dispatch the workflow once everything is present.

## Connect Garrison

Use the Garrison build with private catalog support. Sign in once with `gh auth login` on the player's computer. In **Mods → Catalog → Source**, enter:

```text
https://api.github.com/repos/AOE-Garrison/garrison-mod-catalog/contents/catalog.json?ref=main
```

Press **Sync**. Garrison uses the existing GitHub CLI login and does not save a token in its catalog cache. Access is limited to repository members while this repository is private. Index, covers and downloads use the authenticated GitHub API; storage redirects receive no GitHub token.

For diagnostics, `garrison-play catalog-sync <source-url>` uses the same implementation.

[Подробная инструкция на русском](docs/ADDING_MODS.ru.md).
