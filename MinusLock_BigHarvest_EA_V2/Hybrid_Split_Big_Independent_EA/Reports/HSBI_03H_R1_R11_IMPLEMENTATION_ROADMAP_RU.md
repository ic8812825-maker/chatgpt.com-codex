# HSBI-03H-R1 — Конкретный roadmap R1.1 и минимальный будущий slice

DocumentVersion=HSBI-03H-R1-V1
SourceCommitSHA=70cc4c861b391a7916403106ff07f25729e602da
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=AUDIT_SPEC_ONLY_PROPOSED_AWAITING_OWNER_APPROVAL

Репозиторий: ic8812825-maker/chatgpt.com-codex; ветка work. Все пути относительно MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/. Режим GITHUB_MCP_REMOTE_ONLY, локальных файловых операций нет. SourceCommitSHA — исследованная база, не будущий commit отчётов.
D-06=A и NewFar=A/MINIMUM_SAFE_V1 сохраняются. Новых owner selections и approval receipts этот документ не создаёт. Все числовые торговые примеры синтетические; подтверждённых брокерских сделок в них нет.
PRODUCTION_CHANGED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.
UNAVAILABLE — отсутствует доказательство, CONFLICT — противоречие, REJECT — доказанное нарушение. Ни один из этих результатов не разрешает новый финансовый эффект. Математическое ожидание не является фактическим PASS.

Scope=R11-C→R11-A→R11-B→R11-D→R11-E; future development only
Dependencies=HSBI_R11_P0_DEPENDENCY_PLAN;03F/03G normative locks;03H physical semantics/owner package/67-test qualification
OpenQuestions=owner bundles/provider/build/native acceptance; source/allocations/lineage/cost/profile; отдельное разрешение implementation
AcceptanceCriteria=точные модули/prerequisites/tests/rollback/stop каждого этапа; минимальный slice не зависит от фиктивного funding; ни один stage не разрешён

## Последовательность и границы

C → A; C+A → B; C+A+B → D; C+A+B+D и qualified provider/durable backend → E acceptance.
Provider protocol и тестовые receipts можно специфицировать до реализации A/B, но они не становятся квалифицированными от описания. Native numeric/codec должен быть определён раньше identity wire/body, иначе A сравнится по меняющимся округлённым representations. B не строится на неполном source key: новый EventID или allocation alias не может восстановить grant.
C также нужен B напрямую: точное conservation невозможно на неопределённых currency scale/overflow/rounding. Последующая переделка C может инвалидировать A/B schemas; поэтому версии/domain receipts фиксируются до них.

В каждом этапе сначала закрываются нормативные prerequisites и готовится exact test design; implementation лишь после ОТДЕЛЬНОГО разрешения reviewed patch scope. Положительный audit или выбор принципа не даёт такого разрешения. Порядок не означает, что C/A/B уже complete.

## Сохраняемые blockers

P0_TOTAL=14,P0_CLOSED=0,ERR038=OPEN; TL001=CONFIRMED_STATIC/P1_PROPOSED; ERR018=OPEN_CONTRACT_GAP. D06=A,NewFar=A. Formal receipts0, CR09 selections0/11.
ERR038: bounded lots/positions не finite worst money loss при неограниченном adverse move; нельзя снять finite-sample native тестом. Нет обещаний прибыльности/ограниченного рыночного убытка/активации.

## R11-C — Numeric

StageStatus=PROPOSED_BLOCKED; ImplementationPermission=NO

Цель: Устранить nonfinite/domain/overflow разрешения до source identity и allocation.

Точные исходные модули существующего dependency plan (верхняя граница будущего review, не текущая allowlist записи):

- `Include/Risk/HSBI_RiskGateResult.mqh`
- `Include/Money/HSBI_MoneyState.mqh`
- `Include/Execution/HSBI_TransactionTypes.mqh`
- `Include/Execution/HSBI_ExecutionIntent.mqh`
- `Include/Execution/HSBI_ActionTypes.mqh`
- `Include/Execution/HSBI_EventTypes.mqh`
- `Include/Planning/HSBI_BrokerGrid.mqh`
- `Include/Risk/HSBI_NewFarGateTypes.mqh`

