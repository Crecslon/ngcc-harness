#!/bin/sh
set -eu

COMMIT=e724a12a834bfc063dc0d2959d864842f269eb1e
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP=$(mktemp -d /tmp/ngcc-polarlac-timing.XXXXXX)
trap 'rm -rf -- "$TMP"' EXIT HUP INT TERM

git clone --quiet https://github.com/acprk/ngcc-round1-cryptanalysis.git "$TMP/audit"
git -C "$TMP/audit" checkout --quiet "$COMMIT"
test "$(git -C "$TMP/audit" rev-parse HEAD)" = "$COMMIT"

if [ -z "${CORE:-}" ]; then
    AFFINITY=$(taskset -pc $$ | sed 's/.*: //')
    CORE=${AFFINITY%%,*}
    CORE=${CORE%%-*}
fi

cd "$TMP/audit/polarlac-timing-leak"
REF="$HERE/Implementations/Reference_Implementation/x86/POLARLAC-Light" \
CORE="$CORE" CC="${CC:-cc}" ./run_all.sh
