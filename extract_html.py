#!/usr/bin/env python3
"""Extract HTML from Claude API JSON response, removing markdown code fences."""
import sys
import json
import re

raw = sys.stdin.read()
resp = json.loads(raw)

if "error" in resp:
    print(f"API Error: {resp['error']}", file=sys.stderr)
    sys.exit(1)

text = resp["content"][0]["text"]

# Remove leading ```html or ```
text = re.sub(r"^\s*```(?:html)?\s*\n?", "", text)
# Remove trailing ```
text = re.sub(r"\n?\s*```\s*$", "", text)

text = text.strip()

if "<!DOCTYPE" not in text and "<html" not in text:
    print("No valid HTML found in response", file=sys.stderr)
    print(text[:200], file=sys.stderr)
    sys.exit(1)

print(text)
