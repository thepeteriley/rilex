#!/bin/bash
# Run only inside the disposable Rilex live QA guest, from its virtual QA CD.
set -euo pipefail
[[ $EUID == 0 && -f /run/live/medium/live/filesystem.squashfs ]] || { echo 'Requires disposable live QA guest.' >&2; exit 1; }
[[ $(cat /sys/class/dmi/id/product_name) == *QEMU* || $(cat /sys/class/dmi/id/sys_vendor) == *QEMU* ]] || { echo 'Refusing non-QEMU host.' >&2; exit 1; }
SEED=$(cd -- "$(dirname -- "$0")" && pwd)
[[ -f "$SEED/authorized_keys" ]] || exit 1
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y openssh-server
install -d -m700 /root/.ssh
install -m600 "$SEED/authorized_keys" /root/.ssh/authorized_keys
systemctl start ssh
printf 'QA SSH ready; key belongs only to this disposable test environment.\n'
