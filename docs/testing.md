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

## Included disposable VM tools

`tests/launch-vm.sh uefi` and `tests/launch-vm.sh bios` launch QEMU with a
file-backed 32 GB test disk under `.cache`, VNC on localhost:5901, and QMP/serial
logs under `.cache/qa-MODE`. They accept no physical disk argument. Stop one
VM before starting another. `tests/launch-vm.sh installed` omits the ISO and
reuses the installation test disk. On macOS the script locates Homebrew QEMU
firmware; on Linux install OVMF, or supply a matching `OVMF_CODE`/`OVMF_VARS` pair.

Capture evidence with:

```sh
python3 tests/qmp.py .cache/qa-uefi/qmp.sock screenshot .cache/qa-uefi/desktop.png
python3 tests/qmp.py .cache/qa-uefi/qmp.sock key meta_l-ret
python3 tests/qmp.py .cache/qa-uefi/qmp.sock status
```

These launch/control tools do not assert a passing desktop or installer test.
Every interaction still needs observation and recorded results. VNC and
forwarded SSH ports bind only to loopback; no credentials are included in the
source or release payload.

## Hyprland graphics under software-emulated QEMU

A plain `virtio-vga` virtual device presents a KMS display without host GL acceleration. For a diagnostic attempt from an active guest VT (after stopping SDDM), run as the live user:

```sh
LIBGL_ALWAYS_SOFTWARE=1 AQ_NO_MODIFIERS=1 Hyprland --config /etc/xdg/hypr/hyprland.lua
```

These are test-session environment variables, not installed desktop defaults. If logs specifically show atomic commit failure, retry with `AQ_NO_ATOMIC=1`. Ensure Mesa's Debian `libgl1-mesa-dri` package is installed. Successful initialization must show the actual renderer in the Hyprland log and a usable desktop; setting an environment variable does not itself establish software rendering. A TTY/session without DRM device access is a different failure and must be diagnosed before adjusting rendering.

This path is an inference from the pinned sources, pending runtime verification: [Hyprland v0.55.2 OpenGL.cpp](https://github.com/hyprwm/Hyprland/blob/v0.55.2/src/render/OpenGL.cpp) falls back to the primary DRM node and GBM, while [Aquamarine v0.10.0 DRM.cpp](https://github.com/hyprwm/aquamarine/blob/v0.10.0/src/backend/drm/DRM.cpp) implements `AQ_NO_MODIFIERS` and `AQ_NO_ATOMIC`. The resulting Mesa software renderer must still provide working GBM buffers and DRM PRIME import; failures can prevent the compositor starting.

Old `WLR_RENDERER_ALLOW_SOFTWARE` and `WLR_BACKENDS` instructions target Hyprland's previous wlroots architecture and do not configure this Aquamarine release. Bare Aquamarine headless does not eliminate the DRM allocator requirement. Nesting inside a pixman-only Weston is also insufficient: the [Aquamarine Wayland backend](https://github.com/hyprwm/aquamarine/blob/v0.10.0/src/backend/Wayland.cpp) requires `zwp_linux_dmabuf_v1`, valid device feedback and a DRM node. A nested successful session would validate applications/configuration, but would still need separate direct live-boot validation.
