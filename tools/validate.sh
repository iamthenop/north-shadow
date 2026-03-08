#!/usr/bin/env bash
set -euo pipefail

POSTS_DIR="${POSTS_DIR:-_posts}"
OUT_DIR="${OUT_DIR:-_timestamps}"

die() { echo "Error: $*" >&2; exit 3; }
need() { command -v "$1" >/dev/null 2>&1 || die "Missing dependency: $1"; }

usage() {
  cat <<EOF
Usage:
  ./.tools/validate.sh _posts/file.md
EOF
}

need openssl

[[ $# -eq 1 ]] || { usage; exit 3; }

IN_FILE="$1"
[[ -f "$IN_FILE" ]] || die "File not found: $IN_FILE"

case "$IN_FILE" in
  "$POSTS_DIR"/*.md) ;;
  *)
    die "Input must be a markdown file under $POSTS_DIR/"
    ;;
esac

BASE="$(basename "$IN_FILE")"
P7S="$OUT_DIR/$BASE.p7s"
TSQ="$OUT_DIR/$BASE.p7s.tsq"
TSR="$OUT_DIR/$BASE.p7s.tsr"

missing=0
for f in "$P7S" "$TSQ" "$TSR"; do
  [[ -f "$f" ]] || missing=1
done

if [[ $missing -ne 0 ]]; then
  echo "Missing one or more timestamp artifacts for $IN_FILE" >&2
  exit 1
fi

if ! openssl cms -verify \
  -binary \
  -in "$P7S" \
  -inform PEM \
  -content "$IN_FILE" \
  -noverify \
  -out /dev/null >/dev/null 2>&1; then
  echo "CMS signature does not match current file contents: $IN_FILE" >&2
  exit 2
fi

if ! openssl ts -verify \
  -queryfile "$TSQ" \
  -in "$TSR" >/dev/null 2>&1; then
  echo "Timestamp response does not match stored query for: $IN_FILE" >&2
  exit 2
fi

echo "Valid: $IN_FILE"
exit 0