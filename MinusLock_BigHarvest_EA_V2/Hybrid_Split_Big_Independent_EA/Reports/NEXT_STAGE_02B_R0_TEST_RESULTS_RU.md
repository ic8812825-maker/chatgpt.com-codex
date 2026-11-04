# 02B-R0 — воспроизводимые результаты проверок

Базовый и фактически проверенный SHA: `4e7d911002824a4a92e49b54f0f964afcf8cf703`. Ветка: `work`. Время окончательного adversarial запуска UTC: `2026-11-04T01:01:52.225622+00:00`. Проверены именно исходники этого SHA; финальный audit/test-only commit не меняет production blobs. Итог публикации и итоговый SHA фиксируются финальным сообщением после повторной проверки remote, не угадываются в self-referencing commit.

## Итог

- Исполнено 81 native subset экспериментов: 35 совпадений с proposed contracts, 46 расхождений. Часть expectations зависит от ещё не утверждённых D-01/CR-09; расхождения не объявлены 46 самостоятельными утверждёнными defects.
- Независимый Python oracle: 58 проверок, все PASS. Это unit-проверка **предложенных** CR-01/02/03/04/07/08, не production broker proof.
- 13/13 source mutations/sensitivity probes обнаружены: 6 fault injections, 5 диагностических repair probes, 2 проверки чувствительности metric/selector. Original/mutant source paths и SHA-256 сохранены в results JSON.
- `--enforce-contract` завершился **exit 1**, `moneyIntegrity=FAIL`. Это ожидаемый красный нормативный gate на текущем production; инфраструктура завершилась без ошибок. Режим без enforce выдаёт 0 за успешную генерацию evidence, а не за денежную корректность.
- Production изменений нет; 74 production-файла (73 Include + EA), запрещённых trade tokens не найдено; `HSBI_IsBrokerDispatchAllowed` остаётся безусловно false. См. `NEXT_STAGE_02B_R0_GUARD_CHECK.json` и source manifest.

## Основные воспроизводимые actual/expected

| Группа / contract | Положительный контроль | Контрпример | Наблюдение |
|---|---|---|---|
| M-01 / CR-01 | согласованный D1/A1 → ALLOW | foreign D/A/cycle-in-key/allocation event | ALLOW вместо REJECT |
| Replay / CR-07 | exact prior → NO_OP | changed consumer / amount | production consumer → CONFLICT; amount только independent oracle → CONFLICT |
| Restart / CR-08 | полный reference registry | registry неизвестен, hasPrior=false | локальный ALLOW против UNAVAILABLE; durable IO UNPROVEN |
| Spent / CR-01 | available источник | alreadyConsumed=10 | allocated branch REJECT; non-allocated branch ALLOW |
| M-02 / CR-02 | независимый matching expected → ALLOW | 9 foreign identity fields | independent expected REJECT; self-copy ALLOW |
| M-02 / CR-02 | свежий canonical authority fixture | stale/digest/Net/reused allocation | independent oracle REJECT; broker boundary UNPROVEN |
| L-01 / CR-03 | exact record → NO_OP | Profit=55/Commission=-5 → 60/-10, Net=50 | production NO_OP против CONFLICT |
| L-02 / CR-04 | same bucket vector → NO_OP | Reserve50/Partial0 → Reserve0/Partial50 | production NO_OP против CONFLICT |
| E / CR-04/05 | valid finite DTO, допустимый bucket | invalid/revision/negative/Infinity/foreign | результаты по каждому полю в matrix/results; caller obligation UNPROVEN |
| M-05 / CR-10 | Core10 → metric10 | Core0/Trend0/Small10 | точная RHS=10 против разрешённого role contribution 0 |
| BigCore / CR-06 | ratios2/1/.5 → valid | rawCore=.001→0 при Trend=.30, slope=.19 | geometry valid вместо REJECT |
| WORST_CASE / CR-09 | FINAL_LEVEL → L2; incomplete → reject | max loss L1≠minimum margin L2 | выбирается L1; DECISION_REQUIRED |

