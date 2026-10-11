# Installed application and desktop integration QA

These observed tests ran on 2026-10-11 as the normal user in the independently booted `feaca7002cb46eb391b0cf40fc5615a09be1d231` installed candidate, on a disposable QEMU disk with no ISO attached. The subsequent `5efe987` candidate uses the same tested desktop configuration and portal stack; its independent installation results are recorded separately. These checks used actual keyboard input and application windows, not simulated test output.

| Check | Actual evidence and result |
|---|---|
| Super+E | Thunar opened the user's home directory; actual client class `thunar`, PID 10541. JSON/screenshot `27-thunar-observed` under `.cache/qa-final-keyboard`. |
| Super+B | Firefox ESR opened its first-run interface; actual class `firefox-esr`, PID 10680. JSON `29-firefox-observed.json`, screenshot `29-firefox.png`. |
| Super+Q | Closed each newly launched application window, restoring the original two terminal windows. |
| Super+slash | Opened the searchable reference; typing `resize` left the resize binding as the result (`31-shortcut-filter.png`). |
| Super+C | Opened clipboard history and selected an older seeded entry (`32-clipboard-picker.png`). `wl-paste` subsequently printed `RilexKeyboardPrimary`, replacing the newer `RilexKeyboardOther` clipboard (`33-clipboard-result.png`). |
| FileChooser portal | Persistent session-bus client displayed the actual GTK file dialog; keyboard selection of `/etc/os-release` returned response 0 and `file:///etc/os-release`. Screenshots 35, 37, 38 and actual `filechooser-guest.jsonl`. |
| ScreenCast portal | Actual provider selection, successful request responses and authorized PipeWire socket; the corrected video consumer received five 4,096,000-byte video buffers and EOS. Actual `screencast-video-pass.log` and screenshots 61–64. |

All listed checks passed within this scope. App launching does not establish complete browser/file-manager functionality. Firefox's normal first-run interface was observed; no test website navigation or browser screen-sharing call was performed. File selection and portal video transport were tested directly through their real interfaces.

The frame consumer used the portal-authorized file descriptor, the returned `pipewire-serial`, and an explicit `video/x-raw` caps filter. Five actual buffer records, EOS and successful pipeline completion were required; a handshake or zero exit status alone did not count. Earlier unconstrained consumers failed with `target not found`; those real failures remain in `screencast-node-failure.log`, `screencast-serial-failure.log`, `screencast-default-server-failure.log` and `screencast-debug.log`. Correcting the QA consumer did not modify the desktop configuration or weaken portal permissions. See [portal QA](qa-portals.md) for the exact test client and limits.

For the frame probe only, signed Debian APT installed `gstreamer1.0-tools` `1.26.2-2` and `gstreamer1.0-pipewire` `1.4.2-1` onto the disposable QA target. These two test packages were not changes to the ISO. Script transfers used a local host loopback server serving only nonsecret QA files, with guest SHA-256 comparison before execution. Actual logs were returned to a bounded loopback receiver; both servers were stopped afterward. The temporary sampler was stopped and WirePlumber logging restored to informational level. The QA VM was then shut down through the normal user's `systemctl poweroff`.

Hardware radio behavior, physical-device audio, browser-mediated sharing, sustained video performance and video pixel quality remain unverified by these tests. Keyboard state tests are documented separately in [qa-keyboard.md](qa-keyboard.md).
