# 23. Полный нормативный реестр решений Hybrid Split Big

Версия: HSB.0R-C.3
STATUS=CLOSED_FOR_HSB1_ARCHITECTURE
OPEN_P0=0
OPEN_P1=0
OPEN_P2=0

## Правило чтения
Каждое решение ниже содержит обязательную норму, configuration-поля, диапазоны, validation, fail-closed, owner и тестовые маршруты. Нормативный текст встроен в owner-документы 03–18; этот реестр обеспечивает трассировку, но не заменяет их.

## Решения

### HSBI-DEC-001 — коэффициенты C/T/S
Версия 1.0; до HSB.0R: OPEN P1. Проблема: fixed ratios и отсутствие post-rounding proof. Требования: HSBI-MATH-001..006, HSBI-GEO-005. Owner: 04; зависимости: 03,05,10,14,15. Варианты: fixed, profile set, bounded solver. Анализ: только bounded configuration с broker-grid и тремя законами не меняет архитектуру. Геометрия/деньги: C/T floor, S ceil, money proof обязателен. Архитектура: Planning/GeometrySolver. Execution/persistence: immutable CandidatePlan хранит raw и normalized values. Risk: margin/exposure. Решение: `C=Floor(F*Rc)`, `T=Floor(F*Rt)`, `S=Ceil(F*Rs)`; после rounding `C+T-S-F>0` и broker-money gates. Fixed profile отвергнут как production default. Configuration: Rc,Rt,Rs; диапазоны `Rc>0, Rt>=0, Rs>0`, значения ограничены volume/risk gates. Fail-closed при NaN, overflow, grid mismatch или провале закона. Unit: rounding/laws; integration: basket planning; tester: trend/reversal/coarse step. Evidence: corrected math acceptance. Статус RESOLVED_FOR_ARCHITECTURE. Commit: HSB.0R-C.3.

### HSBI-DEC-002 — allocation shares
До: OPEN P1. Owner 08; зависимости 03,10,11,12,13; требования HSBI-MONEY-001..020. Варианты fixed shares/typed configurable shares. Принято: shares конфигурируемы в [0,1], сумма allocations не превышает allocatable positive DealNet; per-source equality включает Residual. Negative DealNet не распределяется как прибыль. Initial Profit и DEAL_ENTRY_IN исключены. SourceDealKey/EventKey/ConsumptionKey обязательны. FinalReserve изолирован от PartialFar. Fail-closed при over-allocation, foreign source, duplicate conflict. Owner Money/AllocationLedger; unit conservation; integration harvest/replay; tester costs/restart. RESOLVED_FOR_ARCHITECTURE.

### HSBI-DEC-003 — control prices
До: OPEN P1. Owner 05; требования HSBI-GEO-010..018. Приняты typed prices: CurrentClosePrice, NextBigControlPrice, SmallTransitionControlPrice, AdverseRiskControlPrice, GapStressPrice, FinalClosePrice. BUY close=Bid, SELL close=Ask; tick-grid normalization; timestamp/freshness mandatory. Stale, missing or wrong-side snapshot => fail-closed. Owner Planning/MarketSnapshot; tests BUY/SELL, stale/gap. RESOLVED.

### HSBI-DEC-004 — Future Small depth
До: OPEN P1. Owner 14; требования HSBI-NF-010..018. Варианты depth1, bounded exact, unbounded recursion. Принято exact recursion до terminal/depth/analytical bound, затем conservative bound `F(k+j)<=q^jF(k)`, `0<q<1`, с rounding, costs, margin, transition loss. Depth1 отвергнут. Fail-closed при недоказанном next cycle. Owner Planning/FutureSmall. Unit recursion; integration repeated transitions; tester saw/reversals. RESOLVED.

### HSBI-DEC-005 — NewFar objective
До: OPEN P1. Owner 14; требования HSBI-NF-001..009. Принят broker-valid ascending candidate grid и deterministic minimum-safe candidate. Tie-break: RiskNext, MarginNext, reverse count, safety buffer, N. Fixed TargetNewFarRatio отвергнут как единственный solver. Candidate обязан пройти compression, next feasibility, RecoveryPL, catch-up, risk, margin, Future Small, finite catch-up, terminal. Fail-closed если safe candidate отсутствует. Owner Planning/NewFarSolver. RESOLVED.

