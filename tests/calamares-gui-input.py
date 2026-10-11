#!/usr/bin/env python3
"""Staged QA input for Calamares in a disposable QEMU guest.

Requires QA-only xdotool installed in the live guest. Never launches Calamares,
partitions a disk directly. Confirmation needs explicit disposable-disk authorization.
Screenshot/review each page using qmp.py before moving on; confirmation captures evidence. Coordinates assume
Calamares is fullscreen at 1280x800, US keyboard and its English wizard.
"""
import argparse
import json
from pathlib import Path
import shlex
import subprocess

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--port', type=int, required=True)
p.add_argument('--key', type=Path, required=True)
p.add_argument('--known-hosts', type=Path, required=True)
p.add_argument('--credentials', type=Path)
p.add_argument('action', choices=['next', 'erase-selection', 'account', 'clear-modifiers', 'confirm-install'])
p.add_argument('--confirm-disposable-vda', action='store_true', help='Explicitly authorize only the guarded 32 GiB disposable QEMU disk GUI confirmation.')
p.add_argument('--qmp', type=Path, help='QMP socket for mandatory confirmation screenshots')
p.add_argument('--evidence', type=Path, help='Ignored evidence directory')
a = p.parse_args()
ssh = ['ssh', '-o', 'BatchMode=yes', '-o', f'UserKnownHostsFile={a.known_hosts}',
       '-i', str(a.key), '-p', str(a.port), 'root@127.0.0.1']
# Check the actual guest before any GUI action. The only disk must be our
# explicit 32 GiB virtual device; mounted live media is mandatory.
guard = r'''set -eu
case "$(cat /sys/class/dmi/id/product_name) $(cat /sys/class/dmi/id/sys_vendor)" in *QEMU*|*KVM*) ;; *) exit 80;; esac
findmnt -rn /run/live/medium >/dev/null
[ "$(lsblk -dn -o NAME,TYPE | awk '$2=="disk" {print $1}')" = vda ]
[ "$(blockdev --getsize64 /dev/vda)" = 34359738368 ]
command -v xdotool >/dev/null
pgrep -x calamares >/dev/null
'''
subprocess.run(ssh + ['sh -s'], input=guard, text=True, check=True)

def run(script, data=None):
    subprocess.run(ssh + ['env DISPLAY=:0 sh -c ' + shlex.quote(script)],
                   input=data, text=True, check=True)

def click(x, y):
    run(f'xdotool mousemove {x} {y} sleep 1 click --clearmodifiers 1')

run('xdotool keyup Super_L Super_R Alt_L Alt_R Control_L Control_R Shift_L Shift_R')
if a.action == 'next':
    click(1134, 780)
elif a.action == 'erase-selection':
    click(206, 70)
    print('Selected erase; inspect disk identity and partition summary before continuing.')
elif a.action == 'account':
    if not a.credentials:
        p.error('--credentials is required for account entry')
    if a.credentials.stat().st_mode & 0o077:
        p.error('credentials must have mode 0600')
    values = json.loads(a.credentials.read_text())
    for key, x, y in [('name',300,50),('username',300,110),('hostname',300,170),
                      ('password',300,230),('password',500,230)]:
        click(x,y)
        run('xdotool key --clearmodifiers ctrl+a')
        # The random QA credential goes over SSH stdin, never argv or logs.
        run('xdotool type --clearmodifiers --delay 200 --file -', values[key])
    print('Entered private QA account fields; inspect them and keep autologin disabled.')

elif a.action == 'confirm-install':
    if not (a.confirm_disposable_vda and a.qmp and a.evidence):
        p.error('confirmation requires --confirm-disposable-vda --qmp --evidence')
    a.evidence.mkdir(parents=True, exist_ok=True)
    qmp = Path(__file__).with_name('qmp.py')
    def capture(name):
        subprocess.run(['python3', str(qmp), str(a.qmp), 'screenshot',
                        str(a.evidence / name)], check=True)
    capture('install-summary-before-confirmation.png')
    click(1134,780)
    import time
    time.sleep(3)
    capture('install-destructive-modal.png')
    # Actual reviewed Calamares English modal: Install Now. This action is
    # explicitly gated and never implemented as direct partition commands.
    click(735,392)
    time.sleep(3)
    capture('install-progress-start.png')
