# Writer identification for Riemann Nachlass pages — results

Script: `src/writer_id.py` (classical pipeline, no API calls). Run date: 2026-11-09.
Question: are the unattributed pages T1–T4 in Riemann's hand? T5 and T6 are controls.

Everything below is what the classifier computed on the pages listed. It is evidence about
visual similarity of handwriting under this method; it is not a palaeographic verdict.

## Method

1. **Images.** IIIF scans, 1300 px wide, from GDZ (SUB Göttingen). 6 % margin cropped on each side.
2. **Preprocessing.** Grayscale, 3×3 median filter, illumination flattened by dividing by a
   morphological-closing background estimate, Sauvola binarisation (window 31, k = 0.2) plus a
   minimum local contrast of 12 grey levels, connected components kept if 8 px ≤ area ≤ 2 % of the
   page and height/width < 25 % of the page (removes specks, stains, ruled lines, page edges).
3. **Descriptors.** Per-page contrast stretch (so pencil and ink pages look alike to the detector),
   then OpenCV SIFT keypoints (contrast threshold 0.02, keypoint size 2–48 px) restricted to the
   ink mask dilated by 2 px; the 4000 strongest keypoints per page; RootSIFT descriptors.
4. **Codebook and encoding.** MiniBatchKMeans on up to 1200 descriptors per training page.
   Variant A: k = 200, bag-of-visual-words histogram with square-root and L2 normalisation.
   Variant B: k = 64, VLAD (intra-normalised, signed square root, L2).
   Each page gives 5 samples: the full page and 4 horizontal strips split by descriptor count
   (strips only if the page has ≥ 600 descriptors). Pages with < 150 descriptors are dropped.
5. **Classifier.** StandardScaler + multinomial logistic regression (C = 1, class-balanced
   weights). Page prediction = mean of the probabilities of its full-page and strip samples.
   Baseline: cosine nearest neighbour between full-page encodings (1-NN).
6. **Evaluation.** 5-fold cross-validation, stratified by writer, grouped by page (all samples of a
   page stay in one fold). The codebook, scaler and classifier are refit on the training folds of
   each split; the held-out pages never touch the codebook. Seed 0 throughout. The two variants
   are the only two configurations run; nothing was tuned on the targets.
7. **Targets.** Codebook and classifier refit on all training pages, then applied to T1–T6.

## Dataset

All pages are public-domain scans at SUB Göttingen (GDZ). Pages were selected by deterministic
rules in `writer_id.py list` (non-blank per the transcript, ≥ 200–300 characters transcribed,
evenly spaced through the folio ranges), then every page was looked at; pages that are not in the
catalogued writer's hand were excluded with the reasons listed further down.

