---
id: 01-texture-work
title: Texture sampling
design_refs: [sampling]
validators: [manual]
---

## Purpose

Sample a 2D texture in a fragment shader and control its filtering.

## Prerequisites

- `00-shader-basics`

## Learning objectives

- Sample a texture in a fragment shader
- Configure wrapping and filtering modes

## Theory

A sampler binds a texture unit to a uniform. Provide a direct-copy composition shader before adding effects.

## Concepts to teach

Texture units, samplers, wrapping, filtering.

## Constraints

Do not introduce a second rendering pipeline; extend the existing draw path.

## Suggested progression

Bind a texture, sample it in the fragment shader, and vary the filtering mode.

## Completion conditions

The sampled texture renders with the configured filter.

## On completion, persist

Record the chosen filtering and wrapping modes.

## Optional deeper paths

None.
