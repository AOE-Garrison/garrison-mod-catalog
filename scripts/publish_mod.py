"""Publish a new immutable release from committed metadata and a local bundle ZIP."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

try:
    from .build_catalog import read_metadata, validate_key
    from .prepare_mod import prepare
except ImportError:
    from build_catalog import read_metadata, validate_key
    from prepare_mod import prepare


def publish(root: Path, mod_id: str, package: Path) -> None:
    validate_key(mod_id)
    config = json.loads((root / 'catalog.config.json').read_text())
    repository = config['repository']
    metadata = root / 'mods' / mod_id / 'mod.toml'
    data = read_metadata(metadata)
    if data['details']['id'] != mod_id:
        raise ValueError('Folder name must equal details.id')
    dirty = subprocess.check_output(['git', 'status', '--porcelain', '--', f'mods/{mod_id}'], cwd=root)
    if dirty.strip():
        raise ValueError('Commit and push the mod metadata and cover before publishing')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    remote = subprocess.check_output(['gh', 'api', f'repos/{repository}/commits/main', '--jq', '.sha'], text=True).strip()
    if head != remote:
        raise ValueError('Checkout must match published main before publishing a release')
    with tempfile.TemporaryDirectory(prefix='garrison-publish-') as temp:
        ready = Path(temp) / data['asset']
        if ready.parent != Path(temp) or ready.suffix.lower() != '.zip':
            raise ValueError('asset must be a ZIP filename without directories')
        prepare(metadata, package.resolve(strict=True), ready)
        notes = Path(temp) / 'release-notes.md'
        details = data['details']
        notes.write_text(details['summary'] + '\n\n' + details.get('description', '') + '\n', encoding='utf-8')
        # No --clobber: existing releases/assets must never be overwritten.
        subprocess.run(['gh', 'release', 'create', data['release_tag'], str(ready), '--repo', repository,
                        '--target', head, '--title', f"{details['name']} {details['version']}",
                        '--notes-file', str(notes)], check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('id')
    parser.add_argument('package', type=Path)
    args = parser.parse_args()
    publish(Path(__file__).resolve().parents[1], args.id, args.package)
