---
layout: post
title: "Handbook of Implied Cryptography"
subtitle: "Part I: Why Developers Assume Cryptography"
date: 2026-03-10
author: "Penuel Lascano"
categories: [security-architecture, cryptography, systems-thinking]
tags: [cryptography, software-architecture, protocol-design, security-engineering, lifecycle]
series: "Handbook of Implied Cryptography"
series_number: 1
permalink: /implied-cryptography/why-developers-assume-cryptography/
---

# Handbook of Implied Cryptography  
## Part I — Why Developers Assume Cryptography

There is a certain sequence to starting the motor on the old tin boat at the cottage.

From the shoreline, it looks simple. Fuel. Motor. Pull cord. Go.

It only looks simple.

The fuel mix has to be right. The motor has to be set to neutral. The choke has to sit in a narrow middle position. You cannot prime it too much or it floods. Before starting, the cover comes off and goes back on halfway. Then there is one light pull before the real one.

Someone lightly kicks the gas tank and claps twice.

And even then, it never starts on the first pull.

None of this is written down.

The people who know the boat simply assume you would know.

By then, the sequence has become part of the boat.

---

## The Advice Was Correct

For years the guidance has been consistent: do not implement cryptography yourself; use established libraries.

This advice is correct. Cryptography is subtle, edge cases matter, and small mistakes can survive in production for years.

Libraries solve a real problem. They remove dangerous choices, narrow the space for error, and make strong mechanisms available to ordinary application teams.

The problem begins when teams stop there.

Cryptography stops being treated as a property of the system and starts being treated as a capability that has already been delivered.

The library became the architecture.

---

## The Abstraction

Most developers never implement cryptography directly. They enable it through a framework that turns on HTTPS, a library that signs tokens, or an SDK that encrypts a payload.

This changes how the work feels. The developer does not see a cryptographic system. They see an API call, a helper function, or a configuration option.

That is the power of abstraction. It makes difficult mechanisms easier to use. It also makes them easier to stop thinking about.

A secure connection succeeds, a token validates, and a ciphertext is produced. From the point of view of the application, the problem appears solved.

Once security is experienced as a feature of the dependency, it stops being experienced as a property of the architecture.

---

## Parameters Developers Avoid

Cryptography demands context. It rarely consists of ciphertext alone.

There are always other pieces around it: initialization vectors, algorithm identifiers, modes of operation, and key identifiers. These fields matter to the mechanism, to storage, and to interpretation later.

But they do not usually matter to the work the system believes it is doing. They do not help a user complete a purchase, return a response, or make a feature demo look cleaner.

To the developer implementing the path, they often feel like friction. Another parameter has to pass through a function. Another field has to survive in a payload. Another value has to be preserved in a datastore.

That is when a pattern begins.

The system starts looking for places to hide the structure.

---

## When Parameters Become Implicit

Once hidden, the parameters do not disappear. They become implicit.

The algorithm is fixed inside a helper function. The mode is implied by the library. The IV is generated automatically.

Sometimes that automatic behavior is exactly what should happen. Modern libraries often generate IVs correctly, and that prevents dangerous manual mistakes.

But automatic generation does not remove the IV from the system. The IV still exists. It still has to be stored, travel with the ciphertext, and remain visible to whatever needs to interpret the data later.

Some systems lose sight of that. The parameter becomes something the library knows, but the protocol does not clearly declare.

The encryption still runs and the output still looks correct, but part of the structure has moved out of the design and into assumption.

That shift can go further. Some cryptographic APIs permit omitted values and fill in the blanks internally. In certain legacy integrations around HSMs, an initialization value may be assumed if the calling system does not provide one. The mechanism still operates.

The system still encrypts. It no longer clearly declares how.

---

## The Compression Instinct

Developers compress complexity whenever they can, and this is usually a rational response to delivery pressure.

Instead of carrying separate values through the system, teams combine them. Ciphertext, authentication tag, and metadata are packed together and then encoded again: Base64 inside JSON inside HTTP.

The result is convenient. It moves easily through application boundaries, fits inside existing interfaces, and allows cryptographic detail to disappear behind a single field.

That convenience is real.

But the structure did not vanish. It was compressed.

Compressed structure is still structure. It is simply harder to inspect, document, and evolve.

---

## Delivery Incentives

Most developers are not rewarded for durability.

They are rewarded for delivery.

That is not usually because anyone sat down and chose fragility.

It is how the work is counted.

Modern development runs on short horizons.  
Two-week sprints. Feature tickets. Deployment pipelines.

Credit is given when the path works and the release goes out on time.

Durability is harder to point at. It often has no ticket, no visible milestone, and no demo.

So it is easy for it to lose.

Not because it was rejected.  
Because it was never the unit being measured.

---

## The Sprint Horizon

Cryptography lives on a different timeline. Algorithms age slowly, keys persist for years, and trust anchors often outlive whole teams.

That creates a mismatch. The developer writing the encryption path today is usually working on the next sprint, while the cryptographic consequences may not become visible for years.

Those are not the same horizon.

A system built for delivery will naturally optimize for delivery. Libraries that reduce ceremony are preferred. Framework defaults that remove decisions are preferred. Interfaces that keep the payload small are preferred.

None of this is irrational. It is exactly what the surrounding incentives produce.

The sprint rewards completion in the present.

Cryptography has to survive contact with the future.

---

## Security as an Environmental Property

From inside the application code, everything appears secure. TLS connections succeed, tokens validate, and secrets decrypt.

That reinforces a particular belief: cryptography is already handled.

It feels ambient, like part of the runtime, the platform, or the environment the application already lives inside.

That perception is powerful because it changes the developer’s role in their own mind. They are no longer shaping a cryptographic system. They are calling into one that seems to already exist.

That is why the assumptions feel reasonable.

No one stops to ask what conditions it was actually prepared for.

---

## When Implementation Becomes Protocol

Library defaults often begin as implementation details.

At first they are local.

A helper function chooses the algorithm.  
A wrapper decides how metadata is packed.  
A service defines how ciphertext is represented in a payload.

Those decisions feel reversible.

Then the representation starts moving.

It enters payload formats, database records, and API responses.  
Other systems begin to rely on it.

At that point the decision is no longer local.

It has crossed a boundary.

That is when implementation begins turning into protocol.

And protocols are difficult to change.

---

## The Quiet Beginning

Assumed cryptography rarely begins with negligence. It begins with convenience, then abstraction, then delivery pressure, then habit.

None of these forces look dramatic while they are happening. The system still works, the path still succeeds, and the feature still ships.

That is why the assumptions survive. They do not arrive as obvious mistakes. They arrive as reasonable simplifications that never have to defend themselves.

So the assumptions accumulate.