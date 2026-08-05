# ОТЧЁТ ЭТАПА 3.1.6 — НОРМАТИВНАЯ ГЕОМЕТРИЯ BIG HARVEST И SMALL TRANSITION

## Текущий статус этапа

```text
STAGE_3_1_6_STATUS=IN_PROGRESS
NEXT_ALLOWED_STAGE=NONE
STAGE_3_1_7_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
PYTHON_DEVELOPMENT_ALLOWED=NO
PRODUCTION_MQL5_CHANGED=NO
```

---

# Подэтап 3.1.6.1 — открытие этапа и проверка границ

## 1. Цель

Открыть этап 3.1.6 без изменения торговой логики, подтвердить исходное состояние ветки `work` и зафиксировать единственную разрешённую границу работ.

## 2. Исходный commit SHA

`77478b9170488ca0c4ef92da33e9e7fb6c70d748`

Сообщение исходного коммита:

`План MQL5: утверждена последовательность доведения советника до production-уровня`

## 3. Проверенные файлы и пути

Проверены исключительно объекты внутри разрешённого проекта:

- `MinusLock_BigHarvest_EA_V2/`;
- `MinusLock_BigHarvest_EA_V2/Docs/`;
- `MinusLock_BigHarvest_EA_V2/Docs/STAGE_3_1_5_FINAL_REPORT_RU.md`;
- `MinusLock_BigHarvest_EA_V2/Docs/STAGE_3_1_5_NORMATIVE_MONEY_MODEL_RU.md`;
- `MinusLock_BigHarvest_EA_V2/Docs/PROJECT_STATUS_AND_REAL_TRADING_ROADMAP_RU.md`;
- `MinusLock_BigHarvest_EA_V2/MinusLock_BigHarvest_EA.mq5`;
- `MinusLock_BigHarvest_EA_V2/Include/`.

Файлы и каталоги за пределами `MinusLock_BigHarvest_EA_V2` не использовались.

## 4. Изменённые файлы

Создан:

`MinusLock_BigHarvest_EA_V2/Docs/STAGE_3_1_6_PRODUCTION_GEOMETRY_REPORT_RU.md`

Production-файлы `.mq5` и `.mqh` не изменялись.

## 5. Результат и статус

Граница проекта, ветка и исходный HEAD подтверждены. Этап открыт без изменения production MQL5.

`PASS`

## 6. Commit SHA

`e15eeb60ac4cb65c7c7e20e569a2a88bc94a0047`

Коммит:

`Этап 3.1.6.1: открыт этап нормативной геометрии Big и Small`

---

# Подэтап 3.1.6.2 — инвентаризация всей геометрической документации

## 1. Цель

Провести повторную инвентаризацию всей документации внутри проекта, которая способна влиять на Initial Lock, Far, Big, BigCore, BigTrend, Small, SmallBase, NewFar, Big Harvest, Partial Far, FinalReserve, Final Close, Small Transition, Reverse, terminal-safe исполнение и порядок торговых операций.

Целью инвентаризации не являлось автоматическое назначение последнего по дате документа нормативным. Проверялся фактический смысл документа, его роль, поколение системы, формулы, порядок действий, денежная совместимость и способность влиять на production-сделку.

## 2. Исходный commit SHA

`e15eeb60ac4cb65c7c7e20e569a2a88bc94a0047`

## 3. Проверенная область

Проверены:

- все верхнеуровневые документы и реестры в `MinusLock_BigHarvest_EA_V2/Docs`;
- вложенные `Docs/Evidence/**/INDEX.md` как индексы доказательств;
- корневые Markdown-файлы проекта;
- только документы внутри `MinusLock_BigHarvest_EA_V2`.

Технические журналы `.log`, JSON mapping-файлы и CSV не использовались как самостоятельная production-норма. Они классифицированы как evidence, machine-readable mapping или historical data.

## 4. Метод определения нормативного приоритета

Применён следующий порядок:

