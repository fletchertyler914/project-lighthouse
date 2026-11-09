#!/usr/bin/env python3
"""Handwriting writer identification for the Riemann Nachlass (SUB Göttingen, IIIF).

Classical, reproducible pipeline: Sauvola binarisation -> SIFT descriptors at ink
keypoints -> k-means codebook (training pages only) -> bag-of-visual-words / VLAD
page encoding -> logistic regression (+ cosine nearest-neighbour baseline).

Subcommands
  list   build the page table (TSV) from the IIIF manifests and local transcript JSONs
  fetch  download the listed page images (polite: <= 2 requests/s, research User-Agent)
  run    extract features, evaluate with grouped cross-validation, score the target pages

Typical use
  python3 -E -P src/writer_id.py list  --manifests DIR --data data --out W/pages.tsv
  python3 -E -P src/writer_id.py fetch --pages W/pages.tsv --images W/images
  python3 -E -P src/writer_id.py run   --pages W/pages.tsv --images W/images --out W/results

Only public-domain scans are read; nothing is copied into the repository. Images are
treated as data (never executed). No personal data is produced.
"""
import argparse
import csv
import glob
import json
import os
import re
import sys
import time

IIIF = "https://images.sub.uni-goettingen.de/iiif/image/gdz:{hs}:{canvas:08d}/full/1300,/0/default.jpg"
UA = "hunt-research-bot (academic research)"
HS_B19 = "DE-611-HS-3206670"   # Cod. Ms. B. Riemann 19 (Abelsche Functionen / Theta-Functionen)
HS_B26 = "DE-611-HS-3206190"   # Cod. Ms. B. Riemann 26 (Mathematische Notizen)
# local transcript bundles for the two Riemann volumes (canvas field there is 0-based)
BUNDLE = {HS_B19: "R.AbelTheta", HS_B26: "R.MathNotizen1853"}

TARGETS = [  # (id, HS, folio label, canvas 1-based, note)
    ("T1", HS_B26, "70v", 142, "question page"),
    ("T2", HS_B26, "71r", 143, "question page"),
    ("T3", HS_B26, "228r", 447, "question page"),
    ("T4", HS_B19, "3v", 8, "question page"),
    ("T5", HS_B19, "97r", 197, "control: printed by Noether 1902 as Riemann's"),
    ("T6", HS_B19, "101r", 205, "control: catalogue says Weierstrass; held out of training"),
]
# folios never used for training (targets + reserved neighbours)
EXCLUDE = {HS_B26: {"70r", "70v", "71r", "71v", "228r"}, HS_B19: {"3r", "3v", "97r", "97v", "101r"}}


def folio_num(label):
    m = re.match(r"^(\d+)([rv])$", label or "")
    return (int(m.group(1)), m.group(2)) if m else None


# ----------------------------------------------------------------------------- list
def load_manifest_labels(path):
    m = json.load(open(path, encoding="utf-8"))
    return [c["label"] for c in m["sequences"][0]["canvases"]]


def load_transcripts(data_dir, author, bundles):
    """-> {(bundle, canvas_1based): record} with legibility, text stats, image url."""
    out = {}
    for b in bundles:
        for f in sorted(glob.glob(os.path.join(data_dir, author, "transcripts", b, "c*.json"))):
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            r = d.get("result") or {}
            tr = r.get("transcription") or ""
            topic = (r.get("topic_en") or "").lower()
            blob = json.dumps(r, ensure_ascii=False).lower()
            n_dollar = tr.count("$")
            words = len(re.findall(r"[A-Za-zäöüßÄÖÜ]{3,}", re.sub(r"\$[^$]*\$", "", tr)))
            # prose: a letter/prose page by topic, or almost no formulas but plenty of words
            prose = ("letter" in topic or "prose" in topic) or (len(tr) > 0 and n_dollar / max(len(tr), 1) < 0.01 and words > 80)
            out[(b, int(d.get("canvas", -2)) + 1)] = dict(
                label=d.get("label"), legibility=r.get("legibility"), text_len=len(tr),
                pencil_mention="yes" if "pencil" in blob else "no",
                content="prose" if prose else "maths", image=d.get("image"))
    return out


