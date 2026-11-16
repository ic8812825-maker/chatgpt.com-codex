# HSBI-03G-R1 — reserve, funding authority и расходы

DocumentVersion=HSBI-03G-R1-V1
SourceCommitSHA=e68e73e1b252d20e15588645004f9066c6ae88f0
Scope=HSBI_RESERVE_FUNDING_AUTHORITY_V1
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=PROPOSED_AWAITING_OWNER_APPROVAL
Dependencies=D-01/02/03/06/07/08/10/11/12/13/14/16; CR-09

Репозиторий: `ic8812825-maker/chatgpt.com-codex`, ветка `work`. Все пути ниже находятся внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`. Новый текст является проектом контракта, а не утверждением реализации. Выбор D-06 A и companion NewFar A сохраняется; полный CR-09 не утверждён. Формальных approval receipts нет.

PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.

UNAVAILABLE означает отсутствие обязательного доказательства; CONFLICT — противоречие данных; REJECT — доказанное нарушение. Каждый результат запрещает новый финансовый эффект, delta=0. NO_OP допустим только после проверки подлинного полного прежнего event body и receipt. Числа математических примеров не являются брокерскими константами.

## Граница текущего кода

- [Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24–75](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_ReserveCatchUpEvaluator.mqh#L24-L75) — HSBI_EvaluateReserveCatchUp / validators. SourceBlobSHA=`87a8b7e97727ce6e47c2a2f0abc3e237f6203204`; EvidenceClass=STATIC_REVIEWED.
- [Include/Money/HSBI_ReserveAllocationTypes.mqh:15–30](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_ReserveAllocationTypes.mqh#L15-L30) — allocation/consumption shape. SourceBlobSHA=`f1464320f1f853f12f8e3f3ddc3708bad2a0cd4d`; EvidenceClass=STATIC_REVIEWED.
- [Include/Money/HSBI_EconomicLedgerTypes.mqh:5–12](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_EconomicLedgerTypes.mqh#L5-L12) — source key/equality. SourceBlobSHA=`e589337d228323dba278b242d01e61fc0ee733fe`; EvidenceClass=STATIC_REVIEWED.
- [Include/Money/HSBI_AllocationLedgerTypes.mqh:5–10](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_AllocationLedgerTypes.mqh#L5-L10). SourceBlobSHA=`87f86ec7498bd115f5a21da34d596c0ce0c2170a`; EvidenceClass=STATIC_REVIEWED.
- [Include/Persistence/HSBI_ExecutionJournal.mqh:25–43](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Persistence/HSBI_ExecutionJournal.mqh#L25-L43). SourceBlobSHA=`e65d6d9b0f04a3e236952ec577ea144bf57ee2b2`; EvidenceClass=STATIC_REVIEWED.
- [Include/Persistence/HSBI_PersistenceInterface.mqh:4–7](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Persistence/HSBI_PersistenceInterface.mqh#L4-L7) — stubs. SourceBlobSHA=`36b7181f50fe4554d24f9ea6813906f9f4240d49`; EvidenceClass=STATIC_REVIEWED.

Validator требует projected&&!actual. runtimeConfirmed — флаг расчёта, не подтверждение средств. Allocation shape и один priorConsumptionKey не являются global inventory. Allocated branch не повторяет share, но rejects any consumed>0; это не partial-Free модель. Unallocated branch не имеет такого же guard. Atomic registry/reservations не запрашиваются. Pure repeated preview не расходует деньги; runtime double-spend не объявляется доказанным одним повтором вызова.

## Полномочия

PREVIEW_ONLY содержит conditional G/A/M, manifest и cost/quote/risk profiles; FinancialPermission=NO. Будущий projected income не становится asset из-за positive number/hash/bool. FUNDING_AUTHORITY — отдельный подлинный provider receipt по independently associated broker history, source registry и durable journal. Он подтверждает physical source, actual posted components, currency/profile, eligibility, remaining Free и atomic reservation. Без provider →UNAVAILABLE/PROVIDER_BLOCKED. Выбор D06/NewFar не назначает authority.

## Source identity и conservation

PhysicalSourceKey логически включает BrokerIdentity,ServerIdentity,AccountIdentity,immutable deal/posting identifier и component/subposting kind. EventID обозначает доставку/causation, не новый income. Другой event ID при повторном импорте одной сделки не создаёт source. Correction/reversal — новый связанный append-only fact, не изменённый body. Record содержит symbol/cycle/position/action association и signed components. Account/server/source исключают совпавшие tickets разных счетов.

SourceOriginPlanID и CurrentConsumptionPlanID разделены: carry association может законно связывать разные планы. AllocationKey — распоряжение источником, не source. Новый AllocationKey не восстанавливает grant.

Для положительного eligible source committed conservation имеет ровно пять категорий: G_source=C+P+T+K+R, где C=FinalReserve grant, P=PartialFar grant, T=Transition grant, K=Carry grant, R=Residual/unallocated grant. Буква C в этой формуле не означает lifecycle Consumed. Draft может иметь отдельный ещё не классифицированный U: G_source=C+P+T+K+R+U; commit требует U=0 с явным включением остатка в R. Residual не добавляется второй раз как отдельный Unallocated. Draft U не spendable. Grants и lifecycle states нельзя складывать как разные деньги.

Для bucket b: Grant_b=Consumed_b+Reserved_b+Free_b; states≥0, одна currency/profile, checked exact arithmetic. Spend d≤Free: Free'=Free−d,Consumed'=Consumed+d. Reservation a≤Free: Free'=Free−a,Reserved'=Reserved+a. Reservation commit переносит Reserved→Consumed без повторного debit Free. Release возвращает только unused Reserved. Cancellation не отменяет confirmed consumption. Transfer атомарно меняет разрешённые donor/recipient balances без source inflation. Corrections ниже committed obligations дают debt/conflict/reconciliation, не отрицательный Free или переписывание history.

Unknown broker history и quarantined legacy records не дают grant. Restart блокирует funding до ordered journal recovery и независимой reconciliation; неизвестное spending не считается нулём.

## Обязательные свойства atomic registry — пока не реализованы

Нужны unique physical-source index, full immutable body comparison, eligibility/account/currency checks, source+bucket revisions, compare-and-swap reserve/consume/release, durable intent/outcome, crash reconciliation и взаимное исключение конкурирующих owners. Нельзя разделять check Free и commit так, чтобы между ними другой consumer мог потратить source. Unknown outcome требует reconciliation, не blind retry.

Receipt связывает PhysicalSourceKey, AllocationKey, EventID, ConsumerID, SourceOriginPlanID, CurrentPlanID, StateRevision, RegistryRevisionBefore/After, amount/currency/profile, prefix/action scope и original body. Same authentic event/body/outcome→NO_OP delta0. Same event/altered component при том же net→CONFLICT. Два конкурирующих commits с expected revision5: не более одного; второй не использует cached Free.

Reference R_AUTH, не реальный provider: source18.125 XTEST3,scale1000,share0.8;ReserveGrant14.500,residual3.625,C0/R0/F14.500,rev5. e1 debit9 expected5→C9/F5.5/rev6. e2 debit9 expected6→INSUFFICIENT_FREE delta0; expected5→REVISION_CONFLICT. Replay e1/body9→NO_OP; e1/body8.999→CONFLICT; AllocationAliasA999 не новый grant. Для взаимоисключающих valuations9/9 inventory14.5 покрывает каждую только при доказанном exclusivity; sequential debit18 недопустим.

## CostBasisManifest

- [Include/Money/HSBI_CostModel.mqh:11–18](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_CostModel.mqh#L11-L18) — actual/projected net. SourceBlobSHA=`293a22c0ff14bc6d635e0cc50c79c8e3d4a7d5cd`; EvidenceClass=STATIC_REVIEWED.
- [Include/Money/HSBI_BasketMoneyEvaluator.mqh:7–18](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_BasketMoneyEvaluator.mqh#L7-L18) — leg buffers / basket totals. SourceBlobSHA=`4bea204e91a4719b4b24086304cb51051909a7de`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_NewFarSolver.mqh:119–127](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L119-L127) — Core eligibility / CatchUp buffer. SourceBlobSHA=`3d19eccd6cd318b9b4591e2bc0ccaa95f661930d`; EvidenceClass=STATIC_REVIEWED.

Каждый CostFactID имеет physical source, signed amount/component/interval, position/action volume fraction, actual/projected stage, includedIn metric, remaining flag и original receipt. Actual net=profit+signed commission+swap+fee; rebate сохраняет знак. Spread в Ask/Bid/open/close не вычитается снова. Actual slippage в fill price не повторяется отдельным debit. Future incremental slippage разрешается только по disjoint horizon. Swap уже учтённого interval не прогнозируется повторно. Membership costs частичного закрытия требует доказательства, не произвольной пропорции.

Текущий Basket передаёт B_leg каждой из четырёх legs. B_CU и D06 H_in/H_gate должны иметь disjoint purpose либо отдельно утверждённые conservative headroom layers. Headroom не второй actual expense. Один physical cost нельзя сделать двумя разными переименованием IDs. Unknown overlap→COST_BASIS_UNBOUND, не наиболее выгодный net.

D06 A исключает InitialProfit из recovery/harvest eligibility; negative Initial results и расходы остаются в E. Positive EconomicCyclePnL/BigHarvest/Core projection не доказывают funding inventory. Small и BigReserve не объединяются молча. Eligible Core/Trend/иные sources требуют выбора владельца; поддержка BIG_TREND validator не означает фактическое суммирование Trend текущим NewFar.

## Snapshot authority

Original receipt связывает broker/server/account/symbol/cycle/position/event, full market/cost content, revision, clock epoch, issue/expiry/skew. Fresh=true без authority→UNAVAILABLE. Тот же ID с другим content→CONFLICT. Future timestamp вне approved skew, другой account, missing position, restart без reconciliation→отказ/UNAVAILABLE. Сам hash выявляет отличие, но не доказывает подлинность. Нельзя переписать identity и сравнить её с только что созданным expected как независимое source evidence.

OpenQuestions: CR09-SUB-05…10; actual provider/clock/journal; eligible sources; cost/rounding profiles и owner approvals.
AcceptanceCriteria: SOURCE/FUNDING/COST/SNAPSHOT qualification; conservation при reservation/release/transfer/correction/restart; изменение DTO/plan/event не создаёт денег.

Связи: [scope](HSBI_03G_R1_CR09_REQUIRED_LEVEL_CONTRACT_RU.md), [ballot](HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md), [gates](HSBI_03G_R1_FINAL_READINESS_VERDICT_RU.md).
