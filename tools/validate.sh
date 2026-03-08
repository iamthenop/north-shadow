#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="$ROOT_DIR/tools"

POSTS_DIR="${POSTS_DIR:-_posts}"
OUT_DIR="${OUT_DIR:-_timestamps}"

die() { echo "Error: $*" >&2; exit 3; }
need() { command -v "$1" >/dev/null 2>&1 || die "Missing dependency: $1"; }

usage() {
  cat <<EOF
Usage:
  $0 _posts/file.md
  $0 --proof _timestamps/file.md.proof.json

Exit codes:
  0 = valid
  1 = missing proof artifact
  2 = mismatch / invalid proof
  3 = usage or dependency error
EOF
}

proof_path_for_post() {
  local in_file="$1"
  local base
  base="$(basename "$in_file")"
  printf '%s\n' "$OUT_DIR/$base.proof.json"
}

validate_proof_json_only() {
  local proof_json="$1"
  [[ -f "$proof_json" ]] || { echo "Missing proof bundle: $proof_json" >&2; exit 1; }

  python3 "$TOOLS_DIR/validate_attestation.py" --proof "$proof_json"
}

validate_post_against_proof() {
  local in_file="$1"
  [[ -f "$in_file" ]] || die "File not found: $in_file"

  case "$in_file" in
    "$POSTS_DIR"/*.md|"$ROOT_DIR"/"$POSTS_DIR"/*.md) ;;
    *)
      die "Input must be a markdown file under $POSTS_DIR/"
      ;;
  esac

  local proof_json
  proof_json="$(proof_path_for_post "$in_file")"

  [[ -f "$proof_json" ]] || {
    echo "Missing proof bundle for $in_file: $proof_json" >&2
    exit 1
  }

  python3 "$TOOLS_DIR/validate_attestation.py" --input "$in_file" --proof "$proof_json"
}

main() {
  need python3

  [[ $# -ge 1 ]] || { usage; exit 3; }

  case "${1:-}" in
    --proof)
      [[ $# -eq 2 ]] || { usage; exit 3; }
      validate_proof_json_only "$2"
      ;;
    -h|--help)
      usage
      ;;
    *)
      [[ $# -eq 1 ]] || { usage; exit 3; }
      validate_post_against_proof "$1"
      ;;
  esac
}

main "$@"