def select_riemann(labels, tr, hs, ranges, step, exclude, skip_labels=()):
    """Deterministic pick: non-blank pages in the folio ranges, every `step`-th canvas."""
    rows, k = [], 0
    for i, lab in enumerate(labels):
        canvas = i + 1
        fn = folio_num(lab)
        if not fn or lab in exclude or lab in skip_labels:
            continue
        if not any(a <= fn[0] <= z for a, z in ranges):
            continue
        rec = tr.get((BUNDLE[hs], canvas), {})
        if rec.get("legibility") in (None, "blank") or rec.get("text_len", 0) < 200:
            continue
        k += 1
        if (k - 1) % step:
            continue
        rows.append(dict(writer="Riemann", hs=hs, canvas=canvas, label=lab, role="train",
                         pencil_mention=rec.get("pencil_mention", "na"), content=rec.get("content", "na"),
                         url=IIIF.format(hs=hs, canvas=canvas)))
    return rows


def select_catalogue_hand(labels, hs, writer, first, last):
    rows = []
    for i, lab in enumerate(labels):
        fn = folio_num(lab)
        if fn and first <= fn[0] <= last and lab not in EXCLUDE.get(hs, ()):
            rows.append(dict(writer=writer, hs=hs, canvas=i + 1, label=lab, role="train",
                             pencil_mention="na", content="maths", url=IIIF.format(hs=hs, canvas=i + 1)))
    return rows


# pages inside the comparison bundles that are not (only) in the catalogued writer's hand; found by
# looking at the scans and the transcript topics. (bundle, folio label): reason
NOT_WRITERS_HAND = {
    ("D.Bemerkungen", "2r"): "printed library loan receipt, 1880 (only the signature is Dedekind's)",
    ("D.Bemerkungen", "4r"): "printed-form note from a bookseller to Dedekind",
    ("D.RationaleZahlen", "2r"): "reused court-judgment sheet; most ink is the court clerk's",
    ("D.RationaleZahlen", "9v"): "court judgment, not Dedekind's hand",
    ("D.Bemerkungen", "6r"): "printed title page of Dedekind's 1878 offprint",
    ("D.RationaleZahlen", "3v"): "reused printed publisher's order form",
    ("D.RationaleZahlen", "5v/6r"): "calculations on a reused printed subscription form",
    ("Math.21", "47v"): "German legal pleading dated 1894 (Gauss died 1855)",
    ("Math.21", "15v"): "rotated sheet mixing number tables with English writing exercises",
    ("Math.21", "25r"): "rotated sheet of calligraphy practice (names, capitals)",
    ("Math.21", "47br"): "geometric diagrams on a dot grid, almost no handwriting",
}


def select_other(data_dir, author, writer, bundles, n_total):
    """Evenly spaced non-blank, foliated pages with >=300 chars of transcription."""
    recs = []
    for b in bundles:
        for key, r in sorted(load_transcripts(data_dir, author, [b]).items()):
            if r["legibility"] in (None, "blank") or not r["image"] or r["text_len"] < 300:
                continue
            if r["label"] in (None, "", "-") or (b, r["label"]) in NOT_WRITERS_HAND:
                continue
            recs.append((b, key[1], r))
    rows = []
    for j in range(n_total):
        b, canvas1, r = recs[int(j * len(recs) / n_total)]
        m = re.search(r"gdz:([^:/]+):(\d{8})", r["image"])
        rows.append(dict(writer=writer, hs=m.group(1), canvas=int(m.group(2)), label=r["label"], role="train",
                         pencil_mention="na", content=r["content"], url=r["image"], bundle=b))
    return rows


