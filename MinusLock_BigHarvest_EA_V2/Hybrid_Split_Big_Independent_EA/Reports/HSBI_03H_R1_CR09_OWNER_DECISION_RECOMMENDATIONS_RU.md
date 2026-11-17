# HSBI-03H-R1 — Рекомендации владельцу по 11 вопросам CR-09

DocumentVersion=HSBI-03H-R1-V1
SourceCommitSHA=70cc4c861b391a7916403106ff07f25729e602da
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=AUDIT_SPEC_ONLY_PROPOSED_AWAITING_OWNER_APPROVAL

Репозиторий: ic8812825-maker/chatgpt.com-codex; ветка work. Все пути относительно MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/. Режим GITHUB_MCP_REMOTE_ONLY, локальных файловых операций нет. SourceCommitSHA — исследованная база, не будущий commit отчётов.
D-06=A и NewFar=A/MINIMUM_SAFE_V1 сохраняются. Новых owner selections и approval receipts этот документ не создаёт. Все числовые торговые примеры синтетические; подтверждённых брокерских сделок в них нет.
PRODUCTION_CHANGED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.
UNAVAILABLE — отсутствует доказательство, CONFLICT — противоречие, REJECT — доказанное нарушение. Ни один из этих результатов не разрешает новый финансовый эффект. Математическое ожидание не является фактическим PASS.

Scope=11 существующих subquestions CR09-SUB-01…11; решения за владельца не принимаются
Dependencies=physical/semantics/money отчёты03H; published ballot03G; selected D06 A/NewFar A; numeric/provider/native bundles
OpenQuestions=все11 OwnerSelection=AWAITING; полный CR09 не утверждён; registered approval receipts0
AcceptanceCriteria=каждый вопрос содержит options/evidence/recommendation/consequences/gaps; principle readiness отделена от implementation permission

## Как читать readiness

READY_FOR_OWNER_PRINCIPLE_SELECTION означает достаточные основания выбрать принцип, но НЕ конкретный provider, wire format или готовый implementation. EVIDENCE_REQUIRED_BEFORE_SELECTION означает, что конкретный допустимый set/profile/manifest сейчас выбирать нельзя. CONTRACT_CONFLICT_REQUIRES_RESOLUTION требует связанного versioned amendment; вопрос нельзя закрыть локальным code change.
D-06 A и NewFar A не переоткрываются. Sub-ID не новый canonical decision ID; canonical associations сохранены из существующего ballot. CR09_OWNER_BALLOT=PREPARED_NOT_APPROVED; CR09_OWNER_SELECTIONS=0/11; REGISTERED_APPROVAL_RECEIPTS=0.

| Группа | Вопросы |
|---|---|
| READY_FOR_OWNER_PRINCIPLE_SELECTION |02,03,06,07 |
| EVIDENCE_REQUIRED_BEFORE_SELECTION |05,08,09,10 |
| CONTRACT_CONFLICT_REQUIRES_RESOLUTION |01,04,11 |

Сопоставление01/04/11 включает конфликт normative scope с source и незавершённость формулировок. Оно не объявляет source нормативным выше Docs. В04 physical full close уже доказан Docs13, но перевод этого факта в generic quantity/money purpose нуждается в contract alignment.

## CR09-SUB-01

DecisionID=CR09-SUB-01
CanonicalDecisionId=CR-09
SelectionReadiness=CONTRACT_CONFLICT_REQUIRES_RESOLUTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: all required IDs/prefixes, caps и strict margins до objective. B: сохранить selective-control как diagnostic-only; полный CR09 не утверждать.

SourceEvidence: [03G ballot CR09-SUB-01](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-01); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Docs30 разрешает selective control; selected MINIMUM_SAFE_V1 требует minAll. Нужен versioned amendment без повторного выбора NewFar A.

MathematicalEvidence: Tmax и minM — разные extrema; см. physical witness3600/2240 против−1001/−1201.

PhysicalTransitionEvidence: Физический loss и полный basket loss имеют разный membership.

RecommendedOption: A как целевой all-required принцип; пока B diagnostic-only, full CR09 не утверждать.

Reason: Docs30 разрешает selective control; selected MINIMUM_SAFE_V1 требует minAll. Нужен versioned amendment без повторного выбора NewFar A.

Consequences: Сохранить отдельные required node/action IDs и prefixes; не объявлять current single-control all-level.

MissingEvidence: Утверждённый scope и связанный amended contract, complete source/numeric/funding proofs.

