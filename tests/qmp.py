#!/usr/bin/env python3
"""Small QMP driver for evidence capture and keyboard/mouse interaction."""
import argparse
import json
import pathlib
import socket
import time
parser = argparse.ArgumentParser()
parser.add_argument('socket')
parser.add_argument('action', choices=['screenshot', 'key', 'click', 'status', 'quit', 'type'])
parser.add_argument('values', nargs='*')
parser.add_argument('--typing-delay', type=float, default=0.12)
parser.add_argument('--key-hold', type=int, default=None)
parser.add_argument('--click-delay', type=float, default=0.2)
parser.add_argument('--explicit-key-events', action='store_true', help='Send immediate key press/release pairs, avoiding TCG virtual-clock release timers.')
a = parser.parse_args()
if a.key_hold is None: a.key_hold = 100 if a.action == "key" else 10
if a.typing_delay < 0 or a.click_delay < 0 or not 1 <= a.key_hold <= 1000:
    parser.error("Delays must be nonnegative and key hold must be 1..1000 ms.")
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
def send_key(key):
    if a.explicit_key_events:
        keys = key.split('-')
        events = [{'type': 'key', 'data': {'down': down, 'key': {'type': 'qcode', 'data': code}}}
                  for down, codes in ((True, keys), (False, list(reversed(keys))))
                  for code in codes]
        cmd('input-send-event', {'events': events})
    else:
        result = cmd('human-monitor-command', {'command-line': 'sendkey '+key+' '+str(a.key_hold)})
        if result: raise RuntimeError('HMP sendkey failed: '+result.strip())
if a.action == 'screenshot':
    path = str(pathlib.Path(a.values[0]).resolve())
    cmd('screendump', {'filename': path, 'format': 'png'})
    print(path)
elif a.action == 'key':
    send_key(a.values[0])
elif a.action == 'type':
    mapping = {' ': 'spc', '\n': 'ret', '-': 'minus', '_': 'shift-minus', '=': 'equal', '+': 'shift-equal', '/': 'slash', '?': 'shift-slash', '.': 'dot', '>': 'shift-dot', ',': 'comma', '<': 'shift-comma', ';': 'semicolon', ':': 'shift-semicolon', '\'': 'apostrophe', '"': 'shift-apostrophe', '[': 'bracket_left', ']': 'bracket_right', '{': 'shift-bracket_left', '}': 'shift-bracket_right', '\\': 'backslash', '|': 'shift-backslash', '`': 'grave_accent', '~': 'shift-grave_accent'}
    mapping.update(dict(zip('!@#$%^&*()', ['shift-'+x for x in '1234567890'])))
    value = ' '.join(a.values)
    for char in value:
        if char.isascii() and char.isalnum(): key = ('shift-' if char.isupper() else '')+char.lower()
        elif char in mapping: key = mapping[char]
        else: raise ValueError('Unsupported US keyboard character: '+repr(char))
        send_key(key)
        time.sleep(a.typing_delay)
elif a.action == 'click':
    x, y, width, height = map(int, a.values)
    cmd('input-send-event', {'events': [
        {'type':'abs','data':{'axis':'x','value': int(x*32767/width)}},
        {'type':'abs','data':{'axis':'y','value': int(y*32767/height)}}]})
    time.sleep(a.click_delay)
    cmd('input-send-event', {'events': [{'type':'btn','data':{'button':'left','down':True}}]})
    time.sleep(a.click_delay)
    cmd('input-send-event', {'events': [{'type':'btn','data':{'button':'left','down':False}}]})
elif a.action == 'status': print(cmd('query-status'))
elif a.action == 'quit': cmd('quit')
