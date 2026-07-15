# Базовый аудит этапа денежной модели

## Идентификаторы

- START_SHA: `671c023dc22b5476a2a71319ede424901f28e0f0`
- Дата: `2026-07-15 UTC`
- Ветка: `work`
- Рабочая папка: `MinusLock_BigHarvest_EA_V2`
- Репозиторий: `ic8812825-maker/chatgpt.com-codex`

## Список файлов проекта

Полный список файлов зафиксирован командой:

```bash
cd MinusLock_BigHarvest_EA_V2 && find . -type f | sort > /tmp/project_files.txt
```

Количество файлов на baseline: `334`.

## Текущие defaults из `Include/Config.mqh`

```text
CloseFarShare = 0.10
ReserveShare = 0.90
UseSplitBigGeometry = false
UseLegacySingleBigGeometry = true
UseDynamicReverseSmall = false
AllowRealTrading = false
```

## Результаты baseline-тестов

```text
pytest -q Tests/unit Tests/static Tests/scenario = PASS, 78 passed
python Tests/validate_v2_static.py = PASS
python Tests/default_parameters_v241_check.py = PASS
python Tests/fsm_integrity_check.py = PASS
python Tests/terminal_states_separated_from_pending_check.py = PASS
```

## MetaEditor / MT5

В Linux-контейнере не обнаружены:

```text
metaeditor64.exe
metaeditor.exe
terminal64.exe
wine
```

Статусы:

```text
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

## Текущий статус Split / Legacy

- Split Big реализован как контролируемый режим тестирования.
- Production default остаётся Legacy: `UseSplitBigGeometry=false`, `UseLegacySingleBigGeometry=true`.
- Real trading отключён: `AllowRealTrading=false`.
- До реальной компиляции MetaEditor и MT5 Strategy Tester разрешена только дальнейшая разработка и локальные Python/static проверки.

## Известные ограничения baseline

- Нет подтверждения MetaEditor `0 errors / 0 warnings`.
- Нет Strategy Tester отчётов MT5.
- MQL5 internal tests не запускались в MetaEditor.
- Денежная модель брокера ещё не выделена в единый `BrokerMoneyModel.mqh` на baseline.
