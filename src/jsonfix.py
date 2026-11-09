"""Lenient JSON extraction for model outputs that contain LaTeX (backslashes) inside strings."""
import json
import re

_VALID = set('"\\/bfnrtu')


def _repair(s):
    out = []
    i, n = 0, len(s)
    while i < n:
        if s[i] != "\\":
            out.append(s[i])
            i += 1
            continue
        j = i
        while j < n and s[j] == "\\":
            j += 1
        run = j - i
        nxt = s[j] if j < n else ""
        # an odd run leaves one unpaired backslash that escapes `nxt`
        if run % 2 == 1:
            bad = False
            if nxt == "" or nxt not in _VALID:
                bad = True
            elif nxt == "u" and not re.match(r"[0-9a-fA-F]{4}", s[j + 1:j + 5]):
                bad = True            # \underline, \upsilon ...
            elif nxt in "bfrt" and j + 1 < n and s[j + 1].isalpha():
                bad = True            # \beta \frac \rho \times ... (control chars never precede letters)
            if bad:
                run += 1
        out.append("\\" * run)
        i = j
    return "".join(out)


def lenient_json(text):
    """Return the first {...} object in text parsed as JSON, repairing bad escapes; None if hopeless."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    raw = m.group(0)
    for cand in (raw, _repair(raw), re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", _repair(raw))):
        try:
            return json.loads(cand)
        except json.JSONDecodeError:
            continue
    return None
