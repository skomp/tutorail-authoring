---
id: 01-counting
title: Count inside one window
design_refs: [contract]
validators: [manual]
---

## Purpose

Count requests inside one window.

## Prerequisites

Lesson 00.

## Learning objectives

- Count decisions inside one window

## Theory

Report `Q` at the end of every run, then compare the two totals by hand.

Rejecting request `N + 1` proves the limit holds.

## Concepts to teach

- fixed windows

## Constraints

- The first `N` requests for a key in one window are allowed and `N + 1` is rejected.

## Suggested progression

- Write the counter first.

## Completion conditions

- The counter is covered by a test.

## On completion, persist

Record the counter shape.

## Optional deeper paths

None.
