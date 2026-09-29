"""Build a curated catalog from a separate repository's mods/*/mod.json.

Only published GitHub release assets are admitted. ZIPs are downloaded to a
temporary directory and verified; nothing from a mod is executed. Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import tomllib
import urllib.parse
import urllib.request
import zipfile

MAX_ZIP = 2 * 1024**3 - 1
MAX_EXTRACTED = 4 * 1024**3


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(name: str) -> PurePosixPath:
    parts = name.rstrip('/').split('/')
    if not name or len(name) > 240 or '\\' in name:
        raise ValueError('Unsafe ZIP path')
    for part in parts:
        stem = part.split('.')[0].upper()
        if (not part or part in ('.', '..') or part.endswith(('.', ' '))
                or any(ord(c) < 32 or c in '<>:"|?*' for c in part)
                or stem in ('CON', 'PRN', 'AUX', 'NUL')
                or re.fullmatch(r'(COM|LPT)[1-9¹²³]', stem)):
            raise ValueError('Unsafe ZIP path')
    return PurePosixPath(*parts)


def inspect_package(path: Path) -> tuple[str, list[str]]:
    """Validate the existing v1 manifest and every archive hash without extraction."""
    if path.stat().st_size > MAX_ZIP:
        raise ValueError('ZIP exceeds the supported size')
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) > 2048 or sum(i.file_size for i in infos) > MAX_EXTRACTED:
            raise ValueError('ZIP expands beyond the supported limits')
        names = {}
        manifests = []
        for info in infos:
            name = safe_name(info.filename)
            if str(name).casefold() in names:
                raise ValueError('ZIP contains duplicate paths')
            names[str(name).casefold()] = info
            mode = info.external_attr >> 16 & 0o170000
            if mode not in (0, 0o100000, 0o040000):
                raise ValueError('ZIP contains a link or special file')
            if name.name == 'mod.bundle.json' and not info.is_dir():
                manifests.append(info)
        if len(manifests) != 1:
            raise ValueError('ZIP must contain exactly one mod.bundle.json')
        if manifests[0].file_size > 65536:
            raise ValueError('Bundle manifest is too large')
        manifest = json.loads(archive.read(manifests[0]))
        if set(manifest) != {'schema', 'bundle_key', 'name', 'members'} or manifest['schema'] != 'garrison.mod-bundle/v1':
            raise ValueError('Unsupported bundle manifest')
        key = manifest['bundle_key']
        validate_key(key)
        if not isinstance(manifest['name'], str) or not manifest['name'].strip():
            raise ValueError('Missing bundle name')
        root = PurePosixPath(manifests[0].filename).parent
        keys = set()
        roles = []
        if not manifest['members']:
            raise ValueError('Empty bundle')
        for member in manifest['members']:
            if set(member) != {'mod_key', 'role', 'path', 'sha256'}:
                raise ValueError('Unsupported bundle member')
            validate_key(member['mod_key'])
            if member['mod_key'].casefold() in keys:
                raise ValueError('Duplicate member key')
            keys.add(member['mod_key'].casefold())
            if member['role'] not in ('map', 'tuning'):
                raise ValueError('Unsupported content role')
            roles.append(member['role'])
            relative = safe_name(member['path'])
            if relative.suffix.lower() != '.sga':
                raise ValueError('Member must be an SGA')
            info = names.get(str(root / relative).casefold())
            if info is None or info.is_dir():
                raise ValueError('Missing bundle member')
            with archive.open(info) as stream:
                actual = hashlib.file_digest(stream, 'sha256').hexdigest()
            if actual != member['sha256']:
                raise ValueError('Bundle member hash mismatch')
        if roles.count('map') > 1:
            raise ValueError('A bundle can contain at most one map')
        return key, sorted(set(roles))


def validate_key(value: str) -> None:
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', value) or value.lower() == 'groups':
        raise ValueError('Invalid mod key')


def validate_details(details: dict) -> None:
    required = {'id', 'name', 'version', 'summary', 'updated', 'min_garrison'}
    if not required <= details.keys() or details.keys() - (required | {'description', 'author', 'changelog', 'content_types'}):
        raise ValueError('Missing or unknown mod details')
    if 'content_types' in details:
        types = details['content_types']
        if (not isinstance(types, list) or len(types) > 3
                or any(t not in ('map', 'game-mode', 'tuning-pack') for t in types)
                or len(set(types)) != len(types)):
            raise ValueError('content_types must list distinct map, game-mode or tuning-pack components')
    validate_key(details['id'])
    for key, limit in [('name', 100), ('summary', 180), ('description', 8000), ('author', 100), ('changelog', 8000)]:
        value = details.get(key, '')
        if not isinstance(value, str) or len(value) > limit or any(ord(c) < 32 and c not in '\n\t' for c in value):
            raise ValueError(f'Invalid {key}')
        if key in ('name', 'summary') and not value.strip():
            raise ValueError(f'Missing {key}')
    version = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?'
    for key in ('version', 'min_garrison'):
        value = details[key]
        if len(value) > 40 or not re.fullmatch(version, value):
            raise ValueError(f'{key} must be a semantic version without a build suffix')
        if '-' in value and any(p.isdigit() and len(p) > 1 and p[0] == '0' for p in value.split('-', 1)[1].split('.')):
            raise ValueError('Numeric prerelease components cannot have leading zeros')
    if dt.date.fromisoformat(details['updated']).isoformat() != details['updated']:
        raise ValueError('updated must be YYYY-MM-DD')


def fetch_json(url: str) -> dict:
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Garrison-catalog-builder'}
    token = os.environ.get('GH_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
        data = response.read(2 * 1024**2 + 1)
    if len(data) > 2 * 1024**2:
        raise ValueError('Release metadata too large')
    return json.loads(data)


def read_metadata(path: Path) -> dict:
    """TOML is the editable author form; JSON remains supported."""
    data = (tomllib.loads(path.read_text(encoding='utf-8-sig')) if path.suffix == '.toml'
            else json.loads(path.read_text(encoding='utf-8-sig')))
    if set(data) - {'details', 'release_tag', 'asset', 'cover'}:
        raise ValueError('Unknown catalog authoring fields')
    validate_details(data['details'])
    return data


def build(root: Path, repository: str, ref: str, output: Path, *, private: bool = False) -> dict:
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
        raise ValueError('repository must be ORG/REPO')
    if not re.fullmatch(r'[0-9a-f]{40}', ref):
        raise ValueError('ref must be the full commit SHA containing the metadata and covers')
    mods = []
    ids, bundle_keys = set(), set()
    paths = sorted([*(root / 'mods').glob('*/mod.json'), *(root / 'mods').glob('*/mod.toml')])
    if len({p.parent for p in paths}) != len(paths):
        raise ValueError('Use one mod.toml or mod.json per mod, not both')
    for path in paths:
        data = read_metadata(path)
        details = data['details']
        validate_details(details)
        if details['id'].casefold() in ids:
            raise ValueError('Duplicate catalog ID')
        ids.add(details['id'].casefold())
        tag = urllib.parse.quote(data['release_tag'], safe='')
        release = fetch_json(f'https://api.github.com/repos/{repository}/releases/tags/{tag}')
        if release.get('draft') or release.get('prerelease'):
            raise ValueError('Only published stable releases enter this catalog')
        assets = [a for a in release['assets'] if a['name'] == data['asset']]
        if len(assets) != 1 or not 0 < assets[0]['size'] <= MAX_ZIP:
            raise ValueError('Missing or oversized release ZIP')
        asset = assets[0]
        url = asset['browser_download_url']
        if not url.startswith(f'https://github.com/{repository}/releases/download/'):
            raise ValueError('Release asset is outside the catalog repository')
        with tempfile.TemporaryDirectory(prefix='garrison-catalog-') as temp:
            package = Path(temp) / 'mod.zip'
            if private:
                if not isinstance(asset.get('id'), int) or asset['id'] <= 0:
                    raise ValueError('Invalid GitHub asset ID')
                url = f'https://api.github.com/repos/{repository}/releases/assets/{asset["id"]}'
                # gh handles authentication and strips credentials on storage redirects.
                with package.open('xb') as stream:
                    subprocess.run(['gh', 'api', url, '-H', 'Accept: application/octet-stream'],
                                   stdout=stream, stderr=subprocess.PIPE, check=True, timeout=300)
                count = package.stat().st_size
            else:
                with urllib.request.urlopen(url, timeout=60) as response, package.open('xb') as stream:
                    count = 0
                    while chunk := response.read(128 * 1024):
                        count += len(chunk)
                        if count > asset['size']:
                            raise ValueError('Release asset size changed')
                        stream.write(chunk)
            if count != asset['size']:
                raise ValueError('Incomplete release asset')
            key, roles = inspect_package(package)
            with package.open('rb') as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if key.casefold() in bundle_keys:
            raise ValueError('Duplicate bundle key')
        bundle_keys.add(key.casefold())
        entry = {'details': details, 'bundle_key': key, 'roles': roles,
                 'package': {'url': url, 'sha256': digest, 'size': count}}
        if data.get('cover'):
            relative = safe_name(data['cover'])
            cover = (path.parent / str(relative)).resolve(strict=True)
            if not cover.is_relative_to(root.resolve()) or cover.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp'):
                raise ValueError('Cover must be a repository PNG/JPEG/WebP')
            if not 0 < cover.stat().st_size <= 4 * 1024**2:
                raise ValueError('Cover is empty or exceeds 4 MiB')
            content = cover.read_bytes()
            url_path = urllib.parse.quote(cover.relative_to(root.resolve()).as_posix(), safe='/')
            cover_url = (f'https://api.github.com/repos/{repository}/contents/{url_path}?ref={ref}' if private
                         else f'https://raw.githubusercontent.com/{repository}/{ref}/{url_path}')
            entry['cover'] = {'url': cover_url,
                              'sha256': sha256(content), 'size': len(content)}
        mods.append(entry)
    if len(mods) > 500:
        raise ValueError('Catalog supports at most 500 entries')
    result = {'schema': 'garrison.catalog/v1', 'mods': mods}
    encoded = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if len(encoded) > 2 * 1024**2:
        raise ValueError('Catalog exceeds 2 MiB')
    # Preserve the last published index if any preceding validation fails.
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(encoded)
    try:
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--repository', required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--output', type=Path, default=Path('catalog.json'))
    parser.add_argument('--private', action='store_true', help='Use authenticated GitHub API URLs (GitHub CLI required)')
    args = parser.parse_args()
    build(args.root, args.repository, args.ref, args.output, private=args.private)
