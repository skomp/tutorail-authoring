---
id: 00-shader-basics
title: Shader compilation basics
design_refs: [pipeline]
validators: [manual]
---

## Purpose

Establish how a vertex and fragment shader become one linked program.

## Prerequisites

None.

## Learning objectives

- Compile a vertex and fragment shader
- Link a shader program and check its status

## Theory

A shader is compiled from source text, and two compiled shaders are linked
into one program before it can be used to draw anything.

## Concepts to teach

Compilation, linking, program status.

## Constraints

Copy `starter/package.json`, `starter/tsconfig.json` and `starter/src/main.ts` into their corresponding repository-root paths, preserving `src/`.
Copy the reference values exactly as given, without rounding.

## Suggested progression

Compile both shaders, link the program, check its status, and draw once.

## Completion conditions

The program links without error and one draw call succeeds.

## On completion, persist

Record which files were copied from the starter and where they landed.

## Optional deeper paths

None.
