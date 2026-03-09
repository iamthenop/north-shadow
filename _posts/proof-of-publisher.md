---
layout: post
title: "Proof of Publisher"
subtitle:
date: 2026-03-12
author: "Penuel Lascano"
categories: [security, authorship, provenance]
tags: [provenance, authorship, signing, timestamping, publishing]
permalink: /proof-of-publisher/
---

# Proof of Publisher

Artifacts are easy to publish.

Authorship is harder to prove.

Most publishing systems optimize for distribution.

Very few preserve provenance.

---

## Publishing Is Not Proof

Modern platforms make publishing trivial.

Press a button.
Commit a file.
Push to a platform.

An artifact appears.

But the artifact alone proves nothing.

Accounts can be compromised.
Content can be copied.
Repositories can be mirrored.

The artifact spreads.

Authorship becomes narrative.

---

## Artifacts Drift

Digital artifacts do not remain where they were created.

They are forked.
Archived.
Quoted.
Mirrored.

This is not a flaw.

It is how the internet works.

But drift erodes origin.

Eventually the artifact exists everywhere while its provenance becomes uncertain.

---

## Engineering Already Solved This

In other domains, this problem is treated as fundamental.

Software packages are signed.

Container images are attested.

Supply chains record provenance.

In these systems, artifacts are not trusted simply because they exist.

Artifacts carry proof.

---

## Proof of Publisher

Recently I added a small mechanism to my writing workflow.

I call it **Proof of Publisher**.

Each article is treated as an artifact.

Before publication, the artifact is cryptographically signed and timestamped.

This creates a binding between three things:

1. the artifact
2. the author
3. the moment of publication

The platform may change.

The proof does not.

---

## PUSH / POP

The internal mechanism is intentionally mechanical.

**PUSH** creates the signed artifact.

**POP** extracts the proof that the publisher authored it.

The artifact can travel.

The proof remains attached.

---

## Canonical Record

For my own writing, the canonical record lives in a public repository called **North Shadow**.

Each article exists there first as a signed Markdown artifact.

The repository preserves the artifact, its revision history, and its cryptographic proof of authorship.

Distribution platforms may change.

The artifact record does not.

If you are curious what a signed article artifact looks like, the record is public.

**North Shadow — canonical artifact record**  
https://github.com/iamthenop/north-shadow/

---

## Quiet Provenance

This mechanism is not meant to prevent copying.

Copying is inevitable.

Its purpose is simpler.

To preserve authorship.

Artifacts drift.

Proof survives.

---

## Structural Reality

Publishing creates artifacts.

Proof of publisher preserves origin.

Quietly.