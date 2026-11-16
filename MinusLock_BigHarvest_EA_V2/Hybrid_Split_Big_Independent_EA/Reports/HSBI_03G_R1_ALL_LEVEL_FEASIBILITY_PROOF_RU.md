# HSBI-03G-R1 — доказательство all-level feasibility

DocumentVersion=HSBI-03G-R1-V1
SourceCommitSHA=e68e73e1b252d20e15588645004f9066c6ae88f0
Scope=HSBI_CR09_ALL_REQUIRED_V1 / mathematical predicates
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=PROPOSED_AWAITING_OWNER_APPROVAL
Dependencies=RequiredLevel manifest; quantity; cost/source/snapshot/numeric bundles

Репозиторий: `ic8812825-maker/chatgpt.com-codex`, ветка `work`. Все пути ниже находятся внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`. Новый текст является проектом контракта, а не утверждением реализации. Выбор D-06 A и companion NewFar A сохраняется; полный CR-09 не утверждён. Формальных approval receipts нет.

PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.

UNAVAILABLE означает отсутствие обязательного доказательства; CONFLICT — противоречие данных; REJECT — доказанное нарушение. Каждый результат запрещает новый финансовый эффект, delta=0. NO_OP допустим только после проверки подлинного полного прежнего event body и receipt. Числа математических примеров не являются брокерскими константами.

## Source-level граница

- [Include/Planning/HSBI_FutureSmallProofAggregator.mqh:28–56](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallProofAggregator.mqh#L28-L56) — HSBI_AggregateFutureSmallProof. SourceBlobSHA=`4678ae152960e98b9f398b4497786061d7e8a524`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_NewFarSolver.mqh:114–146](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L114-L146) — HSBI_SolveNewFar. SourceBlobSHA=`3d19eccd6cd318b9b4591e2bc0ccaa95f661930d`; EvidenceClass=STATIC_REVIEWED.
- [Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24–75](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_ReserveCatchUpEvaluator.mqh#L24-L75) — validators / HSBI_EvaluateReserveCatchUp. SourceBlobSHA=`87a8b7e97727ce6e47c2a2f0abc3e237f6203204`; EvidenceClass=STATIC_REVIEWED.
- [Include/Money/HSBI_CostModel.mqh:11–18](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_CostModel.mqh#L11-L18) — actual / projected net. SourceBlobSHA=`293a22c0ff14bc6d635e0cc50c79c8e3d4a7d5cd`; EvidenceClass=STATIC_REVIEWED.
- [Reports/HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md:24–155](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md#L24-L155). SourceBlobSHA=`fa093a00c2887f92da6a8436b0e1c6b1ed32905d`; EvidenceClass=STATIC_REVIEWED.

Producer и aggregator не вычисляют per-level CatchUpMargin. NewFar делает 0 либо1 CatchUp call на candidate после control selection. catchUpProofValid=true относится к одному вызову; allMoneyProofsValid означает валидность money calculations, не all-level positive margin. ERR018=OPEN_CONTRACT_GAP; implementation gap относительно all-required target статически подтверждён. Native unsafe SELECTED не установлен; новый P0 не объявляется.

## Предлагаемый полный предикат

Пусть R — frozen required IDs, X — required execution prefixes.

```text
CandidateFeasible(c) = ManifestApprovedAndBound
 AND ProofCompleteness=COMPLETE
 AND forall l in R: LevelProofValid(l) AND QuantityBindingValid(l)
 AND forall l in R: TransitionUpper(l) <= FrozenCap(l)
 AND forall l in R: CatchUpMarginLower(l) > 0
 AND CostCoverageComplete
 AND SourceIdentityAndSnapshotAuthorityValid
 AND forall x in X: FundingPrefixValid(x)
 AND GeometryRiskMarginCompressionTerminalAndOtherSafetyGatesPass
