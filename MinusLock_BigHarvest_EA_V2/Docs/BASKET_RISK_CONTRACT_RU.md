# Basket Risk — нормативный контракт Этапа 2.0

Статус: `BASKET_RISK_CONTRACT_READY_FOR_REVIEW`  
Тип результата: только документация; код и интеграция отсутствуют.  
Область: `MinusLock_BigHarvest_EA_V2`, ветка `work`.

## 1. Нормативные слова

`MUST`/«обязан» — безусловное требование; `MUST NOT`/«запрещено» — безусловный запрет; `MAY` — допустимый вариант, который не ослабляет `MUST`. Failed invariant никогда не становится PASS через fallback.

Basket Risk — не торговая система и не planner. Это read-only дополнительный защитный слой, который получает уже построенный immutable plan, проверяет его и возвращает typed decision. Он не создаёт прибыль, позиции, геометрию или маршрут.

## 2. Нормативная иерархия

| Приоритет | Authority | Обязательное применение |
|---:|---|---|
| 1 | `HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` | Все `MUST`; failure → REJECT/ERROR/TERMINAL/RECONCILIATION_REQUIRED |
| 2 | `HYBRID_SPLIT_BIG_GATE_GRAPH.md` | Gate/route dependency, short-circuit, Final Close fork |
| 3 | `HYBRID_SPLIT_BIG_MONEY_FLOW.md` | Buckets, conservation, forbidden money edges |
| 4 | `HYBRID_SPLIT_BIG_TRACE_SPEC.md` | Identity, fixed trace contract, fingerprint/revision |
| 5 | complete manual и formula reference | Термины, формулы и смысл profiles/actions |
| 6 | code/MQL5 mapping | Сопоставление будущей реализации без изменения нормы |
| 7 | status/evidence reports | Только доказанность: PASS/PARTIAL/UNKNOWN/NOT_RUN |

Temporal authority: `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`. Агрегация outcomes: `HYBRID_SPLIT_BIG_CATCHUP_OUTCOME_TRUTH_TABLE.md`. State order: `HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md` и normative algorithms.

### 2.1. Разрешение конфликтов

1. Более высокий authority побеждает более низкий.
2. Более новый status report уточняет доказанность, но не меняет invariant.
3. `implemented` означает наличие source, не compile/runtime PASS.
4. Calculation-valid route не равен execution success.
5. При неоднозначности применяется безопасный typed reject/manual outcome, но failed invariant не объявляется PASS.
6. Неразрешённая неоднозначность фиксируется `BASKET_RISK_ERROR` или `BASKET_RISK_RECONCILIATION_REQUIRED`, а не скрытым default.

## 3. Термины и соответствие существующей системе

| Термин Basket Risk | Существующий термин/источник | Нормативный смысл |
|---|---|---|
| Candidate Risk | существующий `RISK` gate | Проверка риска одного готового candidate; не заменяется |
| Existing Margin | существующий `MARGIN` gate | BrokerMoney/conservative margin candidate; не заменяется |
| Cycle Basket Risk | новый будущий слой | Aggregate только активного Symbol+Magic+CycleID |
| Account Basket Risk | новый будущий слой | Account-wide managed exposure после Cycle PASS |
| Execution Freshness | fingerprint/revision contract | Повторная identity/state/price/plan проверка перед TradeEngine |
| Post-Execution Reconciliation | LOGIC-05/06 | Подтверждение actual result и новый snapshot |

## 4. Статусная граница

Настоящий контракт не устанавливает числовую математику Этапа 2.1 и не является approval. Он не повышает существующие статусы.

```text
BASKET_RISK_CONTRACT_APPROVED=NO
BASKET_RISK_CODE=NOT_IMPLEMENTED
PYTHON_ORACLE_IMPLEMENTED=NO
MQL5_INTEGRATION=NO
STATE_MACHINE_INTEGRATION=NOT_IMPLEMENTED
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
REAL_TRADING_ALLOWED=NO
```

## 5. Место в gate graph

Существующий граф сохраняется без перестановки:

