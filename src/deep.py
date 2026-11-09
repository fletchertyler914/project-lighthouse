#!/usr/bin/env python3
"""
deep.py — DEEP per-page analysis (not skimming).

For each mathematical page: send the page IMAGE + its transcription + the transcriptions of the
previous and next pages (arguments run across sheets) to Claude at high effort, and ask it to
reconstruct the mathematics step by step in modern notation, check correctness, identify modern
equivalents and attributions, score how surprising the content would be, and list concrete
checkable formulas. Output is for triage; top pages get hand verification (STATE rule 2).

Key: ~/.config/hunt/anthropic_key (never printed). Resumable. Bug-guard budget.

    python3 -E -P src/deep.py <transcripts_root> <out_dir> --author "Carl Friedrich Gauss" \
        --died 1855 [--bundles Math.28,Math.21] [--workers 4] [--effort high]
"""
import argparse
import json
import pathlib
import sys
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from jsonfix import lenient_json  # noqa: E402

MODEL = "claude-opus-5-5"
PRICE_IN, PRICE_OUT = 4.00 / 1e6, 20.00 / 1e6
SKIP_WORDS = re.compile(r"\b(envelope|address cover|calibration|colour card|color card|book order|"
                        r"household accounts|library note|blank)\b", re.I)

PROMPT = """You are a research mathematician and historian of mathematics doing a DEEP reading of one
page of the unpublished manuscripts of {author} (died {died}), bundle "{bundle}", folio {label}.
You get the page image, a machine transcription of it (may contain errors - trust the image), and
transcriptions of the previous and next pages for context.

Work carefully and completely:
1. RECONSTRUCT: restate every derivation on the page in modern notation, step by step. Say exactly
   what is being computed and what problem it serves. Fill implicit steps only when certain and mark
   them as yours.
2. CHECK: is each step correct? Note errors, slips, or unjustified steps.
3. IDENTIFY: for each substantive result/method: its modern name or closest modern equivalent; who
   is usually credited and when; whether the literature already credits {author} (say what you
   know, or "unsure"). Distinguish routine material from anything non-standard.
4. SURPRISE (0-10): how surprising would it be to a modern specialist/historian, if verified, that
   {author} had this here? 0 = routine or well known as his; 5 = notable unpublished detail;
   8+ = a major result usually credited to someone later and not known to be his.
   Be calibrated and conservative: most pages are 0-2.
5. CHECKABLE: list concrete formulas/claims that a computer algebra system could verify, written
   in plain sympy-compatible notation, each with what it asserts.

Return ONLY JSON:
{{"reconstruction": str, "errors": [str], "results": [{{"what": str, "modern_name": str,
  "usually_credited_to": str, "already_credited_to_author": "yes"|"no"|"unsure", "routine": bool}}],
  "surprise": int, "surprise_reason": str, "checkable": [{{"sympy": str, "asserts": str}}],
  "transcription_corrections": [str]}}

PREVIOUS PAGE (transcription):
{prev}

THIS PAGE (transcription):
{this}

NEXT PAGE (transcription):
{next}
"""

lock = threading.Lock()
spent = {"in": 0, "out": 0, "n": 0}


def usd():
    return spent["in"] * PRICE_IN + spent["out"] * PRICE_OUT


def pages(root, bundles):
    for bdir in sorted(p for p in pathlib.Path(root).iterdir() if p.is_dir()):
        if bundles and bdir.name not in bundles:
            continue
        recs = []
        for f in sorted(bdir.glob("c*.json")):
            rec = json.loads(f.read_text(encoding="utf-8"))
            res = rec.get("result", {}) if rec.get("parsed") else {}
            recs.append((f.stem, rec, res))
        for k, (stem, rec, res) in enumerate(recs):
            if not res or res.get("legibility") == "blank":
                continue
            tr = (res.get("transcription") or "").strip()
            if len(tr) < 80 or SKIP_WORDS.search(res.get("topic_en", "")) and not res.get("methods"):
                continue
            prev = recs[k - 1][2].get("transcription", "") if k > 0 else ""
            nxt = recs[k + 1][2].get("transcription", "") if k + 1 < len(recs) else ""
            yield bdir.name, stem, rec, tr, prev, nxt


def work(client, out, bundle, stem, rec, tr, prev, nxt, author, died, effort, budget):
    f = out / f"{bundle}_{stem}.json"
    if f.exists():
        return f"skip {f.name}"
    with lock:
        if usd() >= budget:
            return f"BUDGET STOP (${usd():.2f})"
    content = [{"type": "image", "source": {"type": "url", "url": rec["image"]}},
               {"type": "text", "text": PROMPT.format(author=author, died=died, bundle=bundle,
                label=rec["label"], prev=prev[:5000] or "(none)", this=tr[:8000], next=nxt[:5000] or "(none)")}]
    try:
        r = client.messages.create(model=MODEL, max_tokens=32000, messages=[{"role": "user", "content": content}],
                                   extra_body={"output_config": {"effort": effort}})
    except anthropic.APIStatusError as e:
        return f"ERR {f.name} HTTP {e.status_code}: {str(e)[:140]}"
    except anthropic.APIConnectionError as e:
        return f"ERR {f.name} connection: {str(e)[:120]}"
    text = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
    data = lenient_json(text)
    f.write_text(json.dumps({"bundle": bundle, "page": stem, "label": rec["label"], "image": rec["image"],
                             "stop_reason": r.stop_reason, "deep": data if data is not None else {"raw": text}},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    with lock:
        spent["in"] += r.usage.input_tokens
        spent["out"] += r.usage.output_tokens
        spent["n"] += 1
    s = data.get("surprise") if data else "unparsed"
    return f"ok {f.name}: surprise={s} (${usd():.2f})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("out_dir")
    ap.add_argument("--author", required=True)
    ap.add_argument("--died", required=True)
    ap.add_argument("--bundles", default="", help="comma list of bundle dir names (default all)")
    ap.add_argument("--only", default="", help="comma list of page stems, e.g. c009,c010 (testing)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--budget", type=float, default=300.0)
    a = ap.parse_args()
    key = pathlib.Path.home().joinpath(".config/hunt/anthropic_key").read_text().strip()
    client = anthropic.Anthropic(api_key=key, max_retries=4, timeout=900)
    out = pathlib.Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    bundles = set(filter(None, a.bundles.split(",")))
    only = set(filter(None, a.only.split(",")))
    todo = [p for p in pages(a.root, bundles) if not only or p[1] in only]
    print(f"{len(todo)} pages to analyse deeply", flush=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(work, client, out, *p, a.author, a.died, a.effort, a.budget) for p in todo]
        for fu in as_completed(futs):
            print(fu.result(), flush=True)
    print(f"\nDONE {spent['n']} pages | in={spent['in']} out={spent['out']} | est. ${usd():.2f}", flush=True)


if __name__ == "__main__":
    main()
