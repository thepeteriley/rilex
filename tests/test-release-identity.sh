#!/bin/bash
# Actual dpkg unpack/remove lifecycle confined to an isolated root database.
set -euo pipefail
DEFAULTS=${1:?Usage: test-release-identity.sh defaults.deb actual-base-files.deb}
BASE=${2:?Supply a real Debian base-files package}
[[ $(uname -s) == Linux && $EUID == 0 ]] || { echo 'Run as root in the disposable Debian build VM.' >&2; exit 1; }
FIXTURE=$(mktemp -d /tmp/rilex-identity-test.XXXXXX)
trap 'rm -rf -- "$FIXTURE"' EXIT
mkdir -p "$FIXTURE/var/lib/dpkg"
touch "$FIXTURE/var/lib/dpkg/status"
# No configure step: postinst service activation is intentionally outside this
# package-file lifecycle test. DPKG_ROOT confines diversion metadata and files.
dpkg --root="$FIXTURE" --force-script-chrootless --force-depends --unpack "$BASE"
cp "$FIXTURE/usr/lib/os-release" "$FIXTURE/debian-original"
dpkg --root="$FIXTURE" --force-script-chrootless --force-depends --unpack "$DEFAULTS"
grep -qx 'ID=rilex' "$FIXTURE/etc/os-release"
cmp "$FIXTURE/usr/lib/os-release.debian" "$FIXTURE/debian-original"
# Re-unpacking the genuine vendor package exercises the same regular-file
# replacement used by base-files updates, without synthesizing a Debian package.
dpkg --root="$FIXTURE" --force-script-chrootless --force-depends --unpack "$BASE"
grep -qx 'ID=rilex' "$FIXTURE/etc/os-release"
cmp "$FIXTURE/usr/lib/os-release.debian" "$FIXTURE/debian-original"
dpkg --root="$FIXTURE" --force-script-chrootless --force-depends --remove rilex-defaults
cmp "$FIXTURE/usr/lib/os-release" "$FIXTURE/debian-original"
[[ ! -e "$FIXTURE/usr/lib/os-release.debian" ]]
dpkg --root="$FIXTURE" --force-script-chrootless --force-depends --purge rilex-defaults
cmp "$FIXTURE/usr/lib/os-release" "$FIXTURE/debian-original"
echo 'Rilex identity survived actual base-files re-unpack; remove and purge restored Debian identity.'
