# Rilex 0.1 User Guide

**Installation, keyboard workflows, customization, and maintenance**  
Edition: 11 October 2026. Audience: users with basic Linux experience.

Rilex is an independent Debian 13 Trixie distribution for x86-64 computers. It combines Debian's package ecosystem with a Hyprland tiling desktop, Waybar, the Fuzzel application launcher, and the Foot terminal. Its guiding principle is: **a Linux desktop built for people who prefer keyboards to mice.**

This guide describes the published **v0.1.0** release. Rilex is not affiliated with Debian or Omarchy, and does not require Omarchy. Its original branding and defaults are independently maintained. Debian and other upstream software retain their own licenses.

The release has passed virtual-machine live boot, UEFI installation, independent installed-system boot, normal-user login, and signed APT metadata refresh. This is a first release for careful testing, preferably on a spare laptop. A successful live boot on your own machine is useful evidence, but does not establish that installation, suspend, or every peripheral will work.

## Contents

1. [Understand the desktop](#1-understand-the-desktop)
2. [Prepare for installation](#2-prepare-for-installation)
3. [Download and verify the image](#3-download-and-verify-the-image)
4. [Create and boot a USB drive](#4-create-and-boot-a-usb-drive)
5. [Evaluate the live session](#5-evaluate-the-live-session)
6. [Install with Calamares](#6-install-with-calamares)
7. [First login and the Welcome utility](#7-first-login-and-the-welcome-utility)
8. [Learn the keyboard workflow](#8-learn-the-keyboard-workflow)
9. [Use the terminal, files, and applications](#9-use-the-terminal-files-and-applications)
10. [Networking, audio, and laptop controls](#10-networking-audio-and-laptop-controls)
11. [Clipboard, screenshots, and screen sharing](#11-clipboard-screenshots-and-screen-sharing)
12. [Customize without losing your changes](#12-customize-without-losing-your-changes)
13. [Install software and develop projects](#13-install-software-and-develop-projects)
14. [Update and maintain the system](#14-update-and-maintain-the-system)
15. [Protect your data and account](#15-protect-your-data-and-account)
16. [Troubleshoot and recover](#16-troubleshoot-and-recover)
17. [Know what has been tested](#17-know-what-has-been-tested)
18. [Quick reference and further reading](#18-quick-reference-and-further-reading)

## 1. Understand the desktop

Hyprland arranges ordinary windows into tiles. Opening a second terminal normally divides the available space instead of stacking one window over another. You choose which window has keyboard focus, which workspace contains it, and how the tiles are arranged. Dialogs and some applications may float above the tiles.

The default layout is **dwindle**, a recursively divided arrangement. Waybar displays workspace and system information. Fuzzel searches installed application launchers. Foot runs Bash by default. Thunar provides a graphical file manager; Ranger provides a terminal alternative. Firefox ESR is the default browser, and Mousepad is the graphical text editor.

The desktop uses Wayland, with XWayland available for traditional X11 applications. PipeWire and WirePlumber handle audio. NetworkManager handles networking, BlueZ handles Bluetooth, and Mako displays notifications. Swaybg draws the wallpaper; its name does not mean that Rilex uses the Sway compositor.

Rilex's defaults use a charcoal background, muted blue accents, readable fonts, and disabled compositor animations. Focus does not follow the mouse automatically. This makes keyboard focus predictable when you move the pointer out of the way.

**Super** means the Windows-logo key on a PC keyboard, or the Command key when the keyboard maps it as Super. In this guide, `Super + H` means hold Super and press H; it does not require Shift. Combinations explicitly containing Shift do require it.

## 2. Prepare for installation

Choose an x86-64 laptop or desktop. This release is not a native ARM or Apple Silicon operating system. A USB drive of at least 4 GB provides room for the approximately 1.65 GiB image; imaging will erase that drive. Leave ample internal disk space for your work, upgrades, and temporary files. Scientific datasets and development environments often occupy much more space than the base desktop.

Before making changes:

- Back up personal files to another device and test that you can read them there.
- Preserve any existing operating system's recovery media and recovery keys.
- Record the target disk's model, capacity, and existing partition layout.
- Connect AC power and have a reliable network connection available.
- Decide whether you can accept an unencrypted installation on this machine.
- Read the limitations below before selecting a partitioning method.

**The tested installation path is UEFI, automatic partitioning of an expendable disk, and an unencrypted filesystem.** Legacy BIOS live boot passed, but installed BIOS boot has not been verified. Manual partitioning, dual boot, and reuse of an existing EFI System Partition remain unverified.

Secure Boot is not verified; disable it for Rilex 0.1. Automatic encryption is disabled, and any encryption options still visible in manual partition dialogs are unsupported. If full-disk encryption is a requirement, do not proceed with this release's supported installation path. A login password does not encrypt an unencrypted disk.

For a first test, use a spare machine whose internal disk can be erased. Installing alongside an important existing OS introduces risks beyond the tested path. A backup is necessary even when a partitioning screen appears to preserve existing data.

## 3. Download and verify the image

Download from the [official Rilex v0.1.0 release](https://github.com/thepeteriley/rilex/releases/tag/v0.1.0):

- `rilex-0.1-amd64.iso`
- `rilex-0.1-amd64.iso.sha256`

The published image is **1,773,174,784 bytes**. Its SHA-256 is:

```text
0ecd67abaabd1d796619f98ba59b1b1f7d2c90f262be4ece5e2bee5fca65235e
```

Keep both files in the same download directory. On Linux:

```sh
sha256sum -c rilex-0.1-amd64.iso.sha256
```

Expect an `OK` result. On macOS:

```sh
shasum -a 256 rilex-0.1-amd64.iso
```

On Windows, in PowerShell:

```powershell
Get-FileHash .\rilex-0.1-amd64.iso -Algorithm SHA256
```

Compare the complete hash, not just its beginning or end. Stop if it differs. A checksum detects a damaged or changed download; it does not independently authenticate its publisher if obtained from the same compromised source.

The release also includes build attestations. With a current GitHub CLI and the downloaded ISO attestation bundle, you can verify provenance:

```sh
gh attestation verify rilex-0.1-amd64.iso \
  --bundle rilex-0.1-amd64.iso.intoto.jsonl \
  -R thepeteriley/rilex \
  --signer-workflow thepeteriley/rilex/.github/workflows/build.yml
```

Local bundle verification was tested without GitHub authentication using CLI 2.97.0. Debian 13's packaged CLI 2.46.0 lacks this command. You may perform verification on another trusted computer before copying the files. Do not add unsuitable package repositories merely to obtain this optional tool. An attestation verifies build origin and integrity, not hardware compatibility.

## 4. Create and boot a USB drive

Use an image writer that supports hybrid Linux ISO images. Select the ISO and the **entire USB device**, then confirm the device model and capacity before writing. Copying the ISO file into a USB filesystem does not create bootable media. The write operation destroys the USB's previous contents.

### Linux

A graphical image writer is a reasonable first choice. For a command-line workflow, inspect devices before and after inserting the USB:

```sh
lsblk -o NAME,SIZE,MODEL,TYPE,FSTYPE,MOUNTPOINTS
```

Unmount the USB's mounted partitions using your file manager or `umount`, then image the whole device. The following destination is a placeholder; replace it only after identifying your USB:

```sh
sudo dd if=rilex-0.1-amd64.iso of=/dev/USB_DEVICE \
  bs=4M status=progress conv=fsync
```

Do not use a partition such as `/dev/sdb1` as the destination. Do not guess that `/dev/sdb` is always the USB. Wait for the command to finish and safely eject the device.

### macOS

Use a compatible graphical image writer, or inspect devices with:

```sh
diskutil list external physical
```

For the command-line method, replace `N` below with the confirmed USB disk number. These examples intentionally contain placeholders:

```sh
diskutil unmountDisk /dev/diskN
sudo dd if=rilex-0.1-amd64.iso of=/dev/rdiskN bs=4m
diskutil eject /dev/diskN
```

Run the eject command only after `dd` has completed successfully. macOS `dd` may not display continuous progress; Ctrl+T requests a status report. If macOS blocks raw-device access, use an appropriately authorized terminal or image writer. A disk number from an earlier session can change after reconnection.

### Windows

Rufus can write the image. Choose the correct USB and ISO; when offered a choice for this hybrid image, use **DD image mode**. Complete the write and safely remove the drive. The [Debian USB-image FAQ](https://www.debian.org/CD/faq/#write-usb) explains hybrid imaging; the [Rufus FAQ](https://github.com/pbatard/rufus/wiki/FAQ#why-doesnt-rufus-recommend-dd-mode-over-iso-mode-for-isohybrid-images-surely-dd-is-better) explains its imaging modes.

### Boot the laptop

Insert the USB, open the computer's firmware boot menu, and choose its UEFI USB entry where available. Boot-menu keys vary by manufacturer. Select the live boot entry and allow the desktop to start. Do not launch installation until you have evaluated the live session.

## 5. Evaluate the live session

The live system lets you explore Rilex without installing it. Ordinary changes in the live environment are temporary; do not assume that preferences, downloaded files, or passwords survive reboot. Save anything important to a separate location. Accessing an internal filesystem from the live desktop can still change its contents if you deliberately write to it.

Start with this checklist:

1. Press `Super + Enter` and confirm that Foot opens.
2. Press `Super + Space`, search for Firefox, and launch it.
3. Open two terminals and try `Super + H/L`, `Super + V`, and `Super + F`.
4. Open Welcome with `Super + W`; use its network option to connect.
5. Open `pavucontrol` from the launcher and test speakers and microphone.
6. Test brightness and volume keys, the keyboard, and the touchpad.
7. Test removable storage and safely eject it after use.
8. Connect any external display you expect to use.
9. Save work, then evaluate suspend/resume if you intend to depend on it.

Screen locking is deliberately disabled for the live account because the image contains no reusable login password. `Super + Escape` displays a notice there. This does not test installed-account locking.

To identify the firmware boot mode in a terminal:

```sh
if [ -d /sys/firmware/efi ]; then
  echo "Booted in UEFI mode"
else
  echo "Booted in BIOS mode"
fi
```

Prefer UEFI for installation because that is the verified installed-boot path. If a required hardware function fails in the live system, investigate before replacing the current operating system.

## 6. Install with Calamares

Open the application launcher with `Super + Space`, search for **Install Rilex**, and start it. Calamares provides the graphical installation workflow. Keep AC power connected throughout.

### Language, location, and keyboard

Choose your language, time zone, and keyboard layout. Use any keyboard test field to verify punctuation and characters needed for your password. Rilex's Hyprland default explicitly specifies a US keyboard layout; choosing another installer layout may also require a desktop override after installation, as described in section 12.

### Partitioning

For the supported first-test path, select the disposable internal disk and automatic partitioning. Confirm its model and capacity. **Automatic partitioning erases the selected disk.** The USB drive and other attached disks may also appear in the device list, so do not rely on list order.

Manual partitioning is available in the installer but remains unverified for this release. If preserving another OS, understand each partition's role and do not format partitions whose data must remain. In UEFI installations, an existing EFI System Partition is normally mounted at `/boot/efi`; formatting it can remove another OS's boot files. This guide does not certify that dual-boot path. Do not enable encryption in any partitioning dialog for version 0.1.

### Account and hostname

Create your own user account and a strong, memorable password. Choose a useful hostname for the machine. Keep the password private; it will be used for login, administrative authorization, and installed-session locking. The installed system should use this account rather than the passwordless live identity.

### Final review

Read the installation summary. Check the disk, partitions to be formatted, bootloader target, account, and time zone. Proceed only when the destructive operations match your intention. Let Calamares finish; interrupting a disk write can leave an incomplete installation.

If installation fails, preserve the error and logs before rebooting. The live user's `~/.cache/calamares/session.log` is a common location; also check `/var/log/Calamares.log` if present. Do not repeatedly change partition settings at random in an attempt to clear the error.

### First boot from the installed disk

Reboot when installation completes and remove the USB when appropriate. Confirm that the machine starts with the USB disconnected. At the SDDM login screen, select **Rilex (Hyprland)** if a session choice is offered, and log in with your new account.

Confirm network access, then run:

```sh
sudo apt update
```

Also test `Super + Escape` and unlock with your password. Independent disk boot, normal-user login, working APT metadata, and lock/unlock are useful first-install acceptance checks. Keep your backup and installation USB until you are satisfied with the installed system.

## 7. First login and the Welcome utility

Rilex Welcome opens once on first desktop startup. You can reopen it any time with `Super + W` or by running `rilex-welcome` in a terminal. It is a keyboard-driven terminal menu: enter a number and press Enter. Return from subprograms to continue using the menu.

| Choice | What it does |
| --- | --- |
| 1 | Opens the searchable keyboard shortcut reference. |
| 2 | Starts `nmtui` for network connections. |
| 3 | Starts the Bluetooth manager. |
| 4 | Refreshes Debian package metadata and offers package upgrades. |
| 5 | Changes wallpaper and dark/light GTK application preferences. |
| 6 | Opens your Foot configuration in Nano. |
| 7 | Displays OS, kernel, Hyprland, and memory information. |
| 8 | Lets you select and read bundled local documentation. |
| 9 | Explains APT, Python environments, and optional development tools. |
| 0 | Closes Welcome. |

The update option uses `sudo`; read its output and package proposal before confirming. In local documentation, type to filter the file list, press Enter to open a document, and use `q` to leave the pager. Escape cancels selection.

The published ISO contains documentation from its build. This expanded guide was written after release publication, so keep a downloaded copy for offline use or consult the [current guide on GitHub](https://github.com/thepeteriley/rilex/blob/main/docs/user-guide.md).

## 8. Learn the keyboard workflow

Learn a small set of keys first: terminal, launcher, focus, close, and workspaces. Add moving and resizing once those are comfortable. Keep `Super + /` in memory: it opens a searchable reference, so you do not have to memorize everything immediately.

### Launch and close applications

`Super + Enter` opens Foot. `Super + Space` opens Fuzzel; type part of an application name, use the arrow keys to choose a match, and press Enter. Escape dismisses the launcher. `Super + B` opens Firefox ESR, and `Super + E` opens Thunar.

`Super + Q` requests that the focused window close. Save changes first and respond to any application confirmation. It does not log out of the desktop.

### Focus, move, and resize

The directional keys follow the vi convention:

| Direction | Focus | Move window | Resize |
| --- | --- | --- | --- |
| Left | Super + H | Super + Shift + H | Super + Ctrl + H |
| Down | Super + J | Super + Shift + J | Super + Ctrl + J |
| Up | Super + K | Super + Shift + K | Super + Ctrl + K |
| Right | Super + L | Super + Shift + L | Super + Ctrl + L |

Focus selects the window receiving keyboard input; moving changes its position in the layout. Resizing adjusts width or height in small increments and repeats while held. Tiled resizing is constrained by the layout and available space, so it may behave differently from resizing a floating window.

`Super + V` toggles floating. It is useful for a small utility or dialog that does not fit comfortably into a tile. `Super + F` toggles fullscreen. Press the same combination again to return. `Super + Shift + Space` toggles an applicable dwindle split's orientation; it does not switch to a different compositor or a different layout family. Try it with multiple tiled windows.

Mouse support remains available: Super plus left-button drag moves a window, and Super plus right-button drag resizes it. Keyboard-first does not require refusing the pointer when an application needs it.

### Organize workspaces

`Super + 1` through `Super + 9` switch workspaces. `Super + Shift + 1` through `Super + Shift + 9` move the focused window to the corresponding workspace; the default move follows the window. Workspaces organize windows, not files, and do not automatically save application state.

Use a simple convention, such as 1 for terminals and code, 2 for the browser, and 3 for documents. A repeatable arrangement reduces the need to search for windows. Empty workspaces may disappear from the bar and be recreated when selected.

With multiple monitors, `Super + Ctrl + Shift + H/L` moves the current workspace to the previous/next monitor. Monitor ordering is not necessarily the same as physical left/right placement. This command needs another active output; physical multi-monitor behavior still requires testing on your hardware.

### A practical first session

1. Press `Super + 1`, then `Super + Enter` twice to open two terminals.
2. Use `Super + H/L` to select between them. Run a command in the focused one.
3. Try `Super + Shift + Space` to change the split, then resize with `Super + Ctrl + H/L`.
4. Open Firefox with `Super + B`. Move it to workspace 2 with `Super + Shift + 2`.
5. Return to the terminals with `Super + 1`; use `Super + 2` to revisit the browser.
6. Open `Super + /`, type a word such as `resize`, then press Escape when finished.

The shortcut reference is a reference menu: selecting a line does not execute that action. Try unfamiliar actions on expendable windows before using them during important work.

## 9. Use the terminal, files, and applications

Foot is a lightweight terminal, not a shell. Bash interprets commands inside it. Use ordinary Linux tools and prefer project directories under your home directory for work that does not need administrative privileges.

In Foot, `Ctrl + Shift + C` copies selected text and `Ctrl + Shift + V` pastes. `Ctrl + C` normally interrupts the foreground command instead. `Ctrl + Shift + R` searches terminal scrollback; Shift+PageUp/PageDown scroll it. These are terminal shortcuts, separate from Super-based desktop controls. Review pasted commands before pressing Enter, especially commands using `sudo`. See the [Foot configuration manual](https://manpages.debian.org/trixie/foot/foot.ini.5.en.html).

Useful tools already included are Git, tmux, Neovim, Nano, btop, ripgrep, fzf, jq, curl, wget, unzip, and the OpenSSH client. Debian calls the `fd` executable **`fdfind`**; use that name unless you deliberately create an alias.

```sh
mkdir -p ~/projects
cd ~/projects
rg --files
fdfind '\.py$' .
```

The last commands list files and search for Python filenames when there are files to search. They do not create a sample project. In terminal applications, use that application's exit keys: `q` for many pagers, Ctrl+X for Nano, and `:q` in Neovim when changes do not need saving. `Super + Q` closes the whole terminal window, potentially interrupting running work.

Use tmux for long-running interactive work, especially remote sessions. Detaching a tmux session is different from shutting down the machine: a local process will not survive a reboot merely because it ran in tmux.

Open Thunar with `Super + E` for graphical browsing and removable drives. Run `ranger` in Foot for terminal navigation. Keep data under recognizable locations such as Documents, Pictures, and `~/projects`; avoid doing routine work in `/root` or system directories. Use `sudo` for a specific administrative command rather than running an entire desktop application as root.

Use the file manager's unmount/eject action before removing USB storage, particularly after writing large files. Wait for writes to complete. An installation image on a USB is not a suitable place for your only backup.

Rilex includes a Wayland desktop with XWayland compatibility, rather than a full GNOME or KDE settings suite. Use Welcome and the individual network, audio, Bluetooth, and configuration tools described here. Some older applications may use X11 through XWayland; compatibility should be checked application by application.

## 10. Networking, audio, and laptop controls

### Wi-Fi and wired connections

Open Welcome option 2 or run `nmtui`. Choose **Activate a connection**, select your network, and enter its credentials locally. Wired connections are normally managed by NetworkManager too. For diagnosis:

```sh
nmcli device status
nmcli connection show --active
nmcli radio wifi
```

These commands report devices, active connections, and the Wi-Fi radio state. If the radio is disabled, `nmcli radio wifi on` enables it; a physical switch or firmware restriction may still prevent use. A connection does not guarantee DNS or internet access. Test browsing and `sudo apt update` rather than relying only on a bar icon.

### Bluetooth

Open Welcome option 3 or launch `blueman-manager`. Enable Bluetooth, put your own device into pairing mode, search for it, and pair with the intended device. Compare any displayed pairing codes. Connect it and test the function you need, such as headphone playback or keyboard input. Pairing alone does not prove that the device's audio profile or microphone works.

### Speakers, headphones, and microphones

Open `pavucontrol` from the launcher. Select the intended output, input, and device profile; its playback and recording tabs help route individual applications. Start playback or recording while adjusting the relevant stream.

```sh
wpctl status
```

This shows PipeWire devices and streams. Volume keys adjust the default output; the microphone mute key toggles the default input when the keyboard exposes that key. Verify the microphone selection inside conferencing applications as well. Bluetooth headset and high-quality playback modes can have different capabilities.

### Brightness, power, and suspend

Brightness keys use `brightnessctl`; support depends on the laptop's backlight interface. Inspect available devices with `brightnessctl --list` if they do not behave as expected. Do not assume that external monitor brightness is controlled in the same way.

**Automatic idle locking and automatic lock-before-suspend are not configured in Rilex 0.1.** Lock explicitly with `Super + Escape` and confirm that the lock screen appears before leaving the installed machine. Test password unlock before relying on it.

Lid-close behavior and suspend/resume are hardware-dependent. If you use lid-close suspend, first lock and verify the screen, then test a lid-close/resume cycle on AC power with no unsaved work. Do not assume that a suspended machine is locked. Test these behaviors again after relevant graphics, firmware, or kernel changes.

For a deliberate shutdown or reboot, save work first and use:

```sh
systemctl poweroff
# Or, when you intend to restart:
systemctl reboot
```

These end your session and running applications. Suspend is not a substitute for saving work or maintaining backups.

## 11. Clipboard, screenshots, and screen sharing

### Clipboard history

`Super + C` opens the clipboard-history selector. Type to filter, select a stored item, and press Enter to place it back on the clipboard. Paste using the destination application's normal shortcut or menu. History includes text and images and persists in your user's cache.

Avoid copying secrets unnecessarily. To clear saved history:

```sh
cliphist wipe
```

This clears history, not necessarily the current clipboard or data retained by another application. To clear the current Wayland clipboard as well:

```sh
wl-copy --clear
```

These actions are not a secure-erasure guarantee. Password managers and applications may have their own clipboard policies. See the [Debian wl-clipboard manual](https://manpages.debian.org/trixie/wl-clipboard/wl-copy.1.en.html) for command behavior.

### Screenshots

`Super + Shift + S` starts region selection. Drag the region with the pointer; Escape cancels. The screenshot is saved under your Pictures directory's `Screenshots` subdirectory with a timestamped filename and copied to the clipboard.

The region tool uses a pointer despite the desktop's keyboard emphasis. For a whole-desktop screenshot from the terminal:

```sh
pictures=$(xdg-user-dir PICTURES)
grim "$pictures/desktop.png"
```

This example overwrites `desktop.png` if it already exists; change the filename when keeping several captures. Review screenshots for private information before sharing them.

### File dialogs and screen sharing

Rilex includes the Hyprland and GTK XDG desktop portals. They provide screen-capture authorization and file-selection integration for applications that use portals. XWayland support alone does not provide Wayland screen sharing.

When an application requests capture, choose the intended display in the portal dialog and explicitly authorize it. Rilex's tests verified GTK file selection and actual portal-authorized PipeWire capture buffers in a VM. Browser conferencing, camera access, capture performance, and your particular meeting service have not been verified. Test a private call before relying on the system for a meeting.

If sharing fails, check the application permissions and logs before installing another portal backend. Competing portal configurations can make selection unpredictable. A logout/login can restore a clean session environment after configuration changes; it also stops active sharing and applications.

## 12. Customize without losing your changes

Use **user-owned configuration** for personal changes. Editing vendor files under `/etc/rilex` or `/etc/xdg` makes future package upgrades harder to review. Keep small changes, make a backup first, and change one thing at a time.

### Hyprland: use Lua overrides

This release uses **Hyprland 0.55's Lua configuration**, not the older `hyprland.conf` format. The Rilex session loads `/etc/xdg/hypr/hyprland.lua` and then, if present, your `~/.config/hypr/user.lua`. Instructions written for older Hyprland releases may be incompatible.

```sh
mkdir -p ~/.config/hypr
nano ~/.config/hypr/user.lua
```

If the file already exists, preserve a copy before editing. For example, to keep a US layout but disable natural scrolling:

```lua
hl.config({
  input = {
    kb_layout = "us",
    touchpad = { natural_scroll = false }
  }
})
```

Choose an appropriate XKB layout identifier instead of `us` if needed; the installer keyboard choice does not remove Rilex's explicit compositor default. Check punctuation, modifiers, and password entry afterward.

An unused shortcut can launch an application:

```lua
hl.bind("SUPER + SHIFT + E", hl.dsp.exec_cmd("mousepad"))
```

Check the default bindings before adding one. Do not assume that adding a duplicate key cleanly replaces an existing action. Use documentation for the installed version and review configuration errors.

Reload and inspect from a terminal inside the running desktop:

```sh
hyprctl reload
hyprctl configerrors
```

An empty configuration-error result is useful, but also test the changed behavior. Environment or startup changes may require logout/login. Keep a working terminal open while experimenting. The [Hyprland 0.55 example](https://github.com/hyprwm/Hyprland/blob/v0.55.0/example/hyprland.lua) is a better starting point than an unversioned dotfile collection.

### Displays and scaling

Defaults choose preferred modes, automatic placement, and automatic scaling. Inspect actual output names:

```sh
hyprctl monitors
```

For a particular display, add a monitor rule to `user.lua`, replacing the example name with the output shown on your machine:

```lua
hl.monitor({
  output = "eDP-1",
  mode = "preferred",
  position = "auto",
  scale = 1.5
})
```

Reload and check text readability, pointer alignment, and applications before keeping the change. Fractional scaling may look different in XWayland applications. Physical HiDPI and hotplug behavior remain hardware validation items. Prefer a small output-specific override to replacing the whole default configuration.

### Wallpaper and application theme

Welcome option 5 accepts an **absolute path** to an existing image, such as `/home/yourname/Pictures/wallpaper.png`. A blank path restores the original wallpaper. Keep the image in a stable location. The choice is stored in `~/.config/rilex/wallpaper`.

The same option selects dark or light GTK application preferences. Restart applications to apply file-based preferences. This changes GTK appearance; it does not recolor every Qt application, Waybar, the terminal, or Hyprland's borders. Those have separate configuration.

### Terminal, launcher, bar, and notifications

| Component | Vendor default | Personal override |
| --- | --- | --- |
| Foot | `/etc/rilex/foot/foot.ini` | `~/.config/foot/foot.ini` |
| Fuzzel | `/etc/rilex/fuzzel/fuzzel.ini` | `~/.config/fuzzel/fuzzel.ini` |
| Waybar layout | `/etc/rilex/waybar/config` | `~/.config/waybar/config` or `config.jsonc` |
| Waybar style | `/etc/rilex/waybar/style.css` | `~/.config/waybar/style.css` |
| Mako | `/etc/xdg/mako/config` | `~/.config/mako/config` |

Welcome option 6 creates a personal Foot configuration if absent and edits it with Nano. New terminals use it. For other components, create their personal directory and copy the vendor file only if you do not already have an override; then edit your copy. Waybar prefers `config` over `config.jsonc` if both exist.

Use `rilex-terminal`, `rilex-launcher`, and `rilex-bar` when launching these components manually; the wrappers select personal files or the correct Rilex defaults. A copied configuration is a complete personal copy: later vendor updates will not automatically merge improvements into it. Compare it with new defaults when upgrading.

After editing Waybar, you can restart only your bar:

```sh
pkill -u "$(id -u)" -x waybar
rilex-bar &
```

A missing bar does not prevent the main keyboard bindings from working. Do not rerun the entire `rilex-session-start` helper as a general repair command; it starts several session components and clipboard watchers.

## 13. Install software and develop projects

### Debian packages

Use APT for system software:

```sh
apt search PACKAGE_NAME
apt show PACKAGE_NAME
sudo apt install PACKAGE_NAME
```

`PACKAGE_NAME` is a placeholder. Read the package description and proposed dependencies before installing. The default image already includes Python 3, pipx, Python virtual-environment support, GCC/build-essential, Make, CMake, and GDB. It intentionally omits heavyweight IDEs.

Optional tools documented by Welcome include:

```sh
sudo apt install gfortran r-base valgrind
```

Install these only when useful for your work. You can add a preferred editor through an appropriate supported delivery method; its packaging and trust policy are separate from the base desktop.

### Python projects

Debian manages the system Python environment. Keep project packages in a virtual environment, and Python command-line applications in pipx. Do not use `sudo pip` or bypass Debian's externally managed environment protection.

```sh
mkdir -p ~/projects/my-project
cd ~/projects/my-project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy scipy matplotlib
python -m pip freeze > requirements.txt
deactivate
```

The example installs packages from the configured Python package index into that project's environment. Review package trust and pin dependencies appropriately for reproducible scientific work. `requirements.txt` records this environment's installed versions; it is not by itself a complete experiment record. Keep code, inputs, processing steps, and relevant toolchain versions too.

For a command-line tool, pipx gives it a separate environment:

```sh
pipx install ruff
pipx ensurepath
```

Log out and back in if the added executable directory is not yet on your PATH. See the [externally managed environment specification](https://packaging.python.org/en/latest/specifications/externally-managed-environments/) and [pipx documentation](https://pipx.pypa.io/stable/explanation/how-pipx-works.html).

### General development habits

Use Git for project source and selected non-secret configuration. Exclude environments, build products, large datasets, access tokens, and private keys. Record enough information to recreate the environment rather than committing binaries unnecessarily.

Compile and run development projects as your normal user. Grant administrative access only for a reviewed installation step. The OpenSSH **client** is included; this does not imply that an SSH server is enabled or listening on the laptop.

## 14. Update and maintain the system

### Routine Debian updates

Update regularly, particularly before installing new software:

```sh
sudo apt update
apt list --upgradable
sudo apt upgrade
```

Read the proposal and any errors. `upgrade` does not remove installed packages; `full-upgrade` may. If an upgrade needs more substantial dependency changes, inspect a simulation first:

```sh
apt -s full-upgrade
```

Do not approve removal of the desktop, network, kernel, or bootloader components merely to clear a dependency error. Likewise, review `apt -s autoremove` before deciding whether to remove unused dependencies. Keep a known-working kernel until a replacement has booted successfully. See the [Debian APT manual](https://manpages.debian.org/trixie/apt/apt.8.en.html).

Reboot after a kernel update when convenient and safe. Save work and keep AC power attached during important system changes. Check free space with `df -h`; low disk space can interrupt downloads, package installation, and user applications.

### Stable and backports

Rilex uses signed Debian Trixie, security, updates, and official Trixie backports repositories. Hyprland and selected companion packages come from backports because they are not supplied by the Stable base in the required form. Testing and Unstable repositories are not enabled.

Backports have a different support and testing model from Stable: support is on a best-effort basis, and packages are rebuilt for Stable from newer Debian sources. Do not describe their security coverage as identical to Stable. Keep backports selective; do not move the whole system to them or mix in arbitrary Testing, Unstable, or Ubuntu repositories. See [Debian's backports instructions](https://backports.debian.org/Instructions/).

Inspect installed and candidate versions with:

```sh
apt policy hyprland
```

Never disable signature checks or TLS verification to make an update succeed. When APT fails, check the actual error, connectivity, clock, disk space, and repository configuration.

### Rilex defaults updates

Version 0.1 has **no hosted Rilex APT repository**. Debian updates do not automatically deliver a new Rilex defaults package. There is no remote installation script that you need to rerun.

For a deliberately chosen release package, download its `.deb` and matching attestation bundle from the official release, verify provenance with a compatible GitHub CLI, then install the local package with APT. The current release example is:

```sh
gh attestation verify rilex-defaults_0.1.0_all.deb \
  --bundle rilex-defaults_0.1.0_all.deb.intoto.jsonl \
  -R thepeteriley/rilex \
  --signer-workflow thepeteriley/rilex/.github/workflows/build.yml
sudo apt install ./rilex-defaults_0.1.0_all.deb
```

The current defaults are already included in an ordinary 0.1 installation; you do not need to reinstall them to begin using the desktop. Future releases must publish their own versions and verification information. Consult [Rilex update documentation](https://github.com/thepeteriley/rilex/blob/main/docs/updates.md) rather than assuming that release infrastructure has been added.

## 15. Protect your data and account

Maintain a backup on a separate device or service. Include personal documents, project source, irreplaceable datasets, and carefully selected configuration. Test restoration of a few files. An archive kept only on the laptop is convenient for undoing an edit, but is not protection against disk failure, theft, or an installation mistake.

Record installed packages and important environment versions so you can rebuild the machine. For example:

```sh
dpkg-query -W > ~/rilex-package-list.txt
```

Move a copy of that inventory into your backup. Keep private keys, tokens, password-manager data, and any configuration containing secrets out of public repositories and support attachments. Use an appropriately protected backup destination.

Lock the installed desktop explicitly when stepping away. Do not treat an unencrypted laptop as safe against physical access simply because its login has a password. If it will hold sensitive research, customer information, or credentials and encryption is mandatory, choose a supported encrypted system until Rilex has verified that installation path.

Before an important upgrade, preserve relevant user configuration and a known-working boot option. Keep the installation USB available as recovery media, but remember that this live environment has no reusable lock password. Close sensitive sessions and protect the physical machine when using it.

## 16. Troubleshoot and recover

### Collect facts before changing things

Inside a working desktop terminal:

```sh
cat /etc/os-release
uname -r
hyprctl version
hyprctl configerrors
systemctl --failed
systemctl --user --failed
```

These establish the OS, kernel, compositor, and failed services. `hyprctl` expects access to your running Hyprland session; do not interpret its failure from an unrelated console or root shell as proof that the compositor is broken.

Use logs to investigate:

```sh
journalctl -b -u sddm
journalctl --user -b
```

Use `q` to leave the pager. Review logs before sharing them; they can contain usernames, hostnames, network details, and application information.

### A configuration change breaks the desktop

If a terminal still works, restore the last good `user.lua`, reload, and inspect errors. If graphical login fails, use `Ctrl + Alt + F3` to try a text console and log in as your normal user. Disable your override without deleting it:

```sh
mv ~/.config/hypr/user.lua \
  ~/.config/hypr/user.lua.disabled-$(date +%Y%m%d-%H%M%S)
```

Do this only if that file exists. Return to the graphical login and start the Rilex session again; the graphical console key varies by system. Preserve the disabled file for diagnosis. Restarting SDDM terminates graphical sessions, so do not do it while they contain unsaved work.

### The bar or launcher is missing

Try `Super + Enter`; the compositor's bindings can still work without Waybar. Run `rilex-bar` or `rilex-launcher` in that terminal and read errors. Check recent personal configuration changes before reinstalling packages. Avoid starting several copies of the bar.

### Network or APT problems

Check `nmcli device status`, active connections, and whether browsing works. Read the APT error: DNS failure, unavailable metadata, signature errors, and insufficient disk space require different fixes. Inspect `timedatectl status` if clock-related failures appear. Do not disable verification or switch to an untrusted mirror as a workaround.

### No sound or wrong microphone

Run `wpctl status` and open `pavucontrol`. Check output/input choice, mute state, profile, and the application's own device selection. Relevant user-service status:

```sh
systemctl --user status pipewire wireplumber
```

An application may have selected a different device from the desktop default. Try a simple local playback or recording test before diagnosing an entire conferencing setup.

### Portal or screen-sharing failures

Inspect the portal services:

```sh
systemctl --user status xdg-desktop-portal \
  xdg-desktop-portal-hyprland xdg-desktop-portal-gtk
```

Some services are activated on demand, so inactivity before a request is not automatically a failure. Check logs around an actual request, ensure you logged into the Rilex session, and try a clean logout/login after saving work. Do not remove or replace portal packages blindly.

### Installation or boot failure

Keep installer logs before restarting. If the installed machine cannot boot, use the live USB to inspect the situation and preserve data; do not run generic partitioning or bootloader repair commands against a guessed disk. Record whether installation was UEFI or BIOS and whether manual partitioning or encryption was attempted. Those distinctions determine whether you followed the tested path.

### Ask for help effectively

Report the Rilex release, hardware model, exact symptom, steps to reproduce, what changed, and relevant logs or screenshots. Include whether the problem occurs in the live session, after installation, or both. State which tests you actually ran. Never post passwords, private keys, tokens, or an unrestricted copy of your home directory.

## 17. Know what has been tested

The release evidence is published in the [Rilex 0.1 test report](https://github.com/thepeteriley/rilex/blob/main/docs/release-0.1.md) and [testing documentation](https://github.com/thepeteriley/rilex/blob/main/docs/testing.md). The final ISO source revision is:

```text
5efe9878386ae51e884ad391ea0045e19a519c66
```

| Capability | Release evidence or limitation |
| --- | --- |
| UEFI and BIOS live boot | Passed in QEMU. |
| UEFI graphical installation | Calamares completed on a disposable virtual disk. |
| Independent installed boot | Passed without the ISO attached. |
| Normal-user login | Password login passed in the installed VM. |
| Hyprland, Waybar, Foot | Ran in live and installed VM sessions. |
| Fuzzel application launch | Actual terminal launch passed. |
| Keyboard defaults | Static binding checks and runtime action tests passed. |
| Networking and audio services | Initialized; signed APT metadata refresh passed. |
| GTK portal file selection | Actual file selection passed in component QA. |
| Portal screen capture | Authorized PipeWire buffers passed in component QA. |
| Installed-account locking | Password lock/unlock passed with the same lock configuration. |
| Physical laptop devices | Must be validated on your own hardware. |
| Installed BIOS, manual partitioning, EFI reuse | Unverified. |
| Secure Boot and encrypted installation | Unsupported for this release. |
| Browser conferencing and suspend/resume | Unverified on physical laptops. |
| Automatic idle/suspend locking | Not configured. |

Expanded keyboard and portal tests used a preceding installed candidate with unchanged desktop configuration and component versions. Final-image installation and boot were tested separately. A working service or successful component test is not a claim that every headset, webcam, browser, or display works.

The release's principal desktop versions are Hyprland 0.55.2, Waybar 0.12, Fuzzel 1.12, Foot 1.21, and Calamares 3.3.14. APT upgrades can change installed versions. Check your machine rather than assuming its state is identical to the original image.

## 18. Quick reference and further reading

### Desktop shortcuts

| Shortcut | Action |
| --- | --- |
| Super + Enter | Open Foot terminal. |
| Super + Space | Search applications in Fuzzel. |
| Super + Q | Close focused window. |
| Super + 1-9 | Switch workspace. |
| Super + Shift + 1-9 | Move window to workspace and follow it. |
| Super + H/J/K/L | Focus left/down/up/right. |
| Super + Shift + H/J/K/L | Move window left/down/up/right. |
| Super + Ctrl + H/J/K/L | Resize window. |
| Super + Ctrl + Shift + H/L | Move workspace to previous/next monitor. |
| Super + F | Toggle fullscreen. |
| Super + V | Toggle floating. |
| Super + Shift + Space | Toggle applicable dwindle split orientation. |
| Super + E | Open Thunar. |
| Super + B | Open Firefox ESR. |
| Super + Shift + S | Select screenshot region; save and copy. |
| Super + Escape | Lock installed session with Hyprlock. |
| Super + / | Search shortcut reference. |
| Super + C | Select clipboard-history item. |
| Super + W | Open Rilex Welcome. |
| Volume / microphone keys | Adjust default audio device or mute. |
| Brightness keys | Adjust supported backlight. |

### Useful commands

| Task | Command |
| --- | --- |
| Network configuration | `nmtui` |
| Bluetooth configuration | `blueman-manager` |
| Audio configuration | `pavucontrol` |
| Audio device status | `wpctl status` |
| Display names and modes | `hyprctl monitors` |
| Reload personal compositor changes | `hyprctl reload` |
| Check compositor configuration | `hyprctl configerrors` |
| Clear clipboard history | `cliphist wipe` |
| List pending Debian updates | `apt list --upgradable` |
| Check disk space | `df -h` |
| Terminal file manager | `ranger` |
| Process/resource viewer | `btop` |

### Project documentation

- [Release downloads and attestations](https://github.com/thepeteriley/rilex/releases/tag/v0.1.0)
- [Installation instructions](https://github.com/thepeteriley/rilex/blob/main/docs/installation.md)
- [Desktop customization](https://github.com/thepeteriley/rilex/blob/main/docs/customization.md)
- [Updates and package verification](https://github.com/thepeteriley/rilex/blob/main/docs/updates.md)
- [Known issues](https://github.com/thepeteriley/rilex/blob/main/docs/known-issues.md)
- [Testing and release evidence](https://github.com/thepeteriley/rilex/blob/main/docs/testing.md)
- [Architecture and provenance](https://github.com/thepeteriley/rilex/blob/main/docs/architecture.md)
- [Build instructions](https://github.com/thepeteriley/rilex/blob/main/docs/building.md)

Rilex retains normal Debian package management and security updates while adding a curated keyboard-driven desktop and independent branding. Keep the base coherent, keep personal changes in user configuration, and test the hardware behaviors you rely on before making this first release your primary workstation.
