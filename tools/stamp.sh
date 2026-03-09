#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="$ROOT_DIR/tools"

POSTS_DIR="${POSTS_DIR:-_posts}"
OUT_DIR="${OUT_DIR:-_timestamps}"
CONF_FILE="${CONF_FILE:-$TOOLS_DIR/stamp.conf}"

SIGNING_PROVIDER="${SIGNING_PROVIDER:-file}"
HASH_ALGORITHM="${HASH_ALGORITHM:-sha256}"
TSA_URL="${TSA_URL:-https://freetsa.org/tsr}"

FILE_CERT="${FILE_CERT:-$HOME/.sign/sign.crt}"
FILE_KEY="${FILE_KEY:-$HOME/.sign/sign.key}"

PKCS11_MODULE="${PKCS11_MODULE:-}"
PKCS11_URI="${PKCS11_URI:-}"
PKCS11_CERT="${PKCS11_CERT:-}"

SIGN_COMMAND="${SIGN_COMMAND:-}"
SIGN_CERT="${SIGN_CERT:-}"

die() { echo "Error: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "Missing dependency: $1"; }

usage() {
  cat <<EOF
Usage:
  $0 _posts/file.md

Environment overrides:
  POSTS_DIR=_posts
  OUT_DIR=_timestamps
  CONF_FILE=tools/stamp.conf
  SIGNING_PROVIDER=file|pkcs11|command
  HASH_ALGORITHM=sha256
  TSA_URL=https://freetsa.org/tsr

Config file:
  If present, \$CONF_FILE is sourced before stamping.

Output:
  Writes:
    _timestamps/<published-file>.p7s
    _timestamps/<published-file>.p7s.tsq
    _timestamps/<published-file>.p7s.tsr
    _timestamps/<published-file>.proof.json
EOF
}

load_config() {
  if [[ -f "$CONF_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$CONF_FILE"
  fi
}

provider_cert_path() {
  case "$SIGNING_PROVIDER" in
    file)
      [[ -n "$FILE_CERT" ]] || die "FILE_CERT is not set"
      printf '%s\n' "$FILE_CERT"
      ;;
    pkcs11)
      [[ -n "$PKCS11_CERT" ]] || die "PKCS11_CERT is not set"
      printf '%s\n' "$PKCS11_CERT"
      ;;
    command)
      [[ -n "$SIGN_CERT" ]] || die "SIGN_CERT is not set"
      printf '%s\n' "$SIGN_CERT"
      ;;
    *)
      die "Unsupported SIGNING_PROVIDER: $SIGNING_PROVIDER"
      ;;
  esac
}

sign_cms() {
  local in_file="$1"
  local out_p7s="$2"

  case "$SIGNING_PROVIDER" in
    file)
      [[ -f "$FILE_CERT" ]] || die "Certificate not found: $FILE_CERT"
      [[ -f "$FILE_KEY"  ]] || die "Key not found: $FILE_KEY"

      openssl cms -sign \
        -binary \
        -in "$in_file" \
        -signer "$FILE_CERT" \
        -inkey "$FILE_KEY" \
        -outform PEM \
        -out "$out_p7s" \
        -nodetach
      ;;
    pkcs11)
      [[ -n "$PKCS11_MODULE" ]] || die "PKCS11_MODULE is not set"
      [[ -n "$PKCS11_URI"    ]] || die "PKCS11_URI is not set"
      [[ -f "$PKCS11_CERT"   ]] || die "Certificate not found: $PKCS11_CERT"

      openssl cms -sign \
        -binary \
        -in "$in_file" \
        -signer "$PKCS11_CERT" \
        -inkey "$PKCS11_URI" \
        -keyform engine \
        -outform PEM \
        -out "$out_p7s" \
        -nodetach
      ;;
    command)
      [[ -n "$SIGN_COMMAND" ]] || die "SIGN_COMMAND is not set"
      [[ -x "$SIGN_COMMAND" ]] || die "SIGN_COMMAND is not executable: $SIGN_COMMAND"
      [[ -f "$SIGN_CERT"    ]] || die "Certificate not found: $SIGN_CERT"

      "$SIGN_COMMAND" "$in_file" "$out_p7s"
      [[ -f "$out_p7s" ]] || die "SIGN_COMMAND did not produce output: $out_p7s"
      ;;
    *)
      die "Unsupported SIGNING_PROVIDER: $SIGNING_PROVIDER"
      ;;
  esac
}

main() {
  need openssl
  need curl
  need python3

  [[ $# -eq 1 ]] || { usage; exit 1; }

  load_config

  local in_file="$1"
  [[ -f "$in_file" ]] || die "File not found: $in_file"

  case "$in_file" in
    "$POSTS_DIR"/*.md|"$ROOT_DIR"/"$POSTS_DIR"/*.md) ;;
    *)
      die "Input must be a markdown file under $POSTS_DIR/"
      ;;
  esac

  mkdir -p "$OUT_DIR"

  local base
  local p7s
  local tsq
  local tsr
  local proof_json
  local metadata_json
  local cert_path

  base="$(basename "$in_file")"
  p7s="$OUT_DIR/$base.p7s"
  tsq="$OUT_DIR/$base.p7s.tsq"
  tsr="$OUT_DIR/$base.p7s.tsr"
  proof_json="$OUT_DIR/$base.proof.json"
  metadata_json="$(mktemp)"
  cert_path="$(provider_cert_path)"

  trap 'rm -f -- '"$(printf '%q' "$metadata_json")" EXIT

  echo "Stamping: $in_file"
  echo "Provider: $SIGNING_PROVIDER"

  sign_cms "$in_file" "$p7s"
  [[ -s "$p7s" ]] || die "CMS signature file is empty: $p7s"

  echo "Creating timestamp query: $tsq"
  openssl ts -query \
    -data "$p7s" \
    "-$HASH_ALGORITHM" \
    -cert \
    -out "$tsq"
  [[ -s "$tsq" ]] || die "Timestamp query file is empty: $tsq"

  echo "Requesting timestamp response: $tsr"
  curl --http1.1 --fail --silent --show-error \
    -D /tmp/tsa.headers \
    -H 'Content-Type: application/timestamp-query' \
    -H 'Accept: application/timestamp-reply' \
    --data-binary "@$tsq" \
    "$TSA_URL" \
    -o "$tsr"

  echo "TSA headers:"
  cat /tmp/tsa.headers

  [[ -s "$tsr" ]] || die "Timestamp response file is empty: $tsr"

  echo "Extracting metadata"
  python3 "$TOOLS_DIR/extract_metadata.py" "$in_file" > "$metadata_json"
  [[ -s "$metadata_json" ]] || die "Metadata extraction produced an empty file"

  echo "Building attestation bundle: $proof_json"
  python3 "$TOOLS_DIR/build_attestation.py" \
    --input "$in_file" \
    --signature "$p7s" \
    --tsq "$tsq" \
    --tsr "$tsr" \
    --metadata "$metadata_json" \
    --hash-algorithm "$HASH_ALGORITHM" \
    --output "$proof_json"

  [[ -s "$proof_json" ]] || die "Attestation bundle is empty: $proof_json"

  echo "Wrote:"
  echo "  $p7s"
  echo "  $tsq"
  echo "  $tsr"
  echo "  $proof_json"
}

main "$@"