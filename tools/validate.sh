#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="$ROOT_DIR/tools"
TIMESTAMPS_DIR="${TIMESTAMPS_DIR:-$ROOT_DIR/_timestamps}"

die() { echo "Error: $*" >&2; exit 3; }
need() { command -v "$1" >/dev/null 2>&1 || die "Missing dependency: $1"; }

usage() {
  cat <<EOF
Usage:
  $0 --proof _timestamps/file.proof.json
  $0 --proof _timestamps/file.proof.json --input path/to/file.md

Notes:
  --proof is the canonical validation target.
  --input is optional and is only used to compare external file bytes
  against the embedded content in the proof bundle.

Exit codes:
  0 = valid
  1 = missing proof artifact
  2 = mismatch / invalid proof
  3 = usage or dependency error
EOF
}

resolve_proof_path() {
  local proof="$1"

  if [[ -f "$proof" ]]; then
    printf '%s\n' "$proof"
    return 0
  fi

  if [[ -f "$TIMESTAMPS_DIR/$proof" ]]; then
    printf '%s\n' "$TIMESTAMPS_DIR/$proof"
    return 0
  fi

  return 1
}

main() {
  need python3

  local proof=""
  local input=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --proof)
        [[ $# -ge 2 ]] || { usage; exit 3; }
        proof="$2"
        shift 2
        ;;
      --input)
        [[ $# -ge 2 ]] || { usage; exit 3; }
        input="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        usage
        exit 3
        ;;
    esac
  done

  [[ -n "$proof" ]] || { usage; exit 3; }

  local resolved_proof
  if ! resolved_proof="$(resolve_proof_path "$proof")"; then
    echo "Missing proof bundle: $proof" >&2
    exit 1
  fi

  if [[ -n "$input" ]]; then
    python3 "$TOOLS_DIR/validate_attestation.py" --proof "$resolved_proof" --input "$input"
  else
    python3 "$TOOLS_DIR/validate_attestation.py" --proof "$resolved_proof"
  fi
}

main "$@"