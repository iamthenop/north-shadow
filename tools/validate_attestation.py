#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


EXIT_VALID = 0
EXIT_MISSING = 1
EXIT_INVALID = 2
EXIT_USAGE = 3


def die(msg: str, code: int = EXIT_INVALID) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a north-shadow attestation bundle. "
            "Optionally compare an external markdown file against the embedded content."
        )
    )
    parser.add_argument("--proof", required=True, help="Path to attestation proof JSON")
    parser.add_argument("--input", help="Optional path to markdown file to compare with embedded content")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise SystemExit(EXIT_MISSING)
    except json.JSONDecodeError as exc:
        die(f"Invalid JSON in proof bundle: {path}: {exc}")
    if not isinstance(data, dict):
        die("Proof bundle must be a JSON object")
    return data


def require_path(doc: dict[str, Any], *path: str) -> Any:
    cur: Any = doc
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            die(f"Missing required field: {'.'.join(path)}")
        cur = cur[key]
    return cur


def b64decode_field(value: str, field_name: str) -> bytes:
    if not isinstance(value, str):
        die(f"Field '{field_name}' must be a base64 string")
    try:
        return base64.b64decode(value, validate=True)
    except Exception as exc:
        die(f"Invalid base64 in field '{field_name}': {exc}")


def compute_hash(data: bytes, algorithm: str) -> str:
    if not isinstance(algorithm, str) or not algorithm:
        die("Hash algorithm must be a non-empty string")
    try:
        h = hashlib.new(algorithm)
    except ValueError as exc:
        raise SystemExit(f"Error: Unsupported hash algorithm: {algorithm}") from exc
    h.update(data)
    return h.hexdigest()


def run_openssl_verify(content: bytes, signature_bytes: bytes) -> None:
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        content_path = td_path / "content.md"
        sig_path = td_path / "signature.p7s"

        content_path.write_bytes(content)
        sig_path.write_bytes(signature_bytes)

        proc = subprocess.run(
            [
                "openssl",
                "cms",
                "-verify",
                "-binary",
                "-inform",
                "PEM",
                "-in",
                str(sig_path),
                "-content",
                str(content_path),
                "-noverify",
                "-out",
                str(td_path / "verified-content.out"),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if proc.returncode != 0:
            die("CMS signature verification failed")


def run_timestamp_verify(tsq_bytes: bytes, tsr_bytes: bytes) -> None:
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        tsq_path = td_path / "stamp.tsq"
        tsr_path = td_path / "stamp.tsr"

        tsq_path.write_bytes(tsq_bytes)
        tsr_path.write_bytes(tsr_bytes)

        proc = subprocess.run(
            [
                "openssl",
                "ts",
                "-verify",
                "-queryfile",
                str(tsq_path),
                "-in",
                str(tsr_path),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if proc.returncode != 0:
            die("Timestamp response verification failed")


def validate_bundle_structure(
    doc: dict[str, Any],
) -> tuple[bytes, bytes, bytes, bytes, str, str]:
    schema = require_path(doc, "schema")
    version = require_path(doc, "version")

    if schema != "north-shadow.attestation":
        die(f"Unexpected schema: {schema}")
    if version != 1:
        die(f"Unsupported schema version: {version}")

    media_type = require_path(doc, "content", "media_type")
    encoding = require_path(doc, "content", "encoding")
    algorithm = require_path(doc, "content", "hash", "algorithm")
    expected_hash = require_path(doc, "content", "hash", "value")
    content_b64 = require_path(doc, "content", "value")

    sig_type = require_path(doc, "proof", "signature", "type")
    sig_encoding = require_path(doc, "proof", "signature", "encoding")
    sig_value = require_path(doc, "proof", "signature", "value")

    tsq_type = require_path(doc, "proof", "timestamp", "query", "type")
    tsq_encoding = require_path(doc, "proof", "timestamp", "query", "encoding")
    tsq_b64 = require_path(doc, "proof", "timestamp", "query", "value")

    tsr_type = require_path(doc, "proof", "timestamp", "response", "type")
    tsr_encoding = require_path(doc, "proof", "timestamp", "response", "encoding")
    tsr_b64 = require_path(doc, "proof", "timestamp", "response", "value")

    if media_type != "text/markdown":
        die(f"Unexpected content.media_type: {media_type}")
    if encoding != "base64":
        die(f"Unexpected content.encoding: {encoding}")
    if sig_type != "cms":
        die(f"Unexpected proof.signature.type: {sig_type}")
    if sig_encoding not in ("base64", "pem"):
        die(f"Unexpected proof.signature.encoding: {sig_encoding}")
    if tsq_type != "rfc3161-tsq":
        die(f"Unexpected proof.timestamp.query.type: {tsq_type}")
    if tsq_encoding != "base64":
        die(f"Unexpected proof.timestamp.query.encoding: {tsq_encoding}")
    if tsr_type != "rfc3161-tsr":
        die(f"Unexpected proof.timestamp.response.type: {tsr_type}")
    if tsr_encoding != "base64":
        die(f"Unexpected proof.timestamp.response.encoding: {tsr_encoding}")

    content = b64decode_field(content_b64, "content.value")

    if not isinstance(sig_value, str):
        die("Field 'proof.signature.value' must be a string")

    if sig_encoding == "base64":
        signature = b64decode_field(sig_value, "proof.signature.value")
    elif sig_encoding == "pem":
        signature = sig_value.encode("utf-8")
    else:
        die(f"Unexpected proof.signature.encoding: {sig_encoding}")

    tsq = b64decode_field(tsq_b64, "proof.timestamp.query.value")
    tsr = b64decode_field(tsr_b64, "proof.timestamp.response.value")

    actual_hash = compute_hash(content, str(algorithm))
    if actual_hash.lower() != str(expected_hash).lower():
        die("Embedded content hash does not match proof bundle")

    return content, signature, tsq, tsr, str(algorithm), str(expected_hash)


def validate_external_input(
    input_path: Path,
    expected_content: bytes,
    algorithm: str,
    expected_hash: str,
) -> None:
    if not input_path.is_file():
        die(f"Input file not found: {input_path}", code=EXIT_USAGE)

    live_bytes = input_path.read_bytes()
    if live_bytes != expected_content:
        die("Input file bytes do not match embedded content bundle")

    actual_hash = compute_hash(live_bytes, algorithm)
    if actual_hash.lower() != expected_hash.lower():
        die("Input file hash does not match proof bundle")


def main() -> None:
    args = parse_args()

    proof_path = Path(args.proof)
    doc = load_json(proof_path)

    content, signature, tsq, tsr, algorithm, expected_hash = validate_bundle_structure(doc)

    if args.input:
        validate_external_input(Path(args.input), content, algorithm, expected_hash)

    run_openssl_verify(content, signature)
    run_timestamp_verify(tsq, tsr)

    if args.input:
        print(f"Valid: {args.input} matches {args.proof}")
    else:
        print(f"Valid: {args.proof}")


if __name__ == "__main__":
    main()