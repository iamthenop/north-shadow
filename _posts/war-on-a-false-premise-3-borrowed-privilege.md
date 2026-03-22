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

Years later, he reportedly presented the ear to Parliament.

The incident became justification for a war between Britain and Spain.

The ear was not the cause of the conflict.

It was the trigger that revealed how authority had already spread beyond control.

Software privilege behaves in much the same way.

---

## The Moment of Elevation

Developers occasionally run into tools that require elevated privileges.

An installer needs access to system directories. A runtime must create network interfaces. A dependency needs to compile native modules. None of this feels especially dramatic in the moment. It feels like work.

So a familiar command appears.

```text
sudo
Run as Administrator
````

Elevation happens once.

The task proceeds. The system appears to behave normally. The software installs, the build completes, and the workflow continues.

But something important has already changed.

---

## Privilege Inheritance

Operating systems attach privileges to processes, not intent.

That distinction matters.

When a privileged process launches another process, the privilege flows forward with it. The system does not stop to ask whether the second process should hold the same authority, or whether the third process in the chain deserves it, or whether the fourth was ever meant to run with elevated power at all.

The chain simply continues.

```text
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

They execute code, often automatically and often at scale.

Consider a common command:

```text
sudo npm install
```

Developers usually run this when dependency permissions become difficult to manage or when an installation path expects system-level access. The command looks simple enough. It feels like one action.

The execution chain is much larger than that.

```text
sudo npm install
→ npm downloads dependencies
→ dependency install scripts execute
→ build tools compile modules
→ post-install hooks run
```

Every step runs with root privileges.

Many of these scripts originate from external packages. Most are harmless. Some are brittle. A few are poorly written. All of them inherit the authority of the original command.

That is the uncomfortable part.

Package managers were designed to automate trust.

Privilege systems were not designed for that level of delegation.

---

## Containers Do Not Eliminate the Problem

Many developers assume containers solve this issue.

Containers do improve isolation in important ways. They help separate environments, reduce dependency conflicts, and create cleaner build paths. But they do not change how privilege propagates.

Docker itself often runs with elevated authority. Container builds execute instructions supplied by external images, Dockerfiles, package managers, and build scripts. The chain becomes longer and the boundaries become less obvious, but the underlying model remains the same.

```text
elevated user
→ container runtime
→ container build steps
→ dependency installers
```

Privilege still spreads through the execution chain.

The location of the work may change.

The model does not.

---

## The JIT Illusion

Some organizations attempt to solve the workstation privilege problem with just-in-time elevation.

The idea appears straightforward. Remove standing administrator rights, grant temporary elevation when required, and return the system to normal afterward.

From a policy perspective, that sounds like progress.

From a systems perspective, the behavior has not changed.

When a user is elevated, every process launched during that window inherits the same authority. The window may be short. The propagation is not. Once granted, privilege continues to move through the execution chain exactly as before.

The elevation is temporary.

The borrowed privilege is not.

---

## The Real Actors

Most privileged actions on developer workstations are not performed by the user directly.

They are performed by installers, package managers, dependency scripts, container runtimes, and build systems. These tools execute code automatically. They pull new components into the environment. They compile, configure, assemble, and modify the system on the user’s behalf.

The user initiates the chain.

The software performs the work.

Yet the system still assigns privilege to the user.

Everything that follows inherits it.

---

## Naming the Pattern

This behavior has a name.

In security architecture it is called ambient authority.

In practice, there is a plainer way to describe it.

Borrowed privilege.

Authority spreads through the system because it follows the user rather than the software performing the action. That is why the problem remains difficult to see at first. The user appears to be in control. The system behaves as if the authority belongs to every tool that can reach it.

And once modern development tooling enters the picture, that assumption no longer holds.

---

## The Wrong Boundary

Modern development environments depend on automation.

Dependencies install themselves. Build systems compile code automatically. Containers assemble entire environments from scripts. Local toolchains routinely execute instructions the user did not write and cannot fully inspect in advance.

Privilege models designed decades ago assumed a different world.

They assumed the user was the primary actor.

But modern systems operate through chains of automated software, and those chains inherit whatever authority the user possesses. That is why the workstation privilege war persists even after local administrator rights are removed and just-in-time elevation is introduced.

The boundary was never corrected.

---

## The Next Question

If privilege should not follow the user, where should it belong?

Modern systems already point toward the answer.

Software can be identified. Publishers can be verified. Artifacts can be trusted. The software performing the action does not have to remain anonymous just because a human launched it.

Privilege does not have to belong to the user.

It can belong to the software performing the action.

That is the question security must finally answer.

---

Next: The Maginot Line