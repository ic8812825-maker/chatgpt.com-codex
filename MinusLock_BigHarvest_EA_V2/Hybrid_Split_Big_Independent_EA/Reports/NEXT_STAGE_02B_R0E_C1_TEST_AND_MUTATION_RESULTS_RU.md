# 02B-R0E-C1 — результаты tests/mutations/package/regressions

BASE_SHA=074165b38f1b6d6253a9629c7d2def988e8e286a

PROPOSED / AWAITING_ADMIN_APPROVAL. Audit/test-only; production/trading/dispatch запрещены.

Reference: 105 различных сценариев × 8 contexts = 840 executions; PASS=840, FAIL=0, INFRA=0. Comparisons=1680 — два top-level comparison на execution, не количество независимых сценариев. Context0 Input.Calls содержит фактические аргументы заявленного public operation; остальные contexts ссылаются на этот fixture. SubjectCalls захватывает реально вызванные операции.

Mutation catalog=55; killed=54, redundant survivors=1, unexplained=0, infra=0. Unsafe acceptance и status-only kills хранятся раздельно. Исходные R0E13 и три initial survivors сохранены в REPRODUCTION, не переименованы в новый каталог.

## Объяснённый survivor

C1-MUT-outer-poststate удаляет повторную внешнюю проверку balance. До delta обязательная _reconcile_store реконструирует все строки по independent journal; private delta проверяет выбранную строку до и после exact debit, все остальные строки неизменны. Public apply проверяет status private delta. Поэтому при допустимом входе условие повторной проверки не может стать false: G=C+V+F, x<=F ⇒G=(C+x)+V+(F-x). Мутация не меняет семантику в этом domain. Весь suite мутанта проходит; отрицательный тест allocation corruption по-прежнему отклоняется обязательным ранним слоем. Не создавалось искусственного обхода private validator ради kill. Это survivor, а не PASS/killed.

## Первоначальные ошибки раскрыты

DEVELOPMENT.json хранит initial contract run:4FAIL/12INFRA из-за ambient Decimal addition в независимом fixture receipt builder; заменено integer minor arithmetic. Malformed nested source record в prototype вызывал TypeError; malformed external journal ранее возвращал UNAVAILABLE; добавлены shape validation и causal semantic mutations без засчитывания runtime errors как kills. Прототип C1 также принимал historical receipt с Magic999 при history Magic7: добавлены historical source/allocation/evaluationContext bindings и три causal probes/mutations. Первый regression runner временно хранил baseline archives перед recursive R7 scan, получил S009 guards219/unique73 и56/6; archive materialization перенесена после recursive suites, frozen test не менялся. Draft source metadata не считается final execution evidence.

## Package

Текущее сохранённое выполнение: Positive=PASS; negativePassed=46; negativeFailed=0. Обязательный каталог содержит 46 package probes:23 прежних класса отдельно и 23 C1 extensions. Hashes disposable artifacts обновляются для semantic isolation; реальные historical bytes/modes не меняются. Required test/guard/mutation inventory вычисляется из executable specifications и их source pins, не из проверяемого evidence. Пустой mutation catalog, coherent deletion теста, дубликаты/unknown IDs, conflicting statuses, wrong section/case, regression hashes и неверные source mappings обязаны отклоняться.

## Регрессии

| Suite | Exit | PASS | FAIL | BaselineMatch | Classification |
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
| R0E_reference | 0 | 728 | 0 | True | PASS |
| R0E_package_baseline | 0 | None | None | True | PASS |
| R0E_mutations | 0 | 13 | 0 | True | PASS |

Исторические FAIL R7/R0 не скрыты. R7 S040B/S040C/S044A/S044B — старые status/markers; S045 — frozen manifest. Обязательными остаются действующие runtime/no-trade guards и baseline preservation, не возврат исторических status labels. C1 не изменяет production, поэтому подтверждённой новой функциональной регрессии при baseline match нет. 02A standalone suite отсутствует; executable report commands покрыты named runs. R0E_mutations — ссылка на реальное reproduction execution, не отдельный фиктивный CLI запуск, который мог бы перезаписать historical JSON.

Команды: check_hsbi_02b_r0e_c1_reproduction.py; check_hsbi_02b_r0e_c1_contracts.py; check_hsbi_02b_r0e_c1_mutations.py; run_hsbi_02b_r0e_c1_regressions.py; build_hsbi_02b_r0e_c1_catalog.py; check_hsbi_02b_r0e_c1_package.py --seal --self-test. Повторный default package run read-only. build_hsbi_02b_r0e_c1_reports.py генерирует только новые отчёты из фактических JSON. Unknown/outside-domain не преобразуется в PASS.

MQL5_COMPILE/MQL5_TESTS/STRATEGY_TESTER=NOT_RUN; MetaEditor/terminal64/Wine availability сохранена в preservation. C++ extraction не MQL5 runtime. Broker authenticity/precision/margin, real partial fills, global funding/debit attribution, durable/concurrent enforcement и full NewFar остаются UNPROVEN. Флаги complete/fresh — fixture provider assumptions, не broker receipts. Ни одна таблица не разрешает trading или implementation.
