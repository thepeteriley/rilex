#!/bin/bash
set -euo pipefail
ISO=${1:?Usage: build/verify-iso.sh dist/rilex-0.1-amd64.iso}
[[ -s "$ISO" ]] || { echo "Missing or empty ISO: $ISO" >&2; exit 1; }
command -v xorriso >/dev/null
LIST=$(xorriso -indev "$ISO" -find / -type f -exec echo 2>/dev/null)
for pattern in '/live/filesystem.squashfs' '/live/vmlinuz' '/live/initrd'; do
 printf '%s\n' "$LIST" | grep -F "$pattern" >/dev/null || { echo "Missing ISO component: $pattern" >&2; exit 1; }
done
BOOT=$(xorriso -indev "$ISO" -report_el_torito plain 2>/dev/null)
printf '%s\n' "$BOOT"
printf '%s\n' "$BOOT" | grep -E 'BIOS' >/dev/null
printf '%s\n' "$BOOT" | grep -E 'UEFI' >/dev/null
printf 'ISO filesystem, kernel, initramfs, BIOS and UEFI boot entries verified. Runtime installation is a separate gate.\n'
