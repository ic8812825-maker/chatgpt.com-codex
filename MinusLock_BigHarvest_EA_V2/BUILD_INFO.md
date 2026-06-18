# MinusLock BigHarvest EA V2 Build Info

Build date: 2026-06-18 UTC
Branch: work
Target folder: MinusLock_BigHarvest_EA_V2
Commit purpose: V2.4.1 RiskGate lifecycle, real BigHarvest reserve, retry pending states, recovery reconciliation and defaults

Included features:
- Initial BUY/SELL lock with rollback
- Initial profit ignored
- Big-Harvest
- Small-at-Far V2.4
- Risk Compression Reverse
- New Big < Old Far rule
- SmallReserveShare reserve add
- FarDistanceMode
- REAL_PRICE_DISTANCE
- EffectiveFarDistancePoints
- Cycle Math CSV report
- Reverse Geometry Validator
- STOP_MAX_LEVELS / UNCLOSED_CYCLE
- Reverse limit close-new-Far handling
- Invalid geometry emergency handling
- Retry FSM state definitions
- Restart recovery through GlobalVariables
- Internal SIMULATION engine
- Real Recovery P/L Validation
- REAL_CYCLE_MATH log and CSV fields


V2.4.1 updates:
- RiskGate blocks only new openings; closes and retry/pending states continue even when spread is high.
- Pending close states have retry handlers with MaxCloseRetryAttempts and RetryLogIntervalSeconds.
- BigHarvest reserve and CloseFarBudget use real HistoryDeals net P/L when available.
- RecoverState persists/reconciles extra context and real open positions after restart.
- Spread blocked logs are throttled with RiskGateLogIntervalSeconds.
- Defaults updated: CloseFarShare=0.40, ReserveShare=0.60, MaxReverseCycles=7, MaxSpreadPoints=60.0.
