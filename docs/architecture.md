# Architecture
Rilex 0.1 targets Debian 13 Trixie amd64 with the Debian kernel and systemd.
Normal packages come from official Trixie, Trixie updates and security archives;
Hyprland and required ecosystem dependencies come from official Trixie backports.
APT retains signature checks and Debian archive keys. Testing and Unstable are
not configured. Backports receive a targeted preference, not a base upgrade.

live-build creates a hybrid BIOS/UEFI live ISO. A locally built Debian package
owns Rilex defaults and utilities. Calamares uses Debian's installation sequence
and bootloader helpers with independently authored Rilex branding. Installer
correctness is a release gate, not inferred from a successful ISO build.

Hyprland handles tiling and XWayland compatibility; Waybar, Fuzzel, Foot, Mako,
PipeWire/WirePlumber, NetworkManager and BlueZ provide desktop services.
GTK portal handles file selection and Hyprland portal handles screencasting.
System defaults live under /etc/xdg and /usr/share/rilex; home configuration has
precedence. User changes must never be overwritten by a login script.

Rilex differs from Debian by providing this integrated keyboard desktop,
branding, welcome utility and release recipe. It shares Omarchy's preference
for keyboard workflows but does not depend on Omarchy code or infrastructure.

Secure Boot and full-disk encryption are not claimed until separately tested.
