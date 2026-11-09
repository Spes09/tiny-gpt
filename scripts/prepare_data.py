"""Apollo 11 PDFs -> raw text -> cleaned text -> train/val split.

Run from the folder that holds the PDFs:  python pdf-transcript.py
Needs: pip install pypdf
Writes: raw/*.txt, clean/*.txt, train.txt, val.txt, cleaning_log.txt
"""
import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

RAW, CLEAN = Path("raw"), Path("clean")
RAW.mkdir(exist_ok=True)
CLEAN.mkdir(exist_ok=True)
LOG = []


def log(msg):
    print(msg)
    LOG.append(msg)


# Fancy punctuation -> ASCII. Anything else outside printable ASCII is dropped and counted.
SWAPS = str.maketrans({
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u00a0": " ", "\u2026": "...", "\t": " ",
})


def norm(line):
    # digits -> #, so "PAGE 12" and "PAGE 13" count as the same header
    return re.sub(r"\d+", "#", line.strip())


def strip_page_junk(pages):
    # Lines near the top/bottom of a page that repeat on >=30% of pages are headers,
    # footers or page numbers. shortcut: only checks the first/last 2 lines per page,
    # widen if the log shows headers sitting deeper.
    seen = Counter()
    for p in pages:
        lines = [l for l in p.splitlines() if l.strip()]
        seen.update({norm(l) for l in lines[:2] + lines[-2:]})
    junk = {k for k, n in seen.items() if n >= 0.3 * len(pages)}
    kept = ["\n".join(l for l in p.splitlines() if norm(l) not in junk) for p in pages]
    return "\n".join(kept), junk


def clean(text):
    text = text.translate(SWAPS)
    dropped = Counter(c for c in text if c != "\n" and not " " <= c <= "~")
    text = "".join(c for c in text if c == "\n" or " " <= c <= "~")
    text = re.sub(r" {2,}", " ", text)      # collapse runs of spaces (layout padding)
    text = re.sub(r" +\n", "\n", text)      # trailing spaces
    text = re.sub(r"\n{3,}", "\n\n", text)  # at most one blank line in a row
    return text.strip() + "\n", dropped


for pdf in sorted(Path(".").glob("*.pdf")):
    stem = re.sub(r"\W+", "_", pdf.stem).strip("_")  # "as11-tec (1)" -> "as11_tec_1"
    pages = [p.extract_text() or "" for p in PdfReader(pdf).pages]
    raw = "\n".join(pages)
    (RAW / f"{stem}.txt").write_text(raw, encoding="utf-8")

    text, junk = strip_page_junk(pages)
    text, dropped = clean(text)
    (CLEAN / f"{stem}.txt").write_text(text, encoding="utf-8")

    log(f"\n== {pdf.name} ({len(pages)} pages)")
    log(f"raw: {len(raw)} chars, {len(set(raw))} unique | clean: {len(text)} chars, {len(set(text))} unique")
    log(f"page junk removed (digits shown as #): {sorted(junk)}")
    log(f"non-ASCII chars dropped: {dict(dropped.most_common(15))}")
    mid = len(text) // 2
    print(f"--- sample from middle of {stem} ---\n{text[mid:mid + 600]}")

# Split each file 90/10 contiguously, so val has some of every source
# (a split on the concatenated corpus would make val only the last file).
train, val = [], []
for f in sorted(CLEAN.glob("*.txt")):
    t = f.read_text(encoding="utf-8")
    cut = int(len(t) * 0.9)
    train.append(t[:cut])
    val.append(t[cut:])
Path("train.txt").write_text("".join(train), encoding="utf-8")
Path("val.txt").write_text("".join(val), encoding="utf-8")

chars = sorted(set("".join(train + val)))
assert all(c == "\n" or " " <= c <= "~" for c in chars), "non-ASCII slipped through"
log(f"\ntrain: {sum(map(len, train))} chars | val: {sum(map(len, val))} chars")
log(f"vocab size {len(chars)}: {''.join(chars)!r}")

Path("cleaning_log.txt").write_text("\n".join(LOG), encoding="utf-8")