#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REF="$HERE/Implementations/Reference_Implementation/Amoeba-576/src"
BACKEND="$REF/backend"
SYMMETRIC="$REF/symmetric"
BUILD=$(mktemp -d /tmp/ngcc-amoeba-dfo.XXXXXX)
trap 'rm -rf -- "$BUILD"' EXIT HUP INT TERM

CC=${CC:-cc}

set --
for source in "$BACKEND"/*.c "$SYMMETRIC"/*.c; do
    case "$source" in
        */cpapke.c|*/ccakem.c|*/kem.c|*main*|*test*|*PQCgen*|*KAT*|*AlgorithmInstance*) ;;
        *) set -- "$@" "$source" ;;
    esac
done

"$CC" -O2 -fgnu89-inline -DSECURITY_LEVEL=128 \
    -I"$BACKEND" -I"$SYMMETRIC" \
    "$HERE/reproduce_dfo_key_recovery.c" "$BACKEND/ccakem.c" "$@" \
    -o "$BUILD/attack" -lm

exec "$BUILD/attack"