Точные production-функции, номера строк и объяснение caller layers: `Reports/NEXT_STAGE_02B_R0_FINDINGS_RU.md` и CR-01–10 в `Docs/NEXT_STAGE_02B_R0_CONTRACT_FREEZE_PROPOSAL_RU.md`. Matrix содержит код входных vectors, proposed expected и отдельные runtime gaps; results — actual outcomes.

## Повторный запуск

Рабочий каталог — корень `Hybrid_Split_Big_Independent_EA`. Требуются Python 3.12+ standard library и `g++` с C++17. Тест не требует сети, терминала или credentials и не изменяет production.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 Tests/Static/check_hsbi_02b_r0_ledger_integrity.py --enforce-contract --output Tests/Evidence/NEXT_STAGE_02B_R0_RESULTS.json
```

Сейчас exit 1 обязателен из-за расхождений. Отсутствие compiler, source anchor, compile failure или mutation survivor приводит к infrastructure exception и не считается PASS. Сборка `-O0 -fno-fast-math`; shim использует IEEE doubles и native строки, поэтому не гарантирует полное соответствие MQL5 numeric/runtime semantics. Temporary Include copies и compiler TMPDIR находятся внутри проекта/Tests и удаляются после запуска.

MQL5 harness подготовлен как **test-only исходный шаблон** `Tests/MQL5/HSBI_02B_R0_MoneyContracts.mq5.in`. Для MetaEditor скопировать его в соседний test-only `.mq5` с тем же stem, сохранив relative Includes, затем компилировать/выполнять как script и сохранять полный журнал CHECKS/CONTRACT_FAILURES. Шаблон `.mq5.in` позволяет хранить тест без попадания в исторический coarse scope gate, запрещающий любые новые `.mq5/.mqh`; это не production EA. Исходник содержит реальные assertions с ожидаемыми отказами текущего кода, а не печать константного PASS. Эти действия здесь **не выполнялись**.

## Актуальные regression suites

Все команды ниже запускались без `--publish-evidence`: frozen evidence не переписывались. Новые stdout/stderr logs находятся только в `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/`, summary хранит команды и exit statuses, привязанные к baseline SHA.

| Проверка | Exit | Значение результата |
|---|---:|---|
| `R8` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R8.log` |
| `R8_current` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R8_current.log` |
| `R10` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R10.log` |
| `R10_regressions` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R10_regressions.log` |
| `R12_alignment` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R12_alignment.log` |
| `R12_acceptance` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R12_acceptance.log` |
| `R12A_coverage` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R12A_coverage.log` |
| `R12A_causal` | 0 | 13 causal cases PASS; SOURCE_MUTATIONS=NOT_STARTED, ACCEPTANCE=NOT_GRANTED сохранены; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R12A_causal.log` |
| `R12A_contract` | 0 | LIMITED: standalone canonicalizer напечатал hash empty ledger; не production verifier; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R12A_contract.log` |
| `R7_frozen` | 1 | FAIL frozen metadata/manifest, см. разбор ниже; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R7_frozen.log` |
| `R8_acceptance` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R8_acceptance.log` |
| `R8_properties` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R8_properties.log` |
| `R8_sensitivity` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R8_sensitivity.log` |
| `R10_acceptance` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R10_acceptance.log` |
| `R10_properties` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R10_properties.log` |
| `R10_mutations` | 0 | PASS в Python/static scope; `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R10_mutations.log` |

R8 current: 48/48 regressions; R10: 28 fixtures и 11 lifecycle steps, 67/67 regressions; R12: 14 aligned predicates, second block=15, sensitivity=7/7. Точные property/mutation counts — в соответствующих свежих logs. Зелёные reference suites не закрывают обнаруженные defects денежных production DTO.

## Исторический R7: точный разбор 57/62

