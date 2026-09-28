#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BASE="$HERE/Implementations and Test_Vectors/Implementations/Reference_Implementation/Rhyme-SM3/Rhyme-SM3-128"
BUILD=$(mktemp -d /tmp/ngcc-rhyme-parity.XXXXXX)
trap 'rm -rf -- "$BUILD"' EXIT HUP INT TERM
CC=${CC:-cc}

"$CC" -O3 -fwrapv -DRHYME_NO_AES -DRHYME_MODE=128 \
    -DOUTPUT_BLANK_TEST_VECTORS=0 -DALGORITHM_INSTANCE='"Rhyme-SM3-128"' \
    -I"$BASE" -I"$BASE/include" -I"$BASE/src/keygen" \
    "$HERE/reproduce_sm3_parity_runtime.c" \
    "$BASE/src/poly.c" "$BASE/src/ntt.c" "$BASE/src/ntt_tables.c" \
    "$BASE/src/sampler.c" "$BASE/src/encoding.c" "$BASE/src/packing.c" \
    "$BASE/src/sign.c" "$BASE/src/zpntt.c" "$BASE/src/symmetric-shake.c" \
    "$BASE/rhyme_xof.c" "$BASE/src/keygen/kg_main.c" \
    "$BASE/src/keygen/kg_solver.c" "$BASE/src/keygen/kg_zint.c" \
    "$BASE/src/keygen/kg_ntt.c" "$BASE/src/keygen/kg_primes.c" \
    "$BASE/randombytes.c" "$BASE/auxfunc.c" "$BASE/drng.c" \
    "$BASE/sm3.c" "$BASE/sm3_xof.c" -lm -o "$BUILD/parity"

exec "$BUILD/parity" "${1:-25000}"
