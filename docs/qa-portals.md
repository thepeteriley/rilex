# Actual desktop portal QA

On 2026-10-11, a normal created user in the independently booted `feaca70`
installed system completed real FileChooser and ScreenCast tests. Its Hyprland
0.55.2, xdg-desktop-portal-hyprland 1.4.1, Stable xdg-desktop-portal 1.20.3,
PipeWire 1.4.2 and WirePlumber 0.5.8 stack and portal configuration are unchanged
in the release candidate `5efe987`; the latter also adds Hyprland GUI utilities.
These interactions supplement the replacement candidate's separate successful
live and installation tests, rather than claiming another installation test.

The QA clients were downloaded as files from a host-loopback-only test server
and their SHA-256 digests inspected before execution. Neither client nor test
server is part of the ISO. QA-only GStreamer tools and its PipeWire plugin were
installed through signed APT in the disposable installed guest.

| Test | Observed result |
|---|---|
| FileChooser.OpenFile | The actual GTK dialog appeared; selecting `/etc/os-release` returned asynchronous response 0 with URI `file:///etc/os-release`. |
| ScreenCast source selection | The actual Hyprland share picker appeared; the tester approved monitor `Virtual-1` at 1280×800. |
| ScreenCast handshake | CreateSession, SelectSources and Start returned response 0; Start supplied a real stream node, PipeWire serial and 1280×800 metadata. OpenPipeWireRemote supplied an open socket FD. |
| Authorized video capture | GStreamer inherited the authorized portal FD while the session remained alive, targeted the returned PipeWire serial and consumed five real video buffers. Five fakesink chain messages, EOS and successful completion produced `RILEX_SCREENCAST_FRAMES_PASS`. |

The frame probe uses `pipewiresrc ... ! video/x-raw ! fakesink`. Initial probes
omitted the video caps filter and negotiated `ANY`; both authorized and default
server comparisons then failed with `target not found` and zero buffers.
The producer was visible in a contemporaneous `pw-dump`, so those failures did
not prove a GPU or portal failure. Adding the video filter to the QA client
resolved the test without changing desktop packages or configuration. During
software-rendered QEMU capture the tester changed window focus to generate
visible damage; the five-buffer pipeline completed in approximately 77 seconds.

Retained evidence under ignored `.cache/qa-final-keyboard` includes
`35-filechooser-dialog.png`, `38-filechooser-result.png`,
`40-screencast-dialog.png`, `41-screencast-result.png`,
`63-video-progress.png`, raw portal responses and GStreamer traces. The final
screenshot visibly records `received_buffers:5` and the strict success marker.
The source clients are `tests/qa-filechooser-portal.py` and
`tests/qa-screencast-portal.py --sample-frames`.

This verifies real portal file selection and monitor video buffers in the
recorded VM. Browser conferencing applications, audio-plus-video sharing,
window/region capture, remote-control permissions, multiple monitors and
physical laptop sharing were not tested. Captured buffers were consumed by a
test sink; their pixel contents were not exported or visually assessed.
