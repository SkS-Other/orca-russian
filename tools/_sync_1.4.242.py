#!/usr/bin/env python3
# Sync ru_overrides.json with the 1.4.222 -> 1.4.242 catalog diff:
# apply new translations, refresh changed sources, drop removed keys.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OV = os.path.join(HERE, "ru_overrides.json")
SKELETON = os.path.join(HERE, "_skeleton_es.json")
EN_EXTRA = os.path.join(HERE, "_skeleton_en_extra.json")
BATCH_NEW = os.path.join(HERE, "_batch52_v1.4.242.json")
BATCH_EN_ONLY = os.path.join(HERE, "_batch53_v1.4.242.json")

sys.path.insert(0, HERE)
import _filter as f

PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}|\{[^}]*\}")

CHANGED = {
    "auto.components.NativeChatResumeFailureGuidance.conflict": "Этот чат открыт в другом окне Orca или в терминале. Закройте его там и повторите попытку.",
    "auto.components.NativeChatResumeFailureGuidance.ownershipUnknown": "Этот чат ещё не готов к возобновлению. Подождите немного и повторите попытку.",
    "auto.components.NativeChatResumeOnRestartModal.continuedMany": "Возобновлено {{value0}} чатов",
    "auto.components.NativeChatResumeOnRestartModal.continuedOne": "Возобновлён 1 чат",
    "auto.components.WorktreeJumpPalette.2770f02910": "Ищите чаты, терминалы, рабочие пространства, задачи, настройки и действия",
    "auto.components.WorktreeJumpPalette.27f10cca63": "Ищите чаты, терминалы, рабочие пространства, задачи, настройки и действия…",
    "auto.components.WorktreeJumpPalette.recentWorktreesHeader": "Недавние рабочие пространства",
    "auto.components.WorktreeJumpPalette.worktreesHeader": "Рабочие пространства",
    "auto.components.cmd.j.quick.actions.splitChatDownDescription": "Открывает новый чат в разделённой панели снизу.",
    "auto.components.cmd.j.quick.actions.splitChatRightDescription": "Открывает новый чат в разделённой панели справа.",
    "auto.components.editor.ExternalFileChangeBanner.7c41e90d12": "Этот файл изменился на диске, пока у вас были несохранённые правки. «Перезаписать» заменит более новое содержимое на диске.",
    "auto.components.settings.AgentsPane.25a41a9aad": "Заново обнаружить агентов, установленных на этом сервере",
    "auto.components.settings.CursorAccountsSection.subtitle": "Показывает использование плана Cursor на основе входа, уже имеющегося на этом компьютере. Orca только читает его — никогда не изменяет ваш вход Cursor.",
    "auto.components.settings.CursorAccountsSection.usageTitle": "Использование плана",
    "auto.components.settings.ExperimentalPane.nativeChat.copy": "Поддерживаемые новые агенты открываются в структурированном чате. Остальные агенты открываются в терминале; существующие чаты остаются доступны.",
    "auto.components.settings.ExperimentalPane.nativeChat.description": "Открывать поддерживаемых новых агентов в интерфейсе чата.",
    "auto.components.settings.RemoteServerUpdateStatus.legacyHelp": "Удалённые обновления для этого сервера недоступны. Обновите Orca на хосте сервера.",
    "auto.components.settings.RuntimeEnvironmentsPane.3f67e8078a": "Новые проекты создаются на этом компьютере, если не выбрать здесь сохранённый сервер. Существующие проекты, файлы и терминалы остаются на своём хосте.",
    "auto.components.settings.RuntimeEnvironmentsPane.64b6bea541": "Хост по умолчанию для новых проектов",
    "auto.components.settings.RuntimeEnvironmentsPane.7b5986c8df": "Подключено к {{value0}}. Чтобы новые проекты по умолчанию создавались там, выберите его в разделе «Дополнительно > Хост по умолчанию для новых проектов».",
    "auto.components.settings.RuntimeEnvironmentsPane.activeServerRowHelp": "Хост по умолчанию для новых проектов. Существующие проекты остаются на своём хосте.",
    "auto.components.settings.RuntimeEnvironmentsPane.ed3e3f069d": "Это удаляет сохранённый сервер из Orca. Хост по умолчанию для новых проектов не меняется.",
    "auto.components.settings.RuntimeEnvironmentsPane.removeActiveServerBlocked": "Этот сервер — хост по умолчанию для новых проектов. Выберите другой в разделе «Дополнительно», прежде чем удалять его.",
    "auto.components.settings.RuntimeEnvironmentsPane.removeActiveServerDescription": "Этот сервер — хост по умолчанию для новых проектов. Выберите другой в разделе «Дополнительно», прежде чем удалять его. Существующие сеансы хоста не затрагиваются.",
    "auto.components.settings.Settings.17bdee4ff1": "Отбросить несохранённые настройки ИИ?",
    "auto.components.settings.Settings.43b68e10f0": "У вас есть несохранённые настройки ИИ. При выходе они будут отброшены.",
    "auto.components.settings.ZcodePlanAccountsSection.usingCliHelp": "Orca читает выбранный Coding Plan из хранилища учётных данных CLI ZCode на этом компьютере. Сохраните ключ API ниже, чтобы привязать план здесь.",
    "auto.components.settings.accounts.search.cursor.description": "Использование плана, полученное из входа Cursor, уже имеющегося на этом компьютере (cursor-agent login).",
    "auto.components.settings.appearance.search.cursor.description": "Показывает использование плана Cursor на основе входа Cursor на этом компьютере.",
    "auto.components.settings.experimental.search.nativeChat.description": "Открывать поддерживаемых новых агентов в интерфейсе чата.",
    "auto.components.settings.providerAccountScope.localCredentials": "Учётные данные и проверки аккаунта этого провайдера принадлежат этому десктопному клиенту. Чтобы использовать сервер, измените «Настройки > Удалённые серверы Orca > Дополнительно > Хост по умолчанию для новых проектов».",
    "auto.components.settings.providerAccountScope.localRateLimit": "Бюджет API {{value0}} получается из CLI на этом десктопном клиенте. Выберите сервер в меню «Хост» в верхней части настроек, чтобы увидеть его бюджет.",
    "auto.components.settings.providerAccountScope.remoteServerCredentials": "Учётные данные и проверки аккаунта этого провайдера принадлежат этому удалённому серверу. Чтобы использовать другой хост, измените «Настройки > Удалённые серверы Orca > Дополнительно > Хост по умолчанию для новых проектов».",
    "auto.components.settings.providerAccountScope.remoteServerRateLimit": "Бюджет API {{value0}} получается из CLI на этом удалённом сервере. Выберите другой хост в меню «Хост» в верхней части настроек, чтобы увидеть его бюджет.",
    "auto.components.settings.runtime.environments.search.4575341c77": "Добавляет сохранённый удалённый сервер Orca, генерирует URL сопряжения или выбирает хост по умолчанию для новых проектов.",
    "auto.components.settings.settingOwnership.agentLaunchDefaults": "Агент по умолчанию, переопределения команд, аргументы CLI и среда запуска сохраняются на выбранном хосте.",
    "auto.components.sidebar.SidebarWorkspaceOptionsMenu.activeRuntimeHost": "По умолчанию для новых проектов",
    "auto.components.sidebar.WorktreeOpenInMenu.remoteEditorUnsupportedDetail": "Выберите VS Code, Cursor или Zed, либо используйте приложение локально.",
    "auto.components.sidebar.WorktreeOpenInMenu.remoteLaunchFailed": "Не удалось открыть путь в редакторе.",
    "auto.components.sidebar.WorktreeOpenInMenu.remoteLaunchFailedDetail": "Проверьте команду редактора, настроенную на этой машине.",
    "auto.components.sidebar.WorktreeOpenInMenu.sshAliasRequired": "Этому редактору нужен SSH-alias из конфига для этого хоста.",
    "browser.clientHosted.unavailableDescription": "Эта страница сейчас недоступна на этом компьютере.",
    "components.agentSessionContinuation.dialogTitle": "Передать другому агенту",
    "components.native-chat.backgroundTasks.stateUnverifiable": "статус недоступен",
    "components.native-chat.backgroundTasks.stateUnverifiableCount": "{{value0}} — статус недоступен",
    "components.native-chat.composer.placeholder": "Спросите что угодно: @ — упомянуть файлы, / — команды",
    "components.native-chat.composer.skillsUnavailableHost": "В SSH-чатах нельзя получить список навыков",
    "components.native-chat.failureWords.accountSwitchInProgress": "Настройка {{agent}} меняется на этом хосте. Повторите попытку после её завершения.",
    "components.native-chat.failureWords.notSignedIn": "В {{agent}} не выполнен вход.",
    "components.native-chat.failureWords.previousExitUnverifiable": "Не удалось остановить {{agent}} от прошлого запуска.",
    "components.native-chat.failureWords.providerRejected": "{{agent}} не принял это сообщение.",
    "components.native-chat.failureWords.providerRejectedQuoted": "{{agent}} не принял это сообщение: {{detail}}.",
    "components.native-chat.structuredSessionHostDeclinedDescription": "Это рабочее пространство не может запустить чат {{value0}}.",
    "components.native-chat.subagents.state.unverifiable": "статус недоступен",
    "components.native-chat.subagents.state.unverifiableCount": "{{value0}} — статус недоступен",
    "components.native-chat.writeNotice.capacity": "Orca на компьютере, где выполняется этот чат, достигла лимита запросов. Обновите Orca там и повторите попытку.",
    "components.tab.bar.SortableTabContextMenu.switchToChatView": "Продолжить в интерфейсе чата",
    "components.tab.bar.SortableTabContextMenu.switchToTerminalView": "Продолжить с терминальным агентом",
}


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
    source = dict(f.walk(json.load(open(SKELETON, encoding="utf-8"))))
    source.update(json.load(open(EN_EXTRA, encoding="utf-8")))
    before = len(ov)

    for key in [k for k in ov if k not in source]:
        del ov[key]
    removed = before - len(ov)

    added = json.load(open(BATCH_NEW, encoding="utf-8"))
    added.update(json.load(open(BATCH_EN_ONLY, encoding="utf-8")))
    unknown = [k for k in list(added) + list(CHANGED) if k not in source]
    if unknown:
        raise SystemExit("keys not present in the new catalog: " + repr(unknown[:5]))
    for key, value in added.items():
        check_placeholders(key, source[key], value)

    ov.update(added)
    ov.update(CHANGED)
    json.dump(ov, open(OV, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
    print(
        f"overrides: {before} -> {len(ov)} "
        f"(+{len(added)} added, {len(CHANGED)} changed, -{removed} removed)"
    )


if __name__ == "__main__":
    main()
