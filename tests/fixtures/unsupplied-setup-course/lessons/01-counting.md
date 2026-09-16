---
id: 01-counting
title: Count within one window
design_refs: [counting]
validators: [manual]
---

## Purpose

Count requests for one client key inside one window.

## Prerequisites

- `00-language-and-contract`

## Learning objectives

- Count requests for one client key
- Reset the count at a window boundary

## Theory

A counter for each client key is enough while one window is in play.

## Concepts to teach

Counters, window boundaries.

## Constraints

- Keep the counter in memory.

## Suggested progression

Add the counter, reset it at the boundary, and test both sides of the edge.

## Completion conditions

The first requests inside a window are allowed and the next one is rejected.

## On completion, persist

Record the counting decision in the instance state.

## Optional deeper paths

None.
