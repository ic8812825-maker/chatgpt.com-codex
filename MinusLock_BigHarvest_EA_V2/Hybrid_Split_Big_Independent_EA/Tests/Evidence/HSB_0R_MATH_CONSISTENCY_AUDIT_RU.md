# Аудит математической непротиворечивости HSB.0R

Статус: PASS на уровне нормативной документации; MQL5/MT5 evidence не выполнялось.

## Размерности

- F,C,T,S,N: lot.
- Rc,Rt,Rs,q: ratio.
- P: price; tick/point: price increment.
- DealNet, RecoveryPL, reserve, risk, margin, transition loss: account money.

## Три закона

1. Catch-Up: аналитический pre-gate не заменяет broker-money proof. Все money terms имеют одну валюту и один control snapshot.
2. Monotonicity: `C+T-S-F>0` после rounding — необходимое условие; production proof сравнивает RecoveryPL на каждой broker-valid цене и включает costs.
3. Compression: candidate и actual residual требуют `0<N<F`, minimum absolute/relative compression, next gross/risk decrease и operational next cycle.

## Ручной вектор

Демонстрационный, не production: F=1.00, Rc=1.60, Rt=0.25, Rs=0.60, step=0.01 → C=1.60,T=0.25,S=0.60,Bnet=1.25,slope=0.25 lot>0. При N=0.50: compression=0.50 lot, ratio=0.50; следующий gross уменьшается при тех же ratios. Денежный PASS не заявляется без OrderCalcProfit/actual broker properties.

Allocation conservation сохраняется per source; buckets не увеличивают RecoveryPL. Transition loss и Final threshold используют money. BUY/SELL зеркальны по ролям, но close-side Bid/Ask различается. Формула конечности применима только при доказанном rounded q<1; terminal lot завершает recursion.

Python не использовался.
