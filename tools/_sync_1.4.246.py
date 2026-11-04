#!/usr/bin/env python3
# Sync ru_overrides.json with the 1.4.242 -> 1.4.246 catalog diff:
# apply new translations (reused + freshly translated), refresh changed sources,
# drop removed keys, and keep the "intentionally English" list in sync.
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OV = os.path.join(HERE, "ru_overrides.json")
SKELETON = os.path.join(HERE, "_skeleton_es.json")
SKELETON_EN = os.path.join(HERE, "_skeleton_en.json")
PRESERVED = os.path.join(HERE, "_preserve_english.json")
BATCHES = sorted(glob.glob(os.path.join(HERE, "_batch*_v1.4.246.json")))

sys.path.insert(0, HERE)
import _filter as f

PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}|\{[^}]*\}|<[a-zA-Z/][^>]*>|%[sd]")

# Strings that are literals rather than UI copy (commands, URLs, brand-only
# tokens, placeholder-only formats): they stay English on purpose.
KEEP_ENGLISH = [
    "auto.components.automations.automation.list.last.run.statusWithRelative",
    "auto.components.mobile.slides.HomeSlide.b5308d5e2c",
    "auto.components.rightSidebar.FolderWorkspacePrChecksPanel.worktreeCountLabel_one",
    "auto.components.settings.experimental.search.browserExtensions.chrome",
    "auto.components.status.bar.workspaceSpaceDecision.activeAndCompletedAgents",
    "auto.components.taskSourceContextSummary.hostStatus",
    "settings.appearance.editorTheme.keyword.monaco",
    "settings.appearance.language.chineseTraditional",
    "settings.appearance.language.german",
    "settings.appearance.language.russian",
    "settings.appearance.language.turkish",
    "settings.appearance.reduceVisualEffects.keywords.gpu",
    "settings.browser.extensions.keywordChrome",
    "settings.browser.extensions.sourceWebStore",
    "settings.general.openInMenu.keyword.devin",
    "settings.general.openInMenu.keyword.devinDesktop",
    "settings.general.openInMenu.keyword.windsurf",
    "settings.openInApp.preset.devinDesktop",
    "sidebar.agentSummary.agentIdentityState",
    "sidebar.agentSummary.mixedStates",
    "wslMove.orchestrator.blocker",
]


def flat(obj, path="", out=None):
    out = {} if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            flat(v, f"{path}.{k}" if path else k, out)
    else:
        out[path] = obj
    return out


def check_placeholders(path, source, value):
    expected = sorted(PLACEHOLDER.findall(source))
    actual = sorted(PLACEHOLDER.findall(value))
    if expected != actual:
        raise SystemExit(f"placeholder mismatch at {path}: {expected} != {actual}")


def main():
    ov = json.load(open(OV, encoding="utf-8"))
    raw_es = json.load(open(SKELETON, encoding="utf-8"))
    raw_en = json.load(open(SKELETON_EN, encoding="utf-8"))
    full_source = flat(raw_es)
    full_source.update({p: v for p, v in flat(raw_en).items() if p not in full_source})
    source = dict(f.walk(raw_es))
    source.update({p: v for p, v in f.walk(raw_en) if p not in source})
    before = len(ov)

    blocked_keys = {k for k in ov if f.blocked(k)}
    for key in [k for k in ov if k not in source]:
        del ov[key]
    removed = before - len(ov)

    added = {}
    overridden = 0
    for path in BATCHES:
        for key, value in json.load(open(path, encoding="utf-8")).items():
            if key not in full_source:
                raise SystemExit(f"{os.path.basename(path)}: key not in catalog: {key}")
            if f.blocked(key):
                blocked_keys.add(key)
                continue
            check_placeholders(key, source[key], value)
            if key in added and added[key] != value:
                overridden += 1
            added[key] = value
    if overridden:
        print(f"later batches refined {overridden} earlier translations")

    unknown = [k for k in KEEP_ENGLISH if k not in full_source]
    if unknown:
        raise SystemExit("KEEP_ENGLISH keys not present in the new catalog: " + repr(unknown[:5]))

    ov.update(added)

    previous = json.load(open(PRESERVED, encoding="utf-8"))
    preserved = sorted((set(previous) | set(KEEP_ENGLISH) | blocked_keys) & set(full_source))

    json.dump(ov, open(OV, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
    json.dump(preserved, open(PRESERVED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(
        f"overrides: {before} -> {len(ov)} "
        f"(+{len(added)} from {len(BATCHES)} batches, -{removed} removed); "
        f"preserve_english: {len(previous)} -> {len(preserved)}"
    )


if __name__ == "__main__":
    main()
