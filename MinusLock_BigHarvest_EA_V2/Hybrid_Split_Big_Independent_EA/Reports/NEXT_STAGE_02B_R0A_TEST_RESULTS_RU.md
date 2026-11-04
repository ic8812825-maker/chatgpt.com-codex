# 02B-R0A — фактические результаты тестов и проверок

База `cb5e55cb38aa4f2eb5b58e5218462c6738f3097a`, ветка work; исходный remote равен local, дерево чистое. UTC baseline: `2026-11-04T01:18:36Z`. UTC повторного R0 runner: `2026-11-04T01:19:41.802030+00:00`. UTC нового Decimal набора: `2026-11-04T01:37:51.352241+00:00`. Полный baseline inventory/hashes/tools: `Tests/Evidence/NEXT_STAGE_02B_R0A_VERIFICATION_SUMMARY.json`.

## Четыре независимых статуса

```text
TEST_INFRASTRUCTURE_STATUS=PASS
REFERENCE_ORACLE_STATUS=PASS_TESTED_VECTORS_WITH_COVERAGE_LIMITS
PRODUCTION_CONTRACT_STATUS=FAIL
RUNTIME_VERIFICATION_STATUS=NOT_RUN
```

PASS инфраструктуры означает завершение заданных экспериментов без parser/compile/hash/mutation-survivor ошибок, не правильность production денег. 46 mismatches сохранены; неподписанные proposed contracts не становятся действующей экономикой.

## Повторный запуск неизменённого R0 runner

```bash
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0_ledger_integrity.py --enforce-contract --output Tests/Evidence/NEXT_STAGE_02B_R0A_RECHECK.json
```

Факт: native81, reference58, mutation13, mismatches46, exit1. Контрольные значения воспроизведены без изменения кода/expected. Историческое поле baseSha=4e7d911… в runner сохранено; testedHead=cb5e55c… фиксирует фактический baseline R0A. Старый results JSON и все historical evidence неизменны.

## Новые исполнимые proposed-contract tests

```bash
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0a_normative_contracts.py --output Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json
```

128 PASS, 0 FAIL, exit0. Expected outcomes не импортируются из production evaluator. Проверяются Decimal суммы/precision/residual, negative/zero net, typed conversion, role Small/opening filter, absolute/incremental/BidAsk/partial-close baseline, actual transition overcap/partial fills, buffer overlap, replay/full spend/reservations, owner namespace, source/proof/digest/net, all-level worst criterion/tie/missing/zero/negative и zero-Core. No-trade проверен отдельным source-sensitive execution неизменённой policy в пяти режимах; безусловный return false покрывает остальные режимы по исходнику.

Точные test IDs, input assertions/actual/expected и нормативный статус PROPOSED_CONTRACT — в новом PROPOSED_TESTS JSON и runner. Контракты и mapping инвариантов — [machine matrix](../Tests/Contracts/NEXT_STAGE_02B_R0A_NORMATIVE_MATRIX.json) и [регистр инвариантов](../Docs/NEXT_STAGE_02B_R0A_MONEY_INVARIANTS_RU.md).

## Проверка независимости: пределы

| Вид доказательства | Что проверено | Чего не доказывает |
|---|---|---|
| R0 static expected против extracted production actual | 81 пар actual/expected; helpers/formula/assembly | Полный NewFar solver/terminal execution |
| 6 source fault mutations | raw source hash изменён, extraction соответствует, outcome меняется на нормативно неправильный | Полное покрытие всех дефектов/всех mutants |
| 5 repair sensitivity | конкретный контрпример меняет результат после локального probe | Исправленную production или complete remediation |
| 2 metric/selector probes | Small term/выбранный уровень влияют на результат | Утверждённый D-03/CR-09 или настоящую min-margin реализацию |
| R0 reference58 | исполненные unit fixtures проходят | Полный authority/precision schema validator |
| Новый Decimal oracle | 128 semantic checks предложенной модели | Реальную broker authenticity, currency conversion и durable IO |
| Source hashes/no-trade | 74 production-файла неизменны; guard возвращает false | MetaEditor/MQL5 runtime acceptance |

Выявленный предел legacy oracle: `oracle_consumption` при plan=999/revision=999 возвращает ALLOW; это отдельный `ORACLE_COVERAGE_GAP`, а не скрытый PASS. Новый proposed authorization эти изменения отвергает. Исторический oracle не переписывался. `detected=true` у R0 означает изменение поведения, а не универсальный mutation score; различие категорий сохранено. Infrastructure exception не считается пойманной mutation.

