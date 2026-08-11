# Приёмка этапа HSB.0 — автономная нормативная база Hybrid Split Big

Версия 1.0. Дата: 2026-08-05.

## Граница

Репозиторий `ic8812825-maker/chatgpt.com-codex`, ветка `work`, родительский каталог `MinusLock_BigHarvest_EA_V2`, новый корень `Hybrid_Split_Big_Independent_EA`. Старый production-код не изменялся; другие проекты не использовались.

## Создано

Корневые README, PROJECT_MAP, BUILD_INFO, CHANGELOG; 23 документа Docs; placeholder-каталоги Include/Core, Planning, Money, Execution, Scenarios, Persistence, Risk, Diagnostics; Tests/MQL5, StrategyTester, Evidence; Sets, Logs, Reports.

## Проверка норм

- Все обязательные документы существуют и написаны на русском языке.
- Зафиксировано 144 нормативных определения Requirement ID `HSBI-*`; повторные появления в traceability являются ссылками, а не новыми определениями. Конфликтующих определений не выявлено.
- Legacy roles/states, отдельный Split Big, generic Big/Small и DUAL_TAIL не включены.
- Допускается ровно один FAR; NEW_FAR — переходная роль.
- `HSBI-NF-001` закрепляет единственный источник NewFar: actual residual исходного BIG_CORE после всех подтверждённых действий Small Transition.
- FinalReserve запрещён для Partial Far.
- Initial Profit исключён из recovery ledgers.
- Final Close имеет одну authority и требует положительный RecoveryPLCloseNow без double counting.
- Transaction contract использует OnTradeTransaction; FSM advance до actual outcome запрещён.
- Persistence versioned/atomic; reconciliation не угадывает состояние.
- BUY/SELL описаны симметрично; формулы dimensioned и broker-rounded.
- Python production-зависимость и production MQL5-код отсутствуют.
- Реальная торговля запрещена.

## Структурные конфликты

P0 не найдено. Структура проекта соответствует PROJECT_MAP. Исполняемых `.mq5/.mqh` в новом проекте нет.

## Открытые нормативные P1

`HSBI-DEC-001..012`: production ratios, allocation shares, control price/range, Future Small depth, NewFar objective, emergency policy, transition loss, final profit, margin/drawdown, symbol/cycle scope, persistence backend и real limitations. По прямому правилу ТЗ наличие открытых нормативных P1 запрещает PASS и HSB.1.

## Итог

```text
PROJECT=Hybrid_Split_Big_Independent_EA
TRADING_SYSTEM=HYBRID_SPLIT_BIG_ONLY
HSB_STAGE_0_DOCUMENTATION=BLOCKED
PROJECT_MAP=PASS
FULL_MANUAL=PASS
MATHEMATICAL_MODEL=PASS
GEOMETRY_MODEL=PASS
STATE_MACHINE_SPECIFICATION=PASS
TRANSACTION_CONTRACT=PASS
MONEY_LEDGER_SPECIFICATION=PASS
PERSISTENCE_SPECIFICATION=PASS
RECONCILIATION_SPECIFICATION=PASS
PRODUCTION_CODE_STARTED=NO
NEXT_ALLOWED_STAGE=HSB.1V
HSB_STAGE_1_STARTED=NO
AWAITING_USER_DECISIONS=YES
REAL_TRADING_ALLOWED=NO
```

HSB.1 самостоятельно не начинается. Для разблокировки Администратор должен утвердить либо явно отложить с безопасным нормативным решением открытые P1, после чего проводится повторная HSB.0 acceptance revision.
