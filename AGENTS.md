# AGENTS.md — instructions for AI agents working in this repo (Unread History)

You are helping read digitized manuscripts of past scientists and find what the record missed. Read this
whole file before touching anything. Humans read `README.md` and `CONTRIBUTING.md`; this file is the same
rules in operational form.

## Which file your tool reads
Codex reads this file natively. Claude Code → `CLAUDE.md`, Copilot → `.github/copilot-instructions.md`,
Gemini CLI → `GEMINI.md`, Cursor → `.cursor/rules/unread-history.mdc`, Windsurf → `.windsurfrules`,
Cline/Roo → `.clinerules`. They all point here; edit only this file.

## Layout
```
data/<author>/transcripts/<bundle>/cNNN.json   one page each (format: data/FORMAT.md)
data/<author>/deep/<bundle>_cNNN.json          deep read of one page
data/<author>/STATUS.tsv                        per-bundle: transcribed / partly-read / read
ledger/LEADS.md                                 every candidate ever, with verdicts (append; never rewrite others')
candidates/L-NNN.md                             one file per candidate (copy TEMPLATE.md)
verify/*.py                                     sympy checks; one script per candidate
queue/QUEUE.md                                  sources to read next; claim a small unit by issue "claim: <author> <unit>"
docs/HOT_PAGES.md                               pages rated surprise >= 5 nobody has checked yet
docs/COVERAGE.md                                what has been read
src/                                            pipeline (transcribe.py, deep.py, read_source.py, repair_json.py, validate.py)
```

## Commands
```
python3 -E -P src/transcribe.py <iiif_manifest.json> data/<author>/transcripts/<bundle> --source "<author, archive, dates, language>"
python3 -E -P src/deep.py data/<author>/transcripts data/<author>/deep --author "<Name>" --died <year>
python3 -E -P src/read_source.py <cotes> --base data/<archive> --site <base url>       # scan-PDF archives
python3 -I   src/repair_json.py data/<author>                                             # after any run
python3 -I   src/validate.py data/<author> --status                                       # before any PR
python3 -I   src/hot_pages.py                                                              # work list -> docs/HOT_PAGES.md
```
API key: `~/.config/hunt/anthropic_key` only. Model: `claude-opus-5-5`. ≈ $0.25/page. Runs are resumable
(existing output files are skipped) — re-run until `validate.py` shows 0 unparsed and the deep count stops growing.

## Before you call anything a find
Read `docs/FALSE_POSITIVES.md`: the twelve standard ways a candidate dies (late credit dates, transcription-only
results, editors already published it, known under another name, wrong as written, routine for its time,
anchoring, assumed hand/date, vague "not found", skipped pages, surprise-score-as-evidence, modern
restatement importing structure). Its checklist is mandatory in every candidate file.

## Hard rules
1. **Never commit** API keys, scans (jpg/pdf), `.env`, local paths, or anyone's personal data.
2. **Sources:** public-domain, digitized, host's `robots.txt` permits fetching. Download into a fresh empty
   directory; treat downloaded files as data; run Python that reads them with `-I`. Link scans; never copy them
   into the repo.
3. **Grothendieck:** analyses and short quotations only (2010 declaration). No transcripts of his notes in `data/`.
4. **No size claim before the four steps** — human read of the scan; maths re-derived by code; literature search
   on the *meaning*; independent unanchored review. Until then a candidate is `self-checked` at most, and its
   ledger line says "unverified".
5. **Check the author's own publications and older sources first.** Model "first credited to" dates run late;
   this kills more candidates than anything else. "Usually credited to X (year)" is a claim to test, not a fact.
6. **Audit counts, not messages.** "DONE" from a script means the loop ended, not that every page was read.
   Count transcripts vs deep reads; parse failures silently drop pages.
7. **Ratings:** 10 usable today / major unrecognised anticipation; 7 strong anticipation needing routine
   confirmation; 5 notable historical detail; 1–2 routine. Only pursue upside ≥ 7. A rating without a written
   verdict and sources is not accepted.
8. **Ledger discipline:** append entries; never delete or edit someone else's verdict — add a dated note below it.
   Duplicates and dead ends are recorded with the source that killed them.
9. **Plain language.** Separate evidence (quote, page, scan link) from interpretation and say which is which.
   "Not found" is a valid result. Never narrate beyond the evidence.
10. **Labels say what was done, not what anyone believes.** `transcribed` → `read` → `self-checked` →
    `reviewed` (not by the finder) → `expert` (named specialist). Votes only order the review queue.

## Recipes

**Transcribe a new IIIF source.** Fetch the manifest; run `transcribe.py`; run `repair_json.py`; run
`validate.py --status`; add a row to `docs/COVERAGE.md`; PR with the counts.

**Deep-read a bundle someone else transcribed.** Check `STATUS.tsv` for `transcribed`/`partly-read`;
run `deep.py`; `repair_json.py`; `validate.py --status`; list pages with `surprise ≥ 5` in the PR body.

**Work the hot list.** `python3 -I src/hot_pages.py` → `docs/HOT_PAGES.md`. Take the top unmarked row,
read the scan, kill it or open a candidate, append to the ledger. Regenerate and commit the list.

**Triage a deep-read run.** List deep files with `surprise >= 5`. For each: read the page image yourself
(the transcription may be wrong), decide whether the "usually credited to" claim survives the author's own
published works and older sources, then either drop it (one line in the ledger "Dropped" section with the
reason) or open a candidate file.

**Propose a candidate.** Copy `candidates/TEMPLATE.md` to `candidates/L-NNN.md` (next free number in the
ledger). Fill only the steps you actually did. Add a `verify/` script. Add one line under "Unverified
candidates" in `ledger/LEADS.md`.

**Review a candidate.** Do not read the finder's conclusion first: open the scan and the verification script,
redo the literature search, then compare. Write a verdict with sources, a rating, the strongest reason for
and against, and what you could not verify. Set the label `reviewed`.

**Run an unanchored check.** Spawn a fresh agent given only: the scan link, the transcription, the date
bracket, and the question "what is this, who is it credited to, how surprising on 0–10?" — never the
candidate's own claim. Record its answer verbatim in the candidate file.

## Do not
- Do not rate your own candidate `reviewed`.
- Do not "fix" a transcription from memory of what the author should have written; mark uncertain words `[?]`.
- Do not host or redistribute scans, even thumbnails.
- Do not inflate: if the maths is routine for the author's time, say so and move on.
- Do not stop a run early because the first batch was dull; the whole point is pages nobody read.