def cmd_list(a):
    lab19 = load_manifest_labels(os.path.join(a.manifests, HS_B19 + ".json"))
    lab26 = load_manifest_labels(os.path.join(a.manifests, HS_B26 + ".json"))
    tr = load_transcripts(a.data, "riemann", [BUNDLE[HS_B19], BUNDLE[HS_B26]])
    rows = []
    # Riemann: theta notes 85r-96v (all non-blank), 1857 drafts 121r-194v (every 5th; 121r is a cover sheet),
    # B.26: four dated letter pages + notes 1r-60r (every 5th)
    rows += select_riemann(lab19, tr, HS_B19, [(85, 96)], 1, EXCLUDE[HS_B19])
    rows += select_riemann(lab19, tr, HS_B19, [(121, 194)], 5, EXCLUDE[HS_B19], skip_labels=("121r",))
    for lab in ("183v", "100r", "122r", "146v"):   # dated/signed letter pages, Riemann
        canvas = lab26.index(lab) + 1
        rec = tr.get((BUNDLE[HS_B26], canvas), {})
        rows.append(dict(writer="Riemann", hs=HS_B26, canvas=canvas, label=lab, role="train",
                         pencil_mention=rec.get("pencil_mention", "na"), content=rec.get("content", "na"),
                         url=IIIF.format(hs=HS_B26, canvas=canvas)))
    rows += select_riemann(lab26, tr, HS_B26, [(1, 60)], 5, EXCLUDE[HS_B26])
    # Weierstrass: the catalogue range is 100r-105v, but on inspection 100r is a 1920 archival note in
    # ink ("... Blätter ... von Weierstrass ... 29.9.20") over faint pencil, 100v/102r/102v/105r/105v are
    # blank, and 101r/101v (one leaf) is the held-out control. Only the two leaves 103-104 carry clear
    # writing in the Weierstrass hand, so training uses exactly those four pages.
    rows += select_catalogue_hand(lab19, HS_B19, "Weierstrass", 103, 104)
    rows += select_catalogue_hand(lab19, HS_B19, "Weber", 115, 120)
    rows += select_other(a.data, "dedekind", "Dedekind", sorted(os.listdir(os.path.join(a.data, "dedekind", "transcripts"))), 30)
    rows += select_other(a.data, "hilbert", "Hilbert", ["600_1", "600_2", "600_3"], 30)
    rows += select_other(a.data, "gauss", "Gauss", ["Math.21", "HB.Opuscula1800"], 30)
    for tid, hs, lab, canvas, note in TARGETS:
        rec = tr.get((BUNDLE[hs], canvas), {})
        rows.append(dict(writer=tid, hs=hs, canvas=canvas, label=lab, role="target", pencil_mention=rec.get("pencil_mention", "na"),
                         content=rec.get("content", "na"), url=IIIF.format(hs=hs, canvas=canvas), note=note))
    seen = set()
    for r in rows:
        key = (r["hs"], r["canvas"])
        assert key not in seen, key
        seen.add(key)
        r["file"] = "%s_%08d.jpg" % (r["hs"], r["canvas"])
    cols = ["writer", "role", "hs", "canvas", "label", "pencil_mention", "content", "file", "url", "note", "bundle"]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    from collections import Counter
    print("pages:", len(rows), dict(Counter(r["writer"] for r in rows)))


