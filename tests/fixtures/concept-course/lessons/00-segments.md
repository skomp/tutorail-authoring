---
id: 00-segments
title: Name a segment by its first record
design_refs: [segments]
validators: [manual]
---

## Purpose

Split one long log into segments a reader can name.

## Prerequisites

None.

## Learning objectives

- Name and order segments by base offset

## Theory

A group commit is one flush that acknowledges many appends at once, so the cost
of the flush is shared. A WAL converts an in-memory mutation into an ordered
durable record stream. The page cache sits between the two, and the broker
reports its metrics once a second. A record is encoded as JavaScript Object
Notation (JSON) before it is framed.

## Concepts to teach

- Base offsets
- Page cache
- Group commit
- metrics

## Constraints

- Segment filenames sort or parse deterministically by base offset.
- A reader SHOULD be able to name every segment without opening it.
- Make one logical row write atomic in the WAL.

## Suggested progression

- Write the segment writer first.

## Completion conditions

- Invalid overlap and duplicate base offset cases are reported.

## On completion, persist

Record the segment naming rule in `STATE.md`.

## Optional deeper paths

None.
