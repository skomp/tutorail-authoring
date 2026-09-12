# Design

## Record model {#record-model}

A record is an opaque byte payload plus a logical offset assigned on append.

## Offset semantics {#offset-semantics}

Offsets are monotonically increasing and stable: replaying from an offset never
skips or duplicates a record a consumer has not already seen.

## Transport boundary {#transport-boundary}

The broker's internal operations (append, fetch, replay) are transport-agnostic.
HTTP and TCP are two adapters over the same internal API.

## Backpressure contract {#backpressure-contract}

A transport bounds its own concurrent connections and in-flight requests, so one
slow or malformed connection cannot exhaust broker resources.
