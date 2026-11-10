# C2 — результаты проверок

BASE_SHA=fae7dfc18ca2d61af2f3446826ef3031825bbfd8

PROPOSED / AWAITING_ADMIN_APPROVAL. Только audit/test-only; production и trading запрещены.

Различные reference scenarios=158; contexts=8; executions=1264; reference PASS=1264. Отдельные schema probes=2462, каждый один раз вне context cross-product; comparisons=9914 (2 на execution +3 на schema probe). Эти величины не суммируются в число независимых сценариев.

Mutation catalog=70; killed=64; redundant survivors=6; unexplained=0; infrastructure errors=0. Каждый redundant survivor имеет mandatory caller proof и whole reference-domain regression. UNSAFE_ACCEPTANCE_KILL и STATUS_CONTRACT_KILL различаются в строках. Начальные два survivors сохранены в DEVELOPMENT.json; выявлено дублирование fact/claim guards, добавлены dual-caller и direct-schema причинные probes, без искусственных exceptions.

Package positive=PASS; negative passed=58; negative failed=0. Старые46 классов остаются отдельно помеченной группой, strict JSON/schema/clause probes добавлены отдельно. Parser/import/runtime error не semantic kill. JSON всех новых artifacts проходит общий strict loader.

Regression status=FAIL; baseline match=True; runs=31. R7/R0 сохраняют исходные exit1 и57/5,35/46. Нет выдуманного standalone02A; повторяется доступный no-trade scan. Commands, timestamps, source/runner hashes, stdout/stderr: REGRESSIONS.json. Adapted C2 runner — новый реальный файл со своим source hash, не подмена C1 runner.

DEVELOPMENT.json сохраняет initial8FAIL/8INFRA (nullable batch dereference и status expectation) и начальный archive adapter failure. Ни одна ошибка не удалена из evidence. Дополнительно сохранены initial regression copy-race, неверный путь mandatory package probe и перезапись inventory edit при reseal. Две bool-counter probes первоначально получили FAIL из-за ожидаемого кода позднего слоя: strict JSON уже корректно отклонял их как PACKAGE_SCHEMA; изменён диагностический expected code, защита не ослаблена. DEVELOPMENT.log/MUTATION.log/REPRODUCTION.log/REGRESSIONS.log сохраняют последовательность запусков. Expected malformed DTO не скрывается blanket except Exception; неожиданные implementation errors видимы как INFRASTRUCTURE_ERROR.

Команды: check_hsbi_02b_r0e_c2_reproduction.py; check_hsbi_02b_r0e_c2_contracts.py; check_hsbi_02b_r0e_c2_mutations.py; run_hsbi_02b_r0e_c2_regressions.py; build_hsbi_02b_r0e_c2_catalog.py; check_hsbi_02b_r0e_c2_package.py --seal --self-test. build_hsbi_02b_r0e_c2_reports.py генерирует только новые документы из evidence. Default package run read-only.

MQL5_COMPILE=NOT_RUN; MQL5_TESTS=NOT_RUN; STRATEGY_TESTER=NOT_RUN. Production не исправлялся. Broker/global funding/durable/concurrency/NewFar — UNPROVEN.
