# Installer integration

`rootfs/` overlays the Debian `calamares-settings-debian` package; it is not a complete replacement for that package. Verified interfaces were inspected directly from official Debian trixie amd64 Packages metadata and package contents:

- `calamares-settings-debian` 13.0.13-1, SHA-256 `70e4b052609817c9cac65ea8e8cffe5b87666b58d65d731e686523c36cd227aa`.
- `calamares` 3.3.14-1 amd64, SHA-256 `8e124c35d726dca93d90880f8a7dc55e6fc5cf5efb7d8ad2234b86d9188af801`.

Source/package provenance: https://packages.debian.org/trixie/calamares-settings-debian and https://packages.debian.org/trixie/calamares . Debian package source licenses remain authoritative; the derived settings.conf retains the ISC notice in LICENSES/calamares-settings-debian-ISC.txt; original overlays and the Rilex SVG use the project license. `settings.conf` retains Debian's module sequence and explanatory comments, with branding, confirmation, and the changes below.

Retain Debian helpers for apt source configuration, machine identity, initramfs, package cleanup, and normal installation. `bootloader-config` is omitted because it installs grub packages via APT during installation; Rilex instead preinstalls `grub2-common`, `grub-common`, `grub-pc-bin`, `grub-efi-amd64-bin`, and `efibootmgr` and uses Calamares's regular `bootloader` job. This avoids requiring a network or ISO apt package pool for a normal unencrypted install. The functional offline installation still requires VM validation. Encryption is unverified and the omitted helper's encryption-specific behavior is not replicated.

SDDM is the supported login manager. `shellprocess` removes the live autologin configuration in the target chroot and both installer launchers. It removes `/etc/sddm.conf`, created by Debian live-config, while leaving persistent Rilex dropins. Requested installer autologin is intentionally not retained for this initial configuration. Package removal clears Debian live-boot/config packages, as in the upstream settings.

The launcher verifies live-medium presence, uses Debian live-config's passwordless live sudo, permits root on XWayland only while Calamares runs, and restores the stale live fstab afterward. This avoids embedding live-user credentials. It never runs unattended or selects a disk programmatically.

Calamares configuration and actual bootloader commands must be checked in the built guest. Seven passing static tests are not a release qualification.

Installer rootfs is staged as a live-build includes.chroot overlay, never inside rilex-defaults.deb. This avoids dpkg ownership collisions with calamares-settings-debian. Debian sources-final writes trixie, trixie-security, trixie-updates and trixie-backports, including main and non-free-firmware. Calamares 3.3.14 bootloader source explicitly invokes grub-install with --target=x86_64-efi or --target=i386-pc, confirming that preinstalled platform payloads satisfy its normal bootloader interface. Both facts still need functional VM verification.

## Partition configuration provenance

Neither inspected Debian package supplies a partition.conf. The complete upstream Calamares v3.3.14 default file is preserved in the overlay, including its CC0-1.0 notice, EFI mount point, swap choices, filesystem and initial selection. Source: https://github.com/calamares/calamares/blob/v3.3.14/src/modules/partition/partition.conf . Only `allowManualPartitioning: true` and `enableLuksAutomatedPartitioning: false` are explicitly changed. The latter is the actual key read by PartitionViewStep.cpp in that version; an `allowEncrypt` option does not exist. This hides automatic encryption, while native manual partition editing can still offer encryption. Manual encrypted installation is unsupported in Rilex 0.1 and must not be selected. Disabling the entire manual workflow would remove required installation functionality.
