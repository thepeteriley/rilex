# Known issues and support boundary

Rilex is currently a development candidate. The authoritative passing and
pending gates are in [testing](testing.md) and [progress](progress.md).

- No release readiness is inferred from source checks or ISO assembly.
- Secure Boot is not verified. Use Secure Boot disabled for development tests.
- Automatic encryption is disabled. Manual partition dialogs may still offer
  encryption; that path is unsupported until a separate installation and boot
  test passes. Use an unencrypted disposable VM for the first release gate.
- Live-account locking is disabled because no reusable user password is embedded.
  Installed users can use Hyprlock with their chosen password.
- Idle locking and lock-before-suspend are not configured. Explicit Super+Escape
  is provided; suspend/resume remains a hardware validation item.
- Apple Silicon runs amd64 guests with QEMU TCG. Hardware virtualization cannot
  accelerate the different instruction set. CPU-rendered desktop testing may
  be slow or may need a different verified GPU/rendering environment.
- Wi-Fi firmware, Bluetooth pairing, microphones, brightness, removable storage,
  external monitors, HiDPI, screen sharing and suspend are unverified on physical
  laptops. Presence of packages does not prove a device works.
- No public Rilex APT archive/signing identity has been deployed. Debian's signed
  repositories provide the base and backports updates; Rilex defaults delivery
  is described in [updates](updates.md).
- The build process is repeatable, but evolving Debian security metadata means
  byte-identical rebuilds are not promised. Every final candidate must retain
  its source revision and package manifest.
