#!/usr/bin/env python3
"""
nam_table.py - build data/nouvelles-annales/unsolved_1842_1910.tsv from the page transcripts.

  1. master list   = number_list of NAM_1915_4_15__246_0 (the 1915 "Liste des numéros des questions restées sans
                     solutions depuis 1842 jusqu'à 1910"), plus the earlier lists (1863, 1868) for cross-reference
  2. statements    = `questions` records of the 1916-18 "Anciennes questions non résolues" reprints, with
                     fragments split over a page break merged (starts_on_previous_page / continues_on_next_page)
  3. status        = data/nouvelles-annales/status.json  {number: {field, status, status_evidence}} written by the
                     status-check step (nam_status.py / by hand); missing -> "unchecked"
Writes questions.json (merged statements, one per number) and the TSV. Pure data processing: run with python3 -I.

    python3 -I src/nam_table.py [--base data/nouvelles-annales]
"""
import argparse
import json
import pathlib
import re

HUNT = pathlib.Path(__file__).resolve().parent.parent
BASE = HUNT / "data" / "nouvelles-annales"
LIST_1915 = "NAM_1915_4_15__246_0"
LIST_1917 = "NAM_1918_4_18__37_1"   # p. 40: numbers still unsolved at 31 Dec 1917 (116 numbers)
LISTS_OLD = {"NAM_1863_2_2__225_0": "1863", "NAM_1868_2_7__144_0": "1868"}   # 1863 = full statements (vols 1-15); 1868 = bare numbers
# items that are not reprints of statements (bare-number lists, editorials, articles about a question): never merged as statements
NOT_REPRINTS = {"NAM_1868_2_7__144_0", "NAM_1915_4_15__241_0", "NAM_1915_4_15__480_0", "NAM_1918_4_18__25_1", LIST_1917}
COLS = ["question_number", "year_posed", "original_citation", "author", "statement_fr", "statement_en",
        "field", "status", "status_evidence", "reprint_source", "on_1915_list", "on_1917_list", "on_1863_list", "on_1868_list"]


