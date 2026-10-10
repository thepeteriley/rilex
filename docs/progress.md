# Rilex 0.1 progress

Status: development, not a verified release.

## Host inspection (2026-10-10)
- macOS 27.0.1, ARM64, 8 CPUs, 24 GiB RAM, 1.3 TiB free.
- Git and authenticated GitHub CLI available (thepeteriley).
- No existing virtualization tools; installed Homebrew QEMU 11.1.2.
- Host passwordless sudo unavailable; host privilege is unnecessary for QEMU TCG.
- amd64 Linux will run with explicit QEMU software emulation, not ARM container execution.

## Tasks
- [x] Inspect host and GitHub authentication.
- [x] Confirm official Debian Trixie backports Hyprland availability.
- [x] Establish Debian amd64 build VM (HTTPS SHA-512 image manifest checked; no detached manifest signature available).
- [x] Implement live-build and Debian defaults package.
- [x] Implement Hyprland desktop and welcome utility; 53 expanded bindings statically checked.
- [x] Configure Calamares and run five static checks; runtime installation pending.
- [ ] Build real hybrid ISO.
- [ ] Test UEFI/BIOS live desktop.
- [ ] Install to disposable VM disk and independently boot.
- [x] Publish source repository: https://github.com/thepeteriley/rilex.
- [ ] Publish verified release and checksums; tag only after installation tests pass.

Hyprland package indexed as 0.55.2+ds-1~bpo13+1 in official
trixie-backports. Actual signed APT metadata and dependency solving remain to be checked.

## Build attempts
Two real GitHub Actions candidate builds started; local emulated amd64 guest
prerequisites installed. Reviewed and fixed Debian installer file ownership,
live-config SDDM session override, and invalid xorriso verifier command.
Source static checks pass; no live desktop or installation pass is claimed.
