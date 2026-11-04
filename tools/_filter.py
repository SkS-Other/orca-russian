import json, sys, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
SKELETON = os.path.join(HERE, "_skeleton_es.json")
DANGEROUS = {"__proto__", "prototype", "constructor"}

PROTECTED_ROOT = "auto.components.settings."
PROTECTED_MODULE = re.compile(r"^plugin", re.I)

# Allowlist of translatable plugin-chrome paths (must match the host exactly).
TRANSLATABLE_CHROME = {
    "auto.components.settings.PluginsSettingsSection.title",
    "auto.components.settings.PluginsSettingsSection.systemLabel",
    "auto.components.settings.PluginsSettingsSection.install",
    "auto.components.settings.PluginsSettingsSection.loading",
    "auto.components.settings.PluginsSettingsSection.empty",
    "auto.components.settings.PluginsSettingsSection.emptyTitle",
    "auto.components.settings.PluginsSettingsSection.noInstalledResults",
    "auto.components.settings.PluginsSettingsSection.noInstalledResultsTitle",
    "auto.components.settings.PluginMarketplaceBrowser.manageSources",
    "auto.components.settings.PluginMarketplaceBrowser.addSource",
    "auto.components.settings.PluginMarketplaceBrowser.refresh",
    "auto.components.settings.PluginMarketplaceBrowser.refreshing",
    "auto.components.settings.PluginMarketplaceBrowser.loading",
    "auto.components.settings.PluginMarketplaceBrowser.tryAgain",
    "auto.components.settings.PluginMarketplaceBrowser.clearSearch",
    "auto.components.settings.PluginMarketplaceBrowser.empty",
    "auto.components.settings.PluginMarketplaceBrowser.emptyTitle",
    "auto.components.settings.PluginMarketplaceBrowser.noInstalled",
    "auto.components.settings.PluginMarketplaceBrowser.noInstalledTitle",
    "auto.components.settings.PluginMarketplaceBrowser.noResults",
    "auto.components.settings.PluginMarketplaceBrowser.noResultsTitle",
    "auto.components.settings.PluginMarketplaceBrowser.noSourcesTitle",
    "auto.components.settings.PluginDevelopmentSection.title",
    "auto.components.settings.PluginDevelopmentSection.add",
    "auto.components.settings.PluginDevelopmentSection.remove",
    "auto.components.settings.PluginDevelopmentSection.pathLabel",
    "auto.components.settings.PluginDevelopmentSection.pathRequired",
    "auto.components.settings.PluginDevelopmentSection.placeholder",
    "auto.components.settings.plugins.search.title",
    "auto.components.settings.plugins.search.description",
    "auto.components.settings.plugins.search.install",
    "auto.components.settings.plugins.search.permissions",
    "auto.components.settings.plugins.search.logs",
    "auto.components.settings.plugins.search.development",
}

def protected(path):
    if not path.startswith(PROTECTED_ROOT):
        return False
    if path in TRANSLATABLE_CHROME:
        return False
    rest = path[len(PROTECTED_ROOT):]
    return bool(PROTECTED_MODULE.match(rest))

# Security and destructive-confirmation copy: the host ignores pack entries for
# these paths (`isProtectedCopyPath`), so shipping them only wastes the entry
# budget. Snapshot of protected-copy-keys.json, see the file's `source` field.
PROTECTED_COPY_FILE = os.path.join(HERE, "_protected_copy.json")
PLURAL_SUFFIX = re.compile(r"_(?:zero|one|two|few|many|other)$")
try:
    _protected_copy = json.load(open(PROTECTED_COPY_FILE, encoding="utf-8"))
    PROTECTED_COPY_KEYS = frozenset(_protected_copy["keys"])
    PROTECTED_COPY_PREFIXES = tuple(_protected_copy["prefixes"])
except FileNotFoundError:
    PROTECTED_COPY_KEYS = frozenset()
    PROTECTED_COPY_PREFIXES = ()

def protected_copy(path):
    if any(path.startswith(prefix) for prefix in PROTECTED_COPY_PREFIXES):
        return True
    candidate = path
    while candidate:
        if candidate in PROTECTED_COPY_KEYS:
            return True
        if PLURAL_SUFFIX.sub("", candidate) in PROTECTED_COPY_KEYS:
            return True
        parent = candidate.rfind(".")
        candidate = "" if parent == -1 else candidate[:parent]
    return False

def blocked(path):
    return protected(path) or protected_copy(path)

# A container is walkable only if an allowlist leaf sits below it.
def container_exempt(path):
    prefix = path + "."
    return any(c.startswith(prefix) for c in TRANSLATABLE_CHROME)

def walk(obj, path=""):
    """Yield (path, value). Drop protected non-allowlist leaves/containers."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if protected(p):
                # Protected leaf or container: skip entirely, unless it is a
                # container holding allowlist chrome (then descend).
                if isinstance(v, dict) and container_exempt(p):
                    yield from walk(v, p)
                else:
                    continue
            elif protected_copy(p):
                continue
            else:
                yield from walk(v, p)
    else:
        yield path, obj

def main():
    d = json.load(open(SKELETON, encoding="utf-8"))
    kept = list(walk(d))
    from collections import Counter
    top = Counter()
    for p, _ in kept:
        top[p.split(".")[0]] += 1
    for k, v in top.most_common():
        print(f"{v:6d}  {k}")
    print("TOTAL kept", len(kept))
    print("DROPPED (protected non-allowlist)", sum(1 for _,_ in [("__",d)] and []) )
    # also report protected dropped count
    dropped = 0
    def count_all(obj, path=""):
        nonlocal dropped
        if isinstance(obj, dict):
            for k, v in obj.items():
                p = f"{path}.{k}" if path else k
                if protected(p) and not (isinstance(v, dict) and container_exempt(p)):
                    def n(o):
                        if isinstance(o,dict): return sum(n(x) for x in o.values())
                        return 1
                    dropped += n(v)
                else:
                    if isinstance(v, dict) and container_exempt(p):
                        count_all(v, p)
                    elif isinstance(v, dict):
                        count_all(v, p)
                    else:
                        pass
        else:
            pass
    count_all(d)
    print("DROPPED leaves (protected)", dropped)

if __name__ == "__main__":
    main()
