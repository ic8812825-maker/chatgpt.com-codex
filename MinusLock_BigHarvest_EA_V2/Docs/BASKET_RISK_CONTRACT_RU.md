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

```text
PLAN_CREATED → PLAN_VALIDATED → SMALLBASE_CLOSED → OLDFAR_CLOSED
→ BIGTREND_CLOSED → BIGCORE_COMPRESSED → ACTUAL_REMAIN_VERIFIED
→ NEXT_GEOMETRY_PREVIEWED → NEWFAR_PROMOTED
→ FINAL_GATE_CHECKED → NEXT_CYCLE_CREATED
```

Ни Basket Risk, ни safe route не пропускают phase. Promotion разрешена только после actual remainder verification; partial/unknown outcome останавливает цепь для reconciliation.

### 10.5. Final route

```text
FULL_FAR_AFFORDABILITY_EVALUATION
→ BUILD_FINAL_CLOSE_ROUTE_STATE
→ FINAL_CLOSE_PREVIEW_REQUIRED
→ FINAL_CLOSE_EXECUTION
→ ZERO_MANAGED_POSITIONS_CONFIRMATION
→ RECONCILIATION
```

`FINAL_CLOSE_PREVIEW_REQUIRED` не означает `CYCLE_SUCCESS`. Success требует confirmed deals, confirmed financial result, ноль managed positions и reconciliation success.

### 10.6. Action allow policy

Risk-increasing action получает `ExecutionAllowed=true` только после всех existing gates, Base/Worst agreement, Cycle PASS, Account PASS и freshness PASS. Risk-reducing action может получить специальный allow при breached risk/margin limits, только если identity/freshness/volume/duplicate/terminal-action checks пройдены и conservative Base/Worst state-after действительно уменьшает риск.

## 11. Typed outcomes

