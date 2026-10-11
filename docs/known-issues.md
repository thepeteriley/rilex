# Known issues and support boundary

Rilex 0.1 has passed VM live-boot, UEFI installation and independent normal-user
login/APT gates. The authoritative passing and unverified checks are in [testing](testing.md) and [progress](progress.md).

- Installed BIOS boot, manual partitioning and reuse of an existing EFI partition have not been tested.
- Secure Boot is not verified. Disable Secure Boot when booting this release.
- Automatic encryption is disabled. Manual partition dialogs may still offer
  encryption; that path is unsupported until a separate installation and boot
  test passes. Use an unencrypted installation for version 0.1.
- Live-account locking is disabled because no reusable user password is embedded.
  Installed users can use Hyprlock with their chosen password.
- Idle locking and lock-before-suspend are not configured. Explicit Super+Escape
  is provided; suspend/resume remains a hardware validation item.
- Apple Silicon runs amd64 guests with QEMU TCG. Hardware virtualization cannot
  accelerate the different instruction set. CPU-rendered desktop testing may
  be slow or may need a different verified GPU/rendering environment.
- Wi-Fi firmware, Bluetooth pairing, microphones, brightness, removable storage,
  external monitors, HiDPI, browser conferencing and suspend are unverified on physical
  laptops. Presence of packages does not prove a device works.
- GTK file selection and five portal-authorized PipeWire screen-capture buffers passed VM component tests; browser conferencing has not been tested. See [application QA](qa-applications.md).
- No public Rilex APT archive/signing identity has been deployed. Debian's signed
  repositories provide the base and backports updates; Rilex defaults delivery
  is described in [updates](updates.md).
- The build process is repeatable, but evolving Debian security metadata means
  byte-identical rebuilds are not promised. Every final candidate must retain
  its source revision and package manifest.
