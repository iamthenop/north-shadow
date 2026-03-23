---
layout: post
title: "Handbook of Implied Cryptography"
subtitle: "Part V: Durable Cryptography"
date: 2026-04-22
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
series_number: 5

permalink: /implied-cryptography/durable-cryptography/
---

## Part V: Durable Cryptography
### Handbook of Implied Cryptography

Part IV described the missing architect.

Local decisions accumulated.  
Operational habits shaped identifiers.  
Protocols inherited implementation details.

Over time the system stiffened.

Eventually it became brittle.

At that point the system discovers something important.

Cryptography is not a feature.

It is infrastructure.

---
## Infrastructure Behaves Differently

Features can be replaced.

A new API can be introduced.  
A service can be rewritten.  
A library can be swapped.

Infrastructure behaves differently.

It connects systems.  
It persists across migrations.  
It survives organizational change.

Cryptography lives in this layer.

Which means its design must survive time.

---
## The Lifecycle Problem

Most cryptographic failures are not failures of mathematics.

The primitives are usually sound.

The failures appear in the lifecycle.

Keys are not rotated.  
Algorithms cannot change.  
Identifiers cannot evolve.  
Payloads cannot adapt.

The system continues to operate.

But its ability to evolve quietly disappears.

---
## Explicit Structure

Durable systems make cryptographic structure visible.

Algorithms are identified.  
Modes are declared.  
Key identifiers exist independently of key material.  
Metadata travels with the ciphertext.

Nothing is implied.

The system states the conditions under which the data can be interpreted.

Future systems can understand it.

---
## Separation of Concerns

Durable systems separate responsibilities.

Developers build applications.

Architects define cryptographic boundaries.

Operators manage keys.

No single layer carries the entire burden.

When these responsibilities blur, cryptography becomes accidental.

---
## Identifiers Before Keys

A durable system assigns identity before it generates secrets.

Keys are created.  
But identifiers already exist.

Key material rotates.

Identifiers persist.

This allows systems to change keys without changing the system that references them.

---
## Protocols That Expect Change

Durable protocols assume the future will be different.

Algorithms will age.  
Key sizes will grow.  
New primitives will appear.

Protocols leave space for that change.

Version fields exist.  
Metadata travels with the payload.  
Formats do not assume fixed cryptographic structure.

The system expects evolution.

---
## Automation as Maintenance

Automation often appears in cryptographic discussions.

Usually as a way to simplify deployment.

But its real purpose is maintenance.

Certificates renew automatically.  
Keys rotate on schedule.  
Protocols adapt without manual intervention.

Automation does not eliminate lifecycle management.

It enforces it.

---
## The Quiet Principle

Durable cryptography does not depend on remembering decisions.

It depends on systems that declare them.

Explicit identifiers.  
Explicit metadata.  
Explicit boundaries.

When the structure is visible, the system can evolve.

---
## Structural Truth

Cryptographic systems rarely fail because encryption was absent.

They fail because evolution was impossible.

Durable cryptography is not implemented.

It is maintained.
