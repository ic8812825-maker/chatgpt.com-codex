# 02B-R1 — точное задание после утверждения контрактов

Базовый SHA: `4e7d911002824a4a92e49b54f0f964afcf8cf703`; ветка `work`; дата 04.11.2026. Локальный HEAD и remote `refs/heads/work` совпали перед записью. Режим: только тесты, контракты-предложения и отчёты. Утверждения администратора не получены. Production-код и исторические evidence не изменяются.

`IMPLEMENTATION_ALLOWED=NO`. Этот документ — подготовленное задание, а не разрешение начать исправления.

## Входной gate

1. Администратор явно утверждает D-01–D-08, CR-01–08/10 и отдельный критерий CR-09 либо исключает WORST_CASE из R1 с fail-closed ограничением его использования.
2. Зафиксировать утверждённую версию схемы, canonicalization/precision, source namespace и migration/reconciliation policy. Сверить новый согласованный baseline/remote HEAD, не использовать старый SHA автоматически.
3. Сохранить запрет dispatch, реальных сделок и изменений Big/Small geometry. Zero-Core передать отдельному geometry этапу; до него нельзя выдавать readiness NewFar.

## Минимальная область R1

Разрешаемая после утверждения область: Money DTO/validators, независимый authoritative lookup interface, Catch-Up authorization и assembly expected identity в NewFar. **NewFar solver на R0 не меняется.** В R1 изменение его assembly разрешается только явно утверждённым scope; objective/tie-break/geometry не затрагивать. Production persistence не заменять in-memory map и не объявлять готовой. При отсутствии реального authority provider возвращать UNAVAILABLE, не создавать подтверждённые records из caller flags.

## Порядок и production-функции

1. CR-03/L-01: `HSBI_EconomicLedgerRecord`, `HSBI_BuildSourceDealKey`, `HSBI_ValidateEconomicRecord`, `HSBI_SameEconomicRecord`, `HSBI_ClassifyEconomicDuplicate`, `HSBI_SerializeEconomicRecord`: account/server/plan/components, canonical immutable equality/digest. Новая схема не доверяет старой неполной сериализации.
2. CR-04/L-02: `HSBI_AllocationLedgerRecord`, `HSBI_AllocatedTotal`, `HSBI_ValidateAllocationConservation`, `HSBI_ClassifyAllocationDuplicate`: immutable grants отдельно от balances, policy/schema, component equality. `HSBI_CanConsumeBucket/Amount` остаются локальными primitives; внешний guard обязательный.
3. CR-01: новый `ValidateConsumptionAgainstAuthoritativeAllocation` с amount/bucket/source/owner/policy/revision и typed authority outcomes. `HSBI_ValidateReserveConsumption`, duplicate/conflict/digest helpers обновляются согласованно; один bool prior не разрешает новую трату.
4. CR-02/M-02: independent lookup broker history → reconciled record → allocation → expected identity; `HSBI_NewFarProofIdentity`, `HSBI_SolveNewFar` assembly, `HSBI_ValidateReserveSourceProof/FarLossProof`, `HSBI_EvaluateReserveCatchUp`. Нельзя получать expected из submitted proof. Пока provider недоступен, кандидат исключается fail-closed.
5. CR-05/07/08: typed MoneyState с known revision, finite fields, commit/replay interface. Атомарная выдача remaining и exactly-once доступны только после отдельной проверенной durable реализации; `HSBI_PersistSnapshotStub` не считать storage. Не расширять R1 до торговли/полного lifecycle.
6. M-05/D-02…06: только утверждённые naming/type/formula изменения. Без решения Small/buffers/FarLoss не менять формулы. Geometry и CR-09 — отдельные commits/этапы с собственным разрешением.

## Проверки приёмки R1

