# Hybrid Split Big — тестовые векторы

| ID | Inputs | Expected decision | Required assertions |
|---|---|---|---|
| TV-01 | F=1.00,C=2.00,T=.80,S=.20,β=.90,N=.30,step=.01 | geometry candidate | KR=2.34; slope lots=1.60; NextBig=.84; then require real money/margin PASS |
| TV-02 | TV-01; NetF=-200,NetS=-40,NetT=30,NetCore=-100, budget=0, limit=0 | REJECT_TRANSITION_BUDGET | TransitionNet=-310; FinalReserve unchanged |
| TV-03 | F=.03, step=.01; raw N=.011; raw next gross=.029 | REJECT_ROUNDING if normalized gates fail | all lots normalized first; no raw-only PASS |
| TV-04 | F=.01,q=.30,min=step=.01 | terminal | Nraw=.003; no N=.01 promotion |
| TV-05 | β=.5,C=1.2,T=.1,S=.1,F=1 | REJECT_RESERVE_CATCHUP | KR=.6<1 |
| TV-06 | finite levels all Deficit>0 | REJECT_NO_FINITE_HARVEST_LEVEL | reject before opening legs |
| TV-07 | valid Big but no candidate N satisfies transition | REJECT_FUTURE_SMALL | reject before opening current basket |
| TV-08 | requested Core close .70, broker fills .35 | ERROR_PARTIAL_EXECUTION | no promotion, mandatory reconciliation |
| TV-09 | reserve event replay | ERROR_DOUBLE_COUNT_DETECTED | Rreal credited exactly once |
| TV-10 | Far BUY and mirrored Far SELL prices | equal normalized money result within tolerance | BUY close Bid / SELL close Ask |

For every vector run Base and Worst Case; store input prices, OrderCalcProfit/OrderCalcMargin output, costs, event keys and expected code.
