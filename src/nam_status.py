#!/usr/bin/env python3
"""
nam_status.py - status check for the Nouvelles Annales "questions non résolues" statements.

Stages (each resumable; all evidence kept under <base>/evidence/):
  triage   model, batched: field, modern restatement, whether an elementary computation can settle it (+ a sympy
           plan), 2-3 literature search queries per source, and what the model believes the status is (a CLAIM to
           test, never evidence on its own).                             -> evidence/triage/<n>.json
  search   no model: zbMATH Open API, StackExchange API (math.SE, MathOverflow), Wikipedia (en, fr), OEIS when the
           triage gives sequence terms, Dickson's History OCR by (year, page) of the original NAM citation, and the
           zbMATH/JFM harvest of NAM items titled "Question NNNN" (solutions indexed by the Jahrbuch).
           Polite: ~1 request/s, fixed User-Agent.                       -> evidence/search/<n>.json
  judge    model, per question: statement + triage + search hits -> status in
           {solved here, solved since (where, year), still apparently open, ill-posed/false as stated, unclear}
           with status_evidence naming every search run.                 -> evidence/judge/<n>.json, status.json
Elementary checks proposed by the triage are NOT run here: they are reviewed by a human/agent and, if sound,
saved as verify/nam_q<n>.py and run by hand (model code is untrusted).

    python3 -E -P src/nam_status.py triage|search|judge|all [--base data/nouvelles-annales] [--budget 20]
        [--numbers 1105,1074] [--workers 3]
"""
import argparse
import json
import pathlib
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from jsonfix import lenient_json  # noqa: E402

MODEL = "claude-opus-5-5"
PRICE_IN, PRICE_OUT = 4.00 / 1e6, 20.00 / 1e6
HUNT = pathlib.Path(__file__).resolve().parent.parent
BASE = HUNT / "data" / "nouvelles-annales"
UA = "hunt-research-bot (academic research)"
DICKSON = pathlib.Path("/tmp/hunt_dl/dickson")
JFM = pathlib.Path("/tmp/hunt_dl/zbmath")

lock = threading.Lock()
spent = {"in": 0, "out": 0, "n": 0}
net_lock = threading.Lock()
last_net = [0.0]


def usd():
    return spent["in"] * PRICE_IN + spent["out"] * PRICE_OUT


def polite_get(url, timeout=60):
    with net_lock:
        wait = 1.05 - (time.time() - last_net[0])
        if wait > 0:
            time.sleep(wait)
        last_net[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def get_json(url):
    try:
        return json.loads(polite_get(url))
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}


TRIAGE_PROMPT = """You are a research mathematician and historian of 19th-century mathematics. Below are {k} problems
("questions") posed in the Nouvelles Annales de Mathématiques between 1842 and 1910 that the journal's editors
listed in 1915 as never having received a published solution, and reprinted in 1916-18. For EACH, return a
triage record. Be concrete and conservative; "unsure" is a fine answer. Never invent references.

Return ONLY a JSON object {{"records": [ ... ]}} with one record per question, in the given order:
  "number": the question number as given
  "field": one of "number theory" | "geometry" | "analysis" | "algebra" | "probability" | "mechanics" | "other"
  "subfield": short free text (e.g. "triangle geometry", "Diophantine equations", "elliptic functions")
  "modern_restatement_en": precise modern restatement, 1-4 sentences, LaTeX allowed
  "kind": "prove" | "find/characterise" | "compute" | "construct" | "ill-defined"
  "well_posed": true | false, with "well_posed_note" explaining any ambiguity, missing hypothesis or known error
  "elementary_check": {{"possible": true|false, "plan": how sympy/numeric search could settle or test it
      (finite search bounds, what would count as PASS/FAIL), "code": complete python3 (sympy allowed) that prints
      PASS/FAIL lines and runs in < 60 s, or ""}}
  "searches": {{"zbmath": [2 short English keyword queries], "stackexchange": [1 English query],
      "wikipedia": [1 English query, 1 French query], "oeis": [a sequence of integer terms as a string, or ""],
      "names": [classical names/terms a historian would search, e.g. "Brocard", "Malfatti circles"]}}
  "belief": {{"status": "known classical theorem" | "known to be solved later" | "known open" | "unclear" |
      "ill-posed/false", "note": 1-3 sentences, "possible_sources": [named books/papers, may be empty]}}

QUESTIONS:
{questions}
"""

