# HSBI-DEC-001 — коэффициенты корзины

Статус: `DEFERRED_WITH_SAFE_CONTRACT`.

## Норма

`C=FloorGrid(F×Rc)`, `T=FloorGrid(F×Rt)`, `S=CeilGrid(F×Rs)`. Размерность F,C,T,S — lot; Rc,Rt,Rs — ratio.

Обязательные диапазоны: `Rc>0`, `Rt>=0`, `Rs>0`; symbol min/max/step обязательны. После округления: `C+T-S>F`; `FinalReserveShare×MoneyGain(C,T,S)>FarLossIncrease+ExecutionBuffer`; `0<N<F`; `Rc×RemainBigCoreOnSmall<1` является только аналитическим pre-gate.

Research profile: `Rc=1.60, Rt=0.25, Rs=0.60`, `RESEARCH_PROFILE_ONLY`, не real default. Любой профиль отклоняется при нарушении broker-normalized трёх законов, margin/risk/Future Small gates.

BUY/SELL симметрия: для Far SELL роли C,T — BUY, S — SELL; для Far BUY наоборот. MQL5 owner: `Planning/GeometrySolver`, tests: rounding, law gates, BUY/SELL symmetry, coarse step.
