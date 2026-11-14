# R4 — GitHub publication checkpoint и сохранение R1/R2/R3

## R4_START_BASELINE

Это промежуточный audit-only snapshot. AUDIT_COMPLETENESS=PARTIAL. Дата UTC: 2026-11-14T11:11:27.635800+00:00.

Repository: `ic8812825-maker/chatgpt.com-codex`; target `work`; planned audit branch `audit/hsbi-audit03-github-closure-r4`. BASE_SHA=`b4d8f1ea5caf492f3abd030e5502d40582c52dc8`.

`git ls-remote origin refs/heads/work refs/heads/audit/hsbi-audit03-github-closure-r4` подтвердил work на базе; audit ref отсутствовал. Локальные HEAD/origin/work совпадали. Рабочее дерево содержало 15 разрешённых modified/untracked AUDIT03 reports. Эти материалы сохранены, reset/clean/rebase/stash/force не использовались.

## Проверка настоящего GitHub

- Remote URL: `https://github.com/ic8812825-maker/chatgpt.com-codex.git` (fetch/push).
- `https://github.com/ic8812825-maker/chatgpt.com-codex`: HTTP 200.
- `https://github.com/ic8812825-maker/chatgpt.com-codex/tree/work/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA`: HTTP 200.
- `git push --dry-run origin HEAD:refs/heads/audit/hsbi-audit03-github-closure-r4`: exit 0, `[new branch]`. Это dry-run, не публикация и не достаточное доказательство фактического права записи.
- `gh api repos/ic8812825-maker/chatgpt.com-codex`, `/branches/work`, `/contents/...?...ref=work`, `/branches/work/protection`, `/rules/branches/work`, `/pulls?state=open&base=work`: exit 1, `Forbidden`.
- Независимое уточнение: curl к API — exit 56, `CONNECT tunnel failed, response 403`, `API_HTTP=000`. Ответ GitHub API не получен; это сетевой proxy отказ, а не установленный GitHub repository permission denial.
- Managed environment status: enforced restricted network; github.com/raw.githubusercontent.com доступны по allowlist, api.github.com отсутствует; диагностическая история not_found. Конфигурация сети и GitHub settings не менялись.
- Branch protection, PR requirements, existing PR, Actions и Code Scanning: NOT_VERIFIED из-за недоступного API. Bypass не использовался. Обычный push в отдельную audit-ветку допускается только со штатным серверным принятием; work не изменяется и PR не сливается.

## Фактическое сохранённое покрытие

Исходный denominator 485 сохранён. Обнаружены ещё 46 применимых JSON документов в Tests/Static, пропущенных прежней инвентаризацией; итог 531, без искусственного уменьшения denominator.

- FULL: 463
- NOT_REVIEWED: 63
- EXACT_DUPLICATE_REVIEW_REUSED: 5

199 уникальных Function ID; 66 существующих карточек с 15 полями; 73 индивидуальных GRD001–073. Это текущий состав карточек, не завершённый census обязательных guards. Старые16 групп и10 transaction rows не прибавляются к73 как независимые atomic clauses. Финансовый mandatory caller total ещё не установлен; локальные pure helper edges не считаются финансовым commit.

51 ERR, 23 IMP; severity P0=14/P1=32/P2=5/P3=0. Все16 прежних административных решений остаются AWAITING_ADMIN_APPROVAL; утверждено0. ERR051=CONDITIONAL_STATIC_RISK: binary64 countermodel возможен в широком caller DTO domain, но broker-domain достижимость/native зависание не воспроизводились. История исходной более сильной оценки сохранена в центральном реестре.

FSM содержит9 ранее разобранных rule families и10 конкретных specification gaps R3-FSM-SG01..10. 140 topology pairs не event/financial handlers. Normative full relation не имеет единого однозначного домена событий/phase/restart: total=UNDEFINED_BY_NORMATIVE_DOMAIN с источниками в FSM_COMPLETE_MATRIX. Реализованных финансовых handlers в main0; pure validators существуют отдельно.

Global money conservation, global loss bound, cycle termination, guaranteed profitability: NO_PROOF. Production не исправлялся. Тесты, MetaEditor, Strategy Tester и native MQL не запускались.

## Preservation перед snapshot

Статическое сравнение всех1515 read-only baseline файлов с Git tree: recomputed Git blob SHA1 от filesystem bytes и file modes совпали, mismatches0. Все74 production sources входят в это множество. Historical evidence/contracts/tests сохранены. 13 baseline AUDIT03 Markdown имеют разрешённую изменяемую область; новые отчёты также только в Reports/HSBI_AUDIT03_*.md.

## Остаток обязательного чтения — точные пути