JUDGE_PROMPT = """You are a careful research mathematician and historian. Decide the present-day status of one problem
posed in the Nouvelles Annales de Mathématiques (never solved in the journal, listed as open in 1915, reprinted
1916-18). You get the statement, a triage record (a prior belief - a CLAIM to test, not evidence) and the raw
results of literature searches. Use ONLY the search results and standard, nameable mathematics as evidence;
when you rely on your own knowledge of a theorem, say so explicitly and give the standard name or a checkable
reference, and lower your confidence.

Status vocabulary (pick exactly one):
  "solved here"                 only if a complete elementary argument settles it (a passing numerical check alone is
                                NOT enough unless the statement is a finite/decidable computation); give the full
                                argument in `argument`; if the check refutes the statement use "ill-posed/false"
  "solved since (where, year)"  a search hit or a named, checkable publication after the posing settles it
                                (also use this when the statement is a theorem that is standard in the later
                                literature; give the standard name and a source)
  "still apparently open"       only if at least THREE distinct searches were run and none found a solution,
                                and you know of none; list the searches
  "ill-posed/false as stated"   with the reason (counterexample, missing hypothesis, misprint)
  "unclear"                     anything else (e.g. too vague to search, hits ambiguous)

Return ONLY JSON:
{{"number": "...", "status": "...", "confidence": "high"|"medium"|"low",
  "status_evidence": one paragraph naming every search run (source and query) and what each found, then the
      decisive evidence or its absence; plain language; no claims beyond the evidence,
  "argument": full mathematical argument if status is "solved here", else "",
  "interest_0_10": how interesting the problem is for a modern reader if genuinely open (0 routine, 10 striking),
  "interest_reason": one sentence}}

QUESTION {number} ({citation}; proposer: {author}):
FR: {fr}
EN: {en}

TRIAGE (prior belief, to be tested):
{triage}

SEARCH RESULTS:
{hits}

ELEMENTARY CHECK (model-written code run in a sandbox; treat its output as a hint, judge the code yourself):
{checks}
"""


def ask(client, prompt, max_tokens=16000):
    import anthropic  # noqa: F401
    r = client.messages.create(model=MODEL, max_tokens=max_tokens, messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
    with lock:
        spent["in"] += r.usage.input_tokens
        spent["out"] += r.usage.output_tokens
        spent["n"] += 1
    return lenient_json(text), text


def load_questions(base, numbers):
    qs = json.loads((base / "questions.json").read_text(encoding="utf-8"))
    qs.pop("?", None)
    if numbers:
        qs = {n: qs[n] for n in numbers if n in qs}

    def key(n):
        m = re.match(r"(\d+)(?: (bis|ter))?", n)
        return (int(m.group(1)), m.group(2) or "")
    return dict(sorted(qs.items(), key=lambda kv: key(kv[0])))


def fname(n):
    return n.replace(" ", "_")


# ----------------------------------------------------------------------------------------------- triage
def stage_triage(client, base, qs, budget, workers, batch=6):
    out = base / "evidence" / "triage"
    out.mkdir(parents=True, exist_ok=True)
    todo = [n for n in qs if not (out / f"{fname(n)}.json").exists()]
    batches = [todo[i:i + batch] for i in range(0, len(todo), batch)]

    def run(b):
        with lock:
            if usd() >= budget:
                return f"BUDGET STOP ${usd():.2f}"
        txt = "\n\n".join(f"[{n}] ({qs[n].get('year_posed')}, p. {qs[n].get('page_cited')}; {qs[n].get('author') or 'no proposer'})\n"
                          f"FR: {qs[n].get('statement_fr')}\nEN: {qs[n].get('statement_en')}" for n in b)
        data, text = ask(client, TRIAGE_PROMPT.format(k=len(b), questions=txt), max_tokens=24000)
        if not data or "records" not in data:
            return f"ERR unparsed triage batch {b}"
        got = 0
        for rec in data["records"]:
            n = str(rec.get("number", "")).strip()
            n = re.sub(r"^\[|\]$", "", n)
            if n in b:
                (out / f"{fname(n)}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
                got += 1
        return f"triage {b}: {got}/{len(b)} (${usd():.2f})"

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for fu in as_completed([ex.submit(run, b) for b in batches]):
            print(fu.result(), flush=True)


# ----------------------------------------------------------------------------------------------- search
def zb_search(q, n=5):
    url = "https://api.zbmath.org/v1/document/_search?" + urllib.parse.urlencode({"search_string": q, "page": 0, "results_per_page": n})
    d = get_json(url)
    if "error" in d:
        return {"query": q, "error": d["error"]}
    res = []
    for r in d.get("result") or []:
        res.append({"id": r.get("id"), "year": r.get("year"), "title": (r.get("title") or {}).get("title"),
                    "source": (r.get("source") or {}).get("source"),
                    "authors": [a.get("name") for a in (r.get("contributors") or {}).get("authors") or []][:4]})
    return {"query": q, "total": (d.get("status") or {}).get("nr_total_results"), "hits": res}


def se_search(q, site, n=5):
    url = "https://api.stackexchange.com/2.3/search/advanced?" + urllib.parse.urlencode(
        {"order": "desc", "sort": "relevance", "q": q, "site": site, "pagesize": n, "filter": "default"})
    import gzip
    try:
        raw = polite_get(url)
        try:
            raw = gzip.decompress(raw)
        except Exception:  # noqa: BLE001
            pass
        d = json.loads(raw)
    except Exception as e:  # noqa: BLE001
        return {"query": q, "site": site, "error": str(e)[:200]}
    return {"query": q, "site": site, "quota_remaining": d.get("quota_remaining"),
            "hits": [{"title": i.get("title"), "link": i.get("link"), "answered": i.get("is_answered"), "score": i.get("score")}
                     for i in d.get("items") or []]}


def wiki_search(q, lang="en", n=5):
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "list": "search", "srsearch": q, "format": "json", "srlimit": n})
    d = get_json(url)
    if "error" in d:
        return {"query": q, "lang": lang, "error": d["error"]}
    return {"query": q, "lang": lang,
            "hits": [{"title": i.get("title"), "snippet": re.sub(r"<[^>]+>", "", i.get("snippet", ""))} for i in (d.get("query") or {}).get("search") or []]}


