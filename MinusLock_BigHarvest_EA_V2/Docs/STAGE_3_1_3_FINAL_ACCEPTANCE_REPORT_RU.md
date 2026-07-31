PROJECT=MinusLock_BigHarvest_EA_V2
STAGE=3.1.3
SUBSTAGE=3.1.3.10
PURPOSE=FINAL_ACCEPTANCE
BRANCH=work
BASE_COMMIT=10a7042d1a2692ad5a25e7afc2b996529a674928
REPOSITORY_SCOPE=MinusLock_BigHarvest_EA_V2/
STAGE_3_1_4_STARTED=NO

# Финальная приёмка Этапа 3.1.3

## 1. Baseline

Дата фиксации baseline: `2026-07-31` (UTC).

```text
BASE_COMMIT_SHORT=10a7042
WORKING_TREE=CLEAN
TRACKED_CHANGES=NONE
MAPPING_SCHEMA_VERSION=3.1.3-ninth-correction-1
MAPPING_SCHEMA_TERMS=230
VALIDATOR=Tests/validate_stage_3_1_3_glossary.py
VALIDATOR_SHA256=be2ba7ab12fc4679a0ef9526bd8b135197abd1a0ffdae412fe758d7e27e88817
PRODUCTION_BLOCKING_RULES_TOTAL=33
MQL5_RUNTIME_LOGIC_CHANGED=NO
BUSINESS_POLICY_CHANGED=NO
PARAMETER_PROFILE_CHANGED=NO
REPOSITORY_SCOPE_VIOLATION=NO
```

Baseline получен до изменений этого задания командами `git status --short
--branch`, `git rev-parse HEAD`, чтением `schema_version` и числа `terms` из
authoritative mapping, а production registry — разбором последнего присваивания
`BLOCKING` в production validator. Старый список из документации не использовался.

### Production BLOCKING registry baseline

```text
DECLARATION_LINE_MISMATCH
DECLARATION_KIND_MISMATCH
DECLARATION_TYPE_MISMATCH
DECLARATION_CONTEXT_MISMATCH
READ_SITE_FILE_MISSING
READ_SITE_LINE_MISSING
READ_SITE_IDENTIFIER_MISSING
WRITE_SITE_FILE_MISSING
WRITE_SITE_LINE_MISSING
WRITE_SITE_IDENTIFIER_MISSING
WRITE_SITE_NOT_WRITE
SEMANTIC_COMPATIBILITY_MISMATCH
CANDIDATE_SCORE_MISMATCH
CLAIMED_COMPUTED_MAPPING_STATUS_MISMATCH
UNIT_CLAIM_MISMATCH
AUTHORITATIVE_CLAIM_MISMATCH
PROJECTED_ACTUAL_CLAIM_MISMATCH
SCOPE_CLAIM_MISMATCH
LIFECYCLE_CLAIM_MISMATCH
MISSING_WITHOUT_CANDIDATE_AUDIT
MISSING_WITH_ACCEPTED_CANDIDATE
NON_MISSING_WITH_EMPTY_ENTRIES
MISSING_WITH_NONEMPTY_ENTRIES
CANDIDATE_WITHOUT_REJECTION_REASON
CANDIDATE_WITHOUT_SCORE
TABLE_RECORD_MISMATCH
INVALID_TYPE_UNIT
INVALID_TYPE_SIGN
INVALID_SOURCE_MATRIX
INVALID_LEDGER_EVENT_TYPE
INVALID_DATA_BOOLEAN_SEMANTICS
MAPPING_ENTITY_KIND_INCOMPATIBLE
INVALID_LIFECYCLE_MATRIX
```

Этот раздел фиксирует только исходную точку. Финальный verdict будет записан
после независимого запуска production validator и всех acceptance-аудитов.

## 2. Production validator и blocking counters

Production validator запущен без модификации. Полный объединённый stdout/stderr
сохранён в
`Docs/Evidence/stage_3_1_3_final_acceptance/production_validator.log`.
Registry прочитан самим validator из текущего source; все 33 напечатанных правила
дали ноль.

