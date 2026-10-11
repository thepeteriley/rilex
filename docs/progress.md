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
- [x] Configure Calamares; seven automated installer checks pass.
- [x] Build real hybrid ISO (two hosted candidates; release qualification pending).
- [x] Test final-image UEFI/BIOS live desktop.
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

## Resumed 2026-10-11

The VMs and build outputs survived the interrupted work. The local emulated
Debian build completed a real hybrid ISO from frozen 530981f plus the documented
identity hook overlay: 1,769,701,376 bytes, SHA-256
`437642510f6e79a67fe12f0a36bd1fbd6171702ae4f20639d9e0b1ed9dca5e6e`.
Its ISO structure passed; older desktop defects exclude it from release.

Corrected e7fd8e4 booted its unmodified desktop in QEMU 11.1.2 on macOS ARM64.
All 17 live-session assertions passed, including Hyprland, Waybar, signed-base
identity, NetworkManager, PipeWire/WirePlumber and both desktop portals.
Screenshot and output are under `.cache/qa-e7-uefi`. The ephemeral QA SSH
bootstrap changes only the disposable live overlay, not the desktop settings
or the ISO. These service checks do not establish laptop hardware support.

Hosted b252079 candidate run38078483245 completed. Both ISO and defaults
package attestations were cryptographically verified against the repository's
`build.yml` signer using `gh attestation verify`; embedded source provenance
now records its exact commit. Its ISO SHA-256 is
`847d08e15d16b7ace6debd1a041e67676e25b52c65d640a508d89a681df2e2ba`,
size 1,769,701,376 bytes. Structural boot checks passed.

The earlier diagnostic installer completed all 41 jobs on the disposable
32 GB virtual disk. Read-only target checks passed EFI GRUB, kernel/initrd,
normal sudo user, live-account cleanup and official APT sources. Independent
boot and normal-user login are being verified; this older diagnostic image
is not the release candidate. Unsupported media-APT jobs were removed after
checking that our ISO contains no Debian package archive. Final source
7d25250 is building in run38145470988; final-image installation remains a gate.

Actual screenshot selection on e7fd8e4 saved a PNG and copied `image/png`.
It also exposed missing first-login XDG folder initialization: the fallback
was `$HOME/Screenshots` instead of the documented Pictures folder. The session
now runs Debian's installed `xdg-user-dirs-update`, preserving existing choices.
Running that real tool in the guest created Pictures successfully. This fix
requires the next final-image boot to verify its automatic invocation.

The older diagnostic installation booted its own virtual disk with every
CD-ROM drive detached. SDDM required the newly created normal user's password;
login reached Hyprland and Rilex Welcome. That user successfully ran
`sudo apt-get update`: all four official Debian channels refreshed and
`APT_EXIT:0` was captured. Screenshots and boot command are in
`.cache/qa-installed-old`. Its immutable older image still contains the known
Waybar launch defect and is not the release candidate. The initial SDDM session
seed now uses its full desktop-file path, following observed fallback behavior.

A staged GUI QA input helper uses guest XTEST timing, verifies QEMU, mounted
live media and exactly one 32 GiB `/dev/vda`, and sends private QA credentials
over SSH stdin. It deliberately leaves screenshots, summary review and the
final destructive confirmation to the QA operator. Python compilation and
all seven installer static assertions pass; final-image runtime remains open.

## Final candidate qualification (2026-10-11)