# ----------------------------------------------------------------------------- fetch
def read_pages(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def cmd_fetch(a):
    import urllib.request
    os.makedirs(a.images, exist_ok=True)
    rows = read_pages(a.pages)
    todo = [r for r in rows if not os.path.exists(os.path.join(a.images, r["file"]))]
    print("to download:", len(todo), "of", len(rows))
    for i, r in enumerate(todo):
        dst = os.path.join(a.images, r["file"])
        req = urllib.request.Request(r["url"], headers={"User-Agent": UA})
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            if not data.startswith(b"\xff\xd8"):
                print("not a JPEG:", r["url"])
                continue
            with open(dst + ".part", "wb") as fh:
                fh.write(data)
            os.replace(dst + ".part", dst)
        except Exception as e:  # keep going; the run step reports missing files
            print("failed:", r["url"], e)
        time.sleep(max(0.0, a.interval - (time.time() - t0)))
        if (i + 1) % 25 == 0:
            print("downloaded", i + 1, flush=True)
    print("done")


# ----------------------------------------------------------------------------- run
def preprocess(path, margin=0.06, win=31, k_sauvola=0.2, min_contrast=12):
    """-> (flattened grayscale uint8, ink mask bool, stats dict)."""
    import cv2
    import numpy as np
    g = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if g is None:
        raise RuntimeError("cannot read " + path)
    H, W = g.shape
    g = g[int(H * margin):int(H * (1 - margin)), int(W * margin):int(W * (1 - margin))]
    g = cv2.medianBlur(g, 3)
    # flatten illumination: divide by a smooth background estimate (closing removes the ink)
    bg = cv2.morphologyEx(g, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
    bg = cv2.GaussianBlur(bg, (0, 0), 15).astype(np.float32)
    norm = np.clip(g.astype(np.float32) / np.maximum(bg, 1) * 255.0, 0, 255)
    # Sauvola threshold on the flattened image
    mean = cv2.boxFilter(norm, -1, (win, win), normalize=True)
    sq = cv2.boxFilter(norm * norm, -1, (win, win), normalize=True)
    std = np.sqrt(np.maximum(sq - mean * mean, 0))
    thr = mean * (1 + k_sauvola * (std / 128.0 - 1))
    fg = (norm < thr) & (norm < mean - min_contrast)
    # drop specks and very large blobs (stains, page edges, margin shadows)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), connectivity=8)
    area = st[:, cv2.CC_STAT_AREA]
    keep = (area >= 8) & (area <= 0.02 * fg.size) & (st[:, cv2.CC_STAT_HEIGHT] < 0.25 * fg.shape[0]) & (st[:, cv2.CC_STAT_WIDTH] < 0.25 * fg.shape[1])
    keep[0] = False
    fg = keep[lab]
    dark = (255.0 - norm[fg]) / 255.0 if fg.any() else np.zeros(1)
    stats = dict(ink_pixels=int(fg.sum()), ink_fraction=float(fg.mean()),
                 darkness_median=float(np.median(dark)), darkness_p90=float(np.percentile(dark, 90)))
    return norm.astype(np.uint8), fg, stats


def page_descriptors(path, max_desc, seed):
    """RootSIFT descriptors at SIFT keypoints restricted to the ink mask. -> (desc float32 [n,128], y [n], stats)"""
    import cv2
    import numpy as np
    norm, fg, stats = preprocess(path)
    if fg.sum() < 500:
        return np.zeros((0, 128), np.float32), np.zeros(0, np.float32), stats
    # per-page contrast stretch so pencil and ink pages look alike to the detector
    lo = np.percentile(norm[fg], 5)
    img = np.clip((norm.astype(np.float32) - lo) / max(255.0 - lo, 1) * 255.0, 0, 255).astype(np.uint8)
    mask = cv2.dilate(fg.astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
    sift = cv2.SIFT_create(contrastThreshold=0.02, edgeThreshold=12)
    kps = sift.detect(img, mask)
    kps = [k for k in kps if 2.0 <= k.size <= 48.0]
    kps.sort(key=lambda k: -k.response)
    kps = kps[:max_desc]
    kps, desc = sift.compute(img, kps)
    if desc is None or len(kps) == 0:
        return np.zeros((0, 128), np.float32), np.zeros(0, np.float32), stats
    desc = desc.astype(np.float32)
    desc = np.sqrt(desc / np.maximum(desc.sum(1, keepdims=True), 1e-9))   # RootSIFT
    y = np.array([k.pt[1] for k in kps], np.float32) / img.shape[0]
    stats["n_desc"] = int(len(desc))
    return desc, y, stats


def load_all_descriptors(rows, images, cache_dir, max_desc, seed):
    import numpy as np
    os.makedirs(cache_dir, exist_ok=True)
    out = {}
    for i, r in enumerate(rows):
        src = os.path.join(images, r["file"])
        cp = os.path.join(cache_dir, r["file"] + ".npz")
        if os.path.exists(cp):
            z = np.load(cp)
            out[r["file"]] = (z["desc"], z["y"], json.loads(str(z["stats"])))
            continue
        if not os.path.exists(src):
            print("missing image:", src)
            continue
        desc, y, stats = page_descriptors(src, max_desc, seed)
        np.savez_compressed(cp + ".tmp.npz", desc=desc, y=y, stats=json.dumps(stats))
        os.replace(cp + ".tmp.npz", cp)   # atomic, so parallel runs can share the cache
        out[r["file"]] = (desc, y, stats)
        if (i + 1) % 20 == 0:
            print("features", i + 1, "/", len(rows), flush=True)
    return out


def fit_codebook(desc_list, k, seed, per_page=1200):
    import numpy as np
    from sklearn.cluster import MiniBatchKMeans
    rng = np.random.RandomState(seed)
    parts = []
    for d in desc_list:
        if len(d) > per_page:
            d = d[rng.choice(len(d), per_page, replace=False)]
        parts.append(d)
    X = np.vstack(parts)
    km = MiniBatchKMeans(n_clusters=k, random_state=seed, batch_size=4096, n_init=3, max_iter=200)
    km.fit(X)
    return km


def encode(desc, km, kind):
    import numpy as np
    k = km.n_clusters
    if len(desc) == 0:
        return np.zeros(k if kind == "hist" else k * 128, np.float32)
    lab = km.predict(desc)
    if kind == "hist":
        h = np.bincount(lab, minlength=k).astype(np.float32)
        h /= max(h.sum(), 1)
        h = np.sqrt(h)
        return h / max(np.linalg.norm(h), 1e-9)
    v = np.zeros((k, desc.shape[1]), np.float32)
    for c in range(k):
        sel = lab == c
        if sel.any():
            v[c] = (desc[sel] - km.cluster_centers_[c]).sum(0)
    v /= np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-9)   # intra-normalisation
    v = v.ravel()
    v = np.sign(v) * np.sqrt(np.abs(v))
    return v / max(np.linalg.norm(v), 1e-9)


def page_samples(desc, y, strips, min_desc=150):
    """Full page + horizontal strips (split by descriptor count) as separate samples."""
    import numpy as np
    out = [("full", desc)]
    if strips > 1 and len(desc) >= strips * min_desc:
        order = np.argsort(y)
        for part in np.array_split(order, strips):
            out.append(("strip", desc[part]))
    return out


def fit_classifier(X, y, seed):
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=5000, class_weight="balanced", random_state=seed))
    clf.fit(X, y)
    return clf


