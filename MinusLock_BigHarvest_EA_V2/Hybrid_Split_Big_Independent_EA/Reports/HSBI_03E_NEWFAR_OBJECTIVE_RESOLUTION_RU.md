# HSBI-03E-B — NewFar objective: minimum-safe-first и risk-first

Версия: **HSBI-03E-R1**. SOURCE_COMMIT_SHA=`b5ca9d377d454dfbec63ece76dd1c759abc3656d`.
Репозиторий `ic8812825-maker/chatgpt.com-codex`, ветка `work`, все относительные source paths внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.
Статус: **PROPOSED / AWAITING_OWNER_DECISION**. Ни один текст не APPROVED. Нормативный выбор, architecture/provider и implementation evidence — разные gates.
STATIC_REVIEWED означает чтение исходного текста; MATH_DERIVED — вывод при указанных предпосылках; COUNTEREXAMPLE_CONFIRMED — опровержение утверждения, не runtime PASS; HISTORICAL_TEST_RESULT — старый artifact; все новые vectors TEST_SPECIFIED_NOT_RUN; NATIVE_NOT_RUN. Новых compile/runtime/mutation/native tests не выполнялось.
UNAVAILABLE — обязательное evidence отсутствует; CONFLICT — доказательства противоречат; REJECT — доказанное нарушение домена/предусловия. Все три запрещают новый effect; финансовая delta=0. NO_OP возможен только по валидному полному старому receipt.
Публикация отчёта не утверждает контракт, не закрывает P0 и не разрешает production/R1.1/dispatch/trading.

NEWFAR_OBJECTIVE_STATUS=AB_READY_A_RECOMMENDED_AWAITING_OWNER.
Companion PolicyId=NEWFAR-OBJECTIVE; это выбор внутри CR-09/integration, не семнадцатый monetary CanonicalDecisionId.

## Источники

Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9–23 (ascending grid,feasibility,minimum-safe-first); Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3–7,19–37 (risk-first,proof completeness); Docs/04_MATHEMATICAL_MODEL_RU.md:15,21–36; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6–18; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md:3–7.
Include/Planning/HSBI_NewFarCandidate.mqh:26–40 HSBI_IsCompleteCandidateProof/HSBI_CompareCandidateTieBreak.
Include/Planning/HSBI_NewFarSolver.mqh:94–151 HSBI_SolveNewFar;119–124 identity construction;149 selection.
Include/Planning/HSBI_FutureSmallProofAggregator.mqh:23–58 HSBI_AggregateFutureSmallProof;50 selects max-transition level.
Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24–76 HSBI_EvaluateReserveCatchUp.
Reports/HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md:370–401; HSBI_03D_CONTRACT_CONSISTENCY_MATRIX_RU.md:56–71.

Code comparator соответствует Docs29, а title/step14 Docs14 — minimum-safe. Новизна Docs29 сама по себе не доказательство owner override Docs14. Нельзя выдать existing code за стратегическое утверждение.

## Feasibility F(c) до objective — одинаковая для A и B

Для immutable input/plan/grid/basis:
1. Independent actual original BIG_CORE residual ownership; one Far;0<N<F; valid grid,min/max,compression lots/ratio,maximum N/F.
2. Каждый required level L и каждый обязательный intermediate execution prefix имеют complete nonproxy money/margin/risk/cost/source/snapshot proof и одинаковые approved profiles.
3. RiskNext<RiskOld−RiskTolerance на одном basis; margin/free margin/drawdown/exposure limits; pointwise recovery monotonicity,geometry,slope,operational terminal semantics.
4. TransitionLoss_l=max(0,−signed actual/projection net on declared basis)≤frozen min4caps; sticky breach D05 запрещает ordinary continuation. AbsoluteFarLoss_l отдельно max(0,−FarCloseNet_l),не TransitionLoss.
5. CatchUpMargin_l=EligibleReserveGain_l−AbsoluteFarLoss_l−DisjointBuffer_l>0 для КАЖДОГО required l; m(c)=min_l margin_l. Для already allocated preview gain берётся связанный amount без второго share; actual funds требуют independent confirmed free source. Projected positive gain не funding.
6. Required future prefix consumes по source inventories без повторного spending одного Free; preview будущего source помечен conditional,не asset. Full future set и any tail theorem explicit; finite L не доказывает unchecked tail. Missing tail proof,если он required Doc14:19–21, не становится feasible из-за objective.
7. Actual post-fill residual повторно проверяется перед promotion; selected preview не promotion permission.

