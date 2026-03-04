---
layout: post
title: "Automating PKI at Scale: An Architectural Perspective"
subtitle: "Part 2: Discovery Without Creating a Governance Silo"
date: 2026-03-17
author: "Penuel Lascano"
categories: [pki, automation, architecture]
tags: [tls, certificate-lifecycle]
series: "Automating PKI at Scale"
series_number: 2
permalink: /automating-pki-at-scale/part-2-discovery/
---

# Part 2: Discovery Without Creating a Governance Silo
### Automating PKI at Scale: An Architectural Perspective

Automation begins with visibility.

You cannot automate what you cannot see.

But visibility without governance creates a different failure mode.

Most organizations respond to certificate sprawl with scanning:

- Network sweeps
- Load balancer inspection
- Cloud API enumeration
- CT log correlation

Necessary. → Not sufficient.

## Discovery Is Not Ownership

Discovery tells you a certificate exists.

It does not tell you:

- Who owns it
- Why it exists
- What depends on it

An inventory without ownership is a list of liabilities.

Automation built on unidentified assets cannot be trusted.

## The CMDB Cannot Be Bypassed

Building a parallel “PKI inventory” feels efficient.
It avoids legacy data issues. It avoids reconciliation work.

It also creates a governance fork.

Now there are two sources of truth:

- The CMDB
- The scanner

Automation layered on top of conflicting data will stall at change control.

Discovery should reconcile the CMDB — not replace it.

## Frequency Exposes Drift

Under annual renewal cycles, stale records hide.

At 200 days, drift becomes visible.
At 100 days, it becomes disruptive.
At 47 days, it becomes constant.

Ownership gaps surface immediately.

Decommissioned services linger. DNS zones move. Application owners change.

Shorter lifetimes compress tolerance for inaccuracy.

## Authority Precedes Automation

Before enabling automated renewal, the system must be able to answer:

- Who owns the service?
- Who controls the domain?
- Who authorizes the certificate?

If those answers are unclear, automation becomes governance friction.

Discovery is technical.
Authority is organizational.

Both are required.

## Structural Reality

Certificate lifetime reduction increases frequency.
Frequency increases interaction.
Interaction exposes governance weakness.

Discovery without alignment amplifies it.

Automation cannot compensate for unclear ownership.

##

Next: why protocol-level automation alone does not solve change-discipline environments.
