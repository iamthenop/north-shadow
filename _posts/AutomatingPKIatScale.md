---
title: Automating PKI at Scale: An Architectural Perspective
author: Penuel Lascano
publication: North Shadow
first_draft: 2026-02-22
first_published: 2026-03-15
version: 1.0
---

# Automating PKI at Scale — Part 1  
## Part 1: The Countdown Has Started

Today, March 15, 2026, the certificate lifetime reduction schedule enters its next phase.

It has started.

Public TLS certificates are now limited to 200 days.

The remaining reductions are already scheduled:

- March 15, 2027 — 100 days
- March 15, 2029 — 47 days

This is not advisory guidance. It is enforced industry policy.
The constraint has changed.

Under 398-day certificates, renewal typically occurred once per year.

At 200 days, that becomes twice per year.
At 100 days, three to four times per year.
At 47 days, seven to eight times per year.

The team size likely does not increase at the same rate.
The change process does not simplify.
The dependency graph does not shrink.

If renewal is still manual, workload multiplies directly with frequency.
Manual renewal will become unsustainable.

There is a second constraint that receives less attention.

The reuse period for domain validation is being reduced to 10 days.
Validation artifacts (DNS records, HTTP tokens, etc.) cannot be reused indefinitely between renewals.

At annual cadence, this rarely surfaces as friction.
As lifetimes shrink, validation becomes a recurring dependency.

If DNS ownership, routing control, or change discipline spans teams, each renewal introduces coordination.

Frequency increases.
Interaction increases.
Slack decreases.

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

### Structural Reality

Most renewal processes were designed when certificates lasted years.

Calendar tracking was sufficient.
Change tickets were occasional.
Institutional memory filled the gaps.

The constraint changed. → The process did not.

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

---

## Automating PKI at Scale — Part 2  
### Part 2: Discovery Without Creating a Governance Silo

Automation begins with visibility.

You cannot automate what you cannot see.

But visibility without governance creates a different failure mode.

Most organizations respond to certificate sprawl with scanning:

- Network sweeps
- Load balancer inspection
- Cloud API enumeration
- CT log correlation

Necessary. → Not sufficient.

### Discovery Is Not Ownership

Discovery tells you a certificate exists.

It does not tell you:

- Who owns it
- Why it exists
- What depends on it

An inventory without ownership is a list of liabilities.

Automation built on unidentified assets cannot be trusted.

### The CMDB Cannot Be Bypassed

Building a parallel “PKI inventory” feels efficient.
It avoids legacy data issues. It avoids reconciliation work.

It also creates a governance fork.

Now there are two sources of truth:

- The CMDB
- The scanner

Automation layered on top of conflicting data will stall at change control.

Discovery should reconcile the CMDB — not replace it.

### Frequency Exposes Drift

Under annual renewal cycles, stale records hide.

At 200 days, drift becomes visible.
At 100 days, it becomes disruptive.
At 47 days, it becomes constant.

Ownership gaps surface immediately.

Decommissioned services linger. DNS zones move. Application owners change.

Shorter lifetimes compress tolerance for inaccuracy.

### Authority Precedes Automation

Before enabling automated renewal, the system must be able to answer:

- Who owns the service?
- Who controls the domain?
- Who authorizes the certificate?

If those answers are unclear, automation becomes governance friction.

Discovery is technical.
Authority is organizational.

Both are required.

### Structural Reality

Certificate lifetime reduction increases frequency.
Frequency increases interaction.
Interaction exposes governance weakness.

Discovery without alignment amplifies it.

Automation cannot compensate for unclear ownership.

Next: why protocol-level automation alone does not solve change-discipline environments.

---

## Automating PKI at Scale — Part 3  
### Part 3: Protocol Is Not an Operating Model

ACME is necessary.
It is not sufficient.

As certificate lifetimes shrink, many conversations default to:

> “Just use ACME.”

Protocol-level automation is an important piece of the solution.
It is not the entire system.

### Different Certificate Classes, Different Lifecycles

Not all certificates behave the same way.

- Public-facing TLS certificates
- Internal service-to-service certificates
- Kubernetes-managed certificates
- Device certificates via SCEP
- Auto-enrolled certificates via Active Directory
- MDM-driven device certificates (Intune, Jamf)

These do not share identical ownership models, renewal triggers, or governance boundaries.

Conflating them leads to architectural confusion.

### ACME Solves Issuance. It Does Not Define Authority.

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

### Kubernetes Is Not the Entire Estate

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

### Device Enrollment Is a Different Plane

Dynamic SCEP for MDM platforms or auto-enrollment via Active Directory addresses device identity.

Those lifecycles are policy-driven and endpoint-scoped.

They should not be conflated with service-level certificate lifecycle management.

Device enrollment belongs to endpoint identity governance.
Service TLS belongs to application and infrastructure governance.

The control planes are different.

Blurring them introduces ownership ambiguity.

### Structural Reality

ACME is an important mechanism.
It is not a lifecycle strategy.

