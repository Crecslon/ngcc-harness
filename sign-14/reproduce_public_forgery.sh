#!/bin/sh
set -eu

COMMIT=d03848f40a49a1d1d146e33c88ce251ac092439d
TMP=$(mktemp -d /tmp/ngcc-lynxer-forgery.XXXXXX)
trap 'rm -rf -- "$TMP"' EXIT HUP INT TERM

git clone --quiet https://github.com/martinfeussner/NGCC-Signature-Audit.git "$TMP/audit"
git -C "$TMP/audit" checkout --quiet "$COMMIT"
test "$(git -C "$TMP/audit" rev-parse HEAD)" = "$COMMIT"

"$TMP/audit/Lynxer/reproducer/run.sh"
