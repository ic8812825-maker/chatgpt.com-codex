# HSB.1V — фактический результат MQL5 unit-тестов

Дата попытки: `2026-08-10T11:04:58Z`. Target: `Tests/MQL5/HSBI_Skeleton_Tests.mq5`; SHA-256: `994986d7e77a58590bcb04871b4c6c458e76710b8f4a4339c5518bad61428da8`.

MT5 Terminal/MetaTester и Wine в PATH и доступных каталогах `/opt`, `/usr`, `/workspace` не найдены. Поэтому script фактически подготовлен к запуску, но выполнить его невозможно. Python/эмуляция не запускались. Build MT5, Experts log и Journal: `UNAVAILABLE`; summary и ошибки выполнения: `NOT_PRODUCED`.

| Test ID | Requirement ID | Expected | Actual | Status | reason code |
|---|---|---|---|---|---|
| T01 | HSBI-GEN-030 | UNIT_TEST allowed | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T02 | HSBI-GEN-030 | REAL_LIMITED rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T03 | HSBI-ID-010 | ulong > int preserved | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T04 | HSBI-ID-010 | valid tuple accepted | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T05 | HSBI-ID-010 | other Symbol rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T06 | HSBI-ID-010 | other Magic rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T07 | HSBI-ID-010 | other Account rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T08 | HSBI-ID-010 | other CycleID rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T09 | HSBI-ID-010 | other PositionIdentifier rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T10 | HSBI-ID-010 | other Role rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T11 | HSBI-ID-010 | stale/reused ticket ignored | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T12 | HSBI-ID-010 | changed volume rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T13 | HSBI-ID-010 | changed role rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T14 | HSBI-ID-010 | two Far rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T15 | HSBI-NF-001 | actual residual only | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T16 | HSBI-FSM-002 | allowed transition accepted | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T17 | HSBI-FSM-002 | forbidden transition rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T18 | HSBI-TX-006 | PLACED blocks transition | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T19 | HSBI-TX-006 | PARTIAL_FILL blocks transition | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T20 | HSBI-TX-006 | TIMEOUT blocks transition | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T21 | HSBI-TX-006 | COMPLETED_FILL permits transition | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T22 | HSBI-TX-006 | delayed/duplicate rejected | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T23 | HSBI-TX-006 | retry retains ActionID | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T24 | HSBI-RECON-002 | conflict routes RECONCILING | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T25 | HSBI-FSM-002 | critical routes EMERGENCY/TERMINAL_SAFE | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |
| T26 | HSBI-FSM-002 | closed pending rejected; revision preserved | unavailable | NOT_RUN | ENVIRONMENT_UNAVAILABLE |

```text
MQL5_UNIT_TESTS=NOT_RUN_ENVIRONMENT_UNAVAILABLE
MQL5_UNIT_TESTS=NOT_RUN_ENVIRONMENT_UNAVAILABLE
TOTAL_PLANNED=26
PASS=NOT_AVAILABLE
FAIL=NOT_AVAILABLE
```

Требование `26/26 PASS; 0 FAIL` не объявляется без фактических Experts/Journal logs.