def oeis_search(terms, n=4):
    url = "https://oeis.org/search?" + urllib.parse.urlencode({"q": terms, "fmt": "json"})
    d = get_json(url)
    if isinstance(d, dict) and "error" in d:
        return {"query": terms, "error": d["error"]}
    res = d.get("results") if isinstance(d, dict) else d
    return {"query": terms, "hits": [{"A": f"A{r['number']:06d}", "name": r.get("name")} for r in (res or [])[:n]]}


_dickson_cache = {}


def dickson_lookup(year, page, names):
    """Lines of Dickson's History (OCR) citing Nouv. Ann. Math. <year>, <page> or mentioning a searched name."""
    if not _dickson_cache:
        for f in sorted(DICKSON.glob("*.txt")):
            t = f.read_text(encoding="utf-8", errors="replace")
            if t.lstrip().startswith("<!DOCTYPE"):
                continue
            _dickson_cache[f.stem] = re.sub(r"[ \t]+", " ", t)
    hits = []
    if year:
        pat = re.compile(r"Nouv\. ?Ann\.? ?(?:Math\.?)?,?[^;\n]{0,25}?" + str(year) + r",? ?(\d[\d\-, ]*)")
        for vol, t in _dickson_cache.items():
            for m in pat.finditer(t):
                pages = re.findall(r"\d+", m.group(1))
                if page and any(abs(int(p) - int(page)) <= 1 for p in pages[:3] if p.isdigit()):
                    s = max(0, m.start() - 250)
                    hits.append({"vol": vol, "match": m.group(0), "context": t[s:m.end() + 80].replace("\n", " ")})
    return {"year_page": f"{year}, {page}", "hits": hits[:6]}


_jfm_cache = {}


def jfm_lookup(number):
    """zbMATH/JFM entries for NAM items whose title names this question number."""
    if not _jfm_cache:
        for f in JFM.glob("*.json"):
            for r in json.loads(f.read_text(encoding="utf-8")):
                _jfm_cache[r["id"]] = r
    n0 = re.match(r"\d+", number).group(0)
    hits = []
    for r in _jfm_cache.values():
        t = (r.get("title") or {}).get("title") or ""
        if re.search(rf"(?<![\d.]){n0}(?![\d])", t):
            hits.append({"id": r.get("id"), "year": r.get("year"), "title": t[:160], "source": (r.get("source") or {}).get("source"),
                         "authors": [a.get("name") for a in (r.get("contributors") or {}).get("authors") or []][:3]})
    return {"number": number, "hits": sorted(hits, key=lambda h: h.get("year") or "")}


