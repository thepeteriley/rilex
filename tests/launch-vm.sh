#!/bin/bash
# Start only disposable file-backed disks; never accepts a host block device.
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")/.." && pwd)
MODE=${1:-uefi}
ISO=${2:-"$ROOT/dist/rilex-0.1-amd64.iso"}
[[ $MODE == uefi || $MODE == bios || $MODE == installed ]] || { echo 'Mode must be uefi, bios or installed.' >&2; exit 2; }
command -v qemu-system-x86_64 >/dev/null
command -v qemu-img >/dev/null
QA="$ROOT/.cache/qa-$MODE"
mkdir -p "$QA"
DISK="$ROOT/.cache/qa-install.qcow2"
if [[ ! -e "$DISK" ]]; then qemu-img create -f qcow2 "$DISK" 32G; fi
[[ -f "$DISK" && ! -L "$DISK" ]] || { echo 'Refusing non-regular test disk.' >&2; exit 1; }
args=(-machine q35 -smp 2 -m 4096 -drive "file=$DISK,if=virtio,format=qcow2" -device virtio-vga -device qemu-xhci -device usb-tablet -nic user,hostfwd=tcp:127.0.0.1:2223-:22 -display none -vnc 127.0.0.1:1 -serial "file:$QA/serial.log" -qmp "unix:$QA/qmp.sock,server=on,wait=off")
if [[ $(uname -s) == Linux && -r /dev/kvm ]]; then args+=(-accel kvm -cpu host); else args+=(-accel tcg,thread=multi -cpu max); fi
if [[ $MODE != bios ]]; then
 code=${OVMF_CODE:-}; vars=${OVMF_VARS:-}
 for candidate in /usr/share/OVMF/OVMF_CODE_4M.fd /usr/share/OVMF/OVMF_CODE.fd /opt/homebrew/share/qemu/edk2-x86_64-code.fd; do
  [[ -n "$code" || ! -f "$candidate" ]] || code=$candidate
 done
 for candidate in /usr/share/OVMF/OVMF_VARS_4M.fd /usr/share/OVMF/OVMF_VARS.fd /opt/homebrew/share/qemu/edk2-i386-vars.fd; do
  [[ -n "$vars" || ! -f "$candidate" ]] || vars=$candidate
 done
 [[ -f "$code" && -f "$vars" ]] || { echo 'Set OVMF_CODE and OVMF_VARS to matching UEFI firmware files.' >&2; exit 1; }
 [[ -f "$QA/vars.fd" ]] || cp "$vars" "$QA/vars.fd"
 args+=(-drive "if=pflash,format=raw,readonly=on,file=$code" -drive "if=pflash,format=raw,file=$QA/vars.fd")
fi
if [[ $MODE != installed ]]; then
 [[ -f "$ISO" && ! -L "$ISO" ]] || { echo 'ISO must be a regular file.' >&2; exit 1; }
 args+=(-drive "file=$ISO,media=cdrom,readonly=on,format=raw" -boot d)
 if [[ -f "$ROOT/.cache/qa-seed.iso" ]]; then args+=(-drive "file=$ROOT/.cache/qa-seed.iso,media=cdrom,readonly=on,format=raw"); fi
fi
printf '%q ' qemu-system-x86_64 "${args[@]}" > "$QA/command.txt"
printf '\n' >> "$QA/command.txt"
exec qemu-system-x86_64 "${args[@]}"
