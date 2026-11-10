#!/usr/bin/env python3
"""
validate.py - check a contribution before opening a PR, and show what is left to do.

    python3 -I src/validate.py data/<author>            # validates transcripts/, reports failed deep reads
    python3 -I src/validate.py data/<author> --status    # also rewrites data/<author>/STATUS.tsv

A transcript page JSON only needs these fields to be usable by everyone else's deep readers:
    image          URL of the page scan (IIIF or library URL; never a copied file)
    label          folio/page label as the library gives it, e.g. "70r" or "p011"
    parsed         true
    result.transcription   the text (original language; LaTeX in $...$; struck text [-...-])
    source         who/what made it: "human", or a model id, or "model:<id>+human"
Everything else in data/FORMAT.md is optional. Pure data processing; run with python3 -I.
"""
import json
import pathlib
import sys

REQUIRED = ("image", "label", "parsed")


def check_page(f):
    try:
        rec = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return f"{f}: not valid JSON ({e})"
    pdf_style = "cote" in rec and "page" in rec  # read_source.py pages: scan PDF + page number, no image URL
    missing = [] if pdf_style else [k for k in REQUIRED if k not in rec]
    if not rec.get("parsed") or rec.get("parsed") == "False":
        return "UNPARSED"  # model output never parsed: run src/repair_json.py, else re-transcribe
    if not isinstance(rec.get("result"), dict) or "transcription" not in rec["result"]:
        missing.append("result.transcription")
    if "source" not in rec and "model" not in rec and not pdf_style:
        missing.append("source (or model)")
    if missing:
        return f"{f}: missing {', '.join(missing)}"
    if not pdf_style and not str(rec["image"]).startswith(("http://", "https://")):
        return f"{f}: image must be a URL, not a local file"
    return None


def check_deep(f):
    try:
        rec = json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return f"could not read JSON ({e})"
    deep = rec.get("deep") if isinstance(rec, dict) else None
    if isinstance(deep, dict) and "raw" in deep:
        return "unparsed model output (run src/repair_json.py for this author)"
    if not isinstance(deep, dict) or not isinstance(deep.get("reconstruction"), str):
        return "missing deep.reconstruction text"
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    root = pathlib.Path(sys.argv[1])
    tdir, ddir = root / "transcripts", root / "deep"
    if not tdir.is_dir():
        print(f"no {tdir}")
        sys.exit(1)
    deep = set()
    for f in sorted(ddir.glob("*.json")):
        msg = check_deep(f)
        if msg:
            print(f"WARN {f}: {msg}")
        else:
            deep.add(f.stem)
    trdir = root / "translations"
    rows, bad = [], 0
    for b in sorted(p for p in tdir.iterdir() if p.is_dir()):
        pages = sorted(b.glob("*.json"))
        n_bad = n_unp = 0
        for f in pages:
            msg = check_page(f)
            if msg == "UNPARSED":
                n_unp += 1
            elif msg:
                print("BAD", msg)
                n_bad += 1
        if n_unp:
            print(f"WARN {b.name}: {n_unp} unparsed page(s) (run src/repair_json.py {root}, or re-transcribe)")
        bad += n_bad
        n_deep = sum(1 for f in pages if f"{b.name}_{f.stem}" in deep)
        n_tr = len(list((trdir / b.name).glob("*.md"))) if (trdir / b.name).is_dir() else 0
        rows.append((b.name, len(pages), n_deep, n_bad, n_unp, n_tr))
    print(f"\n{'bundle':28} {'pages':>6} {'deep':>6} {'bad':>4} {'unparsed':>8} {'transl':>6}")
    for name, n, d, nb, nu, nt in rows:
        print(f"{name:28} {n:6} {d:6} {nb:4} {nu:8} {nt:6}")
    tot = sum(r[1] for r in rows)
    totd = sum(r[2] for r in rows)
    totu = sum(r[4] for r in rows)
    tott = sum(r[5] for r in rows)
    print(f"{'TOTAL':28} {tot:6} {totd:6} {bad:4} {totu:8} {tott:6}")
    if "--status" in sys.argv:
        out = root / "STATUS.tsv"
        lines = ["bundle\tpages_transcribed\tpages_deep_read\tunparsed\ttranslated\tlabel"]
        for name, n, d, nb, nu, nt in rows:
            label = "read" if d >= n * 0.9 else ("partly-read" if d else "transcribed")
            lines.append(f"{name}\t{n}\t{d}\t{nu}\t{nt}\t{label}")
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("wrote", out)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
