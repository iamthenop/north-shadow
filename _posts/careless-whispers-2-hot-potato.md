---
layout: post
title: "Hot Potato"
subtitle: "Part II: The Distribution System"
date: 2026-03-13
author: "Penuel Lascano"
categories: [security-architecture, identity, operations]
tags: [pam, secrets-management, service-accounts, identity]
series: "Careless Whispers"
series_number: 2
permalink: /careless-whispers/hot-potato/
---

# Part II: The Distribution System
### Hot Potato

Below the treehouse, the children have been roasting sweet potatoes under a pile of burning leaves.

Now they are passing them around.

Each one is too hot to hold for long.

That is closer to how secrets behave.

---

## The PAM Pattern

Privileged Access Management solved a simple problem.

Administrators needed credentials to operate systems.  
Those credentials were powerful and often shared.

So the credentials moved into a vault.

Access was governed by policy.  
Identity was verified.  
The vault released the secret only when needed.

The credential moved.  
The vault controlled the movement.

---

## Extending the Pattern

Applications eventually needed the same thing.

Databases required passwords.  
APIs required tokens.  
Services required credentials.

Instead of humans retrieving the secret, the application would do it.

The pattern barely changed.

Identity authenticates.  
Policy is evaluated.  
The vault releases the secret.

---

## Service Accounts

In many environments the identity is not a human.

It is a service account.

A Kubernetes workload.  
An OAuth client.  
An instance role.  
A signed workload token.

The system verifies that identity.

Then the secret is released.

---

## Hot Potato

The secret rarely stays in one place.

The vault holds it briefly.  
The application receives it long enough to use it.  
Rotation replaces it soon after.

The credential moves again.

From vault to application.  
From application to database.  
From service to service.

A game of hot potato.

No system wants to hold the secret longer than necessary.

---

Secrets move.

Keys are held.

---

Next: **The Slippers**