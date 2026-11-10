# tiny-gpt

A small GPT-style transformer, built from scratch and trained character by character on the Apollo 11 mission transcripts. The goal is to understand every piece, so the code is typed along with lectures, then rewritten from memory, and every experiment is logged.

Built while following Andrej Karpathy's [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) lecture series.

**Status:** week 1 of 4 (foundations and data). See the checklist at the bottom.

## Data

Three Apollo 11 transcripts from NASA, extracted from PDF:

| File | What it is |
|------|-----------|
| `as11-cm.pdf` | Command module onboard voice transcript |
| `as11-pao.pdf` | Public affairs (PAO) commentary |
| `as11-tec.pdf` | Technical air-to-ground transcript |

Source: <!-- add the NASA page links you downloaded these from -->

After cleaning there are about 2.2M characters and a 94-symbol vocabulary:

| Source | Clean chars |
|--------|------------|
| cm | 285,471 |
| pao | 1,093,642 |
| tec | 829,675 |

Each file is split 90/10 into contiguous train/val chunks, so validation covers all three sources: 1,987,907 train chars and 220,881 val chars.

### Cleaning decisions

Done by `scripts/prepare_data.py`, and every run writes `data/cleaning_log.txt`.

- Page headers, footers and page numbers: lines near the top or bottom of a page that repeat on at least 30% of pages are removed.
- Smart quotes and dashes become ASCII.
- Any other non-ASCII character (mostly OCR artifacts such as `°`, `·`, `¢`, `£`) is dropped and counted in the log.
- Runs of spaces are collapsed and blank lines are capped at one.
- Speaker tags and timestamps are kept, since they are part of what the model should learn.

Known gaps: leftover headers in `cm` and `pao` may remain, and a few rare OCR symbols are still in the vocabulary.

## Rebuild the dataset

```bash
pip install -r requirements.txt
# put the three PDFs in data/, then:
cd data
python ../scripts/prepare_data.py
```

This writes `data/raw/`, `data/clean/`, `data/train.txt`, `data/val.txt` and `data/cleaning_log.txt`. PDFs and `data/raw/` are not committed.

## Layout

```
scripts/prepare_data.py   PDF extraction, cleaning, train/val split
data/                     cleaned text, train/val files, cleaning log
micrograd/                micrograd lecture code
makemore/                 makemore lecture code, bigram baseline
logs/experiment_log.md    date, change, seed, result for every run
```

## Roadmap

| Week | Focus | Checkpoint |
|------|-------|-----------|
| 1 | Foundations and data: micrograd, makemore 1-3, clean the transcripts, bigram baseline | Cleaned dataset, data write-up, baseline loss |
| 2 | Baseline transformer from "Let's build GPT", rewritten from memory, fixed seeds, plus training setup (checkpointing, mixed precision, LR schedule, loss curves) | Beats the bigram, trusted baseline, loss plot, 3 samples |
| 3 | Ablations, one variable at a time (layers, context length) | Results table with interpretation |
| 4 | Write-up, polished repo, reproduce script | README or blog post, short pitch |

### Week 1 checklist

- [x] micrograd lecture
- [x] Download and extract the transcripts
- [x] Clean text, log decisions
- [ ] makemore parts 1-3
- [ ] Bigram baseline loss

## Results

_Nothing to report yet. Baseline loss, model sizes and ablation tables will go here._
