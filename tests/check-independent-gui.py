#!/usr/bin/env python3
"""Experimental independent disk boot, normal SDDM login and installed checks.

Requires a running disposable VM with no inserted removable/CD media, its
private generated account JSON, and the host QEMU serial-log path. Passwords
never enter argv/logs. Actual guest checks must emit a success marker.
"""
import argparse
import json
from pathlib import Path
import socket
import subprocess
import time
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--qmp',type=Path,required=True)
p.add_argument('--credentials',type=Path,required=True)
p.add_argument('--evidence',type=Path,required=True)
p.add_argument('--serial',type=Path,required=True)
p.add_argument('--boot-wait',type=int,default=180)
a=p.parse_args();base=Path(__file__).parent
a.evidence.mkdir(parents=True,exist_ok=True)
s=socket.socket(socket.AF_UNIX);s.settimeout(10);s.connect(str(a.qmp));f=s.makefile('rwb');json.loads(f.readline())
def command(name,args=None):
 f.write((json.dumps({'execute':name,'arguments':args or {}})+'\n').encode());f.flush()
 while True:
  r=json.loads(f.readline())
  if 'error' in r:raise RuntimeError(r['error'])
  if 'return' in r:return r['return']
command('qmp_capabilities')
blocks=command('query-block')
(a.evidence/'independent-block-devices.json').write_text(json.dumps(blocks,indent=2))
if any(b.get('removable') and b.get('inserted') for b in blocks):
 raise SystemExit('Refusing claim of independent boot with inserted removable media')
if not any(b.get('inserted',{}).get('drv')=='qcow2' for b in blocks):
 raise SystemExit('Disposable qcow2 system disk missing')
def qmp(action,*values):
 subprocess.run(['python3',str(base/'qmp.py'),'--explicit-key-events',str(a.qmp),action,*map(str,values)],check=True)
def screenshot(name):qmp('screenshot',a.evidence/name)
def password():
 subprocess.run(['python3',str(base/'qa-private-keyboard.py'),str(a.qmp),str(a.credentials)],check=True)
time.sleep(a.boot_wait)
screenshot('independent-sddm.png')
# Fresh single created-user SDDM greeter focuses its password field.
password();qmp('key','ret');time.sleep(40)
screenshot('independent-normal-user-desktop.png')
qmp('key','meta_l-ret');time.sleep(8)
qmp('type','sudo -v');qmp('key','ret');time.sleep(3)
password();qmp('key','ret');time.sleep(3)
# Run in the normal created user's graphical terminal. Environment/session
# checks catch failed login instead of treating keyboard API success as proof.
check="( set -e; test $(id -u) -ne 0; test $(id -un) = rilexqa; test ! -d /run/live/medium; grep -qx ID=rilex /etc/os-release; test -s /boot/grub/grub.cfg; hyprctl version; pgrep -u $(id -u) -x waybar; pgrep -u $(id -u) -x foot; systemctl is-active NetworkManager; systemctl --user is-active pipewire wireplumber; systemctl --user is-active xdg-desktop-portal-hyprland; sudo apt-get update; printf '\\nRILEX_INSTALLED_CHECK_PASS\\n'; ) 2>&1 | sudo tee /dev/ttyS0"
qmp('type',check);qmp('key','ret')
for attempt in range(90):
 time.sleep(5)
 serial=a.serial.read_text(errors='replace') if a.serial.exists() else ''
 if '\nRILEX_INSTALLED_CHECK_PASS\r' in serial or '\nRILEX_INSTALLED_CHECK_PASS\n' in serial:
  screenshot('independent-checks-passed.png')
  (a.evidence/'independent-result.txt').write_text('PASS actual normal graphical login, Hyprland, Waybar, Foot, networking/audio/portal and APT refresh with no CD media attached.\n')
  print('PASS actual independent installed-system checks');break
else:
 screenshot('independent-checks-failed.png')
 raise SystemExit('Installed guest emitted no success marker; inspect serial log and screenshots')
