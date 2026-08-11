# HSB.1V — исходный baseline

Дата фиксации: 2026-08-10 (UTC).

## Репозиторий

- Репозиторий: `https://github.com/ic8812825-maker/chatgpt.com-codex.git`.
- Ветка: `work`.
- Исходный SHA: `82664748abff0dec450edc68fb9ceb9c640f98b1`.
- `git status`: чистое рабочее дерево (`## work`).
- Каталог проверки: `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA`.
- Файлов в каталоге на baseline: `118`.
- EA `Hybrid_Split_Big_Independent_EA.mq5`: присутствует.
- MQL5 test script `Tests/MQL5/HSBI_Skeleton_Tests.mq5`: присутствует.

## Статусы на момент начала проверки

```text
HSB_STAGE_0_DOCUMENTATION=PASS
HSB_STAGE_1_STRUCTURE=PASS
HSB_STAGE_1_NO_TRADE_GUARD=PASS
HSB_STAGE_1_DEPENDENCY_AUDIT=PASS
HSB_STAGE_1_COMPILE=NOT_VERIFIED
HSB_STAGE_1_MQL5_TESTS=NOT_VERIFIED
HSB_STAGE_1_STATUS=PARTIAL_ENVIRONMENT_BLOCKED
HSB_STAGE_2_STARTED=NO
TRADING_IMPLEMENTED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
NEXT_ALLOWED_STAGE=HSB.1V
```

Статусы выше являются снимком исходного состояния, а не итогом HSB.1V; выявленные расхождения подлежат синхронизации отдельным коммитом.

## Ограничения HSB.1V

- Только независимый каталог проекта и только MQL5.
- Старый `MinusLock_BigHarvest_EA_V2` не изменяется и не подключается.
- Legacy Big/Small, Split, ReverseSmall, старые `StateMachine` и `TradeEngine` не подключаются.
- Торговые сценарии и production lifecycle не реализуются.
- Торговые API, demo/real trading и trade requests запрещены.
- Python и сторонние parser-ы не являются oracle компиляции или MQL5-тестов.
- HSB.2 не начинается; история Git не переписывается.
