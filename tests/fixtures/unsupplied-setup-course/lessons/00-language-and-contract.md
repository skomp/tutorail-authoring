---
id: 00-language-and-contract
title: Choose a language and state the contract
design_refs: [contract]
validators: [manual]
---

## Purpose

Choose the implementation language and turn a vague requirement into an
observable contract.

## Prerequisites

The learner can run a small program in at least one language.

## Learning objectives

- Separate a behavioural contract from an implementation strategy
- Establish a fast run-and-test feedback loop

## Theory

A limiter is easy to describe vaguely. Start from observable behaviour. Do not
create the counting algorithm yet; this lesson stays with the contract. Do not
create a second project for the tests either; one is enough.

## Concepts to teach

- behavioural contract
- public API versus internal representation

## Constraints

- Let the learner choose any general-purpose implementation language.
- Use a local in-memory component, not a service.

## Suggested progression

- Ask which language the learner wants and why; adapt later guidance to it.
- Have the learner create the smallest conventional runnable project for that
  language with `cargo new`, `go mod init` or `npm init`, whichever the chosen
  language uses, before any contract work begins.
- Offer to explain the project structure if the learner asks about it.
- Define the public contract in prose and then as an API signature or stub.

## Completion conditions

- The project runs using the normal toolchain for the selected language.
- The public API accepts a client key and returns an allow or reject decision.

## On completion, persist

Record the selected language and the public API contract in the instance state.

## Optional deeper paths

None.