| Outcome | CalcValid | Continue | FinalPreview | Terminal | Reject | Error | Recon | Execution |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BASKET_RISK_NOT_EVALUATED` | N | N | N | N | N | N | N | N |
| `BASKET_RISK_ALLOW_CONTINUATION` | Y | Y | N | N | N | N | N | Y после freshness |
| `BASKET_RISK_ALLOW_FINAL_CLOSE_PREVIEW` | Y | N | Y | N | N | N | N | Только preview; close отдельно |
| `BASKET_RISK_ALLOW_RISK_REDUCING_EXECUTION` | Y | N | route-dependent | N | N | N | post-exec | Y после freshness |
| `BASKET_RISK_REJECT_CONFIGURATION` | N | N | N | N | Y | N | N | N |
| `BASKET_RISK_REJECT_VOLUME` | N | N | N | N | Y | N | возможно | N |
| `BASKET_RISK_REJECT_GEOMETRY` | N | N | N | N | Y | N | N | N |
| `BASKET_RISK_REJECT_CYCLE_RISK` | Y | N | N | N | Y | N | N | N |
| `BASKET_RISK_REJECT_ACCOUNT_RISK` | Y | N | N | N | Y | N | N | N |
| `BASKET_RISK_REJECT_MARGIN` | predecessor-dependent | N | N | N | Y | N | N | N |
| `BASKET_RISK_REJECT_WORST_CASE` | Y | N | N | N | Y | N | N | N |
| `BASKET_RISK_REJECT_FUTURE_SMALL` | Y | N | N | N | Y | N | N | N |
| `BASKET_RISK_STALE_PLAN` | N | N | N | N | Y | N | возможно | N |
| `BASKET_RISK_RECONCILIATION_REQUIRED` | N | N | N | N | N | N | Y | N |
| `BASKET_RISK_ERROR` | N | N | N | N | N | Y | возможно | N |
| `BASKET_RISK_TERMINAL` | route-dependent | N | N | Y | N | N | возможно | Только явно разрешён emergency close |

`ExecutionAllowed` для allow outcome — необходимое, но не достаточное разрешение: непосредственно перед execution обязательна freshness. Preview outcome никогда не разрешает пометить actual close confirmed.

## 12. Нормативный каталог ReasonCode

ReasonCode — stable typed uppercase identifier; free text разрешён только как diagnostic detail. Он одинаков во всех pre-open/transition/Future Small/restart contexts и указывает первый failed gate. Downstream gates остаются `Evaluated=false`.

| Группа | Минимальные нормативные коды |
|---|---|
| `IDENTITY_*` | `IDENTITY_SYMBOL_MISMATCH`, `IDENTITY_MAGIC_MISMATCH`, `IDENTITY_CYCLE_MISMATCH`, `IDENTITY_ROLE_IDENTIFIER_MISSING` |
| `CONFIG_*` | `CONFIG_INVALID`, `CONFIG_PROFILE_UNSUPPORTED` |
| `VOLUME_*` | `VOLUME_INVALID`, `VOLUME_BELOW_MIN`, `VOLUME_STEP_MISMATCH` |
| `ROUNDING_*` | `ROUNDING_RECHECK_FAILED`, `ROUNDING_PROVENANCE_MISSING` |
| `GEOMETRY_*` | `GEOMETRY_LAW_FAILED`, `GEOMETRY_COMPRESSION_FAILED`, `GEOMETRY_NEXT_BIG_STRICT_LIMIT` |
| `MONEY_*` | `MONEY_CONSERVATION_FAILED`, `MONEY_FORBIDDEN_EDGE`, `MONEY_PROJECTED_AS_CONFIRMED` |
| `CATCHUP_*` | `CATCHUP_NOT_FINITE`, `CATCHUP_LEVEL_INVALID` |
| `TRANSITION_*` | `TRANSITION_ORDER_INVALID`, `TRANSITION_BUDGET_INVALID` |
| `NEWFAR_*` | `NEWFAR_INVALID`, `NEWFAR_ACTUAL_REMAINDER_UNVERIFIED` |
| `CYCLE_RISK_*` | `CYCLE_RISK_LIMIT_EXCEEDED`, `CYCLE_RISK_INPUT_INCOMPLETE` |
| `ACCOUNT_RISK_*` | `ACCOUNT_RISK_LIMIT_EXCEEDED`, `ACCOUNT_RISK_INPUT_INCOMPLETE` |
| `MARGIN_*` | `MARGIN_STEADY_LIMIT`, `MARGIN_PEAK_LIMIT`, `MARGIN_OVERLAP_LIMIT`, `MARGIN_CONTROL_PRICE_INVALID` |
| `WORST_*` | `WORST_REJECTED`, `WORST_PROFILE_OPTIMISTIC_DIVERGENCE`, `WORST_ROUTE_DIVERGENCE` |
| `FUTURE_SMALL_*` | `FUTURE_SMALL_REJECTED`, `FUTURE_SMALL_NOT_EVALUATED` |
| `FINAL_ROUTE_*` | `FINAL_ROUTE_PREVIEW_REQUIRED`, `FINAL_ROUTE_STATE_INVALID`, `FINAL_ROUTE_NOT_CONFIRMED` |
| `STALE_*` | `STALE_FINGERPRINT`, `STALE_REVISION`, `STALE_PRICE`, `STALE_STATE` |
| `PARTIAL_EXECUTION_*` | `PARTIAL_EXECUTION_OPEN`, `PARTIAL_EXECUTION_CLOSE`, `PARTIAL_EXECUTION_PAIR`, `PARTIAL_EXECUTION_TRANSITION`, `PARTIAL_EXECUTION_FINAL_CLOSE`, `PARTIAL_EXECUTION_UNKNOWN` |
| `RECONCILIATION_*` | `RECONCILIATION_REQUIRED`, `RECONCILIATION_MISMATCH`, `RECONCILIATION_ACTUAL_UNAVAILABLE` |
| `TERMINAL_*` | `TERMINAL_STATE_ACTIVE`, `TERMINAL_ACTION_FORBIDDEN` |
| `INTERNAL_ERROR_*` | `INTERNAL_ERROR_INVARIANT`, `INTERNAL_ERROR_DIMENSION`, `INTERNAL_ERROR_SERIALIZATION` |

Новые коды добавляются versioned append-only; смысл существующего кода не переиспользуется.

## 13. Cycle Basket Risk и Account Basket Risk

Этап 2.0 определяет структуру и dependencies, но не утверждает формулы/лимиты/score; это предмет Этапа 2.1 после `BASKET_RISK_CONTRACT_APPROVED`.

### 13.1. Cycle Basket Risk

Namespace: точное сочетание `Symbol + Magic + CycleID + role identifier`. В cycle aggregation не входят чужие symbol/magic/cycle и unmanaged positions.

| Metric | Dimension | Contract |
|---|---|---|
| `CycleGrossLots` | lot | Сумма gross managed lots активного cycle |
| `CycleDirectionalLots` | lot | Signed directional exposure |
| `CycleNetRecoveryExposure` | lot | Recovery exposure по profile |
| `CycleWorstFloatingLoss` | money | Worst profile forecast |
| `CycleRealizedPL` | money | Confirmed realized only |
| `CycleFloatingNet` | money | Profile floating forecast |
| `CycleRecoveryPL` | money | Без повторного Reserve |
| `CycleReserve` | money | Отдельная классификация |
| `CyclePartialBudget` | money | Только Partial budget |
| `CycleCarry` | money | Carry bucket |
| `CycleTransitionBudget` | money | Transition bucket |
| `CycleRequiredMargin` | money | Conservative state-after |
| `CyclePeakExecutionMargin` | money | Peak execution upper |
| `CycleReverseCount` | count | Целое неотрицательное |
| `CycleHarvestLevel` | count | Текущий level |
| `CycleManagedPositionCount` | count | Verified managed positions |
| `CycleRiskScore` | versioned score | Формула не утверждена Этапом 2.0 |

Для Hybrid: `BigGross=Core+Trend`; `DirectionalExposure=Core+Trend−Small`; `NetRecoveryExposure=Core+Trend−Small−Far`. SmallBase не добавляется к BigGross. Direction signs обязаны следовать фактическому profile direction.

### 13.2. Account Basket Risk

Account layer выполняется после Cycle PASS и не заменяет его. Inputs: `AccountBalance`, `AccountEquity`, `AccountMargin`, `AccountFreeMargin`, `AccountMarginLevel`, `AccountDrawdown`, `AccountManagedGross`, `AccountManagedNet`, `AccountManagedPositionCount`, `ProjectedAccountMarginUpper`, `ProjectedAccountFreeMargin`, `ProjectedAccountMarginLevel`, `ProjectedAccountDrawdown`.

Account aggregation включает все managed cycles по утверждённой identity policy, но не присваивает их позиции текущему CycleID. Unmanaged exposure либо учитывается отдельным account input согласно будущей математике, либо вызывает typed incomplete/unsafe outcome; оно не может молча игнорироваться.

### 13.3. Разрешающее условие

Risk-increasing action допускается только если `predecessors PASS ∧ Base/Worst agreement ∧ CycleRisk PASS ∧ AccountRisk PASS ∧ freshness PASS`. Любой conjunct failure запрещает open. Risk-reducing policy применяется отдельно по разделу 6.3 и не превращает breach в общий PASS.

## 14. Margin contract

Basket Risk потребляет результат существующего Margin Gate и его provenance; не вызывает альтернативную money/margin model.

1. `MARGIN-01`: control price использует текущую рыночную сторону для соответствующей операции/profile.
2. `MARGIN-02`: historical OpenPrice не становится control price автоматически.
3. `MARGIN-03`: `EstimatedReleasedMarginUpper` — forecast bound, не actual release и не confirmed free margin.
4. `MARGIN-04`: PASS использует conservative state-after upper bound.

Обязательны три разные оценки: `SteadyStateMarginUpper`, `PeakExecutionMarginUpper`, `OverlapMarginUpper`. PASS требует соблюдения применимых limits во всех состояниях последовательности, включая временный overlap «новая позиция открыта, старая ещё существует». Только конечная steady-state margin недостаточна. Base/Worst имеют независимые market-side prices и margins.

## 15. Final Close route contract

Если existing full-Far affordability evaluation выбирает Final route:

```text
Partial Far не выполняется
FarLotForFinalClosePreview == FarLotBefore (lot tolerance)
PartialBudgetConsumed == 0 (money tolerance)
Next Basket не строится
continuation geometry не вычисляется
reopen margin не вычисляется
RecoveryAfterReopen не вычисляется
RouteOutcome = FINAL_CLOSE_PREVIEW_REQUIRED
```

Basket Risk проверяет route state/fingerprint/revision, Cycle/Account effects риск-уменьшающего close и freshness. Он не перенаправляет route в Partial Far/continuation. `ALLOW_FINAL_CLOSE_PREVIEW` разрешает только preview. Перед actual close требуется отдельное risk-reducing execution permission; после него — confirmed deals, actual financial result, zero managed positions и reconciliation. Только тогда внешний существующий lifecycle может определить success/loss terminal state.

Нулевое число managed positions проверяется по Symbol/Magic/Cycle/identifier и orphan protection, а не только по очищенному context или comment.

## 16. Typed dimensions и граничные сравнения

| Dimension | Примеры | Только свой tolerance |
|---|---|---|
| money | P/L, reserve, margin, costs | money tolerance |
| lot | volumes, exposure | lot tolerance |
| price | Bid/Ask/open/close price | price tolerance |
| ratio | coverage, compression ratio | ratio tolerance |
| percent | margin usage, drawdown | percent tolerance |
| points | distance, spread offset | points tolerance |
| count/identity | level, revision, ticket | точное integer/identity equality |

Правила:

- lot не сравнивается money tolerance; price — money tolerance; points — price tolerance.
- Raw projected money не округляется перед conservative inequality. Форматирование trace не меняет gate value.
- Lot noise `≤ lot tolerance` не является реальным partial volume.
- Strict inequality сохраняется strict с нормативной tolerance semantics: New Big на лимите отклоняется.
- Far compression обязана превышать lot tolerance, а не быть только положительной математически.
- Residual Far равен zero в lot tolerance либо `≥ SYMBOL_VOLUME_MIN`; Far ниже minimum не продолжает Catch-Up.
- Normalization contract неизменен: Core/Trend/NewFar DOWN, Small UP; после него выполняется volume recheck и все обязательные downstream gates.
- `NaN`, infinity, отсутствующая dimension/provenance или несовместимая unit → `INTERNAL_ERROR_DIMENSION`/typed predecessor reject, не PASS.

Каждое trace field фиксирует unit. Конверсия points↔price или percent↔ratio допустима только явно, с symbol/profile inputs и provenance; скрытая конверсия запрещена.

## 17. Partial execution и reconciliation

Typed execution observations:

- `OPEN_PARTIAL` — requested open исполнен не полностью;
- `CLOSE_PARTIAL` — один close исполнен не полностью;
- `PAIR_PARTIAL` — legs парной операции имеют неполный/асимметричный результат;
- `TRANSITION_PARTIAL` — остановка между transition phases;
- `FINAL_CLOSE_PARTIAL` — Far остаётся после final-close attempt;
- `UNKNOWN_EXECUTION_RESULT` — terminal/deal result нельзя однозначно подтвердить.

Любой partial, reject, timeout, ambiguous ticket/deal или actual/projected mismatch MUST вернуть `BASKET_RISK_RECONCILIATION_REQUIRED`. До reconciliation запрещено: строить следующий open; продолжать старый plan; считать forecast confirmed; повторно начислять деньги; менять role; promote NewFar; очищать context как fully closed.

Reconciliation MUST:

1. заново получить actual managed positions и deals;
2. разрешить ticket+identifier+Symbol+Magic+CycleID+role;
3. проверить actual remaining volumes и lifecycle nets;
4. применить idempotent confirmed ledger events exactly once;
5. сопоставить state/phase с partial result;
6. повысить revision, создать новые profile fingerprints и новый snapshot;
7. повторно провести обязательный gate chain перед следующим open.

Risk-reducing retry может продолжить только заранее определённый close route с actual ticket/volume и duplicate guard; он не разрешает новый open. Если reconciliation невозможно, результат ERROR/TERMINAL/manual intervention согласно существующему lifecycle.

## 18. Exactly-once contract

Exactly once применяется к каждому `HarvestNet`, `PartialFarNet`, open commission leg и ledger event. Projected event не является commit. Один event имеет ровно один terminal commit outcome (`COMMITTED` или typed rejected/rolled-back status по существующему ledger contract) и не может быть повторно credited/debited после restart.

Нормативный состав EventKey:

```text
Symbol + Magic + CycleID + DealTicket + PositionIdentifier
+ LedgerEventType + PlanID + Revision
```

Поля сериализуются deterministic и namespace-aware. Один текст comment, ticket без identifier/cycle или PlanID без deal identity недостаточны. Profile forecast не создаёт отдельный financial event. Basket Risk может только проверить наличие/уникальность/provenance key; commit выполняет существующий ledger после confirmed deal.

## 19. Совместимое расширение trace

Не создаётся отдельный несовместимый лог. Будущие поля добавляются к `HYBRID_GATE`, `HYBRID_CATCHUP_LEVEL`, `HYBRID_DECISION` согласно их fixed-order/version contract:

| Поле | Unit/type | Semantics |
|---|---|---|
| `CycleRiskEvaluated` | bool | Gate реально исполнялся |
| `CycleRiskPassed` | bool/NA | NA если не evaluated |
| `CycleRiskCode` | typed code | Первый cycle result code |
| `AccountRiskEvaluated` | bool | Account gate реально исполнялся |
| `AccountRiskPassed` | bool/NA | NA если short-circuit |
| `AccountRiskCode` | typed code | Первый account result code |
| `ProjectedAccountMarginUpper` | money | Conservative forecast |
| `ProjectedAccountFreeMargin` | money | Forecast, не actual |
| `ProjectedAccountMarginLevel` | percent | Forecast |
| `ProjectedAccountDrawdown` | percent | Forecast |
| `CycleGrossLots` | lot | Active cycle gross |
| `CycleNetExposure` | lot | Signed recovery exposure |
| `CycleWorstLoss` | money | Worst profile forecast |
| `BasketRiskOutcome` | typed outcome | Итог раздела 11 |
| `BasketRiskReasonCode` | typed code | Первый failed gate/result |
| `ExecutionFreshnessPassed` | bool/NA | Recheck непосредственно перед action |
| `ReconciliationRequired` | bool | Блокирует следующий open |

Каждая запись также содержит Timestamp, Symbol, Magic, CycleID, PlanID, ModelVersion, Profile, Fingerprint, Revision и state/route identity. Serialization deterministic, numeric precision/unit versioned, field order fixed. Base/Worst пишутся отдельными profile records плюс aggregate decision; исходные records не переписываются aggregate результатом.

## 20. Таблица совместимости gates и invariants

| Existing gate/invariant | Basket Risk input | Basket Risk check | Возможный outcome | Продолжение |
|---|---|---|---|---|
| Identity | Symbol/Magic/Cycle/identifier | Exact namespace | IDENTITY reject/error | Нет при failure |
| Configuration | config validity/profile | predecessor PASS | CONFIG reject | Нет |
| Volume | raw/normalized lots, broker limits | validity + units | VOLUME reject | Нет |
| Rounding | directions/provenance | required DOWN/UP | ROUNDING reject | Нет |
| Volume recheck | rounded lots | min/max/step/dust | VOLUME reject | Нет |
| Geometry | OldFar/NewFar/legs | GEO-01…05 | GEOMETRY reject | Нет |
| Law 1 | ready plan results | existing law PASS | GEOMETRY reject | Нет |
| Law 2 lots | lots result | existing strict result | GEOMETRY/VOLUME reject | Нет |
| Law 2 money | BrokerMoney result | money law PASS | MONEY reject | Нет |
| Compression | Old/Residual Far | strict tolerance | GEOMETRY reject | Нет |
| Next Big | Core+Trend and limit | strict below limit | GEOMETRY reject | Нет на equality |
| Gross | Core/Trend/Small roles | correct definitions | CYCLE_RISK/error | Только PASS |
| Base Money | Base profile money | valid/provenance | MONEY reject/error | Нет |
| Finite Catch-Up | typed catch-up result | calculation-valid/finite | CATCHUP reject/route | Только valid agreement |
| Transition | plan phase/budget | order and confirmed inputs | TRANSITION reject/recon | Нет при mismatch |
| New Far | verified remainder/plan | role and actual verification | NEWFAR reject/recon | Нет |
| Existing Risk | candidate risk result | predecessor PASS | corresponding reject | Нет |
| Existing Margin | steady/peak/overlap | predecessor PASS/provenance | MARGIN reject | Нет open |
| Worst Case | independent profile | SAFE/WORST/outcome table | WORST reject/error | Только agreement |
| Future Small | typed preview | predecessor result | FUTURE_SMALL reject | Нет open |
| Final Close Preview | RouteState | ROUTE-* invariants | ALLOW_FINAL_CLOSE_PREVIEW | Только preview |
| Cycle Basket Risk | active cycle metrics | future approved limits | CYCLE_RISK reject/allow | PASS required for open |
| Account Basket Risk | account metrics | future approved limits | ACCOUNT_RISK reject/allow | PASS required for open |
| Execution Freshness | current vs frozen identity | fingerprint/revision/state/price | STALE/recon/allow | Только PASS |
| Reconciliation | actual positions/deals/ledger | actual parity/exactly-once | recon/error/new snapshot | Open только после success |

## 21. Полный запрет неверных трактовок

Ни implementation, ни review не вправе утверждать, что Basket Risk: заменяет Risk/Margin Gate; пропускает predecessor failure; меняет CandidatePlan или normalized lot; использует Reserve для Partial; повторно добавляет Reserve к RecoveryPL; сохраняет projected money как confirmed; превращает Final preview в success; разрешает Base без Worst; объединяет profiles; использует historical price для margin control; считает released-margin estimate actual; продолжает open после partial; promotes NewFar без actual Core remainder; затрагивает чужой namespace; использует comment как единственный identity; доказывает MQL5 без MetaEditor; доказывает runtime без Strategy Tester; повышает documentation stage до production ready.

## 22. Acceptance boundary и переход

Этап 2.0 разрешает только:

```text
STAGE_2_0_DOCUMENTATION_AUDIT_COMPLETE
BASKET_RISK_CONTRACT_READY_FOR_REVIEW
BASKET_RISK_EXISTING_INVARIANT_COMPATIBILITY_DOCUMENTED
```

`BASKET_RISK_CONTRACT_APPROVED` может установить только отдельная приёмка. До этого Этап 2.1 не начинается. Даже после approval Этап 2.1 остаётся математической/размерностной документацией без Python Oracle, MQL5, StateMachine и trading changes.
