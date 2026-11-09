#!/usr/bin/env python3
"""
pdf_ask.py - ask one targeted question about a PDF given BY URL (the file is fetched by the API, not here).

    python3 -E -P src/pdf_ask.py <pdf_url> "<question>" [--effort medium]
"""
import argparse
import pathlib

import anthropic

MODEL = "claude-opus-5-5"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("question")
    ap.add_argument("--effort", default="medium")
    a = ap.parse_args()
    key = pathlib.Path.home().joinpath(".config/hunt/anthropic_key").read_text().strip()
    client = anthropic.Anthropic(api_key=key, max_retries=2, timeout=1200)
    content = [{"type": "document", "source": {"type": "url", "url": a.url}},
               {"type": "text", "text": a.question + "\n\nAnswer with page references and verbatim quotes; say 'not found' "
                                        "if the document does not contain it. Do not guess."}]
    r = client.messages.create(model=MODEL, max_tokens=8000, messages=[{"role": "user", "content": content}],
                               extra_body={"output_config": {"effort": a.effort}})
    print("".join(b.text for b in r.content if getattr(b, "type", "") == "text"))
    print(f"\n[tokens in={r.usage.input_tokens} out={r.usage.output_tokens}]")


if __name__ == "__main__":
    main()
