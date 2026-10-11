#!/usr/bin/env python3
"""Enter an ephemeral QA account field through QMP without logging its value.

Only for supervised SDDM/sudo password fields in disposable test VMs. This
never submits Return; screenshot review and submission are separate actions.
"""
import argparse
import json
import pathlib
import socket
import time
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('socket')
p.add_argument('credentials',type=pathlib.Path)
p.add_argument('--field',choices=['password','username'],default='password')
p.add_argument('--delay',type=float,default=.15)
a=p.parse_args()
if a.credentials.stat().st_mode & 0o077:
 p.error('QA credentials must be private mode0600')
value=json.loads(a.credentials.read_text())[a.field]
if not value or not all(c.isascii() and c.isalnum() for c in value):
 p.error('Only nonempty ASCII alphanumeric QA fields are supported')
if a.delay<0:p.error('delay must be nonnegative')
s=socket.socket(socket.AF_UNIX);s.settimeout(10);s.connect(a.socket)
f=s.makefile('rwb');json.loads(f.readline())
def cmd(name,args=None):
 f.write((json.dumps({'execute':name,'arguments':args or {}})+'\n').encode());f.flush()
 while True:
  r=json.loads(f.readline())
  if 'error' in r:raise RuntimeError(r['error'])
  if 'return' in r:return r['return']
cmd('qmp_capabilities')
for char in value:
 keys=(['shift'] if char.isupper() else [])+[char.lower()]
 cmd('input-send-event',{'events':[{'type':'key','data':{'down':down,'key':{'type':'qcode','data':key}}} for down,codes in [(True,keys),(False,keys[::-1])] for key in codes]})
 time.sleep(a.delay)
print('Entered private QA field; value withheld. Return not submitted.')
