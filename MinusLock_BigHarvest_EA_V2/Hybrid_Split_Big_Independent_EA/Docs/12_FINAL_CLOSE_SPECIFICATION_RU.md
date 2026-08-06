# 12. Единый нормативный Final Close

Версия HSB.0R-C.13. Статус: нормативный source of truth.

Единственная authority: Scenarios/FinalClose через Money/FinalCloseCalculator. Другие сценарии могут только запросить preview.

Главный gate: `RecoveryPLCloseNow ≥ MinimumRecoveryProfitMoney + ExecutionSafetyBufferMoney + MoneyTolerance`, где `RecoveryPLCloseNow=RealizedCycleNet+ΣOpenPositionCloseNowNet`. Allocation buckets, включая FinalReserve, повторно не прибавляются.

Coverage gate: FinalReserveAvailable+OtherExplicitlyAllowedFinalSources≥RequiredFinalCloseCoverage. Allowed sources перечисляются типизированно; PartialFar reservation и foreign source запрещены.

Обязательны: PositionsReconciled, NoPendingActions, NoUnknownDeals, OwnershipValid, StateRevisionValid, fresh FinalClosePrice, spread allowed, costs/commission/swap/slippage included, market snapshot fingerprint unchanged.

Theoretical Far loss не заменяет broker money. MaxLevel не является основанием. Negative/insufficient RecoveryPL = reject. Emergency Liquidation — отдельная authority и не маркируется successful recovery.

Lifecycle: immutable FinalClosePlan→persist→sequential/parallel actions по плану→OnTradeTransaction→fills→actual zero managed positions→ledger consumption exactly once→persist CYCLE_CLOSED. Partial fill остаётся executing; retry same ActionID только после reconciliation. Restart восстанавливает plan/actions/consumption.

PASS vector: Realized=500, open close-now=-450 => 50; minimum=10, buffer=5, tolerance=1 => threshold16, gate PASS при coverage. Reject vector: Realized=480, open=-470=>10<threshold16. Owner Money/FinalCloseCalculator+Scenarios/FinalClose. Tests: accept/reject, double count, stale/gap, partial/delayed, restart, unknown/foreign.