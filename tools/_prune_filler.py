#!/usr/bin/env python3
# Drop overrides whose value equals the English fallback. Such an entry changes
# nothing on screen (the runtime renders the same English text) but still counts
# against Orca's 20 000-entry limit for language packs, so it is pure weight.
# The dropped keys are recorded in _preserve_english.json: they are intentionally
# English (brands, commands, code, language names) and must not be re-translated.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EN = os.path.join(HERE, "_skeleton_en.json")
OV = os.path.join(HERE, "ru_overrides.json")
PRESERVED = os.path.join(HERE, "_preserve_english.json")

sys.path.insert(0, HERE)
import _filter as f


def main():
    en = dict(f.walk(json.load(open(EN, encoding="utf-8"))))
    ov = json.load(open(OV, encoding="utf-8"))
    before = len(ov)

    dropped = sorted(k for k, v in ov.items() if en.get(k) == v)
    for key in dropped:
        del ov[key]

    previous = []
    try:
        previous = json.load(open(PRESERVED, encoding="utf-8"))
    except FileNotFoundError:
        pass
    json.dump(
        sorted(set(previous) | set(dropped)),
        open(PRESERVED, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=2,
    )
    json.dump(ov, open(OV, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
    print(f"overrides: {before} -> {len(ov)} (dropped {len(dropped)} entries identical to English)")


if __name__ == "__main__":
    main()
