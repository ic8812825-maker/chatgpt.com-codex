# HSB.1V — фактический результат MQL5 unit-тестов

Дата попытки: `2026-08-11T11:26:45Z`. Target SHA-256: `8d7a691bc7b9de688a9f73d2f456bfdeddea0cc5f4699804aba74d519ab93e6c`.

Выполнены `command -v terminal64`, `command -v metatester64` и поиск соответствующих файлов в `/opt`, `/usr`, `/workspace` с `-maxdepth 5`. Результат пуст: MT5 Terminal и MetaTester недоступны. Experts log, Journal и runtime summary не созданы. Python и имитация не применялись.

Статическая проверка declarations правильной командой дала 26 уникальных ID: `T01`–`T26`; duplicates и gaps отсутствуют. Это не подменяет MQL5 runtime evidence.

| Test ID | Requirement ID | Expected | Actual | Status | Reason code |
|---|---|---|---|---|---|
| T01 | HSBI-ID-010 | normal ulong lossless | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T02 | HSBI-ID-010 | above INT_MAX lossless | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T03 | HSBI-ID-010 | ULONG_MAX lossless | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T04 | HSBI-ID-010 | identity high bits retained | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T05 | HSBI-ID-010 | fingerprint stable | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T06 | HSBI-GEN-030 | REAL_LIMITED blocked | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T07 | HSBI-PERSIST-001 | schema versions rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T08 | HSBI-ID-010 | invalid identity scopes rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T09 | HSBI-FSM-002 | invalid state/revision/reconciliation rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T10 | HSBI-ID-010 | invalid roles/volume/Far/pending rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T11 | HSBI-TX-006 | PLACED blocked | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T12 | HSBI-TX-006 | PARTIAL blocked | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T13 | HSBI-TX-006 | TIMEOUT routes reconciliation | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T14 | HSBI-TX-006 | wrong ActionID rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T15 | HSBI-TX-006 | stale EventID rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T16 | HSBI-TX-006 | fresh event/wrong action rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T17 | HSBI-TX-006 | actual deal/volume required | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T18 | HSBI-TX-006 | full completed barrier contract | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T19 | HSBI-TX-006 | same ActionID pending retry only | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T20 | HSBI-TX-006 | completed retry forbidden/conflict terminal-safe | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T21 | HSBI-ID-010 | foreign account/symbol/magic rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T22 | HSBI-ID-010 | foreign cycle/identifier/role rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T23 | HSBI-ID-010 | stale/reused ticket rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T24 | HSBI-ID-010 | changed volume/direction rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T25 | HSBI-NF-001 | second Far rejected/actual residual required | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T26 | HSBI-GEN-030 | FSM/no-trade guard | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |

```text
DECLARED_TEST_IDS=26
UNIQUE_TEST_IDS=26
T01_TO_T26_COMPLETE=YES
MQL5_UNIT_TESTS=NOT_RUN_ENVIRONMENT_UNAVAILABLE
PASS=NOT_AVAILABLE
FAIL=NOT_AVAILABLE
```

`26/26 PASS` не заявляется без фактического Experts/Journal evidence.
