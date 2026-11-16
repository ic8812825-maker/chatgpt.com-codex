# HSBI-03E-A — D-06: Initial Profit, EconomicCyclePnL и RecoveryResult

Версия: **HSBI-03E-R1**. SOURCE_COMMIT_SHA=`b5ca9d377d454dfbec63ece76dd1c759abc3656d`.
Репозиторий `ic8812825-maker/chatgpt.com-codex`, ветка `work`, все относительные source paths внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.
Статус: **PROPOSED / AWAITING_OWNER_DECISION**. Ни один текст не APPROVED. Нормативный выбор, architecture/provider и implementation evidence — разные gates.
STATIC_REVIEWED означает чтение исходного текста; MATH_DERIVED — вывод при указанных предпосылках; COUNTEREXAMPLE_CONFIRMED — опровержение утверждения, не runtime PASS; HISTORICAL_TEST_RESULT — старый artifact; все новые vectors TEST_SPECIFIED_NOT_RUN; NATIVE_NOT_RUN. Новых compile/runtime/mutation/native tests не выполнялось.
UNAVAILABLE — обязательное evidence отсутствует; CONFLICT — доказательства противоречат; REJECT — доказанное нарушение домена/предусловия. Все три запрещают новый effect; финансовая delta=0. NO_OP возможен только по валидному полному старому receipt.
Публикация отчёта не утверждает контракт, не закрывает P0 и не разрешает production/R1.1/dispatch/trading.

D06_POLICY_STATUS=OPTIONS_READY_A_RECOMMENDED_AWAITING_OWNER.

## Точные источники и независимый вывод

- Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:16–20,28: completed Initial Plus, Initial Profit excluded из RealizedCycleNet и budgets.
- Docs/04_MATHEMATICAL_MODEL_RU.md:18,24,27,30: close-now, actual transition loss, threshold и buckets.
- Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6,9–24: signed components, opening/Initial не harvest, buckets не дополняют прибыль.
- Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md:5–17: единственная authority, result+coverage+freshness+actual completion.
- Docs/24_BROKER_MONEY_MODEL_RU.md:5–11; Docs/HSBI_DG01_CONTRACT_RESOLUTION_RU.md:85–99: costs, basis overlap, headroom.
- Docs/NEXT_STAGE_02B_R0F_MONEY_CONTRACT_CANDIDATE_RU.md:21–33: raw/posted/net separation, absolute Far, all-level.
- Reports/HSBI_MONEY_CONTRACT_PROPOSED_SPEC_RU.md:51–61 CF01–CF04; Reports/HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md:274–305; Reports/HSBI_03D_OWNER_APPROVAL_BALLOT_RU.md:150–169.
- Include/Money/HSBI_CostModel.mqh:11–18 HSBI_TryActualDealNet/HSBI_TryProjectedNetMoney.
- Include/Money/HSBI_MoneyTypes.mqh:6–9 HSBI_RecoveryPLSnapshot/HSBI_BuildRecoveryPL.
- Include/Money/HSBI_BasketMoneyEvaluator.mqh:7–18 HSBI_BasketLegInput/HSBI_EvaluateBasketMoney.
- Include/Money/HSBI_BrokerMoneyModel.mqh:6–20 HSBI_CalculateProjectedProfit.
- Include/Scenarios/HSBI_InitialLockTypes.mqh:4 initialProfitExcluded; HSBI_FinalCloseTypes.mqh:4 DTO only.

HSBI-03D не утверждённая норма. Текущий helper суммирует переданные realized+open и сравнивает threshold; он не устанавливает membership, независимый cost coverage или полный FinalClose. Наличие initialProfitExcluded bool не доказательство фактического исключения.

## Общий cost/membership contract для A и B

Определить один immutable CycleScopeID, account/currency/profile и independently associated экономические факты. EconomicSet(t) содержит все подтверждённые, уникальные actual postings этого scope: closing deals, отдельно отражённые opening commissions/fees, swap/correction postings при доказанной association. Opening posting не становится harvest source. Unknown association не пропускается как0.
R_all(t)=Σ unique actual net postings. Если компонент уже содержится в deal net, он не добавляется вторым posting. Signed rebates сохраняют знак.

O_phys(t)=close-now valuation actual remaining positions с физическими расходами, явно уже включёнными по CostCoverageMap.
C_rem(t)≥0 — ожидаемые физические debits, ещё не включённые ни в R_all, ни в O_phys. Если существуют будущие signed rebates, они имеют отдельный подтверждённый valuation component, а не отрицательный guessed cost.
EconomicCyclePnL E(t)=R_all(t)+O_phys(t)−C_rem(t).

