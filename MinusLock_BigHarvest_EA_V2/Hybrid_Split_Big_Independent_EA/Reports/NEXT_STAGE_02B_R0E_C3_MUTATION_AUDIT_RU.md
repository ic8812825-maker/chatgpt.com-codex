# C3 — аудит шести survivors

BASE_SHA=3737116bff6e2275d674b3dd7b816de93715f27c

AUDIT / PROPOSED / AWAITING_ADMIN_APPROVAL. Production, trading и dispatch запрещены.


Оригинальный C2 каталог64 killed/6 reported redundant воспроизведён отдельно. Новая классификация не переписывает C2 evidence.

## C2-C1-MUT-outer-poststate

SourceFunction: apply_for_test
Classification: REDUNDANT_IN_DECLARED_PUBLIC_DOMAIN
MandatoryCaller: apply_for_test
ExactSourceChange: `[{"new": "if False:return _answer('UNAVAILABLE'),copy.deepcopy(store)", "old": "if not balance(b['OriginalGrant'],b['Consumed'],b['Reserved'],b['RemainingFree'],b['Reservations']):return _answer('UNAVAILABLE'),copy.deepcopy(store)"}]`
CallerProof: Public apply always authorizes: _reconcile_store reconstructs ALL pre-state rows from independent journal. _operate_for_registry_replay calls _apply_registry_delta, which validates selected row before and after exact delta and returns no commit on failure. apply checks returned status. Other rows unchanged. Thus outer repeat is redundant over the declared public input domain; mutation of mandatory private delta itself is outside this equivalence claim.

| Public API | Original negative | Mutant negative | Independent expected | Zero delta |
|---|---|---|---|---|
| apply_for_test | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | True |

## C2-C1-MUT-malformed-default-identity

SourceFunction: verify_allocation_identity
Classification: REDUNDANT_IN_DECLARED_PUBLIC_DOMAIN
MandatoryCaller: verify_allocation_identity, authorize, apply_for_test
ExactSourceChange: `[{"new": "require(allocation['source']==source)", "old": "require(type(presented) is dict and allocation['source']==source)"}, {"new": "presented=copy.deepcopy(expected) if presented is None else presented\n        require(set(presented)==set(expected))", "old": "require(set(presented)==set(expected))"}]`
CallerProof: C2 public authorize/_reconcile_store/verify_allocation_identity validates nested schema before this old clause. Mandatory schema cannot be bypassed by public apply. Original and mutant preserve the typed rejection on this causal input; not an unsafe acceptance kill.

| Public API | Original negative | Mutant negative | Independent expected | Zero delta |
|---|---|---|---|---|
| verify_allocation_identity | REJECT | REJECT | REJECT | True |
| authorize | REJECT | REJECT | REJECT | True |
| apply_for_test | REJECT | REJECT | REJECT | True |

## C2-C1-MUT-digest-format

SourceFunction: _reconcile_store
Classification: REDUNDANT_IN_DECLARED_PUBLIC_DOMAIN
MandatoryCaller: authorize, apply_for_test, available, recover_store
ExactSourceChange: `[{"new": "", "old": " and all(c in '0123456789abcdef' for c in receipt[field])"}]`
CallerProof: C2 public authorize/_reconcile_store/verify_allocation_identity validates nested schema before this old clause. Mandatory schema cannot be bypassed by public apply. Original and mutant preserve the typed rejection on this causal input; not an unsafe acceptance kill.

| Public API | Original negative | Mutant negative | Independent expected | Zero delta |
|---|---|---|---|---|
| authorize | REJECT | REJECT | REJECT | True |
| apply_for_test | REJECT | REJECT | REJECT | True |
| available | CONFLICT | CONFLICT | CONFLICT | True |
| recover_store | CONFLICT | CONFLICT | CONFLICT | True |

## C2-C1-MUT-journal-self-repair

SourceFunction: _reconcile_store
Classification: REDUNDANT_IN_DECLARED_PUBLIC_DOMAIN
MandatoryCaller: authorize, apply_for_test, available, recover_store
ExactSourceChange: `[{"new": "if any(type(e) is not dict for e in authority['coreJournal'].values()):authority['coreJournal']=copy.deepcopy(store['ledger']['events'])", "old": "_validate_core_journal(authority['coreJournal'])"}]`
CallerProof: C2 public authorize/_reconcile_store/verify_allocation_identity validates nested schema before this old clause. Mandatory schema cannot be bypassed by public apply. Original and mutant preserve the typed rejection on this causal input; not an unsafe acceptance kill.

| Public API | Original negative | Mutant negative | Independent expected | Zero delta |
|---|---|---|---|---|
| authorize | REJECT | REJECT | REJECT | True |
| apply_for_test | REJECT | REJECT | REJECT | True |
| available | CONFLICT | CONFLICT | CONFLICT | True |
| recover_store | CONFLICT | CONFLICT | CONFLICT | True |

## C2-C1-MUT-malformed-source-ignore

SourceFunction: _authorize
Classification: REDUNDANT_IN_DECLARED_PUBLIC_DOMAIN
MandatoryCaller: authorize, apply_for_test, available, recover_store
ExactSourceChange: `[{"new": "if type(known) is not dict:known=None", "old": "if known is not None:\n        exact.fields(known,('source','recordDigest','granted','net','phase','unallocated'));require(type(known['recordDigest']) is str)"}]`
CallerProof: C2 public authorize/_reconcile_store/verify_allocation_identity validates nested schema before this old clause. Mandatory schema cannot be bypassed by public apply. Original and mutant preserve the typed rejection on this causal input; not an unsafe acceptance kill.

| Public API | Original negative | Mutant negative | Independent expected | Zero delta |
|---|---|---|---|---|
| authorize | REJECT | REJECT | REJECT | True |
| apply_for_test | REJECT | REJECT | REJECT | True |
| available | CONFLICT | CONFLICT | CONFLICT | True |
| recover_store | CONFLICT | CONFLICT | CONFLICT | True |

## C2-MUT-cost-shape-caller

SourceFunction: cost_coverage
Classification: NOT_GLOBALLY_REDUNDANT_STATUS_GAP
MandatoryCaller: cost_coverage, authorize, apply_for_test
ExactSourceChange: `[{"new": "pass", "old": "if expected is not None:dto.validate(\"CostSet\",expected)"}]`
CallerProof: Mandatory CostClaim schema rejects the boolean claim before fact comparison; removing only the CostSet caller cannot bypass it. Direct cost_coverage and public apply both preserve rejection. Dual caller mutation separately demonstrates necessity of the complete layer.

| Public API | Original negative | Mutant negative | Independent expected | Zero delta |
|---|---|---|---|---|
| cost_coverage | CONFLICT | UNAVAILABLE | CONFLICT | True |
| authorize | REJECT | REJECT | REJECT | True |
| apply_for_test | REJECT | REJECT | REJECT | True |

Positive controls и actual calls/lines сохранены в SURVIVORS.json. Для outer post-state дополнительно используется алгебра: G=C+V+F, 0<x<=F => G=(C+x)+V+(F-x); lower delta проверяет before/after, остальные rows реконструируются и не меняются. Для schemas удаление нижней проверки не обходит публичный обязательный validation caller. Это объяснение domain-limited, не универсальная полнота mutation coverage.

C2-MUT-cost-shape-caller: counterexample fact.OverlapKnown=1, normal valid claims. Original CONFLICT, mutant UNAVAILABLE; public apply/authorize оба REJECT. Старый causal bool-policy input не обнаруживал это различие. Поэтому глобальная избыточность этого mutant опровергнута на status contract; unsafe acceptance/double spend не доказаны.
