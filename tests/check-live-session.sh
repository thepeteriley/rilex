#!/bin/bash
# Run as the logged-in desktop user in a booted Rilex VM, never in the build chroot.
set -uo pipefail
failures=0
check() {
  local label=$1
  shift
  if "$@"; then printf 'PASS %s\n' "$label"; else printf 'FAIL %s\n' "$label"; failures=$((failures+1)); fi
}
check live-medium test -f /run/live/medium/live/filesystem.squashfs
check hyprland hyprctl version
check hyprland-monitors hyprctl monitors
check waybar pgrep -u "$(id -u)" -x waybar
check networkmanager systemctl is-active NetworkManager
check pipewire systemctl --user is-active pipewire
check wireplumber systemctl --user is-active wireplumber
check audio wpctl status
check portal systemctl --user is-active xdg-desktop-portal
check hyprland-portal systemctl --user is-active xdg-desktop-portal-hyprland
check bindings hyprctl binds
check config-errors bash -c '[ -z "$(hyprctl configerrors)" ]'
check installer command -v rilex-install
check terminal command -v foot
check launcher command -v fuzzel
printf 'Failures: %s\n' "$failures"
exit "$((failures > 0))"
