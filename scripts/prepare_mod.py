"""Add the same catalog metadata to a local mod ZIP, without altering its SGA files.

python scripts/prepare_mod.py mods/my-mod/mod.toml original.zip ready.zip
The output must not exist. The optional cover is copied beside the bundle manifest.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import shutil
import zipfile

try:
    from .build_catalog import inspect_package, read_metadata, safe_name
except ImportError:
    from build_catalog import inspect_package, read_metadata, safe_name


def prepare(metadata: Path, source: Path, output: Path) -> None:
    data = read_metadata(metadata)
    inspect_package(source)
    cover = None
    if data.get('cover'):
        relative = safe_name(data['cover'])
        cover = (metadata.parent / str(relative)).resolve(strict=True)
        if (not cover.is_relative_to(metadata.parent.resolve())
                or cover.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp')
                or not 0 < cover.stat().st_size <= 4 * 1024**2):
            raise ValueError('Cover must be a PNG/JPEG/WebP below the mod folder, up to 4 MiB')
    with zipfile.ZipFile(source) as src:
        manifest = next(i for i in src.infolist() if PurePosixPath(i.filename).name == 'mod.bundle.json')
        base = PurePosixPath(manifest.filename).parent
        sidecar = str(base / 'garrison.mod.json')
        cover_name = 'garrison-cover' + cover.suffix.lower() if cover else None
        cover_dest = str(base / cover_name) if cover_name else None
        with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as dst:
            for info in src.infolist():
                if info.filename.casefold() in {sidecar.casefold(), (cover_dest or '').casefold()}:
                    continue
                with src.open(info) as original, dst.open(info.filename, 'w') as copied:
                    shutil.copyfileobj(original, copied, 128 * 1024)
            record = {'schema': 'garrison.mod-details/v1', 'details': data['details']}
            if cover:
                record['cover'] = cover_name
                dst.write(cover, cover_dest)
            dst.writestr(sidecar, json.dumps(record, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('metadata', type=Path)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    prepare(args.metadata, args.source, args.output)
