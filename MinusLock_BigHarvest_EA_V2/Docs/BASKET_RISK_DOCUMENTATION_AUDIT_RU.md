# Этап 2.0 — аудит документации Basket Risk

Дата аудита: 2026-07-26 UTC  
Ветка: `work`  
START_SHA: `1603b8b7576b3317fd80367188e900fd955ae5bb`  
Проект: `MinusLock_BigHarvest_EA_V2`  
Статус документа: `STAGE_2_0_DOCUMENTATION_AUDIT_COMPLETE`

## 1. Метод и граница аудита

Аудит выполнен до проектирования контракта. Полностью прочитаны обязательные источники ТЗ и прямо названные ими authority-документы. Документы трактуются как нормативные только в пределах заявленной ими области. Исторический `PASS` не переносится на Basket Risk. Исходный код, тесты, workflow и `.set` не являются объектом изменения этого этапа.

Приоритет при конфликте: системные инварианты → gate/route dependency → money flow → trace → manual/formula → mapping → status/evidence. Temporal authority — `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`. Статусные отчёты не могут ослабить `MUST`.

## 2. Реестр изученных источников

Обозначения актуальности: **A** — действующий authority; **C** — действующий контекст/контракт; **S** — status/evidence; **H** — исторический материал, применимый только без конфликта с A/C.

