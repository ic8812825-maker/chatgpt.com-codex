# C3 — денежные контракты и production

BASE_SHA=3737116bff6e2275d674b3dd7b816de93715f27c

AUDIT / PROPOSED / AWAITING_ADMIN_APPROVAL. Production, trading и dispatch запрещены.

Независимые сценарии: 76; PASS=76; FAIL=0; INFRA=0. Их expected — literals и новый integer coefficient/scale oracle без imports subject evaluator. До/после и trace reserve/release/consume/owner rejection находятся в INDEPENDENT_TESTS.json; raw/posted/currency/grid не смешиваются.

D01 naming conflict описан в CONTRACT_CLARIFICATIONS; исходный grant50, consumed10, reserved15, free25. D02 projection не source; incomplete history unavailable. D03 Small10→ResidualHeld10 и Big0. D04 absolute50 против incremental10/Reserve30. D05 prefix/final/sticky/peak неодинаковы. D06 unknown cost/overlap блокируется. D07 in-memory exact replay0 delta; altered conflict; durable/concurrent unavailable. D08 foreign18 identity fields отвергаются, но trusted fixture provider не broker history. Все эти proposed semantic choices остаются неутверждёнными.

CR09: L1 margin79/transition50, L2 margin-6/transition1: A rejects L2, B positive L1. Cancellation1e28-.010-(1e28-.005)=-.005 точно отрицательна. Sequential reserve1e28 после двух.01 =1e28-.02. Signed64 max+1/min*(-1) недоступны, а не truncated. Лоты требуют min/max/step/origin и positive required legs.

| Production finding | Source/function | Доказательство / требуемое исправление |
|---|---|---|
| L01 / namespace | Include/Money/HSBI_EconomicLedgerTypes.mqh:6–11; HSBI_SameEconomicRecord/HSBI_ClassifyEconomicDuplicate/HSBI_BuildSourceDealKey | Native subset: components60/-10→70/-20 при net50 принимаются как duplicate1, нормативно conflict2. Account/Broker/Server в key отсутствуют. Full immutable payload + namespace после approval |
| L02 | Include/Money/HSBI_AllocationLedgerTypes.mqh:8; HSBI_ClassifyAllocationDuplicate | Native subset: FinalReserve50/Partial0 →0/50 total50, actual1 вместо conflict2 |
| M01 | Include/Money/HSBI_ReserveAllocationTypes.mqh:25–30; HSBI_ValidateReserveConsumptionKey | Local nonempty key/plan checks не связывают все поля с authoritative allocation; frozenR0 behavioral failures сохранены. Требуется allocation-bound durable consumption, не bool hasPrior |
| M02 | Include/Planning/HSBI_NewFarSolver.mqh:124; expectedReserveIdentity/expectedFarIdentity assignment | Expected копируется из проверяемого proof, независимость не доказана. Нужен provider→reconciled record→allocation→expected identity |
| M05 | Include/Money/HSBI_LevelMoneyEvaluator.mqh; reserveGainMoney | Small contribution остаётся source-role decision D03, формула production не изменена |
| Zero-Core | Include/Planning/HSBI_GeometrySolver.mqh:32–35; HSBI_SolveBigGeometry | coreGrid допускает0, slope только nonnegative core. Far.1 coreRatio.01 trendRatio3 smallRatio.1 даёт Core0/Trend.3/Small.01/slope.19; обязательная Core отсутствует |
| CR09 production | Include/Planning/HSBI_FutureSmallProofAggregator.mqh:50 | WORST_CASE выбирает worstTransitionLossLevel, не minCatchUpMargin |
| Persistence | Include/Persistence/HSBI_PersistenceInterface.mqh:7; HSBI_PersistSnapshotStub | success=false, PERSISTENCE_NOT_IMPLEMENTED; durable/CAS/restart UNPROVEN |
| Broker precision/fills/global funding | Provider/backend отсутствует | Fixtures не подтверждают actual broker posted values, partial executions, source-wide economic capital или concurrent settlement |

Native source normative result=FAIL; finding=L01_L02_CONFIRMED. Это воспроизведение дефекта, не production PASS. Production modifications=NO. Остальные статические finding не объявлены выполненным MQL5 runtime тестом.

Регрессии: FAIL; BaselineMatch=True. Исторические R7/R0 FAIL не исправлены. Матрица70 frozen guards и C3 public obligations явно различает reproduction и независимое покрытие; GUARD_COVERAGE=PARTIAL.
