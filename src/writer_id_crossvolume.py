#!/usr/bin/env python3
"""Leave-one-volume-out check for src/writer_id.py (no network; reuses its descriptor cache).

Question: does the classifier call the target pages "Riemann" only because Riemann training pages
come from the same two volumes (same paper, same scanning campaign)?

Run A: the Riemann class is trained on Cod. Ms. B. Riemann 19 pages only; every Riemann page of
       Cod. Ms. 26 is held out and scored, together with the six target pages.
Run B: the same with the volumes swapped.
The other writers' training pages are unchanged. Both encodings of writer_id.py are run.

Use (after `writer_id.py run` has filled W/results/desc_cache):
  python3 -E -P src/writer_id_crossvolume.py --pages W/pages.tsv --images W/images --cache W/results/desc_cache
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import writer_id as W  # noqa: E402


def main():
    import numpy as np
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--pages", required=True)
    p.add_argument("--images", required=True)
    p.add_argument("--cache", required=True, help="descriptor cache dir written by writer_id.py run")
    p.add_argument("--seed", type=int, default=0)
    a = p.parse_args()

    rows = W.read_pages(a.pages)
    feats = W.load_all_descriptors(rows, a.images, a.cache, 4000, a.seed)
    usable = lambda r: r["file"] in feats and len(feats[r["file"]][0]) >= 150
    train_all = [r for r in rows if r["role"] == "train" and usable(r)]
    targets = [r for r in rows if r["role"] == "target" and usable(r)]

    def run(name, keep_hs, kind, k):
        tr = [r for r in train_all if r["writer"] != "Riemann" or r["hs"] == keep_hs]
        held = [r for r in train_all if r["writer"] == "Riemann" and r["hs"] != keep_hs]
        km = W.fit_codebook([feats[r["file"]][0] for r in tr], k, a.seed)
        X, y = [], []
        for r in tr:
            d, yy, _ = feats[r["file"]]
            for _, dd in W.page_samples(d, yy, 4):
                X.append(W.encode(dd, km, kind))
                y.append(r["writer"])
        clf = W.fit_classifier(np.array(X), np.array(y), a.seed)

        def score(r):
            d, yy, _ = feats[r["file"]]
            S = [W.encode(dd, km, kind) for _, dd in W.page_samples(d, yy, 4)]
            return dict(zip(clf.classes_, clf.predict_proba(np.array(S)).mean(0)))

        res = [(r, score(r)) for r in held]
        n_ok = sum(max(pr, key=pr.get) == "Riemann" for _, pr in res)
        n_r = sum(r["writer"] == "Riemann" for r in tr)
        print("\n[run %s | %s k=%d] Riemann class trained on %s only (%d pages); held-out Riemann pages of the other "
              "volume classified Riemann: %d/%d" % (name, kind, k, keep_hs, n_r, n_ok, len(res)))
        for r, pr in res:
            top = max(pr, key=pr.get)
            if top != "Riemann":
                print("   miss: %s %5s -> %s %.2f (Riemann %.2f)" % (r["hs"], r["label"], top, pr[top], pr["Riemann"]))
        for t in targets:
            pr = score(t)
            top = max(pr, key=pr.get)
            nxt = sorted(pr.items(), key=lambda kv: -kv[1])[1]
            print("   %s %s %5s: %s %.3f | P(Riemann) %.3f | next %s %.3f"
                  % (t["writer"], t["hs"], t["label"], top, pr[top], pr["Riemann"], nxt[0], nxt[1]))

    for kind, k in (("hist", 200), ("vlad", 64)):
        run("A", W.HS_B19, kind, k)
        run("B", W.HS_B26, kind, k)


if __name__ == "__main__":
    main()
