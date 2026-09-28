#!/bin/sh
set -eu

COMMIT=e724a12a834bfc063dc0d2959d864842f269eb1e
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP=$(mktemp -d /tmp/ngcc-mamba-reaction.XXXXXX)
trap 'rm -rf -- "$TMP"' EXIT HUP INT TERM

git clone --quiet https://github.com/acprk/ngcc-round1-cryptanalysis.git "$TMP/audit"
git -C "$TMP/audit" checkout --quiet "$COMMIT"
test "$(git -C "$TMP/audit" rev-parse HEAD)" = "$COMMIT"

cd "$TMP/audit/mamba-nike-key-recovery"
REFROOT="$HERE/Implementations/Reference_Implementation" \
NKEYS="${NKEYS:-1}" CC="${CC:-cc}" ./run_all.sh
