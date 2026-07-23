# Hybrid Split Big — mapping математической модели и текущего MQL5-кода

Аудит проведён без изменения MQL5. Статус отражает существующий код на ветке `work`, а не требование к будущему коду.

| Математическая роль | Смысл | Существующая сущность MQL5 | Файл | Поле / функция | Статус |
|---|---|---|---|---|---|
| Far | текущая опорная позиция | `ROLE_FAR`, `Ctx.farLot`, ticket/identifier | `Include/Types.mqh` | enum role; context fields | EXACT_MAPPING |
| BigCore | основная Big часть | `ROLE_BIG_CORE`, `Ctx.bigCoreLot` | `Include/Types.mqh`, `RecoveryMath.mqh` | `CalcBigCoreLot` | EXACT_MAPPING |
| BigTrend | дополнительная Big часть | `ROLE_BIG_TREND`, `Ctx.bigTrendLot` | `Include/Types.mqh`, `RecoveryMath.mqh` | `CalcBigTrendLot` | EXACT_MAPPING |
| SmallBase | leg направления Far | `ROLE_SMALL_BASE`, `Ctx.smallBaseLot` | `Include/Types.mqh`, `RecoveryMath.mqh` | `CalcSmallBaseLot` | EXACT_MAPPING |
| FinalReserveReal | защищённый ledger reserve | `Ctx.totalReserve`, `ReserveLedger` | `Include/StateMachine.mqh` | event-key ledger | PARTIAL_MAPPING |
| PartialFarBudget | budget partial Far | `partialFarBudgetCarry`, pending fields | `Include/Types.mqh` | carry/pending context | PARTIAL_MAPPING |
| TransitionBudget | отдельная money basket | projected/actual transition nets only | `Include/Types.mqh` | no dedicated available/consumed ledger | NO_CURRENT_MAPPING |
| CycleID | cycle identity | `Ctx.cycleId`, role comment `ML|...|C...` | `Include/Types.mqh` | `BuildRoleComment`, parser | EXACT_MAPPING |
| Harvest level | level identity | `Ctx.harvestLevel` | `Include/Types.mqh`, `StateMachine.mqh` | ledger snapshot | EXACT_MAPPING |
| Symbol/Magic binding | ownership | symbol + `MagicNumber` in snapshots | `Include/StateMachine.mqh` | reserve context validation | EXACT_MAPPING |

## Фактические ограничения
* Split роли существуют отдельно; математическая спецификация не вводит вымышленный `BigTrend`.
* `CalcBigCoreLot` и `CalcBigTrendLot` используют normalise-down, а `CalcSmallBaseLot` — normalise-up; это должно быть воспроизведено в MQL5 parity tests, хотя reference model по умолчанию консервативно применяет Down как нормативную рекомендацию.
* Комментарий уже содержит роль, CycleID, level и reverse cycle, поэтому идентификация Harvest возможна при корректном сохранении комментария.
