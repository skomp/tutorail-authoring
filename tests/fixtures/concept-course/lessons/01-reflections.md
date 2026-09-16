---
id: 01-reflections
title: Reflect the scene off itself
design_refs: [ssr]
validators: [manual]
---

## Purpose

Add screen-space reflections to the finished scene.

## Prerequisites

Lesson 00.

## Learning objectives

- March a ray through the depth buffer

## Theory

The reflection pass marches a ray and compares each step against the stored
surface.

## Concepts to teach

Depth linearisation, thickness bias and edge fade.

## Constraints

Expose step count, thickness and maximum distance as controlled parameters.

## Suggested progression

- Begin with a reconstruction diagnostic.

## Completion conditions

- The pass can be switched off.

## On completion, persist

Record the chosen encoding.

## Optional deeper paths

None.
