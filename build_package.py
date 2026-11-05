"""Freeze the prepared lab with hidden skills and verify every copied/archive hash."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
DEST = ROOT.parent / 'UPLOAD_THIS_FOLDER'
ARCHIVE = ROOT.parent / 'Lab19_GITHUB_READY.zip'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build():
    files = sorted(p for p in ROOT.rglob('*') if p.is_file()
                   and not any(part in {'__pycache__', '.venv', '.DS_Store'} for part in p.relative_to(ROOT).parts)
                   and p.suffix != '.pyc' and p.name != 'manifest.json')
    manifest = {}
    for source in files:
        relative = source.relative_to(ROOT)
        target = DEST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        manifest[str(relative)] = digest(source.read_bytes())
        assert digest(target.read_bytes()) == manifest[str(relative)]
    metadata = {'status': 'Prepared technical work; consult CHECKOUT.md for remaining floor/activity items.',
                'sha256': manifest}
    encoded = json.dumps(metadata, indent=2) + '\n'
    (ROOT / 'manifest.json').write_text(encoded)
    (DEST / 'manifest.json').write_text(encoded)
    with zipfile.ZipFile(ARCHIVE, 'w', zipfile.ZIP_DEFLATED) as archive:
        for relative in manifest:
            archive.write(DEST / relative, relative)
        archive.write(DEST / 'manifest.json', 'manifest.json')
    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(manifest) | {'manifest.json'}
        for relative, expected in manifest.items():
            assert digest(archive.read(relative)) == expected
    print(f'Verified {len(manifest)} files, hidden skills, copied hashes and ZIP integrity: {ARCHIVE.name}')


if __name__ == '__main__':
    build()
