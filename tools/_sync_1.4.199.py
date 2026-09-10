#!/usr/bin/env python3
# Sync ru_overrides.json with the 1.4.190 -> 1.4.199 es-catalog diff:
# apply new translations, refresh changed sources, drop removed keys.
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OV = os.path.join(HERE, "ru_overrides.json")
TMP = "/private/var/folders/qn/hjwpy1892091h8r2_lwhcg400000gn/T/opencode"

ADDED = {
    "settings.appearance.language.french": "Français",

    "auto.store.slices.worktrees.createdWithoutParentNesting": 'Создано без вложения в "{{value0}}"',
    "auto.store.slices.worktrees.createdWithoutParentNestingUnnamed": "Создано без вложения в выбранный родительский worktree",
    "auto.store.slices.worktrees.createdWithoutParentNestingDetail": "Родительское рабочее пространство было недоступно. Его можно задать в меню рабочего пространства.",

    "auto.components.terminal.pane.TerminalErrorToast.remoteTerminalClosed": "Удалённый терминал был закрыт.",
    "auto.components.tab.bar.TabBarCreateEntry.omniboxPlaceholderWithHistory": "Поиск открытых вкладок, истории, файлов, URL и агентов…",
    "auto.components.tab.bar.TabBarCreateEntry.openPage": "Открыть страницу",

    "auto.components.status.bar.CaffeinateStatusSegment.active": "Активен",
    "auto.components.status.bar.CaffeinateStatusSegment.inactive": "Неактивен",
    "auto.components.status.bar.CaffeinateStatusSegment.ariaLabel": "{{title}}, {{status}}",
    "auto.components.status.bar.CaffeinateStatusSegment.onDescription": "Не давать этому компьютеру засыпать никогда",
    "auto.components.status.bar.CaffeinateStatusSegment.autoDescription": "Не давать компьютеру засыпать, пока работает агент",
    "auto.components.status.bar.CaffeinateStatusSegment.offDescription": "Разрешить системе уходить в сон как обычно",
    "auto.components.status.bar.resource.memory.metric.privateBytesDescription": "Сумма частных байт (private bytes): память, выделенная этими процессами, — учитывается и резидентная, и выгруженная на диск. Именно её хост засчитывает в лимит выделенной памяти, поэтому показатель продолжает расти, даже когда рабочий набор выше сокращается за счёт выгрузки.",

    "auto.components.skills.SkillsPage.cb142070b4": "Обновить",
    "auto.components.skills.SkillsPage.a68dee6a32": "Поиск навыков",
    "auto.components.skills.SkillsPage.f43ad6edf3": "Навыки",
    "auto.components.skills.SkillsPage.ea72d6185b": "Не удалось разобрать навыки",
    "auto.components.skills.SkillsPage.dc4c3328ee": "Показать файл",
    "auto.components.skills.SkillsPage.9963dff6d3": "Описание не найдено.",
    "auto.components.skills.SkillsPage.995fde8337": "Не удалось показать файл навыка",
    "auto.components.skills.SkillsPage.4acd6d68ec": "Навыки не найдены",
    "auto.components.skills.SkillsPage.6a62a0168c": "Нет совпадений",
    "auto.components.skills.SkillsPage.08a321a984": "Ни один навык не соответствует текущему поиску и фильтрам.",
    "auto.components.skills.SkillsPage.cd7893fbc1": "Разбор навыков",
    "auto.components.skills.SkillsPage.35b9a724a0": "Доступен",
    "auto.components.skills.SkillsPage.c13b82793c": "Управление установками",
    "auto.components.skills.SkillsPage.aee7b99cc6": "Установить по ссылке",
    "auto.components.skills.SkillsPage.filterProvider": "Фильтр по агенту",
    "auto.components.skills.SkillsPage.filterSource": "Фильтр по источнику",
    "auto.components.skills.SkillsPage.allSources": "Все",
    "auto.components.skills.SkillsPage.clearFilters": "Сбросить фильтры",
    "auto.components.skills.SkillsPage.closeSkills": "Закрыть навыки",
    "auto.components.skills.SkillsPage.closeTooltip": "Закрыть · Esc",
    "auto.components.skills.SkillsPage.moreActions": "Ещё действия",
    "auto.components.skills.SkillsPage.sharedLinks": "Общие ссылки",
    "auto.components.skills.SkillsPage.emptyCopy": "Разобранные папки навыков пусты. Установите общий пакет или обновите страницу после добавления навыка.",
    "auto.components.skills.SkillsPage.retry": "Повторить",
    "auto.components.skills.SkillsPage.remoteShareNotice": "Эти навыки находятся на {{host}}. Откройте «Навыки» на той машине, чтобы поделиться ими.",
    "auto.components.skills.SkillsPage.viewSwitch": "Показать",
    "auto.components.skills.SkillsPage.searchLinks": "Поиск ссылок",
    "auto.components.skills.SkillsPage.deleteSkills": "Удалить навыки…",

    "auto.components.skills.SkillShareSelectionControls.01c5a15e02": "Поделиться навыками",

    "auto.components.skills.SkillRow.updatedUnknown": "Без даты",
    "auto.components.skills.SkillRow.pathCopied": "Путь скопирован",
    "auto.components.skills.SkillRow.copyPath": "Копировать путь",
    "auto.components.skills.SkillRow.detailPath": "Путь",
    "auto.components.skills.SkillRow.skillActions": "Действия для {{value0}}",
    "auto.components.skills.SkillRow.viewDetails": "Подробнее",
    "auto.components.skills.SkillRow.deleteSkill": "Удалить…",

    "auto.components.skills.SkillsList.listLabel": "Навыки",

    "auto.components.skills.sourceStatus.missing": "Папка не найдена",
    "auto.components.skills.sourceStatus.remoteRepo": "Удалённый репозиторий — не разобран",
    "auto.components.skills.sourceStatus.unavailable": "Не разобрано",
    "auto.components.skills.sources.heading": "Папки навыков",

    "auto.components.skills.sourceKind.home": "Домашняя",
    "auto.components.skills.sourceKind.workspace": "Рабочее пространство",
    "auto.components.skills.sourceKind.bundled": "Встроенная",
    "auto.components.skills.sourceKind.plugin": "Плагин",

    "auto.components.skills.count.skillOne": "{{count}} навык",
    "auto.components.skills.count.skillOther": "{{count}} навыков",
    "auto.components.skills.count.sourceOne": "{{count}} источник",
    "auto.components.skills.count.sourceOther": "{{count}} источников",
    "auto.components.skills.count.fileOne": "{{count}} файл",
    "auto.components.skills.count.fileOther": "{{count}} файлов",
    "auto.components.skills.count.resultOne": "{{count}} результат",
    "auto.components.skills.count.resultOther": "{{count}} результатов",
    "auto.components.skills.count.selected": "Выбрано: {{count}}",
    "auto.components.skills.count.shareOne": "Поделиться {{count}} навыком",
    "auto.components.skills.count.shareOther": "Поделиться {{count}} навыками",
    "auto.components.skills.count.linkOne": "{{count}} ссылка",
    "auto.components.skills.count.linkOther": "{{count}} ссылок",

    "auto.components.skills.filter.allAgents": "Все агенты",
    "auto.components.skills.filter.sharedAgent": "Общий (.agents)",

    "auto.components.skills.SkillsSelectionHeader.exit": "Выйти из режима выбора",
    "auto.components.skills.SkillsSelectionHeader.exitTooltip": "Выйти из режима выбора · Esc",
    "auto.components.skills.SkillsSelectionHeader.title": "Выберите навыки, чтобы поделиться",
    "auto.components.skills.SkillsSelectionHeader.selectAll": "Выбрать все {{count}} подходящих",
    "auto.components.skills.SkillsSelectionHeader.clear": "Сбросить",
    "auto.components.skills.SkillsSelectionHeader.deleteTitle": "Выберите навыки для удаления",

    "auto.components.skills.SkillDetailDialog.agents": "Агенты",
    "auto.components.skills.SkillDetailDialog.updated": "Обновлено",
    "auto.components.skills.SkillDetailDialog.copy": "Копировать",

    "auto.components.skills.host.local": "Этот компьютер",
    "auto.components.skills.host.remote": "Подключённая среда",

    "auto.components.sidebar.SidebarHeader.projects": "Проекты",
    "auto.components.sidebar.SidebarHeader.spaces": "Пространства",
    "auto.components.sidebar.SidebarHeader.views": "Вид боковой панели",
    "auto.components.sidebar.SidebarHeader.addProject": "Добавить проект",

    "auto.components.settings.HiddenExperimentalGroup.7c4e18d2f6": "Включает жесты захвата сбоев Bold на этой машине: {{samplingShortcut}} запускает всплеск сэмплирования; {{captureShortcut}} сохраняет данные с панели на диск.",
    "auto.components.settings.HiddenExperimentalGroup.b09f24a51d": "Диагностика рендеринга терминала",
    "auto.components.settings.HiddenExperimentalGroup.f2c81d904a": "Скрытые экспериментальные настройки",

    "auto.components.settings.experimental.search.agentDashboard.dashboard": "панель",

    "auto.components.settings.agent-awake-copy.modeTitle": "Не давать компьютеру засыпать",
    "auto.components.settings.AgentAwakeSetting.on": "Включено",
    "auto.components.settings.AgentAwakeSetting.auto": "Агент",
    "auto.components.settings.AgentAwakeSetting.off": "Выключено",

    "auto.components.right.sidebar.SourceControl.branchFilesChangedVsBaseOne": "1 файл изменён относительно {{ref}}",
    "auto.components.right.sidebar.SourceControl.branchFilesChangedVsBaseOther": "{{count}} файлов изменено относительно {{ref}}",
    "auto.components.right.sidebar.SourceControl.compareBaseCommitsAheadOne": "1 коммит впереди {{ref}}",
    "auto.components.right.sidebar.SourceControl.compareBaseCommitsAheadOther": "{{count}} коммитов впереди {{ref}}",
    "auto.components.right.sidebar.SourceControl.compareBaseCommitsBehindOne": "1 коммит позади {{ref}}",
    "auto.components.right.sidebar.SourceControl.compareBaseCommitsBehindOther": "{{count}} коммитов позади {{ref}}",

    "auto.components.editor.CombinedDiffViewer.skippedConflictsExcluded": "Из этого diff-вида исключено {{count}} неразрешённых конфликтов.",
    "auto.components.editor.CombinedDiffViewer.skippedConflictsExcluded_one": "Из этого diff-вида исключён {{count}} неразрешённый конфликт.",
    "auto.components.editor.CombinedDiffViewer.skippedConflictsExcluded_other": "Из этого diff-вида исключено {{count}} неразрешённых конфликтов.",

    "auto.components.automations.AutomationListToolbar.runs": "Запуски",
    "auto.components.automations.AutomationRunsDashboard.search": "Поиск запусков…",
    "auto.components.automations.AutomationRunsDashboard.filters": "Фильтры",
    "auto.components.automations.AutomationRunsDashboard.host": "Хост",
    "auto.components.automations.AutomationRunsDashboard.status": "Статус",
    "auto.components.automations.AutomationRunsDashboard.refresh": "Обновить запуски",
    "auto.components.automations.AutomationRunsDashboard.successful24h": "Успешные · 24 ч",
    "auto.components.automations.AutomationRunsDashboard.failed24h": "Неудачные · 24 ч",
    "auto.components.automations.AutomationRunsDashboard.successful7d": "Успешные · 7 дней",
    "auto.components.automations.AutomationRunsDashboard.failed7d": "Неудачные · 7 дней",
    "auto.components.automations.AutomationRunsDashboard.historyUnavailableOne": "История запусков недоступна для 1 автоматизации. В подсчётах учитывается только доступная история.",
    "auto.components.automations.AutomationRunsDashboard.historyUnavailableMany": "История запусков недоступна для {{count}} автоматизаций. В подсчётах учитывается только доступная история.",
    "auto.components.automations.AutomationRunsDashboard.automation": "Автоматизация",
    "auto.components.automations.AutomationRunsDashboard.triggered": "Запущена",
    "auto.components.automations.AutomationRunsDashboard.trigger": "Запустить",
    "auto.components.automations.AutomationRunsDashboard.loading": "Загрузка запусков…",
    "auto.components.automations.AutomationRunsDashboard.noRuns": "Запусков пока нет",
    "auto.components.automations.AutomationRunsDashboard.emptyDescription": "Запуски появятся здесь после запуска автоматизации.",
    "auto.components.automations.AutomationRunsDashboard.runs": "Запуски",
    "auto.components.automations.AutomationRunsDashboard.local": "Локальный",
    "auto.components.automations.AutomationRunsDashboard.remote": "Удалённый",

    "auto.components.automations.AutomationsPageBreadcrumb.ariaLabel": "Навигационная цепочка автоматизаций",
    "auto.components.automations.AutomationsPageBreadcrumb.runDetails": "Детали запуска",

    "auto.components.automations.AutomationPromptDisclosure.showLess": "Свернуть",
    "auto.components.automations.AutomationPromptDisclosure.showMore": "Показать больше",

    "auto.components.automations.AutomationDetail.host": "Хост",

    "auto.components.automations.AutomationsPage.moved": "Автоматизация перемещена на {host}.",
    "auto.components.automations.AutomationsPage.moveOriginalKept": "Создано на {host}, но не удалось удалить оригинал. Удалите его на прежнем хосте.",
    "auto.components.automations.AutomationsPage.moveOriginalUnverified": "Создано на {host}, но не удалось проверить удаление оригинала. Проверьте прежний хост, прежде чем повторять попытку.",
    "auto.components.automations.AutomationsPage.tableHost": "Хост",

    "auto.components.automations.createDestination.label": "Хост",
    "auto.components.automations.createDestination.placeholder": "Выберите хост",
    "auto.components.automations.createDestination.storedOn": "Хранится и планируется: {authority}.",
    "auto.components.automations.createDestination.unselected": "Выберите хост, на котором будут храниться и запускаться по расписанию эта автоматизация.",
    "auto.components.automations.createDestination.orphan": "Автоматизации без хоста не могут размещать новые. Выберите хост, на котором создать эту автоматизацию.",
    "auto.components.automations.createDestination.unavailable": "Этот хост пока не может размещать новую автоматизацию. Выберите другой хост.",
    "auto.components.automations.createDestination.stale": "{host} изменился, пока форма была открыта. Выберите его заново перед сохранением.",
    "auto.components.automations.createDestination.projectMismatch": "Этого проекта нет на {host}. Выберите проект на этом хосте или другой хост.",
    "auto.components.automations.createDestination.noProjects": "На {host} нет настроенных проектов. Добавьте проект там или выберите другой хост.",
    "auto.components.automations.createDestination.updateRequired": "Обновите сервер Orca на {hosts}, чтобы хранить автоматизации там.",
    "auto.components.automations.createDestination.move": "При сохранении эта автоматизация будет создана на {host}, а оригинал и история его запусков будут удалены.",

    "auto.components.activity.ActivityPrototypePage.threadListOptionsFiltered": "Настройки списка тредов, фильтры активны",
    "auto.components.activity.ActivityPrototypePage.showSearch": "Показать поиск",
    "auto.components.activity.ActivityPrototypePage.markThreadRead": "Отметить тред прочитанным",
    "auto.components.activity.ActivityPrototypePage.clearCompleted": "Очистить завершённые",
    "auto.components.activity.ActivityPrototypePage.none": "Нет",
    "auto.components.activity.ActivityPrototypePage.search": "Поиск",
    "auto.components.activity.ActivityPrototypePage.showUnreadOnly": "Только непрочитанные",
    "auto.components.activity.ActivityPrototypePage.showChildAgents": "Показывать дочерних агентов",
    "auto.components.activity.ActivityPrototypePage.activityOptions": "Настройки активности",
    "auto.components.activity.ActivityPrototypePage.interrupted": "Прерван",
    "auto.components.activity.ActivityPrototypePage.state.working": "Работает",
    "auto.components.activity.ActivityPrototypePage.state.monitoring": "Следит за фоновыми задачами",
    "auto.components.activity.ActivityPrototypePage.state.blocked": "Заблокирован",
    "auto.components.activity.ActivityPrototypePage.state.waiting": "Ожидает ввода",
    "auto.components.activity.ActivityPrototypePage.state.failed": "Сбой",
    "auto.components.activity.ActivityPrototypePage.state.done": "Завершено",
    "auto.components.activity.ActivityPrototypePage.state.idle": "Бездействует",
    "auto.components.activity.ActivityPrototypePage.state.unverifiable": "Нет недавних обновлений",
    "auto.components.activity.ActivityPrototypePage.state.permission": "Требует внимания",
    "auto.components.activity.ActivityPrototypePage.filtersSection": "Фильтры",
    "auto.components.activity.ActivityPrototypePage.viewSection": "Вид",

    "auto.components.activity.ActivityScopeFilterControls.resetScope": "Показать все хосты и проекты",
    "auto.components.activity.ActivityThreadRow.clearNotification": "Убрать уведомление",

    "auto.components.ComposerParentWorktreePicker.label": "Родительский worktree",
    "auto.components.ComposerParentWorktreePicker.noParent": "Без родительского worktree",
    "auto.components.ComposerParentWorktreePicker.description": "Вкладывает это рабочее пространство в другое в боковой панели. Базовую ветку не меняет.",
    "auto.components.ComposerParentWorktreePicker.searchPlaceholder": "Поиск рабочих пространств...",
    "auto.components.ComposerParentWorktreePicker.noMatches": "Нет совпадений.",

    "components.terminalPane.TerminalContextMenu.copySessionId": "Копировать ID сеанса",
    "components.terminalPane.TerminalContextMenu.copySessionIdSuccess": "ID сеанса скопирован",
    "components.terminalPane.TerminalContextMenu.copySessionIdError": "Не удалось скопировать ID сеанса",

    "dashboard.sidebar.dashboardLabel": "Панель агентов",
    "dashboard.sidebar.openActivity": "Открыть активность",
    "dashboard.sidebar.closeActivity": "Закрыть просмотр активности",
    "dashboard.sidebar.projects": "Проекты",
    "dashboard.sidebar.workspaces": "Рабочие пространства",

    "agentsSidebarIntro.migrated.title": "Агентов стало проще находить",
    "agentsSidebarIntro.migrated.description": "Ваш просмотр «Агенты» теперь отдельная вкладка боковой панели. Активность и фильтры сохранены.",
    "agentsSidebarIntro.migrated.dismiss": "Понятно",
    "agentsSidebarIntro.migrated.action": "Открыть «Агенты»",
    "agentsSidebarIntro.new.title": "Знакомьтесь: вкладка «Агенты»",
    "agentsSidebarIntro.new.description": "Смотрите, чем заняты ваши агенты, что уже готово и где нужно ваше вмешательство.",
    "agentsSidebarIntro.new.hide": "Скрыть «Агенты»",
    "agentsSidebarIntro.new.action": "Попробовать «Агенты»",
    "agentsSidebarIntro.new.hiddenToast": "Вкладка «Агенты» скрыта. Включить её снова можно в Настройки → Experimental.",
}

