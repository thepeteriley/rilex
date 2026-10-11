# Rilex

A Linux desktop built for people who prefer keyboards to mice.

Rilex 0.1 is a Debian 13 Trixie amd64 distribution integrating Hyprland,
Waybar, Fuzzel and Foot with a restrained charcoal and blue desktop.
[Download v0.1.0](https://github.com/thepeteriley/rilex/releases/tag/v0.1.0):
a real hybrid ISO, checksum, package manifest and verified build attestations.

The image passed UEFI and BIOS live boot, graphical Calamares installation,
independent disk-only boot, normal password login and signed Debian APT refresh
in QEMU. Read the [release test report](docs/release-0.1.md) before installing.
Secure Boot, encryption and physical laptop compatibility remain unverified;
this first release is intended for careful testing on a spare machine.

Hyprland comes from official Debian Trixie backports. The base remains Stable;
Testing and Unstable are not used. Rilex is independently maintained and is not
affiliated with Debian or Omarchy.

Start with the complete [Rilex user guide](docs/user-guide.md), covering installation,
keyboard workflows, customization, maintenance and recovery.

See [build instructions](docs/building.md), [installation](docs/installation.md),
[keyboard shortcuts](docs/keyboard-shortcuts.md), [architecture](docs/architecture.md),
[updates](docs/updates.md), [testing](docs/testing.md), and [progress](docs/progress.md).

Original Rilex code and artwork use the MIT license. Bundled Debian software
retains its upstream licenses; see [provenance](LICENSES/README.md).
