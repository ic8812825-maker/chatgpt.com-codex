# 3.1.6.3.3 — аудит OnInit и runtime mode

## Фактическая последовательность

1. `ConfigureWorkingParameters()`.
2. `ValidateInputs()`.
3. `ValidateWorkingParameters()`.
4. `ValidateFSMIntegrity()`.
5. Выбор manual/ATR geometry и расчёт adaptive geometry.
6. `PrintGeometryDiagnostics()` и `LogBigMoveLevels()`.
7. Жёсткий запрет `UseMarketOrders=false`.
8. `ValidateTradingEnvironment()`.
9. `RecoverState()`; при неуспехе допускается reset только при `IsProvenCleanStart()`.
10. После recovery: orphan validation, state-position consistency, state integrity, `RunReconciliation()`.
11. Логирование режима и `INIT_SUCCEEDED`.

## Runtime modes

- Отдельного единого enum `LEGACY/SPLIT/HYBRID` нет.
- Верхний выбор задают два взаимоисключающих bool: `UseLegacySingleBigGeometry` и `UseSplitBigGeometry`.
- Hybrid задаётся дополнительным `UseHybridSplitBigGeometry` внутри Split path.
- `UseHybridGeometrySolver` объявлен backward-compatible флагом и не является главным activation switch.
- Значения по умолчанию активируют Legacy, а не Hybrid.

## Ответы на критические вопросы

- Legacy и Split одновременно запрещены validation.
- Split может быть включён при Hybrid=false; тогда активен старый Split path.
- Hybrid=true при Split=false не блокируется отдельной проверкой как самостоятельная несовместимая комбинация; Hybrid-проверки находятся внутри `if(UseSplitBigGeometry)` и production dispatch всё равно выбирается по Split flag. Статус: `CONFLICTING`.
- `AllowRealTrading=false` приводит `IsInternalSimulationMode()` к true. Это не только запрет отправки реальных заявок, но автоматический выбор simulation engine.
- Hedging requirement обходится в simulation mode, поскольку `ValidateTradingEnvironment()` сразу возвращает true.
- Recovery выполняется после environment validation.
- При persistence mismatch и непроверенном clean start инициализация блокируется.
- При успешном recovery выполняются orphan, consistency, integrity и reconciliation gates.

## Замечания

| ID | Критичность | Содержание |
|---|---|---|
| INIT-001 | P1 | Нет единого runtime enum; Hybrid является вложенным флагом Split и может образовать недопустимую комбинацию с Legacy selection. |
| INIT-002 | P1 | `AllowRealTrading=false` автоматически включает simulation semantics. Аудит реального production path на таких defaults невозможен без отдельного режима dry-run/no-trade. |
| INIT-003 | P2 | Hedging и terminal trade checks не выполняются в simulation mode, поэтому init PASS не доказывает готовность real MT5 environment. |
| INIT-004 | P2 | Timer initialization в `OnInit` не найден; periodic reconciliation вызывается из ticks, а не гарантированным timer path. |

## Статус

`OnInit`: `MIXED_MODE / PARTIAL / UNSAFE`.
Production MQL5 не изменялся.