def stage_search(base, qs, workers):
    tdir, out = base / "evidence" / "triage", base / "evidence" / "search"
    out.mkdir(parents=True, exist_ok=True)

    def run(n):
        f = out / f"{fname(n)}.json"
        if f.exists():
            return f"skip search {n}"
        tf = tdir / f"{fname(n)}.json"
        tri = json.loads(tf.read_text(encoding="utf-8")) if tf.exists() else {}
        s = tri.get("searches") or {}
        q = qs[n]
        rec = {"number": n, "zbmath": [], "stackexchange": [], "wikipedia": [], "oeis": [], "dickson": {}, "jfm_titles": {}}
        for qq in (s.get("zbmath") or [])[:2]:
            rec["zbmath"].append(zb_search(qq))
        for nm in (s.get("names") or [])[:1]:
            rec["zbmath"].append(zb_search(nm))
        for qq in (s.get("stackexchange") or [])[:1]:
            rec["stackexchange"].append(se_search(qq, "math.stackexchange"))
            if (tri.get("belief") or {}).get("status") in ("known open", "unclear"):
                rec["stackexchange"].append(se_search(qq, "mathoverflow"))
        wq = s.get("wikipedia") or []
        if wq:
            rec["wikipedia"].append(wiki_search(wq[0], "en"))
        if len(wq) > 1:
            rec["wikipedia"].append(wiki_search(wq[1], "fr"))
        if s.get("oeis"):
            rec["oeis"].append(oeis_search(s["oeis"]))
        rec["dickson"] = dickson_lookup(q.get("year_posed"), q.get("page_cited"), s.get("names") or [])
        rec["jfm_titles"] = jfm_lookup(n)
        f.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        nh = sum(len(x.get("hits", [])) for k in ("zbmath", "stackexchange", "wikipedia", "oeis") for x in rec[k])
        return f"search {n}: {nh} web hits, dickson={len(rec['dickson'].get('hits', []))}, jfm={len(rec['jfm_titles'].get('hits', []))}"

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for fu in as_completed([ex.submit(run, n) for n in qs]):
            print(fu.result(), flush=True)


# ----------------------------------------------------------------------------------------------- check
def stage_check(base, qs, timeout=120):
    """Run the triage's proposed elementary checks (model-written python) in a scratch dir with a timeout.
    Output goes to evidence/checks/<n>.json and is shown to the judge as raw text; nothing is trusted blindly -
    a human/agent reviews the code before any 'solved here' verdict is kept (see verify/nam_q*.py)."""
    import subprocess
    import tempfile
    tdir, out = base / "evidence" / "triage", base / "evidence" / "checks"
    out.mkdir(parents=True, exist_ok=True)
    scratch = pathlib.Path(tempfile.mkdtemp(prefix="nam_checks_"))
    for n in qs:
        f = out / f"{fname(n)}.json"
        tf = tdir / f"{fname(n)}.json"
        if f.exists() or not tf.exists():
            continue
        ec = (json.loads(tf.read_text(encoding="utf-8")).get("elementary_check") or {})
        code = (ec.get("code") or "").strip()
        if not ec.get("possible") or len(code) < 20:
            continue
        src = scratch / f"q{fname(n)}.py"
        src.write_text(code, encoding="utf-8")
        t0 = time.time()
        try:
            r = subprocess.run([sys.executable, "-E", "-P", str(src)], capture_output=True, text=True, timeout=timeout, cwd=str(scratch))
            res = {"number": n, "plan": ec.get("plan"), "code": code, "returncode": r.returncode,
                   "stdout": r.stdout[-6000:], "stderr": r.stderr[-3000:], "seconds": round(time.time() - t0, 1)}
        except subprocess.TimeoutExpired:
            res = {"number": n, "plan": ec.get("plan"), "code": code, "returncode": None, "stdout": "", "stderr": f"TIMEOUT after {timeout}s", "seconds": timeout}
        f.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        tag = "PASS" if "PASS" in res["stdout"] and "FAIL" not in res["stdout"] else "FAIL/ERR" if res["returncode"] else "mixed"
        print(f"check {n}: rc={res['returncode']} {tag} {res['seconds']}s | {res['stdout'].strip().splitlines()[-1][:100] if res['stdout'].strip() else res['stderr'].strip().splitlines()[-1][:100] if res['stderr'].strip() else ''}", flush=True)


