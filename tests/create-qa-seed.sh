#!/bin/bash
# Creates a QA-only virtual CD; never shipped inside the release ISO.
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")/.." && pwd)
SEED="$ROOT/.cache/qa-seed"
mkdir -p "$SEED"
if [[ ! -f "$ROOT/.cache/qa_ed25519" ]]; then ssh-keygen -q -t ed25519 -N '' -f "$ROOT/.cache/qa_ed25519"; fi
cp "$ROOT/.cache/qa_ed25519.pub" "$SEED/authorized_keys"
cp "$ROOT/tests/check-live-session.sh" "$SEED/check-live-session.sh"
cp "$ROOT/tests/qa-seed-bootstrap.sh" "$SEED/bootstrap.sh"
xorriso -as mkisofs -V RILEX_QA -o "$ROOT/.cache/qa-seed.iso" "$SEED"
