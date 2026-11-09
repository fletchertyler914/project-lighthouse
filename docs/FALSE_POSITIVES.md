# False positives — how a "find" in an old manuscript turns out to be nothing, and the check that catches it

Reading archives with language models produces candidates fast. Almost all of them die. These are the standard
ways they die, with the check that catches each one. The checklist at the end is required in every candidate
file before the label `self-checked`, and again before any rating.

## 1. The attribution date is too late
Models (and most people) date an idea by its famous paper, not by its first appearance. "Usually credited to
X (year)" is a hypothesis, and it is wrong often enough that it should never be the basis of a claim.
**Check:** the author's own publications first (collected works, printed letters, lecture notes, talks), then
sources older than the proposed date, then the standard histories of the subfield.

## 2. The result exists only in the transcription
One misread symbol, one hallucinated line, and a routine page becomes a discovery. The scan is the evidence;
the transcription is a guess about it.
**Check:** a human reads the scan. Any verification code is written from the scan, not from the JSON.

## 3. The editors already published it
Collected-works editors, Nachträge volumes and catalogue commentaries cover far more of a Nachlass than people
assume. Many "unpublished" sheets were printed a century ago under a heading nobody searches.
**Check:** the editors' reports and commentary for that folder; the archive's catalogue entry; the historical
literature on that specific bundle.

## 4. Known under another name
The same mathematics is often named after someone else, stated in a different special case, or written in
another notation. A name search finds nothing; a meaning search finds the textbook.
**Check:** search by the mathematics itself (the equation, a special case, numerical values) in two or three
phrasings, and in the author's own language.

## 5. Wrong as written
Notebooks contain guesses. A boxed conjecture is not a theorem, and a confident claim can be false.
**Check:** test the statement on the first non-trivial example before doing anything else.

## 6. Routine for its time
Competent contemporaries could have done it in an afternoon; the author simply didn't publish it. This is the
most common reason a 6 becomes a 3.
**Check:** "could a good student of that decade do this from the textbooks of that decade?" If yes, rate ≤ 3.

## 7. Anchoring
A reviewer told "this anticipates X" will find X. So will a model.
**Check:** the independent review receives only the scan, the transcription, the date bracket and the
question "what is this, who is it credited to, how surprising 0–10?" — never the candidate's claim.

## 8. Hand and date assumed
A sheet in a bundle is not necessarily in the author's hand or from the catalogue's date range. Copies,
students' notes, later insertions and misfiled papers are common.
**Check:** state explicitly what the rating depends on. Dating evidence (dated adjacent pages, paper, ink,
internal references) goes in the candidate file. "The author wrote" is not allowed until a palaeographer says
so; "the Nachlass contains" is.

## 9. "Not found" that means "didn't look well"
A model reporting "no earlier source found" describes one search, not the literature.
**Check:** list the exact queries, databases and sources checked, so someone else can repeat them.

## 10. "Fully read" when pages were skipped
Parse failures, budget stops and rate limits silently drop pages; the log still prints DONE.
**Check:** `validate.py` counts: unparsed = 0, deep reads ≥ maths pages. Audit numbers, not messages.

## 11. The surprise score is a model opinion
It is a triage number for ordering the hot list. It is not evidence, not a rating and not reportable.
**Check:** ratings come only from the four-step protocol, written down with sources.

## 12. Modern restatement imports structure that is not on the page
"In modern terms this is a Hodge structure" can be true of the restatement and false of the page.
**Check:** verbatim quote first, then the gloss, then the interpretation — each labelled. If the modern object
needs ingredients the page does not have, say which.

## Wording rules
- Never "discovered", "proved", "anticipated" without the four steps done and cited. Before that: "the page
  contains", "in modern terms this reads as", "if the reading is right".
- Every rating carries its conditions ("7 if hand and date hold").
- Dead candidates stay in the ledger with the source that killed them. A deleted dead candidate is a false
  positive waiting to be rediscovered.

## Pre-flight checklist (copy into the candidate file)
- [ ] I read the scan myself; the key lines are quoted verbatim in the original language
- [ ] I tested the statement on a simple example / ran the verification script written from the scan
- [ ] I checked the author's own publications and the editors' commentary for this folder
- [ ] I searched by meaning (equation, values, alternative names), in the author's language too, and listed the queries
- [ ] I looked for a source older than the proposed "credited to" date
- [ ] I stated what the rating depends on (hand, date, reading) and did not assume any of it
- [ ] The surprise score is nowhere in my claim
- [ ] Someone or something unanchored has looked at it, or the label is still `self-checked`

---
*Examples of each mode in this repo's ledger:* 1 → L-023, L-024; 2 → several Dropped entries; 3 → L-020, L-031;
4 → L-008, L-016; 5 → L-004, L-027; 8 → L-019; 10 → Montpellier batch 2, Göttingen gap-fill 2026-11.
