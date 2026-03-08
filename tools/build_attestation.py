#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a north-shadow attestation bundle from markdown and proof artifacts."
    )
    parser.add_argument("--input", required=True, help="Path to the markdown file")
    parser.add_argument("--signature", required=True, help="Path to the CMS signature file")
    parser.add_argument("--tsq", required=True, help="Path to the RFC 3161 timestamp query")
    parser.add_argument("--tsr", required=True, help="Path to the RFC 3161 timestamp response")
    parser.add_argument("--metadata", required=True, help="Path to extracted metadata JSON")
    parser.add_argument("--hash-algorithm", required=True, help="Hash algorithm name, e.g. sha256")
    parser.add_argument("--output", required=True, help="Output attestation JSON path")
    return parser.parse_args()


def b64_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def hash_bytes(data: bytes, algorithm: str) -> str:
    try:
        h = hashlib.new(algorithm)
    except ValueError as exc:
        raise SystemExit(f"Unsupported hash algorithm: {algorithm}") from exc
    h.update(data)
    return h.hexdigest()


def read_json_file(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit(f"Metadata file must contain a JSON object: {path}")
    return data


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    sig_path = Path(args.signature)
    tsq_path = Path(args.tsq)
    tsr_path = Path(args.tsr)
    metadata_path = Path(args.metadata)
    output_path = Path(args.output)

    for path in (input_path, sig_path, tsq_path, tsr_path, metadata_path):
        if not path.is_file():
            raise SystemExit(f"Required file not found: {path}")

    content_bytes = input_path.read_bytes()
    signature_bytes = sig_path.read_bytes()
    tsq_bytes = tsq_path.read_bytes()
    tsr_bytes = tsr_path.read_bytes()
    metadata = read_json_file(metadata_path)

    doc: dict = {
        "schema": "north-shadow.attestation",
        "version": 1,
        "content": {
            "media_type": "text/markdown",
            "encoding": "base64",
            "hash": {
                "algorithm": args.hash_algorithm,
                "value": hash_bytes(content_bytes, args.hash_algorithm),
            },
            "value": b64_bytes(content_bytes),
        },
        "proof": {
            "signature": {
                "type": "cms",
                "encoding": "base64",
                "value": b64_bytes(signature_bytes),
            },
            "timestamp": {
                "query": {
                    "type": "rfc3161-tsq",
                    "encoding": "base64",
                    "value": b64_bytes(tsq_bytes),
                },
                "response": {
                    "type": "rfc3161-tsr",
                    "encoding": "base64",
                    "value": b64_bytes(tsr_bytes),
                },
            },
        },
    }

    clean_metadata = {}
    for key in ("series", "title"):
        value = metadata.get(key)
        if isinstance(value, str) and value.strip():
            clean_metadata[key] = value.strip()

    if clean_metadata:
        doc["metadata"] = clean_metadata

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()