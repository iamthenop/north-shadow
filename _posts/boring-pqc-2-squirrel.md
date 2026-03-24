---
layout: post
title: "Part II: What Responsible Maintenance Looks Like"
subtitle: "PQC Readiness the Boring Way"
author: "Penuel Lascano"
date: 2026-03-25 09:00:00 -0400
categories: [cryptography, security-architecture]
tags: [post-quantum-cryptography, pki, systems-thinking, infrastructure, lifecycle]
series: "PQC Readiness the Boring Way"
series_number: 2
permalink: /pqc-readiness-the-boring-way-part-2/
---

# Part II: What Responsible Maintenance Looks Like
### PQC Readiness the Boring Way

By morning, the pumpkin is not untouched.

The squirrel has been gathering all summer, a little at a time.

A system that waits for winter will not be ready for winter.

Post-quantum readiness should feel more like that than most organizations expect.

That is why readiness cannot be confined to a project plan.

It has to become a habit.

Post-quantum readiness does not begin with deployment.

It begins with posture.

Not inventory for presentation.  
Not dashboards for reassurance.

Posture.

## Do Not Create New Long-Lived Dependencies

The first discipline is containment.

Do not introduce new long-term dependencies on aging primitives.

That work begins long before any organization decides it is “migrating.”

It begins when new systems are designed, purchased, and deployed.

When deploying new systems:

Prefer shorter certificate lifetimes.  
Avoid hard-coding algorithm assumptions.  
Design interfaces that tolerate larger keys and signatures.  
Ensure libraries can be upgraded without architectural redesign.

This is not migration.

It is how future friction is kept from hardening into structure.

## Use Renewal Cycles with Intent

Most enterprise cryptography already rotates.

Certificates expire.  
Keys are reissued.  
Trust stores change.

Those cycles matter because they already bring systems back into human hands.

Something is reviewed.  
Something is renewed.  
Something is touched on purpose.

These events are not interruptions.

They are opportunities.

Each renewal is a chance to avoid reinforcing yesterday’s assumptions.

Over time the fleet changes.

Quietly.

## Infrastructure Has Its Own Cadence

Cryptography does not exist in isolation.

Hardware support.  
Firmware capabilities.  
Vendor roadmaps.  
Cloud platform releases.

These constraints determine what is possible.

They also determine when change can be absorbed without unnecessary strain.

Responsible maintenance aligns cryptographic evolution with those cycles.

Not ahead of them without reason.  
Not behind them out of neglect.

## Understand What “Ready” Means

Ready does not mean fully migrated.

It does not mean every system has already changed.

It means the system can tolerate change when change arrives.

Algorithms can evolve without architectural surgery.  
Renewal processes can introduce new primitives.  
New deployments do not increase rigidity.

Readiness is structural.

Not completion.

## Measure Drift, Not Panic

Panic compresses thinking.

When uncertainty rises, the instinct is to buy time.

Issue the longer certificate.  
Extend the key.  
Defer rotation.

It feels practical.

It also feels temporary.

That is part of the appeal.

But deferral is not neutral.

Deferred maintenance behaves like compounded interest.

Each extension is small.  
Over time the corrections grow.

Work that could have been absorbed gradually begins to collect in the same future window.

Gradual pressure becomes concentrated replacement.

Maintenance does not disappear.

It accrues.

Drift is the correct metric.

Not whether the work has been “finished.”  
Whether the system is becoming easier to move.

Are new deployments aligned with the direction of travel?  
Are renewal events reducing rigidity or increasing it?  
Is change absorbed through normal service intervals?

Completion percentages create artificial finish lines.

Drift measures trajectory.

If pressure accumulates gradually, readiness is not a race.

It is steady direction.

The worst outcome is not slow migration.

The worst outcome is accumulated correction.

Steady maintenance prevents compounding.