Предлагаемые будущие изменения: Сначала проверять конечность ВСЕХ входов и limits, затем intermediates и closed enum membership; checked settled arithmetic и projected interval wrappers только по approved profiles. Не менять старые bytes/schema молча.

Необходимые решения владельца: D-10/D-11/D-15; связанное D-12 numeric/codec согласование.

Необходимые provider evidence: Currency/posting ranges/rounding/error profile; native build/domain; реальные instrument grid properties для broker gates.

Необходимые тесты: MONEY/VOLUME, native NaN/Infinity/±0/overflow/bounds; COMPATIBILITY. Все existing valid finite controls сохраняются.

Критерии приёмки: Нет допуска из nonfinite input/limit/intermediate; strict boundary oracle согласован; compile+native artifact с exact source/profile; не заявлять весь C закрытым по одному guard.

Возможность отката: отдельный reviewed commit пакета; сохранить baseline tree/fixtures/receipts; при regression обычный revert после анализа зависимых commits, без force/reset. Persistent facts/schema не переписывать: append-only migration либо read-only compatibility/quarantine. No-trade guards остаются обязательны.

Условия остановки: Domain/profile не утверждён; native baseline отсутствует; required edits вне slice; изменение trade policy; survivor без анализа. При changed base — re-audit до нового patch, не автоматический rebase. No false PASS, no lowering expected.

## R11-A — Source Identity

StageStatus=PROPOSED_BLOCKED; ImplementationPermission=NO

Цель: Связать экономический факт с физическим broker/server/account/posting и полным immutable body.

Точные исходные модули существующего dependency plan (верхняя граница будущего review, не текущая allowlist записи):

- `Include/Money/HSBI_EconomicLedgerTypes.mqh`
- `Include/Core/HSBI_Identifiers.mqh`
- `Include/Money/HSBI_MoneyProofIdentity.mqh`

Предлагаемые будущие изменения: Additive typed source identity/schema, полный equality включая price/role/components/open/volume и origin association. Event delivery не source. Old wire records read-only/quarantine. Не присваивать caller identity как будто независимый proof.

Необходимые решения владельца: D-02/D-08/D-12/D-13/D-15/D-16; CR09-SUB-05/06/10/11.

Необходимые provider evidence: Independent broker history/position/action association; original full body/cost/clock receipts; actual BigCore residual decoder.

Необходимые тесты: SOURCE/SNAPSHOT; altered-components-same-net; wrong-account/server; actual residual/source mismatch; native codec goldens.

Критерии приёмки: Один immutable source для разных deliveries; altered body conflict; unknown provider unavailable; migration preserves historical bytes; native direct-caller negatives.

Возможность отката: отдельный reviewed commit пакета; сохранить baseline tree/fixtures/receipts; при regression обычный revert после анализа зависимых commits, без force/reset. Persistent facts/schema не переписывать: append-only migration либо read-only compatibility/quarantine. No-trade guards остаются обязательны.

Условия остановки: C не квалифицирован; namespace/body/provider incomplete; source reuse alias; отсутствует approved schema/legacy policy. При changed base — re-audit до нового patch, не автоматический rebase. No false PASS, no lowering expected.

## R11-B — Allocation

StageStatus=PROPOSED_BLOCKED; ImplementationPermission=NO

Цель: Сохранить source money глобально при grants/reservations/consumption и конкуренции.

Точные исходные модули существующего dependency plan (верхняя граница будущего review, не текущая allowlist записи):

- `Include/Money/HSBI_AllocationLedgerTypes.mqh`
- `Include/Money/HSBI_AllocationPolicyTypes.mqh`
- `Include/Money/HSBI_MoneyState.mqh`
- `Include/Money/HSBI_ReserveAllocationTypes.mqh`

