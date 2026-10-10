# Desktop customization

Rilex uses distribution defaults under `/etc/xdg` and user overrides under `$XDG_CONFIG_HOME` (normally `~/.config`). Package upgrades update distribution defaults without replacing user-owned files.

Create `~/.config/hypr/user.lua` for Hyprland settings; it loads after Rilex defaults. For example:

```lua
hl.config({ input = { kb_layout = "us", touchpad = { natural_scroll = false } } })
hl.monitor({ output = "eDP-1", mode = "preferred", position = "auto", scale = 1.5 })
```

Default monitors use preferred resolution and automatic scaling. Use `hyprctl monitors` to discover output names. Restart the session after changing environment settings; ordinary config changes can be reloaded with `hyprctl reload`. Errors appear in `hyprctl configerrors`.

Copy `/etc/rilex/waybar`, `/etc/rilex/fuzzel`, `/etc/rilex/foot` or `/etc/xdg/mako` into `~/.config/` before editing their files. Rilex wrappers choose user configs first, then the Rilex defaults via each application’s explicit configuration argument. Debian’s vendor application defaults remain package-owned and unchanged. Restart the corresponding application after edits. Rilex Welcome offers wallpaper selection, GTK dark/light theme selection and terminal configuration. It saves the image path in `~/.config/rilex/wallpaper`.

Audio device and microphone selection are available in `pavucontrol`; network configuration uses keyboard-friendly `nmtui`. Bluetooth configuration uses Blueman or `bluetoothctl`. Thunar handles removable media via UDisks. Screenshot region selection uses the pointer; terminal users can run `grim filename.png` for a whole-screen image.

The wallpaper and logo are original SVG artwork supplied under the repository's license. No Omarchy artwork or code is included. Rilex combines Debian packages and independently maintained desktop defaults; it is not affiliated with Debian or Omarchy.

## Session diagnostics

SDDM starts the Rilex session with the distribution Lua config explicitly. The config imports Wayland session variables into D-Bus/systemd before starting desktop helpers, so portal services can connect to the correct display. Failed audio/environment imports are logged with `journalctl -t rilex-session` and do not prevent Waybar or the launcher from starting. Inspect `systemctl --user status pipewire wireplumber xdg-desktop-portal` and `journalctl --user -b` for service failures.

The live account has no user-selected password and cannot securely unlock Hyprlock, so `rilex-lock` displays a notice during the live session. Installed accounts use their own passwords. Suspend/resume and lid behavior require hardware validation; Rilex does not claim an idle-lock service or automatic lock-before-suspend in this candidate.

## Login screen and initial session

The initial Rilex defaults package seeds SDDM's `[Last] Session=rilex.desktop` only when its state file is absent or empty; subsequent package updates preserve the user's remembered session. Select **Rilex (Hyprland)** in the login screen session menu if you previously selected another session. The separate upstream Hyprland entry is retained by its Debian package.

Breeze remains the Debian-provided login theme. Its supported `theme.conf.user` override points to `/etc/rilex/sddm-breeze.conf`, using original Rilex SVG artwork. Edit this conffile to customize login branding; Debian package conffile handling preserves local edits. No Debian Breeze theme file is replaced. Sources: [SDDM v0.21 configuration](https://github.com/sddm/sddm/blob/v0.21.0/src/common/Configuration.h), [session preselection](https://github.com/sddm/sddm/blob/v0.21.0/src/greeter/SessionModel.cpp), and [Debian's matching KDE 6.3.6 theme settings](https://github.com/KDE/plasma-desktop/blob/v6.3.6/sddm-theme/theme.conf.cmake). Visual rendering still requires live testing.
