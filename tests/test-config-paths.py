#!/usr/bin/env python3
"""Check default asset paths against a real package staging tree or .deb payload."""
import io
import pathlib
import re
import subprocess
import sys
import tarfile

artifact = pathlib.Path(sys.argv[1]) if len(sys.argv) == 2 else None
if artifact is None:
    raise SystemExit('Usage: test-config-paths.py STAGING_DIRECTORY_OR_DEB')
if artifact.is_dir():
    files = {str(path.relative_to(artifact)): path.read_bytes()
             for path in artifact.rglob('*') if path.is_file() and not path.is_symlink()}
else:
    archive = subprocess.check_output(['dpkg-deb', '--fsys-tarfile', str(artifact)])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tree:
        files = {member.name.removeprefix('./'): tree.extractfile(member).read()
                 for member in tree if member.isfile()}
checked = set()
for name, contents in files.items():
    if name.startswith('usr/bin/rilex-'):
        for reference in re.findall(r'/(?:etc/rilex|usr/share/rilex)/[A-Za-z0-9_./-]+', contents.decode()):
            # Existing directory references also count; require actual contained assets.
            key = reference.lstrip('/')
            if key not in files and not any(file.startswith(key+'/') for file in files):
                raise SystemExit(f'{name} references missing packaged asset: {reference}')
            checked.add(reference)
assert checked, 'No default paths were checked; not a Rilex package payload'
print(f'Validated {len(checked)} default asset paths in real Rilex package payload.')
