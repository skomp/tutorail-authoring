---
id: 01-offsets-and-replay
title: Logical offsets and replay
design_refs: [record-model, offset-semantics]
validators: [go-build, go-test]
---

## Purpose

Turn insertion order into an explicit, addressable log. A consumer must be
able to resume from a logical position and replay old records.

## Prerequisites

- Complete `00-running-broker`.

## Learning objectives

- Assign each appended record a logical offset.
- Support fetching a range of records starting at a given offset.

## Theory

See the offset semantics design note.

## Concepts to teach

- Logical offsets, distinct from any storage-level position
- Replay as bounded, ordered re-fetching

## Constraints

- Offsets are assigned in append order and never reused.
- Replay never skips or duplicates a record already fetched.

## Suggested progression

Add an offset field to the record type, assign it on append, and add a
range-fetch operation. Test replay from an arbitrary offset.

## Completion conditions

Replay from offset N returns every record appended at or after N, in order.

## On completion, persist

Record the offset assignment rule and the range-fetch signature.

## Optional deeper paths

A framed TCP transport is offered alongside this lesson; see
`tcp-transport`.
