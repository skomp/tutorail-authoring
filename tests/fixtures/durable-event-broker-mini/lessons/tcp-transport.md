---
id: tcp-transport
title: A framed TCP transport
optional: true
design_refs: [transport-boundary, backpressure-contract, record-model]
validators: [go-build, go-test-race]
---

## Purpose

Add a compact streaming transport that exposes what an HTTP adapter hides:
messages need framing, reads and writes may be partial, and connection
lifetime must participate in cancellation and shutdown.

## Prerequisites

- The append, fetch and replay operations from `01-offsets-and-replay` exist.

## Learning objectives

- Design a versioned, length-prefixed request and response protocol.
- Decode several messages from one connection without assuming read boundaries.
- Handle short reads, short writes, malformed lengths, and disconnects.

## Theory

TCP is an ordered byte stream, not a message channel. One write need not
correspond to one read, and a read may contain part of a frame or several.

## Concepts to teach

- Byte-stream framing
- Partial reads and exact-read helpers
- Connection deadlines and cancellation

## Constraints

- The protocol has a documented maximum frame size and version.
- All broker actions call the same internal operations the in-memory log uses.
- One malformed connection cannot crash the broker.

## Suggested progression

Define a minimal append and fetch envelope, implement exact framed I/O, and
test using a connection that deliberately fragments and combines writes.

## Completion conditions

- TCP append and fetch produce the same results as the in-memory operations.
- Tests cover frames split across reads and several frames in one read.
- Race-enabled tests succeed.

## On completion, persist

Record the wire version, frame envelope, size limit and connection bounds.

## Optional deeper paths

None.
