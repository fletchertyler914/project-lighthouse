#!/usr/bin/env python3
"""
nam_transcribe.py - transcribe the Nouvelles Annales de Mathématiques "questions non résolues" pages
(lists of question numbers 1863/1868/1915 and the 1916-18 reprints with full statements) from page scans.

Same conventions as read_source.py (model, key file, budget guard, resumable, key never printed), but with a
question-structured prompt: besides the verbatim transcription each page JSON gets
  result.number_list   bare question numbers on list pages
  result.questions     one record per (possibly partial) question statement: number, year_posed, page_cited,
                       author, statement_fr (verbatim), statement_en, starts_on_previous_page, continues_on_next_page
Each page is sent as three overlapping horizontal strips of the ink-cropped scan so that exponents and
subscripts survive the API's image downscaling (the NUMDAM OCR layer loses them; we read the image).

    python3 -E -P src/nam_transcribe.py [--cotes ID,ID] [--pages 2,3] [--workers 3] [--budget 35]
        [--base data/nouvelles-annales] [--scratch /tmp/hunt_dl/nam]
    <base>/inventory.tsv: cote, pdf, date, pages, title.  Page images: <scratch>/<cote>/img/pNNN.jpg
    (made by src/pdf_images.py from the single-item NUMDAM PDFs; nothing is downloaded here).
Output: <base>/transcripts/<cote>/pNNN.json in the data/FORMAT.md "PDF-sourced page" shape.
"""
import argparse
import base64
import io
import json
import pathlib
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic
from PIL import Image, ImageOps

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from jsonfix import lenient_json  # noqa: E402

MODEL = "claude-opus-5-5"
PRICE_IN, PRICE_OUT = 4.00 / 1e6, 20.00 / 1e6
HUNT = pathlib.Path(__file__).resolve().parent.parent
BASE = HUNT / "data" / "nouvelles-annales"
DL = pathlib.Path("/tmp/hunt_dl/nam")
SITE = "https://www.numdam.org"
STRIPS = 3
OVERLAP = 140           # px of the full-resolution scan shared by neighbouring strips (about two text lines)
MAX_PIXELS = 1_150_000  # the API downsamples anything larger; stay just under so nothing is lost twice

PROMPT = """This is page {page} of {n} of item {cote} of the Nouvelles Annales de Mathématiques (Paris), printed
French, {title} ({date}): lists and reprints of problems posed 1842-1910 that were never solved.
The page is given as {k} overlapping horizontal strips, top to bottom (neighbouring strips share about two lines;
do not transcribe shared lines twice). Read the IMAGE: exponents, subscripts, primes, accents and the distinction
between the digits 1/7, 3/5, 0/6 matter. Mark anything you cannot read with [?]. Do not complete or normalise.

Reprinted questions look like:  "1074 (1872, 190). - statement ... F. DIDON."  i.e. question number, then in
parentheses the year and page of the original Nouvelles Annales volume, a dash, the statement, and the proposer.
Some entries carry no author, some have a "bis" number, some run over the page break.

Return ONLY a JSON object:
  "legibility": "good" | "fair" | "poor" | "blank"
  "kind": "list" | "statements" | "editorial" | "other" | "blank"
  "topic_en": one plain-English sentence on what the page contains
  "transcription": verbatim transcription of the whole page in French, line breaks as \\n, mathematics in LaTeX
      inside $...$, uncertain words followed by [?]
  "number_list": if the page lists bare question numbers, ALL of them in reading order as strings (keep "bis"),
      else []
  "questions": one record per question statement or statement fragment on this page, in page order:
      {{"number": "1074", "year_posed": 1872, "page_cited": "190", "author": "F. Didon" or "",
        "statement_fr": verbatim statement (without the leading number/citation and without the author name),
        "statement_en": faithful English translation (LaTeX kept),
        "starts_on_previous_page": false, "continues_on_next_page": false,
        "editorial_note": any remark printed about this question (footnote, 'résolue', cross-reference) or ""}}
  "notes_en": English summary of any editorial text on the page that is not part of a question statement
"""

lock = threading.Lock()
spent = {"in": 0, "out": 0, "n": 0}


def usd():
    return spent["in"] * PRICE_IN + spent["out"] * PRICE_OUT


