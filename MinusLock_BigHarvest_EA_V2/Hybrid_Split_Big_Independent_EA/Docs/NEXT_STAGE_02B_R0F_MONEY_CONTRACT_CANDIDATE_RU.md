# R0F — кандидат денежных контрактов

BASE_SHA=ad5ce78d74c53b34358cd7508982aa888976057a

PROPOSED / AWAITING_ADMIN_APPROVAL. CONTRACT-DECISION-PREPARATION / TEST-ONLY. Не разрешение production или торговли.

## Иерархия и статус

Первичные Docs04/08/16/24/31/32 — исторические нормативные источники. Их наличие/статус source-of-truth не заменяет явное административное решение о proposed изменениях. Production source — фактическое поведение, не разрешение изменить экономику. R0D/R0E/C1/C2/C3 — proposed/spec/test evidence; C3 предложения не стали APPROVED. Спорные версии перечислены в CONFLICT_RESOLUTION; выбранной production policy в R0F нет. Independent counterexamples опровергают свойства в указанном scope, не подтверждают broker execution.

## R0F-01: закрытая кандидатная схема баланса

OriginalGrant=Consumed+Reserved+Free; RemainingGross=Reserved+Free; все четыре части неотрицательны и имеют одну currency/precision/ownership. Bare Gross запрещён в новом API из-за конфликта с legacy RemainingGross. Grant — immutable исходный ресурс, Consumed никогда не возвращается в Free без отдельного подтверждённого экономического события. AvailableReserve не равен просто полю Free: нужен полный authority/journal/global-funding proof.

Reserve x: F'=F-x,R'=R+x; release своему owner: F'=F+x,R'=R-x; consume free: C'=C+x,F'=F-x; consume reserved своему owner: C'=C+x,R'=R-x. Везде x>0, checked bounds, новый event/revision. Чужой owner не тратит reserved. Grant50/C10/R15/F25 =>RemainingGross40; C+R+RemainingGross=65 неверно. Source total COMMITTED ΣOriginalGrants=EligibleNet, Unallocated0; PREPARED Σgrants+Unallocated=EligibleNet, spending forbidden. Zero/negative actual net сохраняется economic, eligible grant0 без отдельного loss-consumption contract.

Exact event payload с original revision даёт NO_OP/zero delta; changed payload same event — CONFLICT. Complete trusted fixture journal — предпосылка модели, не durable proof. Unknown history/currency/precision/owner →UNAVAILABLE. Legacy adapter только при доказанной старой семантике RemainingGross: F=RemainingGross-Reserved. Не создавать фиктивный account/owner и не выполнять persistent migration.

## R0F-02: money types и переходы

ProjectedBasketNet — плановая корзина; ProjectedCloseNowNet — оценка закрытия по текущему snapshot/спреду/расходам; ActualRealizedDealNet — наблюдённые подтверждённые закрытия с исходными знаками Profit/Swap/Commission/Fee; ReconciledEconomicNet — независимая сверка raw/posted components, currency, precision и source; EligibleSourceGrant — разрешённая policy доля подтверждённого допустимого источника; AvailableReserve — неистраченный/неудержанный ресурс после complete ledger/journal и global attribution.

Прогноз100 не создаёт actual grant. Неполная history не known0. Raw signed sum точна в объявленном representation; ObservedDealNet — отдельное raw поле. Даже .1+.2 binary observations не равны exact decimal.3: это не основание локально создать broker posting. Независимые posted components/net и verified policy сохраняются отдельно. ReconciliationReceipt привязан к immutable source digest, хранится отдельным append-only envelope; текущий receipt не переписывает raw identity. Kind/confirmed/PolicyVerified в Python — trusted fixture boundary, не аутентификация брокера. Формальный registry шести типов — CONTRACT_MATRIX.MoneyTypes; runtime nominal-type enforcement и полный AvailableReserve API не реализуются. operate/state — trusted integer-balance algebra, не способ подтвердить авторизацию по вручную созданному state. Извлечение числа из projection не создаёт independent receipt.

## R0F-03: Big/Small

Рекомендуемый A: Core0/Trend0/Small10 =>BigReserve0/ResidualHeld10. B: только отдельный утверждённый transfer event с debit+credit и source provenance. Role/policy не меняются в старом source payload. Opening costs остаются economic facts, но не harvest grant; INOUT требует независимого разделения закрытой/открытой частей. HSBI_LevelMoneyEvaluator reserveGainMoney и Reserve Allocation/Catch-Up не меняются до approval D03 и отдельной production-фазы.

