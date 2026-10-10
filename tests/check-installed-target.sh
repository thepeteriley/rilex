#!/bin/bash
# Read-only structural checks for a completed installation on the disposable VM disk.
# The caller must mount vda2 and its vda1 EFI partition before running this script.
# This supplements, never replaces, booting without the ISO.
set -euo pipefail
TARGET=${1:?Usage: check-installed-target.sh MOUNTED_ROOT CREATED_USER}
CREATED_USER=${2:?Pass the user created through Calamares}
[[ $EUID == 0 && -r /sys/class/dmi/id/product_name ]]
[[ $(cat /sys/class/dmi/id/product_name) == *QEMU* || $(cat /sys/class/dmi/id/sys_vendor) == *QEMU* ]]
[[ $(findmnt -n -o SOURCE --target "$TARGET") == /dev/vda2 ]]
[[ $(findmnt -n -o SOURCE --target "$TARGET/boot/efi") == /dev/vda1 ]]
[[ -s $TARGET/boot/grub/grub.cfg ]]
[[ -s $TARGET/boot/efi/EFI/Rilex/grubx64.efi ]]
find "$TARGET/boot" -maxdepth 1 -type f -name 'vmlinuz-*' | rg .
find "$TARGET/boot" -maxdepth 1 -type f -name 'initrd.img-*' | rg .
rg -q '^ID=rilex$' "$TARGET/etc/os-release"
awk -F: -v user="$CREATED_USER" '$1 == user && $3 >= 1000 && $7 !~ /(nologin|false)$/ {found=1} END {exit !found}' "$TARGET/etc/passwd"
awk -F: -v user="$CREATED_USER" '$1 == "sudo" && ("," $4 ",") ~ ("," user ",") {found=1} END {exit !found}' "$TARGET/etc/group"
[[ ! -e $TARGET/etc/sddm.conf.d/90-rilex-live.conf ]]
[[ ! -e $TARGET/usr/share/applications/rilex-install.desktop ]]
[[ ! -e $TARGET/usr/share/applications/calamares-install-debian.desktop ]]
[[ ! -e $TARGET/etc/sudoers.d/live ]]
rg -q 'trixie-security' "$TARGET/etc/apt/sources.list"
rg -q 'trixie-backports' "$TARGET/etc/apt/sources.list"
chroot "$TARGET" dpkg-query -W linux-image-amd64 hyprland sddm grub2-common
printf '%s\n' 'PASS installed-target structural checks; independent boot is still required.'
