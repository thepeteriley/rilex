# Installed desktop keyboard verification

On 2026-10-11, the normal user in the independently booted, locally installed `feaca7002cb46eb391b0cf40fc5615a09be1d231` candidate was tested through actual QEMU keyboard events. This used the disposable `.cache/qa-final-install.qcow2` with no attached ISO. The desktop had a Welcome terminal and an ordinary Foot terminal. QMP sent explicit Super/key press and release events; a guest background sampler recorded actual `hyprctl -j activewindow` and `hyprctl -j clients` output to the VM serial log. No compositor dispatch commands substituted for keyboard input.

Observed checks passed:

| Keys | Actual result |
|---|---|
| Super+H/L | Focus address changed to the left window and back |
| Super+Shift+H/L | The two windows exchanged horizontal positions and returned |
| Super+Ctrl+H/L | Focused window width changed by 30 pixels and returned |
| Super+V | Floating state became true, then false |
| Super+Shift+Space | Two-window tiling changed from horizontal to vertical and returned |
| Super+Shift+3, Super+3 | Focused window moved to workspace 3; workspace selection followed it |
| Super+1, Super+3, Super+Shift+1 | Workspace navigation and moving the window back restored the original workspace |
| Super+F | Fullscreen state became 2 at 1280×800, then returned to 0 |
| Super+Enter | A third Foot window appeared with a new client address |
| Super+Q | That third window closed; the screenshot shows the original two windows restored |

Ignored `.cache/qa-final-keyboard` retains the controller, `results.log`, numbered JSON states, `assertions.json`, and screenshots. Fifteen assertions against actual captured states passed. Fullscreen needed a separately observed retest because early paired presses outpaced useful sampling under TCG. The final close result was confirmed visually in `25-end.png`; its last JSON sample remained stale, so it is not cited as client-removal evidence.

The keyboard configuration file has no differences between this installed candidate and source revision `5efe987` (the subsequent GUI-utilities package addition). This verifies these bindings for the installed candidate and that shared configuration; it does not replace independent installation verification of a subsequent rebuilt ISO. Directional J/K movement, other numbered workspaces, multi-monitor workspace moves and hardware multimedia keys remain outside this test. The sampler was stopped and the VM left running, logged in, for further QA.

## Application and clipboard checks

Additional actual keyboard tests in the same installed session passed: Super+E opened Thunar at the normal user's home directory (`27-thunar-observed.json` and screenshot), and Super+B opened Firefox ESR's first-run interface (`29-firefox-observed.json` and screenshot). Their observed client classes were `thunar` and `firefox-esr`; Super+Q closed each new application window. These establish launch and window-close behavior, not complete browser or file-manager functionality. No test navigation to an external website was requested.

Super+slash opened the keyboard reference. Typing `resize` reduced the searchable reference to the resize binding (`31-shortcut-filter.png`). For clipboard validation, the terminal seeded `RilexKeyboardPrimary` with `wl-copy`, then seeded `RilexKeyboardOther` as the current clipboard. Super+C opened history; typing `Primary` selected the older entry (`32-clipboard-picker.png`). After Return, actual `wl-paste` output was `RilexKeyboardPrimary` (`33-clipboard-result.png`), verifying history selection restored that entry rather than merely showing a picker.
