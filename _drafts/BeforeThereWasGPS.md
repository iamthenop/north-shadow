---
layout: post
title: "Before There Was GPS"
subtitle: ""
date: 2026-03-06
author: "Penuel Lascano"
categories: [pki, automation, architecture]
tags: [tls, certificate-lifecycle]
series: 
series_number: 
permalink: /before-there-was-gps/909090
---

# Before There Was GPS
Before GPS, driving somewhere unfamiliar required a map.

Sometimes it was a folded road atlas.
Sometimes directions written by someone who had been there before.

> “Take the highway until the water tower.
> Turn left at the gas station.
> If you cross the river, you’ve gone too far.”

At first you follow the instructions carefully.
But after a few trips something else happens.
You begin to understand the terrain.

The roads start to make sense.
Landmarks connect.
If you miss a turn, you can still recover.

You are no longer just following directions.

You have a map.

Security once worked this way too.

## The Map of Software

Today much of security happens through tools.

Scanners report vulnerabilities.
Agents watch systems.
Dashboards promise visibility.

These tools are useful but they can hide the terrain.
Many people working in security today use the tools.
Far fewer have seen the terrain those tools were built to navigate.

To understand why certain vulnerabilities exist — and why certain defenses matter — it helps to see the landscape directly.

One of the first clear maps was written in 1996 by Aleph One.
The paper was called *Smashing the Stack for Fun and Profit*.

Despite the playful title, it became one of the founding documents of modern security.

The paper is still widely available and surprisingly readable today:
[http://phrack.org/issues/49/14.html]

Aleph One drew one of the first maps.

## The Trick

Programs move through instructions the way a traveler follows a route.

Each time a function finishes, the processor follows a small marker that tells it where to continue.

Most of the time those markers point exactly where they should.
But software sometimes places important things very close together.
When a program trusts input too freely, data can wander beyond the space intended for it.
Occasionally it reaches something important — like the marker that tells the processor where to go next.

Imagine Wile E. Coyote painting a tunnel on the side of a canyon wall.

The Road Runner runs straight through it.

Nothing about the motion changes.
The Road Runner simply follows the path in front of him.

Programs behave in much the same way.

If the marker changes, the processor still follows it.
Not the path the developer intended. Possibly one chosen by someone else.

Today we call this remote code execution.

The name sounds complex. The mechanism is not.
The program simply followed the tunnel.

## Why the Map Matters

Modern systems contain many defenses:
- memory protections
- address randomization
- control-flow safeguards

These defenses can look abstract when encountered through policy or tooling.

But they are not arbitrary.

They are guardrails placed along hazards the field discovered long ago.
Without the map, security feels like a long list of rules.
With the map, the terrain becomes visible.
And the rules begin to make sense.

## Walking the Terrain

Maps are most useful when you walk the ground yourself.
The moment this idea truly clicks is not when you read about it.
It is when you see a program behave in a way its author never intended.

For decades the security community has maintained small environments designed for exactly this purpose.

They are called *wargames*.

These systems contain intentionally vulnerable programs meant to be explored, not abused.
If you've never seen the trick yourself, a wargame is the safest place to learn it.

```bash
ssh level1@io.netgarage.org
password: level1
```
You connect.
You examine a program.
You try to understand why it behaves the way it does.

When you succeed, the next level opens.

No alarms.
No incident reports.
Just curiosity.

The first time a program jumps somewhere it wasn’t supposed to go, something important happens.

The map becomes clear.

And once you’ve seen the terrain, many things in security stop looking mysterious.
They start to look like engineering.
Lessons the field learned long ago.

Some of those lessons were first written down nearly three decades ago.

Like any good map, they remain worth studying.
