# 02B-R0B — фактические проверки

База `9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b`, ветка work. Audit/test-only. Production-код не изменён, исторические records/evidence не переписаны. Все решения ждут администратора.

UTC baseline: 2026-11-04T01:56:44Z. UTC нового oracle: `2026-11-04T02:26:07.329728+00:00`. UTC mutations: `2026-11-04T02:26:23.017732+00:00`. Source hashes и проверяемый SHA привязаны в новых evidence. Итоговый commit не меняет production blobs; его SHA/remote parity фиксируются после публикации.

## Новый независимый oracle

141 PASS, 0 FAIL, exit0. Набор содержит 14 positive identity controls, 14 single-field negatives с zero balance/journal/revision deltas, replay после revision/policy changes, full consumption/spent rejection, source/budget/bucket/finite/precision tests, signed rebates, JPY0/USD2/KWD3 fixtures, single-vs-double rounding, raw64 golden vectors, all required CR-09 cases и восемь geometry profiles. Negative money/loss и insufficient proof depth не становятся positive future proof.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0b_contracts.py --output Tests/Evidence/NEXT_STAGE_02B_R0B_TEST_RESULTS.json
```

Expected outcomes взяты из формальных proposed contracts и literal vectors. История/posted receipts/context — независимые fixtures, не реальные broker confirmations. Decimal/source raw64 — разные слои: raw64 не создаёт posted money. Модель совершает только in-memory test state evolution. CONSERVATION_ONLY/GEOMETRY_ONLY/POSITIVE не означают торговый допуск.

## Mutations

30/30 final KILLED; initial8 survivors раскрыты полностью. Original R0A128 и production не менялись. Семантические causal tests изолируют нужное ограничение; исключения не считаются kills. Подробности: [mutation report](NEXT_STAGE_02B_R0B_MUTATION_RESULTS_RU.md).

## Исторические regressions

Каждый реальный запуск хранит command, UTC start/finish, SHA, exitCode, actual pass/fail counters/scope, stdout/stderr и evidence path в новом REGRESSIONS JSON. Counter0 у canonicalizer означает **ноль assertions**, не пройденные денежные tests. Frozen evidence не публиковались заново.

| Run | Exit | PASS | FAIL | Область/причина |
|---|---:|---:|---:|---|
| R8 | 0 | 48 | 0 | acceptance cases; see raw findings |
| R8_legacy | 0 | 13 | 0 | wrapper checks; historical vector counts in stdout |
| R8_properties | 0 | 4 | 0 | boolean properties |
| R8_sensitivity | 0 | 10 | 0 | runner case counters |
| R10 | 0 | 67 | 0 | acceptance cases; see raw findings |
| R10_verify | 0 | 28 | 0 | fixture cases; lifecycle steps reported separately |
| R10_properties | 0 | 4 | 0 | boolean properties |
| R10_mutations | 0 | 8 | 0 | forward semantic mutations; reverse/harness/probes kept separately in stdout |
| R12 | 0 | 15 | 0 | second block fixtures; R10/sensitivity separate in stdout |
| R12_alignment | 0 | 14 | 0 | predicate alignments; failures are findings |
| R12A | 0 | 13 | 0 | causal checks |
| R12A_coverage | 0 | 22 | 0 | AST coverage rows, not runtime assertions |
| R7_frozen | 1 | 57 | 5 | frozen static checks; Frozen status/manifest expectations |
| 02B_R0 | 1 | 35 | 46 | native proposed-contract comparisons; verify counts below; Known 46 unremediated proposed-contract mismatches |
| 02B_R0A | 0 | 128 | 0 | runner does not publish comparable case counters; not invented |
| R12A_canonicalizer | 0 | 0 | 0 | hash-only computation: zero test assertions |
| 02A | None | None | None | Standalone runner отсутствует: NOT_RUN. Все команды архивного 02A report повторены как R8/R10/R12/R12A/R7; native/broker NOT_RUN. |

R7: 57/62, отказы S040B/S040C/S044A/S044B — historical status markers/values; S045 — frozen manifest против позднего дерева. Исправлений frozen evidence ради PASS нет. R0: native81, reference58, probes13, mismatches46, exit1 — ожидаемый текущий красный нормативный gate. R0A:128PASS. R12A SOURCE_MUTATIONS=NOT_STARTED, SECOND_BLOCK_ACCEPTANCE=NOT_GRANTED сохраняются; new Python mutations не являются R12A native acceptance.

Для 02A отдельного executable suite нет. Не выдуманы exit/pass/fail; доступные команды его archived execution report выполнены. Это не означает, что broker/runtime 02A проверен.

## NOT_RUN / UNPROVEN

MQL5_COMPILE/MQL5_TESTS/STRATEGY_TESTER/BROKER_PRECISION/BROKER_MARGIN=NOT_RUN — MetaEditor/MT5/целевого account runtime нет. DURABLE_RESTART/CAS/concurrency/own-reservation settlement/provider authenticity/NewFar integration=UNPROVEN. Partial-fill arithmetic R0A fixture прошла, реальное partial execution не проверено. Никакой zero-Core/ledger/source production remediation не выполнялась.

## Состав изменений и отсутствие секретов

Только новые Docs/Reports/Tests внутри разрешённого каталога. Полный список и hashes проверяются перед commit. Evidence происходят из synthetic B1/S1/Account1 fixtures и read-only runners; process environment/credential files не читались и не публиковались. Проверка сигнатур секретов и ручная проверка происхождения новых данных фиксируются в финальном verification inventory; универсальная DLP гарантия не заявляется.

## Фактический полный список новых файлов (22)

- `Docs/NEXT_STAGE_02B_R0B_AUTHORITY_AND_REPLAY_CONTRACT_RU.md`
- `Docs/NEXT_STAGE_02B_R0B_CONTRACT_FREEZE_PROPOSAL_RU.md`
- `Docs/NEXT_STAGE_02B_R0B_FINAL_NORMATIVE_REVIEW_RU.md`
- `Docs/NEXT_STAGE_02B_R0B_PRECISION_POLICY_REVIEW_RU.md`
- `Docs/NEXT_STAGE_02B_R1_1_IMPLEMENTATION_SPEC_RU.md`
- `Reports/NEXT_STAGE_02B_R0B_ADMIN_APPROVAL_SHEET_RU.md`
- `Reports/NEXT_STAGE_02B_R0B_DECISIONS_REQUIRED_RU.md`
- `Reports/NEXT_STAGE_02B_R0B_FINAL_VERDICT_RU.md`
- `Reports/NEXT_STAGE_02B_R0B_FINDINGS_RU.md`
- `Reports/NEXT_STAGE_02B_R0B_MUTATION_RESULTS_RU.md`
- `Reports/NEXT_STAGE_02B_R0B_TEST_RESULTS_RU.md`
- `Tests/Contracts/NEXT_STAGE_02B_R0B_VERIFICATION_MATRIX.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0B_BASELINE.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0B_MUTATION_RESULTS.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0B_R0A_RECHECK.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0B_R0_RECHECK.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0B_REGRESSIONS.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0B_TEST_RESULTS.json`
- `Tests/Reference/hsbi_02b_r0b_independent_oracle.py`
- `Tests/Static/check_hsbi_02b_r0b_contracts.py`
- `Tests/Static/check_hsbi_02b_r0b_mutations.py`
- `Tests/Static/run_hsbi_02b_r0b_regressions.py`

Дополнительный no-trade static scan: 74 production-файла, 0 forbidden tokens, exit0; command/UTC/SHA в REGRESSIONS#02A_no_trade_scan. Скан сигнатур секретов новых файлов — 0 совпадений; все account/source данные происходят из synthetic fixtures.