```text
CANONICAL_TERMS=230
TERMS_AUDITED=230
BLOCKING_RULES_TOTAL=33
BLOCKING_RULES_ZERO=33
BLOCKING_RULES_NONZERO=0
BLOCKING_COUNTERS=NONE
STAGE_3_1_3_NINTH_CORRECTION_VALIDATION=PASS
```

Полный итог production blocking counters:

```text
DECLARATION_LINE_MISMATCH=0
DECLARATION_KIND_MISMATCH=0
DECLARATION_TYPE_MISMATCH=0
DECLARATION_CONTEXT_MISMATCH=0
READ_SITE_FILE_MISSING=0
READ_SITE_LINE_MISSING=0
READ_SITE_IDENTIFIER_MISSING=0
WRITE_SITE_FILE_MISSING=0
WRITE_SITE_LINE_MISSING=0
WRITE_SITE_IDENTIFIER_MISSING=0
WRITE_SITE_NOT_WRITE=0
SEMANTIC_COMPATIBILITY_MISMATCH=0
CANDIDATE_SCORE_MISMATCH=0
CLAIMED_COMPUTED_MAPPING_STATUS_MISMATCH=0
UNIT_CLAIM_MISMATCH=0
AUTHORITATIVE_CLAIM_MISMATCH=0
PROJECTED_ACTUAL_CLAIM_MISMATCH=0
SCOPE_CLAIM_MISMATCH=0
LIFECYCLE_CLAIM_MISMATCH=0
MISSING_WITHOUT_CANDIDATE_AUDIT=0
MISSING_WITH_ACCEPTED_CANDIDATE=0
NON_MISSING_WITH_EMPTY_ENTRIES=0
MISSING_WITH_NONEMPTY_ENTRIES=0
CANDIDATE_WITHOUT_REJECTION_REASON=0
CANDIDATE_WITHOUT_SCORE=0
TABLE_RECORD_MISMATCH=0
INVALID_TYPE_UNIT=0
INVALID_TYPE_SIGN=0
INVALID_SOURCE_MATRIX=0
INVALID_LEDGER_EVENT_TYPE=0
INVALID_DATA_BOOLEAN_SEMANTICS=0
MAPPING_ENTITY_KIND_INCOMPATIBLE=0
INVALID_LIFECYCLE_MATRIX=0
```

## 3. Causal audit release-blockers

Standalone-запуск сначала воспроизвёл дефект entry point: каталог `Tests/` не
входил в `sys.path`, хотя вызов через production validator работал. Исправлена
первопричина запуска, а не результаты controls. После исправления каждый rule из
production `BLOCKING` registry прошёл через `production.validate`: чистый
positive artifact оставил counter нулевым, целевая negative mutation подняла
соответствующий counter. Итог сохранён в
`Docs/Evidence/stage_3_1_3_final_acceptance/counter_audit.log`.

```text
COUNTER_AUDIT=PASS
PRODUCTION_BLOCKING_REGISTRY_USED=YES
BLOCKING_COUNTERS_TOTAL=33
BLOCKING_COUNTERS_REGISTERED=33
COUNTER_AUDIT_EXECUTES_VALIDATOR=1
COUNTER_AUDIT_SOURCE_SCAN_AS_PROOF=0
MISSING_CAUSAL_RULES=0
INEFFECTIVE_CAUSAL_RULES=0
VACUOUS_BLOCKING_RULES=0
COUNTER_POSITIVE_NOT_CLEAN=0
```

## 4. Полный canonical mapping

Production engine заново обработал все строки обеих canonical tables и все 230
terms в обоих языковых направлениях. Для каждого языка присутствуют 230
candidate audits. Статусы вычислены production semantic engine; mapping JSON не
использовался как источник winner/use sites. Допустимый contract статусов:
`EXACT_MATCH`, `SEMANTIC_MATCH`, `PARTIAL_MATCH`, `AMBIGUOUS`, `MISSING`,
`NOT_APPLICABLE`.

