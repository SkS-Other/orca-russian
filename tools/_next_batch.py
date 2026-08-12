#!/usr/bin/env python3
# Print the next N untranslated keys (default: auto.* group) so each batch
# can be translated and appended to ru_overrides.json.
import json, sys, os
import _filter as f

HERE = os.path.dirname(os.path.abspath(__file__))

N = int(sys.argv[1]) if len(sys.argv) > 1 else 150
GROUP = sys.argv[2] if len(sys.argv) > 2 else "auto."

d = json.load(open(os.path.join(HERE, "_skeleton_es.json"), encoding="utf-8"))
kept = dict(f.walk(d))
try:
    done = set(json.load(open(os.path.join(HERE, "ru_overrides.json"), encoding="utf-8")).keys())
except FileNotFoundError:
    done = set()

pending = [(p, v) for p, v in kept.items() if p.startswith(GROUP) and p not in done]
print(f"# pending in '{GROUP}': {len(pending)} / showing {min(N, len(pending))}")
for p, v in pending[:N]:
    print(f"{p}||{v}")