## CR09-SUB-02

DecisionID=CR09-SUB-02
CanonicalDecisionId=CR-09
SelectionReadiness=READY_FOR_OWNER_PRINCIPLE_SELECTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: ALTERNATIVE_SCENARIOS одного starting inventory. B: SEQUENTIAL_TRANSITIONS с state chain. C: явный branching scenario tree с exclusivity и per-path prefixes.

SourceEvidence: [03G ballot CR09-SUB-02](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-02); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Docs13 и Docs04 сильнее всего поддерживают последовательную цепь. Это рекомендация стратегии, не признание текущего кода B.

MathematicalEvidence: R+U сохраняется при переводе open→closed на фиксированной цене; направление новой Far меняется с Core.

PhysicalTransitionEvidence: Old FarSELL1@100 →CoreBUY0.4@120; следующий Far обязан бытьBUY@120.

RecommendedOption: B для одной физической траектории; C только как отдельно заданная оболочка путей; A лишь для явно независимых counterfactuals.

Reason: Docs13 и Docs04 сильнее всего поддерживают последовательную цепь. Это рекомендация стратегии, не признание текущего кода B.

Consequences: Нужен полный StateAfter→StateBefore. Current scalar template остаётся nonqualified.

MissingEvidence: Owner intent terminal/path scope; real position/open/cost/realized lineage. Для реализации всё ещё evidence required.

## CR09-SUB-03

DecisionID=CR09-SUB-03
CanonicalDecisionId=CR-09
SelectionReadiness=READY_FOR_OWNER_PRINCIPLE_SELECTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: frozen exact IDs/guards; обязательный tail без proof блокирует. B: заранее ограниченный finite scope с явным отказом от утверждения непроверенного tail. C: разрешить bound theorem только для всех перечисленных safety predicates.

SourceEvidence: [03G ballot CR09-SUB-03](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-03); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Нельзя вывести scope обязательств из числа удачных proof rows.

MathematicalEvidence: R={L1…L4},P={L1…L3}: покрытие3/4, q-bound не money proofL4.

PhysicalTransitionEvidence: Незакрытая promoted Far0.16 ещё является открытой позицией; малый lot не CLOSED.

RecommendedOption: A для frozen required IDs/guards; C только после теоремы; B допускает лишь объявленную конечную гарантию.

Reason: Нельзя вывести scope обязательств из числа удачных proof rows.

Consequences: Заранее фиксировать manifest, edges, terminal/tail и prefixes.

MissingEvidence: Owner terminal definition, model assumptions, complete tail theorem для всех safety predicates.

## CR09-SUB-04

DecisionID=CR09-SUB-04
CanonicalDecisionId=CR-09; D-04
SelectionReadiness=CONTRACT_CONFLICT_REQUIRES_RESOLUTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: full old FarBefore. B: next FarAfter. C: физический FarClosed по Action membership. D: original candidate при доказанной неизменной обязанности.

SourceEvidence: [03G ballot CR09-SUB-04](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-04); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Docs13 закрывает old Far полностью; NewFar123 использует исходный candidate, Docs24 термин FarLossIncrease не фиксирует полный action scope. Требуется единый obligation contract.

MathematicalEvidence: F1,N0.4: compression0.6,closedOldFar1; при price loss1000/lot расход1000, а не600/400.

PhysicalTransitionEvidence: Position oldFar исчезает, CoreID сохраняется. PartialFar same-ID0.1 — другой action.

RecommendedOption: A либо эквивалентный доказанный C для FULL_CLOSE_OLD_FAR; B/D только для иного явно указанного purpose.

Reason: Docs13 закрывает old Far полностью; NewFar123 использует исходный candidate, Docs24 термин FarLossIncrease не фиксирует полный action scope. Требуется единый obligation contract.

Consequences: Quantity rhs и Far money proof обязаны иметь один LevelID/position/action/volume.

MissingEvidence: Точный FarObligationKind, approved action volume/cost receipts; actual provider отсутствует.

## CR09-SUB-05

DecisionID=CR09-SUB-05
CanonicalDecisionId=D-02/03/06/14; CR-09
SelectionReadiness=EVIDENCE_REQUIRED_BEFORE_SELECTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: только подтверждённые разрешённые Core facts, Initial исключён. B: Core+Trend либо иной явно перечисленный set с independent association. C: projected sources только в conditional preview, без денег к расходованию.

SourceEvidence: [03G ballot CR09-SUB-05](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-05); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Core-only projected scalar не actual closing income; целиком Core не закрывают.

