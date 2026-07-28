# Отчёт пятой коррекции Этапа 3.1.3

## CURRENT_STATE_AUDIT

```text
HEAD_BEFORE=a136a4ded9c38438207ce20aa9a72d76d0f0b1cd
ORIGIN_WORK_BEFORE=a136a4ded9c38438207ce20aa9a72d76d0f0b1cd
WORKTREE_BEFORE=CLEAN
FIFTH_CORRECTION_BASE_COMMIT=a136a4ded9c38438207ce20aa9a72d76d0f0b1cd
```

## PRE_FIX_DEFECT_REPRODUCTION

Независимым чтением validator до изменений подтверждены все 10 defects:

```text
scope_match hardcoded True=REPRODUCED
unit_match equals type_ok=REPRODUCED
source/authority derived from JSON authoritative=REPRODUCED
projected_actual_match checks non-empty JSON claim=REPRODUCED
lifecycle_match checks non-empty JSON claim=REPRODUCED
computed status depends on JSON-assisted dimensions=REPRODUCED
20 positive labels duplicate one base_ok=REPRODUCED
adversarial equals negatives[:10]=REPRODUCED
15 repeated score lies inflate count=REPRODUCED
source/lifecycle matrices incomplete=REPRODUCED
```

## SOURCE_DERIVED_SEMANTICS

`SourceSemanticEvidence` строится только из parsed symbol и очищенного source text declaration/read/write sites. Unit inference использует API anchors, identifier naming, input declarations и use expressions. Source authority различает POLICY, LEDGER, TERMINAL_SNAPSHOT, REQUEST, DERIVED, CACHE и TEST_ORACLE. Scope выводится из file location, storage kind и parent context. Temporal и lifecycle classes выводятся из source class/use graph, а не JSON.

```text
JSON_FIELDS_USED_AS_SEMANTIC_TRUTH=0
HARDCODED_SCOPE_MATCH=0
UNIT_MATCH_EQUALS_TYPE_MATCH=0
JSON_AUTHORITATIVE_USED_FOR_COMPUTED_AUTHORITY=0
JSON_PROJECTED_ACTUAL_USED_FOR_COMPUTED_CLASS=0
JSON_LIFECYCLE_USED_FOR_COMPUTED_LIFECYCLE=0
SOURCE_MATRIX_CLASSES=47
LIFECYCLE_MATRIX_CLASSES=16
SCHEMA_VERSION=3.1.3-fifth-correction-1
```

## MAPPING

После повторного source-derived audit 230/230 terms недоказанные mappings удалены, а не сохранены ради coverage.

```text
CANONICAL_TERMS=230
TERMS_AUDITED=230
MQL5_EXACT_MATCH=4
MQL5_SEMANTIC_MATCH=0
MQL5_PARTIAL_MATCH=44
MQL5_AMBIGUOUS=0
MQL5_MISSING=182
PYTHON_EXACT_MATCH=0
PYTHON_SEMANTIC_MATCH=0
PYTHON_PARTIAL_MATCH=39
PYTHON_AMBIGUOUS=0
PYTHON_MISSING=191
MQL5_MANUAL_REVIEWS=30
PYTHON_MANUAL_REVIEWS=30
```

Каждая retained entry хранит claims (`claimed_unit`, `claimed_scope`, `claimed_source_class`, `claimed_authoritative`, `claimed_projected_actual`, `claimed_lifecycle`, `claimed_score`, `claimed_mapping_status`) и отдельный computed source evidence object. Validator независимо пересчитывает его и сравнивает claims.

## INFERENCE COUNTERS

```text
UNIT_INFERENCE_MISSING=0
UNIT_INFERENCE_AMBIGUOUS=0
UNIT_INFERENCE_CONTRADICTORY=0
UNIT_CLAIM_MISMATCH=0
SOURCE_CLASS_UNRESOLVED=0
AUTHORITATIVE_CLAIM_MISMATCH=0
CACHE_CLAIMED_AUTHORITATIVE=0
PROJECTED_SOURCE_CLAIMED_REALIZED=0
REQUEST_SOURCE_CLAIMED_FILLED=0
PROJECTED_ACTUAL_INFERENCE_MISSING=0
PROJECTED_ACTUAL_CLAIM_MISMATCH=0
PROJECTED_MAPPED_AS_ACTUAL=0
ACTUAL_MAPPED_AS_PROJECTED=0
REQUESTED_MAPPED_AS_FILLED=0
SCOPE_INFERENCE_MISSING=0
SCOPE_CLAIM_MISMATCH=0
TEST_ONLY_MAPPED_AS_RUNTIME_EXACT=0
OFFLINE_TOOL_MAPPED_AS_RUNTIME_EXACT=0
LIFECYCLE_INFERENCE_MISSING=0
LIFECYCLE_CLAIM_MISMATCH=0
INVALID_LEDGER_LIFECYCLE=0
INVALID_DEAL_LIFECYCLE=0
INVALID_REQUEST_LIFECYCLE=0
INVALID_SNAPSHOT_LIFECYCLE=0
INVALID_POLICY_LIFECYCLE=0
CANDIDATE_SCORE_MISMATCH=0
CLAIMED_COMPUTED_MAPPING_STATUS_MISMATCH=0
```

## TESTING

Positive controls use 20 distinct named production/isolated fixtures and invoke full `validate()`. Negative controls cover 48 separately named rules without repeated score padding. The adversarial campaign is a separate 15-case list, not a slice of negative tests.

```text
NEGATIVE_TESTS_TOTAL=48
NEGATIVE_TESTS_PASSED=48
UNIQUE_NEGATIVE_RULES=48
POSITIVE_TESTS_TOTAL=20
POSITIVE_TESTS_PASSED=20
UNIQUE_POSITIVE_RULES=20
ADVERSARIAL_TESTS_TOTAL=15
ADVERSARIAL_TESTS_CAUGHT=15
UNIQUE_ADVERSARIAL_RULES=15
MONEY_AS_LOT_ATTACK=PASS
CACHE_AS_AUTHORITATIVE_ATTACK=PASS
TEST_ONLY_AS_RUNTIME_ATTACK=PASS
PRICE_AS_LOT_ATTACK=PASS
```

## SCOPE CONTROL

```text
MQL5_CHANGED=NO
MQH_CHANGED=NO
TRADING_LOGIC_CHANGED=NO
STAGE_3_1_4_STARTED=NO
BUSINESS_POLICY_CHANGED=NO
PARAMETER_PROFILE_CHANGED=NO
```

STAGE_3_1_3_FIFTH_CORRECTION_STATUS=PASS

Semantic mapping больше не зависит от JSON claims как источника истины.
Unit/source/scope/projected-actual/lifecycle evidence вычисляется независимо из исходного кода.
Этап 3.1.3 ожидает независимую проверку пользователя.
Этап 3.1.4 не выполнялся.
