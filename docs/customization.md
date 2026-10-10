# Desktop customization

Rilex uses distribution defaults under `/etc/xdg` and user overrides under `$XDG_CONFIG_HOME` (normally `~/.config`). Package upgrades update distribution defaults without replacing user-owned files.

Create `~/.config/hypr/user.lua` for Hyprland settings; it loads after Rilex defaults. For example:

```lua
hl.config({ input = { kb_layout = "us", touchpad = { natural_scroll = false } } })
hl.monitor({ output = "eDP-1", mode = "preferred", position = "auto", scale = 1.5 })
```

Default monitors use preferred resolution and automatic scaling. Use `hyprctl monitors` to discover output names. Restart the session after changing environment settings; ordinary config changes can be reloaded with `hyprctl reload`. Errors appear in `hyprctl configerrors`.

Copy `/etc/xdg/waybar`, `/etc/xdg/fuzzel`, `/etc/xdg/foot` or `/etc/xdg/mako` into `~/.config/` before editing their files. Restart the corresponding application after edits. Rilex Welcome offers wallpaper selection, GTK dark/light theme selection and terminal configuration. It saves the image path in `~/.config/rilex/wallpaper`.

Audio device and microphone selection are available in `pavucontrol`; network configuration uses keyboard-friendly `nmtui`. Bluetooth configuration uses Blueman or `bluetoothctl`. Thunar handles removable media via UDisks. Screenshot region selection uses the pointer; terminal users can run `grim filename.png` for a whole-screen image.

The wallpaper and logo are original SVG artwork supplied under the repository's license. No Omarchy artwork or code is included. Rilex combines Debian packages and independently maintained desktop defaults; it is not affiliated with Debian or Omarchy.
