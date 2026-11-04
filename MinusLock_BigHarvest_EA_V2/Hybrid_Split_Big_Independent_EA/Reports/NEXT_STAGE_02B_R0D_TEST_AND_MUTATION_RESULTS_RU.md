# 02B-R0D — фактические тесты и mutations

База `ec7ae40fe22e1d6e5bed035450750502a1182ab5`; новые pending sources связаны SHA256. В evidence сохраняются UTC, command, source hashes, tested SHA и исходные exit codes. Все новые контракты PROPOSED.

## Reference и context

118 разных сценариев,8 configurations, 944 executions, 4696 явно учитываемых comparison predicates, 944PASS/0FAIL/0INFRASTRUCTURE_ERROR, exit0. Эти числа не складываются. Predicate counts считают явные проверки/поля; вложенный trace — составной предикат, не отдельное утверждение на каждый Python operator.

Direct calls всех11 APIs и composed posted/allocation/balance/authorization/apply/next/full/replay/spent path проверены. Домен включает1e64 closure, большой1e28 reserve, minor-unit−1/0/+1 при KWD3, cancellation−.005, prefix rejection/unknown/unsupported, typed snapshot pairs и visible injected RuntimeError. Expected — literal vectors и integer coefficient/scale; Fraction используется subject, не expected arithmetic. Independent wire encoder не вызывает subject canonical/digest.

Context configurations в TEST_RESULTS: precision1/2/3/9/28/64/100/256, разные rounding, sticky flags, all traps, Emax/Emin вплоть до0. Каждый вызов сохраняет context неизменным. Ни один публичный helper не требует caller setup context. Subject не выполняет Decimal арифметику.

## Новый каталог v2

22/22 KILLED, final survivors0, infrastructureErrors0. Causal positive control проходит, original negative совпадает с independent expected, mutant нарушает outcome. Exception никогда не KILLED. Полнота всех мыслимых mutations не заявляется.

| MutationID | CausalTestID | Итог |
|---|---|---|
| amount-positive | amount-negative | MUTATION_KILLED |
| available-reserved | reserved-available | MUTATION_KILLED |
| posted-grid | posted-grid | MUTATION_KILLED |
| local-verified | local-unverified | MUTATION_KILLED |
| worst-ambient-context | WORST-cancellation | MUTATION_KILLED |
| sequential-ambient-context | SEQUENTIAL-large | MUTATION_KILLED |
| lost-small-consumption | SEQUENTIAL-large | MUTATION_KILLED |
| margin-sign | WORST-cancellation | MUTATION_KILLED |
| snapshot-type | snapshot-type-decimal | MUTATION_KILLED |
| canonical-type-collision | CODEC-str-decimal | MUTATION_KILLED |
| snapshot-receipt | snapshot-content | MUTATION_KILLED |
| post-state-validation | POSTSTATE-fault | MUTATION_KILLED |
| consumed-reavailable | COMPOSITION-full | MUTATION_KILLED |
| altered-replay | COMPOSITION-replay-conflict | MUTATION_KILLED |
| unsupported-domain | DOMAIN-direct | MUTATION_KILLED |
| snapshot-schema | snapshot-schema | MUTATION_KILLED |
| raw-net | raw-sum | MUTATION_KILLED |
| proof-digest | digest-forged | MUTATION_KILLED |
| source-role | source-role | MUTATION_KILLED |
| source-history | history-missing | MUTATION_KILLED |
| posted-net | posted-net | MUTATION_KILLED |
| input-alias | CONTROL-apply | MUTATION_KILLED |

