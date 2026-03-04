---
layout: post
title: "Automating PKI at Scale: An Architectural Perspective"
subtitle: "Part 3: Protocol Is Not an Operating Model"
date: 2026-03-19
author: "Penuel Lascano"
categories: [pki, automation, architecture]
tags: [tls, certificate-lifecycle]
series: "Automating PKI at Scale"
series_number: 3
permalink: /automating-pki-at-scale/part-3-protocol/
---

# Part 3: Protocol Is Not an Operating Model
### Automating PKI at Scale: An Architectural Perspective

ACME is necessary.
It is not sufficient.

As certificate lifetimes shrink, many conversations default to:

> “Just use ACME.”

Protocol-level automation is an important piece of the solution.
It is not the entire system.

## Different Certificate Classes, Different Lifecycles

Not all certificates behave the same way.

- Public-facing TLS certificates
- Internal service-to-service certificates
- Kubernetes-managed certificates
- Device certificates via SCEP
- Auto-enrolled certificates via Active Directory
- MDM-driven device certificates (Intune, Jamf)

These do not share identical ownership models, renewal triggers, or governance boundaries.

Conflating them leads to architectural confusion.

## ACME Solves Issuance. It Does Not Define Authority.

ACME automates:

- CSR generation
- Domain validation
- Certificate issuance

It does not answer:

- Who authorizes this certificate to exist?
- Who owns the DNS zone?
- Who owns the endpoint?
- What system depends on it?
- What happens if issuance succeeds but deployment fails?

Protocol handles transaction.
Operating model handles accountability.

## Kubernetes Is Not the Entire Estate

In Kubernetes environments, certificate automation often feels “solved.”

Controllers renew. Secrets rotate. Pods reload.

But most enterprises are not Kubernetes-only.

They include:

- Load balancers
- Legacy application servers
- Appliances
- Hybrid cloud workloads
- SaaS integrations
- Device fleets

Automation strategies that assume homogeneous orchestration collapse under heterogeneity.

## Device Enrollment Is a Different Plane

Dynamic SCEP for MDM platforms or auto-enrollment via Active Directory addresses device identity.

Those lifecycles are policy-driven and endpoint-scoped.

They should not be conflated with service-level certificate lifecycle management.

Device enrollment belongs to endpoint identity governance.
Service TLS belongs to application and infrastructure governance.

The control planes are different.

Blurring them introduces ownership ambiguity.

## Structural Reality

ACME is an important mechanism.
It is not a lifecycle strategy.

Certificate lifecycle management requires:

- Ownership clarity
- Boundary definition
- Governance alignment
- Deployment guarantees

Protocol without operating model is partial automation.

And partial automation is where friction accumulates.

##

Next: deployment is where most automation strategies silently fail.
