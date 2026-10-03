"""Build a curated catalog.json from the mod releases a catalog repository lists.

``catalog.config.json`` names the repository and, under ``mods``, each mod's id
and the version to list. That version's GitHub release is ``<id>-v<version>``
with the asset ``<id>-<version>.zip``, the package Garrison writes. Everything
the catalog says about a mod comes from that ZIP's ``garrison.json``: its
details, its archives' roles and its cover, which is copied to
``covers/<sha256>.<ext>`` beside catalog.json so the index can link it.

The build is incremental. An entry is reused unchanged when the previous
catalog.json lists the same release asset (address and size) and GitHub's
asset digest still equals the package hash it recorded. Otherwise the ZIP is
downloaded once to a temporary folder, hashed and verified; nothing from a mod
is executed. Mods no longer listed are dropped. Stdlib only, so the catalog
repository can run it as it is.
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
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile

MAX_ZIP = 2 * 1024**3 - 1
MAX_EXTRACTED = 4 * 1024**3
COVER_BYTES = 4 * 1024**2
CONFIG_NAME = 'catalog.config.json'
MANIFEST_NAME = 'garrison.json'
MANIFEST_SCHEMA = 'garrison.mod/v1'
CATALOG_SCHEMA = 'garrison.catalog/v1'
COVERS = 'covers'
COVER_SUFFIXES = ('.png', '.jpg', '.jpeg', '.webp')
VERSION = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?'


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def release_tag(mod_id: str, version: str) -> str:
    return f'{mod_id}-v{version}'


def package_name(mod_id: str, version: str) -> str:
    return f'{mod_id}-{version}.zip'


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


def inspect_package(path: Path) -> tuple[dict, list[str], tuple[str, bytes] | None]:
    """Validate a mod ZIP without extracting it.

    Returns the details of its ``garrison.json``, the sorted roles of its
    archives, and its cover as ``(suffix, bytes)`` or ``None``. Every archive's
    hash is checked against the manifest.
    """
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
            if name.name.casefold() == MANIFEST_NAME and not info.is_dir():
                manifests.append(info)
        if len(manifests) != 1:
            raise ValueError(f'ZIP must contain exactly one {MANIFEST_NAME}')
        if manifests[0].file_size > 65536:
            raise ValueError('The mod manifest is too large')
        manifest = json.loads(archive.read(manifests[0]))
        if (not isinstance(manifest, dict) or set(manifest) != {'schema', 'bundle_key', 'members', 'details'}
                or manifest['schema'] != MANIFEST_SCHEMA):
            raise ValueError(f'Unsupported mod manifest: package the mod again with Garrison ({MANIFEST_SCHEMA})')
        key = manifest['bundle_key']
        validate_key(key)
        details = manifest['details']
        validate_details(details)
        if details['id'] != key:
            raise ValueError('details.id must equal the bundle key')
        root = PurePosixPath(manifests[0].filename).parent
        keys = set()
        roles = []
        if not manifest['members']:
            raise ValueError('The mod names no archive')
        for member in manifest['members']:
            if set(member) != {'mod_key', 'role', 'path', 'sha256'}:
                raise ValueError('Unsupported archive entry')
            validate_key(member['mod_key'])
            if member['mod_key'].casefold() in keys:
                raise ValueError('Duplicate archive key')
            keys.add(member['mod_key'].casefold())
            if member['role'] not in ('map', 'tuning'):
                raise ValueError('Unsupported content role')
            roles.append(member['role'])
            relative = safe_name(member['path'])
            if relative.suffix.lower() != '.sga':
                raise ValueError('An archive must be an SGA')
            info = names.get(str(root / relative).casefold())
            if info is None or info.is_dir():
                raise ValueError('Missing archive')
            with archive.open(info) as stream:
                actual = hashlib.file_digest(stream, 'sha256').hexdigest()
            if actual != member['sha256']:
                raise ValueError('Archive hash mismatch')
        if roles.count('map') > 1:
            raise ValueError('A mod can contain at most one map')
        cover = None
        if 'cover' in details:
            info = names.get(str(root / details['cover']).casefold())
            if info is None or info.is_dir():
                raise ValueError(f'The cover {details["cover"]} is not beside {MANIFEST_NAME}')
            if not 0 < info.file_size <= COVER_BYTES:
                raise ValueError('The cover is empty or exceeds 4 MiB')
            cover = (PurePosixPath(details['cover']).suffix.lower(), archive.read(info))
        return details, sorted(set(roles)), cover


def validate_key(value: str) -> None:
    """The library key rule, for catalog ids, bundle keys and member keys.

    A copy of Garrison's one rule (``garrison_wire::check_library_key``), kept
    here so this tool runs on its own; ``tests/fixtures/library_key_vectors.json``
    holds both to the same cases. Every character it admits is URL-safe, so an
    id stands in ``garrison://install/<id>`` as it is.
    """
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', value) or value.lower() == 'groups':
        raise ValueError('Invalid mod key')


def validate_version(value: str, field: str = 'version') -> None:
    if not isinstance(value, str) or len(value) > 40 or not re.fullmatch(VERSION, value):
        raise ValueError(f'{field} must be a semantic version without a build suffix')
    if '-' in value and any(p.isdigit() and len(p) > 1 and p[0] == '0' for p in value.split('-', 1)[1].split('.')):
        raise ValueError('Numeric prerelease components cannot have leading zeros')


def version_order(value: str) -> tuple:
    """Semantic version precedence, for refusing a rollback the client would refuse."""
    core, _, prerelease = value.partition('-')
    numbers = tuple(int(part) for part in core.split('.'))
    if not prerelease:
        return numbers, (1,)
    parts = tuple((0, int(p), '') if p.isdigit() else (1, 0, p) for p in prerelease.split('.'))
    return numbers, (0, parts)


def validate_details(details: dict) -> None:
    """The client's ``ModDetails`` rules, as ``src/core/mod_bundle.check_details`` writes them."""
    if not isinstance(details, dict):
        raise ValueError('Mod details must be an object')
    required = {'id', 'name', 'version', 'summary', 'updated', 'min_garrison'}
    if not required <= details.keys() or details.keys() - (required | {'description', 'author', 'changelog',
                                                                       'content_types', 'cover'}):
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
        if (not isinstance(value, str) or len(value) > limit
                or any(ord(c) < 32 and c not in '\n\t' or 0x7F <= ord(c) < 0xA0 for c in value)):
            raise ValueError(f'Invalid {key}')
        if key in ('name', 'summary') and not value.strip():
            raise ValueError(f'Missing {key}')
    for key in ('version', 'min_garrison'):
        validate_version(details[key], key)
    try:
        dated = dt.date.fromisoformat(details['updated']).isoformat() == details['updated']
    except (TypeError, ValueError):
        dated = False
    if not dated:
        raise ValueError('updated must be YYYY-MM-DD')
    if 'cover' in details:
        cover = details['cover']
        if (not isinstance(cover, str) or len(cover) > 64 or '/' in cover or cover.startswith('.')
                or PurePosixPath(cover).suffix.lower() not in COVER_SUFFIXES):
            raise ValueError('cover must name a PNG, JPEG or WebP file beside garrison.json')
        safe_name(cover)