```text
CANONICAL_TERMS=230
TERMS_AUDITED=230
MQL5_TERMS_WITH_CANDIDATE_AUDIT=230
PYTHON_TERMS_WITH_CANDIDATE_AUDIT=230

MQL5_EXACT_MATCH=4
MQL5_SEMANTIC_MATCH=0
MQL5_PARTIAL_MATCH=44
MQL5_AMBIGUOUS=0
MQL5_MISSING=182
MQL5_NOT_APPLICABLE=0

PYTHON_EXACT_MATCH=0
PYTHON_SEMANTIC_MATCH=0
PYTHON_PARTIAL_MATCH=39
PYTHON_AMBIGUOUS=0
PYTHON_MISSING=191
PYTHON_NOT_APPLICABLE=0

MISSING_WITHOUT_CANDIDATE_AUDIT=0
MISSING_WITH_ACCEPTED_CANDIDATE=0
MISSING_WITH_UNREVIEWED_CANDIDATES=0
FALSE_UNIQUE_WINNER=0
AMBIGUITY_NOT_DECLARED=0
```

`MISSING` означает завершённый discovery и сохранённые rejection reasons/scores,
а не отсутствие exact name. Нулевое число `AMBIGUOUS` является вычисленным
результатом: production pipeline поддерживает ambiguity, но на этом HEAD не
нашёл неразрешимой пары совместимых лидеров.

## 5. Declaration identity, use graph, dataflow, units и lineage

`seventh_regressions` и `ninth_regressions` повторно прогнаны через production
engine. Контроли различают MQL5 global/local/parameter/nested/struct-field и
Python module/local/parameter/attribute identities; use до declaration не
привязывается к более поздней local declaration. Одинаковое имя в разных scopes
даёт разные `DeclarationIdentity` (`file`, line/column, declaration kind,
`scope_id`, `parent_symbol`), поэтому name-only lookup не является identity.

```text
DECLARATION_SCOPED_IDENTITY=PASS
SHADOWING_CONTROL=PASS
DECLARATION_BEFORE_USE=PASS
NAME_ONLY_BINDING=NO
VALIDATOR_OWNS_USE_DISCOVERY=YES
JSON_USE_SITES_USED_AS_TRUTH=NO
USE_GRAPH_DECLARATION_SCOPED=YES
```

Use graph хранит declaration identity и раздельные reads/writes; production
validator самостоятельно обнаружил 203 read и 161 write sites. Resolved graph
содержит source/sink declaration identities, expression, operator и operands.
Контроли доказали отсутствие cross-scope утечки одноимённых operands и
отбрасывание unresolved source вместо глобального «первого имени».

```text
TOTAL_READ_SITES_DISCOVERED=203
TOTAL_WRITE_SITES_DISCOVERED=161
DATAFLOW_NODES=276
DATAFLOW_EDGES=134
RESOLVED_DATAFLOW=PASS
UNRESOLVED_REQUIRED_DATAFLOW_EDGES=0
```

Fixed-point control доказал цепочку `LOT * RATIO -> LOT`, затем
`LOT - LOT -> LOT`, а также отказ типизировать `LOT + MONEY` как LOT. Lineage
идёт по resolved declarations и разделяет configuration, derived values,
terminal snapshots/positions, requests, deal history/ledger, cache, test и
offline tool. Cache/request/projected/test/offline evidence не повышается до
несовместимой runtime authority.

```text
FIXED_POINT_UNIT_PROPAGATION=PASS
UNIT_CONTRADICTIONS=0
UNIT_UNKNOWN_REQUIRED_VALUES=0
UNIT_CLAIM_MISMATCH=0
SOURCE_LINEAGE=PASS
CACHE_PROMOTED_TO_AUTHORITY=0
PROJECTED_PROMOTED_TO_ACTUAL=0
REQUEST_PROMOTED_TO_FILLED=0
TEST_ANALOGUE_PROMOTED_TO_RUNTIME=0
OFFLINE_ANALOGUE_PROMOTED_TO_RUNTIME=0
NINTH_REGRESSION_INVARIANTS=PASS
SHADOWING_TESTS=PASS
```

## 6. Symbol + Magic + Cycle scope

Scope proof пересчитан для concrete candidate identity и его scoped reads,
writes, resolved callers/dataflow. Контроли покрывают global runtime,
per-plan/request/position/deal и требуют Cycle там, где это задаёт canonical
contract. Отдельные Symbol и Magic mentions из разных путей не объединяются.