def inventory():
    rows = {}
    for ln in (BASE / "inventory.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        cote, pdf, date, pages, title = ln.split("\t")
        rows[cote] = dict(cote=cote, pdf=pdf, date=date, pages=int(pages), title=title)
    return rows


def ink_bbox(img):
    """Bounding box of the printed area: rows/columns of the 1/8-scale image holding ink above a noise floor."""
    small = ImageOps.autocontrast(img.convert("L")).resize((max(1, img.width // 8), max(1, img.height // 8)))
    px = small.load()
    w, h = small.size
    rows = [sum(1 for x in range(w) if px[x, y] < 110) for y in range(h)]
    cols = [sum(1 for y in range(h) if px[x, y] < 110) for x in range(w)]
    ys = [y for y, c in enumerate(rows) if c >= 3 and c < 0.9 * w]   # ignore full black borders
    xs = [x for x, c in enumerate(cols) if c >= 3 and c < 0.9 * h]
    if not ys or not xs:
        return 0, 0, img.width, img.height
    pad = 6
    return (max(0, (min(xs) - pad) * 8), max(0, (min(ys) - pad) * 8),
            min(img.width, (max(xs) + pad) * 8), min(img.height, (max(ys) + pad) * 8))


def strips(path, k=STRIPS):
    img = Image.open(path).convert("L")
    img = img.crop(ink_bbox(img))
    H = img.height
    step = (H + (k - 1) * OVERLAP) / k
    out = []
    for i in range(k):
        y0 = int(max(0, i * step - i * OVERLAP))
        y1 = int(min(H, y0 + step))
        s = img.crop((0, y0, img.width, y1))
        scale = min(1.0, (MAX_PIXELS / (s.width * s.height)) ** 0.5)
        if scale < 1.0:
            s = s.resize((int(s.width * scale), int(s.height * scale)), Image.LANCZOS)
        b = io.BytesIO()
        s.save(b, "JPEG", quality=85)
        out.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                "data": base64.b64encode(b.getvalue()).decode()}})
    return out


def do_page(client, meta, k, budget):
    out = BASE / "transcripts" / meta["cote"] / f"p{k:03d}.json"
    if out.exists():
        return f"skip {meta['cote']} p{k:03d}"
    with lock:
        if usd() >= budget:
            return f"BUDGET STOP (${usd():.2f})"
    img = DL / meta["cote"] / "img" / f"p{k:03d}.jpg"
    content = strips(img) + [{"type": "text", "text": PROMPT.format(page=k, n=meta["pages"], cote=meta["cote"], title=meta["title"],
                                                                     date=meta["date"], k=STRIPS)}]
    try:
        r = client.messages.create(model=MODEL, max_tokens=20000, messages=[{"role": "user", "content": content}])
    except anthropic.APIError as e:
        return f"ERR {meta['cote']} p{k:03d}: {str(e)[:140]}"
    text = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
    data = lenient_json(text)
    with lock:
        spent["in"] += r.usage.input_tokens
        spent["out"] += r.usage.output_tokens
        spent["n"] += 1
    out.parent.mkdir(parents=True, exist_ok=True)
    rec = {"cote": meta["cote"], "page": k, "label": f"p{k:03d}",
           "image": f"{SITE}/{meta['pdf']}#page={k + 1}",  # PDF page 1 is the NUMDAM cover sheet
           "model": MODEL, "source": MODEL, "stop_reason": r.stop_reason, "parsed": data is not None,
           "result": data if data is not None else {"raw": text}, "human_corrected": False}
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    d = data or {}
    return (f"ok {meta['cote']} p{k:03d} {d.get('kind')} {d.get('legibility')} q={len(d.get('questions', []))} "
            f"nums={len(d.get('number_list', []))} (${usd():.2f})")


def main():
    global BASE, DL
    ap = argparse.ArgumentParser()
    ap.add_argument("--cotes", default="", help="comma list of item ids; default all in inventory")
    ap.add_argument("--pages", default="", help="comma list of page numbers (only with a single cote)")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--budget", type=float, default=35.0)
    ap.add_argument("--base", default=str(BASE))
    ap.add_argument("--scratch", default=str(DL))
    a = ap.parse_args()
    BASE, DL = pathlib.Path(a.base), pathlib.Path(a.scratch)
    inv = inventory()
    cotes = [c for c in a.cotes.split(",") if c] or list(inv)
    key = pathlib.Path.home().joinpath(".config/hunt/anthropic_key").read_text().strip()
    client = anthropic.Anthropic(api_key=key, max_retries=4, timeout=900)
    jobs = []
    for c in cotes:
        meta = inv[c]
        pages = [int(p) for p in a.pages.split(",") if p] if a.pages else range(1, meta["pages"] + 1)
        jobs += [(meta, k) for k in pages]
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for fu in as_completed([ex.submit(do_page, client, m, k, a.budget) for m, k in jobs]):
            print(fu.result(), flush=True)
    print(f"RUN DONE | {spent['n']} calls | in={spent['in']} out={spent['out']} | ${usd():.2f} | {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