```text
IDENTITY → CONFIGURATION → VOLUME → ROUNDING → VOLUME_RECHECK
→ GEOMETRY → BASE_MONEY → FINITE_CATCHUP → TRANSITION → NEW_FAR
→ RISK → MARGIN → WORST_CASE → FUTURE_SMALL
→ FINAL_CLOSE_PREVIEW → FINAL_DECISION
```

Basket Risk концептуально расширяет разрешающий контур только после получения calculation-valid CandidatePlan и согласованных Base/Worst результатов:

```text
existing predecessors PASS
→ CandidatePlan calculation-valid and frozen
→ existing Candidate RISK PASS
→ existing MARGIN PASS
→ Base/Worst agreement
→ Cycle Basket Risk
→ Account Basket Risk
→ final typed Basket Risk decision
→ Execution Freshness Gate
→ TradeEngine
→ confirmed TradeTransaction/deals
→ Post-Execution Reconciliation Gate
→ new snapshot or terminal result
```

`FINAL_CLOSE_PREVIEW` остаётся route fork существующего графа. Для Final route Basket Risk возвращает разрешение preview/risk-reducing execution, а не continuation нового basket и не cycle success.

### 5.1. Predecessor contract

Basket Risk имеет `CalculationValid=false` и не выполняет собственные Cycle/Account checks, если не прошёл хотя бы один из: identity, configuration, volume, rounding recheck, geometry, Base/Worst consistency, обязательный existing Risk/Margin gate; либо predecessor вернул ERROR, state terminal, plan не calculation-valid.

Первый failed predecessor определяет ReasonCode. Все downstream-поля получают `Evaluated=false`, а не ложный `Passed=false/true`. Basket Risk не может повторно вычислить predecessor, исправить его вход или разрешить downstream после failure.

### 5.2. Gate responsibilities

| Gate | Ответственность | Basket Risk relationship |
|---|---|---|
| Existing Candidate Risk | Риск готового candidate по существующим laws/limits | Обязательный predecessor, не дублируется |
| Existing Margin | Margin конкретного candidate/маршрута | Обязательный predecessor, не заменяется account aggregation |
| Cycle Basket Risk | Совокупность legs/buckets активного recovery cycle | Новый additive restrictive gate |
| Account Basket Risk | Совокупность managed cycles и account state | Новый additive restrictive gate |
| Execution Freshness | Неизменность identity/revision/fingerprint/state/prices | Обязательный recheck непосредственно перед execution |
| Reconciliation | Actual positions/deals/ledger после execution | Обязателен до следующего open при partial/reject/mismatch |

## 6. Граница ответственности и read-only contract

### 6.1. Разрешено

Basket Risk MUST:

- принять immutable `StateBefore`, `CandidatePlan`, `RouteState`, Base/Worst profiles, fingerprint и revision;
- проверить готовые значения по существующим invariants;
- вычислить в будущем только отдельно утверждённые Cycle/Account aggregate risk metrics без изменения исходного plan;
- вернуть typed outcome и первый typed ReasonCode;
- сохранить provenance каждого input/output;
- short-circuit при predecessor failure;
- различать forecast и confirmed actual.

### 6.2. Запрещено

Basket Risk MUST NOT:

- рассчитывать или выбирать Core, Trend, Small, NewFar, Reverse geometry или next trigger;
- менять `MinimumSafeNewFar`, `TargetNewFarRatio`, `MaximumNewBigToOldFarRatio`;
- менять normalized lots либо повторять rounding с иным результатом;
- распределять Harvest или перемещать деньги между buckets;
- использовать FinalReserve в Partial Far/Transition/margin/opens;
- менять CandidatePlan, RouteState, profile, revision или fingerprint;
- строить Next Basket на Final Close route;
- считать Final Close preview подтверждённым close;
- ослаблять strict bound или law при отсутствии safe candidate;
- вызывать TradeEngine, StateMachine либо ledger commit на Этапе 2.0.

Отсутствие безопасного candidate означает `SAFE_REJECTED`, no-trade/manual-safe typed outcome либо более сильный ERROR/TERMINAL; это не разрешение изменить закон.

