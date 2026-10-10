#!/bin/bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")/.." && pwd)
[[ $EUID == 0 && $(uname -s) == Linux ]] || { echo 'Run with sudo on Linux.' >&2; exit 1; }
WORK="$ROOT/.build/iso"
if [[ -d $WORK ]]; then
 cd "$WORK"
 lb clean --purge
 # Only remove the generated configuration. Preserve downloaded package cache.
 rm -rf -- config .build
fi
