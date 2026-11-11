# Руководство и нормативная иерархия

BASE_SHA=4185b84f7a6a8847f6a9c5796f07113907be447d

Режим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.

Найдено основное руководство `Docs/03_FULL_SYSTEM_MANUAL_RU.md`, все51 строки прочитаны. Это компактная схема, а не готовое operator handbook: подробности разнесены по00–32 owner-docs и historical/proposed amendments. Формальные источники владельцев не равны работающему implementation. Все133 документа проиндексированы с SHA256/headings/status locators;31 owner-текст прочитан целиком,19/21/22 и многие исторические appendices проиндексированы/выборочно сопоставлены, не повторно доказаны целиком.

Иерархия: явные пользовательские границы текущего задания > отдельные документированные административные решения в их scope > owner-contracts с явными amendments > historical acceptance только своего этапа > proposed R0A–R0H (AWAITING) > reference evidence/фактический code. Нельзя превратить code или PASS в экономический норматив. Docs23 CLOSED_FOR_HSB1_ARCHITECTURE не разрешает исправления/торговлю; OPEN_P0=0 относится к старому архитектурному срезу, не текущему source verdict.

Основные противоречия: minimum-safeN (03:21/14:22) против risk-first (29:3/code); allocation equality (08:12) и inequality/remaining+consumed (32:3) без typed phase/balance mapping; FarLossIncrease имя против absolute фактической величины; WORST_CASE maxTransitionLoss не предложенный minCatchUpMargin; thin3-field legacy equality против immutable economic identity; старые ManagedIdentity безAccount в02:20 против23:22/Core. Никакое изменение не утверждено этим аудитом. D01–D08/CR09/NUM/SNAP/funding остаются pending, complete/current authority package не доказан.

