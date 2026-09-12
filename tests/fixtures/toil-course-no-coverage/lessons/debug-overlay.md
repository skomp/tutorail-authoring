---
id: debug-overlay
title: On-screen debug overlay
optional: true
design_refs: []
validators: [manual]
---

## Purpose

Give a curious learner a lightweight way to see performance numbers while
iterating, without touching the render path.

## Prerequisites

- `01-texture-work`

## Learning objectives

- Draw framerate and draw-call counts as an overlay

## Theory

An overlay text renderer draws small bitmap glyphs directly to the canvas,
outside the main scene's draw calls.

## Concepts to teach

Overlay rendering, bitmap glyphs, frame timing.

## Constraints

None beyond the main path's.

## Suggested progression

Measure frame time, draw the counters as an overlay, and confirm the main
scene is unaffected.

## Completion conditions

The learner can toggle the overlay without changing the rendered scene.

## On completion, persist

Record whether the overlay was taken.

## Optional deeper paths

None.
