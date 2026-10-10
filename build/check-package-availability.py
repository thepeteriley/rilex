#!/usr/bin/env python3
"""Read the actual Debian amd64 indexes and check package-list names.

This is advisory research, not a replacement for APT's signature validation.
The ISO build always uses signed APT metadata and never trusts this script to
validate downloaded packages.
"""
from pathlib import Path
import lzma
import urllib.request

root = Path(__file__).resolve().parent.parent
available = {}
for suite, component in [('trixie', 'main'), ('trixie', 'contrib'),
                         ('trixie', 'non-free-firmware'), ('trixie-backports', 'main')]:
    url = f'https://deb.debian.org/debian/dists/{suite}/{component}/binary-amd64/Packages.xz'
    with urllib.request.urlopen(url, timeout=60) as response:
        data = lzma.decompress(response.read()).decode()
    for stanza in data.split('\n\n'):
        fields = {}
        for line in stanza.splitlines():
            if not line.startswith(' ') and ': ' in line:
                key, value = line.split(': ', 1)
                fields[key] = value
        if 'Package' in fields:
            available.setdefault(fields['Package'], {})[suite] = fields['Version']
missing = []
for line in (root / 'config/package-lists/rilex.list.chroot').read_text().splitlines():
    name = line.split('#', 1)[0].strip()
    if not name:
        continue
    if name not in available or 'trixie' not in available[name]:
        missing.append(name)
for name in ['hyprland', 'hyprlock', 'xdg-desktop-portal-hyprland']:
    print(f'{name}: {available.get(name, {})}')
if missing:
    raise SystemExit(f'Packages unavailable in stable: {missing}')
print('All baseline package names exist in official Debian stable indexes.')