Предлагаемые будущие изменения: Разделить пятикомпонентный grant vector и lifecycle Grant=Consumed+Reserved+Free. Equality committed allocation, остаток вResidual. Запрет source inflation через новыйEventID/AllocationKey. Unknown outcome блокирует новый debit; journal provider — отдельный reviewed interface, не придуманная bool authority.

Необходимые решения владельца: D-01/D-02/D-03/D-07/D-10/D-11/D-14/D-16; CR09-SUB-05/07.

Необходимые provider evidence: Atomic unique source registry/CAS; complete durable intents/outcomes; correction/reversal/history and reconciled revisions.

Необходимые тесты: FUNDING01…08,CU06, source alias, reservation/partial commit/release, two-owner/crash/correction; native exact arithmetic.

Критерии приёмки: Ни один prefix не тратит больше подтверждённого Free; immutable replay zero; consumed не release; correction below commitments reconciliation; CAS race≤1commit.

Возможность отката: отдельный reviewed commit пакета; сохранить baseline tree/fixtures/receipts; при regression обычный revert после анализа зависимых commits, без force/reset. Persistent facts/schema не переписывать: append-only migration либо read-only compatibility/quarantine. No-trade guards остаются обязательны.

Условия остановки: A/C incomplete; missing atomic durable backend; shares/offsets/bucket purposes unapproved; negative/unbound money; crash evidence отсутствует. При changed base — re-audit до нового patch, не автоматический rebase. No false PASS, no lowering expected.

## R11-D — Reserve Binding

StageStatus=PROPOSED_BLOCKED; ImplementationPermission=NO

Цель: Связать per-level obligations, full physical action group и funding с независимыми source facts.

Точные исходные модули существующего dependency plan (верхняя граница будущего review, не текущая allowlist записи):

- `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh`
- `Include/Money/HSBI_ReserveAllocationTypes.mqh`
- `Include/Planning/HSBI_NewFarSolver.mqh`
- `Include/Planning/HSBI_FutureSmallProofAggregator.mqh`
- `Include/Money/HSBI_CatchUpModel.mqh`

Предлагаемые будущие изменения: Не loop старый ci вслепую. Ввести typed obligation/result scopes, all-required minimum with bounds, complete membership и prefix funding. FarClosed=full old Far для Docs13; Core closed C−N. Preview/funding separate. Actual residual independent revalidation. MINIMUM_SAFE_V1 лишь после полного feasible predicate, с new plan version.

Необходимые решения владельца: D-02/D-03/D-04/D-06 A/CR-09/D-07/D-08/D-13/D-14; CR09-SUB-01…11.

Необходимые provider evidence: Complete per-level original action/position/direction/volume/cost/quote/risk/margin receipts; R_A/B/C outputs; physical graph и prefixes.

Необходимые тесты: Все TL/CU,VOLUME,COST,OBJECTIVE; S1/S2/S3; два promotions с alternating directions/inherited Core open; fullCore vs closedCore; unknown/tail/source/cost negative.

Критерии приёмки: T_physical/T_basket/A/minMargin разные typed поля; quantity/money один action scope; все required proofs complete; negative/unknown blocks; successful branch trace и native fixtures.

Возможность отката: отдельный reviewed commit пакета; сохранить baseline tree/fixtures/receipts; при regression обычный revert после анализа зависимых commits, без force/reset. Persistent facts/schema не переписывать: append-only migration либо read-only compatibility/quarantine. No-trade guards остаются обязательны.

Условия остановки: Любое01/04/11 conflict unresolved; eligibility/profile/provider unbound; fixed-template lineage mismatch; unsupported tail; new DTO вне future approved allowlist. При changed base — re-audit до нового patch, не автоматический rebase. No false PASS, no lowering expected.

## R11-E — Integration

StageStatus=PROPOSED_BLOCKED; ImplementationPermission=NO