```text
SYMBOL_SCOPE_SUPPORTED=YES
MAGIC_SCOPE_SUPPORTED=YES
SYMBOL_MAGIC_SCOPE_SUPPORTED=YES
CANDIDATE_PATH_SCOPE_PROOF=PASS
GLOBAL_UNION_SCOPE_PROOF_USED=NO
SCOPE_CLAIM_MISMATCH=0
```

## 7. Positive, negative и adversarial suites

Полный verbose output сохранён в
`Docs/Evidence/stage_3_1_3_final_acceptance/regression_suites.log`. Это новый
запуск на acceptance HEAD, а не перенос чисел из прежнего отчёта. Suites
включают mutations, positive controls, adversarial attacks, shadowing,
recomputation, candidate audit parity и canonical table parity.

```text
NEGATIVE_TESTS_TOTAL=48
NEGATIVE_TESTS_PASSED=48
POSITIVE_TESTS_TOTAL=20
POSITIVE_TESTS_PASSED=20
ADVERSARIAL_TESTS_TOTAL=15
ADVERSARIAL_TESTS_CAUGHT=15
POSITIVE_FIXTURES_TOTAL=25
POSITIVE_FIXTURES_PASSED=25
ADVERSARIAL_FIXTURES_TOTAL=25
ADVERSARIAL_FIXTURES_CAUGHT=25
REGRESSION_SUITES=PASS
```

## 8. Нормативный manual, lot lifecycle, signs и tolerances

Табличные фрагменты manual и authoritative glossary сравнены byte-for-byte
после разбора всех обязательных колонок (CanonicalName/term, Type, Unit, Sign,
Projected/Actual, Authority, Rounding, Tolerance, Aliases, Status): второй
канонической таблицы с иным содержимым нет.

```text
CANONICAL_TABLE_EQUALITY=PASS
MANUAL_GLOSSARY_PARITY=PASS
```

Lot contract однозначно разделяет типы и authority pipeline:

```text
RawLot (LOT_RAW)
→ CalculatedLot (LOT_CALCULATED)
→ NormalizedLot (LOT_NORMALIZED)
→ RequestedLot (LOT_REQUESTED)
→ FilledLot (LOT_FILLED)
→ ActualPositionLot (LOT_POSITION_ACTUAL)
LOT_LIFECYCLE_PIPELINE=PASS
REQUESTED_LOT_IS_FILLED_LOT=NO
```

Money sign audit подтвердил signed P/L (`GrossProfit`, `NetProfit`, все формы
`RecoveryPL`, `FarLossSigned`) и отдельные неотрицательные magnitudes/budgets/
costs (`GrossLoss`, `FarLossMagnitude`, Reserve/PartialFarBudget/TransitionBudget/
Carry, commission/swap/fee/spread/slippage costs). Поэтому «loss» без указания
signed/magnitude не является допустимой подстановкой.

Tolerance contract связывает `MoneyTolerance` только с account money,
`VolumeToleranceLots` с lots, `PriceTolerance` с price, `PointTolerance` с
points, `RatioTolerance` и `ComparisonEpsilon` с dimensionless values, а
identity — с exact policy. Normative equality не опирается на
неклассифицированный magic `1e-9`.

```text
MONEY_SIGN_CONTRACT=PASS
TOLERANCE_UNIT_CONTRACT=PASS
```

## 9. Граница Этапа 3.1.4

История проверена от parent первого commit Этапа 3.1.3
`65752df780a3ee524d44da5114943ed6cc91a39b` до acceptance HEAD. Все 75
изменённых путей находятся только в `Docs/` или `Tests/`; `.mqh` внутри
`Tests/stage_3_1_3/fixtures/` являются статическими fixtures, не production
runtime. Production MQL5, Include, Sets/parameter profiles, order open/close,
risk gates и формулы трёх законов не менялись.

```text
MQL5_RUNTIME_LOGIC_CHANGED=NO
BUSINESS_POLICY_CHANGED=NO
PARAMETER_PROFILE_CHANGED=NO
STAGE_3_1_4_STARTED=NO
TRADING_POLICY_CHANGED_BY_STAGE_3_1_3=NO
```

