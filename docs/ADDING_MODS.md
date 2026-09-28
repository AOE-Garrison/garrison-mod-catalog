# Add a mod, cover and description

## File layout

Each mod has its own `mods/<id>/` folder containing:

- `mod.toml`: a UTF-8 text file with labelled fields;
- `cover.jpg` (or PNG/WebP): a 1600 x 600 cover, no larger than 4 MiB.

The image does not need a prefix. Its filename must match the `cover` field.
Upload the mod ZIP to Releases. Do not commit SGA files, ZIPs, Blender scenes
or game source assets to Git.

## Add a mod

From the repository root:

```powershell
gh auth login
python scripts/new_mod.py my-mod --name "My Mod" --author "overbait"
```

Fill in the generated `mods/my-mod/mod.toml`:

| Field | Value |
| --- | --- |
| `release_tag` | A unique tag, such as `my-mod-v0.1.0` |
| `asset` | The release ZIP filename, such as `my-mod-0.1.0.zip` |
| `cover` | `cover.jpg`, or an empty string if there is no cover |
| `details.id` | A permanent ID matching the folder name |
| `name` | The card title |
| `version` | A three-part semantic version, such as `0.1.0` |
| `summary` | A short description, up to 180 characters |
| `author` | The author's name |
| `updated` | The publication date in `YYYY-MM-DD` format |
| `min_garrison` | The minimum supported Garrison version |
| `description` | Details and launch instructions shown by the `i` button |
| `changelog` | Changes in this release |

Include the in-game map and tuning names in the launch instructions.
The MAP/TUNING content type is read automatically from `mod.bundle.json`.

Add the cover, then commit and push the mod folder:

```powershell
git add mods/my-mod
git commit -m "Add My Mod metadata and cover"
git push origin main
python scripts/publish_mod.py my-mod D:/Mods/my-mod.zip
```

The script validates the input ZIP and SGA checksums, adds the description
and cover, and creates a new GitHub Release. The input ZIP is preserved.
Wait for **Build mod catalog** to pass in Actions, then press **Sync** in Garrison.

If validation after the push reports a missing release, run `publish_mod.py`:
publishing the release triggers validation again. For other failures, inspect
the Actions log. A failed build never replaces the last valid catalog.

## Update a mod

Change the version, release tag, ZIP filename, date and changelog. Keep the
same ID and bundle/member keys. Repeat commit, push and publish. Never replace
an existing release asset: even a correction to a published ZIP needs a new version.

## Access and connection

This repository is private. Bjorn and overbait inherit admin access as
AOE-Garrison owners. On another computer, install GitHub CLI and run
`gh auth login` with an account that has access to this repository.
Never put tokens in TOML/JSON files or distribute them with mods.

In Garrison, open **Mods > Catalog > Source** and use:

```text
https://api.github.com/repos/AOE-Garrison/garrison-mod-catalog/contents/catalog.json?ref=main
```

Press **Sync**. The catalog changes only after an explicit sync; installing
or updating a mod is a separate action. Installed catalog mods are managed
on their Catalog cards and do not also appear in Local. The catalog does not
select the map or tuning pack in the game lobby.
