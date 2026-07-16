# Baseline завершения Big и Small

START_SHA=1f1cd49bbd703942f6393fee5b3a96659e172cfe
BRANCH=work
PROJECT_FOLDER=MinusLock_BigHarvest_EA_V2
DATE=2026-07-16

## Defaults и режимы

Источник defaults: `Include/Config.mqh`. Legacy включён, Split выключен, Dynamic Reverse Small выключен, `MaximumNewFarRatio=0.97`, `AllowRealTrading=false`. StartLot=0.10; BigRatio=1.15; SmallRatio=0.25; Split ratios: BigCore=1.60, BigTrend=0.25, SmallBase/Far=0.60. MaxHarvestLevels=7, MaxReverseCycles=7.

## Текущая архитектура

State Machine содержит Initial, Far, Legacy Big/Small, Split open/harvest, Small reverse/transition, pending/retry, Final Close, max-level, recovery и error states. Основные функции обнаруживаются командами `rg -n 'ProcessSplit|ProcessBig|ProcessSmall|EvaluateFinalCloseGate|Reserve|PartialFar|RecoveryPL' Include/StateMachine.mqh`.

Point-based часть: triggers/distances, slippage points, ATR geometry. Money-based часть: `BrokerMoneyModel.mqh`, lifecycle deal net, Reserve ledger, projected Far close loss и Final Close evaluation. Broker model остаётся неполной: double spread, единый buffer, постоянный swap и неполная basket aggregation.

## Известные FAIL/UNKNOWN

- Persistence: Python PASS, MQL5/MetaEditor NOT_RUN; полный Ledger validation ранее FAIL.
- Big Recovery Improvement: UNKNOWN.
- Reserve Catch-Up: UNKNOWN.
- Partial Far money safety: UNKNOWN.
- Small Transition: UNKNOWN.
- New Far compression: UNKNOWN.
- Finite reversals: UNKNOWN.
- False Reverse: UNKNOWN.
- Big/Small interaction: UNKNOWN.
- `Sets/Unverified/BigScenario_Best_1.set`: UNVERIFIED, не для MT5/production.
- MetaEditor: отсутствует, NOT_RUN.
- MT5: отсутствует, NOT_RUN.
- REAL_TRADING_ALLOWED=NO.

## Существующие тесты

Активный Python suite, static scripts, scenario tests, CleanStart MQL5 harness (NOT_RUN), offline optimizer/simulator. Python не заменяет MQL5 runtime.

## Формулы baseline

- Legacy Big lot: `NormalizeNearest(Far*BigRatio)`; Small: `NormalizeUp(Far*SmallRatio)`.
- Split net exposure: `BigCoreActual+BigTrendActual-SmallBaseActual-FarActual`.
- Coverage: `(Reserve+Carry+допустимый нераспределённый Harvest)/WorstCaseFarCloseLoss`.
- Small target пока не гарантирован runtime-формулой `NormalizeDown(OldFar*MaximumNewFarRatio)`.
- RecoveryPL должен исключать Initial ignored profit и включать realized/floating recovery net после costs.

Этот документ фиксирует baseline, но не доказывает безопасность Big или Small.
