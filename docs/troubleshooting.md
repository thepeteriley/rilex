# Troubleshooting

If the desktop fails, switch to a text console and inspect `journalctl -b -u sddm` and the user journal. Inspect `hyprctl configerrors` inside the desktop. GPU support and VM rendering depend on the pinned Hyprland build; preserve the compositor logs rather than switching the release to another compositor.

For launcher or bar failures, launch `fuzzel` or `waybar` from Foot and retain stderr. Check the relevant configuration under `/etc/rilex` and `~/.config`.

For networking use `nmcli device status`, `nmcli radio`, and `journalctl -b -u NetworkManager`. Missing laptop firmware is separate from NetworkManager configuration. For audio inspect `wpctl status` and `systemctl --user status pipewire wireplumber`.

Calamares uses the Debian settings package's full partition, unpack, user, initramfs and bootloader modules. It requires the live SquashFS at `/run/live/medium/live/filesystem.squashfs`. The Rilex override omits Debian's `bootloader-config` apt-install helper: both GRUB platform payloads must already be in the image for the normal unencrypted path. Inspect installer logs for missing GRUB modules or EFI mount errors. Do not work around failure by installing to another physical disk.

For an installed system that fails to boot, preserve the VM disk and installer logs and reattach the ISO for diagnosis. Verify `/boot/grub/grub.cfg`, the EFI System Partition and initramfs. Do not claim installation success based on the final installer page alone.

APT should use signed official Debian trixie/security/updates metadata. A failed signature check must be corrected at its cause (clock, network, keys), never bypassed with unauthenticated options.
