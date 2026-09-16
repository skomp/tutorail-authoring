# Course quality audit: `prose-course`

This report states figures in prose and carries no element table at all. A
checker that returns "clean" here has not read it. The right answer is that
the parser is blind, not that the report is sound.

## 1. The course and its total

```
  lesson 00-first    4
  lesson 01-second   3
  --------------------------------------
  sum of lessons     7
  − unserved objectives (0 × −3)    0
  --------------------------------------
  COURSE TOTAL       7
```

## 2. The per-lesson table

| Lesson | Score | Objectives served |
|---|---:|---|
| `lessons/00-first.md` — Begin | **4** | 2 of 2 |
| `lessons/01-second.md` — Continue | **3** | 2 of 2 |

### `lessons/00-first.md` — 4

`:10 +2` "Decide the shape of the record." · `:11 +1` "Apply that shape to a
second case." · `:12 +1` "Sketch the container." · `:13 0` "Run the tests."

### `lessons/01-second.md` — 3

`:20 +2` "Choose a representation." · `:21 +1` "Repeat it for a second key."