Полный машинно-воспроизводимый boundary result сохранён в
`Docs/Evidence/stage_3_1_3_final_acceptance/stage_3_1_4_boundary_audit.log`.

## 10. Scope и reproducibility

```text
REPOSITORY=ic8812825-maker/chatgpt.com-codex
BRANCH=work
PERMITTED_DIRECTORY=MinusLock_BigHarvest_EA_V2/
SOURCE_HEAD=10a7042d1a2692ad5a25e7afc2b996529a674928
REPOSITORY_SCOPE_VIOLATION=NO
```

В рамках задания изменены исключительно final report/evidence и два standalone
test entry points внутри разрешённого каталога. Runtime/business/profile files
не затронуты.

### Опубликованный commit и файлы

Фактическая Git-история содержит единый опубликованный commit предыдущей
приёмки `c261318f9c3e0f5ec90586fc791c4e69f0e68cbd` непосредственно после baseline.
Он содержит report, восемь evidence logs и изменения двух standalone test entry
points. Ранее перечисленные промежуточные SHA `49871f2`–`927c628` не являются
объектами этого репозитория и не используются как publication evidence.

```text
FINAL_ACCEPTANCE_CONTENT_COMMIT=c261318f9c3e0f5ec90586fc791c4e69f0e68cbd
FINAL_ACCEPTANCE_CONTENT_REMOTE_REACHABLE=YES
PREVIOUS_INTERMEDIATE_SHA_CLAIM_VERIFIED=NO
```

## 11. Known limitations

* MQL5 frontend — conservative static parser, не compiler AST. Macro expansion,
  overload resolution и broker/runtime state не могут быть полностью доказаны
  статически.
* Python frontend использует AST, но внешние runtime side effects и динамически
  созданные attributes вне доступного source статически не доказываются.
* `UNKNOWN` evidence не повышается оптимистически до match/authority; отсутствие
  статического доказательства сохраняется как rejection/partial/missing.
* Execution fill, terminal snapshot и deal history остаются фактическими только
  при runtime evidence; request или projected calculation их не заменяют.

## 12. Open conflicts, назначенные поздним этапам

Parameter profile conflicts 001–006 (`BigRatio`, `SmallRatio`, shares), mode
routing 020/031 и policy conflicts 022/023 остаются OPEN с явными conflict IDs и
resolution stages 3.1.6–3.1.8. Этот этап не выбирал численные профили и не менял
policy. При сохранённых типах/unit/sign/lifecycle это
`NOT_A_STAGE_3_1_3_BLOCKER`.

## 13. Final acceptance

Все conjunctive критерии выполнены: 230/230, table parity, declaration-scoped
identity/use/dataflow/unit/lineage/scope, 33/33 clean causal blockers, полностью
успешные suites и отсутствие runtime/policy/profile изменений. Этап 3.1.4 не
начат и требует отдельного разрешения пользователя.

```text
STAGE_3_1_3_FINAL_ACCEPTANCE=PASS
STAGE_3_1_3_STATUS=CLOSED
NEXT_STAGE=3.1.4
NEXT_STAGE_STARTED=NO
NEXT_ALLOWED_STAGE=3.1.4
AWAITING_USER_APPROVAL=YES
```

### Closure revalidation

После формирования полного отчёта production validator повторно запущен на
closure HEAD. Полный output сохранён в `final_revalidation.log`; 230 terms, 33
нулевых blockers и все suite totals повторились, terminal marker — PASS.

```text
CLOSURE_REVALIDATION=PASS
STAGE_3_1_3_NINTH_CORRECTION_VALIDATION=PASS
FINAL_ACCEPTANCE_COMMIT=c261318f9c3e0f5ec90586fc791c4e69f0e68cbd
NEXT_STAGE_STARTED=NO
AWAITING_USER_APPROVAL=YES
```

FINAL_VERDICT
STAGE_3_1_3_FINAL_ACCEPTANCE=PASS
STAGE_3_1_3_STATUS=CLOSED
NEXT_ALLOWED_STAGE=3.1.4
STAGE_3_1_4_STARTED=NO
REPOSITORY_SCOPE_VIOLATION=NO
