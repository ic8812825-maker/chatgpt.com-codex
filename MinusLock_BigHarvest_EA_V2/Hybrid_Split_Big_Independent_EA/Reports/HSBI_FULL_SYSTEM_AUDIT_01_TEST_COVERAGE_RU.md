# Доказательства и реальные границы покрытия

BASE_SHA=4185b84f7a6a8847f6a9c5796f07113907be447d

Режим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.

`STATICALLY_INSPECTED`, `REFERENCE_EXECUTED`, `EXTRACTED_CPP_SUBSET_EXECUTED_NOT_NATIVE`, `HISTORICAL_EVIDENCE_ONLY`, `NOT_RUN`, `UNVERIFIED` не взаимозаменяемы.

## Текущие независимые проверки

- Main manual51/51lines read;31 ownerdocuments fullread;133 docsindexed. Historical appendices не все заново семантически проверены.
- 74/74 production files статически рассмотрены;199 declarations;16 mainincludeclosure;13 conservative entry-reachable functions. Никакой «процентготовности» не вычисляется.
- C++extracted **54 scopedchecks: 27PASS/27FAIL** against normative/caller expectations. Real source bodies, but LP64/math/string adapters and explicit synthetic calculation-only brokerstubs. Not MetaEditor/nativeMT5. Нельзя считать codefile-leveladapter compilation выполнением всех functions.
- **20 analytical accounting scenarios PASS**, initial/final balances/quotes/positions/traces сохранены. No signals/scenario controllers executed.
- **15 abstract invariant families**, **245 exact-distinct generated positive/negative input pairs PASS**, seed20261111. Из360 rawpairs удалены115 exactduplicates. Numeric variants не245 независимых mathematical proofs.
- **15 analytical guard mutations killed**; no parser/runtime exception counted kill. Первоначальный14/15 survivor иточные initialsourcebytes сохранены в DEVELOPMENT/INITIAL_REFERENCE_SOURCE; причина — неправильный positivecontrol для attribution, исправлен тестfixture, не production.
- **20 exact spec-arithmetic vectors PASS**. Это отдельный oracle/literal checklist, не полный native coverage всех49families/137sourcesites.

## Свежие historical commands

| Run | Actual exit | Pass/Fail counts | Count scope |
|---|---|---|---|
| R8 | 1 | None/None | Actual CLI stdout retained; aggregate acceptance findings separate from scenario counts |
| R10 | 1 | None/None | Actual CLI stdout retained; aggregate acceptance findings separate from scenario counts |
| R12 | 0 | None/None | Actual CLI stdout retained; aggregate acceptance findings separate from scenario counts |
| R12A | 0 | None/None | Actual CLI stdout retained; aggregate acceptance findings separate from scenario counts |
| R7_FROZEN | 1 | 57/5 | Frozen static checks |
| R0 | 1 | 35/46 | Frozen extracted C++ contract cases; not MQL5 native |
| R0A | 0 | 128/0 | Historical runner own test/execution counting; contexts not distinct scenarios |
| R0B | 0 | 141/0 | Historical runner own test/execution counting; contexts not distinct scenarios |
| R0C | 0 | 221/0 | Historical runner own test/execution counting; contexts not distinct scenarios |
| R0D | 0 | 944/0 | Historical runner own test/execution counting; contexts not distinct scenarios |
| R0E | 0 | 728/0 | Historical runner own test/execution counting; contexts not distinct scenarios |
| C1 | 0 | 840/0 | Historical runner own test/execution counting; contexts not distinct scenarios |
| C2 | 0 | 1264/0 | Historical runner own test/execution counting; contexts not distinct scenarios |
| R0F_API | 0 | None/None | Direct immutable API run; see actual stdout |
| R0G_API | 0 | None/None | Direct immutable API run; see actual stdout |
| R0H_API | 0 | None/None | Direct immutable API run; see actual stdout |

Полные commands,UTC,start/end,subject/runner hashes,actual stdout/stderr и outputpaths в REGRESSIONS/EXECUTIONS. PassCount=None означает runner не выдал сопоставимый counter; не заменён0 или выдуманнымPASS. R8/R10 SCOPE failures раскрыты в AcceptanceDetail, R0F enumeration отдельно от fresh116 execution. Overall historical regressions=FAIL. Отличие от C3 только scopeR8/R10 не автоматически «functional regression», source bytes preserved и exactfindingsquoted. Full279Python scripts и все прежниеmutations/packagechecks не выполнялись.

## Не выполнено / не доказано

MQL5main/harness compile, native MQL5 execution, brokerOrderCalcProfit/OrderCalcMargin, actual history/partialfill/requote/timeout/retcode processing, durable restart/crash/CAS/concurrency, full account globalfunding, operational finalclose/smalltransition/NewFar promotion, backtest/demo/statistical profitability — NOT_RUN/UNVERIFIED/UNIMPLEMENTED согласно контексту. Эти статусы неconvertedPASS. Old accepted UNIT/static/model evidence cannot substitute. Package verification proves artifact integrity/consistency only, not the truth of all mathematical/systemclaims.

## Повторение новых проверок

`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_common.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_reference.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_math.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_regressions.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_followup.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_build.py`

Sourceextraction success exit0 means reproduction infrastructure succeeded, не normative sourcechecks allPASS. Actual EXTRACTED.json.Fail оставлен27. Начальные development failures nothidden. Финальный VERIFY orchestrator captures fresh subprocess exits without rewriting frozenfiles; default packageverification read-only.