### 6.3. Route classification

- **Risk-increasing:** любой open, следующий Big basket, Reverse/Future Small open, рост gross или overlap margin. Требует всех predecessor, Base/Worst, Cycle и Account PASS.
- **Risk-reducing:** managed close, Partial Far, Final Close, emergency close, завершение partially executed close route. Drawdown/margin breach сам по себе не блокирует однозначное уменьшение риска, но identity, ticket, Symbol/Magic/Cycle, volume, freshness, duplicate guard, terminal action filter и reconciliation остаются обязательными.
- Неоднозначное действие не классифицируется автоматически как risk-reducing: требуется доказательство state-after exposure/margin upper bounds для Base и Worst.

### 6.4. Запрещённые интерпретации

Запрещено трактовать Basket Risk как замену existing Risk или Margin; обход predecessor; mutating optimizer; новый money model; источник confirmed P/L; разрешение Base-only; общий Base/Worst state; разрешение open после partial; средство promotion любого Big; identity по одному comment; основание MQL5/runtime/production PASS. Historical open price не становится margin control price, а `EstimatedReleasedMarginUpper` — фактическим освобождением.

## 7. Совместимость с денежными корзинами

Basket Risk использует существующие buckets без нового ledger: `RealizedCyclePL`, `PartialBudget`, `FinalReserve`, `Carry`, `TransitionBudget`, `CumulativeTransitionLoss`.

```text
Confirmed Harvest deals → Actual HarvestNet → EligibleHarvest
→ PartialAdd + ReserveAdd + CarryAdd

Confirmed Transition credits → TransitionBudget
```

Нормативные рёбра и conservation проверяются, но Basket Risk ничего не начисляет и не списывает. `FinalReserve` — защищённая классификация уже реализованной прибыли внутри `RealizedCyclePL`, а не дополнительная прибыль.

### 7.1. Запрещённые рёбра

```text
FinalReserve -X-> Partial Far / Transition / Margin / Opens
PartialBudget -X-> Final Close / Transition / Opens
TransitionBudget -X-> Opens / Final Close
Projected money -X-> persisted bucket
Initial ignored profit -X-> RecoveryPL / Reserve / TransitionBudget
```

### 7.2. Нормативные отдельные показатели

| Поле | Единица | Смысл |
|---|---|---|
| `EconomicRecoveryPL` | money | Экономический результат по утверждённой формуле; provenance обязателен |
| `RealizedCyclePL` | money | Только confirmed realized cycle entries |
| `FloatingBasketNet` | money | Плавающая net оценка, не persisted credit |
| `FinalReserveAvailable` | money | Доступная reserve, уже внутри realized |
| `PartialBudgetAvailable` | money | Доступный только Partial Far budget |
| `CarryAvailable` | money | Carry по существующему контракту |
| `TransitionBudgetAvailable` | money | Только confirmed transition bucket |
| `RequiredFinalFarCloseLoss` | money | Прогноз/actual явно маркируется |
| `CoverageRatio` | ratio | Dimensionless coverage, отдельно от money |
| `ProjectedFinalCycleNet` | money | Forecast, никогда не confirmed |

Формула `RealizedCyclePL + FloatingPL + FinalReserve` запрещена как double count. Projected и actual имеют разные provenance/status.

### 7.3. Conservation checks

- `PartialAdd + ReserveAdd + CarryAdd = EligibleHarvest` в money tolerance.
- Для каждого bucket: opening + confirmed credits − confirmed debits = closing.
- Negative Harvest не создаёт credits.
- Reserve в level model не уменьшается; debit — только confirmed Final Far Close по действующему контракту.
- Mismatch даёт `MONEY_*` reject/error или reconciliation, но не корректировку plan/ledger внутри Basket Risk.

## 8. Immutable Basket Risk snapshot

Basket Risk snapshot расширяет существующие `StateBefore`, `CandidatePlan`, `RouteState` и два profile snapshots; не создаёт параллельный temporal model.

