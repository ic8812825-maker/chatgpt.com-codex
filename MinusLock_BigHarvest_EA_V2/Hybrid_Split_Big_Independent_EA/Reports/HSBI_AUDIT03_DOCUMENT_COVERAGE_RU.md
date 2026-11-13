# AUDIT03 — карта документального покрытия

**AUDIT_COMPLETENESS=PARTIAL. FULL_MANUAL_READ=YES (Docs/03, строки1–51).** Полное чтение основных34 нумерованных Docs не означает полное чтение исторических приложений. Ни перечень файлов, ни подсчёт строк, ни SHA256 не считаются семантическим прочтением. Диапазоны ниже относятся к фактически прочитанному тексту в текущем аудите; усечённые выводы не засчитаны как полные, если не перечитаны.

## Иерархия

Нумерованные Docs — первичные заявленные source-of-truth с историческими уточняющими границами. HSB.2C/2D/2E — исторические execution/preparation contracts, не разрешение текущего торгового runtime. NEXT_STAGE R0–H и DG01 — proposed/specification/audit материалы: approval от наличия текста не возникает. Production показывает фактические предикаты, но не автоматически утверждённую экономику. Исторические test evidence не заменяют математический вывод. При несовместимости direction/objective/active legs — CONFLICT/DECISION_REQUIRED, а не молчаливое правило «новее всегда правильно».

Для консервативного числителя NORMATIVE_DOCUMENTS_TOTAL взяты все136 Markdown в Docs: сюда включены потенциально определяющие требования исторические/proposed приложения. Это **не136 утверждённых нормативов**. Полностью прочитаны51; остальные имеют явный gap. Нормативную приоритетность каждого непрочитанного приложения ещё надо сверить, поэтому полнота намеренно не повышается.