## R0F-04: Far/Catch-Up

AbsoluteFarLoss=max(0,-ProjectedCloseNowFarNet), incremental=max(0,absolute-baselineAbsolute) только diagnostic с verified basis/volume/cycle/plan/revision/clock lineage. Absolute50 baseline40 reserve30: покрытие incremental10 не покрывает50. BUY close по Bid, SELL по Ask. Restart/partial close/basis change без подтверждённого baseline делает incremental UNAVAILABLE.

CatchUpMargin_i=EligibleReserve_i-AbsoluteFarLoss_i-SafetyBuffer_i; all-required forecast proof требует min_i margin_i>0 и полные required levels, money/risk/margin/exposure/transition/lot/snapshot gates. Margin0 не PASS. Это необходимо, но недостаточно для real execution: broker authenticity, актуальная ликвидность/цены/margin, actual fills, durable ownership и последовательное расходование не доказаны. SINGLE_LEVEL maxTransition имеет другой scope. Нельзя несколько последовательных шагов финансировать одним и тем же исходным Free; ReserveAfter_i=ReserveBefore_i-Consumed_i.

## R0F-05: три политики, без выбора по умолчанию

| Policy | После Fill1=-15, cap12 | После Fill2=+100 | Cap gate после2 |
|---|---|---|---|
| A current signed | net-15, loss15, breach | net85, loss0 | Численно проходит; не runtime permission |
| B sticky | breach=true | breach=true | Не проходит до approved reset |
| C peak | peak15 | peak15 | Не проходит при cap12 |

У A reset означает новую доказанную operation/window, не обнуление actual losses; у B нужен отдельный authorized reset event с причиной/политикой/history linkage; у C historical peak нельзя уменьшать произвольной сменой окна. Cap/policy фиксируются на operation: смена cap/version не может молча очистить breach. Complete independently ordered unique fills нужны B/C после restart; отсутствие префикса →UNAVAILABLE. A может оценить проверенный текущий net, но не доказывает отсутствие прошлых breaches. Порядок [+100,-15] даёт net85/peak0: нельзя переставлять broker events ради результата. Partial closes не обходят cap через новые локальные batch labels; operation/cycle membership independently confirmed. Стоимость A — cumulative net; B — плюс persistent breach/reset receipts; C — плюс peak/ordered history/checkpoints. Backend не реализуется.

Никакая A/B/C не выбрана. Все параметры tests — PROPOSED fixture policies; при policy=None model возвращает UNAVAILABLE. Реальное действие в R0F запрещено при любом cap gate.

## R0F-08: immutable allocation и mutable consumption

Immutable AllocationGrantRecord: logical source, AllocationID/EventID, allocation policy, currency/precision, eligible source receipt, OriginalGrant vector FinalReserve/PartialFar/Transition/Carry/Residual, phase/unallocated. Same source/event с FinalReserve50/Partial0→0/50 — CONFLICT, хотя total50. Mutable Consumed/Reserved/Free/owners/revision/journal — отдельный ConsumptionState: replay grant никогда не сбрасывает consumed. Same state revision с изменённым consumed/available — конфликт snapshot; легальный расход требует нового event/revision. PREPARED не расходуется. Подготовка — отдельный versioned draft/PreparationID, не изменяемый replay уже committed AllocationEventID. Final source allocation commit имеет полный immutable payload/manifest и Unallocated0. Если есть child allocations, source-level commit обязан атомарно покрыть их полный manifest; partial child не получает ресурс до полного group commit. Изменение draft не переписывает committed payload. Любая последующая transfer/rebalance policy требует нового события с conservation, а не повторного funding source. Нельзя выдавать residual/unallocated за permission to spend.

## R0F-09: ровно один раз и authority

In-memory idempotency — только память fixture. Immutable journal — payload/sequence/source binding; durability — проверяемый commit/recovery; CAS/concurrent authorization — отдельный backend atomicity; broker reconciliation и snapshot-content binding — независимые evidence. Ни одно не следует автоматически из другого. Expected строится из independently provided record/allocation/context, не presented proof. Исторический source plan не обязан равняться текущему consumption plan. Recovery reconstruction не новое spending permission.

Конкретные тесты: TEST_RESULTS.json TestIDs R0F-BALANCE-TRACE/MIGRATE-*/EXACT-REPLAY/ALTERED-REPLAY/PROJECTED-NOT-ACTUAL/SMALL-ONLY/ABSOLUTE-FAR/TRANSITION-A/B/C/BUCKET-PERMUTATION. Их scope — fixture algebra/encoders, не production money model.
