# Garrison 0.1.8 catalog release

The matching client and Blender extension 0.1.8 were published on October 29,
2026. The three packages below are separate GitHub release assets; their remote
SHA-256 digests match the reviewed inputs. Update Garrison and Sync Catalog to
install them. The procedure below applies to future updates too: never activate
nonexistent assets or bypass package validation with hand-written index entries.

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

These checksums identify the published release files. The updated feed has nine
projects; the legacy projection retains the original six for 0.1.7 readers.

| Proposed asset | SHA-256 |
| --- | --- |
| `persians_independent-0.1.0.zip` | `1dea196fb58b43a2c5d9d469e2e21201171ad95ef513709c9e424d3ce6af6282` |
| `vietnamese_independent-0.1.0.zip` | `fb20784415e4c59800978af766a8df077d9a458bffffb9d08701cb465f1eab6a` |
| `ui_colors-0.1.0.zip` | `d0db6b20925ae62766cfac63c67cea8f2753d3231cb1838b377c877d03ec3dfa` |

[Persians 0.1.0](https://github.com/AOE-Garrison/garrison-mod-catalog/releases/tag/persians_independent-v0.1.0) ·
[Vietnamese 0.1.0](https://github.com/AOE-Garrison/garrison-mod-catalog/releases/tag/vietnamese_independent-v0.1.0) ·
[In-game UI Colors 0.1.0](https://github.com/AOE-Garrison/garrison-mod-catalog/releases/tag/ui_colors-v0.1.0)

The separate English maintainer packet contains the handoff, card template,
the two extracted civilization declarations and release identities. The generic
authoring specification remains in the Blender extension's offline guide.
The same handoff ZIP is attached to both civilization releases.

The packaged 0.1.8 player was accepted with both civilizations and UI Colors
enabled together. The operator confirmed map startup, near-immediate saved
palette application and live color changes. The authors' model/texture and
unfinished gameplay work remains outside this integration release.
