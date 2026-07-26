# Этап 2.0 — отчёт нормативной спецификации Basket Risk

## 1. Идентификация

```text
START_SHA=1603b8b7576b3317fd80367188e900fd955ae5bb
END_SHA=FINAL_REPORT_COMMIT (точный SHA фиксируется внешним git log после создания этого документа; self-reference SHA внутри собственного commit математически невозможен)
CONTRACT_CONTENT_SHA=eeb73278fdad3851c5352132eff3a361c527a606
BRANCH=work
REMOTE_NAME=origin
REMOTE_URL=https://github.com/ic8812825-maker/chatgpt.com-codex.git
START_DATE_UTC=2026-07-26T15:34:55Z
PROJECT_FILE_COUNT_AT_START=468
WORKTREE_AT_START=CLEAN
```

Подготовка выполнена через `git status`, `git branch --show-current`, `git remote -v`, `git fetch origin`, `git pull --ff-only origin work`, `git rev-parse HEAD`. Отсутствовавшая локальная запись `origin` была восстановлена на обязательный URL до fetch/pull; tracked-файлы при этом не менялись.

## 2. Изученные документы

Полный реестр с назначением, актуальностью, контрактами, ограничениями, статусами, UNKNOWN и конфликтами находится в `BASKET_RISK_DOCUMENTATION_AUDIT_RU.md`. Прочитаны полностью:

1. `Docs/MANUAL.md`
2. `Docs/FULL_AUDIT_REPORT.md`
3. `Docs/BIG_SCENARIO_FULL_AUDIT.md`
4. `Docs/BIG_SCENARIO_ENGINEERING_AUDIT.md`
5. `Docs/BIG_SMALL_COMPLETION_BASELINE_RU.md`
6. `Docs/BIG_SMALL_COMPLETION_FINAL_REPORT_RU.md`
7. `Docs/BIG_SMALL_VALIDATION_FINAL_REPORT_RU.md`
8. `Docs/BIG_SMALL_END_TO_END_FINAL_REPORT_RU.md`
9. `Docs/BIG_SMALL_PRODUCTION_READINESS_REPORT_RU.md`
10. `Docs/BIG_SMALL_FINAL_RUNTIME_VALIDATION_RU.md`
11. `Docs/NEXT_STAGE_BASELINE_AUDIT_RU.md`
12. `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`
13. `Docs/HYBRID_SPLIT_BIG_LOGIC_DESIGN_RU.md`
14. `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`
15. `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
16. `Docs/HYBRID_SPLIT_BIG_GATE_GRAPH.md`
17. `Docs/HYBRID_SPLIT_BIG_TRACE_SPEC.md`
18. `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
19. `Docs/HYBRID_SPLIT_BIG_CODE_MAPPING.md`
20. `Docs/HYBRID_SPLIT_BIG_MQL5_MAPPING.md`
21. `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_PLAN_RU.md`
22. `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_GAPS.md`
23. `Docs/HYBRID_SPLIT_BIG_VALIDATION_REPORT_RU.md`
24. `Docs/HYBRID_SPLIT_BIG_ORACLE_ARCHITECTURE.md`
25. `Docs/HYBRID_SPLIT_BIG_PROGRAMMER_CHECKLIST.md`
26. `Docs/SPLIT_GEOMETRY_MATH.md`
27. `Docs/SPLIT_GEOMETRY_STATE_MACHINE.md`
28. `Docs/BIG_RESERVE_CATCH_UP_PROOF_RU.md`
29. `Docs/BIG_RECOVERY_IMPROVEMENT_PROOF_RU.md`
30. `Docs/ADAPTIVE_GEOMETRY_LIFECYCLE_AUDIT.md`
31. `Docs/HYBRID_SPLIT_BIG_METAEDITOR_COMPILE.md`
32. `Docs/STAGE_1_2_4_1_EVIDENCE_RU.md`
33. `Docs/ADMIN_STAGE_1_2_2_MT5_CHECKLIST_RU.md`
34. `Docs/DEAL_LEVEL_VALIDATION_BASELINE_RU.md`
35. `Docs/AUDIT_AFTER_REMOTE_ADVANCE_RU.md`
36. `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
37. `Docs/HYBRID_SPLIT_BIG_CATCHUP_OUTCOME_TRUTH_TABLE.md`
38. `Docs/HYBRID_SPLIT_BIG_MQL5_NORMATIVE_ALGORITHMS_RU.md`
39. `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
40. `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`
41. `Docs/HYBRID_SPLIT_BIG_ADMIN_DECISIONS_REQUIRED.md`
42. `Docs/TEST_PLAN.md`
43. `BUILD_INFO.md`

## 3. Созданные файлы

```text
Docs/BASKET_RISK_DOCUMENTATION_AUDIT_RU.md
Docs/BASKET_RISK_CONTRACT_RU.md
Docs/BASKET_RISK_STAGE_2_0_REPORT_RU.md
```

Иные tracked-файлы не изменены.

## 4. Коммиты

