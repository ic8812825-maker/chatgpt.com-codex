# Этап HSB.0R-C — корректирующая синхронизация нормативной базы Hybrid Split Big

Версия: HSB.0R-C.1
Статус: IN_PROGRESS

## Назначение

Настоящий отчёт открывает корректирующий документальный этап HSB.0R-C. Его цель — устранить замечания независимой проверки этапа HSB.0R и встроить решения HSBI-DEC-001…014 непосредственно в основные нормативные документы `Docs/03–18`.

## Исходная точка

- Репозиторий: `ic8812825-maker/chatgpt.com-codex`
- Ветка: `work`
- Разрешённый проект: `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA`
- Исходный HEAD: `56122a41a56cfa4ec99f87e1ed595688e6040f9a`
- Родитель HSB.0R.26: `3395ae9fae103e24c1b70653e1d504b22fa2c25f`

## Исправляемые замечания

| ID | Критичность | Содержание | Начальный статус |
|---|---:|---|---|
| DOC-SYNC-001 | P1 | Основные документы 03–18 не содержат полный нормативный текст решений | OPEN |
| DEC-REGISTRY-001 | P1 | Реестр решений неполный и остаётся IN_PROGRESS | OPEN |
| STATUS-SYNC-001 | P1 | BUILD_INFO и финальный отчёт содержат разные статусы | OPEN |
| MATH-AUDIT-001 | P2 | Математическая приёмка недостаточна | OPEN |

## Основные нормативные документы

`Docs/03_FULL_SYSTEM_MANUAL_RU.md` — `Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md` являются обязательным source of truth. Reports и Evidence могут только подтверждать норму, но не заменять её.

## Границы

На этапе запрещены production `.mq5/.mqh`, `OnTick`, `OnTradeTransaction`, TradeEngine, исполняемая StateMachine, Python, MetaEditor, Strategy Tester и начало HSB.1.

## Статус

```text
HSB_STAGE_0R_CORRECTION=IN_PROGRESS
HSB_STAGE_0_DOCUMENTATION=BLOCKED
NEXT_ALLOWED_STAGE=NONE
HSB_STAGE_1_START_ALLOWED=NO
PRODUCTION_CODE_STARTED=NO
REAL_TRADING_ALLOWED=NO
```

## Git-цепочка

| Подэтап | Commit SHA | Статус |
|---|---|---|
| HSB.0R-C.1 | заполняется после публикации | IN_PROGRESS |

## Следующий разрешённый подпункт

`HSB.0R-C.2` — карта внедрения решений HSBI-DEC-001…014 в owner-документы.