def evaluate(train, feats, a, writers):
    """Grouped 5-fold CV (codebook refit per fold). -> per-page predictions."""
    import numpy as np
    from sklearn.model_selection import StratifiedGroupKFold
    pages = [r for r in train if r["file"] in feats and len(feats[r["file"]][0]) >= 150]
    y = np.array([r["writer"] for r in pages])
    groups = np.arange(len(pages))
    skf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=a.seed)
    pred = {}
    for fold, (tr_idx, te_idx) in enumerate(skf.split(np.zeros(len(pages)), y, groups)):
        km = fit_codebook([feats[pages[i]["file"]][0] for i in tr_idx], a.k, a.seed)
        Xtr, ytr, full_tr = [], [], []
        for i in tr_idx:
            d, yy, _ = feats[pages[i]["file"]]
            for kind, dd in page_samples(d, yy, a.strips):
                e = encode(dd, km, a.encoding)
                Xtr.append(e)
                ytr.append(pages[i]["writer"])
                if kind == "full":
                    full_tr.append((e, i))
        clf = fit_classifier(np.array(Xtr), np.array(ytr), a.seed)
        Ftr = np.array([e for e, _ in full_tr])
        for i in te_idx:
            d, yy, _ = feats[pages[i]["file"]]
            samples = [encode(dd, km, a.encoding) for _, dd in page_samples(d, yy, a.strips)]
            P = clf.predict_proba(np.array(samples)).mean(0)
            sims = Ftr @ samples[0]
            j = int(np.argmax(sims))
            nn = pages[full_tr[j][1]]
            pred[pages[i]["file"]] = dict(
                prob={c: float(p) for c, p in zip(clf.classes_, P)}, pred=str(clf.classes_[int(np.argmax(P))]),
                nn_writer=nn["writer"], nn_page="%s %s" % (nn["hs"], nn["label"]), nn_sim=float(sims[j]), fold=fold)
        print("fold", fold, "done", flush=True)
    return pages, pred