1. прямое текущее задание Администратора этапа 3.1.6;
2. закрытая нормативная денежная модель этапа 3.1.5;
3. математически непротиворечивые Hybrid Split Big contracts;
4. совместимость с actual MT5 deals, positions, identifiers, persistence и reconciliation;
5. отсутствие конфликта с правилом единственного Far;
6. supporting-документы, доказательства и mapping;
7. historical, legacy, Split Big и отчётные документы;
8. Python-oracle, offline-оптимизация и прежние PASS — только историческое evidence, не production-доказательство.

Ни дата изменения файла, ни слово `FINAL`, `PASS`, `PRODUCTION` или `READINESS` в названии не создают нормативную силу автоматически.

## 5. Нормативные классы, принятые на этапе 3.1.6

| Класс | Значение | Право определять production-сделку |
|---|---|---|
| `PRIMARY_BOUNDARY` | текущее ТЗ и обязательные правила этапа 3.1.6 | Да, в пределах этапа |
| `MONEY_NORMATIVE` | денежная семантика закрытого этапа 3.1.5 | Да, для денег, identity и actual-deal semantics |
| `GEOMETRY_CANDIDATE` | Hybrid-документы, подлежащие консолидации в новый единый документ | Только после проверки и устранения конфликтов |
| `SUPPORTING` | формулы, proof, glossary, trace, mapping, test vectors | Нет самостоятельного права менять бизнес-логику |
| `REPORT` | аудит, implementation report, validation, readiness, changelog | Нет |
| `HISTORICAL` | Legacy/Split/старые baseline и миграционные материалы | Нет |
| `CONFLICTING` | содержит альтернативные роли, коэффициенты или порядок | Использование запрещено до решения |
| `OBSOLETE_FOR_PRODUCTION` | Python/offline/simulation как критерий готовности | Нет |

## 6. Главная таблица документов с наивысшим влиянием

| Документ | Статус 3.1.6 | Сценарий и роли | Формулы / порядок | Выявленный конфликт | Нормативный приоритет |
|---|---|---|---|---|---|
| `Docs/STAGE_3_1_5_NORMATIVE_MONEY_MODEL_RU.md` | `MONEY_NORMATIVE` | весь recovery-cycle; managed deals; allocation buckets | DealNet, RecoveryPLCloseNow, actual/requested, exactly-once, restart | Не определяет полную торговую геометрию | 1 для денег и identity |
| `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md` | `GEOMETRY_CANDIDATE` | Far, BigCore, BigTrend, SmallBase, NewFar, Big/Small | три закона, Catch-Up, Recovery slope, compression, Small Transition | Формулы и профили требуют согласования с execution и 3.1.5 | 2 после текущего ТЗ |
| `Docs/HYBRID_SPLIT_BIG_MQL5_NORMATIVE_ALGORITHMS_RU.md` | `GEOMETRY_CANDIDATE` | immutable state, Harvest, unified NewFar solver, Final Close | MQL5-oriented sequence, gates, ledgers, persistence | фиксированные allocation-доли и отдельные execution orders не принимаются автоматически | 2 после проверки |
| `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md` | `GEOMETRY_CANDIDATE` | Initial Lock, единственный Far, C/T/S, Harvest, Transition | SmallBase→OldFar→BigTrend→staged BigCore; actual residual Core→NewFar | содержит profiles и исторические Python-validation ссылки | 2 после фильтрации |
| `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` | `GEOMETRY_CANDIDATE` | все роли и terminal constraints | `0<NewFar<OldFar`, Reserve не участвует в Partial Far, actual≠projected | отдельные старые route-инварианты требуют сопоставления с новым единым порядком | 2 для инвариантов |
| `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md` | `GEOMETRY_CANDIDATE` | state transitions | переходы Hybrid | должен быть сверён с фактическим MQL5 mapping | 3 |
| `Docs/HYBRID_SPLIT_BIG_GATE_GRAPH.md` | `GEOMETRY_CANDIDATE` | pre-open и revalidation | порядок gate | не является execution-доказательством | 3 |
| `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md` | `SUPPORTING` | allocation flow | разрешённые денежные рёбра | подчиняется модели 3.1.5 | 3 |
| `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` | `GEOMETRY_CANDIDATE` | последовательные Harvest levels | temporal state-before/state-after | нуждается в MQL5 mapping | 3 |
| `Docs/BASKET_RISK_CONTRACT_RU.md` | `SUPPORTING_NORMATIVE_SUBSYSTEM` | basket risk, margin, worst case | risk/margin contracts | не определяет роли NewFar и полный transaction order | 3 в пределах risk |
| `Docs/MANUAL.md` | `CONFLICTING_LEGACY` | Legacy Big/Small, DUAL_TAIL | Big=Far×1.30; Small=Big×0.37; old Far может остаться | нарушает единственный Far; не имеет BigCore/BigTrend/SmallBase; Final Close без обязательного RecoveryPL gate | Запрещён как production-норма |
| `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` | `HISTORICAL_BASELINE` | старый профиль Big/Small | альтернативные ratios/shares | конфликт параметров с MANUAL и Hybrid contracts | Только история |
| `Docs/HYBRID_SPLIT_BIG_ADMIN_DECISIONS_REQUIRED.md` | `CONFLICTING` | открытые policy-варианты | альтернативные решения | сам документ не выбирает победителя | Нельзя использовать без решения |
| `Docs/DOCUMENTATION_CONFLICT_REGISTRY_RU.md` | `SUPPORTING_REGISTRY` | 45 конфликтных тем | доказательные пары документов | реестр фиксирует, но не разрешает конфликты | Высокий audit-приоритет, не бизнес-норма |
| `Docs/DOCUMENTATION_INVENTORY_AND_AUTHORITY_RU.md` | `HISTORICAL_INVENTORY` | baseline 69 Docs-файлов | предварительная классификация | прямо заявляет отсутствие единственного source of truth | Supporting baseline |

