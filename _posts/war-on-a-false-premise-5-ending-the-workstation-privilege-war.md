---
layout: post
title: "War on a False Premise"
subtitle: "Part V: Ending the Workstation Privilege War"
date: 2026-03-24
author: "Penuel Lascano"
categories: [security, architecture, systems-thinking]
tags: [machine-identity, endpoint-security, privilege-management, security-architecture]
series: "War on a False Premise"
series_number: 5
permalink: /war-on-a-false-premise/ending-the-workstation-privilege-war/
---

# Part V: Ending the Workstation Privilege War

For years, workstation security has been framed as a fight over administrator privileges.

Security teams remove them.  
Developers request them.  
Support teams manage the exceptions.

Policies are written.  
Tools are deployed.  
Dashboards track the number of remaining administrators.

Eventually the number approaches zero.

And yet the conflict never ends.

---

## For Security Leadership

The workstation privilege war is not a technical failure.

Security teams correctly identified the risk of administrator privileges.
They deployed controls to reduce it.

But the conflict persists because the security model never changed.

Modern systems are operated primarily by software.
Yet workstation security still assigns authority to users.

Until that model shifts, the war will continue.

---

## The Illusion of Control

Endpoint privilege management tools attempt to manage this conflict.

Just-in-time elevation grants temporary authority.  
Approval workflows authorize exceptions.  
Policies attempt to limit exposure.

These controls create activity.

They generate dashboards.  
They produce reports.  
They demonstrate progress.

But the underlying conflict remains.

Developers still need privileged operations.  
Support teams still struggle to keep environments current.  
Security teams continue to enforce the policy.

The organization manages the symptoms of a flawed model.

---

## The System That Actually Exists

Modern development environments are not operated primarily by humans.

They are operated by software.

Package managers install dependencies.  
Build systems compile modules.  
Containers assemble runtime environments.  
Automation scripts configure entire systems.

The user initiates the process.
The software performs the work.
Yet the privilege model still assumes the human is the actor.

Authority follows the user.
Every process launched by that user inherits it.

Security removed administrator privileges from humans.
Software inherited them instead.

---

## The Question Security Keeps Asking

For years, the industry has focused on a single question.

Who should be allowed to elevate?

It is the wrong question.

Modern systems are defined not by which users hold power.
They are defined by which software is trusted to perform privileged operations.

Once that shift is understood, the control plane changes.

Privilege no longer belongs to the user.
It belongs to machine identity anchored to trusted software artifacts.

---

## Machine Identity

Modern systems already provide the signals required to implement this model.

Software can be identified.  
Publishers can be verified.  
Artifacts can be trusted.

Code signing.  
Verified repositories.  
Artifact integrity checks.

These signals establish machine identity anchored to trusted software artifacts.

Authority can now be granted to the software performing the action.

Not to the human who launched it.

---

## A Different Model

The legacy model looks like this:
```
user identity
→ receives privilege
→ launches software
→ software inherits privilege
```

The modern model looks different:
```
trusted software artifact
→ establishes machine identity
→ receives scoped privilege
```

Installers receive permission to modify system directories.
Container runtimes receive permission to configure networking.
Build tools receive permission to compile native modules.

Each action is tied to the software performing it.

Not to the user.

---

## Leadership Responsibility

Ending the workstation privilege war is not a tooling decision.

It is a leadership decision about how authority is modeled within the organization.
For two decades the industry attempted to win this conflict by restricting users.

The conflict persisted.
Because the boundary never moved.

Security defended the line around human identity.
Modern systems operate somewhere else entirely.

The real boundary lies between trusted and untrusted software.

---

## The War That Never Ends

For years security programs measured maturity by a simple metric.

How many users still have administrator privileges?

But maturity is not a number on a dashboard.

If the control worked, the conflict would have ended.

It did not.

Security removed administrator privileges from users.

Software inherited them anyway.

Every installer.  
Every dependency script.  
Every container build.  
Every automated toolchain.

The authority never disappeared.

It simply moved.

---

## Structural Reality

In 1859 the United States and Britain nearly went to war over a pig.

The farmer was not the cause of the conflict.
The pig was not the cause either.
The problem was the border.

A treaty referenced a boundary that did not clearly exist.
Once the boundary was clarified, the conflict ended.

The workstation privilege war is not so different.

Security removed administrator privileges from users.
But the boundary was never redrawn.
Privilege still follows the user.

Until that changes, the war will continue.

Developers will work around it.  
Operations will manage the friction.  
Security will enforce the policy.

Each group doing its job.
Each group fighting the others.

The workstation privilege war ends when security, developers, and operations finally share the same cause.