# Euler — access notes (survey 2026-11-09)

- **Index:** `euler_index.tsv` — all 866 Eneström numbers with title, year, language, printed pages, PDF URL,
  whether the Euler Archive lists an English translation (207 works as of 2021; list known incomplete), notes.
- **Scans:** University of the Pacific Digital Commons (`scholarlycommons.pacific.edu/euler-works/<E>`,
  PDF = `cgi/viewcontent.cgi?article=<E+999>&context=euler-works`) is the canonical host, but its downloads sit
  behind a Cloudflare browser challenge — automated fetching does not work and must not be worked around.
  The MAA mirror serves the original scans directly for many works:
  `http://eulerarchive.maa.org/docs/originals/E<NNN>.pdf` (three-digit, zero-padded; HTTP, 404 for some).
  These are CCITT-G4 fax-encoded bitonal scans (`src/pdf_images.py` handles them via Pillow).
  Opera omnia volumes open at Basel (`bez.unibas.ch/LEOOI<n>`, Series I) and PublBEZ (II/26, II/27, CC BY-SA);
  HathiTrust and archive.org hold more (see `euler_index.tsv` notes).
- **Untranslated:** 659 works, ≈ 24,000 printed pages after removing duplicate collections; Latin ≈ 20,000.
- **Notebooks (Adversaria mathematica, 12 vols, ≈ 3,000 pp):** originals in St Petersburg, photocopies in Basel —
  neither online nor open. Only the 1862 *Opera postuma* extracts (E806, E819) are readable.
- **First batch (`inventory.tsv`):** 24 untranslated works available on the MAA mirror, ≈ 1,000 pages:
  posthumous/unfinished number theory and variational papers, elasticity and buckling, series and elliptic
  arcs, the tides prize essay. Chosen for priority disputes and posthumous/unfinished status.
- **Baseline for novelty:** Opera omnia editors' introductions and commentaries; Fellmann, *Leonhard Euler*;
  Sandifer, *How Euler Did It*; Truesdell's Series II introductions (mechanics); Weil, *Number Theory*.
