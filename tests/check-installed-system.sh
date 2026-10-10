#!/bin/bash
# Run inside the installed guest AFTER ejecting the ISO and independently booting.
set -euo pipefail
grep -qx ID=rilex /etc/os-release
[ "$(readlink /etc/os-release)" = ../usr/lib/os-release ]
[ ! -d /run/live/medium ]
[ -s /boot/grub/grub.cfg ]
findmnt /
getent passwd "$(id -un)"
[ "$(id -u)" -ne 0 ]
systemctl is-active NetworkManager
hyprctl version
pgrep -u "$(id -u)" -x waybar
sudo apt-get update
printf '%s\n' 'PASS installed-system checks; preserve this output with boot screenshots.'