Certificate lifecycle management requires:

- Ownership clarity
- Boundary definition
- Governance alignment
- Deployment guarantees

Protocol without operating model is partial automation.

And partial automation is where friction accumulates.

Next: deployment is where most automation strategies silently fail.

---

## Automating PKI at Scale — Part 4  
### Part 4: Issuance Is Not Deployment

Issuing a certificate is a transaction.
Deploying it is a change.

Those are not the same thing.

ACME can complete successfully.
The CA can return a valid certificate.
The renewal pipeline can report “success.”

And the service can still present the old certificate.

Issuance without verified deployment is not automation.
It is optimistic scripting.

---

### Deployment Is a Control Plane

Certificate renewal touches:

- Load balancers
- Reverse proxies
- Application servers
- Containers
- Appliances
- Trust stores

Each of these has its own reload behavior.

Some hot-reload.
Some require restart.
Some cache aggressively.
Some fail silently.

Automation that stops at file write assumes behavior.
Change management exists because assumptions fail.

---

### Change Discipline Does Not Disappear

There is a common belief that automation eliminates change management.

It does not.
It transforms it.

Instead of approving each renewal, governance must approve:

- The automation pattern
- The deployment mechanism
- The validation logic
- The rollback strategy

Once approved, renewals can execute within that guardrail.

Without that discipline, automated deployment becomes untracked configuration drift.
With it, renewal becomes predictable infrastructure behavior.

---

### Post-Install Validation Is Mandatory

A certificate that exists in a directory is not necessarily active.

Validation must confirm:

- The service is presenting the new certificate
- The correct chain is served
- The expected key algorithm is in use
- No stale instance is still advertising the old certificate

At annual cadence, failure might be caught manually.
At 47-day cadence, failure accumulates quietly.

If validation is not automated, friction returns.

---

### Partial Automation Compounds Risk

If issuance is automated but deployment requires:

- A separate ticket
- A separate team
- A separate window

Then renewal is no longer deterministic.

It becomes asynchronous coordination.

Frequency increases.
Coordination increases.
Variance increases.

At scale, variance becomes outage probability.

---

### Structural Reality

Issuance answers:
> “Can we obtain a certificate?”

Deployment answers:
> “Is the service actually using it?”

The industry conversation often focuses on the first.
Operational stability depends on the second.

Automation that stops before verified deployment is incomplete.

And incomplete automation accumulates friction.

If you automate renewal, finish the job.

Verify deployment. → Verify activation. → Verify behavior.

Anything less is ceremony with better tooling.

---

Next: high-assurance environments and why HSM-backed deployments change the equation again.

---

## Automating PKI at Scale — Part 5  
### Part 5: Automation in High-Assurance Environments

Automation becomes more complex when private keys are not files.

In high-assurance environments, keys may be:

- Generated inside hardware security modules (HSMs)
- Restricted from export
- Bound to compliance controls
- Subject to audit and dual control

The automation model must adapt.
The constraint changes again.

---

### Key Strategy Is Not an Implementation Detail

In software-only environments, key rotation is often straightforward.

In HSM-backed systems, key lifecycle decisions are architectural:

- Reuse keys across renewals?
- Generate new keys per renewal?
- Rotate on schedule independent of certificate lifetime?

Shorter certificate lifetimes increase certificate churn.
They should not automatically increase key churn.

Those are separate risk domains.

Confusing them creates unnecessary operational load.

---

### The HSM Is a Boundary

When keys are generated and stored inside an HSM:

- CSR generation must integrate with the module
- Slot and label management must be deterministic
- Cluster synchronization must be predictable
- Audit logging must remain intact

Automation that assumes filesystem access fails here.

Protocol-level automation must respect hardware boundaries.

The HSM is not a performance detail.
It is a control plane.

---

### Dual Control and CI/CD Can Coexist

High-assurance does not prohibit automation.
It requires deliberate automation.

Instead of approving each certificate event, governance can approve:

- The automated CSR pattern
- The key generation policy
- The renewal window
- The audit visibility model

Control shifts from individual transactions to system design.

That is stronger governance — not weaker.

---

### Certificate Cadence and Key Cadence Are Related — But Not Identical

Shorter certificate lifetimes reduce exposure in environments where private key protection is variable or widely distributed.
That is part of the rationale behind the 47-day trajectory.

In HSM-backed systems, key material is generated and protected under stronger controls.
The risk profile differs.

That does not eliminate the need for key rotation.

It means key rotation should be driven by:

- Cryptographic risk tolerance
- Protection boundary strength
- Regulatory requirements
- Algorithm transition strategy

Certificate lifetime reduction addresses exposure frequency.
Key rotation addresses compromise impact.

Conflating the two leads either to excessive churn — or unjustified stasis.

Both are architectural errors.

---

Next: TLS inspection — the lifecycle dependency most teams forget until it fails.

---

## Automating PKI at Scale — Part 6  
### Part 6: TLS Inspection Is an Issuing Authority Inside Your Network

A TLS inspection proxy is not simply a traffic control.