F(c) — conjunction,а не weighted penalty. Unsafe candidates полностью исключены. Не менять guards/caps/cost basis ради более красивого rank. CatchUp margin0 не PASS.

## Точные варианты

### A — MINIMUM_SAFE_V1

Полный proposed текст:
> Сначала построить полный declared candidate set и выполнить одинаковую F(c) для всех required proofs. Среди feasible normalized grid volumes выбрать lexicographic minimum tuple (N,RiskNext,MarginNext,FutureTransitionCount,−m(c),CanonicalCandidateTieID). Это minimum-safe-first. При одинаковом N сохраняются Doc14 risk/margin/transitions/safety tie rules; последний deterministic key разрешает лишь полное числовое равенство и не подтверждает authenticity. Нельзя выбрать candidate вне F. Если ни одного feasible candidate — NO_SAFE_CANDIDATE без state delta. Непроверенный required tail — UNPROVEN/UNAVAILABLE. Новая objective policy меняет plan digest; старый persisted plan не переписывается.

A ближе к прямо названной minimum-safe стратегии Docs14 и сильнее compression по N среди допустимых, но не гарантирует minimum risk/margin и не доказывает global money bound. Нужно отдельно разрешить future change Docs29:3 и comparator36–40; сейчас их не меняем.

### B — RISK_FIRST_V1

Полный proposed текст:
> Выполнить тот же полный F(c), затем lexicographic minimum (RiskNext,MarginNext,FutureTransitionCount,−m(c),N,CanonicalCandidateTieID). Nonfeasible candidates не участвуют. Источники,thresholds,required levels,tail status и future-source restrictions идентичны A. Policy/version и полный candidate/proof set включаются в persisted plan manifest; no safe candidate и unavailable proof не имеют fallback к unsafe ratio/volume. Изменение objective не исправляет proof/provider deficiencies.

B соответствует Docs29 и порядку текущего comparator. Для совместимости с CR09 safety tie показатель должен быть minimum всех required margins,а не выбранного control level. S07:140 сейчас использует catchResult margin выбранного level: существующий code не объявляется already CR09-qualified.
B может увеличить N,потребовать больше margin/transitions или снизить CatchUp headroom,хотя его первичный RiskNext меньше/равен.

## Три математических сценария выбора

Все числа ниже — synthetic mathematical fixtures в общей money unit,не broker evidence/production PASS. OldFar=1 lot,grid0.1,actual candidate upper≥0.4; RiskOld30,RiskTolerance1,margin cap100,Transition cap12,minimum compression0.1 и minimum ratio0.1,maximum N/F0.8. Для показанных feasible rows предполагаются остальные F gates и TWO required levels valid,остальные обязательные proofs/terminal requirements предоставлены как математические premises. Без этих реальных evidence production status UNAVAILABLE.
m_l=G_l−FarLoss_l−1; G_l — eligible gain на этом preview level,не обещание reuse actual Free. TransitionLoss column отдельно,не FarLoss. Rank=A rank/B rank;excluded не ранжируется.

### NF1

| Candidate (N) | RiskNext | MarginNext | Future transitions | TransitionLoss | CatchUpMargin=min levels | Feasible | Rank A/B |
|---|---:|---:|---:|---:|---:|---|---|
| a (0.2) | 18 | 40 | 2 | 10 | 2 | YES,MODEL_ONLY | 1/2 |
| b (0.3) | 12 | 50 | 3 | 6 | 4 | YES,MODEL_ONLY | 2/1 |
| x (0.1) | 1 | 20 | 1 | 3 | -1 | NO | excluded |

Exact level inputs:
- a: G=(20,19),AbsoluteFarLoss=(17,16),buffer1 each → margins=(2,2).
- b: G=(25,24),AbsoluteFarLoss=(20,19),buffer1 each → margins=(4,4).
- x: G=(10,10),AbsoluteFarLoss=(10,10),buffer1 each → margins=(-1,-1).

A selects a,B selects b. B уменьшает primary risk18→12 и улучшает min margin2→4,но margin usage40→50 и N0.2→0.3 больше. x имеет лучший risk1 и меньший N,но отрицательные margins; оба objective исключают x.

