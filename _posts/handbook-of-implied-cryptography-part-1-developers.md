---
layout: post
title: "Handbook of Implied Cryptography"
subtitle: "Part I: Why Developers Assume Cryptography"
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
series_number: 1

permalink: /implied-cryptography/assumed-cryptography/
---

# Part I: Why Developers Assume Cryptography
### Handbook of Implied Cryptography

Modern software rarely begins with cryptography.

It begins with a feature.

An API endpoint.  
A mobile application.  
A service exchanging data with another service.

Security enters later.

Often as a library.

---
## The Advice Was Correct

For years the guidance has been consistent.

Do not implement cryptography yourself.  
Use established libraries.

This advice is correct.

Cryptography is subtle.  
Mistakes are expensive.

But something quiet followed.

Many systems stopped designing cryptography at all.

The library became the architecture.

---
## The Abstraction

Most developers never implement cryptography directly.

They enable it.

A framework enables HTTPS.  
A library signs tokens.  
An SDK encrypts a payload.

Libraries simplify cryptography for good reasons.

They remove dangerous choices.  
They generate keys.  
They select safe defaults.

But they also change how developers perceive the system.

Security begins to look like a capability of the library.

Not a property of the architecture.

The dependency is installed.

The problem appears solved.

---
## Parameters Developers Avoid

Cryptography demands context.

Initialization vectors.  
Algorithm identifiers.  
Modes of operation.  
Key identifiers.

None of these fields carry business meaning.

To the developer implementing an API, they feel like friction.

Another parameter to pass through a function.  
Another field in a payload.

So the instinct appears quickly.

Hide them.

---
## When Parameters Become Implicit

Once hidden, the parameters do not disappear.

They become implicit.

The algorithm is fixed inside a helper function.  
The mode is implied by the library.  
The IV is generated automatically.

Sometimes it is not even generated.

It is assumed.

Some cryptographic APIs allow this.  
Even certain HSM interfaces permit an implicit initialization vector if the calling system omits one.

Modern libraries correctly generate IVs automatically.

This prevents dangerous mistakes.

But the IV still exists.

It must be stored.  
It must travel with the ciphertext.  
It must remain visible to the protocol.

When that structure disappears from the design, the system still encrypts.

But it no longer declares how.

---
## The Compression Instinct

Developers compress complexity whenever they can.

Instead of separate fields, the system produces a single blob.

Ciphertext.  
Authentication tag.  
Metadata.

All packed together.

Often encoded again.

Base64 inside JSON inside HTTP.

The payload becomes convenient to transport.

But difficult to interpret.

---
## Delivery Incentives

Most developers are not rewarded for durability.

They are rewarded for delivery.

Modern development operates on short horizons.

Two-week sprints.  
Feature tickets.  
Deployment pipelines.

Success is measured when the feature ships.

Not years later when the system must evolve.

---
## The Sprint Horizon

Cryptography lives on a longer timeline.

Algorithms age slowly.  
Keys persist for years.  
Trust anchors outlive entire teams.

The developer implementing encryption today will likely not be present when the system must change.

So the system optimizes for the present.

Libraries that remove ceremony.  
Frameworks that “just work.”

Security becomes something the environment provides.

---
## Security as an Environmental Property

From inside the application code, everything appears secure.

TLS connections succeed.  
Tokens validate.  
Secrets decrypt.

The system behaves correctly.

So the assumption becomes reinforced.

Cryptography is already handled.

---
## When Implementation Becomes Protocol

Library defaults begin as implementation details.

Over time they leak outward.

Into payload formats.  
Into database records.  
Into API responses.

Eventually they become the protocol.

And protocols are difficult to change.

---
## The Quiet Beginning

Assumed cryptography rarely begins with negligence.

It begins with convenience.

Then abstraction.  
Then habit.

The system still works.

So the assumptions accumulate.
