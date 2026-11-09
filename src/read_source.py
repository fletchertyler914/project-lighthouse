#!/usr/bin/env python3
"""
read_source.py - per-page reading of the Montpellier Grothendieck scans (no skimming).

For each cote: download its PDF (polite, cached) into <scratch>/<cote>/ (own dir, data only),
extract the page JPEGs with src/pdf_images.py (pure Python, python -I), then
  stage 1: transcribe every page (image sent as base64)       -> <base>/transcripts/<cote>/pNNN.json
  stage 2: deep-read every non-trivial page with neighbours    -> <base>/deep/<cote>_pNNN.json
Resumable (existing JSON files are skipped). Bug-guard budget. Key never printed.

    python3 -E -P src/read_source.py 108,26,48 [--stage both|transcribe|deep] [--workers 4] [--budget 300]
        [--base data/grothendieck-montpellier] [--site https://grothendieck.umontpellier.fr] [--scratch /tmp/hunt_dl/groth]
    <base>/inventory.tsv must have columns: cote, pdf, date, pages, title (tab-separated).

ETHICS: Grothendieck's 2010 declaration -> read for research only; never republish beyond short quotes.
"""
import argparse
import base64
import json
import pathlib
import re
import subprocess
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from jsonfix import lenient_json  # noqa: E402

MODEL = "claude-opus-5-5"
PRICE_IN, PRICE_OUT = 4.00 / 1e6, 20.00 / 1e6
HUNT = pathlib.Path(__file__).resolve().parent.parent
BASE = pathlib.Path(__file__).resolve().parent.parent / "data" / "grothendieck-montpellier"
DL = pathlib.Path("/tmp/hunt_dl/groth")
UA = "hunt-research-bot (academic research; polite, cached)"
MIN_WIDTH = 500  # smallest page-scan width accepted (older library scans are ~600 px wide)
SITE = "https://grothendieck.umontpellier.fr"

T_PROMPT = """This is page {page} of {n} of item {cote} of {context}, titled "{title}" (date: {date}).
{material}

Return ONLY a JSON object:
  "legibility": "good" | "fair" | "poor" | "blank"
  "kind": "math" | "verso_unrelated" | "cover" | "blank" | "other"
  "topic_en": one plain-English sentence on what the page is about
  "transcription": verbatim transcription in the ORIGINAL language, line breaks as \\n, mathematics in
      LaTeX inside $...$, struck text as [-...-], insertions as {{+...+}}, uncertain words followed by [?].
      Do not translate, normalise or complete. For unrelated versos give only a one-line description.
  "items": every stated problem, question, conjecture, plan, definition-to-find or unproved claim:
      {{"kind": "problem"|"question"|"conjecture"|"plan"|"claim", "quote": exact words from your
       transcription, "english": faithful translation, "status_on_page": "solved on page"|"left open"|"unclear"}}
"""

D_PROMPT = """You are a research mathematician ({fields}) and historian of mathematics doing a DEEP reading
of one page of {context}, item {cote} "{title}" (date: {date}), page {page} of {n}. You get the page image, a
machine transcription (may contain errors - trust the image) and transcriptions of the neighbouring pages.

We are looking for anything the mathematical community MISSED: (a) unfinished threads nobody took up,
(b) FINISHED results or constructions on this page that are not in the literature or not credited to
{author}, (c) MISSED CONNECTIONS - links this page makes (or implies) between ideas/fields that the
later literature did not make, (d) anything else missing from the record. Most pages contain none of these.

Work carefully:
1. RECONSTRUCT the mathematics in modern language, step by step; say what problem it serves.
2. CHECK correctness; note errors or gaps.
3. IDENTIFY each substantive idea: modern name/closest modern notion; who is usually credited and when;
   whether it appears in {author}'s other published or circulated texts ({published}) - say
   "unsure" if you do not know. Never invent references.
4. MISSED? For (a)-(d) above, say concretely what would be new to a specialist today, or "none".
5. SURPRISE 0-10 (calibrated, conservative; most pages 0-2): 5 = notable unpublished detail;
   8+ = a specialist would be genuinely surprised AND it seems absent from the literature.

Return ONLY JSON:
{{"reconstruction": str, "errors": [str],
  "ideas": [{{"what": str, "modern_name": str, "usually_credited_to": str,
     "in_author_published_texts": "yes"|"no"|"unsure", "where_published": str, "routine": bool}}],
  "missed": [{{"type": "unfinished"|"finished_uncredited"|"connection"|"other", "claim": str,
     "quote": str, "why_it_might_matter_today": str}}],
  "surprise": int, "surprise_reason": str, "transcription_corrections": [str]}}

PREVIOUS PAGE (transcription):
{prev}

THIS PAGE (transcription):
{this}

NEXT PAGE (transcription):
{next}
"""