| Document | Lines | Review boundary | Title |
|---|---|---|---|
| BUILD_INFO.md | 324 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | ## Нормативный статус HSB.1V (2026-08-10) |
| CHANGELOG_RU.md | 307 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # CHANGELOG |
| Docs/00_PROJECT_CHARTER_RU.md | 31 | READ_FULL_OWNER_TEXT | # Устав проекта Hybrid Split Big |
| Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md | 56 | READ_FULL_OWNER_TEXT | # Глоссарий и размерности Hybrid Split Big |
| Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md | 36 | READ_FULL_OWNER_TEXT | # Роли и identity Hybrid Split Big |
| Docs/03_FULL_SYSTEM_MANUAL_RU.md | 51 | READ_FULL_OWNER_TEXT | # Полный системный мануал Hybrid Split Big |
| Docs/04_MATHEMATICAL_MODEL_RU.md | 43 | READ_FULL_OWNER_TEXT | # 04. Полная математическая модель Hybrid Split Big |
| Docs/05_GEOMETRY_MODEL_RU.md | 32 | READ_FULL_OWNER_TEXT | # 05. Геометрическая модель и контрольные цены |
| Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | 22 | READ_FULL_OWNER_TEXT | # 06. State Machine Hybrid Split Big |
| Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md | 25 | READ_FULL_OWNER_TEXT | # 07. Event-driven transaction execution contract |
| Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md | 25 | READ_FULL_OWNER_TEXT | # 08. Economic Ledger и Allocation Ledger |
| Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md | 28 | READ_FULL_OWNER_TEXT | # 09. Initial Lock и создание исходного Far |
| Docs/10_BIG_HARVEST_SPECIFICATION_RU.md | 17 | READ_FULL_OWNER_TEXT | # 10. Полная спецификация Big Harvest |
| Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md | 14 | READ_FULL_OWNER_TEXT | # 11. Partial Far |
| Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md | 18 | READ_FULL_OWNER_TEXT | # 12. Единый нормативный Final Close |
| Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | 23 | READ_FULL_OWNER_TEXT | # 13. Small Transition и единственный NewFar |
| Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md | 28 | READ_FULL_OWNER_TEXT | # 14. Broker-valid deterministic minimum-safe NewFar Solver |
| Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md | 24 | READ_FULL_OWNER_TEXT | # 15. Risk, Margin, Drawdown и Emergency contract |
| Docs/16_PERSISTENCE_AND_RESTART_RU.md | 21 | READ_FULL_OWNER_TEXT | # 16. Persistence и restart contract |
| Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md | 26 | READ_FULL_OWNER_TEXT | # 17. Reconciliation и terminal-safe recovery routes |
| Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md | 30 | READ_FULL_OWNER_TEXT | # 18. Независимая MQL5-архитектура Hybrid Split Big |
| Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md | 434 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 19. Матрица требований и MQL5 mapping HSB.1 |
| Docs/20_TEST_STRATEGY_RU.md | 28 | READ_FULL_OWNER_TEXT | # Стратегия MQL5 и MT5 тестирования |
| Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md | 309 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Критерии production-готовности |
| Docs/22_OPEN_DECISIONS_REGISTER_RU.md | 325 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Hybrid Split Big Independent EA |
| Docs/23_NORMATIVE_DECISIONS_RESOLUTION_RU.md | 29 | READ_FULL_OWNER_TEXT | # 23. Полный нормативный реестр решений Hybrid Split Big |
| Docs/24_BROKER_MONEY_MODEL_RU.md | 21 | READ_FULL_OWNER_TEXT | # 24. Broker-Money Model HSB.2A |
| Docs/25_BROKER_GRID_AND_ROUNDING_RU.md | 17 | READ_FULL_OWNER_TEXT | # 25. Broker Grid и rounding HSB.2A |
| Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md | 17 | READ_FULL_OWNER_TEXT | # 26. Geometry Engine HSB.2A |
| Docs/27_CONTROL_PRICES_AND_COSTS_RU.md | 17 | READ_FULL_OWNER_TEXT | # 27. Control Prices и Costs HSB.2A |
| Docs/27_FUTURE_SMALL_SOLVER_RU.md | 41 | READ_FULL_OWNER_TEXT | # 27. Future Small Solver HSB.2B |
| Docs/28_NEW_FAR_SOLVER_RU.md | 39 | READ_FULL_OWNER_TEXT | # 28. NewFar Solver HSB.2B |
| Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md | 37 | READ_FULL_OWNER_TEXT | # 29. Candidate objective и tie-break HSB.2B |
| Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | 15 | READ_FULL_OWNER_TEXT | # 30. Aggregate proof Future Small |
| Docs/31_MONEY_PROOF_IDENTITY_RU.md | 7 | READ_FULL_OWNER_TEXT | # 31. Identity broker-money proof |
| Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | 7 | READ_FULL_OWNER_TEXT | # 32. Reserve allocation и consumption |
| Docs/HSB.2C_Execution_Intent_Spec.md | 5 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C — Execution Intent |
| Docs/HSB.2C_Idempotency_and_Restart_Safety.md | 5 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C — Idempotency и restart safety |
| Docs/HSB.2C_Journal_Persistence_Reconciliation.md | 7 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C — Journal, persistence и reconciliation |
| Docs/HSB.2C_Preflight_and_Lifecycle.md | 5 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C — Preflight и lifecycle |
| Docs/HSB.2C_R1_Correction_Spec_RU.md | 5 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C-R1 — correction specification |
| Docs/HSB.2C_R1_Journal_Chain_RU.md | 3 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C-R1 — journal chain |
| Docs/HSB.2C_R1_P1_Publication_Spec_RU.md | 5 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C-R1-P1: publication contract |
| Docs/HSB.2C_R1_P1_Runtime_Policy_RU.md | 13 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C-R1-P1: runtime policy |
| Docs/HSB.2C_R1_P1_Traceability_RU.md | 10 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C-R1-P1: traceability |
| Docs/HSB.2C_R1_P2_Include_Graph_Audit_RU.md | 15 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C-R1-P2 — аудит include graph |
| Docs/HSB.2C_R1_P2_Publication_Audit_RU.md | 3 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Publication audit HSB.2C-R1-P2 |
| Docs/HSB.2C_R1_P2_Runtime_Policy_Canonical_RU.md | 11 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Canonical Runtime Policy HSB.2C-R1-P2 |
| Docs/HSB.2C_R1_P2_Traceability_RU.md | 9 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Traceability HSB.2C-R1-P2 |
| Docs/HSB.2C_R1_Runtime_Mode_Policy_RU.md | 3 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C-R1 — runtime mode policy |
| Docs/HSB.2C_R1_Security_Invariants_RU.md | 5 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C-R1 — security invariants |
| Docs/HSB.2C_R1_Traceability_RU.md | 10 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C-R1 — traceability |
| Docs/HSB.2C_Traceability.md | 13 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2C — Traceability |
| Docs/HSB_2D_ALLOCATION_CONSUMPTION_RUNTIME_RU.md | 3 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2D — Allocation и Consumption Runtime |
| Docs/HSB_2D_PERSISTENCE_RESTART_CONTRACT_RU.md | 3 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2D — Persistence и Restart |
| Docs/HSB_2D_RUNTIME_INTEGRATION_RU.md | 5 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2D — Runtime Integration |
| Docs/HSB_2D_TRANSACTION_BARRIER_RU.md | 3 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2D — Transaction Decision Barrier |
| Docs/HSB_2D_V2_EXACT_TEST_PROCEDURE_RU.md | 11 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2D-V2: точная пользовательская процедура |
| Docs/HSB_2D_V2_METAEDITOR_USER_VERIFICATION_RU.md | 3 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2D-V2 MetaEditor/MT5 handoff |
| Docs/HSB_2D_V2_REQUIRED_EVIDENCE_CHECKLIST_RU.md | 13 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2D-V2: обязательный evidence checklist |
| Docs/HSB_2E_API_CONTRACTS_R2_RU.md | 38 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E-PREP-R2 — semantic API и ownership contracts |
| Docs/HSB_2E_API_CONTRACTS_RU.md | 77 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E точные API-контракты |
| Docs/HSB_2E_BIG_HARVEST_IMPLEMENTATION_CONTRACT_RU.md | 27 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E BIG_HARVEST implementation contract |
| Docs/HSB_2E_DEPENDENCY_GRAPH_RU.md | 8 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E dependency graph |
| Docs/HSB_2E_FINAL_CLOSE_IMPLEMENTATION_CONTRACT_RU.md | 27 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E FINAL_CLOSE implementation contract |
| Docs/HSB_2E_FORMULA_CONTRACTS_R2_RU.md | 34 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E-PREP-R2 — нормативные formula contracts |
| Docs/HSB_2E_FSM_TRANSITION_TABLE_RU.md | 20 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E FSM transition table |
| Docs/HSB_2E_FULL_TRADING_LOGIC_IMPLEMENTATION_PLAN_RU.md | 289 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E — полный план будущей торговой реализации |
| Docs/HSB_2E_INITIAL_LOCK_IMPLEMENTATION_CONTRACT_RU.md | 27 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E INITIAL_LOCK implementation contract |
| Docs/HSB_2E_NEW_FAR_CATCH_UP_IMPLEMENTATION_CONTRACT_RU.md | 27 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E NEW_FAR_CATCH_UP implementation contract |
| Docs/HSB_2E_PARTIAL_FAR_RESERVE_IMPLEMENTATION_CONTRACT_RU.md | 27 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E PARTIAL_FAR_RESERVE implementation contract |
| Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md | 21 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E persistence schema |
| Docs/HSB_2E_PREP_R2_ADMIN_HANDOFF_RU.md | 7 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Административный handoff HSB.2E-PREP-R2 |
| Docs/HSB_2E_PREP_R3_IMPLEMENTATION_HANDOFF_RU.md | 27 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E-PREP-R3 — административный implementation handoff |
| Docs/HSB_2E_PREP_R4_IMPLEMENTATION_HANDOFF_RU.md | 24 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E PREP-R4 — implementation handoff |
| Docs/HSB_2E_PREP_R4_R1_IMPLEMENTATION_HANDOFF_RU.md | 7 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E PREP-R4-R1 — implementation handoff |
| Docs/HSB_2E_PREP_R4_R2_IMPLEMENTATION_HANDOFF_RU.md | 16 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # PREP-R4-R2 implementation handoff |
| Docs/HSB_2E_PREP_R4_R3_IMPLEMENTATION_HANDOFF_RU.md | 25 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E PREP-R4-R3 — исполнимый implementation handoff |
| Docs/HSB_2E_PREP_R4_R4_IMPLEMENTATION_HANDOFF_RU.md | 36 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E PREP-R4-R4 — monotonic implementation handoff |
| Docs/HSB_2E_PREP_R4_R5_IMPLEMENTATION_HANDOFF_RU.md | 17 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E PREP-R4-R5 — provenance-backed implementation handoff |
| Docs/HSB_2E_PREP_R4_R6_IMPLEMENTATION_HANDOFF_RU.md | 17 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E PREP-R4-R6 — corrected executable specification handoff |
| Docs/HSB_2E_PREP_R4_R7_IMPLEMENTATION_HANDOFF_RU.md | 23 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E PREP-R4-R7 — implementation handoff |
| Docs/HSB_2E_PREP_R4_R8_IMPLEMENTATION_HANDOFF_RU.md | 19 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E PREP-R4-R8 — implementation handoff |
| Docs/HSB_2E_PRODUCTION_FILE_MAP_RU.md | 38 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E production file map |
| Docs/HSB_2E_SCENARIO_CONTRACTS_R2_RU.md | 18 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E-PREP-R2 — scenario decision contracts |
| Docs/HSB_2E_SIMULATION_FIRST_ARCHITECTURE_RU.md | 3 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E simulation-first architecture |
| Docs/HSB_2E_SMALL_TRANSITION_IMPLEMENTATION_CONTRACT_RU.md | 27 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E SMALL_TRANSITION implementation contract |
| Docs/HSB_2E_TEST_MATRIX_RU.md | 21 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E planned test matrix |
| Docs/HSB_2E_TRANSACTION_LIFECYCLE_RU.md | 22 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSB.2E transaction lifecycle |
| Docs/NEXT_STAGE_01_BASELINE_AUDIT_RU.md | 54 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Этап 1 — исходное состояние и карта проекта |
| Docs/NEXT_STAGE_02A_MONEY_INTEGRITY_AUDIT_RU.md | 257 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSBI — NEXT STAGE 02A |
| Docs/NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md | 167 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0A — кандидат фиксации денежных контрактов |
| Docs/NEXT_STAGE_02B_R0A_MONEY_INVARIANTS_RU.md | 393 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0A — сквозные денежные инварианты |
| Docs/NEXT_STAGE_02B_R0A_NORMATIVE_REVIEW_RU.md | 78 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0A — адресный нормативный review |
| Docs/NEXT_STAGE_02B_R0B_AUTHORITY_AND_REPLAY_CONTRACT_RU.md | 54 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0B — authority, identities и replay |
| Docs/NEXT_STAGE_02B_R0B_CONTRACT_FREEZE_PROPOSAL_RU.md | 111 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0B — окончательное предложение фиксации контрактов |
| Docs/NEXT_STAGE_02B_R0B_FINAL_NORMATIVE_REVIEW_RU.md | 193 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0B — финальная нормативная проверка |
| Docs/NEXT_STAGE_02B_R0B_PRECISION_POLICY_REVIEW_RU.md | 44 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0B — денежная точность и posted amounts |
| Docs/NEXT_STAGE_02B_R0C_NORMATIVE_AND_R1_1_ADDENDUM_RU.md | 24 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0C — дополнение к нормативному пакету и будущему R1.1 |
| Docs/NEXT_STAGE_02B_R0C_ORACLE_CONTRACT_RU.md | 70 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0C — контракт независимого test-only oracle |
| Docs/NEXT_STAGE_02B_R0D_NORMATIVE_ADDENDUM_RU.md | 16 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0D — нормативное дополнение, PROPOSED |
| Docs/NEXT_STAGE_02B_R0D_NUMERIC_CONTRACT_RU.md | 47 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0D — PROPOSED численный контракт до реализации модели |
| Docs/NEXT_STAGE_02B_R0D_SNAPSHOT_IDENTITY_CONTRACT_RU.md | 24 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0D — PROPOSED схема snapshot до выбора encoder |
| Docs/NEXT_STAGE_02B_R0E_C1_API_SCOPE_AND_COMPOSITION_RU.md | 85 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # C1 — scope API и обязательная композиция |
| Docs/NEXT_STAGE_02B_R0E_C1_CONTRACT_ADDENDUM_RU.md | 43 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0E-C1 — дополнение к предлагаемым контрактам |
| Docs/NEXT_STAGE_02B_R0E_C2_DTO_SCHEMA_CONTRACT_RU.md | 17 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # C2 — предлагаемый контракт вложенных DTO |
| Docs/NEXT_STAGE_02B_R0E_C2_GUARD_COVERAGE_AND_RECOVERY_SCOPE_RU.md | 26 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # C2 — clauses, композиция и scope recovery |
| Docs/NEXT_STAGE_02B_R0E_C3_CONTRACT_CLARIFICATIONS_RU.md | 31 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # C3 — уточнения для административного рассмотрения |
| Docs/NEXT_STAGE_02B_R0E_C3_VERIFICATION_BOUNDARIES_RU.md | 23 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # C3 — границы доказательств |
| Docs/NEXT_STAGE_02B_R0E_CONTRACT_FREEZE_CANDIDATE_RU.md | 285 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0E — кандидат согласованных денежных контрактов |
| Docs/NEXT_STAGE_02B_R0E_NUMERIC_ARCHITECTURE_RU.md | 38 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0E — архитектура точной арифметики применительно к MQL5 |
| Docs/NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md | 71 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0E — production-дефекты и ограниченный план будущего remediation |
| Docs/NEXT_STAGE_02B_R0F_DEPENDENCY_GRAPH_RU.md | 41 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # R0F — граф зависимостей |
| Docs/NEXT_STAGE_02B_R0F_ECONOMIC_IDENTITY_SPEC_RU.md | 52 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # R0F — immutable Economic Ledger identity |
| Docs/NEXT_STAGE_02B_R0F_MONEY_CONTRACT_CANDIDATE_RU.md | 55 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # R0F — кандидат денежных контрактов |
| Docs/NEXT_STAGE_02B_R0F_NUMERIC_CODEC_OPTIONS_RU.md | 35 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # R0F — numeric architecture и два codec-кандидата |
| Docs/NEXT_STAGE_02B_R0F_R1_IMPLEMENTATION_SPEC_RU.md | 48 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # R0F — будущий R1.1: два точных scope |
| Docs/NEXT_STAGE_02B_R0G_CODEC_DECISION_RU.md | 34 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # R0G — codec ballot alternatives |
| Docs/NEXT_STAGE_02B_R0G_MINIMAL_DIFF_PLAN_RU.md | 40 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # R0G — one-file diff и native acceptance plan |
| Docs/NEXT_STAGE_02B_R0G_MINIMAL_IDENTITY_CONTRACT_RU.md | 55 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # R0G — минимальный identity contract |
| Docs/NEXT_STAGE_02B_R0G_MQL5_API_SPEC_RU.md | 43 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # R0G — предлагаемые MQL5 signatures, не production code |
| Docs/NEXT_STAGE_02B_R0H_CODEC_COMPARISON_RU.md | 22 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # F64Z и T17Z: сравнение и границы |
| Docs/NEXT_STAGE_02B_R0H_IDENTITY_API_SPEC_RU.md | 17 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # R0H-ID/STATUS: source observations vs funding |
| Docs/NEXT_STAGE_02B_R0H_MINIMAL_R1_DIFF_PLAN_RU.md | 15 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Local scope/callsites и будущий diff |
| Docs/NEXT_STAGE_02B_R0H_NATIVE_DOMAIN_SPEC_RU.md | 15 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Native domain — proposed, NOT_RUN |
| Docs/NEXT_STAGE_02B_R0_CONTRACT_FREEZE_PROPOSAL_RU.md | 72 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R0 — предложение фиксации контрактов |
| Docs/NEXT_STAGE_02B_R1_1_IMPLEMENTATION_SPEC_RU.md | 89 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R1.1 — спецификация ограниченного Economic Ledger этапа |
| Docs/NEXT_STAGE_02B_R1_IMPLEMENTATION_TASK_RU.md | 58 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R1 — точное задание после утверждения контрактов |
| Docs/NEXT_STAGE_02B_R1_PHASED_IMPLEMENTATION_PLAN_RU.md | 235 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # 02B-R1 — атомарный план после отдельного утверждения |
| Docs/NEXT_STAGE_02B_REMEDIATION_PLAN_RU.md | 86 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # HSBI NEXT STAGE 02B — минимальный план исправлений |
| Docs/NEXT_STAGE_02_MONEY_AUDIT_RU.md | 271 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Этап 2 — независимый аудит денежной модели HSBI |
| PROJECT_MAP_RU.md | 328 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Карта проекта Hybrid Split Big Independent EA |
| README_RU.md | 370 | INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED | # Hybrid Split Big Independent EA |

