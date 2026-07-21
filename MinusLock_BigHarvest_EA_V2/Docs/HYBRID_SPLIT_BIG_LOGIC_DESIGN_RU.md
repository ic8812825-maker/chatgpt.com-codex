# Hybrid Split Big / Strong Far Compression — нормативный проект

## Статусы и граница применения

| Статус | Значение |
|---|---|
| DESIGN_PROPOSED | Заменён новой выбранной схемой ниже. |
| DESIGN_ANALYTICALLY_VALIDATED | PASS: неравенства, ручные примеры и broker rounding проверены. |
| DESIGN_SELECTED | PASS: выбран `Target NewFar + TransitionPlan`. |
| MQL5_IMPLEMENTED | PASS: денежный preview, план, phase states и gates реализованы. |
| CODE_MATCHES_DESIGN | PASS: таблица соответствия в implementation report. |
| PYTHON_TESTED | PASS: независимая модель повторяет формулы данного документа. |
| MT5_TESTED | PENDING: требует MetaEditor и Strategy Tester. |
| FINAL_APPROVED | PENDING до MT5-тестов. |

Этот документ является источником требований; Python не является источником
торговой логики. `UseHybridSplitBigGeometry=false` сохраняет прежний путь.

## 1. Аудит и рассмотренные архитектуры

Текущий Split использует `C=1.60F`, `T=0.25F`, `S=0.60F` и фиксированный
остаток Core 0.60, то есть `NewFar=0.96F`: компрессия 4% неприемлема. Были
рассмотрены: **A** fixed remain, **B** Target NewFar, **C** Target NewBig,
**D** money-minimum NewFar, **E** dynamic target, **F** temporary hedge,
**G** staged Core close. A отклонён из-за отсутствия денежного gate; F — из-за
дополнительного хвоста/margin; C является ограничением B; D/E являются
политиками поиска B; G — безопасный порядок исполнения B. Выбрана схема
**B+G**: target-first, затем staged close до фактического остатка; BigTrend
закрывается и никогда не становится Far.

## 2. Обозначения и денежные корзины

`F` — OldFar, `C` — BigCore, `T` — BigTrend, `S` — SmallBase. В Big: C/T
против F, S вместе с F. Все суммы разделены: `TotalReserve` содержит только
подтверждённые ledger credits; `PartialFarBudgetCarry` — только partial Far;
`TransitionCompressionBudget` — только завершённый reverse; floating P/L и
Initial Profit не принадлежат ни одной из них. Для любого completed action:

`RealizedNet = ReserveCredit + PartialFarBudgetUsed + TransitionBudgetUsed + UnallocatedNet`.

Один deal/ledger event может попасть ровно в одну корзину.

## 3. Big geometry и доказательства

Кандидат после broker floor-to-step: `C=cF`, `T=tF`, `S=sF`.

* Recovery slope: `R'=V(C+T-S-F)`. Требование `R' >= MinimumRecoverySlopeMoneyPerPoint`.
* Projected recovery обязан возрастать минимум на
  `MinimumRecoveryImprovementMoney` **на каждом 1-point шаге** от 0 до
  `target+max(500,FarDistance)`; диагностически в журнале выделяются
  `{0,1,5,10,25,50,target,target+50,target+FarDistance}`.
  Расчёт использует тот же `CalcProjectedPositionNetMoney`, что и EA, включая
  Bid/Ask, commission, swap, fee, spread, slippage и execution buffer.
* Projected reserve slope: `Q'=ReserveShare*V(C+T-S)`; Far loss slope
  `L'=V*F`. Требование `Q'/L' >= MinimumReserveCatchUpRatio > 1`.
  Это **projected coverage**, не `TotalReserve`; фактический Reserve кредитуется
  только после HistoryDeal lifecycle net на Big harvest.
* Basket/margin/position gate проверяются до открытия. При любом FAIL уровень
  не открывается.

## 4. Target NewFar и следующий Big

Сначала строится целевой объём `N`: solver перебирает volume-step кандидаты от
`min(TargetNewFarRatio*F, C)` вниз/вверх в допустимом диапазоне. Для каждого:

