#!/bin/sh
set -eu

COMMIT=66c991978995c17d1514825a9e9d2ff6810bb22a
TMP=$(mktemp -d /tmp/ngcc-sqitriangle-rescaling.XXXXXX)
trap 'rm -rf -- "$TMP"' EXIT HUP INT TERM

git clone --quiet https://github.com/martinfeussner/NGCC-Signature-Audit.git "$TMP/audit"
git -C "$TMP/audit" checkout --quiet "$COMMIT"
test "$(git -C "$TMP/audit" rev-parse HEAD)" = "$COMMIT"

"$TMP/audit/SQIsignTriangle/reproducer/run.sh" "${1:-3}"
