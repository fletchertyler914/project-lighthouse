# Data formats

## Minimal transcript page (enough for everyone's deep readers)
```json
{"image": "https://…", "label": "70r", "parsed": true, "source": "human | <model id> | model:<id>+human",
 "result": {"transcription": "…"}}
```
Check with `python3 -I src/validate.py data/<author>`. `data/<author>/STATUS.tsv` lists each bundle as
`transcribed` / `partly-read` / `read`.

## Transcript page: `data/<author>/transcripts/<bundle>/cNNN.json`

```json
{
  "canvas": 140,                 "label": "70r",
  "image": "https://images.sub.uni-goettingen.de/iiif/image/gdz:<ID>:00000141/full/1300,/0/default.jpg",
  "model": "claude-opus-5-5",    "stop_reason": "end_turn",   "parsed": true,
  "result": {
    "legibility": "good|fair|poor|blank",
    "rotated": false,
    "topic_en": "one plain-English sentence",
    "transcription": "verbatim, original language; LaTeX in $...$; struck text [-...-]; insertions {+...+}; [?] after uncertain words",
    "methods": [{"what": "...", "quote": "..."}],
    "items": [{"kind": "problem|question|conjecture|plan|claim", "quote": "...", "english": "...", "status_on_page": "solved on page|left open|unclear"}]
  },
  "human_corrected": false
}
```
PDF-sourced pages (`read_source.py`) use `"cote"`/`"page"` instead of `"canvas"`/`"label"` and add `"kind"`
(`math|verso_unrelated|cover|blank|other`).

## Deep read: `data/<author>/deep/<bundle>_cNNN.json`

```json
{
  "bundle": "Math.28", "page": "c010", "label": "7r", "image": "...",
  "deep": {
    "reconstruction": "modern restatement, step by step",
    "errors": ["..."],
    "results": [{"what": "...", "modern_name": "...", "usually_credited_to": "...", "already_credited_to_author": "yes|no|unsure", "routine": false}],
    "surprise": 0,  "surprise_reason": "...",
    "checkable": [{"sympy": "...", "asserts": "..."}],
    "transcription_corrections": ["..."]
  }
}
```
Montpellier deep reads use `"ideas"` and `"missed"` (`unfinished|finished_uncredited|connection|other`) instead of
`"results"`/`"checkable"`.

## Translations: `data/<author>/translations/<bundle>/cNNN.md`
One file per page, same name as the transcript. First line: `<!-- page: <bundle>/<cNNN> | by: human | <model id> | model:<id>+human -->`,
then the translation in the original line order. Original-language transcription stays the source of truth;
translations are a convenience for readers and for agents that search in English.

## Stable page ids
`<library>:<shelfmark>:<folio>` (e.g. `SUB:Cod.Ms.B.Riemann 26:70r`, `UM:cote 136:p011`). Scans are linked, never copied.