## 7. Инвентаризация семейств документации

### 7.1 Нормативные и кандидатные Hybrid-документы

| Документ | Назначение | Статус |
|---|---|---|
| `HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md` | математическое ядро трёх законов | `GEOMETRY_CANDIDATE` |
| `HYBRID_SPLIT_BIG_MQL5_NORMATIVE_ALGORITHMS_RU.md` | алгоритмический MQL5-контракт | `GEOMETRY_CANDIDATE` |
| `HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md` | полный функциональный мануал | `GEOMETRY_CANDIDATE` |
| `HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` | обязательные инварианты | `GEOMETRY_CANDIDATE` |
| `HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md` | таблица переходов | `GEOMETRY_CANDIDATE` |
| `HYBRID_SPLIT_BIG_GATE_GRAPH.md` | порядок gate | `GEOMETRY_CANDIDATE` |
| `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` | временная модель уровней | `GEOMETRY_CANDIDATE` |
| `HYBRID_SPLIT_BIG_CATCHUP_OUTCOME_TRUTH_TABLE.md` | outcome truth table | `SUPPORTING` |
| `HYBRID_SPLIT_BIG_GLOSSARY_AND_DIMENSIONS_RU.md` | словарь и размерности | `SUPPORTING` |
| `HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md` | краткий справочник формул | `SUPPORTING` |
| `HYBRID_SPLIT_BIG_MONEY_FLOW.md` | денежные рёбра | `SUPPORTING`, ниже 3.1.5 |
| `HYBRID_SPLIT_BIG_TRACE_SPEC.md` | формат trace/evidence | `SUPPORTING` |
| `HYBRID_SPLIT_BIG_TEST_VECTORS.md` | тестовые векторы | `SUPPORTING` |
| `HYBRID_SPLIT_BIG_PROGRAMMER_CHECKLIST.md` | контроль реализации | `SUPPORTING` |
| `HYBRID_SPLIT_BIG_PROOF_REPORT_RU.md` | отчёт доказательств | `REPORT` |
| `HYBRID_SPLIT_BIG_FINITE_CATCHUP_REPORT_RU.md` | отчёт finite catch-up | `REPORT` |
| `BIG_RECOVERY_IMPROVEMENT_PROOF_RU.md` | proof улучшения RecoveryPL | `SUPPORTING` |
| `BIG_RESERVE_CATCH_UP_PROOF_RU.md` | proof Reserve Catch-Up | `SUPPORTING` |