# defaults describe the Montpellier Grothendieck fonds; override per source with --context/--author/--material/--published/--fields
CTX = {
    "context": "Alexander Grothendieck's unpublished mathematical notes (Montpellier archive)",
    "author": "Grothendieck",
    "material": "Mostly French handwriting, some typescript; the page may be rotated, struck through, or be an "
                "unrelated verso (letters, listings, admin papers).",
    "published": "EGA, SGA, FGA, Esquisse d'un programme, Pursuing Stacks, Les Dérivateurs, La Longue Marche, "
                 "Récoltes et Semailles, letters",
    "fields": "algebraic geometry, topology, category theory, number theory",
}

lock = threading.Lock()
spent = {"in": 0, "out": 0, "n": 0}


def usd():
    return spent["in"] * PRICE_IN + spent["out"] * PRICE_OUT


def inventory():
    rows = {}
    lines = (BASE / "inventory.tsv").read_text(encoding="utf-8").splitlines()[1:]
    for ln in lines:
        cote, pdf, date, pages, title = ln.split("\t")
        rows[cote] = dict(cote=cote, pdf=pdf, date=date, pages=pages, title=title)
    return rows


def fetch(cote, pdf):
    d = DL / cote
    img = d / "img"
    if (img / "index.tsv").exists():
        return img
    d.mkdir(parents=True, exist_ok=True)
    f = d / pathlib.Path(pdf).name
    if not f.exists() or f.stat().st_size == 0:
        req = urllib.request.Request(f"{SITE}/{pdf}", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=600) as r, open(f, "wb") as w:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                w.write(chunk)
        time.sleep(1.5)
    subprocess.run([sys.executable, "-E", "-P", str(HUNT / "src/pdf_images.py"), str(f), str(img), "--min-width", str(MIN_WIDTH)], check=True)
    return img


def ask(client, content, effort=None, max_tokens=16000):
    kw = dict(model=MODEL, max_tokens=max_tokens, messages=[{"role": "user", "content": content}])
    if effort:
        kw["extra_body"] = {"output_config": {"effort": effort}}
    r = client.messages.create(**kw)
    text = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
    data = lenient_json(text)
    with lock:
        spent["in"] += r.usage.input_tokens
        spent["out"] += r.usage.output_tokens
        spent["n"] += 1
    return r, data, text


def image_block(path):
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                        "data": base64.b64encode(path.read_bytes()).decode()}}


def do_transcribe(client, meta, img, k, n, budget):
    out = BASE / "transcripts" / meta["cote"] / f"p{k:03d}.json"
    if out.exists():
        return f"skip T {meta['cote']} p{k:03d}"
    with lock:
        if usd() >= budget:
            return f"BUDGET STOP (${usd():.2f})"
    content = [image_block(img / f"p{k:03d}.jpg"),
               {"type": "text", "text": T_PROMPT.format(page=k, n=n, cote=meta["cote"], title=meta["title"], date=meta["date"], **CTX)}]
    try:
        r, data, text = ask(client, content)
    except anthropic.APIError as e:
        return f"ERR T {meta['cote']} p{k:03d}: {str(e)[:140]}"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"cote": meta["cote"], "page": k, "stop_reason": r.stop_reason, "parsed": data is not None,
                               "result": data if data is not None else {"raw": text}}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    d = data or {}
    return f"ok T {meta['cote']} p{k:03d} {d.get('kind')} {d.get('legibility')} items={len(d.get('items', []))} (${usd():.2f})"


def tr_of(cote, k):
    f = BASE / "transcripts" / cote / f"p{k:03d}.json"
    if not f.exists():
        return {}
    rec = json.loads(f.read_text(encoding="utf-8"))
    return rec["result"] if rec.get("parsed") else {}


