---
layout: post
title: "Part III: Borrowed Privilege"
subtitle: "Robert Jenkins' Ear"
date: 2026-03-12
author: "Penuel Lascano"
categories: [security, architecture, endpoint security]
tags: [security architecture, developer tooling, privilege management, ambient authority, software supply chain]
series: "War on a False Premise"
series_number: 3
permalink: /war-on-a-false-premise/borrowed-privilege
---

# Part III: Borrowed Privilege

In 1731, a British merchant captain named Robert Jenkins claimed that Spanish coast guards boarded his ship and cut off his ear.

Years later he reportedly presented the ear to Parliament.

The incident became justification for a war between Britain and Spain.

The ear was not the cause of the conflict.

It was the trigger that revealed how authority had already spread beyond control.

Software privilege behaves in much the same way.

---

## The Moment of Elevation

Developers occasionally encounter tools that require elevated privileges.

An installer needs access to system directories.  
A runtime must create network interfaces.  
A dependency needs to compile native modules.

So a familiar command appears:
```
sudo
Run as Administrator
```

Elevation happens once.

The task proceeds.

The system appears to behave normally.

But something important has already changed.

---

## Privilege Inheritance

Operating systems attach privileges to **processes**, not intent.

When a privileged process launches another process, the privilege flows forward.

The chain continues.
```
elevated shell
→ package manager
→ dependency installer
→ build script
→ downloaded code
```

Each step inherits the authority of the original process.

None of these components requested that authority directly.

They borrowed it.

---

## Ecosystems That Execute Code

Modern development ecosystems do more than download packages.

They execute code.

Consider a common command:
```
sudo npm install
```


Developers often run this when dependencies require system access or when local permissions become difficult to manage.

The command appears simple.

But the execution chain is much larger.

```
sudo npm install
→ npm downloads dependencies
→ dependency install scripts execute
→ build tools compile modules
→ post-install hooks run
```

Every step runs with root privileges.

Many of these scripts originate from external packages.

Most are harmless.

Some are poorly written.

All inherit the authority of the original command.

Package managers were designed to automate trust.

Privilege systems were not designed for that level of delegation.

---

## Containers Do Not Eliminate the Problem

Many developers assume containers solve this issue.

Containers improve isolation.

But they do not change how privilege propagates.

Docker itself often runs with elevated authority.

Container builds execute instructions supplied by external images and build scripts.

The chain becomes longer, but the model remains the same.

```
elevated user
→ container runtime
→ container build steps
→ dependency installers
```

Privilege still spreads through the execution chain.

---

## The JIT Illusion

Some organizations attempt to solve the workstation privilege problem with **Just-In-Time elevation**.

The model appears straightforward.

Remove standing administrator rights.  
Grant temporary elevation when required.  
Return the system to normal afterward.

But the underlying behavior has not changed.

When a user is elevated, every process launched during that window inherits the same authority.

The elevation may be temporary.

The privilege propagation is not.

Once granted, authority flows through the entire execution chain.

---

## The Real Actors

Most privileged actions on developer workstations are not performed by the user.

They are performed by:

- installers  
- package managers  
- dependency scripts  
- container runtimes  
- build systems  

These tools execute code automatically.

The user simply initiates the chain.

Yet the system assigns privilege to the user.

Every tool that follows inherits it.

---

## Naming the Pattern

This behavior has a name.

In security architecture it is called **ambient authority**.

In practice it is easier to describe as something else.

**Borrowed privilege.**

Authority spreads through the system because it follows the user.

Not the software performing the action.

---

## The Wrong Boundary

Modern development environments depend on automation.

Dependencies install themselves.  
Build systems compile code automatically.  
Containers assemble entire environments from scripts.

Privilege models designed decades ago assume a different world.

They assume the user is the primary actor.

But modern systems operate through chains of automated software.

And those chains inherit whatever authority the user possesses.

---

## The Next Question

If privilege should not follow the user, where should it belong?

Modern systems already provide the answer.

Software can be identified.

Publishers can be verified.

Artifacts can be trusted.

Privilege does not have to belong to the user.

It can belong to the software performing the action.

---

Next: **Part IV: The Maginot Line**