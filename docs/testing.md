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

The manually triggered `boot-smoke.yml` workflow accepts the run ID of a successful **Build candidate ISO** run in the same repository. It resolves and checks out that exact source revision, runs source checks, verifies the artifact's SHA-256 checksum and ISO/kernel/initramfs/BIOS/UEFI structure, then starts a disposable 32 GB qcow2 disk with the selected UEFI or BIOS boot path. It does not run an installer or select partitions. Its token has read-only repository contents and Actions artifact access.

The default graphics mode uses plain `virtio-vga` with QMP surface capture. An optional VirGL accommodation uses Linux Xvfb with host Mesa llvmpipe and QEMU `virtio-vga-gl` / GTK `gl=on`. VirGL translates guest GL into the host software GL implementation. This is an experimental alternative to the macOS plain virtio-vga test; host EGL/GLX/virgl compatibility can still fail. Host renderer information, QEMU errors, serial output and screenshots around 60 and 120 seconds after entering the live GRUB option are uploaded as evidence. Plain mode captures QMP surfaces; VirGL captures the Xvfb host window because GL devices can return `no surface` to QMP screendump. A completed workflow means evidence was captured, not that the desktop or installer passed. Inspect the screenshots and logs, then perform live-session and separate installation verification before accepting any release criterion. The blank disposable disk is excluded from uploaded evidence.

## Installer failure evidence

Run `tests/collect-installer-diagnostics.sh` only inside the disposable QEMU guest. It reads configuration, package versions, boot platform, disks and recent logs without launching the installer or changing disks. Preserve its output privately, because installer logs can contain user names. Identify the first failing Calamares job and its exact command/stderr before retrying. In particular distinguish missing GRUB platform files from a missing EFI mount, partition operations from unpackfs failures, and initramfs generation from later APT package cleanup. Do not replay destructive partition commands by hand. Run the graphical installer against the VM's disposable virtio disk only and capture its summary before confirmation.

The optional `diagnostic_shell` input edits only the selected disposable VM's GRUB invocation to add `systemd.debug_shell=1` and a serial console. It leaves the ISO untouched. After collecting boot screenshots it switches to the guest's root debug console to copy the SDDM journal/configuration and discovered Hyprland logs into the serial evidence. Inspect `grub-debug-edit.png` and `debug-shell.png` to confirm that the kernel option and commands actually reached their intended consoles. This deliberately privileged diagnostic shell is confined to the disposable test boot and must never become an ISO default or be used on a normal installed system.

### Observed Linux TCG renderer failure

