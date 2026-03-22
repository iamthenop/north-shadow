---
layout: post
title: "Part II: The Packaging Trap"
subtitle: "The Cod Wars"
date: 2026-03-12
author: "Penuel Lascano"
categories: [security, architecture, endpoint security]
tags: [endpoint security, desktop engineering, developer tooling, software distribution, privilege management]
series: "War on a False Premise"
series_number: 2
permalink: /war-on-a-false-premise/the-packaging-trap
---

# Part II: The Packaging Trap

For nearly twenty years, the United Kingdom and Iceland fought a series of confrontations known as the Cod Wars.

The dispute centered on fishing rights.

As fishing technology advanced, Iceland repeatedly expanded its territorial fishing limits in an attempt to regain control of local waters.

Each expansion triggered diplomatic disputes, naval escorts, and new enforcement efforts.

But the real issue was not the fishermen.

It was the rules governing the sea.

They had been written for a different era.

Modern software packaging faces a similar problem.

---

## The Obvious Solution

Most organizations attempt to solve the workstation privilege problem the same way.

Remove local administrator rights.

Then provide software through centralized packaging.

Support teams maintain approved tools.  
Security reviews them.  
Developers request what they need.

In theory, everyone gets what they want.

In practice, the packaging queue never stops growing.

---

## The Velocity Problem

Developer ecosystems move quickly.

Languages evolve.  
Frameworks update.  
Package managers introduce new dependencies.

A tool that works today may require a different version tomorrow.

Enterprise packaging pipelines move differently.

Request.  
Review.  
Test.  
Package.  
Deploy.

Each step is reasonable.

Together, they take time.

Often days.  
Sometimes weeks.

By the time a tool is packaged, developers may already need the next version.

---

## External Ecosystems

Some developer tools exist outside the organization’s control.

Integration simulators.  
Protocol testing environments.  
Vendor-provided development frameworks.

These tools evolve according to external industry timelines.

Updates appear when specifications change or vendors release new behavior.

The release cadence is frequent.

But rarely predictable.

When a new version appears, developers often need it immediately.

Packaging these tools through centralized workstation management quickly becomes impractical.

By the time a version is approved and distributed, a newer one may already exist.

Support teams are not failing.

They are trying to keep pace with software whose lifecycle is governed elsewhere.

---

## The Combinatorial Explosion

Developer environments rarely consist of a single tool.

They are stacks.

A runtime.  
A package manager.  
A container system.  
Framework dependencies.  
Build plugins.  
IDE extensions.

Each layer introduces its own versioning.

The number of possible combinations grows quickly.

Packaging pipelines are not designed to manage thousands of environment permutations.

They are designed to distribute stable applications.

Developer ecosystems behave differently.

They evolve continuously.

---

## When Packaging Becomes Software Distribution

At this point, support teams are no longer simply deploying software.

They are operating a software distribution system.

They review packages.  
Resolve dependencies.  
Track compatibility.  
Maintain versions.

But ecosystems like npm, pip, cargo, and homebrew already solve these problems.

They operate at internet scale.

An internal packaging pipeline cannot realistically compete with that velocity.

---

## The Trap

Packaging appears to offer control.

But the control is temporary.

The backlog grows.  
Developers wait.  
Exceptions appear.

Soon the organization introduces new mechanisms.

Temporary administrator access.  
On-demand privilege elevation.  
Manual approvals.

The packaging model has not solved the privilege problem.

It has only delayed it.

---

## The Boundary Is Still Wrong

The workstation privilege debate continues because the underlying boundary remains unclear.

Packaging attempts to control which software can be installed.

But the real issue is not installation.

It is execution.

Once software runs, it inherits the privileges of the user.

And that changes the nature of the problem entirely.

---

Next: **Part III: Borrowed Privilege**