Каждый CostFactID имеет source,component,includedIn,volume fraction,window,currency,posting status. Фактический cost находится ровно в одном месте. Spread в Ask-open/Bid-close и фактическая slippage в цене не вычитаются снова. Будущий incremental slippage допускается только по disjoint horizon. Уже actual swap/commission/fee не прогнозируется повторно. Новое начисление swap за будущий период — другой interval.

Существующая норма Docs04:18 включает execution buffer внутри open net, а Docs12:7 включает buffer в threshold. Это не основание молча удалить один из них. Ввести явно:
H_in≥0 — declared valuation headroom уже внутри legacy-compatible close-now result;
H_gate≥0 — threshold headroom;
Q(t)=E(t)−H_in;
Theta=MinimumRecoveryProfitMoney+H_gate+MoneyTolerance.
Если передан legacy openNet с буфером, H_in берётся из independent basis receipt; его нельзя угадывать из числа. Economic diagnostic E допускает add-back только именно подтверждённого headroom, не actual expense.
CostBasisManifest обязан указать IDs и назначение H_in/H_gate. Два отдельно утверждённых headroom layers могут быть консервативными и не являются двумя actual расходами. Если это один неразрешённо дублированный allowance или overlap unknown — UNAVAILABLE, а не автоматическая смена threshold/нормы. Пример ниже явно объявляет H_in4,H_gate5; это fixture, не broker default.

I(t) — подтверждённый InitialProfitExcludedNet из независимо установленного INITIAL_PLUS action group, с однократным attribution связанных signed costs. Допустим только положительный net завершённой INITIAL_PLUS group; не произвольная сумма положительных deals. Rollback/negative Initial events не исчезают, остаются в R_all. Неполная Initial group не позволяет вычислить окончательное I. До завершения Initial plan ordinary FinalClose блокирован; partial actual economics видны в E, positive prefix held/not harvest. Не вводится guessed I=0. Определение group/cost membership — явное proposed уточнение, подлежащее owner approval.

Correction/reversal,затрагивающий Initial group,append-only связывается с исходной group/receipt. Пока полный adjusted membership/cost receipt не проверен,dependent result UNAVAILABLE;старый I receipt не переписывается,а derived I(t) имеет отдельную revision/causation. Negative corrected group не превращается в исключаемую прибыль;loss остаётся в R_all. Это не auto-migration и не повторный source grant.

## Вариант A — сохранить Initial exclusion

### Полный нормативный текст D06-A/HSBI-03E-R1

> RecoveryRealized_A=R_all−I; RecoveryResult_A=Q−I=R_all−I+O_phys−C_rem−H_in. EconomicCyclePnL=E хранится отдельно и не используется вместо RecoveryResult_A для ordinary FinalClose. Initial Profit остаётся вне recovery и harvest budgets согласно Docs09. Все отрицательные/rollback экономические факты сохраняются. FinalCloseResultGate_A: RecoveryResult_A≥Theta. Threshold и остальные gates Docs12 не ослабляются. Нельзя прибавлять allocation buckets к E/Q/RecoveryResult. Missing Initial/cost/basis evidence → UNAVAILABLE. Ordinary authorization требует одновременно result gate, independently confirmed allowed coverage, freshness/ownership/revision, no pending/unknown, complete costs и safety policy. CLOSED только после actual fills,actual zero managed positions,exactly-once ledger,durable result. Emergency отдельна.

Scope: обычная Recovery/FinalClose policy; E — economic diagnostic/reconciliation, не funding inventory и не account Balance/Equity.
Инвариант E−H_in−RecoveryResult_A=I. При I≥0 R_A≤Q. Положительная E не отменяет отрицательный R_A.
Положительный vector: R_all100,O_phys−8,C_rem2 →E90;I50,H_in4 →R_A36;Theta10+5+1=16: result gate PASS при отдельно valid остальных gates.
Отрицательный: R_all40,O_phys−4,C_rem1 →E35;I50,H_in4 →R_A−19<16: REJECT, хотя E положительна.
Partial close: completed Initial I не меняется при закрытии других позиций. Economic facts пересекают open→realized один раз. При R_all20,O_phys30,C_rem2 E48; partial realizes gross12 with cost1→R_all31,O_phys18,C_rem1,E48. При неизменных I/H_in result тот же; это условный fixed-price/cost illustration, не обещание исполнения. Partial actual fills не означают CLOSED, pending блокирует новую обычную authority.
Partial INITIAL_PLUS: actual fees/losses учитываются в E; group не complete→Initial-exclusion unresolved→ordinary authorization BLOCKED, no guessed final I. После complete ассоциация и I фиксируются receipt; no grant creation.

