-- Rilex defaults for Hyprland 0.55; personal overrides load last.
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto" })
hl.env("XDG_CURRENT_DESKTOP", "Hyprland")
hl.env("XDG_SESSION_DESKTOP", "Hyprland")
hl.env("XDG_SESSION_TYPE", "wayland")
hl.env("XCURSOR_SIZE", "24")
hl.config({
 general = { gaps_in = 5, gaps_out = 12, border_size = 2, layout = "dwindle",
  col = { active_border = "rgb(7699bc)", inactive_border = "rgb(343b45)" } },
 decoration = { rounding = 6, blur = { enabled = false }, shadow = { enabled = false } },
 animations = { enabled = false },
 input = { kb_layout = "us", follow_mouse = 0, touchpad = { natural_scroll = true, tap_to_click = true } },
 dwindle = { preserve_split = true },
 misc = { disable_hyprland_logo = true, force_default_wallpaper = 0 },
})
hl.on("hyprland.start", function() hl.exec_cmd("rilex-session-start") end)
local function run(key, cmd) hl.bind(key, hl.dsp.exec_cmd(cmd)) end
run("SUPER + Return", "foot")
run("SUPER + space", "fuzzel")
run("SUPER + E", "thunar")
run("SUPER + B", "firefox-esr")
run("SUPER + SHIFT + S", "rilex-screenshot")
run("SUPER + Escape", "rilex-lock")
run("SUPER + slash", "rilex-shortcuts")
run("SUPER + C", "rilex-clipboard")
run("SUPER + W", "foot --title=Rilex-Welcome rilex-welcome")
hl.bind("SUPER + Q", hl.dsp.window.close())
hl.bind("SUPER + F", hl.dsp.window.fullscreen({ action = "toggle" }))
hl.bind("SUPER + V", hl.dsp.window.float({ action = "toggle" }))
hl.bind("SUPER + SHIFT + space", hl.dsp.layout("togglesplit"))
local directions = { H = "left", J = "down", K = "up", L = "right" }
for key, direction in pairs(directions) do
 hl.bind("SUPER + " .. key, hl.dsp.focus({ direction = direction }))
 hl.bind("SUPER + SHIFT + " .. key, hl.dsp.window.move({ direction = direction }))
end
for i = 1, 9 do
 hl.bind("SUPER + " .. i, hl.dsp.focus({ workspace = i }))
 hl.bind("SUPER + SHIFT + " .. i, hl.dsp.window.move({ workspace = i }))
end
hl.bind("SUPER + CTRL + H", hl.dsp.window.resize({ x = -30, y = 0, relative = true }), { repeating = true })
hl.bind("SUPER + CTRL + L", hl.dsp.window.resize({ x = 30, y = 0, relative = true }), { repeating = true })
hl.bind("SUPER + CTRL + K", hl.dsp.window.resize({ x = 0, y = -30, relative = true }), { repeating = true })
hl.bind("SUPER + CTRL + J", hl.dsp.window.resize({ x = 0, y = 30, relative = true }), { repeating = true })
hl.bind("SUPER + CTRL + SHIFT + H", hl.dsp.workspace.move({ monitor = "-1" }))
hl.bind("SUPER + CTRL + SHIFT + L", hl.dsp.workspace.move({ monitor = "+1" }))
hl.bind("SUPER + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind("SUPER + mouse:273", hl.dsp.window.resize(), { mouse = true })
run("XF86AudioRaiseVolume", "wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+")
run("XF86AudioLowerVolume", "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")
run("XF86AudioMute", "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")
run("XF86AudioMicMute", "wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle")
run("XF86MonBrightnessUp", "brightnessctl set +5%")
run("XF86MonBrightnessDown", "brightnessctl set 5%-")
-- Only user-owned overrides are loaded; updates never replace them.
local home = os.getenv("HOME")
local config = os.getenv("XDG_CONFIG_HOME") or (home .. "/.config")
local file = io.open(config .. "/hypr/user.lua", "r")
if file then file:close(); dofile(config .. "/hypr/user.lua") end
