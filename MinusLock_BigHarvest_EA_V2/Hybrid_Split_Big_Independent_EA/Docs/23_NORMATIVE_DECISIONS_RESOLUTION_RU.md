# 23. Единый реестр нормативных решений HSB.0R-C

Версия: HSB.0R-C.2
Статус: MAPPING_COMPLETE

## Карта внедрения решений

| Decision ID | Owner document | Зависимые документы | Раздел owner-документа | Requirement ID | Текущий текст | Новый нормативный текст | Удаляемая неоднозначность | Test vector | Статус |
|---|---|---|---|---|---|---|---|---|---|
| HSBI-DEC-001 | 04_MATHEMATICAL_MODEL | 03,05,10,14,15 | Объёмы C/T/S | HSBI-MATH-001..006 | ratios без полного safe contract | broker-grid C/T/S, ranges, post-rounding gates | fixed profile как default | V1-V6 | MAPPED |
| HSBI-DEC-002 | 08_MONEY_LEDGER | 03,10,11,12,13 | Allocation | HSBI-MONEY-001..020 | общие buckets | per-source conservation и isolation | двойной учёт | V7 | MAPPED |
| HSBI-DEC-003 | 05_GEOMETRY_MODEL | 03,04,10,12,13,15 | Control prices | HSBI-GEO-010..018 | не типизированы | typed Bid/Ask prices, timestamp, freshness | stale/theoretical price | V1,V2,V8 | MAPPED |
| HSBI-DEC-004 | 14_NEW_FAR_SOLVER | 03,04,13,15 | Future Small | HSBI-NF-010..018 | depth 1 | exact recursion + conservative bound | скрытый dead-end | V11,V12 | MAPPED |
| HSBI-DEC-005 | 14_NEW_FAR_SOLVER | 03,04,13 | Objective | HSBI-NF-001..009 | fixed target ratio | deterministic minimum-safe selection | неоднозначный optimum | V3-V6,V12 | MAPPED |
| HSBI-DEC-006 | 15_RISK_AND_MARGIN | 03,06,12,17 | Emergency | HSBI-RISK-020..030 | смешение с Final Close | отдельная Emergency authority | ложный recovery PASS | reject routes | MAPPED |
| HSBI-DEC-007 | 13_SMALL_TRANSITION | 04,08,15 | Transition Loss | HSBI-SMALL-020..026 | один лимит | min четырёх caps | неконтролируемый loss | V10 | MAPPED |
| HSBI-DEC-008 | 12_FINAL_CLOSE | 03,04,08 | Threshold | HSBI-FC-001..012 | неполный threshold | profit+buffer+tolerance | разные формулы | V8,V9 | MAPPED |
| HSBI-DEC-009 | 15_RISK_AND_MARGIN | 03,10,13,14 | Limits | HSBI-RISK-001..019 | нестрогие limits | typed configurable ranges, fail-closed | silent unsafe defaults | stress vectors | MAPPED |
| HSBI-DEC-010 | 02_ROLES_AND_IDENTITY | 03,07,09,16,17,18 | Scope | HSBI-ID-001..015 | Symbol+Magic | Account+Symbol+Magic+CycleID+identifier+role | cross-cycle ownership | identity vectors | MAPPED |
| HSBI-DEC-011 | 16_PERSISTENCE | 06,07,08,17,18 | Backend | HSBI-PERSIST-001..018 | общая snapshot идея | crash-consistent versioned commit + journal | ложная атомарность | crash vectors | MAPPED |
| HSBI-DEC-012 | 21_PRODUCTION_READINESS | 03,15,18 | REAL_LIMITED | HSBI-PROD-010..020 | future real unspecified | explicit approval+all gates | несанкционированный real | production gates | MAPPED |
| HSBI-DEC-013 | 05_GEOMETRY_MODEL | 03,06,13 | Small confirmation | HSBI-GEO-019..025 | touch only | repeated fresh snapshot+debounce | false trigger | V1,V2 | MAPPED |
| HSBI-DEC-014 | 07_TRANSACTION_CONTRACT | 03,06,09..13,17 | Retry/timeout | HSBI-TX-020..032 | retry unspecified | same ActionID+history+reconciliation | duplicate request | timeout vectors | MAPPED |

Evidence подтверждает норму, но не заменяет owner-документ. Reports не являются нормативным source of truth.