### 7.2 Mapping, gaps и вопросы

| Документ | Назначение | Статус |
|---|---|---|
| `HYBRID_SPLIT_BIG_CODE_MAPPING.md` | исторический code mapping | `SUPPORTING`, требует перепроверки 3.1.6.3 |
| `HYBRID_SPLIT_BIG_MQL5_MAPPING.md` | MQL5 mapping | `SUPPORTING`, требует перепроверки 3.1.6.3 |
| `HYBRID_SPLIT_BIG_IMPLEMENTATION_GAPS.md` | перечень gaps | `REPORT` |
| `HYBRID_SPLIT_BIG_OPEN_QUESTIONS.md` | открытые вопросы | `CONFLICTING/UNRESOLVED` |
| `HYBRID_SPLIT_BIG_ADMIN_DECISIONS_REQUIRED.md` | требуемые решения Администратора | `CONFLICTING` |
| `HYBRID_SPLIT_BIG_LOGIC_DESIGN_RU.md` | проект логики | `SUPPORTING` |
| `HYBRID_SPLIT_BIG_IMPLEMENTATION_PLAN_RU.md` | старый план реализации | `HISTORICAL` |
| `HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md` | отчёт реализации | `REPORT` |
| `HYBRID_SPLIT_BIG_VALIDATION_REPORT_RU.md` | validation report | `REPORT` |
| `HYBRID_SPLIT_BIG_METAEDITOR_COMPILE.md` | сведения о compile | `REPORT`; нельзя считать текущим compile PASS |
| `HYBRID_SPLIT_BIG_STRATEGY_TESTER_ADMIN_PLAN_RU.md` | план ручной проверки | `SUPPORTING` |

### 7.3 Python/oracle и машинные материалы

| Документ или файл | Статус | Причина |
|---|---|---|
| `HYBRID_SPLIT_BIG_ORACLE_ARCHITECTURE.md` | `OBSOLETE_FOR_PRODUCTION` | Python/oracle не заменяет MQL5 |
| `HYBRID_SPLIT_BIG_ORACLE_COVERAGE.md` | `OBSOLETE_FOR_PRODUCTION` | coverage является историческим evidence |
| `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` | `MACHINE_MAPPING` | не является читаемой production-нормой |
| `HYBRID_SPLIT_BIG_MAPPING_CANDIDATE_AUDIT.json` | `MACHINE_EVIDENCE` | audit data, не бизнес-правило |
| `Best_Parameters.md` | `HISTORICAL_OFFLINE` | прямо указывает, что MT5 не запускался |
| `Optimization_Report.csv` | `HISTORICAL_DATA` | offline-оптимизация запрещена как доказательство 3.1.6 |

### 7.4 Legacy и Split Big

| Документ | Поколение | Статус 3.1.6 |
|---|---|---|
| `Docs/MANUAL.md` | Legacy Big/Small | `CONFLICTING_LEGACY` |
| `MIGRATION_FROM_LEGACY.md` | migration | `HISTORICAL` |
| `SPLIT_GEOMETRY_MATH.md` | Split | `HISTORICAL_SUPPORTING` |
| `SPLIT_GEOMETRY_STATE_MACHINE.md` | Split | `HISTORICAL_SUPPORTING` |
| `SPLIT_GEOMETRY_TEST_PLAN.md` | Split | `HISTORICAL_TEST` |
| `TEST_PLAN_SPLIT_GEOMETRY.md` | Split | `HISTORICAL_TEST`, частично дублирует предыдущий |
| `SPLIT_BIG_ARCHITECTURE_FIX_REPORT_RU.md` | Split | `REPORT` |
| `SPLIT_BIG_EXACT_PERSISTENCE_REPORT_RU.md` | Split | `REPORT` |
| `SPLIT_BIG_FINAL_RECOVERY_SAFETY_REPORT_RU.md` | Split | `REPORT` |
| `SPLIT_BIG_FINAL_SAFETY_REPORT_RU.md` | Split | `REPORT` |
| `SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md` | Split | `REPORT` |
| `SPLIT_BIG_RECOVERY_ORDER_REPORT_RU.md` | Split | `REPORT` |
| `SPLIT_BIG_TRANSACTION_SAFETY_REPORT_RU.md` | Split | `REPORT` |
| `SPLIT_MONEY_MODEL_FINAL_REPORT_RU.md` | Split | `REPORT`, ниже 3.1.5 |
| `CHANGELOG_SPLIT_BIG.md` | Split changelog | `REPORT` |
| `CHANGELOG_SPLIT_GEOMETRY.md` | Split changelog | `REPORT` |