def do_deep(client, meta, img, k, n, effort, budget):
    out = BASE / "deep" / f"{meta['cote']}_p{k:03d}.json"
    if out.exists():
        return f"skip D {out.name}"
    this = tr_of(meta["cote"], k)
    if not this or this.get("kind") not in ("math", "other") or this.get("legibility") == "blank" \
            or len((this.get("transcription") or "").strip()) < 80:
        return f"skip D {out.name} (not math / too short)"
    with lock:
        if usd() >= budget:
            return f"BUDGET STOP (${usd():.2f})"
    prev = tr_of(meta["cote"], k - 1).get("transcription", "") if k > 1 else ""
    nxt = tr_of(meta["cote"], k + 1).get("transcription", "") if k < n else ""
    content = [image_block(img / f"p{k:03d}.jpg"),
               {"type": "text", "text": D_PROMPT.format(cote=meta["cote"], title=meta["title"], date=meta["date"], **CTX,
                page=k, n=n, prev=prev[:5000] or "(none)", this=this["transcription"][:9000], next=nxt[:5000] or "(none)")}]
    try:
        r, data, text = ask(client, content, effort=effort, max_tokens=32000)
    except anthropic.APIError as e:
        return f"ERR D {out.name}: {str(e)[:140]}"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"cote": meta["cote"], "title": meta["title"], "page": k, "stop_reason": r.stop_reason,
                               "deep": data if data is not None else {"raw": text}}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    return f"ok D {out.name}: surprise={(data or {}).get('surprise', 'unparsed')} (${usd():.2f})"


def main():
    global BASE, SITE, DL
    ap = argparse.ArgumentParser()
    ap.add_argument("cotes", help="comma list, e.g. 108,26,150")
    ap.add_argument("--stage", default="both", choices=["both", "transcribe", "deep"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--effort", default="high")
    ap.add_argument("--budget", type=float, default=300.0)
    ap.add_argument("--base", default=str(BASE), help="data dir holding inventory.tsv, transcripts/, deep/")
    ap.add_argument("--site", default=SITE, help="base URL the inventory's pdf column is relative to")
    ap.add_argument("--scratch", default=str(DL), help="download/extraction dir (own dir, data only)")
    ap.add_argument("--context", default=CTX["context"], help="what the source is, e.g. 'Leonhard Euler's printed works (Euler Archive scans)'")
    ap.add_argument("--author", default=CTX["author"])
    ap.add_argument("--material", default=CTX["material"], help="one or two sentences on what the pages physically are")
    ap.add_argument("--published", default=CTX["published"], help="where to check whether the author published it")
    ap.add_argument("--fields", default=CTX["fields"])
    a = ap.parse_args()
    CTX.update(context=a.context, author=a.author, material=a.material, published=a.published, fields=a.fields)
    BASE, SITE, DL = pathlib.Path(a.base), a.site.rstrip("/"), pathlib.Path(a.scratch)
    inv = inventory()
    key = pathlib.Path.home().joinpath(".config/hunt/anthropic_key").read_text().strip()
    client = anthropic.Anthropic(api_key=key, max_retries=4, timeout=900)
    for cote in filter(None, a.cotes.split(",")):
        meta = inv[cote]
        img = fetch(cote, meta["pdf"])
        n = len((img / "index.tsv").read_text().splitlines()) - 1
        print(f"== cote {cote} ({n} pages) {meta['title'][:70]}", flush=True)
        if n <= 0:
            print(f"== SKIP cote {cote}: no page images extracted (unsupported encoding or too small); see {img}", flush=True)
            continue
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            if a.stage in ("both", "transcribe"):
                for fu in as_completed([ex.submit(do_transcribe, client, meta, img, k, n, a.budget) for k in range(1, n + 1)]):
                    print(fu.result(), flush=True)
            if a.stage in ("both", "deep"):
                for fu in as_completed([ex.submit(do_deep, client, meta, img, k, n, a.effort, a.budget) for k in range(1, n + 1)]):
                    print(fu.result(), flush=True)
        print(f"== done cote {cote} | total ${usd():.2f} ({spent['n']} calls)", flush=True)
    print(f"RUN DONE | in={spent['in']} out={spent['out']} | ${usd():.2f}", flush=True)


if __name__ == "__main__":
    main()
