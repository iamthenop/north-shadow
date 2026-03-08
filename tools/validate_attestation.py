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


def die(msg: str, code: int = 2) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a north-shadow attestation bundle, optionally against a live markdown file."
    )
    parser.add_argument("--proof", required=True, help="Path to the attestation proof JSON")
    parser.add_argument("--input", help="Optional path to a markdown file to validate against the proof")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise SystemExit(1)
    except json.JSONDecodeError as exc:
        die(f"Invalid JSON in proof bundle: {path}: {exc}")
    if not isinstance(data, dict):
        die("Proof bundle must be a JSON object")
    return data


def b64decode_field(value: str, field_name: str) -> bytes:
    try:
        return base64.b64decode(value, validate=True)
    except Exception as exc:
        die(f"Invalid base64 in field '{field_name}': {exc}")


def compute_hash(data: bytes, algorithm: str) -> str:
    try:
        h = hashlib.new(algorithm)
    except ValueError as exc:
        die(f"Unsupported hash algorithm: {algorithm}") from exc
    h.update(data)
    return h.hexdigest()


def require_path(doc: dict, *path: str):
    cur = doc
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            die(f"Missing required field: {'.'.join(path)}")
        cur = cur[key]
    return cur


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
                "/dev/null",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
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
        )
        if proc.returncode != 0:
            die("Timestamp response verification failed")


def validate_bundle_structure(doc: dict) -> tuple[bytes, bytes, bytes, bytes, str, str]:
    schema = require_path(doc, "schema")
    version = require_path(doc, "version")
    if schema != "north-shadow.attestation":
        die(f"Unexpected schema: {schema}")
    if version != 1:
        die(f"Unsupported schema version: {version}")

    algorithm = require_path(doc, "content", "hash", "algorithm")
    expected_hash = require_path(doc, "content", "hash", "value")
    content_b64 = require_path(doc, "content", "value")
    sig_b64 = require_path(doc, "proof", "signature", "value")
    tsq_b64 = require_path(doc, "proof", "timestamp", "query", "value")
    tsr_b64 = require_path(doc, "proof", "timestamp", "response", "value")

    content = b64decode_field(content_b64, "content.value")
    signature = b64decode_field(sig_b64, "proof.signature.value")
    tsq = b64decode_field(tsq_b64, "proof.timestamp.query.value")
    tsr = b64decode_field(tsr_b64, "proof.timestamp.response.value")

    actual_hash = compute_hash(content, algorithm)
    if actual_hash.lower() != str(expected_hash).lower():
        die("Embedded content hash does not match proof bundle")

    return content, signature, tsq, tsr, algorithm, expected_hash


def validate_live_input(input_path: Path, expected_content: bytes, algorithm: str, expected_hash: str) -> None:
    if not input_path.is_file():
        die(f"Input file not found: {input_path}", code=3)

    live_bytes = input_path.read_bytes()
    if live_bytes != expected_content:
        die("Input file bytes do not match embedded content bundle")

    actual_hash = compute_hash(live_bytes, algorithm)
    if actual_hash.lower() != str(expected_hash).lower():
        die("Input file hash does not match proof bundle")


def main() -> None:
    args = parse_args()
    proof_path = Path(args.proof)
    doc = load_json(proof_path)

    content, signature, tsq, tsr, algorithm, expected_hash = validate_bundle_structure(doc)

    if args.input:
        validate_live_input(Path(args.input), content, algorithm, expected_hash)

    run_openssl_verify(content, signature)
    run_timestamp_verify(tsq, tsr)

    if args.input:
        print(f"Valid: {args.input}")
    else:
        print(f"Valid: {args.proof}")


if __name__ == "__main__":
    main()