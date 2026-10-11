#!/usr/bin/env python3
"""Run actual live QA checks using the ordinary desktop process environment.

Read over SSH stdin as root in the disposable live guest. No environment
values or credentials are printed. The check script is on the QA-only CD.
"""
import os
from pathlib import Path
import subprocess
if os.getuid()!=0 or not Path('/run/live/medium/live/filesystem.squashfs').is_file():
 raise SystemExit('Requires disposable live QA guest root')
pids=subprocess.check_output(['pgrep','-u','live','-x','foot']).decode().split()
if not pids:raise SystemExit('Ordinary live Foot session not found')
env=dict(x.split('=',1) for x in Path('/proc/'+pids[0]+'/environ').read_text().split('\0') if '=' in x)
for key in ['HYPRLAND_INSTANCE_SIGNATURE','XDG_RUNTIME_DIR','DBUS_SESSION_BUS_ADDRESS']:
 if not env.get(key):raise SystemExit('Desktop session missing required variable '+key)
subprocess.run(['runuser','-u','live','--','bash','/mnt/qa/check-live-session.sh'],env=env,check=True)
