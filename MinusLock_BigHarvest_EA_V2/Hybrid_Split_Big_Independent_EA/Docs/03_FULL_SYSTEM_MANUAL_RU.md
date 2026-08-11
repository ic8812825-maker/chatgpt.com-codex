# Полный системный мануал Hybrid Split Big

Версия HSB.0R-C.4. Статус: нормативный source of truth, самодостаточен.

## Полный цикл
`IDLE → Initial Lock actual fills → close INITIAL_PLUS actual deal → FAR → immutable CandidatePlan → C/T/S basket actual fills → Big Harvest → Allocation → Final Close или Partial Far`, либо `Small confirmation → immutable transition → close SMALL_BASE → OldFar → BIG_TREND → planned BIG_CORE part → actual BIG_CORE residual → NEW_FAR → FAR нового цикла`.

## Роли и направления
Far SELL: BIG_CORE и BIG_TREND BUY, SMALL_BASE SELL. Far BUY: BIG_CORE и BIG_TREND SELL, SMALL_BASE BUY. BUY close рассчитывается по Bid, SELL close по Ask. Одновременно допускается только один FAR.

## Объёмы и три закона
`C=FloorBrokerGrid(F×Rc)`, `T=FloorBrokerGrid(F×Rt)`, `S=CeilBrokerGrid(F×Rs)`, `Bnet=C+T-S`. После округления обязательны: `Bnet-F>0`; broker-money Reserve Catch-Up; `RecoveryPL(P+tick)>RecoveryPL(P)` на проверяемом диапазоне; compression `0<N<F` с risk/margin/next-cycle gates. Rc>0, Rt≥0, Rs>0; любые NaN, overflow, invalid volume или failed proof дают reject. Demonstration profile не является default.

## Typed control prices
CurrentClosePrice, NextBigControlPrice, SmallTransitionControlPrice, AdverseRiskControlPrice, GapStressPrice, FinalClosePrice всегда содержат Bid/Ask side, tick-normalized price, timestamp и freshness. Stale snapshot блокирует действие.

## CandidatePlan и Future Small
Plan immutable и связан с Account+Symbol+Magic+CycleID+StateRevision+market snapshot. Future Small проверяется exact recursion до terminal/depth/bound, затем conservative `F(k+j)≤q^jF(k)`, 0<q<1. Depth 1 не является доказательством.

## NewFar
Solver перебирает broker-valid N по возрастанию и выбирает minimum-safe. Fixed TargetNewFarRatio не является solver. Tie-break: RiskNext, MarginNext, expected transitions, safety buffer, N. Источник NEW_FAR — только actual remaining original BIG_CORE ticket/identifier после подтверждённых fills.

## Money и allocation
`DealNet=Profit+Swap+Commission+Fee`. Initial Profit и opening DEAL_ENTRY_IN исключены. Для каждого SourceDealKey: `FinalReserve+PartialFar+Transition+Carry+Residual=AllocatableDealNet`; отрицательный DealNet не распределяется как прибыль. EventKey и ConsumptionKey обеспечивают exactly-once. FinalReserve никогда не используется Partial Far.

## Partial Far
Только PartialFarBudget резервируется; `CloseLotRaw=Budget/FarCloseLossPerLot`, затем floor по broker step и повторная проверка стоимости. Actual consumption определяется actual closing DealNet. Unused reservation освобождается. Partial fill блокирует следующий шаг.

## Transition Loss
`TransitionNet=ΣActualClosingDealNet`, `TransitionLoss=max(0,-TransitionNet)`. Разрешённый loss — минимум absolute cap, equity cap, OldFar-risk cap и cumulative-cycle cap.

## Final Close
Единая authority: `RecoveryPLCloseNow ≥ MinimumRecoveryProfitMoney + ExecutionSafetyBufferMoney + MoneyTolerance`, где `RecoveryPLCloseNow=RealizedCycleNet+ΣOpenPositionCloseNowNet`. Allocation buckets повторно не прибавляются. Дополнительно обязательны reconciled positions, no pending actions, no unknown deals, valid ownership, fresh FinalClosePrice, costs and allowed coverage.

## Small confirmation
Touch недостаточен. Нужны close-side touch, повторный fresh snapshot, configurable hold/retrace, persisted debounce key и отсутствие active transition. Duplicate trigger — NO-OP.

## Transaction, retry и timeout
`Plan→Action→Persist→Request→OnTradeTransaction→fill accumulation→actual state→ledger→persist→FSM advance`. REQUEST_SENT/PLACED/DONE_PARTIAL не равны completed. Retry допускается только с тем же ActionID, после history check, при отсутствии completed deal, reconciliation=PENDING и исключённом duplicate request. TIMEOUT не равен failure или completed и ведёт в reconciliation.

## Risk, margin и emergency
Перед открытием: ownership→freshness→spread→volume→margin→free margin→drawdown→gross exposure→worst case. Неизвестное значение = fail-closed. Emergency Liquidation отделена от recovery Final Close, не получает recovery PASS, блокирует открытия и требует manual review/no auto-resume.

## Scope, persistence и REAL_LIMITED
Identity: AccountLogin+Symbol+Magic+CycleID+PositionIdentifier+Role. Generation 1: один цикл на Symbol+Magic; multi-symbol только при полной изоляции. Persistence: crash-consistent versioned file commit protocol, canonical serialization, SHA-256, temp write, reread verify, commit marker, previous snapshot, append-only journal, per-identity lock. REAL_LIMITED запрещён до всех readiness gates, Demo Forward PASS и отдельного одобрения администратора.

## Restart/error semantics
Restart сверяет actual positions/orders/deals, snapshot и action/event ledgers. Нельзя угадывать FAR, восстанавливать только по comment или продолжать после conflict. Critical mismatch → RECONCILIATION/TERMINAL_SAFE.

Статус: OPEN_P0=0, OPEN_P1=0, OPEN_P2=0; production code отсутствует; real trading запрещена.
> **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены.
