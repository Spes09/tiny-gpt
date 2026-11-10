# Experiment log

One entry per change or run: date, what changed, seed, result, what I think it means.

## 2026-11-10: Data preparation (week 1)

**Sources:** three Apollo 11 transcripts from NASA, all with a text layer (0 empty pages, no OCR needed).

| File | Pages | Raw chars | Clean chars |
|------|-------|-----------|-------------|
| as11-cm | 248 | 285,966 | 285,471 |
| as11-pao | 633 | 1,101,556 | 1,093,642 |
| as11-tec | 626 | 842,287 | 829,675 |

**What I removed:**
- Page headers, footers and page numbers: lines near the top or bottom of a page that repeat on at least 30% of pages. Caught `END OF TAPE` (pao) and `Page #` and `(GOSS NET #) Tape #/#` (tec). Nothing caught in cm.
- Non-ASCII characters, mostly OCR artifacts: `°`, `·`, `¢`, `£`, `¥` and a few others (under 0.1% of the text).
- Extra spaces and runs of blank lines.

**What I kept:** speaker tags and timestamps. They are part of what the model should learn.

**Split:** each file 90/10, contiguous, so validation covers all three sources. Train 1,987,907 chars, val 220,881 chars. Vocabulary: 94 characters.

**Known gaps (to check):**
- [ ] Leftover headers in cm and pao (check the most repeated lines).
- [ ] Rare junk symbols still in the vocab (`{ | } ~ ^ _ \`): count them and look at their context.
- [ ] Whether the dropped `°` was real degree signs.
- [ ] Whether to keep front matter, indexes and appendices in the training text.

**Decision log:** add a line here each time one of these gets resolved.
