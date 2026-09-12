---
id: 00-bootstrap
title: Workspace bootstrap
design_refs: [bootstrap-sequencing]
validators: [manual]
---

## Purpose

Reproduce, verbatim, two real sentences fix round 2 found this scanner
getting wrong in opposite directions.

## Prerequisites

None.

## Learning objectives

- Acquire a working development workspace

## Theory

An asynchronous follower is an internal consumer with stricter identity rules. It can
create another copy, but the leader acknowledges without waiting for it. Therefore the
copy is neither a quorum nor a failover protocol. Without authority and election rules,
the follower must remain read-only.

## Concepts to teach

Workspace bootstrap, tutor setup versus learner task, and frame checksum verification.

## Constraints

Before presenting any learner task, the tutor MUST read `starter/README.md`; copy
`starter/package.json`, `starter/package-lock.json`, `starter/tsconfig.json`, `starter/index.html`
and `starter/src/main.ts` into their corresponding workspace-root paths; initialise Git if the
workspace is not already a repository; run `npm install`; and verify the untouched starter with
`npm run typecheck` and `npm run build`. This bootstrap is tutor work and is not offered as the
first task. Stop and report a setup failure rather than asking the learner to repair course
scaffolding.

## Suggested progression

Acquire the context once tutor bootstrap succeeds.

## Completion conditions

The workspace matches the untouched starter.

## On completion, persist

Record that bootstrap succeeded.

## Optional deeper paths

None.
