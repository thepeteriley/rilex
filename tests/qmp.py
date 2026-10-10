#!/usr/bin/env python3
"""Small QMP driver for evidence capture and keyboard/mouse interaction."""
import argparse
import json
import pathlib
import socket
parser = argparse.ArgumentParser()
parser.add_argument('socket')
parser.add_argument('action', choices=['screenshot', 'key', 'click', 'status', 'quit'])
parser.add_argument('values', nargs='*')
a = parser.parse_args()
s = socket.socket(socket.AF_UNIX)
s.settimeout(10)
s.connect(a.socket)
f = s.makefile('rwb')
json.loads(f.readline())
def cmd(name, args=None):
    f.write((json.dumps({'execute': name, 'arguments': args or {}})+'\n').encode()); f.flush()
    while True:
        result = json.loads(f.readline())
        if 'error' in result: raise RuntimeError(result['error'])
        if 'return' in result: return result['return']
cmd('qmp_capabilities')
if a.action == 'screenshot':
    path = str(pathlib.Path(a.values[0]).resolve())
    cmd('screendump', {'filename': path, 'format': 'png'})
    print(path)
elif a.action == 'key':
    cmd('human-monitor-command', {'command-line': 'sendkey '+a.values[0]})
elif a.action == 'click':
    x, y, width, height = map(int, a.values)
    cmd('input-send-event', {'events': [
        {'type':'abs','data':{'axis':'x','value': int(x*32767/width)}},
        {'type':'abs','data':{'axis':'y','value': int(y*32767/height)}},
        {'type':'btn','data':{'button':'left','down':True}},
        {'type':'btn','data':{'button':'left','down':False}}]})
elif a.action == 'status': print(cmd('query-status'))
elif a.action == 'quit': cmd('quit')
