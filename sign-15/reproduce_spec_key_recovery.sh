#!/bin/sh
set -eu

COMMIT=d03848f40a49a1d1d146e33c88ce251ac092439d
TMP=$(mktemp -d /tmp/ngcc-atlas-spec-recovery.XXXXXX)
trap 'rm -rf -- "$TMP"' EXIT HUP INT TERM

git clone --quiet https://github.com/martinfeussner/NGCC-Signature-Audit.git "$TMP/audit"
git -C "$TMP/audit" checkout --quiet "$COMMIT"
test "$(git -C "$TMP/audit" rev-parse HEAD)" = "$COMMIT"

REPRO="$TMP/audit/MORNING-ATLAS/reproducer"
"$REPRO/verify_evidence.sh"

if [ "${ATLAS_FULL:-0}" = 1 ]; then
    PY=${NGCC_SAGE_PYTHON:-python3}
    "$PY" -c 'import numpy, scipy, fpylll'
    env PYTHON="$PY" "$REPRO/run_full.sh" 3000000 4 12 "$TMP/full-key-4"
fi