Цель: Обеспечить завершение каждого шага, reconciliation и no-trade end-to-end acceptance.

Точные исходные модули существующего dependency plan (верхняя граница будущего review, не текущая allowlist записи):

- `Include/Core/HSBI_Context.mqh`
- `Include/Core/HSBI_Invariants.mqh`
- `Include/Core/HSBI_StateMachine.mqh`
- `Include/Execution/HSBI_TransactionTypes.mqh`
- `Include/Persistence/HSBI_ExecutionJournal.mqh`
- `Include/Persistence/HSBI_ExecutionStateSnapshot.mqh`
- `Include/Persistence/HSBI_PersistenceInterface.mqh`
- `Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh`
- `Include/Runtime/HSBI_RuntimeRestartValidator.mqh`

Предлагаемые будущие изменения: Полный mandatory caller graph; state-chain/transaction barrier; completed fills before next action, unknown blocks retry, compare original body before no-op, single residual Core identity; no automatic resume. Dispatch всегдаfalse. Полный trading backend не входит в этот план.

Необходимые решения владельца: D-05/D-07/D-08/D-13/D-14/D-15/D-16 и все dependencies A/B/C/D; новый scoped owner permission отдельно.

Необходимые provider evidence: Read-only actual positions/history/provider; qualified durable journal+registry/restart; broker calculations; known clock epochs; branch traces.

Необходимые тесты: Группы2…6, все67; every crash boundary, delayed/partial fill, actual≠requested, journal altered body, restart epoch; no-order E2E.

Критерии приёмки: Pinned source/build/receipt-bound artifacts; no unknown pending source; no false completion; dispatch attempts0; outside-allowlist diff0. Native acceptance не доказывает unbounded market safety ERR038.

Возможность отката: отдельный reviewed commit пакета; сохранить baseline tree/fixtures/receipts; при regression обычный revert после анализа зависимых commits, без force/reset. Persistent facts/schema не переписывать: append-only migration либо read-only compatibility/quarantine. No-trade guards остаются обязательны.

Условия остановки: Любой partial/unknown outcome, unreconciled history, twoFar, wrap stateRevision, no durable evidence; изменение disabled dispatch; ERR038 не снят. При changed base — re-audit до нового patch, не автоматический rebase. No false PASS, no lowering expected.

## Нужные интерфейсы, ещё НЕ входящие в старую границу review

Физическая семантика может потребовать future additive/versioned изменения в:
- Include/Planning/HSBI_FutureSmallTypes.mqh — node/action state/identity/obligation scope;
- Include/Planning/HSBI_FutureSmallSolver.mqh — полноценный projected StateAfter→StateBefore, inherited direction/open basis/realized/money inventory;
- Include/Planning/HSBI_NewFarCandidate.mqh — selected MINIMUM_SAFE_V1/minAll typed proof/result;
- Include/Money/HSBI_BasketMoneyEvaluator.mqh — full basket versus closing membership/residual metrics;
- Include/Money/HSBI_CandidateMoneyEvaluator.mqh — complete per-candidate/required proof chain.

Эти существующие пути проверены в исходном tree, но не объявляются разрешёнными к изменению. Старый R11-D allowlist сам по себе их не открывает. Требуются отдельные interface design, normative amendment, caller/legacy impact и scope review. Roadmap не создаёт новых production файлов и не предлагает скрыто менять Docs29 либо исторические expected.

## Самый маленький безопасный implementation slice для будущего разрешения

Предложение: только finite-input/finite-limit rejection в HSBI_ValidateRiskInput существующего Include/Risk/HSBI_RiskGateResult.mqh, без изменения публичной структуры/enum ordinals/codec/threshold comparators. Source blob=f172bd2ab9cfc461ab403a8ce490a4b71ce3c8c4. Exact RiskInput/RiskLimits поля объявлены в Include/Risk/HSBI_RiskTypes.mqh, blob6f40356c18949a0465c1595b0229a67bbcd46dc7.
Это часть R11-C, не закрытие C и не изменение денег/allocations/NewFar. Current helper напрямую сравнивает числа; все double inputs и limits должны быть finite до сравнений. Предложенный scope не задаёт новые допустимые ranges и не меняет finite negative domain — это потребовало бы отдельной policy.