### 8.1. Identity header

| Поле | Тип/единица | Contract |
|---|---|---|
| Timestamp | UTC datetime | Момент freeze; не execution confirmation |
| Symbol | string | Непустой, точное совпадение managed symbol |
| Magic | integer identity | Точное совпадение |
| CycleID | stable identity | Уникален в namespace |
| Revision | monotonic integer | Любое изменение требует нового result |
| Fingerprint | deterministic identity hash | Profile-specific, включает mutable economics |
| PlanID | stable plan identity | Persisted plan binding |
| State | typed state | StateBefore/RouteState binding |
| Profile | BASE/WORST | Неизменяем и независим |
| ModelVersion | stable schema version | Обязателен для serialization |

### 8.2. Managed position record

Для каждого leg: `Ticket`, `Identifier`, `Role`, `Direction`, `Lot`, `OpenPrice`, `CurrentClosePrice`, `ProjectedClosePrice`, `LifecycleNet`, `ConfirmedState`. Допустимые роли: `Far`, `LegacyBig`, `LegacySmall`, `BigCore`, `BigTrend`, `SmallBase`, `ReverseSmall`.

Только actual verified remainder `BigCore` может быть promoted в NewFar на соответствующем route. `BigTrend` и Legacy `ReverseSmall` NewFar не становятся. Ticket/comment не заменяют identifier и namespace.

### 8.3. Money state

Snapshot хранит раздельно: `RealizedPLBefore`, `RealizedPLAfterHarvest`, `RealizedPLAfterPartial`; `PartialBudgetBefore/Add/Consumed/After`; `ReserveBefore/Add/After`; `CarryBefore/Add/After`; `TransitionBudget`; `CumulativeTransitionLoss`; `RecoveryBefore/After`; `CoverageBefore/After`. Каждое поле имеет money/ratio dimension и projected/confirmed provenance.

### 8.4. Margin state

Обязательны `MarginBeforeSnapshot`, `EstimatedReleasedMarginUpper`, `RemainingFarMargin`, `NextCoreMargin`, `NextTrendMargin`, `NextSmallMargin`, `SteadyStateMarginUpper`, `PeakExecutionMarginUpper`, `OverlapMarginUpper`, `MarginLevelAfter`, `MarginUsageAfter`, `ProjectedFreeMarginAfter`. Единое `ProjectedMargin` не заменяет эти состояния.

### 8.5. Freeze и freshness

После freeze запрещено менять ticket, identifier, lot, role, bucket, revision, profile, plan или price snapshot. Любое изменение экономически mutable input создаёт новый fingerprint/revision и новый preview. Mismatch → `BASKET_RISK_STALE_PLAN` либо `BASKET_RISK_RECONCILIATION_REQUIRED`; execution запрещён.

Fingerprint serialization MUST быть deterministic, с fixed field order, units, normalized numeric representation, ModelVersion и Profile. Base fingerprint не используется как Worst fingerprint.

## 9. Независимые профили BASE и WORST

Basket Risk MUST получить два независимо frozen profile state. Для каждого существуют собственные state sequence, fingerprint, price inputs, spread provenance, margin calculations, risk metrics, gate states, outcome и ReasonCode.

### 9.1. Запрет смешения

- Worst spread/shock не мутирует baseline spread/state.
- При `cumulativeSpreadStress=false` execution shock применяется один раз на level.
- Worst leg/net не может улучшиться относительно Base без явного market/model provenance; иначе `WORST_PROFILE_OPTIMISTIC_DIVERGENCE`.
- Base и Worst lots, prices, states или route outcomes не усредняются.
- `CONTINUE`/`FINAL_ROUTE`, `PASS`/`REJECT` и иные mixed outcomes — divergence, не PASS.

### 9.2. Агрегация

Приоритет: `ERROR` → `TERMINAL` → reconciliation/stale → reject/divergence → согласованный calculation-valid route/pass. `FINITE_PASS` существует только при `BASE=FINITE_PASS` и `WORST=FINITE_PASS`. Final route разрешён только при согласованном Final route обоих profiles.

