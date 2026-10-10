#!/usr/bin/env python3
"""Validate source artifacts without claiming compositor or installation coverage."""
import json
import pathlib
import subprocess
import sys
import shutil
import xml.etree.ElementTree as ET
root = pathlib.Path(__file__).resolve().parents[1]
for pattern in ('build/*.sh', 'scripts/rilex-*', 'config/hooks/live/*.hook.chroot', 'packaging/rilex-defaults/DEBIAN/postinst'):
    for path in root.glob(pattern):
        subprocess.run(['bash', '-n', str(path)], check=True)
for path in root.glob('desktop/**/*.svg'):
    ET.parse(path)
json.loads((root / 'desktop/waybar/config').read_text())
subprocess.run([sys.executable, str(root / 'tests/test-installer.py')], check=True)
lua = shutil.which('lua5.4') or shutil.which('lua')
if lua:
    subprocess.run([lua, str(root / 'tests/check-bindings.lua')], cwd=root, check=True)
else:
    print('Lua runtime unavailable; binding schema check skipped.')
print('Source shell syntax, SVG XML, Waybar JSON and installer tests passed.')
