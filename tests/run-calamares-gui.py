#!/usr/bin/env python3
"""Experimental real GUI installation into an explicitly authorized QA QEMU disk.

SSH/bootstrap and fullscreen 1280x800 live desktop must already be ready.
Captures every page, checks successful Calamares log completion, then stops.
Independent boot/login must be performed separately before qualifying release.
"""
import argparse
import json
import os
from pathlib import Path
import secrets
import shlex
import string
import subprocess
import time

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--port',type=int,required=True)
p.add_argument('--key',type=Path,required=True)
p.add_argument('--known-hosts',type=Path,required=True)
p.add_argument('--qmp',type=Path,required=True)
p.add_argument('--evidence',type=Path,required=True)
p.add_argument('--credentials',type=Path,required=True)
p.add_argument('--confirm-disposable-vda',action='store_true',required=True)
p.add_argument('--install-timeout',type=int,default=1800,help='Maximum real installer observation time in seconds; emulated ARM hosts may need 3600.')
a=p.parse_args()
if not 60 <= a.install_timeout <= 7200:p.error('--install-timeout must be 60..7200 seconds')
a.evidence.mkdir(parents=True,exist_ok=True)
ssh=['ssh','-o','BatchMode=yes','-o',f'UserKnownHostsFile={a.known_hosts}','-i',str(a.key),'-p',str(a.port),'root@127.0.0.1']
base=Path(__file__).parent

def remote(command):
 return subprocess.run(ssh+[command],check=True,text=True,capture_output=True).stdout

def capture(name):
 subprocess.run(['python3',str(base/'qmp.py'),str(a.qmp),'screenshot',str(a.evidence/name)],check=True)

def input_action(action):
 args=['python3',str(base/'calamares-gui-input.py'),'--port',str(a.port),'--key',str(a.key),'--known-hosts',str(a.known_hosts),'--credentials',str(a.credentials),'--qmp',str(a.qmp),'--evidence',str(a.evidence),'--confirm-disposable-vda',action]
 subprocess.run(args,check=True)
 time.sleep(5)

# Guard before installing ephemeral QA-only input tooling or opening installer.
remote('set -eu; test -f /run/live/medium/live/filesystem.squashfs; '
       'case "$(cat /sys/class/dmi/id/product_name) $(cat /sys/class/dmi/id/sys_vendor)" in *QEMU*|*KVM*) ;; *) exit 80;; esac; '
       'test "$(lsblk -dn -o NAME,TYPE | awk \'$2=="disk" {print $1}\')" = vda; '
       'test "$(blockdev --getsize64 /dev/vda)" = 34359738368')
remote('apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y xdotool')
if a.credentials.exists():
 raise SystemExit('Refusing overwrite of existing QA credentials; provide a fresh private path.')
fd=os.open(a.credentials,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w') as f:
 json.dump({'name':'Rilex QA','username':'rilexqa','hostname':'rilex-qa','password':''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(24))},f)
# Preserve the ordinary live-user environment and invoke the actual shipped
# wrapper. This does not patch the ISO or replace Calamares jobs.
remote("python3 - <<'END'\nimport os,subprocess\npids=subprocess.check_output(['pgrep','-u','live','-x','foot']).decode().split()\nif not pids: raise SystemExit('Need ordinary live Foot environment')\nenv=dict(x.split('=',1) for x in open('/proc/'+pids[0]+'/environ').read().split('\\0') if '=' in x)\nlog=open('/tmp/rilex-qa-installer.log','w')\nsubprocess.Popen(['/usr/sbin/runuser','-u','live','--','rilex-install'],env=env,stdout=log,stderr=log,start_new_session=True)\nEND")
time.sleep(25)
# Hyprland sees actual QMP input rather than XWayland-only synthetic keys.
# Immediate down/up avoids emulation timer key repeats.
remote("DISPLAY=:0 xdotool keyup Super_L Super_R Alt_L Alt_R Control_L Control_R Shift_L Shift_R")
subprocess.run(['python3',str(base/'qmp.py'),'--explicit-key-events',str(a.qmp),'key','meta_l-f'],check=True)
time.sleep(5)
# Fixed Qt coordinates are permitted only after actual compositor geometry
# and focused fullscreen installer verification; otherwise stop before disk UI.
state=json.loads(remote("python3 - <<'END'\nimport json,subprocess\npid=subprocess.check_output(['pgrep','-u','live','-x','foot']).decode().split()[0]\nenv=dict(x.split('=',1) for x in open('/proc/'+pid+'/environ').read().split('\\0') if '=' in x)\ndef get(name): return json.loads(subprocess.check_output(['/usr/sbin/runuser','-u','live','--','hyprctl','-j',name],env=env))\nprint(json.dumps({'monitors':get('monitors'),'active':get('activewindow')}))\nEND"))
(a.evidence/'installer-geometry.json').write_text(json.dumps(state,indent=2))
active=state['active']
monitor=next((m for m in state['monitors'] if m.get('id')==active.get('monitor')),None)
if not monitor or (monitor.get('width'),monitor.get('height'),monitor.get('scale'),monitor.get('transform')) != (1280,800,1,0):
 capture('unsupported-installer-geometry.png');raise SystemExit('Installer coordinate assumptions do not match actual 1280x800 scale1 monitor')
if 'calamares' not in active.get('class','').lower() or not active.get('fullscreen'):
 capture('installer-not-focused-fullscreen.png');raise SystemExit('Actual active window is not fullscreen Calamares')
capture('wizard-01-welcome.png')
for name in ['location','keyboard','partition']:
 input_action('next');capture('wizard-'+name+'.png')
input_action('erase-selection');capture('wizard-erase.png')
input_action('next');capture('wizard-users.png')
input_action('account');capture('wizard-users-filled.png')
input_action('next');capture('wizard-summary.png')
input_action('confirm-install')
# Read actual job completion; GUI click exit status is not a test result.
for attempt in range((a.install_timeout+9)//10):
 time.sleep(10)
 log=remote('cat /root/.cache/calamares/session.log')
 (a.evidence/'installer.log').write_text(log)
 if 'completion: failed' in log or 'Installation failed' in log:
  capture('installer-failure.png');raise SystemExit('Installer error: inspect real log and screenshots')
 if 'completion: succeeded' in log:
  capture('installer-complete.png');break
else:
 capture('installer-timeout.png');raise SystemExit('No actual Calamares completion within configured timeout')
print('GUI installation jobs completed; independent disk boot/login/APT remain mandatory.')
