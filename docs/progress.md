# Rilex 0.1 progress

Status: development, not a verified release.

## Host inspection (2026-10-10)
- macOS 27.0.1, ARM64, 8 CPUs, 24 GiB RAM, 1.3 TiB free.
- Git and authenticated GitHub CLI available (thepeteriley).
- No existing virtualization tools; installed Homebrew QEMU 11.1.2.
- ARM hardware virtualization is available (`kern.hv_support=1`), but cannot accelerate x86 guests.
- Host passwordless sudo unavailable; host privilege is unnecessary for QEMU TCG.
- amd64 Linux will run with explicit QEMU software emulation, not ARM container execution.

## Tasks
- [x] Inspect host and GitHub authentication.
- [x] Confirm official Debian Trixie backports Hyprland availability.
- [x] Establish Debian amd64 build VM (HTTPS SHA-512 image manifest checked; no detached manifest signature available).
- [x] Implement live-build and Debian defaults package.
- [x] Implement Hyprland desktop and welcome utility; 53 expanded bindings statically checked.
- [x] Configure Calamares and run five static checks; runtime installation pending.
- [x] Build real hybrid ISO (two hosted candidates; release qualification pending).
- [ ] Test UEFI/BIOS live desktop.
- [ ] Install to disposable VM disk and independently boot.
- [x] Publish source repository: https://github.com/thepeteriley/rilex.
- [ ] Publish verified release and checksums; tag only after installation tests pass.

Hyprland package indexed as 0.55.2+ds-1~bpo13+1 in official
trixie-backports. Signed APT metadata was verified by debootstrap. Actual APT simulation resolved
all pinned desktop packages from Stable and official backports.

## Build attempts
Hosted candidate builds were superseded after integration review; the current
build is tracked in GitHub Actions. Local emulated amd64 guest prerequisites
installed, and its disposable root filesystem expanded to 79 GiB. Reviewed and fixed Debian installer file ownership,
live-config SDDM session override, and invalid xorriso verifier command.
Source static checks pass; runtime results are recorded below.

Package payload comparison passed against seven actual Debian packages (Foot,
Fuzzel, Waybar, Mako, Calamares settings, SDDM, Breeze). Vendor conffiles are
untouched; Rilex application wrappers select user configuration first, then
`/etc/rilex` defaults. CI source checks passed. No runtime test is inferred
from these static or package-ownership results.

The local build rejected a changed local .deb after indexing (Hash Sum mismatch).
The package index was regenerated with frozen inputs; APT refresh then passed.
No hash/signature/TLS validation was disabled. Source 530981f is frozen for the
resumed local candidate. The source recipe now selects lightweight Maui instead
of Breeze to avoid importing Plasma. Hosted candidate d642a14 remains useful
for initial desktop diagnosis; a compact current-source hosted build also runs.

## Real candidate evidence
Hosted run [38076402014](https://github.com/thepeteriley/rilex/actions/runs/38076402014)
built source 3d36fcd successfully. The downloaded archive digest and ISO checksum
passed. That compact candidate was downloaded to `.cache/candidate-3d36`, 1,769,701,376 bytes,
SHA-256 `bc362bf1779ea714736b7aaa140f54a504118588de713cb6c9982f11d997c800`.
Its live filesystem, kernel/initramfs, BIOS and UEFI boot entries passed structural
checks. It is a development candidate, not a verified release.

Earlier candidate d642a14 was booted under QEMU TCG on macOS ARM64. UEFI GRUB
loaded kernel 6.12.111, mounted the live SquashFS and entered Hyprland. Rilex
welcome, wallpaper and Foot appeared; Super+Enter opened terminal windows.
Waybar, portals, application launching and installation remain under investigation.
This runtime evidence belongs to the earlier candidate, not the compact ISO.
The upstream session watchdog invocation was corrected after seeing its warning.
No independent installed-system boot has yet passed; no release/tag exists.

Runtime investigation found and fixed the Waybar default path mismatch (3363b9b),
required Calamares branding slideshow (fafcc69), and live-build's regular
`/etc/os-release` shadowing the package identity (b4bda6d). Patched live-session
checks passed all 15 service assertions. Fuzzel appeared through Super+Space.
These fixes require a fresh candidate; existing ISO files are diagnostic builds.

Hosted corrected source e7fd8e4 built successfully in run
[38077567221](https://github.com/thepeteriley/rilex/actions/runs/38077567221).
Its artifact digest, ISO checksum and structural verification passed.
`dist/rilex-0.1-amd64.iso` now holds this corrected diagnostic candidate:
1,769,701,376 bytes, SHA-256
`ec54e0092af724cc887e1f6f3b5bc683e01e594daaa0fbf57860550d1792ac04`.
Container provenance recorded `unknown`; b252079 now passes the exact CI commit
explicitly and rejects missing source provenance. An attestation-enabled build
is running. Source e7fd8e4 is identifiable from the Actions run, but its embedded
metadata defect excludes it from release qualification.

The earlier diagnostic ISO installer reached reviewed summary/confirmation,
created only the disposable vda partitions, and began unpackfs. Super+2 switched
workspaces and Fuzzel successfully launched Foot. All 53 bindings were present
in actual `hyprctl -j binds` output. Installation completion/independent reboot
remain pending.

Generated VM/download caches were atomically relocated to
`/Users/pete/.cache/rilex-build-20261010`, with the project `.cache` path kept
as a symlink. Dropbox had been hashing actively written VM files continuously.
The rename stayed on the same filesystem; both QA VMs remained running and
QMP endpoints passed status checks. Credentials remain in the ignored private
cache directory, not the source or distribution image.
