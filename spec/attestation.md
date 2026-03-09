# Attestation Bundle

## Purpose

The attestation bundle is a portable proof object for published markdown content.

It exists to preserve, in one explicit structure:

- the exact markdown payload that was attested
- the cryptographic proof over that payload
- the timestamp material associated with that proof
- optional human-friendly metadata for indexing and browsing

The bundle is designed to make cryptographic structure visible and durable. It avoids reliance on repository paths, local filenames, or operational conventions that are only obvious within one implementation.

## Design intent

The bundle is a container, not the cryptographic subject.

The signed subject is the exact markdown file bytes represented in `content.value`.

The bundle may also carry convenience metadata, but convenience metadata is not part of the signed subject unless a future schema version explicitly states otherwise.

This distinction matters.

The bundle should make it obvious which fields are:
- attested content
- proof material
- descriptive metadata

Nothing should be implied by placement, naming, or repository convention alone.

## Structure

A bundle contains four top-level concerns:

- `schema`
- `version`
- `content`
- `metadata`
- `proof`

### `schema`

A stable schema identifier for the object type.

Example:

```json
"schema": "north-shadow.attestation"