## Полный мануал: section traceability

| Section / locator | Requirement / mechanism | Code & tests | Verdict |
|---|---|---|---|
| Полный цикл Docs/03:5 | `IDLE → Initial Lock actual fills → close INITIAL_PLUS actual deal → FAR → immutable CandidatePlan → C/T/S basket actual fills → Big Harvest → Allocation → Final Close или Partial Far`, либо `Small confirmation → immutable transition → close SMALL_BASE → OldFar → BIG_TREND → planned BIG_CORE part → actual BIG_CORE residual → NEW_FAR → FAR нового цикла`. | EXTRACTED.json, REFERENCE.json, state/call matrices | UNIMPLEMENTED |
| Роли и направления Docs/03:8 | Far SELL: BIG_CORE и BIG_TREND BUY, SMALL_BASE SELL. Far BUY: BIG_CORE и BIG_TREND SELL, SMALL_BASE BUY. BUY close рассчитывается по Bid, SELL close по Ask. Одновременно допускается только один FAR. | EXTRACTED.json, REFERENCE.json, state/call matrices | PARTIALLY_VERIFIED |
| Объёмы и три закона Docs/03:11 | `C=FloorBrokerGrid(F×Rc)`, `T=FloorBrokerGrid(F×Rt)`, `S=CeilBrokerGrid(F×Rs)`, `Bnet=C+T-S`. После округления обязательны: `Bnet-F>0`; broker-money Reserve Catch-Up; `RecoveryPL(P+tick)>RecoveryPL(P)` на проверяемом диапазоне; compression `0<N<F` с risk/margin/next-cycle gates. Rc>0, Rt≥0, Rs>0; любые NaN, overflow, invalid volume или failed proof дают reject. Demonstration profile не является default. | EXTRACTED.json, REFERENCE.json, state/call matrices | CONTRADICTORY |
| Typed control prices Docs/03:14 | CurrentClosePrice, NextBigControlPrice, SmallTransitionControlPrice, AdverseRiskControlPrice, GapStressPrice, FinalClosePrice всегда содержат Bid/Ask side, tick-normalized price, timestamp и freshness. Stale snapshot блокирует действие. | EXTRACTED.json, REFERENCE.json, state/call matrices | PARTIALLY_VERIFIED |
| CandidatePlan и Future Small Docs/03:17 | Plan immutable и связан с Account+Symbol+Magic+CycleID+StateRevision+market snapshot. Future Small проверяется exact recursion до terminal/depth/bound, затем conservative `F(k+j)≤q^jF(k)`, 0<q<1. Depth 1 не является доказательством. | EXTRACTED.json, REFERENCE.json, state/call matrices | CONTRADICTORY |
| NewFar Docs/03:20 | Solver перебирает broker-valid N по возрастанию и выбирает minimum-safe. Fixed TargetNewFarRatio не является solver. Tie-break: RiskNext, MarginNext, expected transitions, safety buffer, N. Источник NEW_FAR — только actual remaining original BIG_CORE ticket/identifier после подтверждённых fills. | EXTRACTED.json, REFERENCE.json, state/call matrices | CONTRADICTORY |
| Money и allocation Docs/03:23 | `DealNet=Profit+Swap+Commission+Fee`. Initial Profit и opening DEAL_ENTRY_IN исключены. Для каждого SourceDealKey: `FinalReserve+PartialFar+Transition+Carry+Residual=AllocatableDealNet`; отрицательный DealNet не распределяется как прибыль. EventKey и ConsumptionKey обеспечивают exactly-once. FinalReserve никогда не используется Partial Far. | EXTRACTED.json, REFERENCE.json, state/call matrices | CONTRADICTORY |
| Partial Far Docs/03:26 | Только PartialFarBudget резервируется; `CloseLotRaw=Budget/FarCloseLossPerLot`, затем floor по broker step и повторная проверка стоимости. Actual consumption определяется actual closing DealNet. Unused reservation освобождается. Partial fill блокирует следующий шаг. | EXTRACTED.json, REFERENCE.json, state/call matrices | UNIMPLEMENTED |
| Transition Loss Docs/03:29 | `TransitionNet=ΣActualClosingDealNet`, `TransitionLoss=max(0,-TransitionNet)`. Разрешённый loss — минимум absolute cap, equity cap, OldFar-risk cap и cumulative-cycle cap. | EXTRACTED.json, REFERENCE.json, state/call matrices | PARTIALLY_VERIFIED |
| Final Close Docs/03:32 | Единая authority: `RecoveryPLCloseNow ≥ MinimumRecoveryProfitMoney + ExecutionSafetyBufferMoney + MoneyTolerance`, где `RecoveryPLCloseNow=RealizedCycleNet+ΣOpenPositionCloseNowNet`. Allocation buckets повторно не прибавляются. Дополнительно обязательны reconciled positions, no pending actions, no unknown deals, valid ownership, fresh FinalClosePrice, costs and allowed coverage. | EXTRACTED.json, REFERENCE.json, state/call matrices | UNIMPLEMENTED |
| Small confirmation Docs/03:35 | Touch недостаточен. Нужны close-side touch, повторный fresh snapshot, configurable hold/retrace, persisted debounce key и отсутствие active transition. Duplicate trigger — NO-OP. | EXTRACTED.json, REFERENCE.json, state/call matrices | UNIMPLEMENTED |
| Transaction, retry и timeout Docs/03:38 | `Plan→Action→Persist→Request→OnTradeTransaction→fill accumulation→actual state→ledger→persist→FSM advance`. REQUEST_SENT/PLACED/DONE_PARTIAL не равны completed. Retry допускается только с тем же ActionID, после history check, при отсутствии completed deal, reconciliation=PENDING и исключённом duplicate request. TIMEOUT не равен failure или completed и ведёт в reconciliation. | EXTRACTED.json, REFERENCE.json, state/call matrices | UNIMPLEMENTED |
| Risk, margin и emergency Docs/03:41 | Перед открытием: ownership→freshness→spread→volume→margin→free margin→drawdown→gross exposure→worst case. Неизвестное значение = fail-closed. Emergency Liquidation отделена от recovery Final Close, не получает recovery PASS, блокирует открытия и требует manual review/no auto-resume. | EXTRACTED.json, REFERENCE.json, state/call matrices | CONTRADICTORY |
| Scope, persistence и REAL_LIMITED Docs/03:44 | Identity: AccountLogin+Symbol+Magic+CycleID+PositionIdentifier+Role. Generation 1: один цикл на Symbol+Magic; multi-symbol только при полной изоляции. Persistence: crash-consistent versioned file commit protocol, canonical serialization, SHA-256, temp write, reread verify, commit marker, previous snapshot, append-only journal, per-identity lock. REAL_LIMITED запрещён до всех readiness gates, Demo Forward PASS и отдельного одобрения администратора. | EXTRACTED.json, REFERENCE.json, state/call matrices | UNIMPLEMENTED |
| Restart/error semantics Docs/03:47 | Restart сверяет actual positions/orders/deals, snapshot и action/event ledgers. Нельзя угадывать FAR, восстанавливать только по comment или продолжать после conflict. Critical mismatch → RECONCILIATION/TERMINAL_SAFE. Статус: OPEN_P0=0, OPEN_P1=0, OPEN_P2=0; production code отсутствует; real trading запрещена. > **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены. | EXTRACTED.json, REFERENCE.json, state/call matrices | UNIMPLEMENTED |

Формальная построчная карта owner-требований — REQUIREMENT_MATRIX.Rows. Статус PARTIALLY_VERIFIED не означает весь paragraphPASS. Именованные владельцы вроде TransactionEngine/FillAccumulator/FinalCloseCalculator/SnapshotStore во многих случаях существуют только в руководстве; source содержит DTO/stubs. Полнота operational parameters, account support, rounding/transition/buffer policies, emergency/recovery и proof providers не подтверждена.