```

PreviewFeasible и FundingAuthorized — отдельные результаты. PREVIEW_ONLY не даёт dispatch/reservation/consumption. Вывод для finite scope не распространяется на обязательный unknown tail. ManifestApprovedAndBound — будущее необходимое условие; сегодня оно не выполнено.

В exact fixture M_l=G_l−A_l−B_l, M_min=minR M_l. Для конечного непустого R эквивалентны ∀l M_l>0 и M_min>0. Пустой required set запрещён; vacuous success недопустим. T_max≤H эквивалентно per-level T_l≤H лишь при общем H и полном R; разные caps проверяются отдельно.

Если G∈[G_low,G_up],A∈[A_low,A_up],B∈[B_low,B_up], то M≥G_low−A_up−B_up=M_low. M_low>0 достаточно для strict CatchUp при доказанных bounds. M_low≤0 не даёт guarantee, даже при positive nominal. Неутверждённые bounds →NUMERIC_EVIDENCE_UNAVAILABLE.

Пример: nominal G12.001,A11,B1 даёт0.001; интервалы G[11.999,12.003],A[10.999,11.001],B[1,1.001] дают lower−0.003. Нет positive proof. Exact G12,A11,B1 даёт0, отказ. Нельзя заменить >0 на ≥0/отрицательный epsilon.

## Согласованный контрпример extrema

MODEL_LINEAR_1: BUY gross=v(P−open),SELL gross=v(open−P), coefficient1. Все opens100; Bid=Ask=P; Far/Small SELL, Core/Trend BUY. Core=3F,Trend=F,Small=F. Grid/min0.05,max10. B_leg1 каждому leg; signed commission Far=−f,Small=−s; прочие costs0. Дополнительный B_CU1 — отдельный declared headroom, не вторая физическая комиссия.

При x=F(P−100): FarNet=−x−f−1;CoreNet=3x−1;TrendNet=x−1;SmallNet=−x−s−1;BasketNet=2x−f−s−4. Core-only preview share0.8: G=0.8max(0,CoreNet),A=max(0,−FarNet),M=G−A−1.

| Level | F/Fafter | P | f/s | Far/Core/Trend/Small net | BasketNet | T | G | A | M |
|---|---|---:|---|---|---:|---:|---:|---:|---:|
| L1 |0.4/0.2|125|2.2/25.8|−13.2/29/9/−36.8|−12|12|23.2|13.2|9|
| L2 |0.2/0.1|125|8.2/4.8|−14.2/14/4/−10.8|−7|7|11.2|14.2|−4|
| L3 |0.1/0.05|150|2.2/6.8|−8.2/14/4/−12.8|−3|3|11.2|8.2|2|

Набор M_MINUS. Все volumes на grid, compression ratio0.5; recovery растёт −12→−7→−3, initial−20. Условный margin10×gross=24/12/6≤100; conditional risk90/80/70 при initial100,tolerance1. Это local mathematical premises, не runtime broker/risk authority.

argmaxT=L1, argminM=L2. WORST_CASE проверяет L1 и получает9>0, но all-required minimum−4 отвергает candidate. Следовательно max Transition не определяет min CatchUp. Таблица выведена из legs/costs, не произвольно назначенных итогов.

M_PLUS меняет L2 f3.2,s9.8: Basket−7,Far−9.2,Small−15.8,M2=1 → margins9/1/2. M_ZERO: f4.2,s8.8 →Far−10.2,Small−14.8,M2=0 →отказ. Смена компонентов требует новых original cost receipts, даже при тех же IDs/net basket.

### Достижимость и ограничения

Это coherent projected valuation model, не физическая история successive promotion: template повторяет direction/open prices, Docs13 требует actual Core lineage. Верхний solver отклоняет injected/unit-test input; арифметическая модель не доказывает successful native route. Current FINAL_LEVEL с constantN0.4 отвергает L3 по quantity0.24≤0.4; этот маршрут не объявляется passing.

Producer требует strict recovery growth, откуда T_(l+1)≤T_l. Поэтому растущий T=(3,7,12) не является genuine producer witness. Public DTO с flags не доказывает достижимость такого состояния через producer.

Constant independently stipulated reserve14.5 даёт margins0.3/−0.7/5.3, снова разные extrema. Для alternative valuations это не debit; sequential consumption требует inventory prefix. Basket reserveGain=max(Core+Trend+Small,0) не равен Core-only G NewFar: eligibility нельзя изменить без выбора владельца.

Каждый cost fact имеет одного inclusion owner. B_leg уже входит в leg net; B_CU допустим только при доказанной другой цели/headroom. Unknown overlap →COST_BASIS_UNBOUND. Unknown identity/snapshot оставляет численную диагностику PREVIEW_ONLY, authority UNAVAILABLE.

OpenQuestions: level semantics/Far obligation/eligible set; actual cost/numeric/authority receipts; tail и funding prefixes.
AcceptanceCriteria: независимый exact milli-unit пересчёт; zero/interval boundaries; все required predicates сохраняются при unknown; positive scalar не выдаёт funding permission.

Связи: [metrics](HSBI_03G_R1_TRANSITION_CATCHUP_METRIC_SCHEMA_RU.md), [funding](HSBI_03G_R1_RESERVE_FUNDING_AUTHORITY_RU.md), [vectors](HSBI_03G_R1_QUALIFICATION_TEST_SPEC_RU.md).