| Path | Lines | Фактически прочитано | Статус источника | Формулы | Модули | Конфликты / gaps |
|---|---|---|---|---|---|---|
| Docs/00_PROJECT_CHARTER_RU.md | 31 | 1–31, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F036,F060 | Core/runtime | ERR-016/028 |
| Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md | 56 | 1–56, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F030,F033–035,F044–046 | Core/Money/Grid | ERR-020/036/040 |
| Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md | 36 | 1–36, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F017,F057,F060 | Identity/Context | ERR-002/012/013 |
| Docs/03_FULL_SYSTEM_MANUAL_RU.md | 51 | 1–51, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F001–060 | Full cycle | ERR-015/018/019/028/046 |
| Docs/04_MATHEMATICAL_MODEL_RU.md | 43 | 1–43, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F001–028,F037–038,F058 | Geometry/Money | ERR-006/020/021/032/043 |
| Docs/05_GEOMETRY_MODEL_RU.md | 32 | 1–32, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F039,F044–046 | Planning/ControlPrices | ERR-024/037 |
| Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | 22 | 1–22, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F057 | Core/FSM | ERR-016/025 |
| Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md | 25 | 1–25, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F015,F036,F057 | Execution | ERR-010/017/030 |
| Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md | 25 | 1–25, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F007,F012–019,F053–057,F060 | Money/Ledgers | ERR-001–008/033/047 |
| Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md | 28 | 1–28, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F034–035,F050 | InitialLock | ERR-023/036 |
| Docs/10_BIG_HARVEST_SPECIFICATION_RU.md | 17 | 1–17, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F007,F012,F035 | BigHarvest | ERR-022/033/047 |
| Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md | 14 | 1–14, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F040,F053–056 | PartialFar | ERR-007/008/022 |
| Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md | 18 | 1–18, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F010–011,F035 | FinalClose | ERR-022/036/044 |
| Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | 23 | 1–23, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F024–026,F052 | SmallTransition | ERR-035/041/045 |
| Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md | 28 | 1–28, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F027–029,F037,F047–048 | NewFar | ERR-013/019/032/039/045 |
| Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md | 24 | 1–24, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F026,F031–033,F059 | Risk/Margin | ERR-009/034/035/038 |
| Docs/16_PERSISTENCE_AND_RESTART_RU.md | 21 | 1–21, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F057,F060 | Persistence | ERR-017/030 |
| Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md | 26 | 1–26, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F057,F060 | Reconciliation | ERR-013/016/017/033 |
| Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md | 30 | 1–30, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F057,F060 | Architecture | ERR-016/017/033 |
| Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md | 434 | 1–434, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | Index,not new mathematical proof | Traceability | ERR-027/028 |
| Docs/20_TEST_STRATEGY_RU.md | 28 | 1–28, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | Historical test requirements; not executed | Test strategy | ERR-027/029 |
| Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md | 309 | 1–309, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | Readiness,not proof of all formulas | Readiness | ERR-028/029 |
| Docs/22_OPEN_DECISIONS_REGISTER_RU.md | 325 | 1–325, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | Historical decisions/index | Normative hierarchy | ERR-028 |
| Docs/23_NORMATIVE_DECISIONS_RESOLUTION_RU.md | 29 | 1–29, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | Historical 14 decisions; not R0 approvals | Normative hierarchy | ERR-028 |
| Docs/24_BROKER_MONEY_MODEL_RU.md | 21 | 1–21, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F006–009,F020–023 | BrokerMoney | ERR-022/033/043 |
| Docs/25_BROKER_GRID_AND_ROUNDING_RU.md | 17 | 1–17, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F001–004,F044,F048–049 | Grid | ERR-039/040 |
| Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md | 17 | 1–17, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F005,F039,F051 | Geometry | ERR-014/046 |
| Docs/27_CONTROL_PRICES_AND_COSTS_RU.md | 17 | 1–17, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F020–023,F037–039,F058 | Control/FutureSmall | ERR-021/024/031/037 |
| Docs/27_FUTURE_SMALL_SOLVER_RU.md | 41 | 1–41, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F020–023,F037–039,F058 | Control/FutureSmall | ERR-021/024/031/037 |
| Docs/28_NEW_FAR_SOLVER_RU.md | 39 | 1–39, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F027–029,F047,F060 | NewFar | ERR-013/019/045 |
| Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md | 37 | 1–37, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F047 | Candidate objective | ERR-019 |
| Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | 15 | 1–15, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F023 | Aggregate | ERR-018 |
| Docs/31_MONEY_PROOF_IDENTITY_RU.md | 7 | 1–7, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F017,F060 | Proof identity | ERR-013/033 |
| Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | 7 | 1–7, полностью | PRIMARY_DECLARED_NORMATIVE; historical stage limits | F015,F018–019,F057 | Reserve consumption | ERR-007/008/033 |
| Docs/HSB.2C_Execution_Intent_Spec.md | 5 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–5 |
| Docs/HSB.2C_Idempotency_and_Restart_Safety.md | 5 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–5 |
| Docs/HSB.2C_Journal_Persistence_Reconciliation.md | 7 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–7 |
| Docs/HSB.2C_Preflight_and_Lifecycle.md | 5 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–5 |
| Docs/HSB.2C_R1_Correction_Spec_RU.md | 5 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–5 |
| Docs/HSB.2C_R1_Journal_Chain_RU.md | 3 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–3 |
| Docs/HSB.2C_R1_P1_Publication_Spec_RU.md | 5 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–5 |
| Docs/HSB.2C_R1_P1_Runtime_Policy_RU.md | 13 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–13 |
| Docs/HSB.2C_R1_P1_Traceability_RU.md | 10 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–10 |
| Docs/HSB.2C_R1_P2_Include_Graph_Audit_RU.md | 15 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–15 |
| Docs/HSB.2C_R1_P2_Publication_Audit_RU.md | 3 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–3 |
| Docs/HSB.2C_R1_P2_Runtime_Policy_Canonical_RU.md | 11 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–11 |
| Docs/HSB.2C_R1_P2_Traceability_RU.md | 9 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–9 |
| Docs/HSB.2C_R1_Runtime_Mode_Policy_RU.md | 3 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–3 |
| Docs/HSB.2C_R1_Security_Invariants_RU.md | 5 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–5 |
| Docs/HSB.2C_R1_Traceability_RU.md | 10 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–10 |
| Docs/HSB.2C_Traceability.md | 13 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–13 |
| Docs/HSBI_DG01_CONTRACT_RESOLUTION_RU.md | 259 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–259 |
| Docs/HSBI_DG01_DEPENDENCY_GRAPH_RU.md | 22 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–22 |
| Docs/HSBI_DG01_MINIMAL_R1_1_DIFF_PLAN_RU.md | 33 | 1–33, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSBI_DG01_NATIVE_VERIFICATION_PLAN_RU.md | 33 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–33 |
| Docs/HSBI_DG01_P0_REMEDIATION_MATRIX_RU.md | 173 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–173 |
| Docs/HSBI_FULL_SYSTEM_AUDIT_02_ECONOMIC_CONSERVATION_RU.md | 28 | 1–28, полностью | PROPOSED/HISTORICAL; approval не установлен | F012–019,F024–026,F040–043,F053–060 | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSBI_FULL_SYSTEM_AUDIT_02_FSM_COMPARISON_RU.md | 37 | 1–37, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2D_ALLOCATION_CONSUMPTION_RUNTIME_RU.md | 3 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–3 |
| Docs/HSB_2D_PERSISTENCE_RESTART_CONTRACT_RU.md | 3 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–3 |
| Docs/HSB_2D_RUNTIME_INTEGRATION_RU.md | 5 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–5 |
| Docs/HSB_2D_TRANSACTION_BARRIER_RU.md | 3 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–3 |
| Docs/HSB_2D_V2_EXACT_TEST_PROCEDURE_RU.md | 11 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–11 |
| Docs/HSB_2D_V2_METAEDITOR_USER_VERIFICATION_RU.md | 3 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–3 |
| Docs/HSB_2D_V2_REQUIRED_EVIDENCE_CHECKLIST_RU.md | 13 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–13 |
| Docs/HSB_2E_API_CONTRACTS_R2_RU.md | 38 | 1–38, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_API_CONTRACTS_RU.md | 77 | 1–77, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_BIG_HARVEST_IMPLEMENTATION_CONTRACT_RU.md | 27 | 1–27, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_DEPENDENCY_GRAPH_RU.md | 8 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–8 |
| Docs/HSB_2E_FINAL_CLOSE_IMPLEMENTATION_CONTRACT_RU.md | 27 | 1–27, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_FORMULA_CONTRACTS_R2_RU.md | 34 | 1–34, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_FSM_TRANSITION_TABLE_RU.md | 20 | 1–20, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_FULL_TRADING_LOGIC_IMPLEMENTATION_PLAN_RU.md | 289 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–289 |
| Docs/HSB_2E_INITIAL_LOCK_IMPLEMENTATION_CONTRACT_RU.md | 27 | 1–27, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_NEW_FAR_CATCH_UP_IMPLEMENTATION_CONTRACT_RU.md | 27 | 1–27, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_PARTIAL_FAR_RESERVE_IMPLEMENTATION_CONTRACT_RU.md | 27 | 1–27, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md | 21 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–21 |
| Docs/HSB_2E_PREP_R2_ADMIN_HANDOFF_RU.md | 7 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–7 |
| Docs/HSB_2E_PREP_R3_IMPLEMENTATION_HANDOFF_RU.md | 27 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–27 |
| Docs/HSB_2E_PREP_R4_IMPLEMENTATION_HANDOFF_RU.md | 24 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–24 |
| Docs/HSB_2E_PREP_R4_R1_IMPLEMENTATION_HANDOFF_RU.md | 7 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–7 |
| Docs/HSB_2E_PREP_R4_R2_IMPLEMENTATION_HANDOFF_RU.md | 16 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–16 |
| Docs/HSB_2E_PREP_R4_R3_IMPLEMENTATION_HANDOFF_RU.md | 25 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–25 |
| Docs/HSB_2E_PREP_R4_R4_IMPLEMENTATION_HANDOFF_RU.md | 36 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–36 |
| Docs/HSB_2E_PREP_R4_R5_IMPLEMENTATION_HANDOFF_RU.md | 17 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–17 |
| Docs/HSB_2E_PREP_R4_R6_IMPLEMENTATION_HANDOFF_RU.md | 17 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–17 |
| Docs/HSB_2E_PREP_R4_R7_IMPLEMENTATION_HANDOFF_RU.md | 23 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–23 |
| Docs/HSB_2E_PREP_R4_R8_IMPLEMENTATION_HANDOFF_RU.md | 19 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–19 |
| Docs/HSB_2E_PRODUCTION_FILE_MAP_RU.md | 38 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–38 |
| Docs/HSB_2E_SCENARIO_CONTRACTS_R2_RU.md | 18 | 1–18, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_SIMULATION_FIRST_ARCHITECTURE_RU.md | 3 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–3 |
| Docs/HSB_2E_SMALL_TRANSITION_IMPLEMENTATION_CONTRACT_RU.md | 27 | 1–27, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/HSB_2E_TEST_MATRIX_RU.md | 21 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–21 |
| Docs/HSB_2E_TRANSACTION_LIFECYCLE_RU.md | 22 | 1–22, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/NEXT_STAGE_01_BASELINE_AUDIT_RU.md | 54 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–54 |
| Docs/NEXT_STAGE_02A_MONEY_INTEGRITY_AUDIT_RU.md | 257 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–257 |
| Docs/NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md | 167 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–167 |
| Docs/NEXT_STAGE_02B_R0A_MONEY_INVARIANTS_RU.md | 393 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–393 |
| Docs/NEXT_STAGE_02B_R0A_NORMATIVE_REVIEW_RU.md | 78 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–78 |
| Docs/NEXT_STAGE_02B_R0B_AUTHORITY_AND_REPLAY_CONTRACT_RU.md | 54 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–54 |
| Docs/NEXT_STAGE_02B_R0B_CONTRACT_FREEZE_PROPOSAL_RU.md | 111 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–111 |
| Docs/NEXT_STAGE_02B_R0B_FINAL_NORMATIVE_REVIEW_RU.md | 193 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–193 |
| Docs/NEXT_STAGE_02B_R0B_PRECISION_POLICY_REVIEW_RU.md | 44 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–44 |
| Docs/NEXT_STAGE_02B_R0C_NORMATIVE_AND_R1_1_ADDENDUM_RU.md | 24 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–24 |
| Docs/NEXT_STAGE_02B_R0C_ORACLE_CONTRACT_RU.md | 70 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–70 |
| Docs/NEXT_STAGE_02B_R0D_NORMATIVE_ADDENDUM_RU.md | 16 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–16 |
| Docs/NEXT_STAGE_02B_R0D_NUMERIC_CONTRACT_RU.md | 47 | 1–47, полностью | PROPOSED/HISTORICAL; approval не установлен | F012–019,F024–026,F040–043,F053–060 | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/NEXT_STAGE_02B_R0D_SNAPSHOT_IDENTITY_CONTRACT_RU.md | 24 | 1–24, полностью | PROPOSED/HISTORICAL; approval не установлен | F007–011,F017,F036,F057,F060; scope в названии | Money/Execution/FSM/Identity, по указанному contract | ERR-013/016/017/022/028/033; не все future callers существуют |
| Docs/NEXT_STAGE_02B_R0E_C1_API_SCOPE_AND_COMPOSITION_RU.md | 85 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–85 |
| Docs/NEXT_STAGE_02B_R0E_C1_CONTRACT_ADDENDUM_RU.md | 43 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–43 |
| Docs/NEXT_STAGE_02B_R0E_C2_DTO_SCHEMA_CONTRACT_RU.md | 17 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–17 |
| Docs/NEXT_STAGE_02B_R0E_C2_GUARD_COVERAGE_AND_RECOVERY_SCOPE_RU.md | 26 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–26 |
| Docs/NEXT_STAGE_02B_R0E_C3_CONTRACT_CLARIFICATIONS_RU.md | 31 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–31 |
| Docs/NEXT_STAGE_02B_R0E_C3_VERIFICATION_BOUNDARIES_RU.md | 23 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–23 |
| Docs/NEXT_STAGE_02B_R0E_CONTRACT_FREEZE_CANDIDATE_RU.md | 285 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–285 |
| Docs/NEXT_STAGE_02B_R0E_NUMERIC_ARCHITECTURE_RU.md | 38 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–38 |
| Docs/NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md | 71 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–71 |
| Docs/NEXT_STAGE_02B_R0F_DEPENDENCY_GRAPH_RU.md | 41 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–41 |
| Docs/NEXT_STAGE_02B_R0F_ECONOMIC_IDENTITY_SPEC_RU.md | 52 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–52 |
| Docs/NEXT_STAGE_02B_R0F_MONEY_CONTRACT_CANDIDATE_RU.md | 55 | 1–13,27–55;14–26 NOT_VERIFIED из-за усечения вывода | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Полная семантическая проверка14–26 не засчитана; ERR-028 |
| Docs/NEXT_STAGE_02B_R0F_NUMERIC_CODEC_OPTIONS_RU.md | 35 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–35 |
| Docs/NEXT_STAGE_02B_R0F_R1_IMPLEMENTATION_SPEC_RU.md | 48 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–48 |
| Docs/NEXT_STAGE_02B_R0G_CODEC_DECISION_RU.md | 34 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–34 |
| Docs/NEXT_STAGE_02B_R0G_MINIMAL_DIFF_PLAN_RU.md | 40 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–40 |
| Docs/NEXT_STAGE_02B_R0G_MINIMAL_IDENTITY_CONTRACT_RU.md | 55 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–55 |
| Docs/NEXT_STAGE_02B_R0G_MQL5_API_SPEC_RU.md | 43 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–43 |
| Docs/NEXT_STAGE_02B_R0H_CODEC_COMPARISON_RU.md | 22 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–22 |
| Docs/NEXT_STAGE_02B_R0H_IDENTITY_API_SPEC_RU.md | 17 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–17 |
| Docs/NEXT_STAGE_02B_R0H_MINIMAL_R1_DIFF_PLAN_RU.md | 15 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–15 |
| Docs/NEXT_STAGE_02B_R0H_NATIVE_DOMAIN_SPEC_RU.md | 15 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–15 |
| Docs/NEXT_STAGE_02B_R0_CONTRACT_FREEZE_PROPOSAL_RU.md | 72 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–72 |
| Docs/NEXT_STAGE_02B_R1_1_IMPLEMENTATION_SPEC_RU.md | 89 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–89 |
| Docs/NEXT_STAGE_02B_R1_IMPLEMENTATION_TASK_RU.md | 58 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–58 |
| Docs/NEXT_STAGE_02B_R1_PHASED_IMPLEMENTATION_PLAN_RU.md | 235 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–235 |
| Docs/NEXT_STAGE_02B_REMEDIATION_PLAN_RU.md | 86 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–86 |
| Docs/NEXT_STAGE_02_MONEY_AUDIT_RU.md | 271 | NOT_FULLY_READ; семантическое покрытие не заявлено | HISTORICAL/PROPOSED_CANDIDATE — точная приоритетность NOT_VERIFIED | NOT_REVIEWED | NOT_REVIEWED | Непроверенный остаток1–271 |