`CloseCore=C-N`, `q=N/F`, `NextGross=(c+t)N`,
`NextDirectional=(c+t-s-1)N`.

Требуются `0<N<F`, risk(N)<risk(F), валидная следующая Big geometry, positive
next recovery slope, next catch-up и margin gate. Сначала выбирается кандидат с
`NextGross<F`; если его нет, допускается только `NextDirectional<F`; иначе
reverse запрещён. Поэтому NewFar не назначается автоматически.

При `q<=qMax<1`, с broker floor-to-step, число reverse ограничено
`Nmax=ceil(log(Fmin/F0)/log(qMax))+1`. Для qMax=0.70 и step/minlot=0.01:
0.01→0, 0.05→6, 0.10→8, 0.50→13, 1→14, 2→16, 5→19, 10→21.

## 5. TransitionPlan и Small порядок

До первого необратимого close создаётся и сохраняется `HybridReversePlan`:
identifiers F/C/T/S, target, required Core close, projected nets each leg,
transition net, Reserve floor, next geometry, margin, selected policy and
fallback. Нет valid plan — OldFar закрывать запрещено.

Выбранный фазовый порядок: (1) detect/confirm Small; (2) build/validate plan;
(3) close S и сверить deal; (4) close OldFar и сверить; (5) close T и сверить;
(6) пересчитать actual transition budget; (7) partial close C до target;
(8) проверить actual remainder, risk и preview next; (9) promote C→Far;
(10) final gate/open next. При неполном close, unknown identifier, history
unavailable или restart продолжение возможно только из сохранённого phase; при
неразрешимом состоянии — manual intervention, а не новый ордер.

## 6. State machine и аварийные случаи

`STATE_HYBRID_FAR_ACTIVE → GEOMETRY_BUILD → GEOMETRY_VALIDATE → OPEN_CORE →
OPEN_SMALL_BASE → OPEN_TREND → ACTIVE`. Big: `BIG_TRIGGERED → CLOSE_CORE →
CLOSE_TREND → CLOSE_SMALL → CALC_NET → FULL_FAR_GATE → PARTIAL_FAR →
RESERVE_ADD → FINAL_GATE`. Small: `SMALL_DETECTED → WAIT_OLD_FAR →
REVERSE_CONFIRM → REVERSE_PLAN → REVERSE_VALIDATE → REVERSE_CLOSE_SMALL →
REVERSE_CLOSE_OLD_FAR → REVERSE_CLOSE_TREND → REVERSE_COMPRESS_CORE →
REVERSE_VERIFY_CORE → REVERSE_PREVIEW_NEXT → REVERSE_PROMOTE_FAR →
REVERSE_FINAL_GATE → REVERSE_OPEN_NEXT`.

All close/open failures use existing pending/retry contracts; no phase clears
context before `VerifyFullClose`/actual-volume readback. A missing role,
orphan, invalid margin/spread, MaxReverseCycles, incomplete plan, insufficient
Reserve catch-up or non-monotonic price trace enters invalid/manual safe state.
All lookups and plan identity are Symbol+MagicNumber+CycleId+Identifier+Role.

## 7. Ручной пример (Far SELL; BUY зеркально через Bid/Ask)

Для `F=1.00`, `C=2.00`, `T=0.80`, `S=0.20`, ReserveShare=.90: recovery slope
`=1.60V`; reserve slope `=.90*2.60V=2.34V`, т.е. catch-up 2.34. Target N=.30:
закрывается 1.70 Core, `q=.30`, next gross `.84F`, next directional `.48F`.
При Far BUY все directions зеркальны, а projected closes используют BUY→Bid,
SELL→Ask через existing broker money model. Для F=.10/1/2/5 получаются
C=.20/2/4/10, T=.08/.8/1.6/4, S=.02/.2/.4/1 и N=.03/.3/.6/1.5 до rounding;
если N<min lot, план не создаётся.

## 8. Финальный вердикт

Сильная компрессия разрешается не коэффициентом, а только `HybridReversePlan`,
который доказывает текущую и следующую геометрию до закрытия OldFar. Final
Reserve не расходуется на обычную compression. MT5 validation остаётся
обязательной для FINAL_APPROVED.
