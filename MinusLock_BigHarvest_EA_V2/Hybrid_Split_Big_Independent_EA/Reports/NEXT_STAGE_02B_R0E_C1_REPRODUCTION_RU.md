# 02B-R0E-C1 — независимое воспроизведение замечаний

BASE_SHA=074165b38f1b6d6253a9629c7d2def988e8e286a

PROPOSED / AWAITING_ADMIN_APPROVAL. Audit/test-only; production/trading/dispatch запрещены.

Штатный R0E: 728 PASS; исходный каталог13: 13/13; старые package probes23: 23/23. Это отдельные executions, не новый общий числитель. Команды/UTC/TestedSHA/SourceHashes в REPRODUCTION.json. Архив074165b получен git archive; /tmp предыдущего review не использовался.

## C1-01 — CONFIRMED

Source: Tests/Static/check_hsbi_02b_r0e_package.py / verify.

Expected: REJECT_TAMPERED_PACKAGE.

Actual: `"ACCEPT"`.

Boundary: Old package checker semantic validation. Полные positive controls, inputs и deltas — JSON.

## C1-02-approval — CONFIRMED

Source: Tests/Static/check_hsbi_02b_r0e_package.py / verify.

Expected: REJECT_TAMPERED_PACKAGE.

Actual: `"ACCEPT"`.

Boundary: Old package checker semantic validation. Полные positive controls, inputs и deltas — JSON.

## C1-02-admin — CONFIRMED

Source: Tests/Static/check_hsbi_02b_r0e_package.py / verify.

Expected: REJECT_TAMPERED_PACKAGE.

Actual: `"ACCEPT"`.

Boundary: Old package checker semantic validation. Полные positive controls, inputs и deltas — JSON.

## C1-02-dispatch — CONFIRMED

Source: Tests/Static/check_hsbi_02b_r0e_package.py / verify.

Expected: REJECT_TAMPERED_PACKAGE.

Actual: `"ACCEPT"`.

Boundary: Old package checker semantic validation. Полные positive controls, inputs и deltas — JSON.

## C1-08 — CONFIRMED

Source: Tests/Static/check_hsbi_02b_r0e_package.py / verify.

Expected: REJECT_TAMPERED_PACKAGE.

Actual: `"ACCEPT"`.

Boundary: Old package checker semantic validation. Полные positive controls, inputs и deltas — JSON.

## C1-04 — CONFIRMED

Source: Tests/Reference/hsbi_02b_r0e_contract_model.py / reserve_available.

Expected: UNAVAILABLE availability.

Actual: `{"availability": ["KNOWN_MODEL_AVAILABLE", ["NUMBER", "50", "1"]], "spend": "UNAVAILABLE"}`.

Boundary: No double spend; spend remains blocked. Полные positive controls, inputs и deltas — JSON.

## C1-05 — CONFIRMED

Source: Tests/Reference/hsbi_02b_r0e_contract_model.py / transition_status.

Expected: Must not confirm target-account batch with foreign fill.

Actual: `["CONFIRMED", ["NUMBER", "0", "1"]]`.

Boundary: Missing batch scope; not broker execution. Полные positive controls, inputs и deltas — JSON.

## C1-06 — CONFIRMED

Source: Tests/Reference/hsbi_02b_r0e_contract_model.py / costs_status.

Expected: Not complete cost proof.

Actual: `{"empty": "PASS", "omitted": "PASS"}`.

Boundary: Old helper checks supplied rows only. Полные positive controls, inputs и deltas — JSON.

## C1-07 — CONFIRMED

Source: Tests/Reference/hsbi_02b_r0e_contract_model.py / verify_identity.

Expected: Not allocation-event-bound PASS.

Actual: `"PASS"`.

Boundary: Source-context helper scope. Полные positive controls, inputs и deltas — JSON.

## C1-09 — CONFIRMED

Source: Tests/Static/check_hsbi_02b_r0e_contracts.py / cases.

Expected: Exact subject operation mapping; observed presence alone is not exact target proof.

Actual: `{"DesignatedCases": [{"ActualOperation": "checked_mul", "Classification": "CONFIRMED", "Reported": "checked_add", "SourceTest": "Tests/Static/check_hsbi_02b_r0e_contracts.py", "TestID": "MQL-mul-overflow"}, {"ActualOperation": "transition_status", "Classification": "CONFIRMED", "Reported": "reserve_available", "SourceTest": "Tests/Static/check_hsbi_02b_r0e_contracts.py", "TestID": "D05-unsupported-aggregate"}], "FullMatrixReviewed": 91, "ReportedFunctionNotCalled": 17}`.

Boundary: Static source traceability, no production execution. Полные positive controls, inputs и deltas — JSON.

## Три дополнительные mutations

- R0E-extra-raw: stock=728 PASS, original=REJECT, mutant=COMMITTED_IN_MEMORY; CONFIRMED.
- R0E-extra-grid: stock=728 PASS, original=REJECT, mutant=RECORD_ACCEPTED; CONFIRMED.
- R0E-extra-namespace: stock=728 PASS, original=REJECT, mutant=COMMITTED_IN_MEMORY; CONFIRMED.

Grid case — прямое принятие record, не доказанный spend. Journal case — false known available при реально блокируемом operate, не double spend. Partial fills/cost/allocation cases классифицированы как неполный scope, исправленный новыми mandatory callers C1. C1-09 исходные ссылки проверены против реально вызываемых операций; новая матрица также содержит observed SubjectCalls.
