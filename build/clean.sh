#!/bin/bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")/.." && pwd)
[[ $EUID == 0 && $(uname -s) == Linux ]] || { echo 'Run with sudo on Linux.' >&2; exit 1; }
WORK="$ROOT/.build/iso"
if [[ -d $WORK ]]; then
 cd "$WORK"
 lb clean --all
 # Remove generated configuration after live-build resets build state; keep downloaded cache.
 rm -rf -- config .build
fi