The current `dist/rilex-0.1-amd64.iso` supersedes every historical candidate
above. It was built from `feaca7002cb46eb391b0cf40fc5615a09be1d231` by
[38145830005](https://github.com/thepeteriley/rilex/actions/runs/38145830005),
is 1,771,438,080 bytes, and has SHA-256
`5f8cdc97ee62a33dde1e444325d087d1b648a8b046595cf97c44e9f80717324d`.
The artifact archive, ISO structure, embedded source revision and GitHub
cryptographic build attestations passed verification. Separate final-image
native Linux QEMU live boots passed in UEFI
[38146559897](https://github.com/thepeteriley/rilex/actions/runs/38146559897)
and BIOS [38146562538](https://github.com/thepeteriley/rilex/actions/runs/38146562538).
Both inspected screenshots show Hyprland, Waybar and Foot Welcome.

The same final ISO also passed all 17 local live checks with QEMU 11.1.2 TCG
on macOS ARM64. The actual compositor reported 53 bindings and no config
errors. Super+Space launched Fuzzel, which launched Foot; workspace switching,
terminal and fullscreen bindings were observed. The first-login Pictures
folder was created automatically. Evidence is in the ignored private
`.cache/qa-final-uefi` directory.

The final local Calamares wizard accepted a newly generated private test
account and reached reviewed partition summary and explicit destructive
confirmation. Only a disposable 32 GiB virtual disk was selected. Its real
38-job installation has reached initramfs generation after copying the system
and installing UEFI GRUB and fallback EFI. Target GRUB defaults contain only
`quiet`, with no QA debug-shell/serial boot parameters. Completion and
independent disk-only boot are still pending; native installation run
[38147436556](https://github.com/thepeteriley/rilex/actions/runs/38147436556)
is also in progress. No release/tag has been created.

The final `feaca70` candidate completed all 38 actual Calamares jobs at
2026-10-11 14:44 UTC. A new QEMU process booted only its installed qcow2 disk;
QMP inventory confirmed no inserted CD media. The newly created normal user
logged in through password-protected SDDM to Rilex Hyprland. Actual shell checks
passed Hyprland, Waybar, Foot, NetworkManager, PipeWire, WirePlumber, Hyprland
portal and signed APT refresh against all four official Debian channels.
The serial log contains the strict `RILEX_INSTALLED_QA_PASS` marker; screenshots
and inventory are under `.cache/qa-final-installed`. Installed boot defaults
contained no ephemeral QA debug parameters. The QA controller's single-client
QMP socket ownership was corrected in ac75982; no ISO changes were required.

First-login inspection exposed a missing `hyprland-guiutils` utility. Upstream
uses its dialog for unresponsive applications; official backports provide a
compatible small package. It will be added and a new image rebuilt/retested
before release. This successful installation qualifies `feaca70`, not a future
image. No release/tag exists yet.

Corrected native-QEMU installation QA run38148591896 was independently
inspected, not inferred from its exit code. Candidate feaca7002 and controller
ac759823 completed all38 Calamares jobs, all17 live assertions, created-user
password login, actual Hyprland/Waybar/Foot and service checks, then a signed
APT metadata refresh with the strict guest success marker. The independent
QMP inventory and boot command contain no virtual CD. Screenshots and raw
logs are preserved in `.cache/qa-native-install-38148591896` and the workflow
artifact. Earlier run38147436556 installed successfully but its controller
held the sole QMP connection open during screenshot capture; that QA bug was
fixed. Neither outcome qualifies the newer GUI-utils candidate until its own
run38156156216 completes and its actual evidence is inspected.

Latest GUI-utils candidate 5efe987 passed native installation QA 38156156216.
The artifact was downloaded and independently inspected: exact candidate and
controller provenance, all 17 live assertions, all 38 successful Calamares jobs,
actual destructive GUI confirmation on only the disposable 32 GiB `vda`, disk-only
UEFI boot with no CD in command or QMP inventory, password-protected normal-user
SDDM login, visible Hyprland/Waybar/Foot, active networking/audio/portal and
successful signed APT refresh. The strict installed guest success marker is in
the raw serial output. Screenshots/logs are under ignored
`.cache/qa-native-install-38156156216` and its public workflow artifact; passwords,
private keys and test disks were excluded. The latest-image installation,
independent-boot, normal-user and APT gates now pass. Hardware-dependent features
and the separately documented unsupported cases remain unverified.