| Путь | Назначение и актуальность | Контракты и ограничения | Статус / UNKNOWN | Влияние на Basket Risk и конфликты |
|---|---|---|---|---|
| `Docs/MANUAL.md` | Общий мануал, C/H | Legacy lifecycle, параметры, recovery, safety | MT5 остаётся внешней приёмкой | Контекст действий; новые authority имеют приоритет |
| `Docs/FULL_AUDIT_REPORT.md` | Сквозной аудит Legacy, S/H | RiskGate, OnTester, real P/L, CSV | MetaEditor/Tester required | Не переносить исторические PASS на Basket Risk |
| `Docs/BIG_SCENARIO_FULL_AUDIT.md` | Аудит Big, C/S | Big money route и ограничения модели | Runtime зависит от MT5 | Источник классификации Legacy Big |
| `Docs/BIG_SCENARIO_ENGINEERING_AUDIT.md` | Инженерный аудит Big, C/S | Execution/state risks | Synthetic trace не заменяет MT5 | Basket Risk не объявляет runtime PASS |
| `Docs/BIG_SMALL_COMPLETION_BASELINE_RU.md` | Baseline Big/Small, S | Исходные gaps | Часть пунктов superseded | Только provenance статусов |
| `Docs/BIG_SMALL_COMPLETION_FINAL_REPORT_RU.md` | Отчёт completion, S | Реализованные source-контракты | Compile/runtime не доказаны | `IMPLEMENTED` не равно `PASS` |
| `Docs/BIG_SMALL_VALIDATION_FINAL_REPORT_RU.md` | Validation report, S | Python/static validation | MQL5 NOT_RUN | Запрещает повышение статуса |
| `Docs/BIG_SMALL_END_TO_END_FINAL_REPORT_RU.md` | E2E source report, S | Связность сценариев | Терминальный E2E не подтверждён | Вход status matrix |
| `Docs/BIG_SMALL_PRODUCTION_READINESS_REPORT_RU.md` | Production status, S | Readiness gates | reconciliation PARTIAL, MT5 NOT_RUN | `REAL_TRADING_ALLOWED=NO` |
| `Docs/BIG_SMALL_FINAL_RUNTIME_VALIDATION_RU.md` | Runtime baseline, S | Harness и deal reconciliation | harness NOT_RUN; сценарии UNKNOWN | Basket Risk не закрывает UNKNOWN |
| `Docs/NEXT_STAGE_BASELINE_AUDIT_RU.md` | Текущий baseline, S | Legacy default, Split off | compile/tester NOT_RUN | Исходная точка Этапа 2.0 |
| `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md` | Полный Hybrid manual, C | Термины, три закона, Base/Worst, routes | Runtime не доказан | Семантическая база snapshot/actions |
| `Docs/HYBRID_SPLIT_BIG_LOGIC_DESIGN_RU.md` | Logic design, C | Immutable plan, decision flow | Design не равен implementation | Basket Risk — валидатор, не planner |
| `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md` | Формулы, C | Lots/money/exposure/coverage | Broker parity UNKNOWN | Не создавать дублирующую математику |
| `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` | Главный authority, A | Все `MUST`, typed outcomes | Нарушение не может быть PASS | Высший источник Basket Risk |
| `Docs/HYBRID_SPLIT_BIG_GATE_GRAPH.md` | Gate authority, A | Предшественники, route fork | Downstream после failure запрещён | Определяет место Basket Risk |
| `Docs/HYBRID_SPLIT_BIG_TRACE_SPEC.md` | Trace authority, A | Поля, порядок, fingerprint/revision | Runtime emitter не доказан | Только совместимое расширение trace |
| `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md` | Money authority, A | Buckets и запрещённые рёбра | Actual ledger runtime pending | Нельзя смешивать Reserve/Partial/Transition |
| `Docs/HYBRID_SPLIT_BIG_CODE_MAPPING.md` | Source mapping, C | Наличие и gaps | Mapping может отставать | Не является основанием менять код |
| `Docs/HYBRID_SPLIT_BIG_MQL5_MAPPING.md` | MQL5 mapping, C | Будущая интеграция типов/gates | compile отсутствует | Только терминологическая совместимость |
| `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_PLAN_RU.md` | План, H/C | Последовательность внедрения | Не все этапы закрыты | Basket Risk не выдаёт completion |
| `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_GAPS.md` | Backlog, C/S | Ledger, margin, terminal, parity gaps | Future depth и parity pending | Не маскировать gaps safe default |
| `Docs/HYBRID_SPLIT_BIG_VALIDATION_REPORT_RU.md` | Validation, S | Python/static results | MetaEditor/MT5 отсутствуют | Status matrix |
| `Docs/HYBRID_SPLIT_BIG_ORACLE_ARCHITECTURE.md` | Oracle contract, C | Независимая модель и vectors | Не MT5 emulator | Этап 2.0 Oracle не создаёт |
| `Docs/HYBRID_SPLIT_BIG_PROGRAMMER_CHECKLIST.md` | Checklist, C | Порядок реализации/проверок | Административные пункты открыты | Acceptance boundary |
| `Docs/SPLIT_GEOMETRY_MATH.md` | Split math, C | Core/Trend/Small geometry | Split Small incomplete | Вход только от готового plan |
| `Docs/SPLIT_GEOMETRY_STATE_MACHINE.md` | State model, C | Split route states | runtime pending | Basket Risk FSM не меняет |
| `Docs/BIG_RESERVE_CATCH_UP_PROOF_RU.md` | Reserve proof, C/S | Reserve catch-up assumptions | Broker runtime pending | Не переопределять reserve |
| `Docs/BIG_RECOVERY_IMPROVEMENT_PROOF_RU.md` | Recovery proof, C/S | Monotonic improvement | Условия ограничены моделью | Источник REC checks |
| `Docs/ADAPTIVE_GEOMETRY_LIFECYCLE_AUDIT.md` | Geometry lifecycle, C/S | Freeze/fallback/restart | MT5 ATR runtime pending | Freshness учитывает frozen geometry |
| `Docs/HYBRID_SPLIT_BIG_METAEDITOR_COMPILE.md` | Compile record, S | Команда приёмки | `NOT_VERIFIED` | Нельзя заявлять MQL5 PASS |
| `Docs/STAGE_1_2_4_1_EVIDENCE_RU.md` | CI evidence, S | Python/static/guard scope | broker/runtime excluded | Source evidence, не Basket Risk evidence |
| `Docs/ADMIN_STAGE_1_2_2_MT5_CHECKLIST_RU.md` | Admin checklist, S/C | Compile/run evidence | Не выполнен | Обязательный будущий gate |
| `Docs/DEAL_LEVEL_VALIDATION_BASELINE_RU.md` | Deal baseline, S/C | Actual deal verification | runtime pending | Projected≠confirmed |
| `Docs/AUDIT_AFTER_REMOTE_ADVANCE_RU.md` | Remote advance audit, S | Provenance и новые commits | Историческая точка | Не выше текущего HEAD |
| `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` | Temporal authority, A | StateBefore/After, route state, dimensions | MQL5 parity pending | Immutable sequential Basket snapshot |
| `Docs/HYBRID_SPLIT_BIG_CATCHUP_OUTCOME_TRUTH_TABLE.md` | Outcome authority, A | Base/Worst aggregation | Runtime runner pending | ERROR/TERMINAL dominance |
| `Docs/HYBRID_SPLIT_BIG_MQL5_NORMATIVE_ALGORITHMS_RU.md` | Нормативные алгоритмы, C/A | State/Harvest/Risk/NewFar/ledger | Staged implementation | Запрещает альтернативный planner |
| `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md` | Transition authority, C/A | Допустимый порядок Small route | Runtime pending | Порядок действий неизменяем |
| `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md` | Three Laws math, C/A | Laws 1–3 и strict bounds | Broker parity pending | Basket Risk только проверяет результат |
| `Docs/HYBRID_SPLIT_BIG_ADMIN_DECISIONS_REQUIRED.md` | Решения администратора, C/S | Незакрытые policy decisions | Часть решений открыта | UNKNOWN не превращается в implicit default |
| `Docs/TEST_PLAN.md` | Общий test plan, C/S | MetaEditor/Tester acceptance | Не исполнен полностью | Будущий план доказательства |
| `BUILD_INFO.md` | История build, H/S | Эволюция safety/source | Не runtime evidence | Ниже актуальных authority/status docs |

