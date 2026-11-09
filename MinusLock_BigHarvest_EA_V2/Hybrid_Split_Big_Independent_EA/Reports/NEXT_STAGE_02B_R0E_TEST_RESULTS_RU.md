# 02B-R0E — результаты проверок и границы доказательств

BASE_SHA=2d34c3378edc5f2df064282fa067bb4af2a1e3b0

Статус: PROPOSED / AWAITING_ADMIN_APPROVAL. Только audit/test-only; никаких production-изменений и торговли.

Новый reference: 91 различных сценариев, 8 contexts, 728 выполнений PASS, FAIL0, INFRASTRUCTURE_ERROR0. Два top-level comparisons на выполнение (actual==literal expected и context unchanged) = 1456; это не число независимых экономических сценариев. Nested field equality не искусственно суммируется. Классы каждого сценария сохранены в VERIFICATION_SUMMARY.json. Initial harness run имел16 ошибок (два scenario×8 contexts из-за shadowed replay callable), сохранён в DEVELOPMENT.json, исправление относится только к harness.

Mutation:13 причинных source mutants,13 MUTATION_KILLED, survivors0, infrastructure0. Каждый original/mutant проходит свой положительный контроль; original negative равен literal expected, mutant нарушает его без parser/runtime exception. ExactEdit/count/OriginalSourceHash/MutantSourceHash и результаты в MUTATION_RESULTS.json. Это ограниченный каталог guards R0E, не метрика универсальной устойчивости. Frozen mutation catalogs отдельно: R0B30/R0C30/R0D22, не складываются с новым13.

Денежная модель R0E сохраняет проверенную exact R0D зависимость. Expected берутся из literals и integer coefficient/scale test utilities; source evaluator не используется для expected. Inputs находятся в cases closures, fixture definitions и указанном SourceFile; Input metadata связывает их с TestID, literal vectors записаны явно. Модель не обрабатывает все мыслимые DTO ошибки: неожиданный programming exception остаётся видимым INFRASTRUCTURE_ERROR, а не маскируется REJECT. Cost registry тестирует покрытие, не вычисляет реальные broker costs; complete/fresh — independent fixture attestations, не broker evidence.

## Команды

- `PYTHONDONTWRITEBYTECODE=1 python Tests/Static/check_hsbi_02b_r0e_contracts.py`
- `PYTHONDONTWRITEBYTECODE=1 python Tests/Static/check_hsbi_02b_r0e_mutations.py`
- `PYTHONDONTWRITEBYTECODE=1 python Tests/Static/run_hsbi_02b_r0e_regressions.py`
- `PYTHONDONTWRITEBYTECODE=1 python Tests/Static/check_hsbi_02b_r0e_package.py --seal --self-test` после генерации всех новых документов; повторная read-only проверка без параметров.

Source hashes, UTC, команды и exit codes сохранены в соответствующих JSON. SourceHashes регрессий указывают entry runner; транзитивные зависимости защищены полным baseline Git inventory; R0 native evidence отдельно содержит runner hash/execution. В TestedSHA указан действительно исполнявшийся Git HEAD, новые ещё не закоммиченные subjects идентифицируются SHA256. Будущий final commit в собственные bytes не встраивается; публикация фиксируется итоговым ответом и Git objects.

## Регрессии

| Suite | ExitCode | PASS | FAIL | BaselineMatch | Классификация |
|---|---|---|---|---|---|
| R8 | 0 | 48 | 0 | True | PASS |
| R8_legacy | 0 | 13 | 0 | True | PASS |
| R8_properties | 0 | 4 | 0 | True | PASS |
| R8_sensitivity | 0 | 10 | 0 | True | PASS |
| R10 | 0 | 67 | 0 | True | PASS |
| R10_verify | 0 | 28 | 0 | True | PASS |
| R10_properties | 0 | 4 | 0 | True | PASS |
| R10_mutations | 0 | 8 | 0 | True | PASS |
| R12 | 0 | 15 | 0 | True | PASS |
| R12_alignment | 0 | 14 | 0 | True | PASS |
| R12A | 0 | 13 | 0 | True | PASS |
| R12A_coverage | 0 | 22 | 0 | True | PASS |
| R7_frozen | 1 | 57 | 5 | True | EXPECTED_HISTORICAL_FAILURE |
| 02B_R0 | 1 | 35 | 46 | True | EXPECTED_HISTORICAL_FAILURE |
| 02B_R0A | 0 | 128 | 0 | True | PASS |
| R12A_canonicalizer | 0 | 0 | 0 | True | PASS |
| R0B_reference | 0 | 141 | 0 | True | PASS |
| R0B_mutations | 0 | 30 | 0 | True | PASS |
| 02A_no_trade_scan | 0 | 74 | 0 | True | PASS |
| R0C_reference | 0 | 221 | 0 | True | PASS |
| R0C_mutations | 0 | 30 | 0 | True | PASS |
| R0C_package | 0 | None | None | True | PASS |
| R0D_reference | 0 | 944 | 0 | True | PASS |
| R0D_mutations | 0 | 22 | 0 | True | PASS |
| R0D_package_baseline | 0 | None | None | True | PASS |
| 02A_standalone | None | None | None | NOT_RUN | NOT_RUN |

