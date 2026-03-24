---
layout: post
title: "Part I: The Illusion of the Big Switch"
subtitle: "PQC Readiness the Boring Way"
author: "Penuel Lascano"
date: 2026-03-23 09:00:00 -0400
categories: [cryptography, security-architecture]
tags: [post-quantum-cryptography, pki, systems-thinking, infrastructure, lifecycle]
series: "PQC Readiness the Boring Way"
series_number: 1
permalink: /pqc-readiness-the-boring-way-part-1/
---

# Part I: The Illusion of the Big Switch
### PQC Readiness the Boring Way

It is autumn.

The season is turning, but not all at once.

At the side of the road, a vine has crossed out of a yard and left a pumpkin there.

Nothing happens to it at midnight.

Weather does the work.  
Mice and squirrels make use of it.  
Something with paws has already inspected the edge.

Time does the rest.

Cryptographic risk accumulates more like that than most people want to admit.

When new cryptographic standards emerge, the industry often imagines a decisive moment of transition.

A coordinated migration.  
A clean replacement.  
Old primitives out. New ones in.

Enterprise systems do not move that way.

There was no universal cutover from SHA-1.  
No single moment replaced RSA-1024 everywhere.  
No day when every endpoint began using a new protocol version at once.

These changes spread gradually through infrastructure.

Some systems move early.  
Others lag.  
Some are isolated instead of replaced.

Cryptography sits deep inside the machinery of an organization. It lives in certificate authorities, firmware, hardware security modules, trust stores, software libraries, and vendor products that move on their own schedules.

A primitive can be deprecated quickly.

The systems around it usually cannot.

---

## No Countdown

There is no visible clock counting down to sudden failure.

What exists instead is gradual wear.

Research progresses.  
Standards mature.  
Hardware capabilities evolve.  
Computing power improves.  
Assumptions that once felt comfortable begin to narrow.

Risk does not arrive as a single event.

It accumulates.

NIST has formalized post-quantum algorithms. That does not create a universal migration date. It changes the direction of travel.

The question is not whether change is coming.

The question is how the system absorbs it.

Certificates expire.  
Keys rotate.  
Hardware is refreshed.  
Applications are rebuilt.  
Vendors release new firmware.

Those are service intervals.

They are the points where change can enter without becoming crisis.

There is no midnight transformation.

There is gradual wear.

Responsible operators plan accordingly.