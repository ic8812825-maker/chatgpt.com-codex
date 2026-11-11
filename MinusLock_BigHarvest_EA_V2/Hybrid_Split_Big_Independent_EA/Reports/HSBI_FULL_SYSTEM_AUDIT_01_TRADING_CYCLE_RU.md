# Торговый цикл, фактическая FSM и failure routes

BASE_SHA=4185b84f7a6a8847f6a9c5796f07113907be447d

Режим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.

Реальные enum states — Core/Enums:8, не предложенная пользователем гипотезаINITIAL_STATE→LOSS_EVALUATION и т.п. STATES=33; extracted direct topology evaluated33×33=1089 pairs, это наблюдения predicate, не1089 независимых PASS. Фактический EA callback cycle остаётся DISABLED. Plan→Action→Persist→Request→OnTradeTransaction→actualledger→persist→FSM указан Docs03/07, но не реализован.

## Номинальная последовательность из owner-docs

| From | To | Library topology | Actual orchestrator |
|---|---|---|---|
| INITIAL_PLAN_READY | INITIAL_OPENING_BUY | True | UNIMPLEMENTED |
| INITIAL_OPENING_BUY | INITIAL_OPENING_SELL | True | UNIMPLEMENTED |
| INITIAL_OPENING_SELL | INITIAL_LOCK_ACTIVE | True | UNIMPLEMENTED |
| INITIAL_LOCK_ACTIVE | INITIAL_PLUS_CLOSING | True | UNIMPLEMENTED |
| INITIAL_PLUS_CLOSING | FAR_ACTIVE | True | UNIMPLEMENTED |
| FAR_ACTIVE | CANDIDATE_PLANNED | True | UNIMPLEMENTED |
| CANDIDATE_PLANNED | BASKET_OPENING_CORE | True | UNIMPLEMENTED |
| BASKET_OPENING_CORE | BASKET_OPENING_TREND | False | UNIMPLEMENTED |
| BASKET_OPENING_TREND | BASKET_OPENING_SMALL | False | UNIMPLEMENTED |
| BASKET_OPENING_SMALL | BASKET_ACTIVE | False | UNIMPLEMENTED |
| BASKET_ACTIVE | BIG_HARVEST_PLANNED | False | UNIMPLEMENTED |
| BIG_HARVEST_PLANNED | BIG_HARVEST_EXECUTING | False | UNIMPLEMENTED |
| BIG_HARVEST_EXECUTING | ALLOCATION_PENDING | False | UNIMPLEMENTED |
| ALLOCATION_PENDING | FINAL_CLOSE_PLANNED | False | UNIMPLEMENTED |
| FINAL_CLOSE_PLANNED | FINAL_CLOSE_EXECUTING | False | UNIMPLEMENTED |
| FINAL_CLOSE_EXECUTING | CYCLE_CLOSED | False | UNIMPLEMENTED |

После initial BUY partial/delayed исполнений нужен rollback при незавершённом SELL. Только actual closed INITIAL_PLUS создаёт Far с исходным identifier и exclusion; эти операции представлены контрактами, не runtime. Candidate C/T/S staged open, BigHarvest actual reconciliation, allocation, FinalClose before PartialFar затем newplan — отсутствующие scenario controllers. У Small: confirmation+debounce→immutable transition→closeSmall→oldFar→Trend→partCore→actual originalCore residual→revalidate/promote→newcycle; каждый шаг требует immutable origin/actual fills/durable receipt, не только requested volumes. Scenarios/*.mqh содержат структуры, не исполнение этих шагов.

## Failure matrix

| Event | Normative route | Current scope | Verdict |
|---|---|---|---|
| ACCEPTED/PLACED | PENDING notcomplete | types+completed barrier only | PARTIALLY_VERIFIED |
| PARTIAL_FILL | block nextrole; accumulate actualdeals | barrier rejectsPARTIAL; accumulator absent | PARTIALLY_VERIFIED |
| REJECT/REQUOTE/PRICE_CHANGE/CANCEL | typed noadvance/reconcile | no real retcode mapper/request engine | UNIMPLEMENTED |
| TIMEOUT/UNKNOWN/DISCONNECT | neither failure norcomplete; history lookup | barrier requiresCompleted; lookup/retryengine absent | UNIMPLEMENTED |
| DUPLICATE_IDENTICAL | verified immutable NO_OP zero delta | ledger/journal duplicate helpers incomplete | CONTRADICTORY |
| ALTERED_REPLAY | CONFLICT | ledger/journal falseNOOP counterexamples | CONTRADICTORY |
| OUT_OF_ORDER | history idempotent reconciliation | eventId freshness blocksadvance; actualreconcile absent | UNIMPLEMENTED |
| RESTART/CORRUPTION | durable validate+history+safe fallback | PersistStub fails; DTO validators only | UNIMPLEMENTED |
| RISK/DUAL_FAR_CONFLICT | blockactions/manual/terminalsafe | sourcevalidators have NaN/cardinality gaps | CONTRADICTORY |
| EMERGENCY | liquidation separateauthority/noautoresume | generic enum/topology; no actual emergency engine | UNIMPLEMENTED |

Pure FSM допускает self-loop, global Reconciling/TerminalSafe/Emergency targets и несколько early normal edges. CoreOpening→TrendOpening отсутствует. Reconciling→FarActive без admin parameter не доказывает no-auto-resume; будущий обязательный orchestrator должен это ограничивать. НаulongMAX proposedRevision unchecked. CurrentEA этот helper не вызывает, поэтому это latent library/implementation gap, не текущий авто-resume на реальном счёте.

Liveness: нет доказательства eventual trigger/fill/reconciliation/terminal affordability. Endless waiting возможно в спецификации при flat/stale/disconnect, однако текущий skeleton просто никогда не запускает цикл. Basket growth ограничивается лишь proposed limits/conditional proof; полная реальная bounded transition sequence не реализована. Duplicate/partial/unknown события типизированы, но engine/history accumulation отсутствуют; no missingdeal may be assumed completed. Full STATE_TRANSITION_MATRIX/FULL_CYCLE_SEQUENCE/FAILURE_TRANSITION_MATRIX — STATE_MATRIX.json.
