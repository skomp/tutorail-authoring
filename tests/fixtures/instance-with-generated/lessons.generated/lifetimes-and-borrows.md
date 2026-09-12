---
id: lifetimes-and-borrows
title: Lifetimes and borrows, the short version
design_refs: [row-cell-model]
validators: [cargo-check, manual]
generated: true
generated_at: 2026-09-12
kind: side-lesson
reason: >
  The learner could not get the borrow checker to accept their RowRef, and
  nothing on the main path teaches lifetime elision.
after: lessons/03-first-refactor.md
---

## Purpose

Teach just enough about lifetimes to get past a borrow the compiler rejects.

## Prerequisites

- `03-first-refactor`

## Theory

Your `RowRef` in `src/row.rs` borrows from the table. The compiler reported
error[E0597] because the borrow outlived the table.

## Completion conditions

`cargo check` passes and you can explain which lifetime the compiler inferred.
