---
id: 00-contract
title: Make the decision precise
design_refs: [contract]
validators: [manual]
---

## Purpose

Turn a vague budget into an observable contract.

## Prerequisites

None.

## Learning objectives

- Separate a behavioural contract from an implementation strategy

## Theory

The course names one of those values and uses the same name everywhere. `N` is the
request limit: the number of requests the limiter allows for one client key in one
window. Every later lesson relies on it.

Each attempt advances `K` before the next window opens, and the store reports the
result as a `bool`. A `New` limiter starts empty. The starter carries
`starter/package.json` for the learner to read.

## Concepts to teach

- behavioural contract
- the symbol `N` (the request limit)
- public API versus internal representation

## Constraints

- Configure a positive request limit.
- Keep the decision callable repeatedly for different client keys.

## Suggested progression

- Ask which language the learner wants and why.

## Completion conditions

- A test states which requests are allowed.

## On completion, persist

Record the chosen language.

## Optional deeper paths

None.
