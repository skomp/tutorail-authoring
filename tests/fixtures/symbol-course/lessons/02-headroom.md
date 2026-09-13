---
id: 02-headroom
title: Headroom above the limit
design_refs: [contract]
validators: [manual]
---

## Purpose

Show what happens well above the limit.

## Prerequisites

Lesson 01.

## Learning objectives

- Reason about load far above the budget

## Theory

Drive `2N` requests through one key and watch every decision after the budget
runs out.

## Concepts to teach

- headroom

## Constraints

- Do not change the counter.

## Suggested progression

- Start from the lesson 01 counter.

## Completion conditions

- The run is reproducible.

## On completion, persist

Record the observed rejection count.

## Optional deeper paths

None.
