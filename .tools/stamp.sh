#!/usr/bin/env bash
set -euo pipefail

# ---- config (edit these) ----
SIGNER_CERT="${SIGNER_CERT:-$HOME/.sign/lascanop.crt}"   # signer cert (PEM)
SIGNER_KEY="${SIGNER_KEY:-$HOME/.sign/lascanop.key}"    # signer private key (PEM)
TSA_URL="${TSA_URL:-https://freetsa.org/tsr}"               # RFC3161 TSA endpoint
HASH="${HASH:-sha256}"                                      # sha256 recommended

POSTS_DIR="${POSTS_DIR:-_posts}"
OUT_DIR="${OUT_DIR:-_timestamps}"

# ---- helpers ----
die() { echo "Error: $*" >&2; exit 1; }

need() { command -v "$1" >/dev/null 2>&1 || die "Missing dependency: $1"; }

usage() {
  cat <<EOF
Usage:
  ./stamp.sh <path-to-md> [more-md-files...]
  ./stamp.sh --all

Environment overrides:
  SIGNER_CERT=/path/to/cert.pem
  SIGNER_KEY=/path/to/key.pem
  TSA_URL=https://example.com/tsa
  HASH=sha256
  POSTS_DIR=_posts
  OUT_DIR=_timestamps
EOF
}

# ---- checks ----
need openssl
need curl

[[ -f "$SIGNER_CERT" ]] || die "Signer cert not found: $SIGNER_CERT"
[[ -f "$SIGNER_KEY"  ]] || die "Signer key not found:  $SIGNER_KEY"

mkdir -p "$OUT_DIR"

# ---- build file list ----
files=()
if [[ $# -eq 0 ]]; then
  usage; exit 1
elif [[ "${1:-}" == "--all" ]]; then
  while IFS= read -r -d '' f; do files+=("$f"); done < <(find "$POSTS_DIR" -type f -name "*.md" -print0)
else
  for f in "$@"; do
    [[ -f "$f" ]] || die "File not found: $f"
    files+=("$f")
  done
fi

[[ ${#files[@]} -gt 0 ]] || die "No markdown files found."

# ---- main ----
for in_file in "${files[@]}"; do
  base="$(basename "$in_file")"
  stem="${base%.*}"                      # filename without extension

  p7s="$OUT_DIR/$stem.md.p7s"
  tsq="$OUT_DIR/$stem.md.p7s.tsq"
  tsr="$OUT_DIR/$stem.md.p7s.tsr"

  echo "==> Signing: $in_file"
  openssl cms -sign \
    -in "$in_file" \
    -signer "$SIGNER_CERT" \
    -inkey "$SIGNER_KEY" \
    -outform PEM \
    -binary \
    -nosmimecap \
    -cades \
    -md "$HASH" \
    -out "$p7s"

  echo "==> Building timestamp query: $tsq"
  openssl ts -query \
    -data "$p7s" \
    -"${HASH}" \
    -cert \
    -out "$tsq"

  echo "==> Requesting TSA timestamp: $tsr"
  curl -fsS \
    -H "Content-Type: application/timestamp-query" \
    --data-binary @"$tsq" \
    "$TSA_URL" \
    -o "$tsr"

  echo "==> Done:"
  echo "    $p7s"
  echo "    $tsq"
  echo "    $tsr"
  echo
done
