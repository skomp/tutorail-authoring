# Course quality audit: `tiny-course`

A minimal report that is consistent with itself. Every figure in it is
reachable from the tables below it, so the checker must report nothing and
must say that it found the tables rather than that it found no defect.

## 1. The course and its total

**Arithmetic**

```
  lesson 00-first    4
  lesson 01-second   3
  --------------------------------------
  sum of lessons     7
  − unserved objectives (1 × −3)   −3   (01-second objective 2)
  --------------------------------------
  COURSE TOTAL       4
```

## 2. The per-lesson table

| Lesson | Score | Objectives served |
|---|---:|---|
| `lessons/00-first.md` — Begin | **4** | 2 of 2 |
| `lessons/01-second.md` — Continue | **3** | 1 of 2 |

### `lessons/00-first.md` — 4

| file:line | Sentence | Score |
|---|---|---:|
| `:10` | "Decide the shape of the record." | +2 |
| `:11` | "Apply that shape to a second case." | +1 |
| `:12` | "Run the tests." | 0 |
| `:13` | "Explain why the shape holds." | +2 |
| `:14` | "Copy the starter file into place." | −2 |
| `:15` | "Sketch the container before writing a byte." | +1 |

Sum: 2+1+0+2−2+1 = **4**.

### `lessons/01-second.md` — 3

| file:line | Sentence | Score |
|---|---|---:|
| `:20` | "Choose a representation." | +2 |
| `:21` | "Repeat it for a second key." | +1 |
| `:22` | "Run the suite." | 0 |

Sum: 2+1+0 = **3**.

## 6. Reader questions

The ratio of decisions to evidence steps is high: 3 of 9 scored elements are `teaching`.