| Writer | Source (SUB Göttingen) | GDZ id | Pages listed | Folios / pages |
|---|---|---|---|---|
| Riemann | Cod. Ms. B. Riemann 19 | DE-611-HS-3206670 | 40 | 85r, 85v, 86r, 86v, 87r, 89r, 90v, 91r, 91v, 92r, 92v, 93r, 94r, 95r, 95v, 96r, 96v (theta-function notes, 1862/1865); 122r, 129r, 132r, 135r, 137v, 140r, 142v, 145r, 148r, 152v, 155v, 158r, 160v, 164v, 168v, 171v, 174r, 176v, 179r, 181v, 184r, 187r, 189v (1857 Abelian-functions drafts, every 5th non-blank leaf) |
| Riemann | Cod. Ms. B. Riemann 26 | DE-611-HS-3206190 | 22 | 183v (letter 1853), 100r (1858), 122r (letter draft 1861), 146v (1855); 1r, 3v, 6r, 12r, 18v, 22r, 24v, 27v, 30v, 35r, 37v, 40r, 42v, 45r, 49r, 52v, 55v, 58r (notes, every 5th non-blank) |
| Weierstrass | Cod. Ms. B. Riemann 19 | DE-611-HS-3206670 | 4 | 103r, 103v, 104r, 104v |
| Weber (Heinrich) | Cod. Ms. B. Riemann 19 | DE-611-HS-3206670 | 12 | 115r–120v |
| Dedekind | Cod. Ms. R. Dedekind: Bemerkungen | DE-611-HS-3234986 | 7 | 1r, 1v, 5r, 7r, 8r, 9r, 10r |
| Dedekind | Galois | DE-611-HS-3226591 | 3 | 25r, 25v, 26v |
| Dedekind | Rationale Zahlen | DE-611-HS-3234961 | 8 | 1r, 2v, 4r, 5r, 7r, 8r, 8v, 10r |
| Dedekind | Reciprocität 1855 | DE-611-HS-3234955 | 4 | 21r, 22r, 23v, 24v |
| Dedekind | Stetigkeit | DE-611-HS-3234959 | 7 | 1v, 2r, 3r, 4r, 5r, 6r, 7r/8v |
| Dedekind | Zahlbegriff | DE-611-HS-4289575 | 1 | 1r |
| Hilbert | Cod. Ms. D. Hilbert 600/1 (scientific diary) | DE-611-HS-3763733 | 11 | pp. 1, 11, [24], 37, [50], 63, [76], 89, [102], 115, [128] |
| Hilbert | Cod. Ms. D. Hilbert 600/2 | DE-611-HS-3763752 | 8 | [8], 21, [34], 47, [60], [72], 85, 99 |
| Hilbert | Cod. Ms. D. Hilbert 600/3 | DE-611-HS-3763758 | 11 | [2], 15, [28], 41, [54], 67, [80], 95, [108], 121, [134] |
| Gauss | Cod. Ms. Gauss Math. 21 | DE-611-HS-3381609 | 9 | 1r, 5r, 10v, 14v, 20r, 25v, 32v, 39r, 52r |
| Gauss | Gauss Handbuch, Opuscula 1800 | DE-611-HS-3351307 | 21 | [2], 11, [20], 29, 39, [50], [70], [78], 93, 101, [110], [118], [136], [144], 155, [164], 173, 181, 191, [228], [238] |

Totals listed: Riemann 62, Weierstrass 4, Weber 12, Dedekind 30, Hilbert 30, Gauss 30 = 168.
Dropped automatically for having < 150 ink keypoints (nearly blank): Riemann B.19 122r, B.26 18v,
B.26 55v; Weber 116v. **Evaluated: 164 pages** (Riemann 59, Weierstrass 4, Weber 11, Dedekind 30,
Hilbert 30, Gauss 30).

Never used for training: B.26 fol. 70r–71v and 228r; B.19 fol. 3r–3v, 97r–97v and the whole leaf 101.

**Corrections to the catalogue ranges, made after looking at the scans**

