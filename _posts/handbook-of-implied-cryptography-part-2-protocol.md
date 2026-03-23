---
layout: post
title: "Handbook of Implied Cryptography"
subtitle: "Part II: When Assumptions Become Protocol"
date: 2026-03-10
author: "Penuel Lascano"
categories: [security-architecture, cryptography, systems-thinking]
tags: [cryptography, software-architecture, protocol-design, security-engineering, lifecycle]
series: "Handbook of Implied Cryptography"
series_number: 2
permalink: /implied-cryptography/assumed-protocol/
---

# Handbook of Implied Cryptography  
## Part II — When Implementation Becomes Protocol

By the time most people see the old tin boat, the sequence has already hardened.

The motor has to be in neutral.  
The choke has to sit in the right place.  
The cover comes off and goes back on halfway.  
Someone gives the gas tank a light kick and claps twice.

None of this appears in the shape of the boat itself.

From the shoreline, it is still just a boat.

That is how implementation becomes protocol.

The visible system remains simple.  
The real structure moves into sequence, assumption, and inherited handling.

---

## Implementation Is Flexible

Inside a single application, cryptographic choices are still relatively easy to change.

A library can be replaced.  
An algorithm can be upgraded.  
A helper function can generate IVs differently.

At that stage, the decision is still local. One team can revise it, test it, and ship the change without disturbing much else.

That is what implementation feels like. It is close to the code that made the choice.

---

## Protocols Are Not Flexible

A protocol is different.

A protocol defines how systems interpret data across a boundary. It shapes payloads, token formats, encrypted fields, and assumptions about what the next system will receive.

Once that structure leaves a single service, multiple systems begin to rely on it. Clients parse it. Databases store it. APIs return it. Monitoring systems log it. Integration code quietly learns its shape.

That is when a local decision stops being local.

---

## The Opaque Payload

Most systems eventually produce a familiar artifact: a single opaque field.

A token.  
A payload.  
A string representing encrypted data.

From the outside, it appears simple. One field in the request. One value in the database. One blob passed from system to system.

It only looks simple.

Inside that field, structure still exists. Algorithm choice, mode, IV, authentication tag, version assumptions, and key selection all remain present in some form. They have not disappeared. They have merely been packed together.

That is why opaque payloads are so useful and so dangerous at the same time. They move easily through interfaces because they compress detail into something transportable. But the detail is still there, waiting to be interpreted correctly by the next system that touches it.

The boat works the same way.

From the shoreline, it is only a boat.  
The real structure lives in everything you have to know before you touch the cord.

---

## Hidden Structure

When cryptographic structure is compressed, the system still has to recover it somewhere.

Offsets appear.  
Fields have assumed lengths.  
Metadata is packed into specific positions.  
Certain bytes are treated as if their meaning is obvious.

Over time, that shape becomes familiar to the systems that already depend on it. The parser knows where to look. The helper function knows how to unpack it. The application code learns which parts matter and which parts can be ignored.

But familiarity is not the same thing as clarity.

The structure is still there. It is simply no longer visible in a way that invites inspection.

---

## The Strange Appendage

Sometimes a field is reserved but never truly used. Sometimes a value survives from an older design that no longer exists anywhere else. Sometimes a few bytes remain in the format because removing them would be riskier than explaining them.

Future developers encounter these details as if they were natural.

A length that always appears.  
A flag that no one sets.  
A segment of the payload that gets copied forward without interpretation.

They search the codebase for its purpose. Often they do not find a real answer. What they find instead is repetition.

The protocol simply remembers a decision that was never completed.

---

## Copy-Paste Cryptography

Implementation patterns spread faster than design.

A helper function encrypts a payload. Another service copies it. A third team wraps it in a shared utility. Before long, the pattern is no longer one implementation among many. It is the way the organization does that kind of work.

That spread feels efficient.

It reduces repeated effort.  
It encourages consistency.  
It makes adoption easier.

But it also hardens assumptions. The original implementation may have been local, but repetition turns it into an informal standard long before anyone names it as one.

That is how sequence becomes protocol.

---

## The Payload Becomes an Identifier

At some point, a cryptographic artifact stops being treated as cryptography at all.

A token becomes an identifier.  
A blob becomes a reference.  
A string becomes something the system passes around without interpretation.

This is a subtle shift, but an important one.

Once the payload is treated primarily as an identifier, its internal structure disappears from everyday thought. The application no longer sees a cryptographic object with conditions and metadata. It sees a thing that can be stored, copied, compared, and returned.

The visible system becomes simpler.

The hidden system becomes harder to change.

---

## Structural Hardening

At first these decisions are harmless enough.

They are practical.  
They reduce friction.  
They help software move.

But once the data format spreads across enough systems, the assumptions begin to harden. A client expects the field. A downstream service relies on a specific layout. A datastore preserves the representation exactly as it arrived. A migration script quietly encodes the same assumptions into another layer.

The boat did not become this way all at once.

Something changed.  
A part was replaced.  
A control behaved differently.  
A later decision had to fit an older platform.

Redesigning the whole system would have been too expensive, too disruptive, or simply unnecessary.

So the platform stayed the same.

The sequence carried the change.

---

## The Quiet Transition

No one usually decides to turn implementation into protocol.

The transition happens gradually.

A local helper becomes a shared utility.  
A shared utility shapes a payload.  
A payload travels across a boundary.  
Another system learns to depend on it.

Eventually the original choice is no longer remembered as a choice. It is treated as the natural shape of the system.

By then, the sequence has become part of the boat.