# 02B-R0C — фактические тесты и source mutations

База `8903f7ba5d376dc642024ac8ab4400b884466c55`; pending new files привязаны дополнительными source hashes. Все timestamps в evidence — UTC. Только Python fixtures/static checks; MQL5/broker/runtime не выполнялись.

## Новые независимые сценарии

221 PASS, 0 FAIL, exit0. 221 именованных сценариев / 927 явно учитываемых сравнений-предикатов; это не 927 различных сценариев. Сценарии содержат control/negative/boundary/fault cases, а не только успешно отклонённые запросы. Expected literal statuses/balances заданы test source; independent wire encoder не вызывает subject digest.

221 включает14 single-field request negatives и9 authority-side origin negatives, четыре critical money negatives, snapshot ID/content/receipt, event type/range, deletion of all declared DTO keys, temporal edges, replay/context rotation, full spend/no reuse, origin/current separation, Decimal large/closure и visible injected errors. Original input objects сравниваются с копией, взятой **до** вызова. Exact NO_OP/CONFLICT/REJECT/UNAVAILABLE имеют нулевые deltas. INTERNAL serialization fault возникает после eligibility и до clone updates; исключение остаётся видимым.

## Новый mutation каталог R0C

30/30 KILLED, final survivors0, infrastructureErrors0, exit0. Это отдельный каталог, не прибавление его результатов к старому R0B30. Полнота всех возможных source mutations не заявляется.

| MutationID | CausalTestID | Итог |
|---|---|---|
| account | IDENTITY-Account | MUTATION_KILLED |
| plan | IDENTITY-Plan | MUTATION_KILLED |
| revision | REVISION-state | MUTATION_KILLED |
| revision-exhausted | REVISION-exhausted | MUTATION_KILLED |
| source | ALLOCATION-source | MUTATION_KILLED |
| allocation | ALLOCATION-state | MUTATION_KILLED |
| bucket-vector | ALLOCATION-vector | MUTATION_KILLED |
| precision | AMOUNT-precision | MUTATION_KILLED |
| grant-sum | BALANCE-sum | MUTATION_KILLED |
| reserved | BALANCE-reserved | MUTATION_KILLED |
| consumed | BALANCE-consumed | MUTATION_KILLED |
| replay | REPLAY-changed | MUTATION_KILLED |
| history | HISTORY-empty | MUTATION_KILLED |
| confirmed | SOURCE-unconfirmed | MUTATION_KILLED |
| freshness | SNAPSHOT-expired | MUTATION_KILLED |
| role | SOURCE-role | MUTATION_KILLED |
| proof-digest | DIGEST-forged | MUTATION_KILLED |
| raw-sum | RAW-net-mismatch | MUTATION_KILLED |
| posted-net | POSTED-net-mismatch | MUTATION_KILLED |
| record-identity | RECORD-Magic | MUTATION_KILLED |
| snapshot-id | SNAPSHOT-id | MUTATION_KILLED |
| snapshot-content | SNAPSHOT-content | MUTATION_KILLED |
| event-type | EVENT-invalid-True | MUTATION_KILLED |
| event-range | EVENT-invalid-18446744073709551616 | MUTATION_KILLED |
| future | TIME-future | MUTATION_KILLED |
| missing-field-default | MISSING-event | MUTATION_KILLED |
| atomic-input | DIGEST-forged | MUTATION_KILLED |
| success-input-alias | APPLY-input-unchanged | MUTATION_KILLED |
| allocation-internal | ALLOCATION-internal | MUTATION_KILLED |
| time-domain | TIME-domain | MUTATION_KILLED |

Для каждого mutant сохранены exact edits, original/mutant source hashes, positive control, original negative, mutant negative и literal expected zero deltas. Новый evaluator выполняет causal vector на fresh независимых объектах. Exception => INFRASTRUCTURE_ERROR, никогда KILLED.

**Раскрытые initial результаты:** первый R0C каталог28 дал26 KILLED,1 SURVIVED (shared input alias) и1 INFRASTRUCTURE_ERROR (event-type). Они не удалены: `Tests/Evidence/NEXT_STAGE_02B_R0C_DEVELOPMENT_CHECKS.json#initialMutationRun`. Full-suite mutant event-type доходил до других non-integer event, вызывавших exception; финальный causal runner изолирует True-case, не засчитывая прежнюю ошибку. Alias assertion использовал уже изменённый shared fixture и пропускал дефект; контроль исправлен на fresh fixture. Тот же alias edit повторён отдельной success-input-alias mutation и теперь KILLED. Дополнительно проверяется poisoning state на rejected call. Initial four expected REJECT для foreign record key уточнены до normative CONFLICT; это ошибка начальных expectations, не ослабление model. Проверка unsupported object заменена equality-stable set, чтобы deepcopy identity object не имитировал mutation.