Diagnostic run [38079097210](https://github.com/thepeteriley/rilex/actions/runs/38079097210) booted the compact candidate from source `3d36fcd0c799253f30e643e9b5f72022cd2f5e74`. Its actual SDDM journal shows successful autologin for `live`, the correct Rilex session and a started session, followed by helper exit 11. The kernel reports a segmentation fault in `llvmpipe-0` at an AVX2 gather instruction. The login greeter shown afterwards was the result of that session crash, rather than failed authentication. The guest debug console and kernel options were visually verified, and the journal was collected through the serial device.

The workflow now offers a `qemu64` TCG CPU baseline as a diagnostic accommodation, alongside `max`; KVM still uses `host`. A subsequent real UEFI test verified this accommodation with the newer candidate, as recorded below. It avoids exposing the same optional vector instruction set to guest LLVM. It changes neither the ISO nor the installed desktop's rendering configuration. The root cause is not yet narrowed to a particular Mesa, LLVM or QEMU implementation defect. The older failed evidence must not be counted as a working desktop test.

For slow TCG guests whose HMP key-release timers produce repeated or stuck
keys, `tests/qmp.py --explicit-key-events SOCKET key meta_l-spc` sends explicit
press/release events together. Its `type` action supports the same option with
`--typing-delay 1` for paced text. This path actually opened Fuzzel, filtered
Foot and launched it in the corrected e7fd8e4 live session on macOS QEMU 11.
It is a QA input accommodation, not a desktop keyboard configuration change.


Diagnostic run [38145364789](https://github.com/thepeteriley/rilex/actions/runs/38145364789) tested candidate build [38078483245](https://github.com/thepeteriley/rilex/actions/runs/38078483245), source `b252079d4f23cbccbc7b0fe9593e21627a15f788`, with plain virtio-vga and the `qemu64` TCG CPU. The inspected 300-second screenshot shows the Rilex Waybar, Foot Welcome and original wallpaper in a running Hyprland desktop. Actual guest logs show successful Rilex autologin, `start-hyprland` and Mesa 25.0.7 / llvmpipe LLVM 19.1.7 (128-bit) initialization, without the previous segmentation fault. The required guest diagnostic marker was received. This verifies live UEFI desktop startup for that candidate and environment; it does not verify installation or the final release image.

`tests/launch-vm.sh` now defaults software emulation to the verified `qemu64` baseline. Set `RILEX_QA_TCG_CPU=max` to compare with a newer emulator if needed. KVM continues to use the host CPU. This is a VM testing accommodation and does not change distribution packages or installed-system settings.

For staged Calamares GUI QA after the disposable VM's QA-only SSH bootstrap,
`tests/calamares-gui-input.py --port PORT --key KEY --known-hosts HOSTS ACTION`
can clear stuck modifiers, advance a reviewed page (`next`), select the erase
radio (`erase-selection`), or fill an independently generated private test
account (`account --credentials FILE`). The credential JSON must be mode0600
with name, username, hostname and password fields. Install QA-only `xdotool`
through signed APT in the live overlay first. The helper requires fullscreen
1280x800 English Calamares and checks QEMU, live media, exactly one disk and its
32GiB size before acting. Capture and review each wizard page using `qmp.py`;
inspect the summary before confirming. An explicitly authorized CI operator may
use `confirm-install --confirm-disposable-vda --qmp SOCKET --evidence DIR` to
click the actual GUI summary and destructive modal; it records screenshots of
both and rechecks the disposable guest guard first. This path is experimental
and must be judged from actual job logs and independent installed-system boot.
The helper never calls partition tools directly.

The experimental native-VM controller `tests/run-calamares-gui.py` automates
those staged English wizard inputs with an explicit `--confirm-disposable-vda`
flag. It starts the actual shipped installer wrapper, records every page,
creates a private random QA credential JSON and requires Calamares's real
`completion: succeeded` log message. Its guarded disk must be a 32 GiB QEMU
`vda`; QA-only xdotool and SSH stay in the live overlay.

After stopping that VM, launch its disposable installed disk with **no ISO or
QA seed attached**. `tests/run-installed-qa.py --qmp SOCKET --credentials JSON
--evidence DIR --serial-log FILE` checks the QMP media inventory, enters the
normal user's SDDM password privately, opens Foot and authenticates sudo. The
actual normal-user shell verifies installed identity, absence of live media,
Hyprland, Waybar, networking, audio, portal and signed APT refresh. A strict
success marker must arrive in QEMU's serial log; keyboard API success alone
cannot pass the test. Its default boot wait is 180 seconds. These fixed wizard
and greeter assumptions are experimental and screenshots require review.

BIOS run [38145981415](https://github.com/thepeteriley/rilex/actions/runs/38145981415) subsequently booted the same `b252079` candidate on a separate disposable disk, omitting OVMF firmware. Its inspected 300-second screenshot also shows the running Hyprland desktop, Waybar, Foot Welcome and Rilex wallpaper. This establishes BIOS live desktop startup for that candidate under native Linux TCG with `qemu64`.

The manual `installation-qa.yml` workflow verifies a selected successful build's exact source and ISO, uses a separate checkout for the newer QA controllers, and starts a fresh 32 GB QEMU disk. A separate test CD supplies ephemeral SSH access only inside the disposable live guest. It runs the ordinary live-session checks and the real graphical Calamares workflow, requires actual installer-log completion, then shuts down the live VM. A new VM boots only the installed disk with no virtual CD attached; the driver must perform normal SDDM login and receive the guest's strict installed-system success marker after desktop, audio, portal, networking and signed APT checks. Evidence excludes the random credential file, SSH private key and virtual disk. A workflow definition is not a passed test; actual results must be recorded after inspecting its logs and screenshots.

The final `feaca70` image from build [38145830005](https://github.com/thepeteriley/rilex/actions/runs/38145830005) passed separate native Linux QEMU 8.2 TCG / `qemu64` live boot tests: [UEFI 38146559897](https://github.com/thepeteriley/rilex/actions/runs/38146559897) and [BIOS 38146562538](https://github.com/thepeteriley/rilex/actions/runs/38146562538). Both workflows first verified the exact source, SHA-256 checksum and ISO boot structure. Both inspected 300-second screenshots show a 1280×800 Hyprland desktop with Rilex Waybar, styled Foot Welcome and wallpaper. The UEFI guest diagnostic log confirms successful SDDM session startup and llvmpipe LLVM 19.1.7 (128-bit), without the earlier crash. Expected unsuccessful nested-Wayland/EGL probes fall back to working DRM software rendering; no missing GRUB font warning appeared. These are live boot results. The separate final-image Calamares installation and independent installed-system boot must pass before release readiness can be claimed.

## Keyboard verification scope

The final live guest's retained `bindings.json` reports 53 registered bindings;
the static dispatcher schema also validates 53 unique expanded bindings.
Arguments were reviewed against the pinned [Hyprland v0.55.2 Lua dispatcher source](https://github.com/hyprwm/Hyprland/blob/v0.55.2/src/config/lua/bindings/LuaBindingsDispatchers.cpp):
H/J/K/L direction names, numeric workspaces, relative pixel resizing, floating
and fullscreen toggles, and relative monitor selectors use that version's API.
Moving a window to a workspace follows it by default. Super+Shift+Space sends
`togglesplit` to dwindle; this changes an applicable tiled split's orientation,
and is not a switch to another layout. It requires a suitable multi-window
split, as shown by the pinned [dwindle implementation](https://github.com/hyprwm/Hyprland/blob/v0.55.2/src/layout/algorithm/tiled/dwindle/DwindleAlgorithm.cpp).

Earlier real QEMU sessions recorded Super+Enter opening Foot, Super+Space
opening Fuzzel and launching Foot, workspace switching, rightward focus,
fullscreen and floating toggles. Retained screenshots and compositor JSON are
under `.cache/qa-uefi` and `.cache/qa-e7-uefi`. These earlier interactions support
the unchanged bindings but are not a claim that every shortcut was exercised
on the final ISO. Directional moves, all resize directions, split changes and
workspace transfers across multiple monitors remain outside the recorded
interaction evidence. Monitor transfers also require a second active output.

The replacement image including pinned `hyprland-guiutils`, built from exact
source `5efe9878386ae51e884ad391ea0045e19a519c66` in
[38148757735](https://github.com/thepeteriley/rilex/actions/runs/38148757735),
passed independent native Linux QEMU 8.2 / TCG `qemu64` live boots:
[UEFI 38156157185](https://github.com/thepeteriley/rilex/actions/runs/38156157185)
and [BIOS 38156158288](https://github.com/thepeteriley/rilex/actions/runs/38156158288).
Both exact-source, checksum and ISO structure gates passed. Inspected
300-second screenshots show the 1280×800 Rilex Hyprland desktop, Waybar, Foot
Welcome and wallpaper. UEFI guest diagnostics confirm successful SDDM session
startup and llvmpipe LLVM 19.1.7 (128-bit), without a crash or the earlier
`hyprland-dialog missing from PATH, cannot start ANRManager` error. No warning
overlay appears in the captured desktop; because startup notifications expire,
that screenshot alone cannot prove their absence during the first 15 seconds.
The separate installation test must use this replacement image before these
live boot results can qualify a release.

For interactive portal QA in an ordinary desktop user's session,
`python3 tests/qa-filechooser-portal.py` keeps a real FileChooser.OpenFile
request alive until selection or cancellation. It records the actual response
and file URIs; cancellation does not count as selection success.
`python3 tests/qa-screencast-portal.py` follows the
[official ScreenCast session API](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html),
requires successful asynchronous CreateSession/SelectSources/Start responses,
and checks the stream node and OpenPipeWireRemote file descriptor. The provider's
actual source-selection dialog must be approved. This proves a portal handshake
only, not captured video frames or a browser application's screen sharing.
Both scripts require Debian's python3-gi and time out after180seconds; they are
QA tools and are not included in the desktop image.

The ScreenCast client optionally accepts `--sample-frames` after installing
QA-only `gstreamer1.0-tools` and `gstreamer1.0-pipewire` through signed APT.
It records the installed `gst-inspect-1.0 pipewiresrc` properties, passes the
authorized portal FD into the child without closing the portal session, and
requires five actual fakesink buffer messages plus EOS and successful pipeline
completion. A handshake success remains distinct from this buffer check and
from application-specific browser sharing.

When the provider supplies `pipewire-serial`, the frame probe uses the inspected
GStreamer `target-object` property rather than the deprecated node-ID `path`.
This follows ScreenCast version6 guidance and the installed PipeWire plugin's
serial-target interface. A first actual attempt using `path` failed with
`target not found` and zero buffers; it must not be counted as frame success.
