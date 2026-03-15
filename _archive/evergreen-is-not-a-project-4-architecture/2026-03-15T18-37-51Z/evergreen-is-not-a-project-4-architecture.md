---
layout: post
title: "Evergreen Is Not a Project"
subtitle: "Part IV: Architecture"
date: 2026-03-11
author: "Penuel Lascano"
categories: [architecture, systems, infrastructure]
tags: [evergreen, architecture, distributed-systems, lifecycle, resilience]
series: "Evergreen Is Not a Project"
series_number: 4
permalink: /evergreen-is-not-a-project/architecture/
---

# Part IV: Architecture
### Evergreen Is Not a Project

## Systems That Cannot Stop

Some systems cannot pause for a project.

Payment networks.  
Device fleets.  
Infrastructure platforms.

They operate continuously.

Change must occur while the system is running.

Stopping the system is not maintenance.

It is failure.

---

## Boundaries

Architecture begins with boundaries.

Systems must interact.

But those interactions must be contained.

Clear boundaries allow one part of the system to change.

While the rest continues operating.

When boundaries blur, change spreads.

A small adjustment becomes a system event.

---

## Protocols

Distributed systems depend on stable protocols.

Protocols allow participants to evolve independently.

Old versions remain in service.  
New versions appear gradually.

Devices in the field.  
Services in the cloud.  
Partners across networks.

All must coexist.

Protocols that cannot evolve will eventually require migration.

---

## Gradual Replacement

Healthy systems allow parts to be replaced without stopping the whole.

Nodes rotate.  
Services redeploy.  
Devices upgrade when they can.

Versions overlap.

The system evolves piece by piece.

When components cannot be replaced independently, change gathers into projects.

---

## Responsibility

Developers feel the pressure to deliver.

Features.  
Deadlines.  
Velocity.

That pressure is real.

But the systems we build must survive long after the sprint ends.

Devices remain in the field for years.  
Protocols persist across generations of services.  
Financial systems carry decades of history.

End users depend on this continuity.

Architecture exists to protect the system from the urgency of the present.

---

## The Principle

Distributed systems survive by allowing old and new to coexist.

Boundaries contain change.  
Protocols enable evolution.  
Replacement happens gradually.

When these properties hold, systems evolve through maintenance.

When they do not, organizations launch projects.

Evergreen systems are not built.

They are maintained.