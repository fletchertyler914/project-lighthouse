#!/usr/bin/env python3
"""
repair_json.py - repair read_source.py JSON outputs whose model text failed to parse (usually invalid
backslash escapes such as "\\mathbb" inside JSON strings). Re-parses the stored raw text; if that
succeeds the record is rewritten as parsed. Unrepairable DEEP files are deleted so the next run redoes them.
Pure data processing; run with python3 -I.

    python3 -I src/repair_json.py [base_dir] [--delete]   (default base: data/grothendieck-montpellier;
    --delete removes unrepairable DEEP files so the next deep run redoes them; without it they are only listed)
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from jsonfix import lenient_json  # noqa: E402

BASE = pathlib.Path(__file__).resolve().parent.parent / "data" / "grothendieck-montpellier"


def main():
    global BASE
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    delete = "--delete" in sys.argv
    if args:
        BASE = pathlib.Path(args[0])
    fixed = unfixed = 0
    for f in sorted(BASE.glob("transcripts/*/*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        if rec.get("parsed"):
            continue
        data = lenient_json(rec["result"].get("raw", ""))
        if data is None:
            unfixed += 1
            print("UNFIXED transcript", f)
            continue
        rec["parsed"] = True
        rec["result"] = data
        f.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        fixed += 1
        print("fixed transcript", f)
    for f in sorted(BASE.glob("deep/*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        if "raw" not in rec["deep"]:
            continue
        data = lenient_json(rec["deep"]["raw"])
        if data is None:
            if delete:
                print("DELETE unrepairable deep", f)
                f.unlink()
            else:
                print("UNREPAIRABLE deep (kept; use --delete to remove)", f)
            unfixed += 1
            continue
        rec["deep"] = data
        f.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        fixed += 1
        print("fixed deep", f)
    print(f"REPAIR DONE fixed={fixed} unfixed/deleted={unfixed}")


if __name__ == "__main__":
    main()