def confusion(pages, pred, writers):
    cm = {w: {v: 0 for v in writers} for w in writers}
    for r in pages:
        cm[r["writer"]][pred[r["file"]]["pred"]] += 1
    return cm


def subset_acc(pages, pred, cond):
    sel = [r for r in pages if cond(r)]
    ok = sum(pred[r["file"]]["pred"] == r["writer"] for r in sel)
    return dict(n=len(sel), correct=ok, acc=(ok / len(sel) if sel else None))


def cmd_run(a):
    import numpy as np
    os.makedirs(a.out, exist_ok=True)
    rows = read_pages(a.pages)
    feats = load_all_descriptors(rows, a.images, os.path.join(a.out, "desc_cache"), a.max_desc, a.seed)
    writers = ["Riemann", "Weierstrass", "Weber", "Dedekind", "Hilbert", "Gauss"]
    train = [r for r in rows if r["role"] == "train"]
    targets = [r for r in rows if r["role"] == "target"]
    # medium: "pencil" if the page transcript explicitly mentions pencil, else "ink/unspecified". An image
    # darkness statistic was tried and rejected: scan exposure and ink fading vary more than the
    # pencil/ink difference (known-ink Weber pages measure like faint Riemann pages). It is still recorded.
    for r in rows:
        st = feats.get(r["file"], (None, None, {}))[2]
        r["darkness"] = st.get("darkness_median")
        r["n_desc"] = st.get("n_desc", 0)
        r["medium"] = "pencil" if r.get("pencil_mention") == "yes" else "ink/unspecified"

    pages, pred = evaluate(train, feats, a, writers)
    acc = sum(pred[r["file"]]["pred"] == r["writer"] for r in pages) / len(pages)
    nn_acc = sum(pred[r["file"]]["nn_writer"] == r["writer"] for r in pages) / len(pages)
    bin_ok = sum((pred[r["file"]]["pred"] == "Riemann") == (r["writer"] == "Riemann") for r in pages) / len(pages)
    tp = sum(pred[r["file"]]["pred"] == "Riemann" and r["writer"] == "Riemann" for r in pages)
    fp = sum(pred[r["file"]]["pred"] == "Riemann" and r["writer"] != "Riemann" for r in pages)
    fn = sum(pred[r["file"]]["pred"] != "Riemann" and r["writer"] == "Riemann" for r in pages)
    res = dict(
        config=dict(k=a.k, encoding=a.encoding, strips=a.strips, max_desc=a.max_desc, seed=a.seed),
        n_pages_evaluated=len(pages), n_pages_listed=len(train),
        dropped=[dict(writer=r["writer"], hs=r["hs"], label=r["label"], n_desc=r["n_desc"]) for r in train if r not in pages],
        accuracy=acc, nn_accuracy=nn_acc, confusion=confusion(pages, pred, writers),
        per_writer={w: subset_acc(pages, pred, lambda r, w=w: r["writer"] == w) for w in writers},
        binary_riemann=dict(accuracy=bin_ok, precision=tp / max(tp + fp, 1), recall=tp / max(tp + fn, 1), tp=tp, fp=fp, fn=fn),
        riemann_breakdown={
            "pencil (mentioned in transcript)": subset_acc(pages, pred, lambda r: r["writer"] == "Riemann" and r["medium"] == "pencil"),
            "ink/unspecified": subset_acc(pages, pred, lambda r: r["writer"] == "Riemann" and r["medium"] != "pencil"),
            "maths": subset_acc(pages, pred, lambda r: r["writer"] == "Riemann" and r["content"] == "maths"),
            "prose": subset_acc(pages, pred, lambda r: r["writer"] == "Riemann" and r["content"] == "prose"),
            "B19": subset_acc(pages, pred, lambda r: r["writer"] == "Riemann" and r["hs"] == HS_B19),
            "B26": subset_acc(pages, pred, lambda r: r["writer"] == "Riemann" and r["hs"] == HS_B26),
        },
        errors=[dict(writer=r["writer"], hs=r["hs"], label=r["label"], medium=r["medium"], content=r["content"], **pred[r["file"]])
                for r in pages if pred[r["file"]]["pred"] != r["writer"]],
        pages=[dict(writer=r["writer"], hs=r["hs"], label=r["label"], role=r["role"], medium=r["medium"], content=r["content"],
                    pencil_mention=r["pencil_mention"], n_desc=r["n_desc"],
                    darkness_median=feats[r["file"]][2].get("darkness_median") if r["file"] in feats else None,
                    darkness_p90=feats[r["file"]][2].get("darkness_p90") if r["file"] in feats else None,
                    cv=pred.get(r["file"])) for r in rows],
    )
    # final model on all training pages, applied to the targets
    km = fit_codebook([feats[r["file"]][0] for r in pages], a.k, a.seed)
    Xtr, ytr, full = [], [], []
    for r in pages:
        d, yy, _ = feats[r["file"]]
        for kind, dd in page_samples(d, yy, a.strips):
            e = encode(dd, km, a.encoding)
            Xtr.append(e)
            ytr.append(r["writer"])
            if kind == "full":
                full.append((e, r))
    clf = fit_classifier(np.array(Xtr), np.array(ytr), a.seed)
    F = np.array([e for e, _ in full])
    res["targets"] = []
    for t in targets:
        if t["file"] not in feats or len(feats[t["file"]][0]) < 150:
            res["targets"].append(dict(id=t["writer"], hs=t["hs"], label=t["label"], error="too few descriptors"))
            continue
        d, yy, _ = feats[t["file"]]
        samples = [encode(dd, km, a.encoding) for _, dd in page_samples(d, yy, a.strips)]
        P = clf.predict_proba(np.array(samples)).mean(0)
        Pfull = clf.predict_proba(samples[0][None])[0]
        sims = F @ samples[0]
        order = np.argsort(-sims)[:5]
        res["targets"].append(dict(
            id=t["writer"], hs=t["hs"], label=t["label"], canvas=int(t["canvas"]), note=t.get("note", ""),
            medium=t["medium"], darkness=t["darkness"], n_desc=t["n_desc"],
            pred=str(clf.classes_[int(np.argmax(P))]), prob={c: float(p) for c, p in zip(clf.classes_, P)},
            prob_full_page_only={c: float(p) for c, p in zip(clf.classes_, Pfull)},
            nearest=[dict(writer=full[j][1]["writer"], page="%s %s" % (full[j][1]["hs"], full[j][1]["label"]), sim=float(sims[j])) for j in order]))
    tag = "%s_k%d" % (a.encoding, a.k)
    with open(os.path.join(a.out, "results_%s.json" % tag), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    print(json.dumps({k: res[k] for k in ("accuracy", "nn_accuracy", "binary_riemann", "per_writer", "riemann_breakdown")}, indent=1))
    for t in res["targets"]:
        print(t["id"], t["label"], "->", t.get("pred"), {str(k): round(v, 3) for k, v in t.get("prob", {}).items()},
              "| nn:", [(n["writer"], n["page"].split()[-1], round(n["sim"], 3)) for n in t.get("nearest", [])[:3]])


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list")
    s.add_argument("--manifests", required=True, help="dir with <HS>.json IIIF manifests")
    s.add_argument("--data", required=True, help="repo data/ dir (transcript JSONs)")
    s.add_argument("--out", required=True)
    s = sub.add_parser("fetch")
    s.add_argument("--pages", required=True)
    s.add_argument("--images", required=True)
    s.add_argument("--interval", type=float, default=0.6, help="seconds between requests")
    s = sub.add_parser("run")
    s.add_argument("--pages", required=True)
    s.add_argument("--images", required=True)
    s.add_argument("--out", required=True, help="output directory")
    s.add_argument("--k", type=int, default=200, help="codebook size")
    s.add_argument("--encoding", choices=["hist", "vlad"], default="hist")
    s.add_argument("--max-desc", type=int, default=4000, help="max descriptors per page")
    s.add_argument("--strips", type=int, default=4, help="horizontal strips per page as extra training samples")
    s.add_argument("--seed", type=int, default=0)
    a = p.parse_args()
    {"list": cmd_list, "fetch": cmd_fetch, "run": cmd_run}[a.cmd](a)


if __name__ == "__main__":
    main()