def pages(base, cote):
    d = base / "transcripts" / cote
    out = []
    for f in sorted(d.glob("p*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        if rec.get("parsed"):
            out.append((rec["page"], rec["result"]))
    return out


def norm_num(s):
    s = str(s).strip().replace(" ", " ")
    m = re.match(r"^(\d+)\s*(bis|ter)?\.?$", s, re.I)
    if not m:
        return s
    return m.group(1) + ((" " + m.group(2).lower()) if m.group(2) else "")


def series_volume(year):
    """Nouvelles Annales: s.1 1842-61 (t.1-20), s.2 1862-81, s.3 1882-1901, s.4 1902-21."""
    y = int(year)
    for s, y0 in ((1, 1842), (2, 1862), (3, 1882), (4, 1902)):
        if y0 <= y < y0 + 20:
            return s, y - y0 + 1
    return None, None


def citation(year, page):
    if not year:
        return ""
    s, t = series_volume(year)
    ser = f"({s}) t. {t}" if s else ""
    pg = f", p. {page}" if page else ""
    return f"Nouv. Ann. Math. {ser}, {year}{pg}".replace(" ,", ",")


def merge_statements(base, inv):
    """Walk every reprint item page by page and glue fragments across page breaks."""
    merged = []   # list of dicts
    for cote in inv:
        if cote == LIST_1915 or cote in NOT_REPRINTS:
            continue
        open_frag = None
        last_on_prev_page = None
        for pno, res in pages(base, cote):
            qlist = res.get("questions") or []
            for i, q in enumerate(qlist):
                q = dict(q)
                q["reprint_source"] = f"{cote} p{pno:03d}"
                if q.get("starts_on_previous_page") and open_frag is None and i == 0 and last_on_prev_page is not None \
                        and not q.get("number"):
                    open_frag = last_on_prev_page   # the previous page's last record was not flagged as continuing
                if q.get("starts_on_previous_page") and open_frag is not None:
                    for k in ("statement_fr", "statement_en"):
                        open_frag[k] = (open_frag.get(k) or "").rstrip() + " " + (q.get(k) or "").lstrip()
                    for k in ("number", "year_posed", "page_cited", "author", "editorial_note"):
                        if not open_frag.get(k) and q.get(k):
                            open_frag[k] = q[k]
                    open_frag["reprint_source"] += f"+p{pno:03d}"
                    open_frag["continues_on_next_page"] = q.get("continues_on_next_page", False)
                    if not open_frag["continues_on_next_page"]:
                        open_frag = None
                    continue
                merged.append(q)
                open_frag = q if q.get("continues_on_next_page") else None
            last_on_prev_page = merged[-1] if merged and merged[-1]["reprint_source"].startswith(f"{cote} p{pno:03d}") else None
    by_num = {}
    for q in merged:
        n = norm_num(q.get("number") or "")
        if not n or not re.match(r"^\d", n):
            by_num.setdefault("?", []).append(q)
            continue
        if n in by_num:
            # the same question printed twice (1863 statement and 1916-18 reprint) - keep the later/longer one, note both sources
            old = by_num[n]
            if old["reprint_source"].startswith("NAM_1863") or len(q.get("statement_fr") or "") > len(old.get("statement_fr") or ""):
                q["reprint_source"] = old["reprint_source"] + " | " + q["reprint_source"]
                by_num[n] = q
            else:
                old["reprint_source"] += " | " + q["reprint_source"]
        else:
            by_num[n] = q
    return by_num


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(BASE))
    a = ap.parse_args()
    base = pathlib.Path(a.base)
    inv = [ln.split("\t")[0] for ln in (base / "inventory.tsv").read_text(encoding="utf-8").splitlines()[1:]]

    master = []
    for pno, res in pages(base, LIST_1915):
        master += [norm_num(x) for x in res.get("number_list") or []]
    old = {}
    for cote, yr in LISTS_OLD.items():
        old[yr] = set()
        for pno, res in pages(base, cote):
            old[yr] |= {norm_num(x) for x in res.get("number_list") or []}
            old[yr] |= {norm_num(q.get("number") or "") for q in res.get("questions") or [] if q.get("number")}

    still_1917 = set()
    for pno, res in pages(base, LIST_1917):
        still_1917 |= {norm_num(x) for x in res.get("number_list") or []}

    statements = merge_statements(base, inv)
    status = {}
    sf = base / "status.json"
    if sf.exists():
        status = json.loads(sf.read_text(encoding="utf-8"))

    def key(n):
        m = re.match(r"(\d+)(?: (bis|ter))?", n)
        return (int(m.group(1)), m.group(2) or "") if m else (10**9, n)

    # rows: every number on the 1915 list, plus anything reprinted 1916-18 (statements only in the 1863 item were solved
    # before 1915 by definition of the list and are kept only in questions.json)
    numbers = sorted(set(master) | {n for n, q in statements.items() if n != "?" and not q["reprint_source"].startswith("NAM_1863")}, key=key)
    rows = []
    for n in numbers:
        q = statements.get(n, {})
        st = status.get(n, {})
        on17 = n in still_1917
        if q and not st:
            stat, ev = "unchecked", ""
        elif not q:
            stat, ev = "number only (no statement reprinted 1916-18)", ""
        else:
            stat, ev = st.get("status", ""), st.get("status_evidence", "")
        if not on17 and n in master and not st.get("locked"):
            # the editors' own 31 Dec 1917 list (NAM 1918 p. 40) no longer carries it: solved or withdrawn in 1915-17
            stat = "solved since (Nouvelles Annales 1915-1917, editors' list of 31 Dec 1917)" if not st else stat
            ev = ("absent from the editors' list of questions still unsolved at 31 Dec 1917 (NAM (4) 18, 1918, p. 40), "
                  "i.e. solved or withdrawn in the journal between June 1915 and Dec 1917" + (" | " + ev if ev else ""))
        rows.append({
            "question_number": n,
            "year_posed": q.get("year_posed") or "",
            "original_citation": citation(q.get("year_posed"), q.get("page_cited")),
            "author": q.get("author") or "",
            "statement_fr": (q.get("statement_fr") or "").replace("\t", " ").replace("\n", " "),
            "statement_en": (q.get("statement_en") or "").replace("\t", " ").replace("\n", " "),
            "field": st.get("field", "") if q else "",
            "status": stat,
            "status_evidence": (ev + (" | editorial note: " + q["editorial_note"] if q.get("editorial_note") else "")).strip(" |").replace("\t", " ").replace("\n", " "),
            "reprint_source": q.get("reprint_source", ""),
            "on_1915_list": "yes" if n in master else "no",
            "on_1917_list": "yes" if on17 else "no",
            "on_1863_list": "yes" if n in old.get("1863", set()) else "no",
            "on_1868_list": "yes" if n in old.get("1868", set()) else "no",
        })
    out = base / "unsolved_1842_1910.tsv"
    out.write_text("\t".join(COLS) + "\n" + "\n".join("\t".join(str(r[c]) for c in COLS) for r in rows) + "\n", encoding="utf-8")
    (base / "questions.json").write_text(json.dumps(statements, ensure_ascii=False, indent=1), encoding="utf-8")
    n_state = sum(1 for r in rows if r["statement_fr"])
    print(f"1915 list: {len(master)} numbers ({len(set(master))} distinct); 1863 list: {len(old.get('1863', []))}; 1868 list: {len(old.get('1868', []))}")
    print(f"statements merged: {len(statements) - (1 if '?' in statements else 0)} numbered, {len(statements.get('?', []))} unnumbered fragments")
    print(f"rows: {len(rows)}; with statement: {n_state}; on 1915 list without statement: {sum(1 for r in rows if r['on_1915_list']=='yes' and not r['statement_fr'])}; "
          f"statement but not on 1915 list: {sum(1 for r in rows if r['on_1915_list']=='no')}")
    from collections import Counter
    print(f"31 Dec 1917 list: {len(still_1917)} numbers; not on the 1915 list: {sorted(still_1917 - set(master), key=key)}; "
          f"with statement: {sum(1 for n in still_1917 if statements.get(n))}")
    print("status counts:", dict(Counter(r["status"] for r in rows)))
    print("wrote", out)


if __name__ == "__main__":
    main()
