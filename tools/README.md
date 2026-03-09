# Tools

Utility scripts for publishing markdown posts with cryptographic attestations.

## What this folder does

These scripts support a lightweight publishing workflow for North Shadow:

- publish drafts into `_posts`
- create CMS signatures over markdown content
- request RFC 3161 timestamps from a TSA
- bundle content, signature, and timestamp material into a proof JSON
- validate proof bundles against embedded content

## Main scripts

### `publish.sh`
Shell wrapper for publishing a draft.

### `publish.py`
Core publish workflow:
- materialize post paths
- stamp content
- validate generated proof
- commit changes
- optionally push

### `stamp.sh`
Creates proof artifacts for a markdown file:
- `.p7s`
- `.p7s.tsq`
- `.p7s.tsr`
- `.proof.json`

### `build_attestation.py`
Builds the attestation JSON bundle from content and proof artifacts.

### `extract_metadata.py`
Extracts selected metadata from markdown front matter.

### `validate.sh`
Shell wrapper for attestation validation.

### `validate_attestation.py`
Validates:
- embedded content hash
- CMS signature over content
- RFC 3161 timestamp response
- optional comparison against an external markdown file

## Configuration

Local configuration is expected in:

```text
tools/stamp.conf