def read_config(root: Path) -> dict:
    """``catalog.config.json``: the repository and the version of each listed mod."""
    data = json.loads((root / CONFIG_NAME).read_text(encoding='utf-8-sig'))
    if not isinstance(data, dict) or set(data) - {'repository', 'private', 'source', 'mods'}:
        raise ValueError(f'{CONFIG_NAME} takes repository, private, source and mods')
    if not isinstance(data.get('repository'), str) or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',
                                                                       data['repository']):
        raise ValueError('repository must be ORG/REPO')
    if not isinstance(data.get('private', False), bool):
        raise ValueError('private must be true or false')
    mods = data.get('mods')
    if not isinstance(mods, dict):
        raise ValueError('mods must map each mod id to the version to list')
    if len(mods) > 500:
        raise ValueError('Catalog supports at most 500 entries')
    folded = set()
    for mod_id, version in mods.items():
        validate_key(mod_id)
        validate_version(version)
        if mod_id.casefold() in folded:
            raise ValueError('Duplicate catalog ID')
        folded.add(mod_id.casefold())
    return data


class GitHub:
    """Release lookups and downloads; tests stand in a fake."""

    def __init__(self, repository: str, private: bool) -> None:
        self.repository = repository
        self.private = private

    def release(self, tag: str) -> dict:
        url = f'https://api.github.com/repos/{self.repository}/releases/tags/{urllib.parse.quote(tag, safe="")}'
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Garrison-catalog-builder'}
        token = os.environ.get('GH_TOKEN')
        if token:
            headers['Authorization'] = f'Bearer {token}'
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
            data = response.read(2 * 1024**2 + 1)
        if len(data) > 2 * 1024**2:
            raise ValueError('Release metadata too large')
        return json.loads(data)

    def download(self, asset: dict, url: str, destination: Path) -> int:
        if self.private:
            # gh handles authentication and strips credentials on storage redirects.
            with destination.open('xb') as stream:
                subprocess.run(['gh', 'api', url, '-H', 'Accept: application/octet-stream'],
                               stdout=stream, stderr=subprocess.PIPE, check=True, timeout=300)
            return destination.stat().st_size
        count = 0
        with urllib.request.urlopen(url, timeout=60) as response, destination.open('xb') as stream:
            while chunk := response.read(128 * 1024):
                count += len(chunk)
                if count > asset['size']:
                    raise ValueError('Release asset size changed')
                stream.write(chunk)
        return count


