---
layout: post
title: "Part IV: The Maginot Line"
subtitle: "The Brilliant Defense That Didn't Work"
date: 2026-03-12
author: "Penuel Lascano"
categories: [security, architecture, endpoint security]
tags: [security architecture, machine identity, privilege management, endpoint security, software supply chain]
series: "War on a False Premise"
series_number: 4
permalink: /war-on-a-false-premise/the-maginot-line
---

# Part IV: The Maginot Line

After the First World War, France built one of the most sophisticated defensive systems in history.

The Maginot Line.

Massive fortifications protected the eastern border. Underground rail systems moved troops quickly. Artillery positions covered every expected approach. The engineering was extraordinary, and the strategy was logical enough that it carried the weight of national confidence.

The problem was not the defense.

The problem was the boundary.

In 1940, German forces simply went around the line.

The fortifications worked exactly as designed.

They were defending the wrong border.

Workstation security followed a similar path.

---

## The Security Response

Security teams recognized the workstation problem early.

Malware running with administrator privileges could modify system files, disable security controls, install persistence mechanisms, and move laterally through the network. None of that was hypothetical. The risk was real, and the response was rational.

Remove standing administrator rights.

Over time, that response matured into a familiar collection of controls. Local administrator removal, endpoint privilege management, just-in-time elevation, and approval workflows all emerged from the same instinct. Reduce the blast radius. Constrain elevation. Put friction in front of abuse.

These controls reduced obvious abuse.

The defense worked.

But it focused on the wrong boundary.

---

## The Boundary Security Chose

Security architecture treated privilege as a property of the user.

The model assumed a simple structure.

```text
user identity
→ receives privilege
→ launches software
→ software inherits privilege
````

That model made sense when users were the primary actors performing system operations. It assumed the human at the keyboard was also the principal source of privileged activity.

Modern systems behave differently.

As Part III showed, most privileged operations on developer workstations are performed by automated tools. Package managers, build systems, dependency installers, and container runtimes do most of the actual work. The user initiates the process, but the software carries it forward.

The user rarely performs the privileged action directly.

The user starts the chain.

---

## Borrowed Privilege

Once privilege follows the user, every process launched by that user inherits it.

```text
user
→ toolchain
→ dependencies
→ build scripts
→ downloaded code
```

Authority spreads through the execution chain, often quietly and without any explicit decision at each step. The software does not ask for separate approval. The system simply continues to propagate the authority it has already granted.

None of those components requested the privilege directly.

They borrowed it.

Security controls focused on restricting user elevation. That was understandable. It was also incomplete. The system continued to propagate privilege through software, which meant the control point remained attached to the wrong actor.

The boundary was misplaced.

---

## The Real Actors

Modern development environments are operated primarily by machines.

Installers configure environments. Build tools compile modules. Containers assemble runtime environments. Package managers execute dependency scripts. These systems act automatically, often across long chains of actions that the user neither sees in full nor controls in detail.

Yet the privilege model still assumes the human user is the actor.

The result is predictable.

Software inherits whatever authority the user possesses.

That is the contradiction security architecture must confront. The system is built around human identity, but the work is increasingly being performed by software acting on behalf of that human.

---

## The Wrong Control Plane

Security spent decades refining controls around human identity.

Authentication systems improved. Access management matured. Identity became the central security control because, for many systems, it was the correct one. If the problem was who could log in, identity was the answer. If the problem was who could access data, identity was the answer there too.

But the software ecosystem evolved.

Modern systems are not operated directly by humans alone. They are operated by software acting on behalf of humans, often at a speed and scale that identity systems designed for user access were never meant to govern.

The control plane never moved.

Privilege remained attached to the user.

---

## Machine Identity

Modern systems already contain the building blocks for a different model.

Software can be identified. Publishers can be verified. Artifacts can be trusted. Those signals already exist across the stack, even if they are often discussed under separate headings like code signing, supply chain security, endpoint policy, or application control.

These signals allow systems to recognize the software performing an action.

That recognition creates a new kind of actor.

The machine.

Not the workstation itself.

The software executing within it.

---

## Anchoring Identity

Machine identity alone is not enough.

Machines run many kinds of software. Some of it is trustworthy. Some of it is not. Some of it is internally developed, some vendor supplied, and some downloaded moments earlier as part of a dependency chain. Identity without trust simply moves the ambiguity around.

The identity must be anchored to something trustworthy.

Trusted software artifacts provide that anchor.

Code signing, verified publishers, artifact hashes, and repository trust all contribute to that decision. Each of them helps answer a more useful question than “which user clicked the button?”

They help answer:

What is this software, and why should the system trust it?

Together they allow a system to establish:

**machine identity anchored to trusted software artifacts**

This changes how privilege can be assigned.

---

## A Different Model

Instead of granting authority to the user:

```text
user elevates
→ everything inherits privilege
```

authority can be scoped to the software performing the action.

```text
trusted software artifact
→ establishes machine identity
→ receives scoped privilege
```

That shift changes the entire conversation.

Installers receive permission to modify system directories. Container runtimes receive permission to configure networking. Build tools receive permission to compile native modules. Each action is tied to the software performing it, and each grant can be evaluated in terms of trust, provenance, and scope.

The privilege belongs to the software performing the action.

Not to the user who launched it.

---

## Moving the Line

The Maginot Line failed because it defended the wrong border.

Workstation privilege controls often repeat the same mistake. They defend the boundary around the user because that is where the old model says authority begins. But modern systems operate through software, which means the real control point lies elsewhere.

The real boundary lies between trusted and untrusted software.

Once that boundary moves, the control plane changes with it.

The question is no longer which user should be allowed to elevate.

The question becomes which software should be trusted to perform privileged operations.

That is a much harder question.

It is also the right one.

---

## The Next Step

The technology required for this model already exists.

Machine identities. Artifact trust. Scoped execution privileges. Application control. Verified provenance. The pieces are already present in the ecosystem, even if the industry still talks about them as separate categories.

What remains is not a technical problem.

It is an organizational one.

Security must be willing to admit that the original control worked and still failed.

That is the beginning of a modern model.

---

Next: Ending the Workstation Privilege War