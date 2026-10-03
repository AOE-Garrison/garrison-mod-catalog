# Add or update a mod

Use Python 3.11+ and an authenticated GitHub CLI account with repository write access. Players do not need these tools or an account.

Garrison's **Package for Garrison** creates `<id>-<version>.zip`. Its `garrison.json` contains the bundle key, archive member keys, roles, SHA-256 hashes, mod details and optional cover filename. `details.id` must equal the bundle key. Set the name, summary, author, date, description, changelog, content types and optional cover in the package workflow. Include concrete lobby selections in the description. Content labels do not select lobby settings.

```powershell
python scripts/publish_mod.py path/to/my-mod-1.0.0.zip
git add catalog.config.json
git commit -m "List My Mod 1.0.0"
git push origin main
```

The publisher creates a new release and updates the selected version. The workflow downloads each new package, verifies its complete manifest and archive hashes, copies the cover into `covers/` by content hash, and generates `catalog.json`. A failed validation preserves the prior index. Repeated builds reuse entries only when GitHub's asset digest, size and address still match.

For a local build after publishing:

```powershell
python scripts/build_catalog.py --branch main
```

Review and commit `catalog.json` and `covers/` together. Never edit hashes or sizes by hand. Keep ZIPs in Releases. Do not commit cooked archives, Blender scenes, vendor assets, credentials, local paths or generated diagnostics. Keep any required attribution and notices in the package.

## Existing releases

The October 2026 releases use the existing runtime bundle keys as their catalog IDs:

| Previous catalog ID | Current package and catalog ID | Version |
| --- | --- | --- |
| overfootball | football_45_bundle | 0.8.3 |
| modding-showcase | modding_showcase_full | 0.1.1 |
| ram-napkin-race | ram_napkin_race | 0.9.9 |

The previous IDs described catalog cards separately from runtime bundle keys. Current validation requires them to agree. The new index lists each runtime key once; it does not introduce aliases. Archive member keys and cooked archive contents remain unchanged. Previous GitHub releases remain available and immutable.

An older catalog entry may appear as a new catalog card after Sync because its catalog ID changed. Use the new card, and enable one installed copy of that bundle. The installed bundle key remains the same; no SGA key migration or recook is required. Automatic update continuity from the old catalog card ID is not promised.

Keep IDs and member keys stable for subsequent updates and use a new semantic version and release tag. Removing an ID from the catalog leaves installed copies on the player's computer.

The builder checks packaging and checksums. A successful build does not establish game visuals or multiplayer compatibility. Follow the release's launch instructions and use operator testing for runtime acceptance.
