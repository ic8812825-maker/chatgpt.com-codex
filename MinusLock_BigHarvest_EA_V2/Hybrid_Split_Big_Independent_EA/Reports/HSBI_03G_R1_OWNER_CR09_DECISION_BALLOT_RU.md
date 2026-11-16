# HSBI-03G-R1 — окончательный проект ballot CR-09

DocumentVersion=HSBI-03G-R1-V1
SourceCommitSHA=e68e73e1b252d20e15588645004f9066c6ae88f0
Scope=Owner decision package; no automatic approval
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=PROPOSED_AWAITING_OWNER_APPROVAL
Dependencies=All 16 canonical decisions; existing D06/NewFar selection

Репозиторий: `ic8812825-maker/chatgpt.com-codex`, ветка `work`. Все пути ниже находятся внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`. Новый текст является проектом контракта, а не утверждением реализации. Выбор D-06 A и companion NewFar A сохраняется; полный CR-09 не утверждён. Формальных approval receipts нет.

PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.

UNAVAILABLE означает отсутствие обязательного доказательства; CONFLICT — противоречие данных; REJECT — доказанное нарушение. Каждый результат запрещает новый финансовый эффект, delta=0. NO_OP допустим только после проверки подлинного полного прежнего event body и receipt. Числа математических примеров не являются брокерскими константами.

## Уже сделанный выбор не переоткрывается

- [Reports/HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md:20–95](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md#L20-L95). SourceBlobSHA=`3674348a620f40cb5532a5a965cfd76c2d119431`; EvidenceClass=STATIC_REVIEWED.
- [Reports/HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md:20–76](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md#L20-L76). SourceBlobSHA=`ffd81b9575790a166c50979fd7b1a4c85715a011`; EvidenceClass=STATIC_REVIEWED.
- [Reports/HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md:20–77](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md#L20-L77). SourceBlobSHA=`91aeb48e911c2891c8267b9fedd831f991ceaf56`; EvidenceClass=STATIC_REVIEWED.

D-06=A,Policy=D06-A/HSBI-03E-R1; NewFar companion=A,Policy=MINIMUM_SAFE_V1. OwnerSelection=CONFIRMED_IN_CONVERSATION, FormalApprovalReceipt=NOT_REGISTERED. Этот ballot не ставит подпись, не регистрирует receipt и не открывает A/B этих двух уже выбранных policies. Все новые subquestions ниже остаются AWAITING.

DECISIONS_TOTAL=16;DECISIONS_OWNER_SELECTED=1;DECISIONS_AWAITING=15;COMPANION_OBJECTIVE_SELECTED=1;REGISTERED_APPROVAL_RECEIPTS=0. Subquestion ID — идентификатор вопроса внутри существующих решений, не новое CanonicalDecisionId. Во всех пунктах ImplementationPermission=NO.

## Как фиксировать будущий ответ

Ответ владельца должен указать CR09-SUB-ID, вариант/точный scope, DocumentVersion/SourceCommitSHA и конкретные blob SHA утверждаемого текста. Настоящий audit содержит proposed evidence requirements, но не имитирует подтверждение отсутствующего evidence. EVIDENCE_REQUIRED_BEFORE_SELECTION означает, что сегодня нельзя выбрать конкретную реализацию/profile/provider, опираясь лишь на общую рекомендацию. Можно отдельно принять принцип, сохранив конкретный manifest blocked.

## CR09-SUB-01

DecisionID=CR09-SUB-01
CanonicalDecisionId=CR-09
Question: Утвердить полный scope HSBI_CR09_ALL_REQUIRED_V1?

Options: A: all required IDs/prefixes, caps и strict margins до objective. B: сохранить selective-control как diagnostic-only; полный CR09 не утверждать.

MathematicalConsequences / SafetyConsequences: A требует полного conjunction и блокирует unknown; B не может выдавать qualified minimum all margins.

Dependencies: Все sub-choices02…11 и provider/native evidence.

Recommendation: A как целевой контракт; до binding зависимостей полное утверждение преждевременно.
SelectionReadiness=AWAITING
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED

## CR09-SUB-02

DecisionID=CR09-SUB-02
CanonicalDecisionId=CR-09
Question: Что означают уровни?

Options: A: ALTERNATIVE_SCENARIOS одного starting inventory. B: SEQUENTIAL_TRANSITIONS с state chain. C: явный branching scenario tree с exclusivity и per-path prefixes.

MathematicalConsequences / SafetyConsequences: A не суммирует взаимоисключающие debits; B обязан учитывать все прежние расходы; C требует path-specific conservation. Смешение даёт double-spend/неверную lineage.

Dependencies: Strategy intent, actual promotion/direction/open-price lineage; current fixed-template model недостаточна.

Recommendation: Не выбирать автоматически. Если стратегия последовательная, B требует нового физического evidence, а не переименования массива.
SelectionReadiness=AWAITING
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED

## CR09-SUB-03

DecisionID=CR09-SUB-03
CanonicalDecisionId=CR-09
Question: Как фиксировать RequiredLevelIDs, terminal и tail?

Options: A: frozen exact IDs/guards; обязательный tail без proof блокирует. B: заранее ограниченный finite scope с явным отказом от утверждения непроверенного tail. C: разрешить bound theorem только для всех перечисленных safety predicates.

MathematicalConsequences / SafetyConsequences: A наиболее явно определяет обязательства; B даёт лишь ограниченную гарантию; C требует теоремы cost/margin/source/funding, одного q-bound мало.

Dependencies: Level semantics, termination policy, model/grid assumptions.

Recommendation: A для обязательного набора; C только после отдельного доказательства. Нельзя retroderive requiredCount из provenDepth.
SelectionReadiness=AWAITING
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED

## CR09-SUB-04

DecisionID=CR09-SUB-04
CanonicalDecisionId=CR-09; D-04
Question: Какую обязанность покрывает quantity inequality?

Options: A: full old FarBefore. B: next FarAfter. C: физический FarClosed по Action membership. D: original candidate при доказанной неизменной обязанности.

MathematicalConsequences / SafetyConsequences: В promotion FarClosed=OldFarBefore, compression≠physical close. B/D не покрывают full close автоматически; деньги нужно оценить на том же объёме/position.

Dependencies: Action/position identity, direction/role lineage, broker grid; volume evidence.

Recommendation: Для Docs13 full-close purpose A либо эквивалентный доказанный C. Иной purpose требует отдельного объяснения, решение остаётся владельцу.
SelectionReadiness=EVIDENCE_REQUIRED_BEFORE_SELECTION
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED

## CR09-SUB-05

DecisionID=CR09-SUB-05
CanonicalDecisionId=D-02/03/06/14; CR-09
Question: Какие источники eligible для reserve?

Options: A: только подтверждённые разрешённые Core facts, Initial исключён. B: Core+Trend либо иной явно перечисленный set с independent association. C: projected sources только в conditional preview, без денег к расходованию.

MathematicalConsequences / SafetyConsequences: Core-only и net всего basket не равны; расширение eligibility меняет денежную policy. C не конкурирует с actual funding, это отдельный stage.

Dependencies: D06 A сохраняется; source membership, exact costs, approved allocation policy.

Recommendation: Начать с явно доказанного допустимого set; не считать текущий scalar Core net actual income. B только по явному scope/evidence.
SelectionReadiness=EVIDENCE_REQUIRED_BEFORE_SELECTION
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED

## CR09-SUB-06

DecisionID=CR09-SUB-06
CanonicalDecisionId=D-02/13/14
Question: Как разделить preview и funding authority?

Options: A: отдельные типы и authority receipts; projection всегда nonspendable. B: до provider разрешить только PREVIEW_ONLY diagnostics.

MathematicalConsequences / SafetyConsequences: Оба варианта запрещают projected→spendable по bool/hash; A задаёт полный будущий lifecycle, B сохраняет blocked funding.

Dependencies: Independent provider, registry/journal, original snapshot receipts.

Recommendation: A как принцип; B как текущий operational status до появления provider.
SelectionReadiness=AWAITING
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED

## CR09-SUB-07

DecisionID=CR09-SUB-07
CanonicalDecisionId=D-01/07/14; CR-09
Question: Как финансировать sequential prefixes?

Options: A: atomic reservation/consumption по source Free и каждому path/prefix. B: не разрешать sequential financial authorization до полного provider+journal; alternative valuations отдельно.

MathematicalConsequences / SafetyConsequences: A не позволяет обновлять Free одним и тем же grant; B не скрывает unknown spending. Max branch debit применим лишь к proven exclusivity.

Dependencies: Source unique index,CAS,durable outcomes,crash/restart reconciliation.

Recommendation: A как target, B как действующее ограничение; никакого повторного расходования source.
SelectionReadiness=AWAITING
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED

## CR09-SUB-08

DecisionID=CR09-SUB-08
CanonicalDecisionId=D-04/06/11; CR-09
Question: Какой CostBasisManifest допустим?

Options: A: полный CostFactID inclusion map, disjoint buffers/headroom и partial membership. B: получать unavailable до утверждения конкретного manifest, не выбирать удобный basis.

MathematicalConsequences / SafetyConsequences: Нет двойных комиссий/spread/slippage/swap; H_in/H_gate сохраняют выбранные роли. B не означает cost=0.

Dependencies: Real cost receipts, Initial group membership, cost policy owner, exact profile.

Recommendation: Утвердить принцип A; конкретный manifest выбирать только по evidence. D06 A не пересматривается.
SelectionReadiness=EVIDENCE_REQUIRED_BEFORE_SELECTION
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED

## CR09-SUB-09

DecisionID=CR09-SUB-09
CanonicalDecisionId=D-10/11/12/15; CR-09
Question: Как доказывать численную strict positivity?

Options: A: exact settled + approved interval/error bound projected; lower>0. B: пока не квалифицирован profile, не выдавать safety verdict по floating scalar.

MathematicalConsequences / SafetyConsequences: Nominal positive при lower≤0 не PASS. Signed64 checked arithmetic и currency digits не из symbol. F64Z не утверждается автоматически.

Dependencies: Currency/posting/rounding profile; native precision/overflow/codec evidence.

Recommendation: A как принцип; B как обязательный статус сегодняшнего профиля.
SelectionReadiness=EVIDENCE_REQUIRED_BEFORE_SELECTION
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED

## CR09-SUB-10

DecisionID=CR09-SUB-10
CanonicalDecisionId=D-08/13/14
Question: Кто является source/snapshot/clock authority?

Options: A: независимо квалифицированный broker/history/provider receipt с clock epoch/skew/restart reconciliation. B: authority не назначена, все зависимые funding/feasibility gates blocked.

MathematicalConsequences / SafetyConsequences: Локальный hash/fresh=true не доказывает источник. Ошибочный account/content/revision запрещает эффект.

Dependencies: Конкретный provider identity, authenticated transport/content association, clock evidence.

Recommendation: A как требования; B пока реальные provider/clock не представлены. Не выдумывать имя authority.
SelectionReadiness=EVIDENCE_REQUIRED_BEFORE_SELECTION
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED

## CR09-SUB-11

DecisionID=CR09-SUB-11
CanonicalDecisionId=D-07/08/12/16; CR-09
Question: Как обрабатывать legacy results/plans и новые версии?

Options: A: preserve old records/schema, explicit adapter only с доказанным kind/scope; unknown quarantine и новый plan receipt. B: unsupported legacy остаётся read-only, новая authorization только после полного пересчёта из immutable facts.

MathematicalConsequences / SafetyConsequences: Нельзя назвать legacy Far loss worst basket или old risk-first план minimum-safe. Replay equality относится к полной approved schema.

Dependencies: Result/proof/numeric/objective manifest, durable migration receipt, source completeness.

Recommendation: A для достоверно распознанной истории, B для неизвестной; не silent migration.
SelectionReadiness=AWAITING
OwnerSelection=AWAITING
FormalReceipt=NOT_REGISTERED


## Связанные approval bundles — точные версии проекта

```text
BundleManifestVersion=HSBI-03G-BUNDLES-1
ContractVersion=HSBI_CR09_ALL_REQUIRED_V1
SourceCommitSHA=e68e73e1b252d20e15588645004f9066c6ae88f0
CR09_SCOPE_BUNDLE = {CR09-SUB-01,02,03,04; required-level, quantity, metric, feasibility V1}
MONEY_AUTHORITY_BUNDLE = {D-01,02,07,08,13,14,16; CR09-SUB-05,06,07,08,10,11}
NUMERIC_CODEC_BUNDLE = {D-10,11,12,15; CR09-SUB-09,11}
ObjectiveVersion=MINIMUM_SAFE_V1 (selected companion, not full CR09 approval)
D06Policy=D06-A/HSBI-03E-R1 (selected, evidence dependencies unchanged)
OwnerSelectionsForNewBundles=AWAITING
FormalApprovalReceipts=NOT_REGISTERED
ImplementationPermission=NO
```

Manifest версии связываются с фактическими blob SHA после публикации: владелец утверждает immutable опубликованные blobs, не mutable HEAD по имени work. Self-containing hash в тексте не выдумывается. Доказательства native/provider прикладываются отдельно и не считаются созданными публикацией ballot.

OpenQuestions: все11 вопросов выше; D05 reset authority UNBOUND; actual numeric/source/snapshot evidence. Никакой другой D-ID не меняет статус.
AcceptanceCriteria: владелец может адресно выбрать каждый scope; несовместимые варианты не объединяются без нового manifest; формальная запись не расширяет разрешение на реализацию/торговлю.

Связи: [required levels](HSBI_03G_R1_CR09_REQUIRED_LEVEL_CONTRACT_RU.md), [funding](HSBI_03G_R1_RESERVE_FUNDING_AUTHORITY_RU.md), [gates](HSBI_03G_R1_FINAL_READINESS_VERDICT_RU.md).
