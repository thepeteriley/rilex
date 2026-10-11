#!/usr/bin/python3
"""Keep a real XDG FileChooser request alive until user selection/cancellation."""
import json
import sys
import uuid
from gi.repository import Gio, GLib
bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
token = 'rilexqa_' + uuid.uuid4().hex
sender = bus.get_unique_name()[1:].replace('.', '_')
path = '/org/freedesktop/portal/desktop/request/' + sender + '/' + token
loop = GLib.MainLoop()
result = {}
def response(connection, sender, path, interface, signal, parameters, data):
    code, fields = parameters.unpack()
    result.update(response=code, results=fields)
    print(json.dumps(result), flush=True)
    loop.quit()
bus.signal_subscribe('org.freedesktop.portal.Desktop',
                     'org.freedesktop.portal.Request', 'Response', path, None,
                     Gio.DBusSignalFlags.NONE, response, None)
reply = bus.call_sync('org.freedesktop.portal.Desktop',
                      '/org/freedesktop/portal/desktop',
                      'org.freedesktop.portal.FileChooser', 'OpenFile',
                      GLib.Variant('(ssa{sv})', ('', 'Rilex QA file selection', {
                          'handle_token': GLib.Variant('s', token),
                          'multiple': GLib.Variant('b', False),
                      })), GLib.VariantType.new('(o)'),
                      Gio.DBusCallFlags.NONE, 30000, None).unpack()[0]
if reply != path:
    raise RuntimeError('Unexpected request handle')
print(json.dumps({'request': reply}), flush=True)
def timeout():
    result['timeout'] = True
    loop.quit()
    return GLib.SOURCE_REMOVE
GLib.timeout_add_seconds(180, timeout)
loop.run()
if result.get('timeout'):
    print('FileChooser response timed out', file=sys.stderr)
    sys.exit(1)
# Cancellation is recorded as cancellation, never as file-selection success.
sys.exit(0 if result.get('response') in (0, 1) else 1)
