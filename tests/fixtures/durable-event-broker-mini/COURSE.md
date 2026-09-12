# Durable Event Broker (trimmed fixture)

## Goal

A trimmed copy of the real durable-event-broker course (tutorail-bundles), kept
just big enough to exercise `--lesson` resolution against an optional lesson.

## Teaching philosophy

Small, so a test can read all of it. Real prose and design_refs are trimmed
down to only what this fixture's two main-path lessons and one optional
lesson actually use.

## Chapter map

1. A running broker with an in-memory log
2. Logical offsets and replay
   - optional: a framed TCP transport

## Topics this course must cover

- append and fetch through an in-memory log
- logical offsets and replay
- a framed TCP transport, as an alternative to HTTP