- Все группы matrix имеют положительный контроль и негативные нормативные outcomes. `--enforce-contract` должен завершаться 0 только после закрытия **всех относящихся к утверждённому scope** несовпадений; отдельные deferred geometry/worst критерии сохраняют BLOCKED, а не удаляются ради зелёного результата.
- Foreign account/magic/cycle/position/deal/event/plan/revision/snapshot, stale proof, altered digest/components, missing history/allocation и reused allocation не дают authorization. Неизвестная history → UNAVAILABLE.
- Exact replay даёт NO_OP с нулевыми deltas; altered amount/bucket/policy/source → CONFLICT. Повтор после рестарта, другая заявка на spent bucket и гонка двух consumers проверяются durable fault-injection. Если durable backend ещё отсутствует — эти критерии UNPROVEN и R1 не заявляет end-to-end exactly-once.
- Allocation equality и per-bucket remaining+consumed подтверждены независимым decimal oracle, отрицательные/NaN/Infinity и неизвестные версии отвергаются.
- Source mutations: удалить binding, стереть сравнение immutable components/buckets, скопировать proof в expected, обнулить costs, повторно умножить ReserveShare, разрешить projected→actual, проигнорировать prior registry. Каждая mutation должна быть поймана нужным негативным тестом, а не parser error. Repair sensitivity R0 не заменяет mutation proof исправленного pipeline.
- Свежие R8/R10/R12/R12A; frozen R7 проверять по актуальной области функциональных guards без переписывания исторического evidence.
- MetaEditor compile main/harness, MQL5 unit и broker-money/dry-run проверки отдельно; без них MQL5/StrategyTester=NOT_RUN. C++ shim не повышает эти статусы.
- Diff только утверждённого scope, source hashes и no-trade guards сохранены. Экономические решения и readiness проекта автоматически не повышать.

## Точки контроля

Каждый шаг — отдельный reviewable commit с fixtures, independent expected outcomes, fresh logs и migration analysis. При неоднозначном нормативе остановить только зависимую реализацию и вернуть DECISION_REQUIRED. R1 не разрешает real/demo broker dispatch, OnTradeTransaction trading или изменение no-trade guards.

## Ссылки для реализации

- [Include/Money/HSBI_EconomicLedgerTypes.mqh:9](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L9) — `HSBI_SameEconomicRecord`
- [Include/Money/HSBI_EconomicLedgerTypes.mqh:10](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L10) — `HSBI_ClassifyEconomicDuplicate`
- [Include/Money/HSBI_EconomicLedgerTypes.mqh:7](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L7) — `HSBI_BuildSourceDealKey`
- [Include/Money/HSBI_AllocationLedgerTypes.mqh:8](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L8) — `HSBI_ClassifyAllocationDuplicate`
- [Include/Money/HSBI_AllocationLedgerTypes.mqh:7](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L7) — `HSBI_ValidateAllocationConservation`
- [Include/Money/HSBI_AllocationLedgerTypes.mqh:9](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L9) — `HSBI_CanConsumeBucket`
- [Include/Money/HSBI_AllocationLedgerTypes.mqh:10](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L10) — `HSBI_CanConsumeAmount`
- [Include/Money/HSBI_MoneyState.mqh:5](../Include/Money/HSBI_MoneyState.mqh#L5) — `HSBI_ValidateMoneyState`
- [Include/Money/HSBI_ReserveAllocationTypes.mqh:25](../Include/Money/HSBI_ReserveAllocationTypes.mqh#L25) — `HSBI_ValidateReserveConsumption`
- [Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:35](../Include/Money/HSBI_ReserveCatchUpEvaluator.mqh#L35) — `HSBI_EvaluateReserveCatchUp`
- [Include/Money/HSBI_MoneyProofIdentity.mqh:16](../Include/Money/HSBI_MoneyProofIdentity.mqh#L16) — `HSBI_IsSameMoneyProofIdentity`
- [Include/Planning/HSBI_NewFarSolver.mqh:94](../Include/Planning/HSBI_NewFarSolver.mqh#L94) — `HSBI_SolveNewFar`
- [Include/Planning/HSBI_GeometrySolver.mqh:21](../Include/Planning/HSBI_GeometrySolver.mqh#L21) — `HSBI_SolveBigGeometry`
- [Include/Money/HSBI_BasketMoneyEvaluator.mqh:11](../Include/Money/HSBI_BasketMoneyEvaluator.mqh#L11) — `HSBI_EvaluateBasketMoney`
- [Include/Planning/HSBI_FutureSmallProofAggregator.mqh:23](../Include/Planning/HSBI_FutureSmallProofAggregator.mqh#L23) — `HSBI_AggregateFutureSmallProof`
- [Include/Persistence/HSBI_PersistenceInterface.mqh:7](../Include/Persistence/HSBI_PersistenceInterface.mqh#L7) — `HSBI_PersistSnapshotStub`
