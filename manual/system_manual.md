# Adaptive Lock EV System Manual

## 1. Назначение
Система управления позицией и риском для извлечения edge mean reversion.
## 2. Архитектура
EDGE, REGIME FILTER, POSITION ENGINE, RISK ENGINE.
## 3. Формулы
Z=(P-EMA)/ATR_short; V=ATR_short/ATR_long; EV=mu*Q*PipValue-Cost.
## 4. Edge
Входы только при |Z|>=1.5.
## 5. Regime Filter
MEAN_REVERT <1.2; NEUTRAL 1.2..1.5; VOLATILE >1.5.
## 6. Position Engine
Q=0.01+0.01*min(|Z|/2,1), bounded [0.01,0.02].
## 7. Adaptive Beta
beta=0.7-0.4*confidence; DD>10% => 0.8.
## 8. Risk Engine
MaxTotalLot=0.30; MaxExposure=0.05; no new entries on limit breach.
## 9. FSM
FLOW / STRESS / ESCAPE based on DD and hard stops.
## 10. Excel Calculator Logic
Workbook `adaptive_lock_ev_calculator.xlsx` with mandatory sheets.
## 11. Python Test Logic
Unit tests in `/tests` validate formulas and recommendation constraints.
## 12. Ограничения системы
Не применять в устойчивом тренде или при VOLATILE режиме.
## 13. Версия и изменения
v2.0 initial implementation.
