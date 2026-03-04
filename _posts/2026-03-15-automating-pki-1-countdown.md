---
layout: post
title: "Automating PKI at Scale: An Architectural Perspective"
subtitle: "Part 1: The Countdown Has Started"
date: 2026-03-15
author: "Penuel Lascano"
categories: [pki, automation, architecture]
tags: [tls, certificate-lifecycle]
series: "Automating PKI at Scale"
series_number: 1
permalink: /automating-pki-at-scale/part-1-countdown/
---

# Part 1: The Countdown Has Started
### Automating PKI at Scale: An Architectural Perspective  

Today, March 15, 2026, the certificate lifetime reduction schedule enters its next phase.

It has started.

Public TLS certificates are now limited to 200 days.

The remaining reductions are already scheduled:

- March 15, 2027 — 100 days
- March 15, 2029 — 47 days

This is not advisory guidance. It is enforced industry policy.
The constraint has changed.

##

Under 398-day certificates, renewal typically occurred once per year.

At 200 days, that becomes twice per year.
At 100 days, three to four times per year.
At 47 days, seven to eight times per year.

The team size likely does not increase at the same rate.
The change process does not simplify.
The dependency graph does not shrink.

If renewal is still manual, workload multiplies directly with frequency.
Manual renewal will become unsustainable.

##

There is a second constraint that receives less attention.

The reuse period for domain validation is being reduced to 10 days.
Validation artifacts (DNS records, HTTP tokens, etc.) cannot be reused indefinitely between renewals.

At annual cadence, this rarely surfaces as friction.
As lifetimes shrink, validation becomes a recurring dependency.

If DNS ownership, routing control, or change discipline spans teams, each renewal introduces coordination.

Frequency increases.
Interaction increases.
Slack decreases.

##

Many environments rely on expiry monitoring.

Monitoring detects drift.
It does not remove it.

If renewal begins with an alert, you are already coordinating:

- Change windows
- Application owners
- Network dependencies
- Trust store propagation
- Deployment validation

At annual cadence, this is manageable.
At quarterly cadence, it becomes friction.
At sub-quarter cadence, it becomes structural load.

## Structural Reality

Most renewal processes were designed when certificates lasted years.

Calendar tracking was sufficient.
Change tickets were occasional.
Institutional memory filled the gaps.

The constraint changed. → The process did not.

##

Over the next several posts, I’ll explore key considerations for operating in this new reality:

- Discovery without creating governance silos
- Working with CMDB rather than around it
- Automation in disciplined change environments
- Deployment guarantees, not assumptions
- High-assurance and HSM-backed considerations
- TLS inspection as a lifecycle dependency
- And what this means for cryptographic agility

The countdown has started. Deadlines are set.
Design decisions made during the 200-day phase will determine stability in the 47-day phase.
There is still time to design deliberately.
