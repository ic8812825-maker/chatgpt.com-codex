# История, текущие статусы и неподтверждённые закрытия

BASE_SHA=4185b84f7a6a8847f6a9c5796f07113907be447d

Режим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.

| Historical finding | Current issue | Status | Current evidence |
|---|---|---|---|
| L01 | FSA-001 | OPEN | full-component equality unchanged; direct source counterexample |
| L02 | FSA-002 | OPEN | bucket permutation still identical |
| M01 | FSA-003/FSA-004 | OPEN | foreign keys and exhausted source permission |
| M02 | FSA-010 | OPEN | caller copies/reconstructs expected identity, no independent reconciliation record |
| M05 Small contribution | D03/projection scope; BasketMoney:17 | OPEN | ReserveSourceProof role filter exists; projected Basket field includesSmall. Not actualgrantproof; attribution/globalfunding unresolved |
| ZeroCore/minlot | FSA-011/FSA-029 | OPEN | geometry acceptsCore0/belowmin; Trend0 integration false-reject |
| CR09 | FSA-015 | BLOCKED | maxTransition !=minCatchUp; adminpolicy needed |
| snapshot/provenance | FSA-013 +UR05/09 | BLOCKED | DTO/flags/stringdigest not durable/authentic provider |
| durable/concurrent recovery | FSA-013 | BLOCKED | productionstub, noCAS/crash tests |
| codec/MQL5 compatibility | FSA-026 | BLOCKED | R0H Python148PASS, noMetaEditor |
| legacy caller compatibility | FSA-001/010 | BLOCKED | V2 API proposed; legacy financial callers not safely migrated |
| historical R7/R0 | FSA-024/025 | OPEN | rawFAIL preserved; no frozen repair |

Источники R0A–R0H/C1/C2/C3 Reports, contracts, exact hashes и status locators индексируются HISTORICAL_INDEX.json; это не повторная полная проверка всех прошлых oracle. No old acceptance/status file changed. New reference fixes/status packages не изменили production: L01/L02/M01/M02/zeroCore нельзя считать resolved по PASS новогоPython. Текущий audit independently extracts source cases instead of доверия прежнемуобщемуPASS.

Свежие R0A128/R0B141/R0C221/R0D944/R0E728/C1840/C21264 executions сохраняют свои scope; repeated Decimal contexts — не новые сценарии. C2 schema rows отдельно2462. R0G128 иR0H148 снова выполнялись через API без old save(). Начальный R0F_API лишь перечислил116 cases (stdout116); это не test execution. Отдельный FOLLOWUP действительно вызвал все116 Run и сохранил R0F_FRESH, не подменяя metadata первого запуска.

R7=57PASS/5FAIL: S040B/S040C/S044A/S044B связаны со старыми canonical-status markers/keys, S045 — historical manifest. Это не доказательство ledger correctness и не разрешение отредактировать frozen artifacts. R0=35/46 contract cases остаются FAIL. R8/R10 теперь exit1: толькоSCOPE на трёх test-only R0H .mqh/.mq5; это конфликт устаревшего blanketnoMQL checker с разрешённым R0H harness, не изменение production тела. R12 иR12A сохранилиexit0, но их выводы ограничены qualification predicates, не full EA.

Новое: NaN risk/completion, hidden secondFar in initialslot, spent-source catchup, journal altered-body falseNOOP, gross/net metric mismatch, inactiveTrend mismatch, terminal route/proof gaps. Detailed categories/scopes — DEFECTS.json. Native broker execution всех перечисленных случаев NOT_RUN.
