#!/bin/bash
# Read-only evidence collection inside the disposable QEMU guest.
# Does not launch Calamares, select partitions, change packages, or write disks.
set -uo pipefail
[[ -r /sys/class/dmi/id/product_name ]] || exit 1
[[ $(cat /sys/class/dmi/id/product_name) == *QEMU* || $(cat /sys/class/dmi/id/sys_vendor) == *QEMU* ]] || {
    echo 'Refusing installer diagnostics outside a QEMU guest.' >&2; exit 1;
}
section() { printf '\n### %s\n' "$1"; }
section identity
date --iso-8601=seconds
uname -a
cat /etc/os-release
section disks
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,MODEL
findmnt /
findmnt /run/live/medium || true
section boot-platform
if [[ -d /sys/firmware/efi ]]; then echo UEFI; else echo BIOS; fi
ls /usr/lib/grub
for t in x86_64-efi i386-pc; do
    [[ ! -f /usr/lib/grub/$t/modinfo.sh ]] || sha256sum "/usr/lib/grub/$t/modinfo.sh"
done
section packages
dpkg-query -W calamares calamares-settings-debian grub2-common grub-common grub-pc-bin grub-efi-amd64-bin efibootmgr rilex-defaults hyprland sddm 2>&1
section configuration
for p in /etc/calamares/settings.conf /etc/calamares/modules/{partition,unpackfs,bootloader,displaymanager,shellprocess,packages,users,welcome}.conf /etc/sddm.conf /etc/sddm.conf.d/90-rilex-live.conf; do
    if [[ -f $p ]]; then printf '\nFILE %s\n' "$p"; cat "$p"; fi
done
section apt-sources
find /etc/apt -maxdepth 2 -type f \( -name '*.list' -o -name '*.sources' \) -print -exec cat {} \;
section installer-processes
pgrep -af 'calamares|grub-install|update-initramfs' || true
section installer-log-errors
# Calamares logs may contain user names, so keep raw evidence private until reviewed.
for p in /var/log/Calamares.log /root/.cache/calamares/session.log /home/live/.cache/calamares/session.log; do
    if [[ -f $p ]]; then
        printf '\nLOG %s\n' "$p"
        tail -n 160 "$p"
    fi
done
section display-manager
systemctl status sddm --no-pager || true
