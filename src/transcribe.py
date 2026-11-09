#!/usr/bin/env python3
"""
transcribe.py — transcribe manuscript pages (IIIF) with Claude vision and extract
every stated problem / question / conjecture / plan, verbatim.

- Key is read from ~/.config/hunt/anthropic_key (600 perms). Never printed/logged.
- Images are sent by URL (Anthropic fetches them from the library's IIIF server).
- Resumable: pages with an existing JSON result are skipped (no double billing).
- Hard budget cap: stops when estimated spend reaches --budget USD.
- Model outputs are stored as data (JSON) and never executed.

    python3 -E -P src/transcribe.py <manifest.json> <out_dir> [--only 6,27] [--workers 4] [--budget 20]
"""
import argparse
import json
import pathlib
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic

MODEL = "claude-opus-5-5"
PRICE_IN, PRICE_OUT = 4.00 / 1e6, 20.00 / 1e6          # USD per token (Opus 5.5)
WIDTH = 1300

DEFAULT_SOURCE = ("David Hilbert's handwritten scientific diary (\"Wissenschaftliches Tagebuch\", "
                  "Goettingen, 1886-1912), German in Latin script, with mathematics")

PROMPT = """This is one page of {source}. The page may be rotated; read it in its natural
orientation. It may be a table of numbers or a page of bare calculations; transcribe what is there.

Return ONLY a JSON object with these keys:
  "legibility": "good" | "fair" | "poor" | "blank"
  "rotated": true | false
  "topic_en": one plain-English sentence on what the page is about
  "transcription": verbatim transcription in the ORIGINAL language. Keep line breaks as \\n.
      Mathematics in LaTeX inside $...$. Struck-through text as [-...-]. Insertions as {{+...+}}.
      Mark uncertain words with [?] right after them. Do not translate, normalise, or complete.
  "methods": a list of every distinct mathematical RESULT, FORMULA, ALGORITHM or METHOD on the
      page, each as {{"what": short description in modern terms, "quote": exact words or formula
      copied from your transcription}}. Use [] if none.
  "items": a list of every place where the author STATES a problem, open question, conjecture,
      plan ("I will/should investigate..."), or an unproved claim. For each:
      {{"kind": "problem"|"question"|"conjecture"|"plan"|"claim",
       "quote": exact words copied from your transcription,
       "english": faithful plain-English translation,
       "status_on_page": "solved on page" | "left open" | "unclear"}}
      Use [] if there are none. Do NOT add interpretation or significance judgements.
"""

lock = threading.Lock()
spent = {"in": 0, "out": 0, "pages": 0}


def canvases(manifest):
    m = json.loads(pathlib.Path(manifest).read_text(encoding="utf-8"))
    for i, c in enumerate(m["sequences"][0]["canvases"]):
        yield i, str(c.get("label", "-")).strip(), c["images"][0]["resource"]["service"]["@id"]


def usd():
    return spent["in"] * PRICE_IN + spent["out"] * PRICE_OUT


def call(client, url, source=DEFAULT_SOURCE):
    kwargs = dict(
        model=MODEL, max_tokens=16000,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "url", "url": url}},
            {"type": "text", "text": PROMPT.format(source=source)}]}],
    )
    try:   # server-side refusal fallback (recommended default for Opus 5.5)
        return client.beta.messages.create(betas=["server-side-fallback-2026-07-01"],
                                           extra_body={"fallbacks": "default"}, **kwargs)
    except anthropic.BadRequestError as e:
        if "fallback" in str(e).lower():
            return client.messages.create(**kwargs)
        raise


def work(client, out, i, label, svc, budget, source=DEFAULT_SOURCE):
    f = out / f"c{i:03d}.json"
    if f.exists():
        return f"skip c{i:03d}"
    with lock:
        if usd() >= budget:
            return f"BUDGET STOP before c{i:03d} (${usd():.2f})"
    url = f"{svc}/full/{WIDTH},/0/default.jpg"
    try:
        r = call(client, url, source)
    except anthropic.APIStatusError as e:
        return f"ERR c{i:03d} HTTP {e.status_code}: {str(e)[:120]}"
    except anthropic.APIConnectionError as e:
        return f"ERR c{i:03d} connection: {str(e)[:120]}"
    text = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
    m = re.search(r"\{.*\}", text, re.S)
    try:
        data = json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        data = None
    rec = {"canvas": i, "label": label, "image": url, "model": r.model,
           "stop_reason": r.stop_reason, "parsed": data is not None,
           "result": data if data is not None else {"raw": text}}
    f.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    with lock:
        spent["in"] += r.usage.input_tokens
        spent["out"] += r.usage.output_tokens
        spent["pages"] += 1
    n = len(data.get("items", [])) if data else "?"
    leg = data.get("legibility", "?") if data else "unparsed"
    return f"ok c{i:03d} [{label}] {leg} items={n} stop={r.stop_reason} (${usd():.2f})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("out_dir")
    ap.add_argument("--only", help="comma-separated canvas indices")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--budget", type=float, default=20.0)
    ap.add_argument("--source", default=DEFAULT_SOURCE,
                    help="one-line description of the manuscript (author, archive, dates, languages)")
    a = ap.parse_args()

    key = pathlib.Path.home().joinpath(".config/hunt/anthropic_key").read_text().strip()
    client = anthropic.Anthropic(api_key=key, max_retries=4, timeout=600)
    out = pathlib.Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pages = list(canvases(a.manifest))
    if a.only:
        keep = {int(x) for x in a.only.split(",")}
        pages = [p for p in pages if p[0] in keep]
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(work, client, out, i, lab, svc, a.budget, a.source) for i, lab, svc in pages]
        for fu in as_completed(futs):
            print(fu.result(), flush=True)
    print(f"\nDONE {spent['pages']} pages in {time.time()-t0:.0f}s | tokens in={spent['in']} "
          f"out={spent['out']} | est. cost ${usd():.2f}", flush=True)


if __name__ == "__main__":
    main()
