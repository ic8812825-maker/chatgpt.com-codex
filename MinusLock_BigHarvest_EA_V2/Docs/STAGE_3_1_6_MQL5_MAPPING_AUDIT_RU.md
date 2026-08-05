# Этап 3.1.6.3 — полный аудит текущего MQL5 mapping Hybrid Split Big

## Подпункт 3.1.6.3.1 — исходное состояние

### Граница

- Репозиторий: `ic8812825-maker/chatgpt.com-codex`.
- Ветка: `work`.
- Единственный разрешённый каталог: `MinusLock_BigHarvest_EA_V2`.
- Файлы вне разрешённого каталога не используются как источник кода или решений.

### Git baseline

- Исходный HEAD: `9fb78470baf494d6d4fa7649d5b052d05a71e28a`.
- Родитель: `e15eeb60ac4cb65c7c7e20e569a2a88bc94a0047`.
- Сообщение HEAD: `Этап 3.1.6.2: проведена инвентаризация документации геометрии Big и Small`.

### Полный список production MQL5-файлов

Главный файл:

1. `MinusLock_BigHarvest_EA.mq5`.

Include-файлы:

1. `BrokerMoneyModel.mqh`
2. `Config.mqh`
3. `GeometryEngine.mqh`
4. `HybridCatchUpModel.mqh`
5. `HybridDecisionEngine.mqh`
6. `HybridFutureSmallSolver.mqh`
7. `HybridGeometrySolver.mqh`
8. `HybridMarginModel.mqh`
9. `HybridPartialFarPreview.mqh`
10. `HybridRoundingModel.mqh`
11. `HybridTransitionPlanner.mqh`
12. `HybridWorstCaseModel.mqh`
13. `Logger.mqh`
14. `LotUtils.mqh`
15. `PendingContractEngine.mqh`
16. `PositionResolutionEngine.mqh`
17. `PositionUtils.mqh`
18. `ReconciliationEngine.mqh`
19. `RecoveryMath.mqh`
20. `RiskManager.mqh`
21. `SimulationEngine.mqh`
22. `StateIntegrityEngine.mqh`
23. `StateMachine.mqh`
24. `TradeEngine.mqh`
25. `Types.mqh`

Итого: `1 .mq5 + 25 .mqh = 26` файлов.

### Первичные доказанные наблюдения

1. Главный `.mq5` напрямую подключает все 25 include-модулей; скрытых подкаталогов с `.mqh` в `Include` нет.
2. В `Config.mqh` одновременно существуют Legacy, Split и Hybrid inputs.
3. `UseLegacySingleBigGeometry` и `UseSplitBigGeometry` взаимоисключаются, однако `UseHybridSplitBigGeometry` является вложенным флагом внутри Split, а не отдельным единым runtime enum.
4. Значения по умолчанию: Legacy включён, Split выключен, Hybrid выключен, реальная торговля выключена.
5. `IsInternalSimulationMode()` возвращает true не только при `UseInternalSimulation=true`, но и при `AllowRealTrading=false`; следовательно запрет реальной торговли фактически активирует simulation-compatible execution branch.
6. В `OnTick` при `STATE_IDLE` и нуле managed positions вызывается `OpenInitialLock()` до общего `RunStateMachine()`.
7. `RunPeriodicReconciliation()` вызывается до FSM dispatch; три mismatch/error state дают ранний выход.

### Изменяемые документы

- Создан `Docs/STAGE_3_1_6_MQL5_MAPPING_AUDIT_RU.md`.
- Далее будет обновляться `Docs/STAGE_3_1_6_PRODUCTION_GEOMETRY_REPORT_RU.md`.
- При необходимости будут созданы call graph и findings register.

### Статус

```text
STAGE_3_1_6_STATUS=IN_PROGRESS
SUBSTAGE_3_1_6_3_STATUS=IN_PROGRESS
PRODUCTION_MQL5_AUDIT=IN_PROGRESS
PRODUCTION_MQL5_CHANGED=NO
STAGE_3_1_6_4_START_ALLOWED=NO
STAGE_3_1_7_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```

### Ограничение доказательства

MetaEditor и MT5 Strategy Tester не запускались. Наличие файла или функции не считается доказательством production reachability. Непроверенные пути получают `UNPROVEN`.