### NF2

| Candidate (N) | RiskNext | MarginNext | Future transitions | TransitionLoss | CatchUpMargin=min levels | Feasible | Rank A/B |
|---|---:|---:|---:|---:|---:|---|---|
| a (0.2) | 8 | 40 | 2 | 9 | 3 | YES,MODEL_ONLY | 1/2 |
| b (0.4) | 4 | 45 | 2 | 11 | 1 | YES,MODEL_ONLY | 2/1 |
| x (0.1) | 2 | 20 | 1 | 13 | 4 | NO | excluded |

Exact level inputs:
- a: G=(20,20),AbsoluteFarLoss=(16,15),buffer1 each → margins=(3,4).
- b: G=(18,19),AbsoluteFarLoss=(16,16),buffer1 each → margins=(1,2).
- x: G=(20,20),AbsoluteFarLoss=(15,15),buffer1 each → margins=(4,4).

A selects a,B selects b. B снижает risk8→4,но min margin3→1 и transition loss9→11 хуже. Это прямой trade-off между разными безопасными headrooms. x с положительной CatchUp margin нарушает transition cap13>12; оба исключают.

### NF3

| Candidate (N) | RiskNext | MarginNext | Future transitions | TransitionLoss | CatchUpMargin=min levels | Feasible | Rank A/B |
|---|---:|---:|---:|---:|---:|---|---|
| a (0.2) | 6 | 40 | 1 | 5 | 4 | YES,MODEL_ONLY | 1/2 |
| b (0.3) | 6 | 30 | 3 | 6 | 6 | YES,MODEL_ONLY | 2/1 |
| x (0.1) | 1 | 20 | 1 | 4 | -1 | NO | excluded |

Exact level inputs:
- a: G=(20,21),AbsoluteFarLoss=(15,15),buffer1 each → margins=(4,5).
- b: G=(22,23),AbsoluteFarLoss=(15,15),buffer1 each → margins=(6,7).
- x: G=(20,10),AbsoluteFarLoss=(15,10),buffer1 each → margins=(4,-1).

A selects a,B selects b. Risk6 одинаков. A выбирает N0.2; B выбирает меньшую margin usage30 при N0.3,хотя transitions3 вместо1. x имеет margins4,−1: max-loss/один хороший level не спасает его.

## Что можно и нельзя заключить

| Критерий | A | B |
|---|---|---|
| Прямое соответствие minimum-safe названию/шагу Docs14 | да | требует explicit amendment |
| Соответствие текущему Doc29/comparator | требует change | да по order,не доказательство остальных gates |
| Сохранение safety constraints | одинаковый F | одинаковый F |
| Hidden money model change | не требуется при frozen F/basis | не требуется при том же F/basis |
| Гарантия универсального лучшего результата | нет | нет |
| Совместимость CR09 | да только all-level gate/tie | да только all-level gate/tie |

Не существует universal dominance по этим сценариям: они оптимизируют разные preferences. Если принять фактическую монотонную dependence risk(N),A/B могут совпасть; такая теорема не предоставлена и не подразумевается.
Рекомендуется A как минимально меняющий explicit minimum-safe policy Docs14; B остаётся полноценным выбором владельца при приоритете measured risk. Рекомендация не утверждение стратегии и не доказательство прибыли.

## Acceptance и unresolved

Владелец выбирает A/B и CanonicalCandidateTieID encoding profile. CandidateTieID должен иметь deterministic total order в approved codec; existing rounded digest не автоматически collision-free/economic authority.
Обязательны: paired scenario selections,invalid x excluded,all-level min verification,permutation invariant list order,strict N/Risk/Margin tie,unsupported/missing proof no fallback,immutable plan mismatch,recheck actual residual; TEST_SPECIFIED_NOT_RUN.
Unresolved: strategy preference; numeric/provider/clock domain; finite/tail proof assumptions; Doc14/29 replacement scope; native integration.
Связи: [D06](HSBI_03E_D06_POLICY_RESOLUTION_RU.md),[numeric](HSBI_03E_NUMERIC_CONTRACT_MANIFEST_V1_RU.md),[bundles](HSBI_03E_CONTRACT_DEPENDENCY_RECONCILIATION_RU.md),[ERR038](HSBI_03E_ERR038_PROOF_REQUIREMENTS_RU.md),[ballot](HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md).
