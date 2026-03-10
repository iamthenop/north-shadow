---
layout: post
title: "Automating PKI at Scale: An Architectural Perspective"
subtitle: "Part VI: TLS Inspection Is an Issuing Authority Inside Your Network"
date: 2026-03-25
author: "Penuel Lascano"
categories: [pki, automation, architecture]
tags: [tls, certificate-lifecycle]
series: "Automating PKI at Scale"
series_number: 6
permalink: /automating-pki-at-scale/part-6-tls-inspection/
---

# Part VI: TLS Inspection Is an Issuing Authority Inside Your Network
### Automating PKI at Scale: An Architectural Perspective

A TLS inspection proxy is not simply a traffic control.

It performs two distinct TLS roles:

1. Web client (outbound to the internet)
2. Web server (inbound to internal users)

When an internal browser connects to `https://www.a.com`, two handshakes occur.

First, the proxy connects outward as a client.  
Second, it generates and serves a replacement certificate internally.

That second function makes it an issuing authority.

Whether it is modeled that way determines how it behaves over time.

A useful way to understand this is to think of the proxy as an interpreter.

It speaks one language when communicating with the website.  
It speaks another language when communicating with the browser.

The website presents a certificate the proxy understands.  
The proxy then issues a certificate the browser understands.

Trust depends on who certifies the interpreter.

Changing the trust root is like teaching the browser another language.

#### Role 1: The Proxy as Web Client

To establish outbound TLS, the proxy must trust the public WebPKI.

It must maintain:

- Public root stores
- Intermediate updates
- Validation behavior

This is a trust hygiene problem.

It is not governed by the 200 → 100 → 47-day public certificate reduction schedule.

#### Role 2: The Proxy as Web Server

When the proxy presents a generated certificate for `www.a.com` to an internal browser, it signs that certificate using an internal authority.

This is enterprise PKI territory.

This is where authority design matters.

## The Real Question: What Assurance Boundary Does the Proxy Operate Within?

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
## Inspection Authority Models

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
## Structural Reality

Public certificate lifetime reduction does not directly impact TLS inspection hierarchies.

But inspection is an issuing authority embedded in your network.

If it is not designed with clear authority boundaries and appropriate assurance controls, it becomes a concentrated risk surface.

Flat authority concentrates risk.  
Root coupling concentrates friction.  
Layered authority improves control.

Design it deliberately.