## Исторические regressions

| Suite | Exit | PASS | FAIL | Совпадает baseline |
|---|---:|---:|---:|---|
| R8 | 0 | 48 | 0 | True |
| R8_legacy | 0 | 13 | 0 | True |
| R8_properties | 0 | 4 | 0 | True |
| R8_sensitivity | 0 | 10 | 0 | True |
| R10 | 0 | 67 | 0 | True |
| R10_verify | 0 | 28 | 0 | True |
| R10_properties | 0 | 4 | 0 | True |
| R10_mutations | 0 | 8 | 0 | True |
| R12 | 0 | 15 | 0 | True |
| R12_alignment | 0 | 14 | 0 | True |
| R12A | 0 | 13 | 0 | True |
| R12A_coverage | 0 | 22 | 0 | True |
| R7_frozen | 1 | 57 | 5 | True |
| 02B_R0 | 1 | 35 | 46 | True |
| 02B_R0A | 0 | 128 | 0 | True |
| R12A_canonicalizer | 0 | 0 | 0 | True |
| R0B_reference | 0 | 141 | 0 | True |
| R0B_mutations | 0 | 30 | 0 | True |
| 02A_no_trade_scan | 0 | 74 | 0 | True |
| 02A | None | None | None | NOT_RUN |

Полные Command/StartedUtc/FinishedUtc/TestedSHA/SourceHashes/ExitCode/stdout/stderr/count scope в новом REGRESSIONS JSON. Результаты R0/R0A/R0B направлены в новые R0C_*_RECHECK JSON; исторические evidence не перезаписывались. Old R0B30 recheck сохраняет initial8 R0A survivors и final0; он не доказывает четыре дополнительные защиты. Отдельный reproduction каждой из четырёх ослабленных R0B copies дал141PASS.

R7 остаётся57/62, exit1: S040B/S040C/S044A/S044B — frozen status expectations, S045 — старый manifest; это не доказанная функциональная торговая регрессия. R0: native81=35/46, reference58, source probes13, exit1. Общий REGRESSION_TESTS=FAIL, REGRESSION_BASELINE_MATCH=YES. Нулевой exit R0C regression orchestrator означает совпадение ожидаемых exits, а не превращение R7/R0 в PASS.

02A standalone отсутствует; все доступные команды его execution report повторены. R12A canonicalizer exit0 выполнил0 assertions, scope ограничен. Fresh no-trade scanner проверил74 production files,0 matches и10 scanner controls; native runtime не доказан.

## Команды воспроизведения

```bash
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0c_contracts.py --output Tests/Evidence/NEXT_STAGE_02B_R0C_TEST_RESULTS.json
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0c_mutations.py --reproduce --output Tests/Evidence/NEXT_STAGE_02B_R0C_REPRODUCTION.json
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0c_mutations.py --output Tests/Evidence/NEXT_STAGE_02B_R0C_MUTATION_RESULTS.json
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/run_hsbi_02b_r0c_regressions.py
```

Команды обновляют только новые R0C evidence. Для сохранения самого R0C snapshot перед новым запуском использовать отдельные новые R0C output names либо disposable checkout. Tests/Reference oracle не импортирует исторические модели; old runner/fixture загружаются только reproducibility/regression tools.

MQL5_COMPILE/MQL5_TESTS/STRATEGY_TESTER=NOT_RUN. Broker authenticity/margin/precision, durable journal/CAS/concurrency/restart, global source funding, own-reservation settlement, real partial fills/NewFar integration остаются NOT_RUN/UNPROVEN. Python PASS не является production readiness.

## Проверка состава пакета

`PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0c_package.py` проверяет Git blob/SHA256 всех1087 исходных project files, hashes новых файлов, source hashes test/mutation/regression evidence, source lines matrix и пустые поля approval. Это проверка целостности пакета, не дополнительный денежный oracle.

Добавлены22 новых файла; extra files нужны для четырёх fresh historical rechecks, раскрытия development outcomes и исполнимой проверки сохранности. Полный inventory находится в `Tests/Evidence/NEXT_STAGE_02B_R0C_PRESERVATION.json#newFiles`.
