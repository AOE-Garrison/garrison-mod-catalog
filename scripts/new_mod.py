"""Create a labelled authoring form: python scripts/new_mod.py my-mod --name 'My Mod'."""
import argparse
import datetime
import json
from pathlib import Path

from build_catalog import validate_key


def create(root: Path, mod_id: str, name: str, author: str = '') -> Path:
    validate_key(mod_id)
    template = root / 'templates/mod.toml'
    folder = root / 'mods' / mod_id
    text = template.read_text(encoding='utf-8')
    replacements = {'release_tag': f'{mod_id}-v0.1.0', 'asset': f'{mod_id}-0.1.0.zip',
                    'id': mod_id, 'name': name, 'author': author,
                    'version': '0.1.0', 'updated': datetime.date.today().isoformat()}
    import re
    for field, value in replacements.items():
        text = re.sub(rf'(?m)^{field} = .*$', lambda _: f'{field} = ' + json.dumps(value, ensure_ascii=False), text)
    folder.mkdir(parents=True, exist_ok=False)
    (folder / 'mod.toml').write_text(text, encoding='utf-8')
    return folder


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('id')
    parser.add_argument('--name', required=True)
    parser.add_argument('--author', default='')
    args = parser.parse_args()
    print(create(Path(__file__).resolve().parents[1], args.id, args.name, args.author))
