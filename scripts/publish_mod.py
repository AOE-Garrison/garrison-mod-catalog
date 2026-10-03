"""Publish a mod ZIP Garrison packaged as a new release, and list it in catalog.config.json.

python scripts/publish_mod.py path/to/<id>-<version>.zip

The ZIP is checked as the builder checks it; its garrison.json gives the id,
version and release notes. The release is ``<id>-v<version>`` with the asset
``<id>-<version>.zip``, created with the GitHub CLI and never overwritten.
Then ``mods.<id>`` in catalog.config.json is set to the version: commit and
push that change, and the catalog workflow adds the release to catalog.json.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

try:
    from .build_catalog import CONFIG_NAME, inspect_package, package_name, read_config, release_tag, version_order
except ImportError:
    from build_catalog import CONFIG_NAME, inspect_package, package_name, read_config, release_tag, version_order


def publish(root: Path, package: Path, *, run=subprocess.run) -> dict:
    """Create the release for ``package`` and list its version; returns the new config."""
    config = read_config(root)
    details, _roles, _cover = inspect_package(package)
    mod_id, version = details['id'], details['version']
    mods = dict(config['mods'])
    listed = next((key for key in mods if key.casefold() == mod_id.casefold()), None)
    if listed is not None:
        if listed != mod_id:
            raise ValueError(f'The catalog lists this mod as {listed}; keep its id unchanged')
        if version_order(version) <= version_order(mods[listed]):
            raise ValueError(f'{mod_id} {mods[listed]} is listed; publish a newer version than that')
    tag, asset = release_tag(mod_id, version), package_name(mod_id, version)
    with tempfile.TemporaryDirectory(prefix='garrison-publish-') as temp:
        ready = Path(temp) / asset
        shutil.copyfile(package, ready)
        notes = Path(temp) / 'release-notes.md'
        notes.write_text('\n\n'.join(part for part in (details['summary'], details.get('description', ''),
                                                       details.get('changelog', '')) if part.strip()) + '\n',
                         encoding='utf-8')
        # No --clobber: an existing release or asset is never overwritten.
        run(['gh', 'release', 'create', tag, str(ready), '--repo', config['repository'],
             '--title', f"{details['name']} {version}", '--notes-file', str(notes)], check=True)
    mods[mod_id] = version
    config = {**config, 'mods': dict(sorted(mods.items(), key=lambda item: item[0].casefold()))}
    target = root / CONFIG_NAME
    temporary = target.with_name(target.name + '.tmp')
    temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temporary, target)
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('package', type=Path, help='the mod ZIP Garrison packaged')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    publish(args.root, args.package.resolve(strict=True))
    print(f'Listed in {CONFIG_NAME}. Commit and push it; the catalog workflow then builds catalog.json.')