def _asset_url(github: GitHub, asset: dict) -> str:
    if github.private:
        if not isinstance(asset.get('id'), int) or asset['id'] <= 0:
            raise ValueError('Invalid GitHub asset ID')
        return f'https://api.github.com/repos/{github.repository}/releases/assets/{asset["id"]}'
    url = asset['browser_download_url']
    if not url.startswith(f'https://github.com/{github.repository}/releases/download/'):
        raise ValueError('Release asset is outside the catalog repository')
    return url


def _cover_url(github: GitHub, branch: str, name: str) -> str:
    path = f'{COVERS}/{name}'
    if github.private:
        return f'https://api.github.com/repos/{github.repository}/contents/{path}?ref={branch}'
    return f'https://raw.githubusercontent.com/{github.repository}/{branch}/{path}'


def _cover_file(root: Path, entry: dict) -> Path | None:
    """The repository copy of a previous entry's cover, if it is still intact."""
    cover = entry.get('cover')
    if not cover:
        return None
    name = PurePosixPath(urllib.parse.urlsplit(cover['url']).path).name
    path = root / COVERS / name
    if path.is_file() and path.stat().st_size == cover['size'] and sha256(path.read_bytes()) == cover['sha256']:
        return path
    return None


def _previous(output: Path) -> dict[str, dict]:
    try:
        data = json.loads(output.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict) or data.get('schema') != CATALOG_SCHEMA:
        return {}
    return {entry['details']['id'].casefold(): entry for entry in data.get('mods', [])}


def _note(message: str) -> None:
    print(message, file=sys.stderr)


