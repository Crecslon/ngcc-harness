#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP=$(mktemp -d /tmp/ngcc-atlas-safety.XXXXXX)
trap 'rm -rf -- "$TMP"' EXIT HUP INT TERM
CC=${CC:-cc}

for level in 128 192 256 512; do
    D="$ROOT/Implementation/Reference_Implementation/lwrdsa$level"
    BIN="$TMP/oob-$level"
    LOG="$TMP/oob-$level.log"
    "$CC" -std=c99 -O1 -g -fsanitize=address -fno-omit-frame-pointer \
        -I "$D" -o "$BIN" "$ROOT/atlas_oob_probe.c" \
        "$D/SIG_lwrdsa$level.c" "$D/polyvec.c" "$D/packing.c" \
        "$D/poly.c" "$D/rounding.c" "$D/auxfunc.c" "$D/drng.c"
    if ASAN_OPTIONS=detect_leaks=0 "$BIN" >"$LOG" 2>&1; then
        echo "ATLAS-$level parser unexpectedly returned cleanly" >&2
        exit 1
    fi
    case "$level" in
        128|192)
            grep -q 'AddressSanitizer: heap-buffer-overflow' "$LOG"
            grep -q 'WRITE of size 4' "$LOG"
            echo "CONFIRMED sign-15-5: ATLAS-$level malformed hint writes out of bounds"
            ;;
        256)
            grep -q 'AddressSanitizer: heap-buffer-overflow' "$LOG"
            grep -q 'READ of size 1' "$LOG"
            echo "CONFIRMED sign-15-5: ATLAS-$level unchecked hint count reads beyond the signature"
            ;;
        512)
            grep -q 'AddressSanitizer: stack-buffer-overflow' "$LOG"
            grep -q 'READ of size 2' "$LOG"
            echo "CONFIRMED sign-15-5: ATLAS-$level unchecked hint count reads beyond the hint array"
            ;;
    esac
done