### 7.5 Общие аудиты и Big/Small reports

Следующие документы сохраняются как evidence/status, но не имеют права самостоятельно задавать торговую последовательность:

- `ADAPTIVE_GEOMETRY_LIFECYCLE_AUDIT.md`;
- `BIG_SCENARIO_ENGINEERING_AUDIT.md`;
- `BIG_SCENARIO_FULL_AUDIT.md`;
- `FULL_AUDIT_REPORT.md`;
- `BIG_SMALL_COMPLETION_BASELINE_RU.md`;
- `BIG_SMALL_COMPLETION_FINAL_REPORT_RU.md`;
- `BIG_SMALL_END_TO_END_FINAL_REPORT_RU.md`;
- `BIG_SMALL_FINAL_RUNTIME_VALIDATION_RU.md`;
- `BIG_SMALL_IMPLEMENTATION_FINAL_REPORT_RU.md`;
- `BIG_SMALL_PRODUCTION_READINESS_REPORT_RU.md`;
- `BIG_SMALL_VALIDATION_FINAL_REPORT_RU.md`;
- `DEAL_LEVEL_VALIDATION_BASELINE_RU.md`;
- `PERSISTENCE_AND_CLEAN_START_FINAL_REPORT_RU.md`;
- `NEXT_STAGE_BASELINE_AUDIT_RU.md`;
- `AUDIT_AFTER_REMOTE_ADVANCE_RU.md`;
- `ЗАМЕЧАНИЯ_И_ПРЕДЛОЖЕНИЯ_ПО_СОВЕТНИКУ.md`.

Статус всей группы: `REPORT` либо `HISTORICAL_REVIEW`.

### 7.6 Basket Risk

- `BASKET_RISK_CONTRACT_RU.md` — subsystem contract, применим только в пределах risk/margin;
- `BASKET_RISK_DOCUMENTATION_AUDIT_RU.md` — report;
- `BASKET_RISK_STAGE_2_0_REPORT_RU.md` — report.

Basket Risk не назначает источник NewFar, роли BigCore/BigTrend/SmallBase и transaction order Small Transition.

### 7.7 Этапные отчёты 3.1.3–3.1.5

Все `STAGE_3_1_3_*`, `STAGE_3_1_4_*`, `STAGE_3_1_5_*CORRECTION*`, `STAGE_3_1_5_TEST_REPORT_RU.md` и `STAGE_3_1_5_FINAL_REPORT_RU.md` классифицированы как `REPORT/EVIDENCE`.

Исключение по содержанию:

- `STAGE_3_1_5_NORMATIVE_MONEY_MODEL_RU.md` — действующая денежная норма;
- `STAGE_3_1_5_MQL5_MAPPING_RU.md` — supporting mapping, который должен быть перепроверен;
- `STAGE_3_1_4_THREE_LAWS_PROOF_REPORT_RU.md` — proof report, не execution contract;
- `STAGE_3_1_3_GLOSSARY_AND_DIMENSIONS_REPORT_RU.md` — supporting terminology.

### 7.8 Корневые документы проекта