It performs two distinct TLS roles:

1. Web client (outbound to the internet)
2. Web server (inbound to internal users)

When an internal browser connects to `https://www.a.com`, two handshakes occur.

First, the proxy connects outward as a client.
Second, it generates and serves a replacement certificate internally.

That second function makes it an issuing authority.

Whether it is modeled that way determines how it behaves over time.

---

### Role 1: The Proxy as Web Client

To establish outbound TLS, the proxy must trust the public WebPKI.

It must maintain:

- Public root stores
- Intermediate updates
- Validation behavior

This is a trust hygiene problem.

It is not governed by the 200 → 100 → 47-day public certificate reduction schedule.

---

### Role 2: The Proxy as Web Server

When the proxy presents a generated certificate for `www.a.com` to an internal browser, it signs that certificate using an internal authority.

This is enterprise PKI territory.

This is where authority design matters.

---

### The Real Question: What Assurance Boundary Does the Proxy Operate Within?

Inspection devices dynamically issue certificates at scale.

If the signing key is:

- Software-protected
- Broadly reachable
- Operationally weakly governed

Then the proxy is not a high-assurance issuing environment.

Certificate lifetime reduction in the public ecosystem exists partly because private key protection varies widely across deployments.

The inspection proxy often falls into that category.

That risk is architectural — not compliance-driven.

---

### Inspection Authority Models

Most enterprises operate one of three models.

---

#### Model A — Self-Signed Proxy (Flat Authority)

```
TLS Proxy (self-signed CA)
```

There is no hierarchy.
The proxy is its own root.

- Trust must be distributed independently
- Rotation requires fleet-wide redistribution
- Revocation is rarely meaningful in practice
- There is no containment layer

This model is simple to deploy.

It assumes uniform and consistent trust distribution across all workloads.

In heterogeneous environments, that assumption rarely holds.

It is structurally fragile.

---

#### Model B — Direct Enterprise Signing

```
Enterprise Root (offline)
        ↓
      TLS Proxy
```

Endpoints already trust the enterprise root.

This eliminates independent trust distribution.

But it tightly couples the proxy to the offline root.

- Rotation requires root-level ceremony
- Lifecycle flexibility is limited
- Automation is constrained by governance friction

It improves authority.
It concentrates control.

---

#### Model C — Layered Issuance

```
Enterprise Root (offline)
        ↓
  Proxy Issuer CA (controlled / online)
        ↓
      TLS Proxy
```

This introduces authority separation.

- The root remains stable and offline
- The issuer can rotate independently
- The proxy can rotate independently
- Trust anchors do not change during routine events

Boundaries are defined.
Boundaries enable automation.

---

### Structural Reality

Public certificate lifetime reduction does not directly impact TLS inspection hierarchies.

But inspection is an issuing authority embedded in your network.

If it is not designed with clear authority boundaries and appropriate assurance controls, it becomes a concentrated risk surface.

Flat authority concentrates risk.
Root coupling concentrates friction.
Layered authority improves control.

Design it deliberately.

---

## Automating PKI at Scale — Part 7  
### Part 7: Automation Is a Prerequisite for Cryptographic Agility

Certificate lifetime reduction forces renewal to happen more often.

That exposes:

- Ownership gaps
- Deployment weaknesses
- Authority design flaws
- Inspection hierarchy fragility

But renewal cadence is not the real end state.

Algorithm transition is.

Sooner or later, the question will not be:

> “Can we renew certificates every 47 days?”

It will be:

> “Can we change cryptography across the estate without breaking production?”

---

### Changing Algorithms Is an Infrastructure Event

Changing a key algorithm is not a checkbox in a CA console.

It affects:

- How certificates are requested
- Where keys are generated
- What hardware is involved
- What applications can support
- What inspection devices understand
- What trust stores accept

If renewal is fragile, algorithm change will be more fragile.

Renewal increases operational frequency.
Algorithm shifts increase structural complexity.

Those pressures compound.

---

### Renewal Automation Is the Rehearsal

If your environment can:

- Issue certificates automatically
- Deploy them safely
- Validate them after installation
- Rotate within defined authority boundaries

Then you already have the mechanics required for algorithm transition.

If renewal still requires coordination and ceremony, algorithm change will amplify that friction.

Renewal cadence is rehearsal.
Agility is the performance.

---

### Boundaries Determine Blast Radius

Flat authority models concentrate risk.
Root-coupled systems expand blast radius.
Layered authority contains it.

The same principles apply whether the change is:

- 398 → 200 days
- RSA → ECDSA
- Classical → hybrid
- Hybrid → post-quantum

Frequency revealed operational weaknesses.
Algorithm change will test architectural ones.

---

### Structural Reality

Certificate lifetime reduction is not the destination.
It is pressure.

Pressure reveals system design.

If lifecycle automation is incomplete, agility is illusion.
If authority boundaries are unclear, transition is destabilizing.

Automation is not about speed.
It is about control.

And control is what makes cryptographic change survivable.

