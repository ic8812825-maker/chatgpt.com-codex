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
