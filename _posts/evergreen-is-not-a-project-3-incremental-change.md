---
layout: post
title: "Evergreen Is Not a Project"
subtitle: "Part III: Incremental Change"
date: 2026-03-11
author: "Penuel Lascano"
categories: [architecture, systems, infrastructure]
tags: [evergreen, agile, dependencies, distributed-systems, lifecycle]
series: "Evergreen Is Not a Project"
series_number: 3
permalink: /evergreen-is-not-a-project/incremental-change/
---

# Part III — Incremental Change
### Evergreen Is Not a Project

## Small Steps

Many organizations adopt Agile methods.

Short cycles.  
Frequent delivery.  
Continuous feedback.

The goal is not speed alone.

It is reducing the risk of large change.

Small steps reveal problems early.

Small steps limit the blast radius.

---

## When It Works

Incremental change works when systems can evolve independently.

A service changes without forcing others to change.

Interfaces remain stable.

Components can be replaced while the rest of the system continues operating.

Under these conditions, change stays small.

---

## When It Slows

Dependencies change the size of safe movement.

When connections tighten, small changes ripple outward.

More teams must move together.

Release schedules align.  
Integration phases appear.  
Planning cycles lengthen.

Agile continues.

But the system begins to move in larger steps.

---

## The Observation

Agile does not remove dependencies.

It operates within them.

---

## The Bridge

Agile assumes change can remain small.

Architecture determines whether it can.