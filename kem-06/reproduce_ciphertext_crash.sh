#!/bin/sh
set -eu

COMMIT=e724a12a834bfc063dc0d2959d864842f269eb1e
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP=$(mktemp -d /tmp/ngcc-bra-ct-crash.XXXXXX)
trap 'rm -rf -- "$TMP"' EXIT HUP INT TERM

git clone --quiet https://github.com/acprk/ngcc-round1-cryptanalysis.git "$TMP/audit"
git -C "$TMP/audit" checkout --quiet "$COMMIT"
test "$(git -C "$TMP/audit" rev-parse HEAD)" = "$COMMIT"

cd "$TMP/audit/bra-brqc-padding-malleability"
for level in 128 256 512; do
    echo "=== BRA-$level ==="
    WORK="$TMP/BRA-$level"
    mkdir "$WORK"
    cp -R "$HERE/Implementations/Reference_Implementation/BRA-$level/." "$WORK/"
    make -s -C "$WORK" "BRA-$level" >/dev/null
    set -- "$WORK"/bin/build/*.o
    "${CC:-cc}" -O2 -std=gnu99 -DHDR="\"KEM_BRA-$level.h\"" \
        src/kem_audit.c "$@" -I"$WORK" -o audit
    ./audit 1 0 5
done
