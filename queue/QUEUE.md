# Queue

Claim a **small unit** (one bundle / cote / E-number, ≤ 500 pages) by opening an issue `claim: <author> <unit>`;
the `claimed-by` column is for whole-source surveys only. Add rows for any public-domain, digitized source
whose host permits fetching. Order = current estimate of (chance of a real find) × (pages unread).

| id | author / source | pages (est.) | language | access | status | claimed-by |
|---|---|---|---|---|---|---|
| Q-01 | **Euler** — Opera omnia / Euler Archive (eulerarchive.maa.org, scholarlycommons.pacific.edu); Eneström index; start with works that have no English translation | ~30,000 | Latin, French, German | PDF per work; check robots.txt | surveyed 2026-11-09 (`data/euler/README.md`): 659 works / ~24,000 printed pp have no English translation; first batch of 24 works (~1,000 pp) in `data/euler/inventory.tsv` | — |
| Q-02 | **Euler** — St Petersburg notebooks (Adversaria mathematica; only partly published) | ~3,000 | Latin | **not digitized, not accessible** (Basel copies closed; St Petersburg originals) | blocked; only the 1862 printed extracts E806/E819 are readable | — |
| Q-03 | **Ramanujan** — Notebooks 1–3 and Lost Notebook (archive.org item `ramanujan-unpublished-notebooks-and-lost-notebook`, PD mark; IMSc page images `www.imsc.res.in/~rao/ramanujan/`) | ~900 | English/formulae | PDF / JPEG | ready; novelty baseline = Berndt, *Ramanujan's Notebooks* I–V; Andrews–Berndt, *Lost Notebook* I–V (only missed connections plausible) | — |
| Q-04 | **Grothendieck** — Montpellier cotes not yet read (EGA/SGA drafts etc.; see `data/grothendieck-montpellier/inventory.tsv` minus the 61 cotes with deep reads) | ~8,000 | French | PDF (grothendieck.umontpellier.fr) | parked: 61 cotes / 5,396 pp read → 0 candidates ≥ 7 | — |
| Q-05 | **Gauss** — bundles not yet transcribed (GDZ Nachlass; compare `data/gauss/transcripts/` against the GDZ catalogue) | unknown | Latin/German | IIIF | partial | — |
| Q-06 | **Riemann** — Cod. Ms. B. Riemann bundles without transcripts (compare `data/riemann/transcripts/` against the SUB catalogue) | unknown | German | IIIF | partial | — |
| Q-07 | **Hilbert** — Cod. Ms. D. Hilbert beyond 600 (lecture notes, correspondence) | ~10,000 | German | IIIF | 600/1–3 done (419 pp) | — |
| Q-08 | **Dedekind** — remaining Nachlass bundles | unknown | German | IIIF | 7 bundles done (100 pp) | — |

## Not queued (and why)
- Peirce, Nash, von Neumann, Cantor, Lagrange: considered; not started. Peirce's manuscripts (Harvard) are
  huge and largely unphilosophical-mathematics; Nash's and von Neumann's archives are not freely digitized at
  page level. Add a row with access details if you find a usable digitization.
