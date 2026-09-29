# Garrison mod catalog

Public mod catalog for Garrison. The Garrison product source repository remains
private. Players need no GitHub account, repository invitation or GitHub CLI
to browse this catalog or download its mods.

```text
mods/
  overfootball/      mod.toml + cover.jpg
  ram-napkin-race/   mod.toml + cover.jpg
  modding-showcase/  mod.toml + cover.jpg
templates/mod.toml  labelled form for the next mod
scripts/            create, prepare, publish and validate
catalog.json        generated index; do not edit by hand
```

## Add a mod

1. Install Python 3.11+ and GitHub CLI. Run `gh auth login` with a repository member account.
2. Run `python scripts/new_mod.py my-mod --name "My Mod" --author "Author"`.
3. Fill `mods/my-mod/mod.toml`. Put `cover.jpg` or `cover.png` alongside it and set `cover = "cover.jpg"`. No filename prefix is required. Use 1600Г—600, up to 4 MiB.
4. Commit and push the metadata and cover to `main`.
5. Publish the prepared bundle: `python scripts/publish_mod.py my-mod path/to/bundle.zip`.
6. Check the **Build mod catalog** Actions run. It verifies every archive/hash and commits the new index. A failed build keeps the previous index intact.

The source ZIP must contain exactly one `mod.bundle.json` and its referenced SGA files. The script inserts the matching description and cover. ZIPs belong in GitHub Releases, never in Git history.

For updates, keep the folder, `details.id`, bundle key and member keys stable. Increase `version`, `release_tag` and `asset`; update the date and changelog. Published releases are immutable: do not replace a ZIP under the same version. Use a new version to correct it.

A metadata push before its release exists can fail validation; publishing the release triggers another run. Alternatively publish after preparing the metadata locally and dispatch the workflow once everything is present.

## Connect Garrison

Open **Mods > Catalog > Sync** in Garrison. Current builds already have this
address configured. In an older build, paste it once under **Source**:

```text
https://raw.githubusercontent.com/AOE-Garrison/garrison-mod-catalog/main/catalog.json
```

The index, covers and mod ZIPs are public HTTPS downloads. Garrison remembers
the successful source. Sync refreshes the catalog; the download/update button
installs a selected mod and verifies its published size and SHA-256. No player
sign-in, GitHub CLI or organization membership is required. GitHub authentication
is still required for maintainers who publish releases and edit this repository.

Obtain the Garrison player ZIP from the maintainer or the private product
repository if you have access. Making this mod catalog public does not make
product source or product releases public.

For diagnostics, `garrison-play catalog-sync <source-url>` uses the same implementation.

[Detailed author instructions](docs/ADDING_MODS.md).