| Документ | Статус | Production-влияние |
|---|---|---|
| `BUILD_INFO.md` | `HISTORICAL_CHANGELOG` | описывает версии и старые реализации, но не является единой нормой |
| `Best_Parameters.md` | `HISTORICAL_OFFLINE` | параметры не MT5-approved |
| `CHANGELOG_SPLIT_BIG.md` | `REPORT` | сам фиксирует, что Split Small не был реализован и real trading запрещён |
| `CHANGELOG_SPLIT_GEOMETRY.md` | `REPORT` | scaffold/change history |
| `MQL5_PRODUCTION_DEVELOPMENT_PLAN_RU.md` | `ROADMAP` | определяет последовательность этапов, не торговую формулу |
| `PROJECT_STATUS_AND_REAL_TRADING_ROADMAP_RU.md` | `ROADMAP/STATUS` | real trading остаётся запрещённым |

## 8. Формулы и правила, найденные в нескольких несовместимых вариантах

| Тема | Вариант A | Вариант B/Hybrid | Решение 3.1.6.2 |
|---|---|---|---|
| BigRatio | `1.30` в Legacy MANUAL | `1.15` и другие profiles | не выбирать в inventory; parameter profile conflict |
| SmallRatio | `0.37` в Legacy MANUAL | `0.25` и Hybrid SmallBase ratios | не выбирать |
| CloseBigOnSmall | `0.30` | `0.40` и staged BigCore solver | фиксированное legacy-значение не является нормой |
| ReserveShare | `0.10` | `0.80/0.90/другие profiles` | business/profile policy, не геометрическая константа |
| NewFar source | остаток Legacy Big при возможном старом Far | только actual residual BigCore после full OldFar/SmallBase/BigTrend close | второй вариант является кандидатом этапа 3.1.6 |
| Final Close | Reserve ≥ theoretical Far loss | RecoveryPLCloseNow threshold + actual-cost coverage + reconciled state | legacy-условие запрещено |
| Partial Far | theoretical money/points | только confirmed PartialFarBudget через broker money model | 3.1.5 имеет приоритет |
| RecoveryPL | возможные balance/profile approximations | unique actual managed deals + close-now open legs | 3.1.5 имеет приоритет |
| Order Small | legacy Small→часть Big, old Far может остаться | SmallBase→OldFar→BigTrend→staged BigCore | требуется окончательная норма 3.1.6.8 |

## 9. Документы, которые нельзя использовать как production-норму без дополнительного решения

Категорически нельзя напрямую использовать:

1. `Docs/MANUAL.md` — legacy roles, DUAL_TAIL и устаревший Final Close.
2. `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` — старый parameter baseline.
3. `Docs/HYBRID_SPLIT_BIG_ADMIN_DECISIONS_REQUIRED.md` — содержит нерешённые варианты.
4. `Docs/HYBRID_SPLIT_BIG_OPEN_QUESTIONS.md` — открытые вопросы.
5. Все Split Big implementation/final/readiness reports — описывают другое поколение системы.
6. Все документы Python oracle/offline optimization — не MQL5 production evidence.
7. Любой `FINAL`, `PASS` или `PRODUCTION_READINESS` report без фактического MetaEditor и MT5 evidence.
8. Любой документ, допускающий одновременно OldFar и NewFar.
9. Любой документ, разрешающий BigTrend или SmallBase стать NewFar.
10. Любой документ, включающий FinalReserve в Partial Far.
11. Любой документ, добавляющий Reserve повторно к RecoveryPL.

## 10. Ключевые расхождения и критичность

| ID 3.1.6.2 | Расхождение | Критичность | Дальнейшее действие |
|---|---|---|---|
| DOC-3162-001 | Legacy DUAL_TAIL допускает два хвоста | `P1` | нормативно запретить в 3.1.6.8/3.1.6.9 |
| DOC-3162-002 | несколько источников NewFar | `P1` | закрепить только actual BigCore residual |
| DOC-3162-003 | legacy Final Close не требует RecoveryPLCloseNow | `P1` | закрепить обязательный positive threshold |
| DOC-3162-004 | конкурирующие allocation ratios | `P1` как profile ambiguity | отделить policy inputs от invariant money semantics |
| DOC-3162-005 | Legacy/Split/Hybrid terminology смешана | `P2` | создать единый словарь HBG roles |
| DOC-3162-006 | отчёты с PASS могут быть ошибочно восприняты как MT5 evidence | `P2` | явно маркировать NOT_PROVEN |
| DOC-3162-007 | два Split test-plan документа с различиями | `P3` | оставить historical only |
| DOC-3162-008 | прошлый inventory объявлял authority предварительным до 3.1.8 | `P2` | этап 3.1.6 создаёт новую ограниченную иерархию только для production geometry |

