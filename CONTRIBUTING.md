# Contributing

One rule above all: **contribute freely, claim only through review.** Anyone may add transcriptions, deep
reads, candidates and dead ends. A candidate becomes a "find" only when its label says `reviewed` or `expert`.

## 1. Run the pipeline on a source

- Pick a source from `queue/` (or add one: public-domain, digitized, on a host whose `robots.txt` permits
  fetching). **Claim units are small** — one bundle / cote / E-number, or ≤ 500 pages — never a whole author.
  Claim by opening an issue titled `claim: <author> <unit>`; close it when your PR merges. Check open claim
  issues before starting so two people don't pay for the same pages.
- Scans: IIIF images → `src/transcribe.py <manifest.json> <out_dir> --source "<author, archive, dates, language>"`;
  scan PDFs → `src/read_source.py` (downloads to a scratch dir, extracts page JPEGs with `src/pdf_images.py`,
  transcribes, deep-reads). Both are resumable; both need `~/.config/hunt/anthropic_key`.
- Run `src/repair_json.py` afterwards, then check `src/validate.py` for failed deep reads. If the repair
  script reports unrepairable deep reads, re-run it with `--delete` to clear those outputs before retrying
  the deep-read stage. The pipeline skips existing output files, including failed ones.
- Commit `data/<author>/transcripts/...` and `data/<author>/deep/...` and run
  `python3 -I src/validate.py data/<author> --status`. Never commit scans, keys, or anything from a source
  whose terms forbid republication.

## 1b. Share transcriptions only (no deep reads) — welcome

You do not have to run the pipeline or do any analysis. If you have transcribed pages of a public-domain
manuscript — with any model, any tool, or by hand — put them in `data/<author>/transcripts/<bundle>/` as one
JSON per page with just these fields (full format in `data/FORMAT.md`, but this is enough):

```json
{"image": "https://…/scan-of-the-page.jpg", "label": "70r", "parsed": true,
 "source": "human" ,  "result": {"transcription": "the text, original language, LaTeX in $...$"}}
```

Then run `python3 -I src/validate.py data/<author> --status` — it tells you what is missing and updates
`data/<author>/STATUS.tsv`, which is how others see that your bundle is `transcribed` and still needs
deep reads. Someone else (or you, later) runs `src/deep.py` on it. Plain-text transcriptions (one `.txt`
per page, same names) are fine too if you do not want to make JSON — say so in the PR and a maintainer
will wrap them.

## 1c. Share translations

`data/<author>/translations/<bundle>/cNNN.md`, one per page, first line
`<!-- page: <bundle>/<cNNN> | by: human | <model id> | model:<id>+human -->`, then the English (or other
target language) text in the original line order. Label stays whatever the transcription has; translations
never replace the original-language transcription.

## 2. Fix a transcription by hand

Open the page JSON, set `"human_corrected": true`, fix the text, say what you changed in the PR. A human
reading beats any model output and is used by every later agent.

## 2b. Work the hot list (the fastest way to help)

`docs/HOT_PAGES.md` lists every deep-read page the model rated surprise ≥ 5 that nobody has looked at
(regenerate with `python3 -I src/hot_pages.py`). Pick one, read the scan yourself, check the author's own
publications and older sources, then either add a one-line entry under "Dropped" in the ledger (with the
source that kills it) or open a candidate. Most entries die in ten minutes; that is useful work.

## 3. Propose a candidate

Copy `candidates/TEMPLATE.md`. Fill every section of the four-step protocol you have actually done; leave the
rest empty rather than guessing. Attach: scan link, page JSON, verification script. Label it `self-checked`.
Add one line to `ledger/LEADS.md` under "Unverified candidates".

Before labelling anything `self-checked`, run the checklist in `docs/FALSE_POSITIVES.md` (the twelve standard
failure modes, with the check that catches each). What usually kills a candidate:
- the author's own publications (Esquisse, Werke, Bourbaki talks, letters already in print);
- an older source than the model's "usually credited to" (its dates run late);
- the published editors' reports on the same folder (e.g. Riemann Nachträge 1902);
- the result being "wrong as written" (test it on the first simple example).

## 4. Review a candidate

Independent of the finder's reading — another contributor, or an unanchored agent given only the facts (say which in the file). Redo steps 1–4: read the scan, run or rewrite the verification, search the
literature yourself, and — ideally — run an unanchored check (give a fresh agent only the facts). Write the
verdict in the candidate file with sources and a 0–10 rating:
10 usable today / major unrecognised anticipation; 7 strong historical anticipation needing routine
confirmation; 5 notable historical detail; 1–2 routine. Set the label `reviewed`. Ratings without a written
verdict are not accepted.

## 5. Expert verdict

If you are a specialist in the author or the field: a paragraph on a scan is worth more than anything else in
this repo. Open an issue or PR on the candidate; you are named only if you want to be.

## 6. Improve the repo itself

Code, prompts, formats, docs, this file — all open to PRs. Two conditions:
- **Prompt changes** (`src/transcribe.py`, `src/deep.py`, `src/read_source.py`): show before/after output on
  five pages from `data/` in the PR, so the change is judged on pages, not on taste.
- **Format changes** (`data/FORMAT.md`): update `src/validate.py` in the same PR and say how existing files
  migrate. Readers of old files must not break.
Anything else — better scripts, a web viewer for the hot list, new source adapters, translations of the
docs — just open the PR.

## Style

Plain language in summaries. Separate evidence (quote, page, scan link) from interpretation, and say which is
which. "Not found" is a valid and useful result.
