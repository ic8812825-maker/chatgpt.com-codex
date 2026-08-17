# Предреализационный offline-аудит HSB.2D-V1

## Baseline

- `BASELINE_SHA=1f1d495b50a94352e0b0b13d833d1a58aa19f3b3`
- `BRANCH=work`
- `LOCAL_ORIGIN_WORK=1f1d495b50a94352e0b0b13d833d1a58aa19f3b3`
- `REMOTE_WORK=1f1d495b50a94352e0b0b13d833d1a58aa19f3b3`
- `INITIAL_WORKTREE_CLEAN=YES`
- `BASELINE_VERDICT=PASS`

## Инвентаризация

На baseline обнаружено 2 файла `.mq5`, 73 файла `.mqh`, 142 файла `.md` и 14 служебных `.gitkeep`. Проверены списки `Tests`, `Reports`, `Docs`, `Include`, а также `BUILD_INFO.md`, `README_RU.md`, `PROJECT_MAP_RU.md`, `CHANGELOG_RU.md`, главный EA и MQL5 harness.

Компоненты HSB.2D: `HSBI_RuntimeDecisionTypes.mqh`, `HSBI_RuntimeDecisionValidator.mqh`, `HSBI_RuntimeRestartValidator.mqh`, `HSBI_RuntimeTransactionBarrier.mqh`, документы runtime/allocation/persistence/barrier, тесты T431–T464 и доказательные отчёты HSB.2D.

## Фактическое состояние

- Главный EA — неторгующий skeleton: `OnInit()` выбирает `HSBI_RUNTIME_DISABLED`, `OnTick()` вызывает только `HSBI_SubmitActionStub()`.
- Production broker dispatch и торговые библиотеки отсутствуют.
- Harness декларирует T01–T464; выполнение в MetaEditor/MT5 на этом этапе не подтверждено.
- Runtime decision, restart и transaction barrier реализованы как fail-closed admission/validation contracts, а не как разрешение сделки.

## Найденные несогласованности и риски

1. Нет единого воспроизводимого verifier, include manifest, SHA-256 manifest и negative mutation suite.
2. Исторические статусы могут восприниматься как текущие; нужен канонический статус HSB.2D-V1.
3. Нет пользовательского handoff для настоящей компиляции MetaEditor и запуска T01–T464.
4. Compile-risk: include-граф и guards ранее не проверялись единым детерминированным инструментом.
5. Restart использует точное сравнение нормализованного persisted `actualVolume`; контракт и риск сериализации требуют явного документирования, без произвольного epsilon.
6. Runtime-блокеры: MetaEditor, MT5 runtime, broker properties и Strategy Tester недоступны; соответствующие проверки остаются `NOT_EXECUTED_MT5_UNAVAILABLE`.

Статический поиск production MQL5 не выявил торговых вызовов, `Trade.mqh`, `MqlTradeRequest`, `TRADE_ACTION_*`, `WebRequest` или DLL import. Итог должен быть повторно доказан verifier и negative fixtures.

## Разрешённый scope изменений

Только `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/**`: отчёты, status docs, `Tests/Static`, `Tests/Evidence`, пользовательская инструкция и manifest. Нормативная математика, HSB.2E и broker dispatch не изменяются.
