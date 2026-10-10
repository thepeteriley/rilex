# Test procedure and results

## Recorded results

Source checks pass seven installer assertions, 53 expanded Lua bindings, shell
syntax, SVG XML and Waybar JSON parsing. These are static checks.

Actual hosted builds produced hybrid ISOs from d642a14 and 3d36fcd. Downloaded
artifact digests, ISO SHA-256 and filesystem/kernel/initramfs/BIOS/UEFI structure
passed. The compact 3d36fcd image is 1,769,701,376 bytes and has checksum
`bc362bf1779ea714736b7aaa140f54a504118588de713cb6c9982f11d997c800`.
It remains a development candidate with known runtime defects fixed in later source.

The d642a14 ISO actually booted UEFI under QEMU11.1.2 TCG on macOS ARM64 with
plain virtio-vga. Hyprland0.55.2 initialized through Mesa kms_swrast; XWayland
fell back to software rendering. Rilex wallpaper/welcome appeared, Super+Enter
opened Foot, and Super+Space opened Fuzzel. No special GPU environment flags
were needed for this observed boot. All 15 live service checks passed after
correcting the Waybar launcher path in the disposable live overlay. This is
patched-session evidence, not an unmodified ISO pass. Missing Bluetooth,
backlight and battery devices are expected in this VM.

Actual Calamares launch exposed a missing required branding slideshow field.
The launcher exited before displaying its window; later source supplies an
original slideshow. Installation and independent reboot are still being tested.
Evidence is saved under ignored `.cache/qa-uefi`, including screenshots,
`live-checks-initial.txt`, and installer diagnostics. No release is qualified.

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

For temporary SSH access in the disposable live QA VM, run
`tests/create-qa-seed.sh` before launching it. This creates a separate virtual
CD and a local ephemeral key under ignored `.cache`; neither enters the Rilex
ISO. In the live terminal, mount the second CD read-only and run:

```sh
sudo mount -o ro /dev/sr1 /mnt
/mnt/check-live-session.sh > /tmp/live-checks.log 2>&1
sudo /mnt/bootstrap.sh
```

The helper refuses a non-QEMU or non-live system and installs OpenSSH through
signed Debian APT. Access binds to the launcher's loopback port 2223 using
`.cache/qa_ed25519`. Destroy the disposable live VM after testing; this temporary
SSH setup is not part of the released operating system. Use QMP `type` for US
keyboard input when no VNC client is available; text is literal and key events
are paced.

## Package ownership integration check

The actual `rilex-defaults_0.1.0_all.deb` built in the amd64 Debian guest was compared against downloaded official Debian packages for Foot, Fuzzel, Waybar, Mako, Calamares settings, SDDM and the Breeze greeter theme. `tests/test-package-ownership.py` passed across all seven vendor packages: no shared files or symlinks. Shared directories are allowed.

Foot, Fuzzel and Waybar vendor defaults are Debian conffiles; diverting those would impair Debian conffile upgrade semantics. Rilex instead ships distinct paths under `/etc/rilex`, and its launch wrappers honor user configurations before selecting these defaults. No desktop-configuration diversion or `Replaces` declaration is used. The installer settings enter the live image as a live-build overlay and are not owned by the persistent defaults package.

To repeat this check, download the vendor packages with signed APT in the disposable Debian build guest, build the Rilex package, then pass its path and the vendor `.deb` paths to `python3 tests/test-package-ownership.py`. This check proves absence of collisions for the supplied packages; it does not establish runtime desktop or installer functionality.

## Release identity maintenance check

`tests/test-release-identity.sh` passed in the actual amd64 build guest using Debian `base-files` 13.8+deb13u7 and the built Rilex defaults package. It unpacked the real vendor package, installed the Rilex payload in an isolated dpkg root, re-unpacked the vendor package, and verified `ID=rilex` survived. Removing and purging Rilex defaults restored the original Debian identity byte-for-byte. This exercises regular-file replacement during vendor updates, not a full system upgrade. Debian's own `/etc/debian_version` remains untouched.

During the first local emulated build, replacing the generated defaults `.deb` after live-build had indexed its local repository caused APT to reject it with `Hash Sum mismatch`. No verification was disabled. The recovery freezes the package inputs, regenerates `Packages`, `Packages.gz` and `Release` using `apt-ftparchive`, refreshes APT metadata, and resumes the failed package-install stage while keeping downloaded signed Debian packages. Generated package inputs must remain unchanged once their local repository index is built.

## Experimental Linux-host boot evidence workflow

The manually triggered `boot-smoke.yml` workflow accepts the run ID of a successful **Build candidate ISO** run in the same repository. It resolves and checks out that exact source revision, runs source checks, verifies the artifact's SHA-256 checksum and ISO/kernel/initramfs/BIOS/UEFI structure, then starts a disposable 32 GB qcow2 disk with UEFI firmware. It does not run an installer or select partitions. Its token has read-only repository contents and Actions artifact access.

The graphics accommodation uses Linux Xvfb with host Mesa llvmpipe and QEMU `virtio-vga-gl` / GTK `gl=on`. VirGL translates guest GL into the host software GL implementation. This is an experimental alternative to the macOS plain virtio-vga test; host EGL/GLX/virgl compatibility can still fail. Host renderer information, QEMU errors, serial output and QMP screenshots around 60 and 120 seconds are uploaded as evidence. A completed workflow means evidence was captured, not that the desktop or installer passed. Inspect the screenshots and logs, then perform live-session and separate installation verification before accepting any release criterion. The blank disposable disk is excluded from uploaded evidence.

## Installer failure evidence

Run `tests/collect-installer-diagnostics.sh` only inside the disposable QEMU guest. It reads configuration, package versions, boot platform, disks and recent logs without launching the installer or changing disks. Preserve its output privately, because installer logs can contain user names. Identify the first failing Calamares job and its exact command/stderr before retrying. In particular distinguish missing GRUB platform files from a missing EFI mount, partition operations from unpackfs failures, and initramfs generation from later APT package cleanup. Do not replay destructive partition commands by hand. Run the graphical installer against the VM's disposable virtio disk only and capture its summary before confirmation.
