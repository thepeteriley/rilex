# Keyboard shortcuts

Super is the Windows/Command modifier. Press **Super + /** to search the shortcut reference using Fuzzel; type to filter, Escape to dismiss.

| Key | Action |
| --- | --- |
| Super + Enter | Foot terminal |
| Super + Space | Fuzzel application launcher |
| Super + Q | Close focused window |
| Super + 1–9 | Switch workspace |
| Super + Shift + 1–9 | Move window to workspace |
| Super + H/J/K/L | Focus left/down/up/right |
| Super + Shift + H/J/K/L | Move window left/down/up/right |
| Super + Ctrl + H/J/K/L | Resize window |
| Super + Ctrl + Shift + H/L | Move workspace to previous/next monitor |
| Super + F | Toggle fullscreen |
| Super + V | Toggle floating |
| Super + Shift + Space | Toggle dwindle split orientation |
| Super + E | Thunar |
| Super + B | Firefox ESR |
| Super + Shift + S | Select screenshot region; save to Pictures/Screenshots and copy |
| Super + Escape | Hyprlock |
| Super + / | Search shortcuts |
| Super + C | Clipboard history |
| Super + W | Rilex Welcome |

Volume/microphone and brightness keys control PipeWire and display brightness. Super + left/right mouse drag moves/resizes windows. Clipboard history stores copied data in the user's cache, including potentially sensitive text; clear it with `cliphist wipe`.

Defaults target Hyprland 0.55's Lua API, reviewed against the [v0.55 example](https://github.com/hyprwm/Hyprland/blob/v0.55.0/example/hyprland.lua) and [versioned dispatcher documentation](https://wiki.hypr.land/0.55.0/Configuring/Basics/Dispatchers/). Runtime validation is recorded in testing documentation; syntax review alone does not prove every binding functions.
