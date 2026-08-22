# orca-russian

Russian (ru) language pack for [Orca](https://github.com/stablyai/orca).

## Status

Full coverage of Orca's translatable UI catalog:

- **11,650 / 11,652** translatable strings shipped (99.98%), synced with Orca **v1.4.188**
- Settings, sidebars (source control, checks, ports, file explorer, search, Git history, AI vault), editor (rich Markdown, diff, notebooks, PDF, images), terminal, browser pane, mobile companion app, onboarding, feature wall, automations, dashboard, emulator pane, crash reporting, and application menu
- 2 remaining strings are inline CSS for animated marketing visuals (not prose) and are intentionally dropped — they fall back to the identical English-source CSS, with no user-facing impact

## Installation

Orca discovers language packs through its plugin system. Two ways to install:

- **From git:** Settings → Plugins → Install → Git, point Orca at `https://github.com/SkS-Other/orca-russian.git`
- **From a local checkout:** Settings → Plugins → Development, add the folder path

Then select **Русский — orca-russian** from Settings → Appearance → Language.

## How this pack was built

The Spanish source catalog (`es.json`) was used as the skeleton, and Russian translations were authored in batches grouped by UI namespace, with an LLM-assisted, multi-pass process:

1.  Flatten the Spanish catalog into `path -> string` pairs, excluding keys under the plugin-protected namespace (`auto.components.settings.plugin*`, enforced by Orca's own plugin artifact parser) — except a small allowlist of plugin-chrome strings that are safe to translate.
2.  Translate in batches grouped by component/namespace, with a shared style guide: placeholders (`{{value0}}`, `{{count}}`, etc.) preserved verbatim; brand and technical loanwords (`branch`, `commit`, `worktree`, `workspace`, `pull request`, `merge`, `rebase`, `diff`, `check`, `workflow`, etc.) kept untranslated, consistent with how GitHub/GitLab/VS Code are localized for ru.
3.  Cross-batch consistency pass: reconciled terminology that drifted between independently translated batches (e.g. "Проверки" vs "Контроль" for the checks tab; "Рабочее пространство" vs "Пространство" for workspace).
4.  Validated against the same rules Orca's plugin loader enforces at runtime (`parsePluginLanguagePackArtifact`): max 20,000 entries, max depth 16, no dangerous/unsafe keys, no protected paths, no string over 8,192 chars. The two inline-CSS blobs that exceed the 8,192-char limit are dropped (see [Status](#status)).

## Repo layout

```
orca-russian/
├── orca-plugin.json        # plugin manifest
├── locales/ru.json         # the shipped language pack (sparse catalog)
└── tools/                  # authoring scaffolding (not shipped)
    ├── _skeleton_es.json   # Spanish source catalog (path -> string)
    ├── ru_overrides.json   # Russian translations (path -> string)
    ├── _build.py           # builds locales/ru.json from skeleton + overrides
    ├── _filter.py          # walks the skeleton, drops protected paths
    ├── _next_batch.py      # prints the next N untranslated keys
    └── _batch*.json        # per-batch translation snapshots (history)
```

Rebuild the pack after editing `ru_overrides.json`:

```sh
cd tools && python3 _build.py
```

## Contributing

Corrections and improvements welcome — please open a PR, keeping the existing key structure and the style conventions above. Edit `tools/ru_overrides.json`, then rebuild with `cd tools && python3 _build.py` and commit the regenerated `locales/ru.json`.
