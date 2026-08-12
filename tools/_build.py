#!/usr/bin/env python3
# Build ru.json from the es.json skeleton + ru_overrides.json translations.
# Drops protected non-allowlist paths (else the host rejects the whole pack).
import json, sys, os
import _filter as f

HERE = os.path.dirname(os.path.abspath(__file__))
SKELETON = os.path.join(HERE, "_skeleton_es.json")
OVERRIDES = os.path.join(HERE, "ru_overrides.json")
OUT = os.path.join(HERE, "..", "locales", "ru.json")

MAX_STR = 8192

def set_nested(root, dotted, value):
    parts = dotted.split(".")
    node = root
    for p in parts[:-1]:
        node = node.setdefault(p, {})
        if not isinstance(node, dict):
            raise SystemExit(f"conflict at {dotted}: {p} is not an object")
    node[parts[-1]] = value

def main():
    skel = json.load(open(SKELETON, encoding="utf-8"))
    kept = dict(f.walk(skel))  # path -> source value
    overrides = {}
    try:
        overrides = json.load(open(OVERRIDES, encoding="utf-8"))
    except FileNotFoundError:
        pass

    ru = {}
    missing = 0
    translated = 0
    skipped_too_long = 0
    for path, src in kept.items():
        if path in overrides:
            val = overrides[path]
            if not isinstance(val, str) or val == "":
                # empty => leave source (English fallback)
                continue
            if len(val) > MAX_STR:
                # Host loader rejects strings over 8192 chars. These are
                # inline CSS for animated marketing visuals, not prose;
                # dropping them falls back to the identical English-source CSS.
                skipped_too_long += 1
                continue
            set_nested(ru, path, val)
            translated += 1
        else:
            missing += 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(ru, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"translated={translated} missing(untranslated->en fallback)={missing} skipped_too_long(>{MAX_STR})={skipped_too_long} total_kept={len(kept)} -> {OUT}")

if __name__ == "__main__":
    main()
