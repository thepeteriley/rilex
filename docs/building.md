# Building Rilex 0.1

The supported build target is Debian 13 amd64 with root privileges for live-build's chroot and mounts. Ubuntu amd64 can host a privileged Debian 13 container; using Debian build tools inside that container avoids mixing Ubuntu bootloader tooling into the image. Expect at least 30 GB available space and several hours depending on bandwidth and CPU. Source checks can run on macOS, but ISO assembly needs Linux.

## Debian amd64 host

```sh
sudo apt update
sudo apt install live-build debootstrap xorriso squashfs-tools dosfstools mtools \
  dpkg-dev ca-certificates rsync isolinux syslinux-common \
  grub-pc-bin grub-efi-amd64-bin python3
python3 tests/static-check.py
python3 build/check-package-availability.py
sudo ./build/build-iso.sh
```

Outputs are `dist/rilex-0.1-amd64.iso`, its adjacent `.sha256` checksum, the local defaults package, and `dist/build.log`. The root filesystem records exact installed package versions in `/usr/share/rilex/package-manifest.tsv`. `build/verify-iso.sh` checks structure and El Torito BIOS and UEFI entries. This does not establish that the desktop or installer works; the runtime gates in [testing.md](testing.md) remain mandatory before release.

To discard an incomplete build and regenerate configuration while retaining downloaded packages:

```sh
sudo ./build/clean.sh
sudo ./build/build-iso.sh
```

The script refuses to overwrite an existing build tree. Build trees and caches under `.build` and generated artifacts under `dist` are excluded from Git. Do not run the build from a source checkout whose path changes while the build is active.

## Ubuntu amd64 container

The manually triggered GitHub workflow uses this method. Docker must support privileged Linux containers.

```sh
docker run --rm --privileged -v "$PWD:/src" -w /src debian:trixie bash -c '
  apt-get update &&
  apt-get install -y live-build debootstrap xorriso squashfs-tools dosfstools \
    mtools dpkg-dev ca-certificates python3 rsync isolinux syslinux-common \
    grub-pc-bin grub-efi-amd64-bin &&
  ./build/build-iso.sh'
```

## Apple Silicon macOS

An ARM container does not natively execute this amd64 build. Use QEMU's x86-64 full-system emulation (TCG) and a Debian 13 amd64 guest. Hardware acceleration cannot accelerate an x86 guest on an ARM host. This is slower than building on conventional amd64 Linux.

Install QEMU with `brew install qemu`. Download the amd64 Debian 13 nocloud qcow2 image from the official [Debian cloud image directory](https://cloud.debian.org/images/cloud/trixie/latest/), along with its signed checksum manifest. Verify the manifest against Debian's published cloud-image signing key and verify the image checksum; do not disable signature verification for convenience. Create a writable overlay and expand its virtual size:

```sh
qemu-img create -f qcow2 -F qcow2 -b /absolute/path/debian-13-nocloud-amd64.qcow2 \
  /absolute/path/build-vm.qcow2
qemu-img resize /absolute/path/build-vm.qcow2 80G
qemu-system-x86_64 -machine q35 -accel tcg,thread=multi -smp 4 -m 8192 \
  -drive file=/absolute/path/build-vm.qcow2,if=virtio \
  -nic user,hostfwd=tcp:127.0.0.1:2222-:22 -nographic
```

Provision this disposable build guest via its serial console or a Debian installer with your own SSH public key. Do not embed SSH keys or credentials in the Rilex payload. Ensure the guest filesystem has expanded with `lsblk` and `df -h`; Debian cloud-init can expand the root partition during initial boot. Install the prerequisites above inside the guest, copy the source checkout into `/root/rilex` using `rsync -e 'ssh -p 2222'`, and run `/root/rilex/build/build-iso.sh`. Copy `dist` artifacts back using `rsync` or `scp`. Port 2222 is bound only to the host's loopback address.

Only QEMU-created qcow2 disks belong to this build and test process. Never pass through a physical disk. Runtime Hyprland tests need a virtio GPU with working EGL, or an explicitly tested software-rendering configuration; a serial-only build guest is sufficient for image assembly.

## Sources and trust

The stable base uses `https://deb.debian.org/debian` and `https://security.debian.org/debian-security`; Debian archive signature checks remain enabled. Hyprland 0.55.2, Hyprlock 0.9.6, and the Hyprland XDG portal 1.4.1 are exact official backports package versions in the tracked hook. No testing or unstable suite is enabled and no upstream source compilation is needed. Dependencies resolve through Debian's signed repositories. Available package versions can change; failure to find a pinned package is an actionable build error, not a reason to drop verification or silently change versions.

These commands reproduce the build process. Byte-for-byte reproducibility is not claimed because Debian security repositories evolve. Preserve the package manifest and build log for every candidate; see [packaging/README.md](../packaging/README.md) for the Rilex package delivery boundary.
