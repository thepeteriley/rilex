#!/usr/bin/python3
"""Interactive disposable-guest ScreenCast handshake; does not sample frames.

Requires python3-gi and an ordinary logged-in desktop user's session bus.
API: https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html
The user must approve the actual provider's source-selection dialog.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from gi.repository import Gio, GLib

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--timeout', type=int, default=180)
p.add_argument('--sample-frames', action='store_true',
               help='Require five actual video buffers through QA-only GStreamer')
a = p.parse_args()
bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
service = 'org.freedesktop.portal.Desktop'
path = '/org/freedesktop/portal/desktop'
interface = 'org.freedesktop.portal.ScreenCast'
session = None
remote_fd = None


def log(event, **fields):
    print(json.dumps({'event': event, **fields}), flush=True)


def request(method, signature, values, options):
    token = 'rilexqa_' + uuid.uuid4().hex
    options = {**options, 'handle_token': GLib.Variant('s', token)}
    sender = bus.get_unique_name()[1:].replace('.', '_')
    request_path = '/org/freedesktop/portal/desktop/request/' + sender + '/' + token
    result = {}
    loop = GLib.MainLoop()

    def response(connection, sender_name, object_path, iface, signal, parameters, data):
        code, fields = parameters.unpack()
        result.update(code=code, fields=fields)
        loop.quit()

    subscription = bus.signal_subscribe(service, 'org.freedesktop.portal.Request',
                                        'Response', request_path, None,
                                        Gio.DBusSignalFlags.NONE, response, None)

    def timeout():
        result['timeout'] = True
        loop.quit()
        return GLib.SOURCE_REMOVE

    timer = GLib.timeout_add_seconds(a.timeout, timeout)
    try:
        returned = bus.call_sync(service, path, interface, method,
                                 GLib.Variant(signature, (*values, options)),
                                 GLib.VariantType.new('(o)'),
                                 Gio.DBusCallFlags.NONE, 30000, None).unpack()[0]
        if returned != request_path:
            raise RuntimeError(f'{method}: unexpected request path {returned}')
        log('request', method=method, handle=returned)
        loop.run()
        if result.get('timeout'):
            bus.call_sync(service, returned, 'org.freedesktop.portal.Request', 'Close',
                          None, None, Gio.DBusCallFlags.NONE, 5000, None)
            raise TimeoutError(f'{method}: no response within {a.timeout}s')
        log('response', method=method, response=result['code'], results=result['fields'])
        if result['code'] != 0:
            raise RuntimeError(f'{method}: portal cancelled or failed ({result["code"]})')
        return result['fields']
    finally:
        bus.signal_unsubscribe(subscription)
        if not result.get('timeout'):
            GLib.source_remove(timer)


try:
    session = request('CreateSession', '(a{sv})', (), {
        'session_handle_token': GLib.Variant('s', 'rilexsession_' + uuid.uuid4().hex),
    })['session_handle']
    request('SelectSources', '(oa{sv})', (session,), {
        'types': GLib.Variant('u', 1),
        'multiple': GLib.Variant('b', False),
    })
    start = request('Start', '(osa{sv})', (session, ''), {})
    streams = start.get('streams', [])
    if not streams or not all(isinstance(x[0], int) and x[0] > 0 for x in streams):
        raise RuntimeError('Start returned no valid PipeWire stream node')
    reply, fd_list = bus.call_with_unix_fd_list_sync(
        service, path, interface, 'OpenPipeWireRemote',
        GLib.Variant('(oa{sv})', (session, {})), GLib.VariantType.new('(h)'),
        Gio.DBusCallFlags.NONE, 30000, None, None)
    remote_fd = fd_list.get(reply.unpack()[0])
    info = os.fstat(remote_fd)
    log('pipewire_remote', fd_open=True, fd_mode=info.st_mode, streams=streams)
    log('RILEX_SCREENCAST_HANDSHAKE_PASS', sampled_video_frames=False)
    if a.sample_frames:
        inspect = subprocess.run(['gst-inspect-1.0', 'pipewiresrc'],
                                 text=True, capture_output=True, check=True)
        print(inspect.stdout, flush=True)
        if not all(re.search(r'^\s*' + prop + r'\s*:', inspect.stdout, re.M)
                   for prop in ('fd', 'path', 'num-buffers')):
            raise RuntimeError('Installed pipewiresrc lacks required fd/path/num-buffers properties')
        serial = streams[0][1].get('pipewire-serial')
        if serial is not None:
            if not re.search(r'^\s*target-object\s*:', inspect.stdout, re.M):
                raise RuntimeError('Provider returned a serial but pipewiresrc lacks target-object')
            target = f'target-object={serial}'
        else:
            target = f'path={streams[0][0]}'
        log('gstreamer_target', property=target)
        pipeline = ['gst-launch-1.0', '-v', 'pipewiresrc', f'fd={remote_fd}',
                    target, 'num-buffers=5', '!',
                    'fakesink', 'sync=false', 'silent=false']
        capture = subprocess.run(pipeline, pass_fds=(remote_fd,), text=True,
                                 capture_output=True, timeout=a.timeout)
        print(capture.stdout, flush=True)
        print(capture.stderr, file=sys.stderr, flush=True)
        buffers = len(re.findall(r'last-message = chain', capture.stdout))
        if capture.returncode != 0 or buffers < 5 or 'Got EOS' not in capture.stdout:
            raise RuntimeError(f'GStreamer did not prove five buffers: exit={capture.returncode}, buffers={buffers}')
        log('RILEX_SCREENCAST_FRAMES_PASS', received_buffers=buffers,
            browser_screen_sharing_tested=False)
except Exception as error:
    log('failure', error=str(error))
    sys.exit(1)
finally:
    if remote_fd is not None:
        os.close(remote_fd)
    if session:
        bus.call_sync(service, session, 'org.freedesktop.portal.Session', 'Close',
                      None, None, Gio.DBusCallFlags.NONE, 5000, None)
