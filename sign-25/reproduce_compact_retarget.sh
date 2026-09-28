#!/bin/sh
set -eu

COMMIT=a30462dce48bd484d7c8c4d5b1f971e7dfebacfd
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP=$(mktemp -d /tmp/ngcc-sqisign2d2-retarget.XXXXXX)
trap 'rm -rf -- "$TMP"' EXIT HUP INT TERM

git clone --quiet https://github.com/martinfeussner/NGCC-Signature-Audit.git "$TMP/audit"
git -C "$TMP/audit" checkout --quiet "$COMMIT"
test "$(git -C "$TMP/audit" rev-parse HEAD)" = "$COMMIT"

exec "$TMP/audit/SQIsign2D2/reproducer/build_and_run.sh" "$HERE"
