# HSBI-03G-R1 — типизированная схема TransitionLoss и CatchUp

DocumentVersion=HSBI-03G-R1-V1
SourceCommitSHA=e68e73e1b252d20e15588645004f9066c6ae88f0
Scope=MetricSchema=HSBI_TRANSITION_CATCHUP_METRICS_V1
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=PROPOSED_AWAITING_OWNER_APPROVAL
Dependencies=D-04/06/08/10/11/12/13/15; TL001; CR-09

Репозиторий: `ic8812825-maker/chatgpt.com-codex`, ветка `work`. Все пути ниже находятся внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`. Новый текст является проектом контракта, а не утверждением реализации. Выбор D-06 A и companion NewFar A сохраняется; полный CR-09 не утверждён. Формальных approval receipts нет.

PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.

UNAVAILABLE означает отсутствие обязательного доказательства; CONFLICT — противоречие данных; REJECT — доказанное нарушение. Каждый результат запрещает новый финансовый эффект, delta=0. NO_OP допустим только после проверки подлинного полного прежнего event body и receipt. Числа математических примеров не являются брокерскими константами.

## Доказанный разрыв семантики

- [Include/Money/HSBI_BasketMoneyEvaluator.mqh:7–18](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_BasketMoneyEvaluator.mqh#L7-L18) — HSBI_BasketLegInput / HSBI_EvaluateBasketMoney. SourceBlobSHA=`4bea204e91a4719b4b24086304cb51051909a7de`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_NewFarSolver.mqh:118–151](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L118-L151) — HSBI_SolveNewFar. SourceBlobSHA=`3d19eccd6cd318b9b4591e2bc0ccaa95f661930d`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_NewFarCandidate.mqh:7–15](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarCandidate.mqh#L7-L15) — candidate DTO. SourceBlobSHA=`758f1c89cf75701d3616dabec2fcb06413ee2d4a`; EvidenceClass=STATIC_REVIEWED.
- [Reports/HSBI_03F_R2_TL001_REGISTERED_FINDING_RU.md:1–105](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_TL001_REGISTERED_FINDING_RU.md#L1-L105). SourceBlobSHA=`8de58af1d808cc8d04816e46e77d59f45a7a49a0`; EvidenceClass=STATIC_REVIEWED.

Cap использует aggregate.maximumTransitionLoss (131), candidate хранит aggregateWorstTransitionLoss (138), но successful return transitionLoss получает selected.farLossIncreaseMoney (151). Это absolute Far loss control level из122/141, не basket maximum. T_max≠A_control в общем случае. Gate выполняется до safe[] (134/146): строка возврата сама по себе cap не обходит. TL001 остаётся CONFIRMED_STATIC/P1_PROPOSED, без official ERR-ID и без исправления.

## Проект типов и формул

| MetricKind | Формула | Scope / ValueKind / source |
|---|---|---|
| ActualTransitionLoss | max(0,−Σ unique actual closing net postings) | Actual TransitionActionGroup, CONFIRMED_ACTUAL; source set с signed fees |
| ProjectedBasketTransitionLoss_l | T_l=max(0,−BasketNet_l) | LevelID, PROJECTED; declared basket legs на одном valuation basis |
| MaximumProjectedTransitionLoss | T_max=max(l∈R)T_l | Frozen RequiredLevelSetID, PROJECTED; только COMPLETE set |
| ControlLevelAbsoluteFarLoss | A_c=max(0,−FarCloseNet_c) | ControlLevelID + FarObligationKind/position/volume; actual требует отдельного actual metric |
| ReserveGainMoney_l | G_l=share_l×Eligible_l для unallocated preview; либо bound allocated amount без второго share | LevelID, PREVIEW_ONLY; funding требует отдельного registry receipt |
| CatchUpMarginByLevel_l | M_l=G_l−A_l−B_l | LevelID; B disjoint с уже включёнными costs |
| MinimumCatchUpMargin | min(l∈R)M_l | Frozen RequiredLevelSetID; не control scalar |

ActualTransitionLoss не является historical peak и не стирает sticky breach D05. Actual loss/T_l не равны incremental Far deterioration автоматически. В net закрываемой части Core входит только доказанное membership; вся projected Core не становится actual income частичного закрытия.

Каждый тип содержит MetricKind, ValueKind, Value/LowerBound/UpperBound, CurrencyCode, NumericProfileVersion, CostBasisVersion, LevelID либо RequiredLevelSetID, ScopeID, SourceReferences, SnapshotReferences, ProofVersion, OriginalReceiptBinding. Обязательны Unit, Position/Role/Direction/VolumeBinding, PlanVersion, StateRevision, CalculationStage, а для funding — RegistryRevision/AuthorityID/ClockEpoch/Expiry. Одинаковое число при разных kinds/scopes не взаимозаменяемо.

RequiredLevelCount=|R|, ProvenLevelCount=|P∩R| и ProofCompleteness публикуются отдельно. При неполном R qualified minimum/maximum отсутствуют; допустимы только PREFIX_ONLY diagnostics. Ноль не кодирует unknown. Все суммы имеют currency/profile; ни одна positive projected сумма не является grant.

## Numeric domain и пограничные условия

Settled amount — checked signed64 minor units по утверждённой currency/posting policy D10/11. Диапазон int64: −9223372036854775808…9223372036854775807. Negation/abs(INT64_MIN) переполняется: loss +9223372036854775808 не представим, требуется OVERFLOW/UNAVAILABLE, не wrap/clamp. Сложение/multiply/scale/round проверяются до операции; CurrencyDigits не выводятся из SYMBOL_DIGITS. Конкретный профиль ещё EVIDENCE_BLOCKED.

Projected calculations используют утверждённый floating/interval profile. NaN/Infinity запрещены; negative zero нормализуется только по codec policy; underflow/rounding не превращают unknown в M>0. F64Z остаётся кандидатом; binary64 roundtrip/UTF-8/length/version qualification D12/15 NOT_RUN. Digest representation не даёт source authority.

TL-01: BasketNet=(−12,−2),FarNet=(−3,−2) → T_max12,A_control3; cap12 проходит equality. TL-02: BasketNet=(−3,−1),FarNet=(−12,−6) → T_max3,A_control12; cap5 сравнивается с3, coverage с12. Новая схема содержит оба числа и оба scopes. Достижение successful return в native integration не доказано.

## D-06 A сохраняется

- [Reports/HSBI_03E_D06_POLICY_RESOLUTION_RU.md:28–65](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03E_D06_POLICY_RESOLUTION_RU.md#L28-L65). SourceBlobSHA=`39342ea57a83a8dcd2f8e22ff8b87747c371d0ca`; EvidenceClass=STATIC_REVIEWED.

R_all=Σ unique actual net postings; E=R_all+O_phys−C_rem; Q=E−H_in; RecoveryRealized_A=R_all−I; RecoveryResult_A=Q−I. Инвариант E−H_in−RecoveryResult_A=I. FinalClose result gate: RecoveryResult_A≥MinimumRecoveryProfitMoney+H_gate+MoneyTolerance. E не подменяет recovery или funding inventory. Reserve buckets не прибавляются к E второй раз. CostBasis/I/H_in/H_gate требуют evidence; отсутствие →UNAVAILABLE. Emergency liquidation отдельно, не successful recovery.

## API, legacy и downstream

Предлагаются ResultSchemaVersion=TRANSITION_CATCHUP_RESULT_V1 и ProofSchemaVersion=CR09_PROOF_V1 с immutable receipts. Для явно установленной legacy schema поле HSBI_NewFarSolverResult.transitionLoss на successful route маркируется CONTROL_ABSOLUTE_FAR_LOSS, не MAX_BASKET_TRANSITION_LOSS. Это описание старого значения, не его переопределение. Нет достоверной schema/control scope →UNSUPPORTED/QUARANTINE. Старые persisted plans/expected не переписываются.

- [Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:11–17](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Runtime/HSBI_RuntimeDecisionTypes.mqh#L11-L17) — runtime DTO. SourceBlobSHA=`0cc2619ed6ce7a93ea28c3c655a8d147e18a9231`; EvidenceClass=STATIC_REVIEWED.
- [Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:19–28](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Runtime/HSBI_RuntimeDecisionValidator.mqh#L19-L28) — runtime validation. SourceBlobSHA=`aecbf35e7ced9fd756d80803c63626b9b52c0846`; EvidenceClass=STATIC_REVIEWED.

Прочитанные runtime DTO используют candidate/aggregate/catchup отдельно. Новый внешний consumer solver result здесь не доказан; это NOT_FOUND_IN_SCANNED_SCOPE, не заявление об отсутствии во всём проекте. R2 содержит более широкий исторический xref; текущий этап не выдаётся за новый exhaustive scan74 модулей. Возможный будущий адаптер, принимающий Far loss за checked maximum, остаётся контрактным риском.

OpenQuestions: numeric/profile/codec/native evidence; actual membership; legacy schema и conversion rules.
AcceptanceCriteria: TL01/02 сохраняют оба значения и scopes; unknown legacy fail-closed; missing proof не становится0; exact settled/projected interval разделены.

Связи: [feasibility](HSBI_03G_R1_ALL_LEVEL_FEASIBILITY_PROOF_RU.md), [qualification](HSBI_03G_R1_QUALIFICATION_TEST_SPEC_RU.md).