Для amount/available/consumed-reavailable ранний guard ослаблен, но обязательный post-state balance блокирует invalid state: original REJECT против mutant UNAVAILABLE, zero financial deltas. Это обнаруженное расхождение typed outcome, **не фактический double spend**. Безопасность обязательного post-state gate отдельно проверена POSTSTATE-fault: injected debit формирует invalid copied state; original отклоняет без изменения исходников/journal, removal postgate допускает commit. INTERNAL-error-visible поднимает RuntimeError без silent REJECT. Удаление post-state guard при обычных допустимых входах и доказанно корректном debit эквивалентно по closure proof; его causal test явно расширяет область до injected invalid-debit fault. Это fault-containment probe, не найденный обычный double spend. Snapshot-type removal также остаётся финансово заблокированным codec/receipt, меняя REJECT на CONFLICT. Эти границы раскрыты в EquivalenceAnalysis.

Initial каталог v1:21KILLED/1SURVIVED/0errors. Survived unsupported-domain был замаскирован ранней Decimal-specific проверкой. Добавлен публичный text-number vector DOMAIN-direct; тот же source edit теперь обнаруживается. initialVectorReplay сохраняет исполнимое подтверждение, что старый DTO-вектор остаётся masked. Исторический initial snapshot каталога и причина перехода v1→v2 сохранены в DEVELOPMENT JSON. Ранняя SyntaxError harness до исполнения каталога также раскрыта как инфраструктурная ошибка, а не kill.

## Исторические regressions

| Suite | Exit | PASS | FAIL | BaselineMatch |
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
| R0C_reference | 0 | 221 | 0 | True |
| R0C_mutations | 0 | 30 | 0 | True |
| R0C_package | 0 | None | None | True |
| 02A | None | None | None | NOT_RUN |

R7 frozen57/62 и R0 native35/46 остаются FAIL/exit1; REGRESSION_BASELINE_MATCH=YES не превращает их в PASS. R12A canonicalizer выполняет0 assertions; package checker R0C не публикует comparable case count. R0B/R0C mutation catalogs по30 выполнены отдельно от нового22. Старые221 tests и30mutations не переопределены новым результатом. 02A standalone отсутствует; команды archived execution report повторены, scan74 files/0matches плюс7 positive/3 negative controls. MQL5_COMPILE/MQL5_TESTS/STRATEGY_TESTER=NOT_RUN.

## Package verification

Новый checker самостоятельно читает baseline Git tree и проверяет полный inventory, bytes/blob/SHA256, scope, source hashes, matrix function/line refs, per-row/aggregate verdict и пустые approvals. Seven disposable-copy negatives: missing inventory, altered historical source, spoofed source hash, wrong total, FAIL row under aggregate PASS, missing mandatory file, outside-scope file. Там, где меняется новый JSON, его preservation hash обновляется **в disposable copy**, чтобы не маскировать целевую semantic проверку простым hash mismatch. Actual findings в PACKAGE_RESULTS; historical originals не трогаются.

Self-referential PRESERVATION и PACKAGE_RESULTS исключены из newArtifactHashes; их inventory/schema/verdict проверяются, а окончательные bytes привязываются Git commit. Это явное исключение против self-hash cycle, не гарантия внешней подписи evidence. Default checker read-only; --self-test создаёт только disposable copies и новый PACKAGE_RESULTS.

## Воспроизведение

```bash
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0d_contracts.py --output Tests/Evidence/NEXT_STAGE_02B_R0D_TEST_RESULTS.json
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0d_mutations.py --reproduce --output Tests/Evidence/NEXT_STAGE_02B_R0D_REPRODUCTION.json
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0d_mutations.py --output Tests/Evidence/NEXT_STAGE_02B_R0D_MUTATION_RESULTS.json
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0d_package.py --self-test
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0d_package.py
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/run_hsbi_02b_r0d_regressions.py
```

Для повторного запуска с записью сохранить текущие R0D evidence в disposable checkout либо новые output names и осознанно обновить новый preservation manifest; иначе hash checker правильно обнаружит изменившиеся timestamps/bytes. Исторические evidence нельзя перезаписывать.

Broker authenticity/precision/margin, real fills, durable restart/CAS/concurrency, global source funding и NewFar integration не доказаны. Python/model readiness не является trading readiness.
