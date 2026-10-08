# Russian language pack for Orca

> 🌍 **Русская версия** → [README.md](README.md)

Russian (ru) localization for the [Orca](https://github.com/stablyai/orca) UI. Untranslated keys fall back to the English source automatically.

## Status

Full coverage of Orca's translatable UI catalog:

- **15,005 / 15,007** translatable strings shipped (99.99%), synced with Orca **v1.4.222**
- Settings, sidebars (source control, checks, ports, file explorer, search, Git history, AI vault), editor (rich Markdown, diff, notebooks, PDF, images, CSV tables), terminal, browser pane, mobile companion app, onboarding, automations, skills, agent session search, native chat, dashboard, application menu, and more
- 2 remaining strings are inline CSS for animated marketing visuals (not prose) and are intentionally dropped — they fall back to the identical English-source CSS, with no user-facing impact

## Installation

### Option 1 — from Git (recommended)

1. Open **Settings → Plugins** and click **Install plugin**.
2. Switch to the **Git URL** tab.
3. Paste the URL:

   ```
   https://github.com/SkS-Other/orca-russian.git#main
   ```

   The part after `#` is a mandatory pin (a tag or commit): Orca fetches exactly that revision. `#main` always points to the latest release; version tags `vX.Y.Z` are cut per Orca release.

4. Click **Install**. Orca fetches the plugin and shows the permissions it requests for review. The language pack requests none — it only ships a translation file. Click **Enable plugin**.
5. Make sure the plugin is enabled in the list on the **Plugins** page.

### Option 2 — from a local folder

1. Clone the repository:

   ```sh
   git clone https://github.com/SkS-Other/orca-russian.git
   ```

2. Open **Settings → Plugins → Install plugin**, the **Local folder** tab.
3. Enter the path to the repository folder (e.g. `/Users/you/projects/orca-russian`) and click **Install**.
4. Click **Enable plugin**.

### Switching the UI to Russian

1. Open **Settings → Appearance**.
2. Pick **Русский** in the **Language** list.

Done — the UI switches to Russian.

### Updating the translation

When a new version ships (a `vX.Y.Z` tag matching the corresponding Orca release), reinstall the plugin with the up-to-date ref, for example:

```
https://github.com/SkS-Other/orca-russian.git#v1.4.222
```

Orca keeps plugin versions side by side, so reinstalling is safe.

> **Why is the plugin id `ru-language-pack` instead of `orca-russian`?**
> Orca reserves plugin ids starting with `orca-` for its own official packages and
> refuses to install such identities from third-party git sources or local folders
> ("reserved plugin identity …"). That is why the repository is named `orca-russian`
> while the plugin id is `ru-language-pack`.

## How this pack was built

The Spanish source catalog (`es.json`) was used as the skeleton, and Russian translations were authored in batches grouped by UI namespace, with an LLM-assisted, multi-pass process:

1. Flatten the Spanish catalog into `path -> string` pairs, excluding keys under the plugin-protected namespace (`auto.components.settings.plugin*`, enforced by Orca's own plugin artifact parser) — except a small allowlist of plugin-chrome strings that are safe to translate.
2. Translate in batches grouped by component/namespace, with a shared style guide: placeholders (`{{value0}}`, `{{count}}`, etc.) preserved verbatim; brand and technical loanwords (`branch`, `commit`, `worktree`, `workspace`, `pull request`, `merge`, `rebase`, `diff`, `check`, `workflow`, etc.) kept untranslated, consistent with how GitHub/GitLab/VS Code are localized for ru.
3. Cross-batch consistency pass: reconciled terminology that drifted between independently translated batches (e.g. «Проверки» vs «Контроль» for the checks tab; «Рабочее пространство» vs «Пространство» for workspace).
4. Validated against the same rules Orca's plugin loader enforces at runtime (`parsePluginLanguagePackArtifact`): max 20,000 entries, max depth 16, no dangerous/unsafe keys, no protected paths, no string over 8,192 chars. The two inline-CSS blobs that exceed the 8,192-char limit are dropped (see [Status](#status)).

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
