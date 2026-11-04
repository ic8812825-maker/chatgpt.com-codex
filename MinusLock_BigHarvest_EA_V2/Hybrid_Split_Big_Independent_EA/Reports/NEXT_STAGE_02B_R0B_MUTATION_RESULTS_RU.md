# 02B-R0B — независимые mutation results

База `9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b`, ветка work. Audit/test-only. Production-код не изменён, исторические records/evidence не переписаны. Все решения ждут администратора.

Исходный R0A model: 128 original vectors PASS; 15 новых supplementary causal vectors PASS на неизменённой модели. New oracle: 141 literal-contract vectors PASS. Mutations применялись к отдельным Python copies в project/Tests temporary directory. Include/main/frozen tests не менялись. Original/mutant SHA-256 и текст edits сохранены; parser/import/runtime exception — infrastructure error, не kill.

**Всего 30 probes:** R0A15 + R0B15. **Initial survivors: 8**, раскрыты ниже. **Final survivors: 0** после добавленных tests; infrastructure errors финального runner: 0. Это не универсальный mutation score и не MQL5 production remediation.

| Model | Mutation | Target test | Initial | Final | Минимальный actual / expected |
|---|---|---|---|---|---|
| R0A | account_namespace | OLD-account | MUTATION_SURVIVED | MUTATION_KILLED | "ELIGIBLE_FOR_COMMIT" / "REJECT" |
| R0A | plan | OLD-plan | MUTATION_KILLED | MUTATION_KILLED | "ELIGIBLE_FOR_COMMIT" / "REJECT" |
| R0A | revision | OLD-revision | MUTATION_KILLED | MUTATION_KILLED | "ELIGIBLE_FOR_COMMIT" / "REJECT" |
| R0A | source_identity | OLD-source | MUTATION_KILLED | MUTATION_KILLED | "ELIGIBLE_FOR_COMMIT" / "REJECT" |
| R0A | allocation_identity | OLD-allocation | MUTATION_SURVIVED | MUTATION_KILLED | "ELIGIBLE_FOR_COMMIT" / "REJECT" |
| R0A | bucket_vector | OLD-bucket-vector | MUTATION_SURVIVED | MUTATION_KILLED | true / false |
| R0A | precision | OLD-precision | MUTATION_SURVIVED | MUTATION_KILLED | "ELIGIBLE_FOR_COMMIT" / "REJECT" |
| R0A | grant_sum | OLD-sum-grants | MUTATION_SURVIVED | MUTATION_KILLED | true / false |
| R0A | reserved | OLD-reserved | MUTATION_KILLED | MUTATION_KILLED | true / false |
| R0A | consumed | OLD-consumed | MUTATION_KILLED | MUTATION_KILLED | true / false |
| R0A | replay_identity | OLD-replay | MUTATION_KILLED | MUTATION_KILLED | "NO_OP" / "CONFLICT" |
| R0A | independent_history | OLD-history | MUTATION_KILLED | MUTATION_KILLED | "RECONCILED" / "REJECT" |
| R0A | confirmed_source | OLD-confirmed-source | MUTATION_SURVIVED | MUTATION_KILLED | "RECONCILED" / "REJECT" |
| R0A | snapshot_freshness | OLD-snapshot | MUTATION_SURVIVED | MUTATION_KILLED | "VERIFIED" / "REJECT" |
| R0A | source_role | OLD-role | MUTATION_SURVIVED | MUTATION_KILLED | "VERIFIED" / "REJECT" |
| R0B | account_namespace | ID-foreign-Account | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | plan | ID-foreign-Plan | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | revision | GUARD-state-revision | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | source_identity | GUARD-state-source | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | allocation_identity | GUARD-state-allocation | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | bucket_vector | GUARD-grant-vector | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["CONFLICT", true, true, true] |
| R0B | precision | GUARD-amount-precision | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | grant_sum | GUARD-sum-grants | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | reserved | GUARD-reserved-other-bucket | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | consumed | GUARD-consumed-other-bucket | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | replay_identity | EVENT-altered-amount | MUTATION_KILLED | MUTATION_KILLED | ["NO_OP", true, true, true] / ["CONFLICT", true, true, true] |
| R0B | independent_history | GUARD-history-missing | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | confirmed_source | GUARD-source-unconfirmed | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |
| R0B | snapshot_freshness | GUARD-snapshot-stale | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["UNAVAILABLE", true, true, true] |
| R0B | source_role | GUARD-source-role | MUTATION_KILLED | MUTATION_KILLED | ["COMMITTED_IN_MEMORY", false, false, false] / ["REJECT", true, true, true] |

## Почему восемь mutations выжили на frozen128

- Account: отсутствовал authorize negative с чужим owner при совпадающих остальных полях.
- Allocation identity: проверялся allocationEvent, но не sourceAllocationID отдельно.
- Bucket vector: проверка общей суммы не испытывалась компенсирующим распределением Remaining между buckets.
- Precision: не было off-minor-unit consumption .005 при USD2.
- Grant sum: не было committed grant40/net50 при согласованном remaining40 и Unallocated0.
- Confirmed source: missing event0 на самом source record не испытывался.
- Freshness: stale context одновременно ломал digest, поэтому removal freshness guard не менял результат старого теста.
- Role: Small record одновременно не соответствовал Core identity; identity guard маскировал отсутствующий role gate.

Новые vectors задают согласованные прочие identity/digest поля и фиксированные expected outcomes из контрактов. Target failure проверяется отдельно: произвольный иной failing test не считается достаточным causal kill. Исходный initial survivor остаётся в JSON и таблице, не переписывается в якобы первоначальный KILLED.

Команда:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0b_mutations.py --output Tests/Evidence/NEXT_STAGE_02B_R0B_MUTATION_RESULTS.json
```

Смена original model/hash или отсутствующий anchor вызывает infrastructure failure. Результаты не основаны на fail-to-compile. Expected критических tests — literal REJECT/CONFLICT/NO_OP и фиксированные суммы50/40/0, а не вывод изменяемого evaluator. Математический источник — proposed D-01/D-07/D-08, а не approval администратора. MQL5/broker mutation evidence NOT_RUN.