- `Reports/HSBI_FULL_SYSTEM_AUDIT_01_CODE_REVIEW_RU.md`
- `Reports/HSBI_FULL_SYSTEM_AUDIT_01_DEFECT_REGISTER_RU.md`
- `Reports/HSBI_FULL_SYSTEM_AUDIT_01_DOCUMENTATION_MAP_RU.md`
- `Reports/HSBI_FULL_SYSTEM_AUDIT_01_FINAL_VERDICT_RU.md`
- `Reports/HSBI_FULL_SYSTEM_AUDIT_01_PROJECT_INVENTORY_RU.md`
- `Reports/NEXT_STAGE_02B_R0A_CONFLICTS_AND_BLOCKERS_RU.md`
- `Reports/NEXT_STAGE_02B_R0A_DECISION_RECOMMENDATIONS_RU.md`
- `Reports/NEXT_STAGE_02B_R0A_TEST_RESULTS_RU.md`
- `Reports/NEXT_STAGE_02B_R0B_MUTATION_RESULTS_RU.md`
- `Reports/NEXT_STAGE_02B_R0B_TEST_RESULTS_RU.md`
- `Reports/NEXT_STAGE_02B_R0C_TEST_AND_MUTATION_RESULTS_RU.md`
- `Reports/NEXT_STAGE_02B_R0D_TEST_AND_MUTATION_RESULTS_RU.md`
- `Reports/NEXT_STAGE_02B_R0E_C1_TEST_AND_MUTATION_RESULTS_RU.md`
- `Reports/NEXT_STAGE_02B_R0E_CONFLICT_REGISTER_RU.md`
- `Reports/NEXT_STAGE_02B_R0E_TEST_RESULTS_RU.md`
- `Reports/NEXT_STAGE_02B_R0_DECISIONS_REQUIRED_RU.md`
- `Reports/NEXT_STAGE_02B_R0_FINDINGS_RU.md`
- `Reports/NEXT_STAGE_02B_R0_TEST_RESULTS_RU.md`
- `Tests/Contracts/HSBI_DG01_DECISION_MATRIX.json`
- `Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_01_STATE_MATRIX.json`
- `Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_02_DECISION_MATRIX.json`
- `Tests/Contracts/HSB_2E_R4_R6_MIGRATION_MAP.json`
- `Tests/Contracts/HSB_2E_R4_R7_SEMANTIC_ORACLE.json`
- `Tests/Contracts/HSB_2E_R4_R8_MUTATION_CATALOG.json`
- `Tests/Contracts/HSB_2E_R4_R8_SEMANTIC_ORACLE.json`
- `Tests/Contracts/HSB_2E_R4_R9_R2_HISTORICAL_COMPATIBILITY_ORACLE.json`
- `Tests/Contracts/HSB_2E_R4_R9_R2_HISTORICAL_PROVABILITY_MATRIX.json`
- `Tests/Contracts/HSB_2E_R4_R9_R3_CAUSAL_PAIRS.json`
- `Tests/Contracts/HSB_2E_R4_R9_R3_NATIVE_ECONOMIC_ORACLE_V2.json`
- `Tests/Contracts/HSB_2E_R4_R9_R4A_R10_CASE_CONTRACT.json`
- `Tests/Contracts/HSB_2E_R4_R9_R4A_R8_REQUIRED_CASES.json`
- `Tests/Contracts/HSB_2E_R4_R9_R4A_R9_CASE_CONTRACT.json`
- `Tests/Contracts/NEXT_STAGE_02B_R0B_VERIFICATION_MATRIX.json`
- `Tests/Contracts/NEXT_STAGE_02B_R0C_VERIFICATION_MATRIX.json`
- `Tests/Contracts/NEXT_STAGE_02B_R0D_VERIFICATION_MATRIX.json`
- `Tests/Contracts/NEXT_STAGE_02B_R0E_C1_REQUIRED_CATALOG.json`
- `Tests/Contracts/NEXT_STAGE_02B_R0E_C1_VERIFICATION_MATRIX.json`
- `Tests/Contracts/NEXT_STAGE_02B_R0E_REQUIREMENT_MATRIX.json`
- `Tests/Contracts/NEXT_STAGE_02B_R0_ADVERSARIAL_MATRIX.json`
- `Tests/Static/hsb_2d_v1_include_graph.json`
- `Tests/Static/hsb_2e_api_contracts.json`
- `Tests/Static/hsb_2e_api_contracts_r2.json`
- `Tests/Static/hsb_2e_api_contracts_r3.json`
- `Tests/Static/hsb_2e_fixtures.json`
- `Tests/Static/hsb_2e_fixtures_r2.json`
- `Tests/Static/hsb_2e_formula_contracts_r2.json`
- `Tests/Static/hsb_2e_formula_contracts_r3.json`
- `Tests/Static/hsb_2e_normative_source_map_r3.json`
- `Tests/Static/hsb_2e_prep_r3_mutations.json`
- `Tests/Static/hsb_2e_prep_r4_mutations.json`
- `Tests/Static/hsb_2e_prep_r4_r1_mutations.json`
- `Tests/Static/hsb_2e_prep_r4_r2_mutations.json`
- `Tests/Static/hsb_2e_prep_r4_r3_mutations.json`
- `Tests/Static/hsb_2e_prep_r4_r4_mutations.json`
- `Tests/Static/hsb_2e_production_file_map.json`
- `Tests/Static/hsb_2e_r4_r6_source_mutations.json`
- `Tests/Static/hsb_2e_scenario_contracts_r2.json`
- `Tests/Static/hsb_2e_scenario_contracts_r3.json`
- `Tests/Static/hsb_2e_test_plan.json`
- `Tests/Static/hsb_2e_test_plan_r2.json`
- `Tests/Static/hsb_2e_test_plan_r3.json`
- `Tests/Static/hsb_2e_test_plan_r4.json`
- `Tests/Static/hsb_2e_test_plan_r4_r1.json`

