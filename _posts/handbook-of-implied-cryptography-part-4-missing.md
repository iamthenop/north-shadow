---
layout: post
title: "Handbook of Implied Cryptography"
subtitle: "Part IV: The Missing Architect"
date: 2026-04-20
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
series_number: 4

permalink: /implied-cryptography/missing-architect/
---

# Part IV: The Missing Architect
### Handbook of Implied Cryptography

Part III described cryptographic drift.

Systems accumulate structure.  
Formats persist.  
Assumptions harden.

Over time the system stiffens.

Eventually it becomes brittle.

At that point a question appears.

Who owns the cryptography?

In many systems, no one does.

---
## Local Decisions

Software systems are rarely designed all at once.

They grow.

A service introduces encryption for a payload.  
Another team adds token signing.  
A third integrates a hardware security module.

Each decision solves a local problem.

The system moves forward.

But no one defines the boundaries.

---
## Policy Is Not Architecture

Many organizations do have guidance.

Sensitive data must be encrypted.  
Keys must be protected.  
Approved algorithms must be used.

These rules are important.

But they are not architecture.

They do not define:

Where cryptography belongs.  
How identifiers are assigned.  
How key lifecycles evolve.  
How protocols adapt when algorithms change.

So the implementation decisions remain local.

---
## Device Thinking

In some environments cryptography grows around devices.

Hardware security modules introduce their own operational habits.

Key check values appear in logs.  
Operators reference fragments of key material.  
Identifiers begin to reflect device conventions.

These practices are convenient.

But they shape the system in subtle ways.

The identifier becomes derived from the key.  
The key becomes tied to the device.  
The device becomes embedded in the protocol.

What began as an operational shortcut becomes system structure.

---
## Migration Inheritance

When standards evolve, systems migrate.

Older formats are replaced.  
New key block structures appear.  
Protocols adopt modern mechanisms.

But migrations rarely erase old habits.

Identifiers derived from key fragments.  
Convenience fields embedded in payloads.  
Operational shortcuts preserved for compatibility.

The new system inherits pieces of the old one.

Often unintentionally.

---
## Architectural Silence

Architecture normally removes decisions.

Developers should not choose algorithms.  
They should not design payload structures.  
They should not invent key identifiers.

Those decisions should already exist.

Defined once.

Applied everywhere.

When architecture is absent, the opposite happens.

Every team invents its own pattern.

---
## Parallel Cryptography

Without architectural boundaries, multiple cryptographic systems emerge.

Different payload formats.  
Different key identifiers.  
Different lifecycle assumptions.

Each one works within its own service.

But eventually those systems must interact.

Integration reveals the differences.

---
## Quiet Absence

The absence of cryptographic architecture rarely feels like a failure.

Features ship.  
Systems operate.  
Encryption functions.

The system appears secure.

But no one owns its evolution.

---
## Structural Truth

Cryptographic architecture rarely appears spontaneously.

It must be defined.

Otherwise systems construct it slowly.

Through habits.  
Through shortcuts.  
Through accumulated assumptions.

And by the time the structure is visible, it is already difficult to change.