- Weierstrass, B.19 fol. 100r–105v: 100r is a 1920 archival note in ink (it states that the leaves are
  in Weierstrass's hand) over faint pencil; 100v, 102r, 102v, 105r, 105v are blank; leaf 101 is the
  held-out control. Only the two leaves 103–104 (four pages) carry clear writing in that hand, so the
  Weierstrass class has 4 pages. This is the weakest class.
- Dedekind: excluded Bemerkungen 2r (printed library receipt), 4r (printed note from a bookseller),
  6r (printed offprint title page); Rationale Zahlen 2r and 9v (reused court-judgment sheets, mostly
  a clerk's hand), 3v (reused printed order form), 5v/6r (reused printed subscription form).
- Gauss: excluded Math. 21 fol. 47v (legal pleading dated 1894), 15v (rotated sheet with English
  writing exercises), 25r (calligraphy practice), 47br (dot-grid diagrams, almost no writing).
- Riemann: B.19 121r (folder cover with archival notes) skipped by rule.

Labels for the Riemann breakdown: "pencil" = the page transcript (`data/riemann/transcripts`)
explicitly mentions pencil (10 of the 59 evaluated pages); the rest are "ink/unspecified".
An image darkness statistic was tried for this and rejected: known-ink Weber pages measure like faint
Riemann pages, because scan exposure and ink fading vary more than the pencil/ink difference.
"prose" = transcript topic says letter/prose, or the page has < 1 formula marker per 100 characters
and > 80 words (16 pages); the rest are "maths" (43).

## Held-out accuracy (5-fold grouped CV, 164 pages)

| | Variant A: histogram, k = 200 (primary) | Variant B: VLAD, k = 64 |
|---|---|---|
| Six-class page accuracy (logistic regression) | **160/164 = 97.6 %** | 159/164 = 97.0 % |
| Six-class page accuracy (1-NN cosine baseline) | 151/164 = 92.1 % | 160/164 = 97.6 % |
| Binary Riemann vs not-Riemann accuracy | 161/164 = 98.2 % | 160/164 = 97.6 % |
| Binary precision / recall for Riemann | 0.983 / 0.966 (1 FP, 2 FN) | 1.000 / 0.932 (0 FP, 4 FN) |

Per writer (correct / evaluated), variant A: Riemann 57/59, Weierstrass 4/4, Weber 11/11,
Dedekind 29/30, Hilbert 30/30, Gauss 29/30. Variant B: 55/59, 4/4, 11/11, 30/30, 30/30, 29/30.

Confusion matrix, variant A (rows = true writer, columns = predicted):

| true \ pred | Riemann | Weierstrass | Weber | Dedekind | Hilbert | Gauss |
|---|---|---|---|---|---|---|
| Riemann (59) | 57 | 0 | 1 | 1 | 0 | 0 |
| Weierstrass (4) | 0 | 4 | 0 | 0 | 0 | 0 |
| Weber (11) | 0 | 0 | 11 | 0 | 0 | 0 |
| Dedekind (30) | 0 | 0 | 0 | 29 | 1 | 0 |
| Hilbert (30) | 0 | 0 | 0 | 0 | 30 | 0 |
| Gauss (30) | 1 | 0 | 0 | 0 | 0 | 29 |

Confusion matrix, variant B:

| true \ pred | Riemann | Weierstrass | Weber | Dedekind | Hilbert | Gauss |
|---|---|---|---|---|---|---|
| Riemann (59) | 55 | 0 | 1 | 0 | 1 | 2 |
| Weierstrass (4) | 0 | 4 | 0 | 0 | 0 | 0 |
| Weber (11) | 0 | 0 | 11 | 0 | 0 | 0 |
| Dedekind (30) | 0 | 0 | 0 | 30 | 0 | 0 |
| Hilbert (30) | 0 | 0 | 0 | 0 | 30 | 0 |
| Gauss (30) | 0 | 0 | 0 | 1 | 0 | 29 |

Misclassified pages, variant A: Riemann B.19 129r (letter draft on grey paper → Weber, P = 0.89);
Riemann B.26 6r (a page of numerical tables, mostly digits → Dedekind 0.45 / Gauss 0.44);
Dedekind Zahlbegriff 1r (neat prose → Hilbert 0.52); Gauss Opuscula [228] (→ Riemann 0.70).
Variant B additionally misses Riemann B.19 135r (→ Hilbert) and B.26 45r (→ Gauss), and Gauss
Math. 21 52r (→ Dedekind), but gets B.26 6r, Dedekind 1r and Opuscula [228] right.

Riemann pages by subset (correct / n):

| Subset | Variant A | Variant B |
|---|---|---|
| pencil (mentioned in transcript) | 10/10 | 9/10 |
| ink / unspecified | 47/49 | 46/49 |
| maths | 42/43 | 40/43 |
| prose (letters, drafts) | 15/16 | 15/16 |
| B. Riemann 19 | 38/39 | 37/39 |
| B. Riemann 26 | 19/20 | 18/20 |

The subsets are small; with 10 pencil pages one error is 10 points. The numbers do not show a
pencil/ink or maths/prose weakness, but they cannot exclude one either.

## Target pages

Model fit on all 164 training pages. P = class probability of the logistic regression (mean over the
full page and its 4 strips); "nearest" = training pages with the highest cosine similarity to the
full-page encoding.

| Target | Page | Keypoints | Variant A: prediction, P(Riemann), nearest 3 | Variant B: prediction, P(Riemann), nearest 3 |
|---|---|---|---|---|
| T1 | B.26 fol. 70v (canvas 142) | 2373 | Riemann, 0.998; B.19 94r, 96v, 86v | Riemann, 0.995; B.26 1r, B.19 94r, 86r |
| T2 | B.26 fol. 71r (canvas 143) | 3165 | Riemann, 0.978; B.19 94r, 96v, B.26 3v | Riemann, 0.998; B.19 86v, B.26 1r, B.19 94r |
| T3 | B.26 fol. 228r (canvas 447) | 3632 | Riemann, 0.971 (Gauss 0.021); B.26 45r, B.19 179r, B.26 40r | Riemann, 0.809 (Gauss 0.183); B.19 158r, 181v, B.26 52v |
| T4 | B.19 fol. 3v (canvas 8) | 4000 | Riemann, 0.969 (Dedekind 0.023); B.19 94r, 86r, 96v | Riemann, 0.999; B.19 95r, 93r, 94r |
| T5 (control, Riemann) | B.19 fol. 97r (canvas 197) | 4000 | Riemann, 0.999; B.19 94r, 86r, 96v | Riemann, 1.000; B.26 1r, B.19 94r, 87r |
| T6 (control, Weierstrass) | B.19 fol. 101r (canvas 205) | 3246 | Weierstrass, P(Weierstrass) = 0.975, P(Riemann) = 0.007; nearest 104v (Weierstrass), Hilbert [80], 104r (Weierstrass) | Weierstrass, P = 1.000, P(Riemann) = 0.000; nearest 103r, 104v, 103v (all Weierstrass) |

Using the full page alone (no strips) changes no prediction: P(predicted class) is ≥ 0.98 for every
target in both variants, except T3 in variant B (0.959).

Controls: **T5 comes out Riemann and T6 comes out Weierstrass in both variants**, as expected.
For T1–T5 all of the five nearest training pages are Riemann pages in variant A, except that the 5th
neighbour of T3 is Gauss Opuscula [228] (a page the CV also confused with Riemann).

## Leave-one-volume-out check (added 2026-11-09)

Script: `src/writer_id_crossvolume.py` (reuses the descriptor cache; same seed, same two encodings).
Question: is a target called "Riemann" only because Riemann training pages share its volume?
Run A trains the Riemann class on Cod. Ms. 19 pages only and holds out every Riemann page of Cod. Ms. 26.
Run B swaps the volumes. The other writers' pages are unchanged.

| | Run A, histogram | Run A, VLAD | Run B, histogram | Run B, VLAD |
|---|---|---|---|---|
| Riemann pages in training | 39 (B.19) | 39 (B.19) | 20 (B.26) | 20 (B.26) |
| Known Riemann pages of the other volume called Riemann | 13/20 | 12/20 | 38/39 | 36/39 |
| T1 B.26 70v, P(Riemann) | 0.966 | 1.000 | 0.913 | 0.943 |
| T2 B.26 71r | 0.969 | 1.000 | 0.765 | 0.977 |
| T3 B.26 228r | 0.957 (Gauss 0.04) | 0.888 (Gauss 0.11) | 0.993 | 0.876 (Gauss 0.12) |
| T4 B.19 3v | 0.961 | 0.996 | 0.598 (Dedekind 0.29) | 0.849 |
| T5 control B.19 97r | 1.000 | 1.000 | 0.993 | 0.980 |
| T6 control B.19 101r, P(Weierstrass) | 0.985 | 1.000 | 0.946 | 1.000 |

The rows that matter are T1–T3 in run A and T4 in run B: there the target's own volume contributes no Riemann
training page. All four stay Riemann. T4 is the weakest (0.60 in one encoding, with a 20-page Riemann class).

The second row is a warning about the method. Trained on Cod. Ms. 19 alone, it recognises only 12–13 of the 20
known Riemann pages of Cod. Ms. 26. The misses are the fair-copy prose leaves 22r, 27v, 30v, 35r (called Hilbert
or Weber), the table page 6r, and 24v, 42v, 45r, 52v. So the 97–98 % cross-validation figure above depends on
having pages of the same volume and style in training; across volumes and styles the method is much weaker.
Either those prose leaves are a style the maths pages do not teach, or their catalogue attribution is wrong.

## What this does and does not show

- Under this method, the handwriting on T1, T2, T3 and T4 is classified as Riemann's with
  probabilities 0.97–1.00 (variant A) and 0.81–1.00 (variant B), and their nearest training pages are
  Riemann pages from both volumes. T3 (228r) is the least certain (variant B gives Gauss 0.18).
- The method told the two other hands in the same volume (Weierstrass, Weber) apart from Riemann in
  every cross-validation fold (15/15 pages, 0 Riemann pages called Weierstrass, 1 called Weber), so
  the decision is not just "same paper and scanning campaign as the Riemann pages".
- Held-out accuracy is 97 % on 164 pages, but the comparison set is six writers only. The classifier
  can only say which of these six hands a page resembles most; a page by a seventh writer (a student,
  a copyist, Riemann's brother) would still be assigned to one of the six, most likely Riemann if the
  paper and script style are similar.

## Limitations

- **Six hands only.** Not a verification system; no open-set rejection. See above. A specific missing hand:
  Alfred Clebsch (elasticity; worked on the Nachlass until 1872; a fair copy by him is in Cod. Ms. B. Riemann 3,
  fol. 16–18). He matters most for the elasticity sheet T3.
- **Same-volume confound.** Riemann training pages, Weierstrass, Weber and all six targets come from
  the same two volumes. Paper texture, ruling, show-through and scanning conditions are shared. The
  ink mask and local SIFT descriptors reduce but do not remove this; the Weierstrass/Weber result
  and the leave-one-volume-out check above are the direct checks; the first rests on 15 pages (4 for Weierstrass).
- **Weierstrass class has 4 training pages**, two leaves, one sitting. T6 being recognised shows the
  method works on that hand, but the class is thin.
- **Training labels are catalogue attributions**, not independently verified page by page. Twelve
  catalogue-range pages were found to be printed matter or other hands and excluded (listed above);
  others may remain. B.26 fol. 22r–35r are in a neat fair-copy prose hand; they were all classified
  as Riemann in CV, but their attribution rests on the catalogue.
- **Riemann's 1857 drafts are written on printed ledger forms.** Full-height ruled lines are removed,
  small printed headings are not; some Riemann descriptors are therefore print.
- **Reverse-side show-through** is partly kept on dark-ink pages (e.g. B.26 183v); it is mirrored
  writing by the same hand in that case, but adds noise.
- **Pencil/ink labels** come from the transcript text mentioning pencil (10 pages); the image-based
  statistic failed. The medium of the targets was not determined.
- **SIFT is rotation-invariant per keypoint**, so slant information is partly lost; no attempt was
  made to use upright descriptors. Only two configurations were run, as agreed.
- Single seed, single fold assignment. Differences of one or two pages between variants are noise.

## Reproduce

```
mkdir -p W/manifests   # fetch the two IIIF manifests into W/manifests/<HS>.json first
python3 -E -P src/writer_id.py list  --manifests W/manifests --data data --out W/pages.tsv
python3 -E -P src/writer_id.py fetch --pages W/pages.tsv --images W/images      # <= 2 req/s
python3 -E -P src/writer_id.py run   --pages W/pages.tsv --images W/images --out W/results --k 200 --encoding hist
python3 -E -P src/writer_id.py run   --pages W/pages.tsv --images W/images --out W/results --k 64  --encoding vlad
```
Outputs: `W/results/results_hist_k200.json`, `W/results/results_vlad_k64.json` (per-page CV
predictions, confusion matrices, target scores). Scans stay outside the repository.
Needs: `opencv-python-headless`, `scikit-learn`, `numpy`, `Pillow`.
