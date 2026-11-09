#!/usr/bin/env python3
"""
nam_report.py - render the machine-generated parts of docs/NOUVELLES_ANNALES_UNSOLVED.md (counts by status, the full
table of "still apparently open" items, the interest ranking) from the TSV, status.json and evidence/judge/.
The narrative sections (method, limitations, commentary on the top items) live in the template text below and are
edited by hand. Pure data processing: python3 -I src/nam_report.py
"""
import csv
import json
import pathlib
import re
from collections import Counter

HUNT = pathlib.Path(__file__).resolve().parent.parent
BASE = HUNT / "data" / "nouvelles-annales"
DOC = HUNT / "docs" / "NOUVELLES_ANNALES_UNSOLVED.md"
csv.field_size_limit(10 ** 7)


def key(n):
    m = re.match(r"(\d+)(?: (bis|ter))?", n)
    return (int(m.group(1)), m.group(2) or "") if m else (10 ** 9, n)


def md(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def short(s, n=400):
    s = md(s)
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + " [...]"


def main():
    rows = list(csv.DictReader(open(BASE / "unsolved_1842_1910.tsv", encoding="utf-8"), delimiter="\t"))
    status = json.loads((BASE / "status.json").read_text(encoding="utf-8")) if (BASE / "status.json").exists() else {}
    on15 = [r for r in rows if r["on_1915_list"] == "yes"]
    on17 = [r for r in rows if r["on_1917_list"] == "yes"]
    extras = [r for r in rows if r["on_1915_list"] == "no"]

    def bucket(s):
        s = s.lower()
        for k in ("solved here", "solved since", "still apparently open", "ill-posed", "unclear", "number only", "unchecked"):
            if s.startswith(k):
                return k
        return "other"

    counts = Counter(bucket(r["status"]) for r in rows)
    counts17 = Counter(bucket(r["status"]) for r in on17)
    fields = Counter(r["field"] or "(no statement)" for r in on17)

    out = []
    out.append("<!-- generated tables: python3 -I src/nam_report.py ; narrative sections are hand-written -->")
    out.append(f"## Counts\n")
    out.append(f"- Numbers on the June 1915 list (NAM (4) 15, p. 246): **{len(on15)}** (255 printed entries, 4 of them *bis*).")
    out.append(f"- Of these, reprinted with a full statement in 1916-18: **{sum(1 for r in on15 if r['statement_fr'])}**; number only: "
               f"**{sum(1 for r in on15 if not r['statement_fr'])}** (all of the latter are absent from the 31 Dec 1917 list, i.e. they were "
               f"disposed of before their turn came in the reprinting).")
    out.append(f"- Still on the editors' own list of 31 Dec 1917 (NAM (4) 18, 1918, p. 40): **{len(on17)}** (the editors: \"116 questions seulement restent sans solutions\").")
    out.append(f"- Statements reprinted although not on the 1915 list: {', '.join(r['question_number'] for r in extras)} "
               f"(423, 858 and 2064 are printed only as context for 424, 859 and 2065 and are footnoted as solved; 1433 was added by the editors in 1916).\n")
    out.append("Status of all table rows (" + str(len(rows)) + "):\n")
    out.append("| status | rows | of which on the 31 Dec 1917 list |\n|---|---:|---:|")
    for k, v in counts.most_common():
        out.append(f"| {k} | {v} | {counts17.get(k, 0)} |")
    out.append("\nFields of the 116 questions still open at the end of 1917 (model classification, see limitations):\n")
    out.append("| field | n |\n|---|---:|")
    for k, v in fields.most_common():
        out.append(f"| {k} | {v} |")

    still = [r for r in rows if bucket(r["status"]) == "still apparently open"]
    still.sort(key=lambda r: key(r["question_number"]))
    out.append(f"\n## Table: \"still apparently open\" ({len(still)} items)\n")
    out.append("Statement in English (model translation of the verbatim French in the TSV); evidence column lists the searches run.\n")
    out.append("| no. | year | proposer | field | statement (EN) | evidence |\n|---|---|---|---|---|---|")
    for r in still:
        out.append(f"| {r['question_number']} | {r['year_posed']} | {md(r['author'])} | {r['field']} | {short(r['statement_en'], 700)} | {short(r['status_evidence'], 600)} |")

    # interest ranking from the judge records
    ranked = []
    for r in rows:
        st = status.get(r["question_number"], {})
        if bucket(r["status"]) in ("still apparently open", "unclear") and st.get("interest") is not None:
            ranked.append((st["interest"], r, st))
    ranked.sort(key=lambda t: (-t[0], key(t[1]["question_number"])))
    out.append(f"\n## Interest ranking of the open/unclear items (model score 0-10, to be read as a triage aid only)\n")
    out.append("| no. | year | proposer | score | status | why |\n|---|---|---|---:|---|---|")
    for sc, r, st in ranked[:25]:
        out.append(f"| {r['question_number']} | {r['year_posed']} | {md(r['author'])} | {sc} | {bucket(r['status'])} | {short(st.get('interest_reason', ''), 300)} |")

    solved_here = [r for r in rows if bucket(r["status"]) == "solved here"]
    out.append(f"\n## \"Solved here\" ({len(solved_here)} items)\n")
    for r in solved_here:
        out.append(f"- **{r['question_number']}** ({r['year_posed']}, {md(r['author'])}): {short(r['statement_en'], 500)}\n  - {short(r['status_evidence'], 900)}")

    solved_lit = [r for r in rows if bucket(r["status"]) == "solved since" and r["on_1917_list"] == "yes"]
    out.append(f"\n## \"Solved since\" among the 116 still open at the end of 1917 ({len(solved_lit)} items)\n")
    out.append("| no. | year | proposer | status | evidence |\n|---|---|---|---|---|")
    for r in solved_lit:
        out.append(f"| {r['question_number']} | {r['year_posed']} | {md(r['author'])} | {md(r['status'])} | {short(r['status_evidence'], 500)} |")

    others = [r for r in rows if bucket(r["status"]) in ("ill-posed", "unclear") and r["statement_fr"]]
    out.append(f"\n## \"Ill-posed/false as stated\" and \"unclear\" ({len(others)} items)\n")
    out.append("| no. | year | proposer | status | evidence |\n|---|---|---|---|---|")
    for r in others:
        out.append(f"| {r['question_number']} | {r['year_posed']} | {md(r['author'])} | {md(r['status'])} | {short(r['status_evidence'], 500)} |")

    gen = "\n".join(out) + "\n"
    if DOC.exists():
        txt = DOC.read_text(encoding="utf-8")
        a, b = "<!-- BEGIN GENERATED -->", "<!-- END GENERATED -->"
        if a in txt and b in txt:
            txt = txt[:txt.index(a) + len(a)] + "\n" + gen + txt[txt.index(b):]
            DOC.write_text(txt, encoding="utf-8")
            print("updated generated section of", DOC)
            return
    (BASE / "report_generated.md").write_text(gen, encoding="utf-8")
    print("wrote", BASE / "report_generated.md", "(no BEGIN/END GENERATED markers in the doc yet)")


if __name__ == "__main__":
    main()