## Остальные первичные и исторические материалы

Исходное задание прочитано как текст, включая запрет исполнения и критерий PARTIAL. Историческая JSON-матрица Audit01 с49 semantic families использована только как индекс F01–F49; независимо переоценённые формулы находятся в новом каталоге. Audit02 JSON defect matrix прочитана выборочно; classification не наследована как proof. Исторические DG01/R0 отчёты и их старые tests не запускались, их полнота и exit codes не перепроверены этим этапом. Нет заявления, что вся история evidence прочитана.

## Карта чтения production source

Следующая таблица отделяет полное чтение, диапазон и непрочитанный код. Независимо от чтения все74 production файла сохранены побайтно (см. BASELINE_AND_PRESERVATION).

| Source | Lines | Read range | Scope |
|---|---|---|---|
| Hybrid_Split_Big_Independent_EA.mq5 | 44 | 1–44 | STATIC_SOURCE_ONLY |
| Include/Core/HSBI_Context.mqh | 60 | 1–60 | STATIC_SOURCE_ONLY |
| Include/Core/HSBI_Enums.mqh | 11 | 1–11 | STATIC_SOURCE_ONLY |
| Include/Core/HSBI_Identifiers.mqh | 24 | 1–24 | STATIC_SOURCE_ONLY |
| Include/Core/HSBI_Invariants.mqh | 14 | 1–14 | STATIC_SOURCE_ONLY |
| Include/Core/HSBI_ReasonCodes.mqh | 5 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Core/HSBI_Roles.mqh | 11 | 1–11 | STATIC_SOURCE_ONLY |
| Include/Core/HSBI_RuntimeMode.mqh | 7 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Core/HSBI_RuntimePolicy.mqh | 30 | 1–30 | STATIC_SOURCE_ONLY |
| Include/Core/HSBI_StateMachine.mqh | 11 | 1–11 | STATIC_SOURCE_ONLY |
| Include/Core/HSBI_StateValidator.mqh | 6 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Core/HSBI_Types.mqh | 8 | 1–8 | STATIC_SOURCE_ONLY |
| Include/Core/HSBI_Version.mqh | 12 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Diagnostics/HSBI_Diagnostics.mqh | 7 | 1–7 | STATIC_SOURCE_ONLY |
| Include/Diagnostics/HSBI_Logger.mqh | 7 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Diagnostics/HSBI_PanelModel.mqh | 6 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Execution/HSBI_ActionTypes.mqh | 8 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Execution/HSBI_EventTypes.mqh | 8 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Execution/HSBI_ExecutionIntent.mqh | 45 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Execution/HSBI_ExecutionPreflight.mqh | 49 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Execution/HSBI_ExternalOutcome.mqh | 33 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Execution/HSBI_NoTradeExecution.mqh | 9 | 1–9 | STATIC_SOURCE_ONLY |
| Include/Execution/HSBI_OwnershipGuardTypes.mqh | 17 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Execution/HSBI_TransactionTypes.mqh | 24 | 1–24 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_AllocationLedgerTypes.mqh | 11 | 1–11 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_AllocationPolicyTypes.mqh | 32 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Money/HSBI_BasketMoneyEvaluator.mqh | 29 | 1–29 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_BrokerMarginModel.mqh | 18 | 1–18 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_BrokerMoneyModel.mqh | 22 | 1–22 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_BrokerMoneyTypes.mqh | 20 | 1–20 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_CandidateMoneyEvaluator.mqh | 28 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Money/HSBI_CatchUpModel.mqh | 17 | 1–17 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_CatchUpTypes.mqh | 6 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Money/HSBI_CostModel.mqh | 20 | 1–20 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_EconomicLedgerTypes.mqh | 13 | 1–13 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_LevelMarginEvaluator.mqh | 13 | 1–13 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_LevelMoneyEvaluator.mqh | 16 | 1–16 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_MoneyProofIdentity.mqh | 30 | 1–30 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_MoneyState.mqh | 6 | 1–6 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_MoneyTypes.mqh | 10 | 1–10 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_ReserveAllocationTypes.mqh | 35 | 1–35 | STATIC_SOURCE_ONLY |
| Include/Money/HSBI_ReserveCatchUpEvaluator.mqh | 83 | 1–83 | STATIC_SOURCE_ONLY |
| Include/Persistence/HSBI_ExecutionJournal.mqh | 45 | 1–45 | STATIC_SOURCE_ONLY |
| Include/Persistence/HSBI_ExecutionStateSnapshot.mqh | 44 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Persistence/HSBI_JournalTypes.mqh | 8 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Persistence/HSBI_PersistenceInterface.mqh | 8 | 1–8 | STATIC_SOURCE_ONLY |
| Include/Persistence/HSBI_ReconciliationTypes.mqh | 8 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Persistence/HSBI_SnapshotTypes.mqh | 11 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Planning/HSBI_BrokerGrid.mqh | 38 | 1–38 | STATIC_SOURCE_ONLY |
| Include/Planning/HSBI_CandidatePlan.mqh | 9 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Planning/HSBI_ControlPrices.mqh | 25 | 1–25 | STATIC_SOURCE_ONLY |
| Include/Planning/HSBI_DecisionResult.mqh | 5 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Planning/HSBI_FutureSmallProofAggregator.mqh | 60 | 1–60 | STATIC_SOURCE_ONLY |
| Include/Planning/HSBI_FutureSmallSolver.mqh | 151 | 1–151 | STATIC_SOURCE_ONLY |
| Include/Planning/HSBI_FutureSmallTypes.mqh | 82 | 1–82 | STATIC_SOURCE_ONLY |
| Include/Planning/HSBI_GeometrySolver.mqh | 38 | 1–38 | STATIC_SOURCE_ONLY |
| Include/Planning/HSBI_GeometryTypes.mqh | 7 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Planning/HSBI_NewFarCandidate.mqh | 42 | 1–42 | STATIC_SOURCE_ONLY |
| Include/Planning/HSBI_NewFarSolver.mqh | 154 | 1–154 | STATIC_SOURCE_ONLY |
| Include/Risk/HSBI_CalculationGateTypes.mqh | 14 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh | 52 | 1–52 | STATIC_SOURCE_ONLY |
| Include/Risk/HSBI_NewFarGateTypes.mqh | 18 | 1–18 | STATIC_SOURCE_ONLY |
| Include/Risk/HSBI_RiskGateResult.mqh | 7 | 1–7 | STATIC_SOURCE_ONLY |
| Include/Risk/HSBI_RiskTypes.mqh | 5 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Runtime/HSBI_RuntimeDecisionTypes.mqh | 18 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Runtime/HSBI_RuntimeDecisionValidator.mqh | 30 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Runtime/HSBI_RuntimeRestartValidator.mqh | 18 | 1–18 | STATIC_SOURCE_ONLY |
| Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh | 19 | 1–19 | STATIC_SOURCE_ONLY |
| Include/Scenarios/HSBI_BigHarvestTypes.mqh | 5 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Scenarios/HSBI_FinalCloseTypes.mqh | 5 | 1–5 | STATIC_SOURCE_ONLY |
| Include/Scenarios/HSBI_InitialLockTypes.mqh | 5 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Scenarios/HSBI_PartialFarTypes.mqh | 5 | 1–5 | STATIC_SOURCE_ONLY |
| Include/Scenarios/HSBI_ScenarioTypes.mqh | 6 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |
| Include/Scenarios/HSBI_SmallTransitionTypes.mqh | 5 | NOT_FULLY_READ | HASH_ONLY; no semantic full-read claim |

## Незакрытая полнота

1. Прочитать85 оставшихся/частичных Docs полностью и установить approval/precedence по первичным решениям, а не по имени файла.
2. Перепроверить не полностью прочитанные production headers и полный include/caller graph; даже для прочитанных файлов полнота внешних consumers не доказана.
3. Дополнить каталог формул из этих приложений; нынешние60 — не доказательство полного enumeration всех норм.
4. Формализовать все event-level FSM combinations, включая prefix partials/restart. Нынешняя33-state карта не исчерпывает Event×State.
5. Доказать symbol/domain/cost/provider assumptions, uniform tail и terminal closure либо явно отказаться от соответствующего глобального утверждения.

Эти работы требуют дальнейшего документального прохода; тесты/компиляция здесь запрещены и не включены как якобы завершённые пункты. Native/broker/durable подтверждение возможно только в отдельно разрешённом этапе. Исторические FAIL не стирались и не превращались в fresh PASS.