def build(root: Path, output: Path, *, branch: str = 'main', github: GitHub | None = None) -> dict:
    """Write ``output`` (catalog.json) and ``covers/`` for the releases ``catalog.config.json`` lists."""
    config = read_config(root)
    github = github or GitHub(config['repository'], config.get('private', False))
    if not re.fullmatch(r'[A-Za-z0-9._/-]{1,100}', branch) or '..' in branch:
        raise ValueError('branch must be a plain branch name')
    previous = _previous(output)
    mods, keys, covers = [], set(), {}
    for mod_id, version in sorted(config['mods'].items(), key=lambda item: item[0].casefold()):
        tag, asset_name = release_tag(mod_id, version), package_name(mod_id, version)
        release = github.release(tag)
        if release.get('draft') or release.get('prerelease'):
            raise ValueError(f'{tag}: only published stable releases enter this catalog')
        assets = [a for a in release['assets'] if a['name'] == asset_name]
        if len(assets) != 1 or not 0 < assets[0]['size'] <= MAX_ZIP:
            raise ValueError(f'{tag}: missing or oversized release asset {asset_name}')
        asset = assets[0]
        url = _asset_url(github, asset)
        digest = asset.get('digest') or ''
        old = previous.get(mod_id.casefold())
        entry = None
        if old and old['package']['url'] == url and old['package']['size'] == asset['size'] \
                and old['details']['id'] == mod_id and old['details']['version'] == version:
            if not digest.startswith('sha256:'):
                _note(f'{tag}: GitHub gives no digest for {asset_name}; downloading it to check it')
            elif digest != 'sha256:' + old['package']['sha256']:
                _note(f'WARNING {tag}: {asset_name} was replaced after it was published '
                      f'({digest} instead of sha256:{old["package"]["sha256"]}). Releases must not change; '
                      'publish a new version instead. Downloading it again.')
            elif old.get('cover') and _cover_file(root, old) is None:
                _note(f'{tag}: its cover is missing from {COVERS}/; downloading the release again')
            else:
                entry = old
        if entry is None:
            entry = _download_entry(root, github, branch, mod_id, version, asset, url, digest, covers)
        if old:
            if version_order(version) < version_order(old['details']['version']):
                raise ValueError(f'{mod_id}: {version} is older than the listed {old["details"]["version"]}; '
                                 'Garrison refuses a catalog that rolls a mod back')
            if version == old['details']['version'] and entry['package']['sha256'] != old['package']['sha256']:
                raise ValueError(f'{mod_id} {version}: the package changed without a new version')
        if entry['bundle_key'].casefold() in keys:
            raise ValueError('Duplicate bundle key')
        keys.add(entry['bundle_key'].casefold())
        if entry.get('cover'):
            covers[PurePosixPath(urllib.parse.urlsplit(entry['cover']['url']).path).name] = True
        mods.append(entry)
    result = {'schema': CATALOG_SCHEMA, 'mods': mods}
    encoded = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if len(encoded) > 2 * 1024**2:
        raise ValueError('Catalog exceeds 2 MiB')
    # Covers first, then the index; a failure above keeps the last published index.
    # covers/ always exists, so the workflow can stage it even when empty.
    folder = root / COVERS
    folder.mkdir(exist_ok=True)
    for stale in folder.iterdir():
        if stale.is_file() and stale.name not in covers:
            stale.unlink()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(encoded)
    try:
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return result


def _download_entry(root: Path, github: GitHub, branch: str, mod_id: str, version: str, asset: dict, url: str,
                    digest: str, covers: dict) -> dict:
    tag = release_tag(mod_id, version)
    with tempfile.TemporaryDirectory(prefix='garrison-catalog-') as temp:
        package = Path(temp) / 'mod.zip'
        count = github.download(asset, url, package)
        if count != asset['size']:
            raise ValueError(f'{tag}: incomplete release asset')
        with package.open('rb') as stream:
            package_sha = hashlib.file_digest(stream, 'sha256').hexdigest()
        if digest.startswith('sha256:') and digest != 'sha256:' + package_sha:
            raise ValueError(f'{tag}: the download does not match GitHub\'s digest {digest}')
        details, roles, cover = inspect_package(package)
    if details['id'] != mod_id or details['version'] != version:
        raise ValueError(f'{tag}: its {MANIFEST_NAME} is {details["id"]} {details["version"]}')
    listed = {key: value for key, value in details.items() if key != 'cover'}
    entry = {'details': listed, 'bundle_key': mod_id, 'roles': roles,
             'package': {'url': url, 'sha256': package_sha, 'size': count}}
    if cover:
        suffix, content = cover
        name = sha256(content) + ('.jpg' if suffix == '.jpeg' else suffix)
        target = root / COVERS / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.is_file() or target.read_bytes() != content:
            target.write_bytes(content)
        covers[name] = True
        entry['cover'] = {'url': _cover_url(github, branch, name), 'sha256': sha256(content), 'size': len(content)}
    return entry


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, default=Path('catalog.json'))
    parser.add_argument('--branch', default='main', help='the branch catalog.json and covers/ are published on')
    args = parser.parse_args()
    build(args.root, args.output, branch=args.branch)
