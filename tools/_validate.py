#!/usr/bin/env python3
# Check locales/ru.json against the rules Orca's plugin loader applies in
# strict mode (parsePluginLanguagePackArtifact, Orca v1.4.246):
# entry/depth caps, safe keys, no protected security copy, string policy.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.join(HERE, "..", "locales", "ru.json")
ENGLISH = os.path.join(HERE, "_skeleton_en.json")

sys.path.insert(0, HERE)
import _filter as f

MAX_ENTRIES = 50_000
MAX_DEPTH = 16
MAX_KEY_LEN = 128
MAX_CHARS = 8192
SOURCE_LENGTH_FLOOR = 64
SOURCE_LENGTH_MULTIPLIER = 4
DANGEROUS = {"__proto__", "prototype", "constructor"}
PLURAL = re.compile(r"_(?:zero|one|two|few|many|other)$")
BIDI = re.compile("[\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]")


def flat(obj, path="", out=None):
    out = {} if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            flat(v, f"{path}.{k}" if path else k, out)
    else:
        out[path] = obj
    return out


def english_lookup(en):
    def lookup(path):
        if path in en:
            return en[path]
        base = PLURAL.sub("", path)
        if base == path:
            return None
        return en.get(f"{base}_other", en.get(base))
    return lookup


def string_problem(path, value, lookup):
    for ch in value:
        code = ord(ch)
        if (code <= 0x1F and code != 0x0A) or 0x7F <= code <= 0x9F or code in (0x2028, 0x2029, 0xFEFF):
            return "control or separator character"
    if BIDI.search(value):
        return "bidirectional formatting character"
    source = lookup(path)
    if source is not None and "\n" in value and "\n" not in source:
        return "adds a line break the English text does not have"
    limit = MAX_CHARS if source is None else min(MAX_CHARS, max(SOURCE_LENGTH_FLOOR, SOURCE_LENGTH_MULTIPLIER * len(source)))
    if len(value) > limit:
        return f"exceeds {limit} characters (English source is {len(source) if source else '?'} chars)"
    return None


def main():
    pack = json.load(open(PACK, encoding="utf-8"))
    en = flat(json.load(open(ENGLISH, encoding="utf-8")))
    lookup = english_lookup(en)

    problems = []
    entries = 0

    def walk(node, path, depth):
        nonlocal entries
        if depth > MAX_DEPTH:
            problems.append(f"depth > {MAX_DEPTH} at {path}")
            return
        for key, value in node.items():
            entries += 1
            if entries > MAX_ENTRIES:
                problems.append(f"entries > {MAX_ENTRIES}")
                return
            if not key or len(key) > MAX_KEY_LEN or key in DANGEROUS or "." in key:
                problems.append(f"unsafe key {key!r} under {path or '<root>'}")
                continue
            for ch in key:
                if ord(ch) <= 31:
                    problems.append(f"control character in key {key!r} under {path or '<root>'}")
            child = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                if f.blocked(child) and not f.container_exempt(child):
                    problems.append(f"protected container {child}")
                    continue
                walk(value, child, depth + 1)
            elif isinstance(value, str):
                if f.blocked(child):
                    problems.append(f"protected path {child}")
                    continue
                problem = string_problem(child, value, lookup)
                if problem:
                    problems.append(f"{child}: {problem}")
            else:
                problems.append(f"{child}: value must be a string or object")

    walk(pack, "", 0)
    translated = sum(1 for _ in flat(pack))
    print(f"entries={entries} translated_leaves={translated} limit={MAX_ENTRIES}")
    if problems:
        print(f"FAIL {len(problems)} problem(s):")
        for p in problems[:40]:
            print("  -", p)
        raise SystemExit(1)
    print("OK: pack satisfies Orca v1.4.246 loader rules")


if __name__ == "__main__":
    main()
