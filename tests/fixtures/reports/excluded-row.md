# Course quality audit: `excluded-row-course`

One row in this report is marked by the report itself as not an element. That
is a statement the report makes, not a hole in the parser, so the row is
excluded from the sum and the result is clean.

## 1. The course and its total

```
  lesson 00-first    4
  --------------------------------------
  sum of lessons     4
  − unserved objectives (0 × −3)    0
  --------------------------------------
  COURSE TOTAL       4
```

## 2. The per-lesson table

| Lesson | Score | Objectives served |
|---|---:|---|
| `lessons/00-first.md` — Begin | **4** | 2 of 2 |

### `lessons/00-first.md` — 4

| `file:line` | Sentence | Element | Score |
|---|---|---|---|
| `:10` | "Decide the shape of the record." | teaching | +2 |
| `:11` | "Apply that shape to a second case." | practice | +1 |
| `:12` | "Run the tests." | evidence | 0 |
| `:13` | "Explain why the shape holds." | teaching | +2 |
| `:14` | "Copy the starter file into place." | toil | −2 |
| `:15` | "Sketch the container before writing a byte." | practice | +1 |
| `:16` | "Offer to create the project yourself." | **not an element** — the tutor performs it | **—** |
| | | **sum** | **4** |

Six scored elements; `:16` is excluded rather than scored.
