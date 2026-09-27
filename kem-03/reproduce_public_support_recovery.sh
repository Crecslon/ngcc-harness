#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SRC="$ROOT/Implementations/Reference_Implementation/Loong-Block-ms-128"
TMP=$(mktemp -d /tmp/ngcc-loong-public-supports.XXXXXX)
trap 'rm -rf -- "$TMP"' EXIT HUP INT TERM
CC=${CC:-cc}

"$CC" -std=c99 -O2 -I "$SRC/src" -I "$SRC/lib/rbc-47" \
    -I "$SRC/lib/api_pkc" -o "$TMP/recover" \
    "$ROOT/reproduce_public_support_recovery.c" \
    "$SRC/src/augabidulin.c" "$SRC/src/ct_util.c" \
    "$SRC/src/gabidulin.c" "$SRC/src/loong_api_random.c" \
    "$SRC/src/loong_hash.c" "$SRC/src/loong_support.c" \
    "$SRC/src/loong_xof_reader.c" "$SRC/src/parsing.c" "$SRC/src/qpoly.c" \
    "$SRC/lib/rbc-47/rbc_elt.c" "$SRC/lib/rbc-47/rbc_vec.c" \
    "$SRC/lib/api_pkc/auxfunc.c" "$SRC/lib/api_pkc/drng.c"

"$TMP/recover" "${LOONG_TRIALS:-5}"
