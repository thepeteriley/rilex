# Rilex 0.1 release qualification

Candidate source: `5efe9878386ae51e884ad391ea0045e19a519c66`.
ISO: `rilex-0.1-amd64.iso`, 1,773,174,784 bytes.
SHA-256: `0ecd67abaabd1d796619f98ba59b1b1f7d2c90f262be4ece5e2bee5fca65235e`.

| Check | Actual result and evidence |
|---|---|
| Build | PASS, [38148757735](https://github.com/thepeteriley/rilex/actions/runs/38148757735) |
| Source checks | PASS: seven installer assertions, 53 unique bindings, shell syntax, SVG XML and Waybar JSON |
| ISO checksum and structure | PASS: checksum, filesystem, kernel/initramfs, BIOS and UEFI boot images |
| Build origin | PASS: ISO and defaults package cryptographic GitHub attestations verified against build.yml |
| BIOS live desktop | PASS: [38156158288](https://github.com/thepeteriley/rilex/actions/runs/38156158288), inspected Hyprland/Waybar/Foot Welcome screenshot |
| UEFI live desktop | PASS: [38156157185](https://github.com/thepeteriley/rilex/actions/runs/38156157185), inspected desktop screenshot and successful SDDM/llvmpipe diagnostics; no missing-dialog error or crash |
| Desktop application and portal checks | PASS on preceding installed image with identical desktop configuration/component versions: keyboard-launched Thunar and Firefox ESR, searchable shortcuts, clipboard selection, real GTK file selection, actual ScreenCast selection and five portal-authorized PipeWire video buffers with EOS/exit 0; browser conferencing untested |
| Final-image installation and disk-only login/APT | PASS: [38156156216](https://github.com/thepeteriley/rilex/actions/runs/38156156216), 17 live checks, 38 completed Calamares jobs, actual SDDM password login, four active service checks, official signed APT refresh and strict guest success marker; no virtual CD attached |

The source uses Debian 13 Stable and official Trixie backports only. The final
manifest includes Hyprland 0.55.2, guiutils 0.2.2, Hyprlock 0.9.6, Hyprland
portal 1.4.1, Waybar 0.12.0, Fuzzel 1.12.0, Foot 1.21.0 and Calamares 3.3.14.
The GUI-utils dependency transaction added four packages and preserved the
Stable Mesa 25.0.7 stack.

The preceding `feaca70` image completed both local macOS ARM64/QEMU11 TCG and
native Linux/QEMU8.2 TCG real Calamares installations and independent UEFI
password login, desktop, audio, network, portal and signed APT refresh. Its
installed keyboard configuration is identical to this candidate: fifteen
actual captured-state assertions and visual closing checks passed. See
[installed keyboard QA](https://github.com/thepeteriley/rilex/blob/main/docs/qa-keyboard.md)
for scope. These component checks do not substitute for final-image installation.

Hyprlock lock/unlock was tested on an earlier independently installed image;
its exact lock configuration matches this candidate. See
[lock QA](https://github.com/thepeteriley/rilex/blob/main/docs/qa-lock-test.md).

Untested: physical laptop Wi-Fi/audio/microphones/Bluetooth/brightness/USB,
external displays/HiDPI, suspend/resume, browser conferencing, BIOS installation,
manual partitioning, existing EFI partition reuse, Secure Boot and encryption.
Automatic encryption and automatic idle/suspend locking are not configured.
Virtual tests used only disposable file-backed disks. No host physical disk
was passed through, selected or reformatted. QA keys and random credentials
were restricted to the ignored test cache and live overlay, not the ISO.

ScreenCast probe correction: initial GStreamer tests with unspecified ANY caps
failed with zero buffers and `target not found`. Adding explicit `video/x-raw`
caps allowed the consumer to select the video stream; actual visible desktop
damage produced five buffers and successful EOS using the authorized portal FD.
No distribution configuration, security permission or package was changed for
this correction. See [application/portal QA](https://github.com/thepeteriley/rilex/blob/main/docs/qa-applications.md).

The version tag identifies the exact ISO build source above. Later commits on
main add QA tools and results; the ISO and its embedded documentation preserve
build-time provenance. Rebuilds use normal evolving signed Debian repositories
and are not promised to be byte-identical.