| SHA | Русское сообщение | Пункт |
|---|---|---|
| `343307c` | Этап 2.0: зафиксирован аудит документации Basket Risk | Реестр, invariant/status matrices, contradictions |
| `2530cfa` | Этап 2.0: определена нормативная иерархия Basket Risk | Sources/priority/conflict resolution |
| `403ce68` | Этап 2.0: определено место Basket Risk в графе gates | Gate location/dependencies |
| `7e69ba3` | Этап 2.0: определена граница Basket Risk и существующей логики | Read-only boundary/routes |
| `fb5bda0` | Этап 2.0: закреплена совместимость Basket Risk с денежными корзинами | Buckets/forbidden edges |
| `bbea55d` | Этап 2.0: определён immutable snapshot Basket Risk | Identity/positions/money/margin/freeze |
| `1dac900` | Этап 2.0: определены профили Base и Worst для Basket Risk | Independent profiles/outcome aggregation |
| `83e56b1` | Этап 2.0: определены действия и маршруты Basket Risk | Initial/Legacy/Hybrid/Final routes |
| `6ffd808` | Этап 2.0: определены typed outcomes и ReasonCode Basket Risk | Typed decision flags/reason catalog |
| `3cb817f` | Этап 2.0: определены Cycle Risk и Account Risk | Metrics, namespaces, conjunction |
| `24682fc` | Этап 2.0: определены margin и Final Close контракты Basket Risk | Conservative margin/route fork |
| `94d8b4b` | Этап 2.0: определены размерности и граничные сравнения Basket Risk | Typed tolerances/strict bounds |
| `864fa19` | Этап 2.0: определены partial execution и reconciliation | Partial taxonomy/rebuild snapshot |
| `d19f008` | Этап 2.0: определены exactly-once и trace contracts Basket Risk | EventKey/trace extension |
| `eeb7327` | Этап 2.0: добавлена таблица совместимости Basket Risk | Gate matrix/forbidden interpretations |
| `FINAL_REPORT_COMMIT` | Этап 2.0: подготовлен итоговый отчёт нормативной спецификации | Настоящий отчёт |

## 5. GitHub Actions

После обычного push `1603b8b..eeb7327` в `origin/work` зафиксированы runs:

| Workflow | Run ID | Head | Наблюдаемый результат |
|---|---:|---|---|
| Stage 1.2.4.1 Source Validation | `30208795956` | `eeb7327` | `completed/success` |
| Excel Formula Cycle Check | `30208795944` | `eeb7327` | `completed/success` |
| Lyapunov Audit CI | `30208795980` | `eeb7327` | `in_progress` на момент подготовки отчёта; финальная проверка после push report commit обязательна |

Workflow статусы проверены через GitHub Actions REST API, поскольку `gh` отсутствует в контейнере. Report commit создаёт новый workflow cycle; его окончательный статус не может быть записан внутрь того же commit без бесконечного evidence loop и сообщается внешне.

## 6. Diff до report commit

```text
Docs/BASKET_RISK_CONTRACT_RU.md            | 571 insertions
Docs/BASKET_RISK_DOCUMENTATION_AUDIT_RU.md | 185 insertions
2 files changed, 756 insertions(+)
```

После report commit changed filenames должны быть ровно тремя файлами из раздела 3.

## 7. Неизменённые запрещённые области

```text
MQL5_CHANGED=NO
INCLUDE_MQH_CHANGED=NO
PYTHON_CHANGED=NO
TESTS_CHANGED=NO
TOOLS_CHANGED=NO
WORKFLOWS_CHANGED=NO
SETS_CHANGED=NO
DEFAULTS_CHANGED=NO
STATE_MACHINE_CHANGED=NO
TRADE_ENGINE_CHANGED=NO
ALLOW_REAL_TRADING_DEFAULT=false (не изменялся)
```

## 8. Противоречия и решения

1. Historical source/static PASS против current MetaEditor/MT5 NOT_RUN: PASS ограничен своим слоем.
2. «Production default» Legacy против `REAL_TRADING_ALLOWED=NO`: default означает route selection, не readiness.
3. `implemented` против `PARTIAL/NOT_COMPILED`: source presence не является acceptance.
4. Offline optimizer result против MT5 divergence: MT5 остаётся будущим source of truth.
5. Mapping полного design против implementation gaps: invariant задаёт норму, gaps/status — факт готовности.
6. Calculation-valid Final route против cycle success: route заканчивается preview; success только actual+zero positions+reconciliation.
7. Reserve как отдельный bucket против включения в RealizedCyclePL: показывать отдельно, не складывать повторно.
8. END_SHA внутри собственного commit: используется символический `FINAL_REPORT_COMMIT`, точный immutable SHA сообщается внешним `git log`.

## 9. Оставшиеся UNKNOWN

- Числовые Cycle/Account formulas, thresholds и RiskScore до Этапа 2.1/approval.
- Broker-specific margin/commission/swap/slippage/fill parity.
- MetaEditor compile, MQL5 fixtures и Strategy Tester текущего итогового HEAD.
- Big/Small/interaction runtime status и full five-deal post-trade reconciliation.
- Crash recovery каждой execution phase.
- Recursive Future Small > depth-1.
- Runtime serialization/fingerprint parity новых trace fields.
- Contract approval; `BASKET_RISK_CONTRACT_APPROVED` не установлен.

## 10. Итоговые статусы

```text
STAGE_2_0_DOCUMENTATION_AUDIT_COMPLETE
BASKET_RISK_CONTRACT_READY_FOR_REVIEW
BASKET_RISK_EXISTING_INVARIANT_COMPATIBILITY_DOCUMENTED

BASKET_RISK_CONTRACT_APPROVED=NO
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
BASKET_RISK_CODE=NOT_IMPLEMENTED
PYTHON_ORACLE_IMPLEMENTED=NO
MQL5_INTEGRATION=NO
STATE_MACHINE_INTEGRATION=NOT_IMPLEMENTED
REAL_TRADING_ALLOWED=NO
```

```text
DOCUMENTATION-BASED BASKET RISK CONTRACT CREATED
EXISTING SYSTEM INVARIANTS PRESERVED
EXISTING GATE ORDER PRESERVED
EXISTING MONEY FLOW PRESERVED
EXISTING FINAL CLOSE ROUTE PRESERVED
EXISTING BASE/WORST MODEL PRESERVED
EXISTING DIMENSION CONTRACT PRESERVED
EXISTING TRACE CONTRACT EXTENDED, NOT REPLACED
```