Проверялся `Tests/Static/verify_hsb_2d_v1_r7.py --root <project> --skip-seal`; отказ не скрыт.

| ID | Причина текущего отказа | Что изменилось | Что остаётся обязательным |
|---|---|---|---|
| S040B | missing status keys в старом блоке | verifier читает только `HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN/END`; текущие документы имеют последующие status blocks | актуальный запрет торговли и runtime guards; не восстановление старого CURRENT_STAGE |
| S040C | wrong/None historical expected status | verifier требует CURRENT_STAGE=HSB.2D-V1-R7 и старые acceptance values; текущие stages позднее | новые normative decisions проверяются по собственному scope; старый accepted не повышать |
| S044A | семь документов имеют (0,0) старых markers | старые markers заменены последующими каноническими блоками | корректные актуальные markers/согласованность статусов, не frozen marker name |
| S044B | старые maps пусты, parseable=false | следствие прежнего ограниченного parser scope | актуальный status parser в соответствующих R8/R10 acceptance проверках |
| S045 | frozen manifest не равен текущему дереву и hashes семи документов | последующие docs/evidence изменили исторический file set; новые R0 audit files также не входят в frozen set | production hashes текущего baseline и scope новых изменений; frozen manifest не переписывать |

Точки проверки: `verify_hsb_2d_v1_r7.py:55` (`status`), строки 58 (markers), 106–107 (status/manifest checks). Свежий лог содержит точные missing/wrong/extra/hash lists. Никаких подтверждённых функциональных guard-regressions среди этих пяти отказов нет: остальные 57 проверок прошли, включая decision/restart/barrier guard dominance, authorized NO_OP, lexer и adversarial guards. **Это ограниченный вывод**, не доказательство полной функциональной эквивалентности EA.

Отдельно: R4A_R7 и HSB.2D-V1-R7 — разные исторические suites. `Tests/Contracts/HSB_2E_R4_R9_R4A_R7_REGRESSION_MAPPING.json` переносит 48 требований; поздние R8/R10 возвращают identity/replay/current-state binding. R12A normative decisions (commit `0b2a645`) ограничены static qualification Ledger/Batch/Fill, допускают partial fills и не переписывают historical R10/R11/R12 roots. Этот scope не исправляет production Economic/Allocation DTO. Историческое принятие проекта не менялось.

## NOT_RUN и UNPROVEN

| Проверка | Статус | Причина |
|---|---|---|
| MetaEditor main/harness compilation | NOT_RUN | executable отсутствует |
| MQL5 tests | NOT_RUN | MT5 terminal отсутствует |
| Strategy Tester | NOT_RUN | MT5 отсутствует |
| Broker OrderCalcProfit/OrderCalcMargin/account history | NOT_RUN | нет terminal/account/symbol runtime |
| Полный NewFar solver с authoritative provider | NOT_RUN | протестированы только локальная assembly/equality/Catch-Up граница и selector |
| Durable restart/exactly-once/concurrent consumers | UNPROVEN | production persistence stub, нет полного authority pipeline |
| M02 digest/DealNet independent production reconciliation | UNPROVEN | oracle проверен, реальный источник не подключён |
| R12A second-block native source mutations | NOT_RUN / NOT_STARTED | R0 native subset probes не являются R12A implementation acceptance |
| Экономическая конечность восстановления | UNPROVEN | локальная арифметика/geometry не доказывает broker-executable trajectory |

## Итоговые gates

`PYTHON_TESTS=FAIL` для совокупного нормативного gate (известные mismatches + frozen R7), при `REFERENCE_ORACLE=PASS`, `EVIDENCE_EXECUTION=PASS`, актуальных regression suites PASS в указанной области. MQL5_COMPILE/MQL5_TESTS/STRATEGY_TESTER=NOT_RUN. D-01–08 и CR-09 ожидают администратора. Исправление production, broker dispatch и реальная торговля не разрешены.
