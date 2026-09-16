# Course quality audit: `unreadable-course`

One score cell in this report carries prose where a figure belongs. The row
is not one the report excludes on purpose: it simply cannot be read. Every
figure the checker CAN re-add agrees, so the only thing it has to say is that
it is blind to one row — which is exactly the result that must not be
reported as clean.

## 1. The course and its total

```
  lesson 00-first    6
  --------------------------------------
  sum of lessons     6
  − unserved objectives (0 × −3)    0
  --------------------------------------
  COURSE TOTAL       6
```

## 2. The per-lesson table

| Lesson | Score | Objectives served |
|---|---:|---|
| `lessons/00-first.md` — Begin | **6** | 2 of 2 |

### `lessons/00-first.md` — 6

| file:line | Sentence | Score |
|---|---|---:|
| `:10` | "Decide the shape of the record." | +2 |
| `:11` | "Apply that shape to a second case." | +1 |
| `:12` | "Run the tests." | 0 |
| `:13` | "Explain why the shape holds." | +2 |
| `:14` | "Copy the starter file into place." | scored elsewhere |
| `:15` | "Sketch the container before writing a byte." | +1 |

Sum: 2+1+0+2+1 = **6**.