## 3. Матрица действующих системных правил

Источник формулировок — `HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; route/dimension детализация — gate graph и temporal authority. Формулировки ниже сохраняют исходный смысл.

| ID | Существующее правило | Влияние на Basket Risk | Нельзя нарушать |
|---|---|---|---|
| GEO-01 | `0 < NewFar < OldFar` | Проверить уже рассчитанный plan | Не исправлять NewFar |
| GEO-02 | NextCore+NextTrend строго ниже лимита OldFar | Проверить strict inequality | Равенство не PASS |
| GEO-03 | Strict: Core больше Trend и Small | Проверить profile-specific plan | Не менять lots |
| GEO-04 | После rounding повторить все downstream gates | Принимать только rechecked plan | Не доверять pre-round PASS |
| GEO-05 | Core/Trend/NewFar DOWN, Small UP | Проверить provenance normalization | Не перенормировать |
| MONEY-01 | Reserve неотрицателен; debit только confirmed Final Far Close | Проверить bucket history | Preview не debit |
| MONEY-02 | Partial не финансирует Final/Transition/margin/opens | Проверить forbidden edges | Не взаимозачитывать |
| MONEY-03 | Transition не финансирует opens и не получает Reserve | Проверить lineage | Не объединять buckets |
| MONEY-04 | PartialAdd+ReserveAdd+CarryAdd=EligibleHarvest | Проверить conservation в money tolerance | Не скрывать residual |
| MONEY-05 | Negative Harvest не создаёт credits | Reject invalid allocation | Не clamp с PASS |
| MONEY-06 | Reserve уже в RealizedCyclePL | Раздельно показывать recovery и reserve | Не double count |
| MONEY-07 | Opening+confirmed credits−confirmed debits=closing | Проверить ledger equation | Только confirmed entries |
| LOGIC-01 | Snapshot immutable; fingerprint mismatch=stale | Freshness gate | Никакого silent refresh |
| LOGIC-02 | Persisted CandidatePlan immutable | Basket Risk read-only | Execution plan не мутирует |
| LOGIC-03 | Ledger event idempotent, один commit outcome | Проверить event identity | Нет повторного начисления |
| LOGIC-04 | Роли: Symbol+Magic+CycleID+identifier | Изолировать cycle/account aggregation | Комментарий недостаточен |
| LOGIC-05 | Projected не заменяет actual | Разделить projected/confirmed | Preview не success |
| LOGIC-06 | Partial/reject → reconciliation до open | Typed reconciliation outcome | Продолжение open запрещено |
| REC-01 | ReserveAfter не уменьшается в level model | Проверить последовательность | Market-free decrease запрещён |
| REC-02 | CoverageDeficit не ухудшается без provenance | Проверить Base/Worst delta | Внутренняя math не оправдание |
| REC-03 | RecoveryPL не ухудшается от double count/rounding | Проверить provenance costs | Не округлять в пользу PASS |
| SAFE-01 | Base PASS без Worst PASS не разрешает action | Агрегировать только согласованные профили | Base-only PASS запрещён |
| SAFE-02 | Terminal запрещает opens/promotion/Reserve transfer | Возвратить TERMINAL | Safe default не открывает |
| TIME-01 | Закрытая позиция не обрабатывается повторно | Проверить ConfirmedState | Нет duplicate close |
| TIME-02 | Harvest использует StateBefore текущего level | Snapshot level-bound | Нет данных соседних уровней |
| TIME-03 | Next StateBefore только из предыдущего StateAfter | Проверить temporal chain | Нельзя пропускать state |
| TIME-04 | Cumulative Harvest — непересекающиеся deals | Exactly-once aggregation | Нет повторного deal |
| TIME-05 | Trigger строится от anchor нового state | Проверить готовый plan | Не пересчитывать trigger |
| TIME-06 | Base/Worst имеют независимые states/fingerprints | Два snapshot-профиля | Не смешивать |
| FAR-01 | PartialFarNet входит в RealizedCyclePL | Учитывать один раз | Не вычитать/добавлять повторно |
| FAR-02 | Consumption равно Far loss в tolerance | Проверить projected/actual отдельно | Не смешивать статусы |
| FAR-03 | Reserve не входит в partial solver | Проверить input lineage | Forbidden edge |
| FAR-04 | Residual Far 0 либо ≥ VolumeMin | Reject dust continuation | Не создавать invalid Far |
| FAR-05 | Следующие legs от residual Far | Проверить dependency | Не использовать OldFar |
| FAR-06 | Close cost пересчитывается после partial | Новый snapshot после actual | Старый forecast stale |
| FAR-07 | Full Far → Final Close preview | Route typed outcome | Не partial completion |
| ACC-01 | HarvestNet exactly once | Event-key audit | Нет duplicate credit |
| ACC-02 | PartialFarNet exactly once | Event-key audit | Нет duplicate debit/net |
| ACC-03 | Open commission leg exactly once | Проверить cost lineage | Нет omission/double count |
| ACC-04 | Partial conservation каждый level | Проверить level equation | Не переносить deficit молча |
| ACC-05 | Allocation conservation каждый level | Проверить level equation | Не терять residual |
| OUTCOME-01 | Route outcome calculation-valid, не error | Сохранить route как valid typed result | Route не PASS execution |
| OUTCOME-02 | FINITE_PASS требует Base+Worst FINITE_PASS | Согласие обязательно | Mixed не PASS |
| OUTCOME-03 | ERROR/TERMINAL доминируют | Агрегация с доминированием | Не понижать severity |
| OUTCOME-04 | ReasonCode stable typed | Каталог, не free text | Текст только detail |
| WORST-01 | Worst shock не меняет Base spread | Независимые входы | Не мутировать Base |
| WORST-02 | При non-cumulative shock один раз/level | Проверить provenance | Не накапливать скрыто |
| WORST-03 | Worst net не лучше Base без provenance | Reject divergence | Не принимать optimistic Worst |
| MARGIN-01 | Control price = current market side | Проверить margin input | Не historical price |
| MARGIN-02 | OpenPrice не auto control price | Проверить provenance | Нет подмены |
| MARGIN-03 | Released upper ≠ actual release | Оставить projected field | Не confirmed balance |
| MARGIN-04 | PASS использует conservative state-after upper | Проверить steady/peak/overlap | Не только final state |
| ROUTE-INV-01…10 | Final route сохраняет полный Far, нулевой partial consumption и запрещает next-basket calculations | Отдельный Final Preview outcome | Не объявлять cycle success |
| ROUTE-VALID-01…08 | Route state имеет обязательную форму и calculation-valid semantics | Проверить complete route snapshot | Invalid shape → ERROR |
| ROUTE-FP-01 | Route привязан к profile fingerprint | Freshness для route | Mismatch → STALE |
| ROUTE-REV-01 | Route привязан к revision | Проверить revision перед execution | Старый revision запрещён |
| ROUTE-TOL-01…06 | Route сравнения используют типизированные tolerance | Проверить размерность каждого compare | Нет cross-dimension tolerance |
| DIM-INV-01…10 | Money/lot/price/ratio/percent/points не смешиваются; strict bounds остаются strict | Dimension metadata и conservative comparisons | Нет округления raw money до gate |

## 4. Матрица статусов

`PASS` ниже применяется только в явно доказанном слое. `NOT_RUN`, `PARTIAL`, `UNKNOWN` и `READY_FOR_COMPILE` не повышаются.

| Подсистема | Основной документ | Source | Python/static | MQL5 compile | MT5 runtime | Итог |
|---|---|---|---|---|---|---|
| Legacy Big | `FULL_AUDIT_REPORT.md` | implemented | PASS historical/static | NOT_RUN current HEAD | NOT_RUN | MT5 validation required |
| Split Big | production readiness | implemented | PASS | NOT_RUN | UNKNOWN | controlled testing only |
| Hybrid Split Big | validation report | staged/partial | PASS scoped | NOT_RUN | NOT_RUN | not ready |
| Catch-Up | Stage evidence | source implemented | 186 scoped / 391 all PASS | runner NOT_RUN | NOT_RUN | Python/static only |
| Final Close route | temporal model/evidence | source contract present | PASS scoped | NOT_RUN | UNKNOWN | preview contract only |
| Partial Far | money flow/status reports | implemented | PASS scoped | NOT_RUN | UNKNOWN | actual runtime unproved |
| Reserve ledger | production readiness | implemented | PASS scoped | NOT_RUN | UNKNOWN | broker reconciliation unproved |
| Harvest exactly-once | runtime validation | PARTIAL/implemented | PASS models | NOT_RUN | UNKNOWN | not runtime PASS |
| Small five-leg contract | runtime validation | implemented | PASS models | harness ready, NOT_RUN | UNKNOWN | not runtime PASS |
| Small post-trade reconciliation | production readiness | PARTIAL | partial/model checks | NOT_RUN | NOT_RUN | PARTIAL |
| Persistence/restart | reports | implemented | PASS models | NOT_RUN | UNKNOWN | crash recovery unproved |
| Money model | money baseline | implemented | PASS models | NOT_RUN | broker UNKNOWN | not broker-confirmed |
| Base/Worst | invariant/evidence | source present | PASS oracle/static | NOT_RUN | NOT_RUN | parity pending |
| Margin | invariants/gaps | partial adapter | PASS scoped | NOT_RUN | broker UNKNOWN | conservative basket proof pending |
| Strategy Tester | test plan | n/a | n/a | n/a | NOT_RUN | NOT_RUN |
| Real trading | baseline/readiness | disabled default | n/a | NOT_RUN | NOT_RUN | `REAL_TRADING_ALLOWED=NO` |
| Basket Risk | настоящий этап | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_RUN | NOT_RUN | documentation only |

## 5. Обнаруженные противоречия и разрешение

1. **Исторические PASS против текущего NOT_RUN.** Решение: PASS ограничен source/Python; текущие compile/runtime статусы остаются NOT_RUN.
2. **Legacy называется production default, но production ready не доказан.** Решение: `default` означает выбранный конфигурационный путь, а не разрешение real trading.
3. **Implementation reports используют `implemented`, readiness — `partial/not compiled`.** Решение: implementation — наличие source; acceptance требует отдельного compile/runtime evidence.
4. **Offline/математические рекомендации против MT5 divergence.** Решение: MT5 является будущим source of truth; кандидаты не считаются рабочими.
5. **Некоторые mapping-документы описывают будущую полную архитектуру, gaps фиксирует отсутствие частей.** Решение: gaps/status имеют приоритет для факта реализации, invariants — для нормы.
6. **Final Close может быть calculation-valid route, но не cycle success.** Решение: `FINAL_CLOSE_PREVIEW_REQUIRED`; успех только после confirmed execution и reconciliation.
7. **Reserve выглядит отдельной суммой, но уже классифицирован внутри RealizedCyclePL.** Решение: раздельное отображение без сложения.

## 6. Оставшиеся UNKNOWN

- Точные числовые лимиты Cycle Basket Risk и Account Basket Risk — предмет Этапа 2.1 после approval.
- Broker-specific margin upper bound, commission, swap, slippage и fill semantics.
- MetaEditor compilation текущего HEAD и MQL5 fixture parity.
- Strategy Tester для Legacy/Split/Hybrid и взаимодействия Big/Small.
- Полная actual reconciliation пяти Small deals и crash recovery каждой фазы.
- Политика recursive Future Small глубже depth-1.
- Runtime serialization/fingerprint parity будущих Basket Risk fields.
- Административное утверждение контракта: `BASKET_RISK_CONTRACT_APPROVED` не установлено.

## 7. Заключение аудита

Аудит подтверждает возможность определить Basket Risk только как read-only защитный слой над calculation-valid immutable plan после существующих обязательных gates. Ни один изученный источник не разрешает Basket Risk строить геометрию, перераспределять деньги, заменять margin/risk gates или считать preview фактом.

```text
STAGE_2_0_DOCUMENTATION_AUDIT_COMPLETE
BASKET_RISK_CODE=NOT_IMPLEMENTED
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
REAL_TRADING_ALLOWED=NO
```
