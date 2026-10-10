# Test procedure and results

## Recorded results

On the macOS development host, `python3 tests/test-installer.py` passes five static installer checks. These verify the configured installation sequence, live-only launcher guard, GRUB configuration, and absence of embedded installer passwords, and separation of installer overrides from Debian package ownership. These do not boot the image or validate Calamares installation. No ISO boot, installed-system boot, or hardware validation is established by these results. The release is not ready until the checklist below has recorded evidence.

## VM release gates

Use QEMU on a Linux x86-64 machine, KVM when available, OVMF firmware for UEFI, a virtio GPU with an appropriate rendering path, at least 4 GB RAM, and a newly created disposable 32 GB qcow2 disk. Do not attach any host physical disks. Keep the ISO read-only. Prefer a graphical test session because Hyprland/Calamares functionality cannot be proved by serial boot logs alone. Software rendering support depends on the pinned compositor version and must be tested, not assumed.

1. Verify ISO structure/checksum and BIOS/EFI boot entries.
2. Boot UEFI, capture the login and usable Hyprland desktop. Repeat in BIOS mode if BIOS compatibility will be claimed.
3. Run `tests/check-live-session.sh` as the live desktop user and save output. Inspect `hyprctl configerrors` and the user journal on any failure.
4. Start Fuzzel with Super+Space, launch Foot, Firefox and Thunar, exercise workspace/move/focus/resize bindings, verify Waybar, clipboard, screenshots and notification actions. Capture evidence; process presence is insufficient for these interactions.
5. Launch Calamares, select ONLY the disposable virtual disk, create a user with a fresh password, inspect the summary and accept its confirmation. Save installer logs. Test normal automatic partitioning first; manual/ESP reuse and encryption are separate cases.
6. Shut down, detach the ISO, and boot only the installed qcow2 disk. Log in as the created user and run `tests/check-installed-system.sh`, saving output. Confirm live autologin and installer launchers are gone.
7. Record ISO SHA-256, source Git revision, firmware, QEMU command/version, disk path, test timestamps and screenshots alongside logs. Report actual pass/fail/unverified status for each gate.

A functional installation test must also refresh signed Debian APT metadata successfully. Package signatures and TLS checks must remain enabled.

Laptop-only validation includes suspend/resume, microphone routing, brightness, Bluetooth pairing, Wi-Fi firmware, USB mounting, external displays/HiDPI, and screen sharing. List each as unverified until tested on identifiable hardware. Do not advertise Secure Boot or encryption from static configuration alone.
