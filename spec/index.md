# North Shadow Index Specification

The North Shadow index provides a cryptographically attestable catalog of
published essays.

While each essay has an independent attestation bundle, the index provides
a verifiable snapshot of the complete publication set at a point in time.

The index itself is signed and timestamped using the same workflow used for
individual posts.

---

## Purpose

The index provides:

- A catalog of published essays
- A mapping between posts and their proof bundles
- A tamper-evident record of the publication set

If a post is removed or altered, the index signature will no longer verify.

---

## Location

The index is stored alongside other cryptographic artifacts.

```
_timestamps/index.json
```

Associated signature and timestamp artifacts may include:

```
_timestamps/index.json.p7s  
_timestamps/index.json.p7s.tsq  
_timestamps/index.json.p7s.tsr
```

---

## Design Principles

### Deterministic

The index must be deterministic. It should contain only stable identifiers
and hashes.

### Minimal

The index does not duplicate information already present in proof bundles.

### Tamper Evident

The index is protected by a CMS signature and an RFC 3161 timestamp.

---
## Structure

The index contains:

- schema identifier
- schema version
- ordered list of posts

Each entry maps a post to its proof bundle.

---
## Example

```json
{
  "schema": "north-shadow.index",
  "version": 1,
  "posts": [
    {
      "post": "_posts/2026-03-06-before-there-was-gps.md",
      "proof": "_timestamps/2026-03-06-before-there-was-gps.md.proof.json",
      "proof_sha256": "d4c6e3c8..."
    }
  ]
}
```
---
### Verification

Verification of the index requires:

1. Validate the CMS signature over index.json
2. Validate the RFC 3161 timestamp response
3. Confirm the hashes of listed proof bundles

After validating the index, individual proof bundles may be validated
independently.

---
### Relationship to Attestation Bundles

The index does not replace attestation bundles.

Each essay continues to have its own proof bundle.

The index simply provides a verifiable catalog of those bundles.

---
### Versioning

The schema version field allows future revisions to the index format while
preserving compatibility with earlier versions.