R7 frozen57/62: S040B/S040C/S044A/S044B проверяют старые status keys/канонические markers, S045 — frozen manifest; они расходятся с более поздними документальными blocks/inventory (см. Reports/NEXT_STAGE_02B_R0_TEST_RESULTS_RU.md:75–81); точные failure labels и raw stdout сохранены, тест не исправлялся. R0 native35/81:46 расхождений с proposed contract — действующие blockers/contract conflicts, не новая регрессия R0E. Совпадение baseline не превращает FAIL вPASS. 02A не имеет отдельного suite: executable commands из execution report воспроизведены named runs и scanner, standalone NOT_RUN.

R0D строгий package checker выполнялся на disposable точном Git tree 2d34c33: его frozen inventory не обязан принимать будущие R0E additions. Команда, disposable --root и результат сохранены. Исторические временные пути после запуска удалены; воспроизведение делает runner.

## Package integrity

Package checker самостоятельно читает Git tree, проверяет bytes всех1135 baseline files и74 production sources; добавления только новые R0E Docs/Reports/Tests. Preservation JSON не является источником ожидаемого inventory. Negative probes обновляют хеши только disposable new artifacts для проверки семантических guards. Полнота cases/scenario IDs/executions, contexts, source/mutant hashes, ExactEdit и поля approval проверяются отдельно. Фактические positive/negative outcomes и UTC находятся в PACKAGE_RESULTS.json; они не подменяются обещанием PASS в этом тексте.

## Не выполнено и не доказано

MetaEditor/terminal64/Wine в PATH не найдены; MQL5_COMPILE/MQL5_TESTS/STRATEGY_TESTER=NOT_RUN. C++ extraction не заменяет MQL5. Broker authenticity/precision/margin, реальные partial fills, global debit attribution, durable backend/concurrent double-spend и полная NewFar integration —UNPROVEN/NOT_RUN. Restart fixtures проверяют последовательный in-memory journal reconciliation с independent fixtures, а не crash-consistent storage. Fixture no-trade scan дополняется byte-for-byte сохранностью RuntimePolicy; торговых вызовов не добавлено.

Дополнительные runner/mutation/package/generator/development файлы нужны для воспроизводимости, причинных mutations, integrity probes и раскрытия initial ошибок. Они не заменяют исторические evidence. Administrative approval нигде не присвоен.

Независимые R0D coverage probes воспроизведены новым check_hsbi_02b_r0e_r0d_provenance.py на Git archive baseline: пустые cases, context999, ложные original/mutant hashes и approval после blank line. См. NEXT_STAGE_02B_R0E_R0D_PROVENANCE_PROBES.json; это отдельное доказательство CF-18, не предположение о старом checker. Новый package self-test повторяется на замороженных R0E artifacts; первоначальный прогон с параллельным обновлением test metadata сохранён в DEVELOPMENT.json и не используется как final evidence.

Economic source registry R0E ограничен eligible CLOSE sources. Opening costs здесь проверяются как запрет harvest grant, а не как реализованный полный opening-cost economic ledger; их account-level attribution остаётся открытым решением. Старые JSON runner outputs могут сохранять historical contract baseSha; фактический проверенный SHA исполнения указан в R0E REGRESSIONS.json:TestedSHA, а полный baseline bytes подтверждён preservation Git tree. Не следует читать historical contract baseSha как текущий HEAD.

Дополнительная граница: R0E registry operations не интегрируют полный proof DTO/market receipt в свой API. Source-cap/ownership/replay доказаны как математические registry операции; verify_identity отдельно подтверждает independent expected identity. Полная композиция всех guards с durable consumption/NewFar остаётся UNPROVEN. Это не end-to-end production authorization. Финальные package probes включают также bool context ID и дублированное административное поле.
