---
id: 00-running-broker
title: A running broker with an in-memory log
design_refs: [record-model]
validators: [go-build, go-test]
---

## Purpose

Establish the shortest vertical path through the project: a running process can
append an opaque record and fetch it again.

## Prerequisites

None.

## Learning objectives

- Define append and fetch as the broker's only two operations, for now.
- Keep the storage in memory, so mechanics can be learned before durability.

## Theory

See the record model design note.

## Concepts to teach

- Append-only ordering
- Opaque record payloads

## Constraints

- Append and fetch are the only operations this lesson adds.
- The in-memory store is deliberately not durable yet.

## Suggested progression

Define the record type, implement append and fetch against an in-memory slice,
and test that fetched bytes equal appended bytes in order.

## Completion conditions

Append followed by fetch returns the same bytes, in append order.

## On completion, persist

Record the in-memory record type's shape.

## Optional deeper paths

None.