# ----------------------------------------------------------------------------------------------- judge
def stage_judge(client, base, qs, budget, workers):
    tdir, sdir, out = base / "evidence" / "triage", base / "evidence" / "search", base / "evidence" / "judge"
    out.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(HUNT / "src"))
    from nam_table import citation  # noqa: E402

    def run(n):
        f = out / f"{fname(n)}.json"
        if f.exists():
            return f"skip judge {n}"
        with lock:
            if usd() >= budget:
                return f"BUDGET STOP ${usd():.2f}"
        q = qs[n]
        tri = json.loads((tdir / f"{fname(n)}.json").read_text(encoding="utf-8")) if (tdir / f"{fname(n)}.json").exists() else {}
        hits = json.loads((sdir / f"{fname(n)}.json").read_text(encoding="utf-8")) if (sdir / f"{fname(n)}.json").exists() else {}
        tri_small = {k: tri.get(k) for k in ("field", "subfield", "modern_restatement_en", "kind", "well_posed", "well_posed_note", "belief")}
        cdir = base / "evidence" / "checks"
        chk = json.loads((cdir / f"{fname(n)}.json").read_text(encoding="utf-8")) if (cdir / f"{fname(n)}.json").exists() else None
        chk_txt = ("(no elementary check was run)" if not chk else
                   f"plan: {chk.get('plan')}\ncode:\n{chk.get('code')}\nreturncode: {chk.get('returncode')}\nstdout:\n{chk.get('stdout')}\nstderr:\n{chk.get('stderr')}")
        prompt = JUDGE_PROMPT.format(number=n, citation=citation(q.get("year_posed"), q.get("page_cited")), author=q.get("author") or "none",
                                     fr=q.get("statement_fr"), en=q.get("statement_en"),
                                     triage=json.dumps(tri_small, ensure_ascii=False, indent=1),
                                     hits=json.dumps(hits, ensure_ascii=False, indent=1)[:30000], checks=chk_txt[:12000])
        data, text = ask(client, prompt, max_tokens=12000)
        if not data:
            return f"ERR unparsed judge {n}"
        data["number"] = n
        f.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        return f"judge {n}: {data.get('status')} [{data.get('confidence')}] interest={data.get('interest_0_10')} (${usd():.2f})"

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for fu in as_completed([ex.submit(run, n) for n in qs]):
            print(fu.result(), flush=True)


def write_status(base):
    """Collect judge records (+ triage field) into status.json for nam_table.py."""
    tdir, jdir = base / "evidence" / "triage", base / "evidence" / "judge"
    sf = base / "status.json"
    status = json.loads(sf.read_text(encoding="utf-8")) if sf.exists() else {}
    for f in sorted(jdir.glob("*.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        n = j["number"]
        t = json.loads((tdir / f.name).read_text(encoding="utf-8")) if (tdir / f.name).exists() else {}
        rec = status.get(n, {})
        if rec.get("locked"):  # hand-written verdicts (e.g. "solved here" after a verify/ script) are kept
            continue
        rec.update({"field": t.get("field", rec.get("field", "")), "status": j.get("status", ""), "confidence": j.get("confidence", ""),
                    "status_evidence": j.get("status_evidence", ""), "interest": j.get("interest_0_10"),
                    "interest_reason": j.get("interest_reason", ""), "source": f"model {MODEL} judge over evidence/search"})
        status[n] = rec
    sf.write_text(json.dumps(status, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"status.json: {len(status)} records")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["triage", "search", "check", "judge", "all", "collect"])
    ap.add_argument("--base", default=str(BASE))
    ap.add_argument("--budget", type=float, default=20.0)
    ap.add_argument("--numbers", default="")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    base = pathlib.Path(a.base)
    numbers = [x.strip() for x in a.numbers.split(",") if x.strip()]
    qs = load_questions(base, numbers)
    client = None
    if a.stage in ("triage", "judge", "all"):
        import anthropic
        key = pathlib.Path.home().joinpath(".config/hunt/anthropic_key").read_text().strip()
        client = anthropic.Anthropic(api_key=key, max_retries=4, timeout=900)
    if a.stage in ("triage", "all"):
        stage_triage(client, base, qs, a.budget, a.workers)
    if a.stage in ("search", "all"):
        stage_search(base, qs, workers=2)
    if a.stage in ("check", "all"):
        stage_check(base, qs)
    if a.stage in ("judge", "all"):
        stage_judge(client, base, qs, a.budget, a.workers)
    if a.stage in ("judge", "all", "collect"):
        write_status(base)
    print(f"DONE | {spent['n']} model calls | ${usd():.2f}")


if __name__ == "__main__":
    main()
