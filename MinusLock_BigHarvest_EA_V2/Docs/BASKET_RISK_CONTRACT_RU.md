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