Минимальный будущий patch allowlist: один header RiskGateResult.mqh; новая отдельная suite/evidence под Tests/R11P0/ и Reports/HSBI_R11_P0_* только после scoped permission. RiskTypes читается как dependency, изменение не требуется. Helper finite function использовать только если его include graph/availability доказаны; иначе scoped design должен показать локальную совместимую проверку. Никаких изменений сейчас нет.

Нормативные prerequisites:
1. D10/11/15 согласуют finite double domain, NaN/Infinity rejection и native representation; отрицательные/zero cases отдельны и не меняются неявно.
2. Exact caller/include graph и baseline native compile+valid controls; no-trade mode доказан.
3. Exact future allowlist/source SHA/patch owner review; approvals не получены этим roadmap.
4. Fixture/oracle frozen независимо от subject; будущий native test execution environment разрешён.

Тестовые prerequisites и будущая acceptance:
- finite positive control: projectedMargin1,projectedMarginLevel100,freeMarginAfter100,cycle/accountDD0,gross1,managedPositions1,worstLoss1,transitionLoss1,spread0,snapshotFresh=true; limits maxMargin10,minMarginLevel10,minFree10,maxCycle/accountDD10,maxGross10,maxPositions2,maxWorst10,maxTransition10,maxSpread1. Existing helper должен сохранить passed=true.
- stale control тот же,snapshotFresh=false →false.
- по одному заменить каждое из9 double полей входа и9 double limits на NaN,+Infinity,−Infinity: всего54 malformed numeric variants, каждый failed/failClosed, ни один permit.
- finite equality boundary1==max1 по non-strict upper guards сохраняет существующее поведение; minMarginLevel/free equality так же. Все остальные values из valid control.
- native branch instrumentation показывает отказ ИМЕННО finite guard до сравнений; failedGate/reason mapping заранее согласован и совместим.
- oracle проверяет finite domain без вызова HSBI_ValidateRiskInput; int managedPositions/maxManagedPositions не подменяются double или новым enum.
- native compiler/build/source/profile hashes и 0 dispatch attempts; никаких funds/provider claims.

Эти54 варианты — предложенные будущие probes минимального patch, НЕ дополнительные выполненные тесты и НЕ изменение счётчика67 спецификаций03G. Они не закрывают ERR009 автоматически: нужны accepted artifact и separate finding disposition. Проверить также intermediates/ranges в полном C остаётся обязанностью последующих slices.

Provider dependency slice: реальные деньги/history/registry не нужны для самого чистого predicate, но native ABI/build/finite profile нужен. Это позволяет начать техническую работу после соответствующих approvals, не имитируя funding authority. Торговый риск, full risk correctness и весь EA этим header не квалифицируются.

Rollback slice: ordinary revert одного future commit, исходные signatures/schema сохранены; backend/state migrations отсутствуют. STOP при дополнительном file scope, недоказанном native finite profile, изменившейся базе/caller contract, mutation, no native acceptance или любом ослаблении no-trade policy.

## Путь от аудита к R1.1, не к торговле

Сначала owner principles и resolution01/04/11; затем concrete numeric/identity/cost/authority manifests; после них независимо квалифицируемый минимальный C slice и версии A/B contracts. Далее allocation journal/provider, D physical state/obligation/money/funding и только потом E no-order integration.
Для complex D нужен именно position→action→money→residual→new role→next state. Поменять comparator, denominator или число CatchUp вызовов без этой цепи недостаточно.
Выполнение всех технических prerequisites лишь делает patch reviewable. Ни один этап сейчас не разрешён к реализации; broker dispatch и real trading запрещены.