### HSBI-DEC-006 — Emergency Policy
До: OPEN P1. Owner 15; зависимости 03,06,12,17; требования HSBI-RISK-020..030. Принята отдельная authority: margin, drawdown, identity, persistence, unknown position, duplicate Far, broker failure, manual kill. Emergency не является Final Close и не получает recovery PASS; блокирует открытия, ведёт terminal-safe/manual review, no auto-resume. Owner Risk/EmergencyPolicy. RESOLVED.

### HSBI-DEC-007 — Transition Loss
До: OPEN P1. Owner 13/08; требования HSBI-SMALL-020..026. `TransitionNet=ΣActualClosingDealNet`, `TransitionLoss=max(0,-TransitionNet)`. Допуск=min(absolute money cap,equity cap,OldFar risk cap,cumulative cycle cap). Caps конфигурируемы, неотрицательны; unknown input => reject. Owner Scenarios/SmallTransition+Money. RESOLVED_FOR_ARCHITECTURE.

### HSBI-DEC-008 — Final Close threshold
До: OPEN P1. Owner 12; требования HSBI-FC-001..012. Единая формула: `RecoveryPLCloseNow >= MinimumRecoveryProfitMoney + ExecutionSafetyBufferMoney + MoneyTolerance`. Allocation buckets не прибавляются повторно. Требуются reconciled positions, no pending/unknown, valid ownership, fresh price, costs, allowed coverage. Owner Money/FinalCloseCalculator. RESOLVED_FOR_ARCHITECTURE.

### HSBI-DEC-009 — margin/drawdown
До: OPEN P1. Owner 15; требования HSBI-RISK-001..019. Configurable typed limits: projected margin %, minimum margin level, free margin, cycle/account drawdown, gross exposure, managed positions. Диапазоны валидируются; порядок gates фиксирован; unknown calculation => fail-closed. Research values не являются production defaults. Owner Risk. RESOLVED_FOR_ARCHITECTURE.

### HSBI-DEC-010 — Symbol/Cycle scope
До: OPEN P1. Owner 02/18; требования HSBI-ID-001..015. Identity=`AccountLogin+Symbol+Magic+CycleID+PositionIdentifier+Role`. Generation1: один активный цикл на Symbol+Magic; multi-symbol только при полной изоляции context, ledgers, persistence, actions и reconciliation. Mismatch => blocked/reconciliation. RESOLVED.

### HSBI-DEC-011 — persistence backend
До: OPEN P1. Owner 16; требования HSBI-PERSIST-001..018. Принят crash-consistent versioned file commit protocol: canonical serialization, SHA-256, temp write, close/reread/verify, commit marker, previous valid snapshot, append-only journal, per-identity lock; terminal globals только markers. Ложная filesystem atomicity не заявляется. Corruption => reconciliation/terminal-safe. RESOLVED.

### HSBI-DEC-012 — REAL_LIMITED
До: DEFERRED P1. Owner 21/15/18; требования HSBI-PROD-010..020. Runtime mode определён, но запрещён до ExplicitUserApproval+all readiness gates+DemoForwardPASS. Required whitelist, loss/margin limits, kill switch, full evidence, no auto-resume. Current REAL_TRADING_ALLOWED=NO. RESOLVED_FOR_ARCHITECTURE.

### HSBI-DEC-013 — Small confirmation
До: OPEN P2. Owner 05/13; требования HSBI-GEO-019..025. Touch alone insufficient. Required close-side touch, repeated fresh snapshot, configurable hold/retrace, persisted debounce key, one active trigger. Stale/duplicate => reject. RESOLVED.

### HSBI-DEC-014 — retry/timeout
До: OPEN P2. Owner 07; требования HSBI-TX-020..032. Retry uses same ActionID, only after history recheck, no completed deal, reconciliation=PENDING, state permits retry, duplicate request excluded. Timeout is neither failure nor completed; route to reconciliation. Delayed/duplicate events idempotent by keys. RESOLVED.

## Итог
Все решения имеют owner, диапазон либо точную архитектурную норму, fail-closed и unit/integration/Strategy Tester route. Поля production-оптимизации остаются configuration values, но не создают архитектурной неопределённости.