Compatibility: A сохраняет explicit Docs09 exclusion и FinalClose result policy. Нужны будущие typed membership/cost maps; HSBI_BuildRecoveryPL не принимает эти facts и не доказывает conjunction. No production patch здесь.
Migration: исторические excluded flags/компоненты/partial associations сохраняются. Missing I/cost attribution quarantine; не вычитать весь initial phase и не заменять available balance.
Acceptance: exact duplicate source zero delta; I group sum/fee attribution independently checked; positive/negative/partial vectors; unchanged threshold examples; cost duplication rejection; no closure on partial/pending; native/provider/durability отдельно.

## Вариант B — явное включение Initial в recovery

### Полный нормативный текст D06-B/HSBI-03E-R1

> RecoveryRealized_B=R_all; RecoveryResult_B=Q=R_all+O_phys−C_rem−H_in. Все actual Initial economic postings входят ровно один раз, включая signed costs/rollback loss. Ordinary FinalClose result gate использует RecoveryResult_B≥Theta при неизменных остальных guards. Включение Initial в result не делает Initial Profit harvest/funding source: запреты grants/buckets Docs08:9 и Docs09 budget exclusions сохраняются, coverage independent. Прежний Initial-exclusion marker сохраняется как historical evidence и больше не вычитается только в новом versioned result. Нельзя вычислить R_B как R_all+I: R_all уже включает Initial. Все общие evidence/zero-delta/actual completion требования варианта A действуют.

Инвариант R_B−R_A=I для одинакового cost/scope/basis. Базовое множество R_all дедуплицировано по physical source+posting component; I не второе слагаемое income.
Положительный vector: E35,H_in4,I50 →R_B31≥16, тогда A−19 reject. Это фактическое ослабление Initial-exclusion policy, а не исправление арифметики.
Отрицательный: R_all10,O_phys−20,C_rem1 →E−11,H_in4 →R_B−15<16, хотя отдельный Initial profit может быть50. R_all уже содержит его и другие losses.
Partial close: общий пример E48 сохраняется при том же fixed basis; partial INITIAL_PLUS может входить в E/R_B по actual receipts, но Initial FSM/no-pending/ownership gates всё равно блокируют ordinary completion. Не освобождать profit grants из pending action.
Costs: общий coverage contract; никакого повторного I или component addition к уже net deal. При 60−2−7−1 net50 →R_all contribution50,не110 и не40.
Migration: новый PolicyEpoch/ResultBasisVersion, полный recomputation из immutable source set и migration receipt. Не переписывать old verdict/expected,не retroactively объявлять ранее rejected CLOSED. Нет полного set→UNAVAILABLE. Old approved plans не переводятся B автоматически.
Acceptance: paired A/B vectors,R_B−R_A=I,Initial grants remain0,coverage still mandatory,all costs exactly once,partial/restart/epoch migration tests.

### Какие нормы потребуют отдельного замещения при B

| Источник | Необходимое будущее изменение |
|---|---|
| Docs09:16,20,28 | Только exclusion из RealizedCycleNet/result и Initial result marker semantics; budget/harvest запреты сохраняются |
| Docs04:18,27 | Определить versioned R_B/membership и cost/headroom basis явно |
| Docs08:21 | FinalClose result с новым membership; DealNet/bucket conservation неизменны |
| Docs12:7,13,17 | Название/definition result, paired policy examples; guards/lifecycle не ослабляются |
| HSBI-03D D06 и proposed CF01–CF03 | Не редактировать историю; новое owner decision явно overrides только выбранный scope |
| Future Tests/Contracts | Новая versioned expectation group; старые frozen expected неизменны |

Этот audit не изменяет ни одну строку перечисленных sources.

## Рекомендация и готовое решение владельца

Рекомендуется A: единственная явно действующая Initial норма исключает profit; объективного доказательства, что стратегическая policy должна измениться на B, нет. B математически непротиворечив при приведённом set accounting, но меняет допустимые FinalClose decisions и требует отдельного согласия. Ни A,ни B не гарантируют future realized profit на gap.

Текст выбора: «Выбираю D-06 вариант A [либо B] версии HSBI-03E-R1, с полным общим cost/membership contract и указанным scope. Используемый ordinary FinalClose показатель — RecoveryResult_A [либо B], не EconomicCyclePnL и не сумма buckets. Разрешаю лишь нормативное замещение перечисленного scope после фиксации точных commit/blob версий. Production/R1.1/trading не разрешаю».
OwnerDecision=AWAITING. Отдельный CostBasisManifest с I membership/H_in/H_gate и provider evidence обязателен; без него implementation gates BLOCKED.

Unresolved: выбор A/B; actual Initial group/cost association; headroom coverage/profile; native/domain,receipt registry и durable backend.
Проверка: [numeric vectors](HSBI_03E_NUMERIC_TEST_VECTORS_RU.md),[dependency bundles](HSBI_03E_CONTRACT_DEPENDENCY_RECONCILIATION_RU.md),[owner ballot](HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md),[R11 gates](HSBI_03E_R11_GATE_MATRIX_RU.md).
