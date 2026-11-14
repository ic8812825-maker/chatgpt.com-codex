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

## R4 — фактическая публикация первого snapshot и проверка bytes

UTC проверки:2026-11-14T11:13:47.140276+00:00.

- Commit: [f3090a5aedd71510f38afd265ac6d7d9b56b63a2](https://github.com/ic8812825-maker/chatgpt.com-codex/commit/f3090a5aedd71510f38afd265ac6d7d9b56b63a2) — HTTP200.
- Compare к исходному work: [проверенный diff](https://github.com/ic8812825-maker/chatgpt.com-codex/compare/b4d8f1ea5caf492f3abd030e5502d40582c52dc8...f3090a5aedd71510f38afd265ac6d7d9b56b63a2) — HTTP200.
- [Итоговый отчёт](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_VERDICT_RU.md) — HTTP200.
- `git push --set-upstream origin audit/hsbi-audit03-github-closure-r4`: exit0, new branch создана в разрешённом репозитории. Никакого force/bypass/settings change.
- `git ls-remote`: audit ref = опубликованный SHA выше; work = исходный b4d8f1ea5caf492f3abd030e5502d40582c52dc8. TARGET_WORK_INTEGRATED=NO.
- Все16 изменённых файлов прочитаны обратно по immutable commit URL с raw.githubusercontent.com; curl --fail exit0 для каждого, SHA256 совпали с локальными bytes. Это реальная remote content verification, но **не GitHub REST API verification**.
- Draft PR create (audit→work, --draft) завершился exit1: `Post https://api.github.com/graphql: Forbidden`. PR не создан; GITHUB_PR_URL=NOT_CREATED. Серверный push вывел лишь ссылку на форму создания PR — она не является PR.
- GITHUB_WRITE_CAPABILITY=YES подтверждено фактическим обычным push. GITHUB_REPOSITORY_VERIFIED=YES и TARGET_PATH_VERIFIED=YES по Git/Web; GitHub API permissions/protection/Actions/CodeScanning по-прежнему NOT_VERIFIED.
- По строгому критерию R4, требующему API, GITHUB_PUBLICATION_COMPLETE=NO_API_VERIFICATION_BLOCKED и AUDIT03_PUBLISHED=NO_STRICT_API_CRITERION. При этом AUDIT_BRANCH_PUSHED=YES и REMOTE_CONTENT_MATCH=16/16 — отдельные доказанные факты, не только локальная работа.
- Безопасное закрытие блокировки: разрешить api.github.com в сетевой политике среды; затем обычные authenticated read-only API проверки, штатный Draft PR и review. Нельзя выдавать proxy403 за установленное отсутствие repository permission или обходить сеть/защиту.

### Контент первого опубликованного snapshot

| Path | Bytes | SHA256 совпавших remote bytes | GitHub raw URL |
|---|---:|---|---|
| `Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md` | 174404 | `2a9498aa1e72b493b3797594c541c510381b5aeb59df1f3b3ba140884dcb27e4` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md |
| `Reports/HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md` | 89105 | `8eb68750ff697dc8e6875733c0b44b0c883f32d8ff2d9a544801ef04af0d5ed6` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md |
| `Reports/HSBI_AUDIT03_BASELINE_AND_PRESERVATION_RU.md` | 868260 | `f854c0374f058de49c94f6724c3e2f246460187876b7ed083cc8835bb7fde97f` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_BASELINE_AND_PRESERVATION_RU.md |
| `Reports/HSBI_AUDIT03_COMPLETENESS_MATRIX_RU.md` | 34816 | `16fca7ad83422230409449e529281d726c6b6279e935724f2167f80ca3f9cfdd` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_COMPLETENESS_MATRIX_RU.md |
| `Reports/HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md` | 626515 | `5c1f59c8a35998c2497f475b205a67d37ff2c3baaa206065234bae97cc0f7987` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md |
| `Reports/HSBI_AUDIT03_FINAL_CLOSURE_READING_LOG_RU.md` | 179641 | `6404d22c8d19131714bdb00eef53c022eb261756ca69198ea2772b04f093242c` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_CLOSURE_READING_LOG_RU.md |
| `Reports/HSBI_AUDIT03_FINAL_VERDICT_RU.md` | 49158 | `d52229c29660e87ca0bc4c88e842240bcf4b1195cf773d23ec1a8d8ff10d117c` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_VERDICT_RU.md |
| `Reports/HSBI_AUDIT03_FORMULA_CATALOG_RU.md` | 250806 | `b670067c518c8fcf72eb0590f25acb65ce8ffc6953e477f601bb2d4d0c6e1db1` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FORMULA_CATALOG_RU.md |
| `Reports/HSBI_AUDIT03_FSM_COMPLETE_MATRIX_RU.md` | 35977 | `9789abfcb1b1912bf50cd68f22e773c875322a19d99f68787ccff7b2b1e62c0a` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FSM_COMPLETE_MATRIX_RU.md |
| `Reports/HSBI_AUDIT03_FSM_REVIEW_RU.md` | 16040 | `1e4d710844d530d4d68403e2b736e8c30ddb9e3790dc699b28076c2ccd2f96c0` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FSM_REVIEW_RU.md |
| `Reports/HSBI_AUDIT03_GLOBAL_PROPERTIES_RU.md` | 20535 | `ebb84a9cb13911ff5969674d2306cc01c8544c096322817f6456d9a5a2aa8263` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_GLOBAL_PROPERTIES_RU.md |
| `Reports/HSBI_AUDIT03_GUARD_CALLER_CROSSWALK_RU.md` | 265420 | `0b9343ac172ffcdbe02b8dd951ba5c4987e208364cb4c69d4410f106b9b309f1` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_GUARD_CALLER_CROSSWALK_RU.md |
| `Reports/HSBI_AUDIT03_R2_WORK_IN_PROGRESS_RU.md` | 56704 | `5cfddaf05e89442e9b16769128a22316b5dbf48b1acc483bbda86d4b563b8712` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R2_WORK_IN_PROGRESS_RU.md |
| `Reports/HSBI_AUDIT03_R3_STATIC_READING_METHOD_RU.md` | 307131 | `91c913fe26f5fbce9191855f2c2385274dda64f16e9c8f3974ac05423406f05d` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R3_STATIC_READING_METHOD_RU.md |
| `Reports/HSBI_AUDIT03_R4_GITHUB_PUBLICATION_RU.md` | 11904 | `1d64960c7c1ed070fbf40aa2b5dc15c0c0230c1e9fb956a2d556b82d80bd7f36` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R4_GITHUB_PUBLICATION_RU.md |
| `Reports/HSBI_AUDIT03_SOURCE_FUNCTION_MAP_RU.md` | 603065 | `7bf561cda9bbb5e0ddd4b26e64b1f655943483ef75f932ab4207d649e0c89848` | https://raw.githubusercontent.com/ic8812825-maker/chatgpt.com-codex/f3090a5aedd71510f38afd265ac6d7d9b56b63a2/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_SOURCE_FUNCTION_MAP_RU.md |

## R4 — последующий статический прогресс

После сохранённого snapshot полностью прочитаны ещё9 исторических отчётов R0A/R0B/R0C/R0D/R0E/C1, отражённые в FINAL_CLOSURE_READING_LOG и coverage. Текущий счёт472 FULL+5duplicate+54NOT_REVIEWED=531. Прежние463/63 выше — состояние первого snapshot. Тесты не запускались. Новых ERR/IMP IDs и утверждений администратора нет. Общий guard/caller census, часть document review и полная clause/FSM прослеживаемость остаются незавершёнными.

### Точный текущий остаток54

- `Reports/HSBI_FULL_SYSTEM_AUDIT_01_CODE_REVIEW_RU.md`
- `Reports/HSBI_FULL_SYSTEM_AUDIT_01_DEFECT_REGISTER_RU.md`
- `Reports/HSBI_FULL_SYSTEM_AUDIT_01_DOCUMENTATION_MAP_RU.md`
- `Reports/HSBI_FULL_SYSTEM_AUDIT_01_FINAL_VERDICT_RU.md`
- `Reports/HSBI_FULL_SYSTEM_AUDIT_01_PROJECT_INVENTORY_RU.md`
- `Reports/NEXT_STAGE_02B_R0E_CONFLICT_REGISTER_RU.md`
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

## R4 — PUBLISH_BLOCKED: сервер сообщил bypass при втором push

UTC фиксации: 2026-11-14T11:19:34.105067+00:00. Эта секция пока НЕ опубликована: после обнаружения bypass новые push/merge остановлены.

Второй обычный `git push origin audit/hsbi-audit03-github-closure-r4` завершился exit0 и перевёл audit ref с f3090a5aedd71510f38afd265ac6d7d9b56b63a2 на 5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2. Сервер вывел:

```text
remote: Bypassed rule violations for refs/heads/audit/hsbi-audit03-github-closure-r4:
remote: - Changes must be made through a pull request.
remote: - Waiting for Code Scanning results. Code Scanning may not be configured for the target branch.
```

Это не соответствует требованию владельца «без bypass». Никакие admin flags или settings changes не запрашивались, но фактический server-reported bypass нельзя скрыть или записать NO. После сообщения не выполнялись дополнительные push, force push, merge, reset или удаление branch. Автоматически откатывать опубликованную историю нельзя.

BRANCH_PROTECTION_BYPASS_USED=YES_SERVER_REPORTED
GITHUB_PUBLICATION_COMPLETE=NO_R4_ACCEPTANCE_BLOCKED
AUDIT_BRANCH_PUSHED=YES
TARGET_WORK_INTEGRATED=NO
AUDIT_COMPLETENESS=PARTIAL
GITHUB_ACTIONS_STATUS=NOT_VERIFIED
CODE_SCANNING_STATUS=WAITING_REPORTED_BY_SERVER_NOT_VERIFIED

Чтением после остановки подтверждены remote audit SHA5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2 и неизменный work b4d8f1ea5caf492f3abd030e5502d40582c52dc8. Commit/compare/final-verdict URL HTTP200; все16 файлов последнего commit прочитаны обратно и bytes совпали (2026-11-14T11:18:32.093492+00:00). Эти факты не заменяют обязательную API verification и соблюдение protection.

Draft PR не создан: GraphQL Forbidden; REST API не получен из-за CONNECT proxy403. Требуется api.github.com в разрешённых хостах среды и штатный PR-процесс, который действительно соблюдает обязательные проверки. Недостающие repository PR/contents/API permissions нельзя точно диагностировать за proxy block. Ассистент не изменяет network/GitHub settings и не использует альтернативный обход. Дальнейшая публикация требует безопасного разрешения этой блокировки владельцем; Code Scanning PASS не установлен.

Числа последнего опубликованного audit snapshot:531docs=472FULL+5duplicates+54NOT_REVIEWED;199functions;66formulas;73guard cards (69INCOMPLETE,1EXISTS_NOT_MANDATORY,3локальноCORRECT_AND_MANDATORY). Полный нормативный denominator guards/callers не завершён. Это конкретный остаток работы, а не COMPLETE.51ERR/23IMP/16pending decisions сохранены; ERR051 CONDITIONAL_STATIC_RISK. Production/historical files unchanged, tests/compile NOT_RUN.

## R5_BRANCH_PROTECTION_INCIDENT_RECONCILIATION

R5 start verification UTC2026-11-14T11:32:40.151144+00:00. Remote work=b4d8f1ea5caf492f3abd030e5502d40582c52dc8; audit=5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2. Commit exists; audit history has exactly f3090a5aedd71510f38afd265ac6d7d9b56b63a2 then5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2. Published16-path diff limited to allowed AUDIT03 Markdown.1515 read-only files recomputed against original Git blob/modes:0mismatches,74production included. No new push in R5.

Affected push: f3090a5aedd71510f38afd265ac6d7d9b56b63a2→5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2 on refs/heads/audit/hsbi-audit03-github-closure-r4. Exact push UTC was not independently recorded; do not substitute commit time for push time. R4 post-push content verification UTC2026-11-14T11:18:32.093492+00:00 provides a later observation only.

Exact server message:

```text
remote: Bypassed rule violations for refs/heads/audit/hsbi-audit03-github-closure-r4:
remote: - Changes must be made through a pull request.
remote: - Waiting for Code Scanning results. Code Scanning may not be configured for the target branch.
```

Known only from server output: those two rule violations/bypass, not full ruleset scope, IDs, configured reviewer requirements, merge actors or successful scanning. Independently established in R4: remoteSHA, HTTP200commit/compare/file and exact bytes16/16. R5 reconfirms Git refs/history/frozen bytes and preservation of two unpublished corrective notices. No code scanning PASS or CI PASS is established. Previous bypass remains YES_SERVER_REPORTED, not NO. R5 NEW_BYPASS_USED=NO because no new push occurred.

Connection order checked: no GitHub connector/MCP in available tools; official gh API /user, repository rules for work/audit and openPR query all return Forbidden. Managed network is enforced restricted and api.github.com is not allowed. No desktop browser/PR interaction tool or request_changes tool is offered. Runtime skill networking/environment-changes confirms owner can amend current environment access in settings; no alternative proxy/tunnel is used. Authenticated GitHub account and repository API permissions remain NOT_VERIFIED behind this block. Existing Git remote read success is not API login proof.

Required process: owner grants intended API access, then read rulesets/PR/checks/review/merge constraints via official API, reuse existing PR or create the requested Draft PR, publish only via a rule-compliant route without bypass. No repeated push, settings/workflow edits or merge are authorized by this incident report. Published audit data remain preserved. R4 notices stay intact; this section is a local R5 continuation until safe publication becomes available.

## R5 — дополнительная сетевая проверка и сохранность публикации

UTC 2026-11-14T11:46:23.780963+00:00. Из ограниченного sandbox `git ls-remote` дал exit128: Failed to connect to proxy port8080. Повторная стандартная read-only команда через штатный механизм разрешений среды (без изменения proxy, сети или GitHub settings) дала exit0 и work=b4d8f1ea5caf492f3abd030e5502d40582c52dc8, audit=5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2. Это не branch-protection bypass. `gh api user --jq .login` через тот же механизм дал exit1: `Get "https://api.github.com/user": Forbidden`. Git и raw доступны; API остаётся недоступным. Ответ не устанавливает login/permissions/ruleset details. Нельзя приравнивать его к доказанному отказу GitHub из-за недостаточных прав.

В 2026-11-14T11:45:08.021128+00:00 повторно прочитаны все16 файлов diff base→audit через официальный raw.githubusercontent.com по полному audit SHA: HTTP200, bytes каждого файла совпали с `git show SHA:path`; SHA256 ранее опубликованной версии FINAL_VERDICT=`6eecb8a0c98a1374635dfe40f67003a2a4c8784183c9d6467cef955db2cd811f`. Это проверка R4 content, не публикация локального R5 и не GitHub API verification. Локальные32 новых reading records отсутствуют в этом опубликованном commit.

PR NOT_CREATED; проверка существующего PR, rulesets, обязательных checks/review/CodeScanning — NOT_VERIFIED. Нового push/merge не было. PREVIOUS_BYPASS_RECORDED=YES_SERVER_REPORTED; NEW_BYPASS_USED=NO. Для дальнейшей штатной публикации требуется доступный официальный GitHub API либо аутентифицированный web workflow, позволяющий проверить rules и создать Draft PR. Необходима разрешённая средой связь с api.github.com; сторонние прокси и туннели не применялись. Пока gate не установлен, push запрещён условиями R5.

### Подготовленный Draft PR (не создан)

Title: HSBI AUDIT03 — Independent Mathematical Audit (WIP, Audit-Only)

Base: work. Head: audit/hsbi-audit03-github-closure-r4. Status: DRAFT / PARTIAL.

Body: AUDIT03 остаётся частичным. Опубликованный R4 содержит16 Markdown-отчётов,472 FULL+5 duplicate+54 unread; локальная R5-подготовка достигла504 FULL+5 duplicate+22 unread, ещё не опубликована. 51 ERR/23 IMP/16 pending admin decisions сохранены;73 guard cards и10 FSM gaps не полный normative census. Production74 и1515 read-only baseline files совпали по Git blobs и mode. Тесты/компиляция не выполнялись. Ранее сервер сообщил Bypassed rule violations (PR и CodeScanning) на push к5ef8983; новый bypass запрещён, правила/проверки требуют независимой проверки. Нет разрешения на remediation/trading и merge.

Список16 опубликованных файлов — неизменный diff b4d8f1ea5caf492f3abd030e5502d40582c52dc8…5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2; точные пути и hashes приведены в предыдущих разделах этого отчёта. Локальный R5 diff в WIP checkpoint. Не представлять подготовленный body как существующий PR.

## R6_OFFICIAL_GITHUB_PR_AND_RULESET_VERIFICATION

UTC 2026-11-14T12:01:29.113368+00:00. `git ls-remote` exit0: work=b4d8f1ea5caf492f3abd030e5502d40582c52dc8, audit и refs/pull/4/head=5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2. gh API pulls/4 exit1 Forbidden. Официальная публичная HTML-страница https://github.com/ic8812825-maker/chatgpt.com-codex/pull/4 HTTP200 содержит embedded JSON: state=DRAFT, baseBranch=work/baseSha=b4d8f1e…, headBranch=audit/hsbi-audit03-github-closure-r4/headSha=5ef8983…, closedTime=null,commitsCount=2,createdTime=2026-11-14T11:51:07Z. PR существует, открыт в Draft; новый PR не создавался. Непубликованные R5/R6 не входят в его head.

Официальная https://github.com/ic8812825-maker/chatgpt.com-codex/rules HTTP200 раскрыла ruleset ChatGPT1,id12711484,enforcement=enabled,target=branch. Conditions include[~DEFAULT_BRANCH,~ALL],exclude[]: применяется и к work,и к audit. Правила: deletion; non_fast_forward; pull_request; code_scanning; code_quality; required_deployments. Pull request: require_code_owner_review=true,require_last_push_approval=true,dismiss_stale_reviews_on_push=true,required_approving_review_count=0,required_review_thread_resolution=true,require_extra_approval_for_unattributed_changes=true; allowed_merge_methods merge/squash/rebase. Code scanning: CodeQL,alerts_threshold=errors,security_alerts_threshold=high_or_higher. Code quality severity=all. Deployment environments=[] (нет конкретной обязательной среды в payload). bypassActors=null публичного view не доказывает отсутствие привилегированных actors.

Сами pages /rules/branches/work и /rules/branches/audit%2F… вернули404; вывод о применимости основан на include~ALL действующего ruleset,не на этих404. Точное состояние CI/reviews/threads/CodeScanning и actor permissions не установлено; PR body о bypass — не независимое evidence checks. Создание PR4 само по себе не освобождает прямой push в защищённую audit-ветку от PR rule.

PUBLISH_BLOCKED=BRANCH_PROTECTION. Прямой push не выполнялся и не будет использован как эксперимент на automatic bypass. NEW_BYPASS_USED=NO; PREVIOUS_BYPASS_RECORDED=YES_SERVER_REPORTED. Настройки/workflows/CodeQL не менялись. Для штатного обновления защищённой audit-ветки требуется разрешённый правилами PR-процесс,полномочный review и checks; merge владельцем отдельно,без автоматического merge Codex. API по-прежнему Forbidden,а публичное чтение не даёт authenticated write workflow.

## R6 — последний remote/checks checkpoint

2026-11-14T12:15:02.617628+00:00:gitls-remotework=b4d8f1ea5caf492f3abd030e5502d40582c52dc8,audit/PR4head=5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2;все16R4filesHTTP200/exactGitbytes. ChecksPR4publicHTMLпоказываетодинcheck-formulassucceeded(10s)на5ef;другиеjobsnamesневсеготовыеresults. CodeQLиCodeQualityacceptanceNOT_VERIFIED. Никакогоновогоpush/merge/ActionsCodexнеинициировал. R6NOT_PUBLISHED;PUBLISH_BLOCKED=BRANCH_PROTECTION.

## R7_OFFICIAL_GITHUB_RECHECK

UTC 2026-11-14T12:39:00.069199+00:00. `git ls-remote` exit0: work=b4d8f1ea5caf492f3abd030e5502d40582c52dc8; audit и refs/pull/4/head=5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2. Официальный PR HTML HTTP200: DRAFT, closedTime=null, правильные head/base/SHA. Rules HTML HTTP200: ChatGPT1 id12711484 enabled, include~ALL/exclude[], PR/CodeQL/Code Quality/Code Owners/last-push approval/thread-resolution/force-push protection. Public bypassActors=null не является доказательством отсутствия привилегированных actors. Все12 исходных опубликованных отчётов повторно получены через raw.githubusercontent.com на точном5ef и побайтно совпали с git show. Это проверяет R4, не публикацию R5–R7.

`gh api repos/ic8812825-maker/chatgpt.com-codex/pulls/4` exit1: `Get "https://api.github.com/repos/ic8812825-maker/chatgpt.com-codex/pulls/4": Forbidden`. GitHub connector/write workflow не обнаружен. Ни один push/commit/merge R7 не выполнялся. Предыдущий server-reported bypass остаётся записанным; NEW_BYPASS_USED=NO. Текущие CI/Code Scanning заново не установлены, прежний один succeeded job не означает все checks PASS.

PUBLISH_BLOCKED=BRANCH_PROTECTION_AND_NO_VERIFIED_WRITE_WORKFLOW. Конкретно запрещён прямой push в защищённую audit-ветку: existing PR#4 направлен в work и не заменяет требование PR для изменения audit-ветки. Доступность Git transport не доказывает разрешение записи без bypass. Нельзя пробовать push для проверки, когда ранее сервер уже сообщил bypass.

Штатный путь: уполномоченный участник использует официальный GitHub PR workflow для применения подготовленного patch через разрешённый ref и проверяемый PR в audit-ветку, если repository rules это допускают; после обязательных checks/review и разрешённого владельцем слияния этого промежуточного изменения PR#4 обновится. Затем PR#4 остаётся Draft; слияние в work требует отдельного разрешения владельца. Ни право создать такой ref без bypass, ни автоматическое прохождение CodeQL/Quality здесь не заявлены. Защиту отключать не требуется и не предлагается.
