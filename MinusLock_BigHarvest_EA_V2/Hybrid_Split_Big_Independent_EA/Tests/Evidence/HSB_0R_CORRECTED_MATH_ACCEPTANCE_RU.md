# Расширенная ручная математическая приёмка HSB.0R-C

Версия HSB.0R-C.21
DOCUMENTARY_ALGEBRAIC_CONSISTENCY=PASS
BROKER_MONEY_RUNTIME_PROOF=NOT_PROVEN

Все числа — ДЕМОНСТРАЦИОННЫЙ ПРОФИЛЬ, НЕ PRODUCTION DEFAULT. Для упрощённых money-векторов 1 pip/lot=10 money; runtime обязан использовать OrderCalcProfit.

## V1 Far SELL
F=1.00 SELL; Rc=1.60,Rt=0.25,Rs=0.60; step .01. C=1.60 BUY,T=.25 BUY,S=.60 SELL; Bnet=1.25; slope=.25>0. Price 1.1000→1.1010: BUY close Bid, SELL close Ask; gross directional improvement≈.25×10 pips×10=25 money до costs. PASS analytic, runtime NOT_PROVEN.

## V2 Far BUY
F=1.00 BUY; C=1.60 SELL,T=.25 SELL,S=.60 BUY. При падении 1.1000→1.0990 SELL-side improvement зеркально 25 money до costs. BUY close Bid, SELL close Ask. PASS symmetry.

## V3 step .01
F=.73; raw C=1.168→1.16 floor; T=.1825→.18 floor; S=.438→.44 ceil; Bnet=.90; slope=.17>0. N-grid .01,.02,...,.72; fixed ratio не выбирает N.

## V4 coarse step .10
F=.70; raw C=1.12→1.10; T=.175→.10; S=.42→.50; Bnet=.70; slope=0, candidate profile REJECT. Demonstrates mandatory post-rounding gates.

## V5 terminal lot
Vmin=.01,Vstep=.01,F=.02. N=.01 даёт compression .01 и должен пройти next-cycle feasibility; если следующий C/T/S после rounding не проходит laws, N rejected и route terminal-safe/final-close preview.

## V6 два Small Transition
F0=1.00; actual residual F1=.49; следующий actual residual F2=.24. На step .01: 1.00>.49>.24; compression ratios .51 и .5102. Requested .50/.25 не используются.

## V7 allocation conservation
Source A DealNet=100: Reserve60+Partial20+Transition10+Carry5+Residual5=100. Source B DealNet=-12: allocatable=0, economic=-12. Duplicate A identical=NO-OP, totals unchanged. Same key payload 101=CONFLICT.

## V8 Final Close PASS
RealizedCycleNet=500. Open close-now components: projected profit -430, swap -5, expected close commission -10, execution buffer -5 => -450. RecoveryPL=50. Minimum=10, safety=5, tolerance=1; threshold=16; 50≥16 PASS. Coverage requirement430, allowed sources440 PASS. Reserve not added again.

## V9 Final Close reject
Realized=480, open close-now=-470 =>10<16 REJECT. Другой reject: RecoveryPL=30, но allowed coverage400<430.

## V10 Transition Loss caps
Actual deals: -80,+20,-10 => net -70, loss70. Caps: absolute100; equity 10000×1%=100; OldFarRisk500×15%=75; cumulative remaining60. Allowed=min=60; 70>60 REJECT.

## V11 Future Small recursion
F0=1.00→exact F1=.49→exact F2=.24. Для дальнейшего bound q=.50: F3≤.12,F4≤.06,F5≤.03; на Vmin=.01 finite, но каждый rounded cycle обязан пройти risk/margin/laws. Bound без gates недействителен.

## V12 невозможный следующий cycle
F=.10, step=.10, Vmin=.10: отсутствует broker-valid N с 0<N<F. Candidate set empty→REJECT→TERMINAL_SAFE; новый cycle не создаётся.

## Allocation/sign/range conclusions
Все формулы имеют lot/money/price dimensions; Far BUY/SELL проверены отдельно; floor C/T и ceil S применены; negative DealNet не создаёт allocation; double counting отсутствует.

OPEN_P0=0
OPEN_P1=0
OPEN_P2=0