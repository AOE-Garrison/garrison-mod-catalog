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

This catalog and its release ZIPs are public. Only maintainers need repository
write access and GitHub authentication for the publishing commands above.
The main Garrison product repository remains private. Downloading Garrison
and accessing its source are separate from downloading mods.

Players open **Mods > Catalog > Sync**. The default catalog address is:

```text
https://raw.githubusercontent.com/AOE-Garrison/garrison-mod-catalog/main/catalog.json
```

No GitHub account, GitHub CLI, invitation or token is required. If an older
Garrison build uses another source, paste this address once under **Source**.
The successful address is remembered. Sync refreshes metadata and covers;
installing or updating a mod remains a separate action. The catalog does not
select the map or tuning pack in the game lobby.

Published package bytes and hashes are unchanged by the visibility switch.
The generated index uses direct release download URLs and commit-pinned public
cover URLs. Do not put credentials in any URL or catalog metadata.
