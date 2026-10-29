# Preparing the 0.1.8 catalog

Status: release preparation. Prepared local artifacts are not published assets.
Keep the active config on existing releases until each new ZIP has been reviewed
and uploaded through the publisher. Do not commit download URLs to nonexistent
releases or bypass package verification with hand-written entries.

| Project | Stable catalog ID | First release | Category |
| --- | --- | --- | --- |
| Persians | `persians_independent` | `0.1.0` | `civilizations` |
| Vietnamese | `vietnamese_independent` | `0.1.0` | `civilizations` |
| In-game UI Colors | `ui_colors` | `0.1.0` | `enhancements` |

1. Build and qualify the matching Garrison client and Blender extension 0.1.8.
2. Validate each ZIP using `scripts/build_catalog.py`'s `inspect_package`.
   Check exact source SGA hashes, immutable keys, minimum version, author,
   date, card cover and release notes. Preserve accepted game assets.
3. Include standalone player instructions and the maintainer handoff. Check
   that no private local paths, developer setup requirements or unsupported
   compatibility claims remain in distributed metadata.
4. Qualify the data-only UI Colors package with the renderer supplied by the
   matching player distribution. The old local renderer manifest is insufficient;
   the package must not carry executable sidecars. See [UI Colors](UI_COLORS.md).
5. Publish the compatible client, then publish each new mod with its category.
   Review and commit the resulting config; never overwrite a release asset.
6. Generate `catalog-v2.json` and the filtered `catalog.json` in the same build.
   The former serves 0.1.8; the latter remains parseable by 0.1.7. Commit covers
   with the indexes. An unchanged old client must still see its existing mods.
7. Check clean install, update from a locally imported candidate, enabled-state
   preservation and rollback through Garrison. Retain exact ZIP/SGA checksums.

The two civilization SGAs retain their accepted gameplay bytes. New outer
manifests use release versions and `min_garrison: 0.1.8`; that is not a new
gameplay acceptance claim. Known authored art defects remain with the authors.
Custom games with matching enabled mod versions on all peers are confirmed;
ranked and missing-mod negotiation are not part of this qualification.

## Reviewed package identities

These checksums identify prepared local files, not uploaded releases. A preview
containing the three new entries has nine projects; its legacy projection has
the original six. The active configuration still lists only published releases.

| Proposed asset | SHA-256 |
| --- | --- |
| `persians_independent-0.1.0.zip` | `1dea196fb58b43a2c5d9d469e2e21201171ad95ef513709c9e424d3ce6af6282` |
| `vietnamese_independent-0.1.0.zip` | `fb20784415e4c59800978af766a8df077d9a458bffffb9d08701cb465f1eab6a` |
| `ui_colors-0.1.0.zip` | `d0db6b20925ae62766cfac63c67cea8f2753d3231cb1838b377c877d03ec3dfa` |

The separate English maintainer packet contains the handoff, card template,
the two extracted civilization declarations and release identities. The generic
authoring specification remains in the Blender extension's offline guide.