На этом подэтапе конфликты не исправлялись в production-коде и не скрывались. Они зарегистрированы для нормативной консолидации и MQL5 mapping.

## 11. Проверенные роли

- `Far`: единственный recovery-tail; legacy dual-tail не принят.
- `BigCore`: единственный допустимый источник NewFar после подтверждённого staged close.
- `BigTrend`: harvest/transition role; не может стать Far.
- `SmallBase`: protective role; не может стать Far.
- `OldFar`: должен быть фактически закрыт до promotion NewFar.
- `NewFar`: только actual remaining position volume после deals и reconciliation.

Это пока результат документального authority-аудита. Полная норма будет записана в подэтапах 3.1.6.4–3.1.6.9.

## 12. Проверенная последовательность действий

В документации найдены три поколения последовательностей:

1. Legacy Big/Small с DUAL_TAIL — отклонено как production-норма.
2. Split Big с незавершённым Split Small — historical/report.
3. Hybrid Split Big с C/T/S и actual residual Core — принято как база для дальнейшей нормативной консолидации, но не как доказанная MQL5-реализация.

## 13. Что исправлено

- создана актуальная классификация документов для этапа 3.1.6;
- установлен приоритет денежной модели 3.1.5;
- отделены Legacy, Split и Hybrid поколения;
- зарегистрированы документы, способные опасно повлиять на production-сделку;
- исключены Python/offline PASS как production evidence;
- зафиксировано, что historical inventory 3.1.1 не является окончательным source of truth.

## 14. Что не исправлено

- production MQL5 не изменялся;
- конфликтующие коэффициенты не выбирались;
- MQL5 runtime paths не проверялись — это подэтап 3.1.6.3;
- единый нормативный документ `HYBRID_SPLIT_BIG_PRODUCTION_GEOMETRY_RU.md` ещё не завершён;
- MetaEditor и MT5 Strategy Tester не запускались;
- P1 документальные конфликты зарегистрированы, но будут закрываться нормами 3.1.6.4–3.1.6.9.

## 15. Обоснование отсутствия изменений production-кода

Подэтап 3.1.6.2 является документальной инвентаризацией. Изменение `.mq5` и `.mqh` запрещено без необходимости и здесь не требовалось.

## 16. Доказательство соблюдения границы каталога

Все прочитанные и изменённые пути начинаются с:

`MinusLock_BigHarvest_EA_V2/`

Изменён только:

`MinusLock_BigHarvest_EA_V2/Docs/STAGE_3_1_6_PRODUCTION_GEOMETRY_REPORT_RU.md`

Файлы за пределами проекта не читались и не изменялись.

## 17. Доказательство отсутствия Python-разработки

Python-файлы не создавались и не изменялись. Python tests/oracle не запускались и не использовались как критерий PASS. Python-документы классифицированы только как historical evidence.

## 18. Результат проверки

Инвентаризация завершена. Документация разделена по поколению, полномочию и риску. Определены документы-кандидаты для единой Hybrid production geometry и документы, которые запрещено использовать без дополнительного решения.

## 19. Статус

`PASS`

Статус означает PASS полноты и классификации подэтапа, но не означает разрешение документальных P1-конфликтов, готовность MQL5 или разрешение реальной торговли.

## 20. Commit SHA

Заполняется фактическим SHA отдельного коммита 3.1.6.2 после публикации.

## 21. Условие перехода

Разрешён только подэтап 3.1.6.3 — аудит текущего MQL5 mapping. Этап 3.1.7, production-ready и real trading остаются запрещёнными.

## 22. Контрольная строка

`Ожидается подтверждение пользователя для перехода к следующему этапу`
