#!/bin/bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")/.." && pwd)
[[ $(uname -s) == Linux && $(dpkg --print-architecture) == amd64 ]] || { echo 'Run this on Debian amd64, including an emulated amd64 VM.' >&2; exit 1; }
[[ $EUID == 0 ]] || { echo 'Run with sudo; live-build requires chroot and mount privileges.' >&2; exit 1; }
for tool in lb debootstrap dpkg-deb xorriso rsync sha256sum; do command -v "$tool" >/dev/null || { echo "Missing build prerequisite: $tool" >&2; exit 1; }; done
WORK="$ROOT/.build/iso"
mkdir -p "$WORK" "$ROOT/dist"
if [[ -e "$WORK/.build" || -d "$WORK/chroot" ]]; then
 echo 'Previous build exists. Use sudo build/clean.sh before regenerating configuration.' >&2; exit 1
fi
"$ROOT/build/build-packages.sh"
cd "$WORK"
lb config --mode debian --distribution trixie --architecture amd64 \
 --archive-areas 'main contrib non-free-firmware' --backports true \
 --security true --updates true --apt-secure true --apt-recommends true \
 --mirror-bootstrap https://deb.debian.org/debian \
 --mirror-chroot https://deb.debian.org/debian \
 --mirror-binary https://deb.debian.org/debian \
 --mirror-chroot-security https://security.debian.org/debian-security \
 --mirror-binary-security https://security.debian.org/debian-security \
 --binary-image iso-hybrid --bootloaders 'syslinux grub-efi' \
 --uefi-secure-boot disable --debian-installer none \
 --linux-flavours amd64 --initsystem systemd --initramfs live-boot \
 --firmware-chroot true --firmware-binary true \
 --checksums sha256 --iso-volume RILEX_0_1 --iso-application Rilex \
 --iso-publisher 'Rilex project; unofficial Debian derivative' \
 --bootappend-live 'boot=live components hostname=rilex username=live locales=en_US.UTF-8 keyboard-layouts=us timezone=UTC' \
 --chroot-squashfs-compression-type zstd
rsync -a "$ROOT/config/" config/
# Installer integration overlays Debian Calamares settings only in the live image,
# avoiding conflicting file ownership in the persistent defaults package.
rsync -a "$ROOT/installer/rootfs/" config/includes.chroot/
mkdir -p config/packages.chroot
cp "$ROOT/dist/rilex-defaults_0.1.0_all.deb" config/packages.chroot/
lb build 2>&1 | tee "$ROOT/dist/build.log"
cp live-image-amd64.hybrid.iso "$ROOT/dist/rilex-0.1-amd64.iso"
cp live-image-amd64.packages "$ROOT/dist/rilex-0.1-amd64.packages" 2>/dev/null || true
cd "$ROOT/dist"
sha256sum rilex-0.1-amd64.iso > rilex-0.1-amd64.iso.sha256
"$ROOT/build/verify-iso.sh" "$ROOT/dist/rilex-0.1-amd64.iso"
