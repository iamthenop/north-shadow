---
layout: post
title: "Handbook of Implied Cryptography"
subtitle: "Part II: When Assumptions Become Protocol"
date: 2026-04-15
author: "Penuel Lascano"

categories:
  - security-architecture
  - cryptography
  - systems-thinking

tags:
  - cryptography
  - software-architecture
  - protocol-design
  - security-engineering
  - lifecycle

series: "Handbook of Implied Cryptography"
series_number: 2

permalink: /implied-cryptography/assumed-protocol/
---

# Part II: When Assumptions Become Protocol
### Handbook of Implied Cryptography

Part I described how cryptography becomes implied.

Libraries hide complexity.  
Parameters disappear from interfaces.  
Defaults replace explicit design.

The system still works.

So the assumptions accumulate.

Over time they spread.

Across services.  
Across payloads.  
Across databases.

Eventually they stop being implementation details.

They become the protocol.

---
## Implementation Is Flexible

Inside a single application, cryptographic choices are easy to change.

A library can be replaced.  
An algorithm can be upgraded.  
A function can generate IVs differently.

The change remains local.

Tests pass.  
The application deploys.

Nothing else depends on the decision.

---
## Protocols Are Not Flexible

A protocol is different.

It defines how systems interpret data.

Payload structures.  
Token formats.  
Encrypted fields.

Once these structures leave a service boundary, they become shared assumptions.

Multiple systems begin to rely on them.

Clients parse them.  
Databases store them.  
APIs return them.

Changing them becomes difficult.

---
## The Opaque Payload

Many systems eventually produce a familiar artifact.

A single opaque field.

A token.  
A payload.  
A string representing encrypted data.

The cryptographic structure disappears from view.

Algorithm.  
Mode.  
IV.  
Authentication tag.

All packed together.

Often encoded again.

Base64 inside JSON inside HTTP.

The payload becomes convenient.

Transportable.  
Serializable.  
Easy to pass through systems.

But difficult to interpret.

Inside the payload, structure still exists.

Offsets appear.  
Fields have assumed lengths.  
Certain bytes are interpreted as metadata.

These details are rarely documented.

They survive as implementation knowledge.

Sometimes a field is reserved but never used.

The space remains.

A strange appendage at the edge of the payload.

Future developers discover it years later.

They search the codebase for its meaning.

Often there is none.

The protocol simply remembers a decision that was never completed.

---
## Copy-Paste Cryptography

Implementation patterns spread quickly.

A helper function encrypts a payload.  
Another service copies the same code.  
A third team wraps it in a utility library.

Soon dozens of systems depend on the same pattern.

No one remembers where it originated.

Or why it was written that way.

The pattern becomes institutional knowledge.

A silent standard.

---
## The Token Becomes an Identifier

Opaque tokens illustrate the pattern clearly.

A service issues a token.

Clients store it.  
Other services validate it.  
Infrastructure passes it through unchanged.

The token contains cryptographic structure.

But that structure is rarely visible.

The system treats the token as an identifier.

A string.

Not a cryptographic artifact.

Its interpretation depends entirely on hidden assumptions.

---
## Structural Hardening

At first these decisions are harmless.

Local.  
Convenient.  
Practical.

But once the data format spreads across systems, the assumptions harden.

Clients depend on the structure.  
Logs capture the format.  
Databases store the representation.

Changing the cryptography now requires changing the payload.

And payload formats behave like protocols.

They resist change.

---
## Quiet Transition

The transition rarely happens intentionally.

A library default becomes a helper function.  
A helper function becomes a shared utility.  
The utility shapes a payload format.

Soon the payload travels everywhere.

By then the decision is no longer local.

It is infrastructure.

---

## Structural Truth

Cryptography begins as implementation.

But systems rarely keep it there.

Over time, the implementation leaks into the protocol.

And protocols remember every assumption.

Even the ones no one meant to make.