## Предсуществующие неопубликованные отчёты — SHA256 на старте R4

| Path | Bytes | SHA256 |
|---|---:|---|
| `Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md` | 174061 | `f859ee8de1797659de3feaa0ae92ed331d785f747ee22e7de34eec54ed37e24c` |
| `Reports/HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md` | 89105 | `8eb68750ff697dc8e6875733c0b44b0c883f32d8ff2d9a544801ef04af0d5ed6` |
| `Reports/HSBI_AUDIT03_BASELINE_AND_PRESERVATION_RU.md` | 868260 | `f854c0374f058de49c94f6724c3e2f246460187876b7ed083cc8835bb7fde97f` |
| `Reports/HSBI_AUDIT03_COMPLETENESS_MATRIX_RU.md` | 33929 | `b1b90eccaf40d4e28cad939c572fc9ccb42aee1fbae79974dda2f6cbed3584ba` |
| `Reports/HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md` | 626515 | `5c1f59c8a35998c2497f475b205a67d37ff2c3baaa206065234bae97cc0f7987` |
| `Reports/HSBI_AUDIT03_FINAL_VERDICT_RU.md` | 47802 | `05add6af7764b1d18b2e33df28b7867c0dc14b1cfb4308d8a84d1c8cf49132e6` |
| `Reports/HSBI_AUDIT03_FORMULA_CATALOG_RU.md` | 250806 | `b670067c518c8fcf72eb0590f25acb65ce8ffc6953e477f601bb2d4d0c6e1db1` |
| `Reports/HSBI_AUDIT03_FSM_REVIEW_RU.md` | 16040 | `1e4d710844d530d4d68403e2b736e8c30ddb9e3790dc699b28076c2ccd2f96c0` |
| `Reports/HSBI_AUDIT03_GLOBAL_PROPERTIES_RU.md` | 20535 | `ebb84a9cb13911ff5969674d2306cc01c8544c096322817f6456d9a5a2aa8263` |
| `Reports/HSBI_AUDIT03_SOURCE_FUNCTION_MAP_RU.md` | 603065 | `7bf561cda9bbb5e0ddd4b26e64b1f655943483ef75f932ab4207d649e0c89848` |
| `Reports/HSBI_AUDIT03_FINAL_CLOSURE_READING_LOG_RU.md` | 179641 | `6404d22c8d19131714bdb00eef53c022eb261756ca69198ea2772b04f093242c` |
| `Reports/HSBI_AUDIT03_FSM_COMPLETE_MATRIX_RU.md` | 35977 | `9789abfcb1b1912bf50cd68f22e773c875322a19d99f68787ccff7b2b1e62c0a` |
| `Reports/HSBI_AUDIT03_GUARD_CALLER_CROSSWALK_RU.md` | 265420 | `0b9343ac172ffcdbe02b8dd951ba5c4987e208364cb4c69d4410f106b9b309f1` |
| `Reports/HSBI_AUDIT03_R2_WORK_IN_PROGRESS_RU.md` | 55934 | `d4711084f1b155dfced106d033719238b5eaccf632e22c2a50642495acb3c81c` |
| `Reports/HSBI_AUDIT03_R3_STATIC_READING_METHOD_RU.md` | 307131 | `91c913fe26f5fbce9191855f2c2385274dda64f16e9c8f3974ac05423406f05d` |

## Граница публикации

На момент создания этой записи фактический commit/push ещё не выполнен. SHA/compare/PR нельзя заранее объявить созданными. После обычного push требуется отдельно проверить удалённый ref, содержимое и GitHub API. До API-проверки GITHUB_PUBLICATION_COMPLETE не получает YES. Git branch publication и TARGET_WORK_INTEGRATED — разные факты; merge в work требует отдельного одобрения владельца.

TESTS_EXECUTED_BY_CODEX=NO
MQL5_COMPILE=NOT_RUN
MQL5_NATIVE_TESTS=NOT_RUN
ADMIN_APPROVAL_COMPLETE=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