Новый helper reconciled_net моделирует только eligible closing-source path Reserve. Opening commissions/fees не исчезают: general economic accounting должен сохранить их отдельно; отсутствие harvest grant не запрещает economic record. Source fixtures complete/fresh обозначают предпосылки теста, не фиктивное подключение брокера. USD/2-digit и linear unit-price fixtures ограничивают числовую область теста; полный schema/authority caller integration остаётся UNPROVEN.

## Свежие regressions

Запуски без --publish-evidence, stdout/stderr/commands/exit сохраняются только в новом `NEXT_STAGE_02B_R0A_REGRESSIONS.json`.

| Набор | Exit | Область результата |
|---|---:|---|
| R8_legacy | 0 | PASS Python/static scope |
| R8_acceptance | 0 | PASS Python/static scope |
| R8_properties | 0 | PASS Python/static scope |
| R8_sensitivity | 0 | PASS Python/static scope |
| R10 | 0 | PASS Python/static scope |
| R10_acceptance | 0 | PASS Python/static scope |
| R10_properties | 0 | PASS Python/static scope |
| R10_mutations | 0 | PASS Python/static scope |
| R12_alignment | 0 | PASS Python/static scope |
| R12_acceptance | 0 | PASS Python/static scope |
| R12A_coverage | 0 | PASS Python/static scope |
| R12A_causal | 0 | PASS causal fixtures; SOURCE_MUTATIONS=NOT_STARTED, ACCEPTANCE=NOT_GRANTED сохранены |
| R12A_canonicalizer | 0 | LIMITED: hash empty ledger; не production money verifier |
| R7_frozen | 1 | FAIL: 57/62; historical status/manifest mismatch, не скрыт |

R8 acceptance 48/48, R10 acceptance 67/67, R12 second-block15 и sensitivity7/7, R12A causal13. R7: S040B/S040C/S044A/S044B требуют frozen canonical status markers/values, которых нет в поздних документах; S045 сравнивает исторический manifest с текущим деревом. Остальные 57 guards/static checks проходят. Frozen artifacts не менялись; функциональная регрессия из этих пяти отказов не установлена. Это не доказательство полной эквивалентности EA. Разбор точных ID/source: R0 test report и новые stdout logs.

## NOT_RUN / UNPROVEN

- MQL5_COMPILE=NOT_RUN; MQL5_TESTS=NOT_RUN: MetaEditor/MT5 недоступны. Из существующего .mq5.in не создавался якобы проверенный .mq5; компилируемость template не заявляется.
- STRATEGY_TESTER=NOT_RUN; broker money/margin/history/account modes=NOT_RUN.
- Durable commit/replay/CAS/concurrency/crash recovery=UNPROVEN: in-memory apply не является файловым backend.
- Полная NewFar money authorization, mandatory caller chain и broker-reachable future trajectory=UNPROVEN/NOT_RUN.
- Административные D-01–08/CR-09=AWAITING; zero-Core не исправлен, geometry scope отдельно.

## Scope и публикация

Только новые audit/test-only документы, JSON, reference и runner в разрешённом каталоге. Старые R0 29 файлов и 74 production hashes сверены; изменённых historical artifacts нет. Source/guard manifest и log hashes входят в verification summary. Публикация выполняется одним новым commit после diff и повторной remote parity проверки; конечный SHA фиксируется финальным сообщением, а не угадывается внутри self-referencing commit. Исходный нормативный gate остаётся FAIL; утверждение и R1 запрещены до решения администратора.

## Полный список новых файлов R0A (15)

- `Docs/NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md`
- `Docs/NEXT_STAGE_02B_R0A_MONEY_INVARIANTS_RU.md`
- `Docs/NEXT_STAGE_02B_R0A_NORMATIVE_REVIEW_RU.md`
- `Docs/NEXT_STAGE_02B_R1_PHASED_IMPLEMENTATION_PLAN_RU.md`
- `Reports/NEXT_STAGE_02B_R0A_ADMIN_APPROVAL_SHEET_RU.md`
- `Reports/NEXT_STAGE_02B_R0A_CONFLICTS_AND_BLOCKERS_RU.md`
- `Reports/NEXT_STAGE_02B_R0A_DECISION_RECOMMENDATIONS_RU.md`
- `Reports/NEXT_STAGE_02B_R0A_TEST_RESULTS_RU.md`
- `Tests/Contracts/NEXT_STAGE_02B_R0A_NORMATIVE_MATRIX.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0A_RECHECK.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0A_REGRESSIONS.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0A_VERIFICATION_SUMMARY.json`
- `Tests/Reference/hsbi_02b_r0a_normative_model.py`
- `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`