MathematicalEvidence: S3 fullCore3000,closedCore2600; share даёт2400 против2080; обе суммы пока projected.

PhysicalTransitionEvidence: Core partial close происходит после old Far; его будущая прибыль не ранний cash.

RecommendedOption: C как stage-разделение; A/B concrete eligible set выбирать после source evidence. Сохранять Initial exclusion.

Reason: Core-only projected scalar не actual closing income; целиком Core не закрывают.

Consequences: Потребуются approved eligibility membership, positive settled source и allocation receipts.

MissingEvidence: Реальные sources/частичные costs, policy shares и association. Нельзя молча включить Small/Trend.

## CR09-SUB-06

DecisionID=CR09-SUB-06
CanonicalDecisionId=D-02/13/14
SelectionReadiness=READY_FOR_OWNER_PRINCIPLE_SELECTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: отдельные типы и authority receipts; projection всегда nonspendable. B: до provider разрешить только PREVIEW_ONLY diagnostics.

SourceEvidence: [03G ballot CR09-SUB-06](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-06); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Projection не bank inventory; bool/hash не финансовая authority.

MathematicalEvidence: S1 funding inventory может быть5000, projected Core gain0: величины независимы.

PhysicalTransitionEvidence: До confirmed closing source cash от Core не возник.

RecommendedOption: A как принцип раздельных типов/receipts, B как нынешний operational статус.

Reason: Projection не bank inventory; bool/hash не финансовая authority.

Consequences: Preview не reserve/consume/dispatch; FundingAuthorized требует отдельного provider.

MissingEvidence: Конкретный qualified provider/journal, independent settled facts; принцип можно выбрать раньше.

## CR09-SUB-07

DecisionID=CR09-SUB-07
CanonicalDecisionId=D-01/07/14; CR-09
SelectionReadiness=READY_FOR_OWNER_PRINCIPLE_SELECTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: atomic reservation/consumption по source Free и каждому path/prefix. B: не разрешать sequential financial authorization до полного provider+journal; alternative valuations отдельно.

SourceEvidence: [03G ballot CR09-SUB-07](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-07); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Последовательные closes требуют денег раньше поздней прибыли.

MathematicalEvidence: S3 terminal loss400, prefix need4000, Free500: блокируется первая Small1000.

PhysicalTransitionEvidence: Small→Far→Trend→Core order зафиксирован Docs13; менять порядок ради funding здесь нельзя.

RecommendedOption: A как target atomic per-path prefix, B до provider/journal.

Reason: Последовательные closes требуют денег раньше поздней прибыли.

Consequences: Freeze reservation before first irreversible step; CAS и durable recovery обязательны.

MissingEvidence: Owner loss-consumption/offset contract, allowed buckets, atomic registry и crash/concurrency evidence.

## CR09-SUB-08

DecisionID=CR09-SUB-08
CanonicalDecisionId=D-04/06/11; CR-09
SelectionReadiness=EVIDENCE_REQUIRED_BEFORE_SELECTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: полный CostFactID inclusion map, disjoint buffers/headroom и partial membership. B: получать unavailable до утверждения конкретного manifest, не выбирать удобный basis.

SourceEvidence: [03G ballot CR09-SUB-08](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-08); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Нулевые costs синтетических примеров не допустимы как реальные broker defaults.

MathematicalEvidence: 10−1−2−0.5=6.5; commission входит один раз; R+U−remainingCosts без повторов.

PhysicalTransitionEvidence: Нелинейная комиссия partial close требует собственного receipt; Core C и C−N не имеют автоматически одинаковых fees.

RecommendedOption: A как inclusion принцип; B для любого неутверждённого concrete manifest.

Reason: Нулевые costs синтетических примеров не допустимы как реальные broker defaults.

Consequences: CostFactID/stage/window/position/volume/includedIn; H_in/H_gate distinct purposes D06 A.

MissingEvidence: Actual cost receipts, minimum-fee/rebate/swap/partial membership, approved separate headroom.

## CR09-SUB-09

DecisionID=CR09-SUB-09
CanonicalDecisionId=D-10/11/12/15; CR-09
SelectionReadiness=EVIDENCE_REQUIRED_BEFORE_SELECTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: exact settled + approved interval/error bound projected; lower>0. B: пока не квалифицирован profile, не выдавать safety verdict по floating scalar.

SourceEvidence: [03G ballot CR09-SUB-09](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-09); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Произвольный epsilon не доказывает strict margin>0.

