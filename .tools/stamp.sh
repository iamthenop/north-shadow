#!/usr/bin/env bash
set -euo pipefail

POSTS_DIR="${POSTS_DIR:-_posts}"
OUT_DIR="${OUT_DIR:-_timestamps}"
CERT="${CERT:-$HOME/.sign/sign.crt}"
KEY="${KEY:-$HOME/.sign/sign.key}"
TSA_URL="${TSA_URL:-https://freetsa.org/tsr}"
HASH="${HASH:-sha256}"

die() { echo "Error: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "Missing dependency: $1"; }

usage() {
  cat <<EOF
Usage:
  ./.tools/stamp.sh _posts/file.md

Environment overrides:
  POSTS_DIR=_posts
  OUT_DIR=_timestamps
  CERT=~/.sign/sign.crt
  KEY=~/.sign/sign.key
  TSA_URL=https://freetsa.org/tsr
  HASH=sha256
EOF
}

need openssl
need curl

[[ $# -eq 1 ]] || { usage; exit 1; }

IN_FILE="$1"
[[ -f "$IN_FILE" ]] || die "File not found: $IN_FILE"

case "$IN_FILE" in
  "$POSTS_DIR"/*.md) ;;
  *)
    die "Input must be a markdown file under $POSTS_DIR/"
    ;;
esac

[[ -f "$CERT" ]] || die "Certificate not found: $CERT"
[[ -f "$KEY" ]] || die "Key not found: $KEY"

mkdir -p "$OUT_DIR"

BASE="$(basename "$IN_FILE")"
P7S="$OUT_DIR/$BASE.p7s"
TSQ="$OUT_DIR/$BASE.p7s.tsq"
TSR="$OUT_DIR/$BASE.p7s.tsr"

echo "Signing: $IN_FILE"
openssl cms -sign \
  -binary \
  -in "$IN_FILE" \
  -signer "$CERT" \
  -inkey "$KEY" \
  -outform PEM \
  -out "$P7S" \
  -nodetach

echo "Creating timestamp query: $TSQ"
openssl ts -query \
  -data "$P7S" \
  -"$HASH" \
  -cert \
  -out "$TSQ"

echo "Requesting timestamp response: $TSR"
curl --fail --silent --show-error \
  -H 'Content-Type: application/timestamp-query' \
  --data-binary "@$TSQ" \
  "$TSA_URL" \
  -o "$TSR"

echo "Wrote:"
echo "  $P7S"
echo "  $TSQ"
echo "  $TSR"