# C2 — независимое воспроизведение C1

BASE_SHA=fae7dfc18ca2d61af2f3446826ef3031825bbfd8

PROPOSED / AWAITING_ADMIN_APPROVAL. Только audit/test-only; production и trading запрещены.

Штатный C1: 840 PASS; mutation kills 54, redundant 1; package negative 46.

C2-01: bool PolicyVersion в fact+claim при root1 разрешает in-memory debit10 из50 в C1. Это ошибка типов, не создание денег/real trade. C2-02: nested batch None/empty/bool, empty history record и snapshot без payload дают TypeError/KeyError в C1. C2 typed DTO устраняет expected-input exceptions. C2-03: все шесть отдельных mutations сохраняют840 PASS старого suite; отдельные negative fixtures отличают оригинал от мутанта. Оригинальные guards работают; это coverage gaps.

C2-04: last-key-wins C1 принимает скрытый FAIL/exit1 при последнем PASS/0; обратный порядок фиксируется отдельно и может корректно отвергаться. Опубликованные evidence не обвиняются в дубликатах. C2-05: recovery ограничен reconstruction/bindings, не полным historical reauthorization; см. scope table.

Полные входы, source edits/hashes, original/mutant outcomes: Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REPRODUCTION.json. Старый strict package запускается на точном Git archive C1. Adapter меняет только archive root/path-relative bookkeeping в отдельном module; исходный checker и исторические evidence не изменяются. Actual adapter source hash — hash C2 reproduction runner.

## Поля воспроизведения по FindingID

### C2-01

FindingID: C2-01
SourceFunction: cost_coverage / authorize / apply_for_test
PositiveControl: normal50/10/.5; C1 StockReference APPLY-positive passed
ExactInputOrSourceChange: fact+claim PolicyVersion=True, root1
IndependentExpected: typed refusal, no debit
ActualOutcome: Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REPRODUCTION.json#Findings[C2-01]
StateDelta: free50→40, consumed0→10, revision2→3
ProofBoundary: test-only malformed identifier, no real trade
Classification: CONFIRMED

### C2-02

FindingID: C2-02
SourceFunction: _authorize / economic_record / recover_store
PositiveControl: normal apply/recover controls in stock840
ExactInputOrSourceChange: nested expected None/empty/bool; extra empty record; missing snapshot payload
IndependentExpected: typed outcome, no unexpected exception
ActualOutcome: Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REPRODUCTION.json#Findings[C2-02-*] + SnapshotMissingPayload
StateDelta: InputsUnchanged recorded for apply probes; snapshot state delta not separately measured in old run
ProofBoundary: expected-input exceptions reproduced; C2 zero deltas tested separately
Classification: CONFIRMED

### C2-03

FindingID: C2-03
SourceFunction: _reconcile_store / _authorize / _bind_allocation
PositiveControl: original+mutant full C1 suite840 PASS for each edit
ExactInputOrSourceChange: six exact source edits in SixAdditionalMutations
IndependentExpected: original rejects; mutant violates literal binding requirement
ActualOutcome: Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REPRODUCTION.json#SixAdditionalMutations
StateDelta: explicit state summaries/zeroDelta in causal apply; receipt checks pure
ProofBoundary: coverage gap, not original bypass
Classification: CONFIRMED

### C2-04

FindingID: C2-04
SourceFunction: check_hsbi_02b_r0e_c1_package.load / verify
PositiveControl: untampered exact C1 archive PASS
ExactInputOrSourceChange: duplicate Result/ExitCode, both orders; disposable hashes refreshed
IndependentExpected: reject ambiguous duplicate-key JSON
ActualOutcome: Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REPRODUCTION.json#DuplicateJSON
StateDelta: disposable bytes only; real history unchanged
ProofBoundary: last-wins ambiguity; reverse order may correctly reject
Classification: CONFIRMED

### C2-05

FindingID: C2-05
SourceFunction: recover_store / authorize
PositiveControl: normal stock recovery control passed
ExactInputOrSourceChange: historical50 versus receipt required50.5
IndependentExpected: limited reconstruction only; new authorize REJECT
ActualOutcome: Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REPRODUCTION.json#RecoveryScope
StateDelta: inputsUnchanged=True
ProofBoundary: historical full eligibility outside declared recovery scope; not claimed double spend
Classification: UNPROVEN

