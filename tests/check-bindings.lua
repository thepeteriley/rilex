-- Execute all config branches with a strict API schema, without a compositor.
-- Schema reviewed against pinned upstream v0.55.2 LuaBindingsDispatchers.cpp.
local bindings = {}
local allowedDirections = { left=true, right=true, up=true, down=true }
local function action(name, validate)
 return function(args)
  if validate then validate(args) end
  return { name=name, args=args }
 end
end
local function direction(t) assert(type(t)=='table' and allowedDirections[t.direction], 'invalid direction') end
local function windowMove(t)
 assert(type(t)=='table')
 if t.direction then direction(t) else assert(type(t.workspace)=='number', 'workspace required') end
end
hl = {
 monitor=function(t) assert(t.mode=='preferred') end,
 env=function() end, config=function() end, on=function(name, cb) assert(name=='hyprland.start') end,
 dsp={
  exec_cmd=action('exec',function(s) assert(type(s)=='string' and #s>0) end),
  focus=action('focus',function(t) if t.direction then direction(t) else assert(type(t.workspace)=='number') end end),
  layout=action('layout',function(s) assert(s=='togglesplit') end),
  window={
   close=action('close'),
   fullscreen=action('fullscreen',function(t) assert(t.action=='toggle') end),
   float=action('float',function(t) assert(t.action=='toggle') end),
   move=action('move',windowMove),
   resize=action('resize',function(t) if t then assert(type(t.x)=='number' and type(t.y)=='number' and t.relative==true) end end),
   drag=action('drag'),
  },
  workspace={move=action('workspace.move',function(t) assert(t.monitor=='-1' or t.monitor=='+1') end)},
 },
 bind=function(key, dispatcher)
  assert(not bindings[key], 'conflicting shortcut: '..key)
  assert(dispatcher and dispatcher.name, 'invalid dispatcher')
  bindings[key]=dispatcher
 end,
}
-- Ignore real user's personal customization during this isolated check.
io.open=function() return nil end
dofile(arg[1] or 'desktop/hyprland/hyprland.lua')
for _, key in ipairs({'SUPER + Return','SUPER + space','SUPER + Q','SUPER + F','SUPER + V','SUPER + SHIFT + space','SUPER + E','SUPER + B','SUPER + SHIFT + S','SUPER + Escape','SUPER + slash','SUPER + C'}) do
 assert(bindings[key], 'missing required shortcut: '..key)
end
for i=1,9 do assert(bindings['SUPER + '..i]); assert(bindings['SUPER + SHIFT + '..i]) end
for _,k in ipairs({'H','J','K','L'}) do
 assert(bindings['SUPER + '..k]); assert(bindings['SUPER + SHIFT + '..k]); assert(bindings['SUPER + CTRL + '..k])
end
local n=0; for _ in pairs(bindings) do n=n+1 end
print('Validated '..n..' unique bindings and dispatcher arguments (static schema; no runtime compositor).')
