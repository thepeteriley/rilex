#!/usr/bin/env python3
"""Compare real .deb contents; reject Rilex ownership of vendor files.

Usage: test-package-ownership.py rilex-defaults.deb vendor1.deb [...]
Use actual Debian packages, e.g. foot, fuzzel, waybar, calamares-settings-debian.
Directories may be shared; files and symlinks may not.
"""
import subprocess
import sys
import tarfile
import io

def payload(package):
    archive = subprocess.check_output(['dpkg-deb', '--fsys-tarfile', package])
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as tree:
        return {member.name.removeprefix('./') for member in tree
                if member.isfile() or member.issym() or member.islnk()}

if len(sys.argv) < 3:
    raise SystemExit('Provide Rilex defaults .deb and at least one actual vendor .deb')
rilex = payload(sys.argv[1])
conflicts = []
for package in sys.argv[2:]:
    for path in sorted(rilex & payload(package)):
        conflicts.append(f'{package}: /{path}')
if conflicts:
    raise SystemExit('Conflicting package ownership:\n' + '\n'.join(conflicts))
print(f'No Rilex/vendor file ownership collisions across {len(sys.argv)-2} actual Debian packages.')
