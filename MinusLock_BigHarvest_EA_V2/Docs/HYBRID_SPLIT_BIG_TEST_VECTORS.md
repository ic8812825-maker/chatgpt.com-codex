# Hybrid Split Big — воспроизводимые test vectors

Все vectors используют broker-agnostic linear adapter из `Tests/HybridSplitBig`, currency USD, explicit input JSON и expected decision code. Это не MT5 parity claim: перед терминальным внедрением значения P/L/Margin заменяются `OrderCalcProfit`/`OrderCalcMargin` outputs.

## Общая модель
`point_value=10`; base Bid/Ask `99.90/100.10`; commission=2 per closed leg; swap=fee=0; slippage=.10; volume min/step `.01`, max `100`; margin `100`/lot; α=.20, β=.70, γ=.10; Harvest levels `100,200,300`. Полный JSON содержит Symbol, currency, direction, Bid/Ask/spread, all open prices/lots, costs, reserve, shares, transition limits, volume, margin and levels.

| ID | Scenario | Key input / expected result |
|---|---|---|
| TV-01 | Far BUY full PASS | F=1,C=2,T=.8,S=.2,N=.3; KR=2.34, slope=1.6, NextBig=.84; `PASS_ALL_LAWS` |
| TV-02 | Far SELL mirror | mirrored prices; same adapter money; `PASS_ALL_LAWS` |
| TV-03 | law 1 fail | β=.5,C=1.2,T=.1,S=.1,F=1; KR=.6; `REJECT_RESERVE_CATCHUP` |
| TV-04 | law 2 fail | `C+T-S-F<=0`; `REJECT_BIG_SLOPE` |
| TV-05 | no finite Catch-Up | every level Deficit>0; `REJECT_NO_FINITE_HARVEST_LEVEL` |
| TV-06 | finite level | deficit reaches <=0 at declared level; `PASS_FINITE_CATCHUP` |
| TV-07 | geometry/money conflict | TransitionNet=-310, loss cap=0; `REJECT_TRANSITION_BUDGET` |
| TV-08 | cumulative loss | first loss accepted by per cap, second exceeds cumulative cap; `REJECT_CUMULATIVE_TRANSITION_LOSS` |
| TV-09 | raw rounding failure | raw candidate valid, normalised candidate fails; `REJECT_ROUNDING` |
| TV-10 | minimum lot | F=.01, raw N=.003; `TERMINAL_SAFE_STATE` or Final Close precheck |
| TV-11 | reserve replay | same Harvest event twice; `ERROR_DOUBLE_COUNT_DETECTED` |
| TV-12 | double commission | included commission repeated in exit cost; `ERROR_DOUBLE_COMMISSION` |
| TV-13 | partial fill | requested .70, filled .35; `ERROR_PARTIAL_EXECUTION` |
| TV-14 | final mismatch | forecast passes, confirmed actual below tolerance; `ERROR_FINAL_RESULT_MISMATCH` |
| TV-15 | margin upper bound | conservative upper exceeds limit; `REJECT_MARGIN` |
| TV-16 | T=0 policy | optional mode not approved; `REJECT_OPTIONAL_BIGTREND_POLICY` |
| TV-17 | S=0 policy | optional mode not approved; `REJECT_OPTIONAL_SMALLBASE_POLICY` |
| TV-18 | future depth | depth-1 continuation fails; `REJECT_FUTURE_SMALL` |
| TV-19 | Worst Case | base pass, configured worst fails; `WORST_CASE_FAIL` |
| TV-20 | restart | restored ledger/context mismatch; `ERROR_RESTORE_RECONCILIATION` |

Expected allocation for the completed positive Harvest example `E=44.20`: Partial=`8.84`, Reserve=`30.94`, Carry=`4.42`, residual=`0.00`. Negative Harvest creates zero allocations and is recorded only in `RealizedCyclePL`.

**Единые определения:** `TransitionNet` — знаковый итог Small Transition; `FinalReserveReal` — только confirmed protected reserve; `CoverageDeficit` — remaining Far close cost plus buffer minus `FinalReserveReal`. Эти определения идентичны основному мануалу и formula reference.