MathematicalEvidence: 12−11−1=0 rejects; nominal0.001 при lower11.999−11.001−1.001=−0.003 не guarantee.

PhysicalTransitionEvidence: Partial lots/closed money должны соответствовать approved grids и rounding одного action.

RecommendedOption: A как принцип exact settled и bounded projected, B до квалификации конкретного профиля.

Reason: Произвольный epsilon не доказывает strict margin>0.

Consequences: Checked overflow, currency profile, conservative interval. F64Z не утверждён этим текстом.

MissingEvidence: D10/11/12/15 profile, native casts/NaN/overflow/codec/error bounds.

## CR09-SUB-10

DecisionID=CR09-SUB-10
CanonicalDecisionId=D-08/13/14
SelectionReadiness=EVIDENCE_REQUIRED_BEFORE_SELECTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: независимо квалифицированный broker/history/provider receipt с clock epoch/skew/restart reconciliation. B: authority не назначена, все зависимые funding/feasibility gates blocked.

SourceEvidence: [03G ballot CR09-SUB-10](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-10); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Fresh=true и expected=только что присвоенный identity не независимый источник.

MathematicalEvidence: issued120−now100=20>skew2: reject даже при expiry130.

PhysicalTransitionEvidence: Нужна actual history связь CoreID/fills/residual; requested N не actualN.

RecommendedOption: A как требования к authority, B как фактический статус до evidence.

Reason: Fresh=true и expected=только что присвоенный identity не независимый источник.

Consequences: Original full body receipts, broker/server/account/clock/revision/restart binding.

MissingEvidence: Конкретный provider, transport/authentication, clocks/skew, complete position/history receipts.

## CR09-SUB-11

DecisionID=CR09-SUB-11
CanonicalDecisionId=D-07/08/12/16; CR-09
SelectionReadiness=CONTRACT_CONFLICT_REQUIRES_RESOLUTION
OwnerApprovalRequired=YES
OwnerSelection=AWAITING
FormalApprovalReceipt=NOT_REGISTERED
ImplementationPermission=NO

ExistingOptions: A: preserve old records/schema, explicit adapter only с доказанным kind/scope; unknown quarantine и новый plan receipt. B: unsupported legacy остаётся read-only, новая authorization только после полного пересчёта из immutable facts.

SourceEvidence: [03G ballot CR09-SUB-11](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md#cr09-sub-11); Docs13/14/24/29/30 и source inventory в [physical reconstruction](HSBI_03H_R1_PHYSICAL_TRANSITION_RECONSTRUCTION_RU.md). Docs14 minimum-safe и Docs29/current comparator risk-first требуют amendment к уже выбранному A. Старый transitionLoss — Far scalar, не basket max.

MathematicalEvidence: TL01 checkedMax12,returnedFar3; нельзя изменить label без schema. Выбранный objective aN0.2 вместо legacy bN0.3.

PhysicalTransitionEvidence: Старый plan с иной последовательностью/identity нельзя возобновить по новому названию policy.

RecommendedOption: A только для доказанного legacy kind/scope; B для unknown history. Новая authorization после полного пересчёта.

Reason: Docs14 minimum-safe и Docs29/current comparator risk-first требуют amendment к уже выбранному A. Старый transitionLoss — Far scalar, не basket max.

Consequences: Preserve bytes/history; explicit adapters/quarantine, новые immutable plan receipts; no auto-resume.

MissingEvidence: Approved schema/codec/objective mappings, durable migration receipts и native compatibility.

## Пакет будущего решения и то, что остаётся запрещено

Владелец при будущей фиксации указывает sub-ID, вариант и точный purpose/scope, версию текста и immutable SourceCommitSHA/blob SHA утверждаемого документа. При composite варианте разделяет strategic principle, concrete implementation/profile и evidence acceptance. Публикация этих рекомендаций не является таким ответом и не регистрирует approval receipt.

До согласования01/04/11 нельзя назвать current single-control proof полным CR09, small candidate — объёмом закрытой old Far, risk-first — выбранным minimum-safe. При выбореB в02 source ещё требует state-chain specification и тестов: простая замена farDirection или loop CatchUp недостаточна.

Ни одна рекомендация не закрывает P0, ERR038, ERR018 либо TL001. Формальный owner выбор принципа не устраняет missing provider/native proof. Квалификация, versioned normative amendments и отдельный implementation scope должны предшествовать разрешению кода.
