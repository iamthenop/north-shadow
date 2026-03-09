#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="$ROOT_DIR/tools"
TIMESTAMPS_DIR="${TIMESTAMPS_DIR:-$ROOT_DIR/_timestamps}"

# Optional local config
if [[ -f "$TOOLS_DIR/stamp.conf" ]]; then
  # shellcheck disable=SC1091
  source "$TOOLS_DIR/stamp.conf"
fi

die() { echo "Error: $*" >&2; exit 3; }
need() { command -v "$1" >/dev/null 2>&1 || die "Missing dependency: $1"; }

usage() {
  cat >&2 <<'EOF'
Usage: validate.sh <proof.json> [input.md]

Validates:
  - embedded content hash
  - CMS content signature (without signer CA trust)
  - RFC3161 timestamp response (with TSA trust)

TSA trust must be configured by at least one of:
  TSA_CA_FILE
  TSA_CA_PATH
  TSA_CA_STORE
EOF
  exit 1
}

main() {
  need python3
  need openssl

  local proof input resolved_proof
  proof="${1:-}"
  input="${2:-}"

  [[ -n "$proof" ]] || usage

  if [[ -f "$proof" ]]; then
    resolved_proof="$proof"
  elif [[ -f "$TIMESTAMPS_DIR/$proof" ]]; then
    resolved_proof="$TIMESTAMPS_DIR/$proof"
  else
    die "Proof bundle not found: $proof"
  fi

  [[ -n "${TSA_CA_FILE:-}${TSA_CA_PATH:-}${TSA_CA_STORE:-}" ]] \
    || die "Configure TSA_CA_FILE, TSA_CA_PATH, or TSA_CA_STORE for timestamp verification"

  local -a py_args=(
    --proof "$resolved_proof"
  )

  [[ -n "${input:-}" ]] && py_args+=(--input "$input")
  [[ -n "${TSA_CA_FILE:-}" ]] && py_args+=(--tsa-ca-file "$TSA_CA_FILE")
  [[ -n "${TSA_UNTRUSTED_FILE:-}" ]] && py_args+=(--tsa-untrusted-file "$TSA_UNTRUSTED_FILE")
  [[ -n "${TSA_CA_PATH:-}" ]] && py_args+=(--tsa-ca-path "$TSA_CA_PATH")
  [[ -n "${TSA_CA_STORE:-}" ]] && py_args+=(--tsa-ca-store "$TSA_CA_STORE")

  python3 "$TOOLS_DIR/validate_attestation.py" "${py_args[@]}"
}

main "$@"