CHANGED = {
    "auto.components.Terminal.7958465754": "Есть терминалы с запущенными процессами. Закрыть окно всё равно?",
    "auto.components.terminal.pane.TerminalRemoteRuntimeReconnectBanner.retryingBody": "Orca повторяет попытку автоматически. Этот терминал возобновится, если соединение вернётся.",
    "auto.components.status.bar.resource.memory.metric.workingSetDescription": "Сумма рабочего набора (WS): страницы, находящиеся в RAM прямо сейчас. Общие страницы могут отображаться в нескольких процессах, а память, которую Windows выгрузил на диск, здесь не учитывается.",
    "auto.components.activity.ActivityPrototypePage.770d458144": "Группировать по",
    "dashboard.sidebar.label": "Агенты",
}

REMOVED = [
    "auto.components.tab.bar.TabBarCreateEntry.0e5b7a3f16",
    "auto.components.tab.bar.tab.create.entry.classifier.c41f8d20b7",
    "auto.components.sidebar.SidebarHeader.ca6f729da2",
    "auto.components.sidebar.SidebarHeader.25a95899c9",
    "auto.components.settings.HiddenExperimentalGroup.d0f914a528",
    "auto.components.settings.HiddenExperimentalGroup.1014ddbfaf",
    "auto.components.settings.HiddenExperimentalGroup.232cf83de8",
    "auto.components.settings.HiddenExperimentalGroup.3e9e827ca5",
    "auto.components.right.sidebar.SourceControl.f9b2441bb6",
    "auto.components.right.sidebar.SourceControl.b715ef615b",
    "auto.components.right.sidebar.SourceControl.c1a8f3e204",
    "auto.components.right.sidebar.SourceControl.d2b9g4f315",
    "auto.components.right.sidebar.SourceControl.createPrIntentEmptyGeneratedBody",
    "auto.components.editor.CombinedDiffViewer.39e73e7181",
    "auto.components.editor.CombinedDiffViewer.689b99f8ad",
]

def main():
    ov = json.load(open(OV, encoding="utf-8"))
    before = len(ov)
    for k in REMOVED:
        ov.pop(k, None)
    removed = before - len(ov)
    # sanity: every added key must exist in the new es catalog
    new_es = json.load(open(f"{TMP}/es-1.4.199.json", encoding="utf-8"))
    def flat(o, p=""):
        out = {}
        if isinstance(o, dict):
            for k, v in o.items():
                out.update(flat(v, f"{p}.{k}" if p else k))
        else:
            out[p] = o
        return out
    new_flat = flat(new_es)
    missing_in_src = [k for k in ADDED if k not in new_flat]
    if missing_in_src:
        raise SystemExit("ADDED keys not present in new es catalog: " + repr(missing_in_src[:5]))
    ov.update(ADDED)
    ov.update(CHANGED)
    json.dump(ov, open(OV, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
    print(f"overrides: {before} -> {len(ov)} (+{len(ADDED)} added, {len(CHANGED)} changed, -{removed} removed)")

if __name__ == "__main__":
    main()