| Base | Worst | Aggregate |
|---|---|---|
| ERROR/любой | любой | `BASKET_RISK_ERROR` |
| любой | ERROR | `BASKET_RISK_ERROR` |
| TERMINAL | любой не ERROR | `BASKET_RISK_TERMINAL` |
| любой не ERROR | TERMINAL | `BASKET_RISK_TERMINAL` |
| FINITE_PASS | FINITE_PASS | Допускает переход к Basket gates |
| FINAL_ROUTE | FINAL_ROUTE | `ALLOW_FINAL_CLOSE_PREVIEW` после Basket checks |
| CONTINUE | CONTINUE | `ALLOW_CONTINUATION` после Basket checks |
| различные valid routes | различные | `REJECT_WORST_CASE`/typed divergence |
| PASS | REJECT/NOT_EVALUATED | `REJECT_WORST_CASE` |

Calculation-valid route остаётся route, а не confirmed execution.

## 10. Классификация действий и маршрутов

ActionCode типизирован и связан с существующим route; он не является командой исполнения.

### 10.1. Initial

`OPEN_INITIAL_BUY`, `OPEN_INITIAL_SELL`, `CLOSE_INITIAL_PROFIT_LEG`, `PROMOTE_INITIAL_LOSS_LEG_TO_FAR`. Первый plus leg не входит в RecoveryPL, Reserve или TransitionBudget.

### 10.2. Legacy Big/Small

`OPEN_LEGACY_BIG`, `OPEN_LEGACY_SMALL`, `CLOSE_LEGACY_BIG`, `CLOSE_LEGACY_SMALL`, `PARTIAL_CLOSE_FAR`, `FINAL_CLOSE_FAR`.

### 10.3. Hybrid Big

`OPEN_BIG_CORE`, `OPEN_BIG_TREND`, `OPEN_SMALL_BASE`, `CLOSE_BIG_CORE`, `CLOSE_BIG_TREND`, `CLOSE_SMALL_BASE`, `ALLOCATE_CONFIRMED_HARVEST`, `PARTIAL_CLOSE_FAR`, `BUILD_NEXT_BASKET`.

Allocation допустима только из confirmed Harvest deals и сама не является open. `BUILD_NEXT_BASKET` risk-increasing и требует полного gate chain.

### 10.4. Hybrid Small transition

Порядок неизменяем:
+
+```text
+PLAN_CREATED → PLAN_VALIDATED → SMALLBASE_CLOSED → OLDFAR_CLOSED
+→ BIGTREND_CLOSED → BIGCORE_COMPRESSED → ACTUAL_REMAIN_VERIFIED
+→ NEXT_GEOMETRY_PREVIEWED → NEWFAR_PROMOTED
+→ FINAL_GATE_CHECKED → NEXT_CYCLE_CREATED
+```
+
+Ни Basket Risk, ни safe route не пропускают phase. Promotion разрешена только после actual remainder verification; partial/unknown outcome останавливает цепь для reconciliation.
+
+### 10.5. Final route
+
+```text
+FULL_FAR_AFFORDABILITY_EVALUATION
+→ BUILD_FINAL_CLOSE_ROUTE_STATE
+→ FINAL_CLOSE_PREVIEW_REQUIRED
+→ FINAL_CLOSE_EXECUTION
+→ ZERO_MANAGED_POSITIONS_CONFIRMATION
+→ RECONCILIATION
+```
+
+`FINAL_CLOSE_PREVIEW_REQUIRED` не означает `CYCLE_SUCCESS`. Success требует confirmed deals, confirmed financial result, ноль managed positions и reconciliation success.
+
+### 10.6. Action allow policy
+
+Risk-increasing action получает `ExecutionAllowed=true` только после всех existing gates, Base/Worst agreement, Cycle PASS, Account PASS и freshness PASS. Risk-reducing action может получить специальный allow при breached risk/margin limits, только если identity/freshness/volume/duplicate/terminal-action checks пройдены и conservative Base/Worst state-after действительно уменьшает риск.
