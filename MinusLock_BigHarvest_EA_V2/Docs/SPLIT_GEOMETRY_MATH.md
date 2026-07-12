# Split Geometry Math: BigCore + BigTrend + SmallBase + DynamicReverseSmall

## Core ratios

Let:

```text
F = Far lot
A = BigCoreRatio
B = BigTrendRatio
C = SmallBaseToFarRatio
R = ReserveShare
K = CloseBigCoreOnSmall
M = RemainBigCoreOnSmall
```

Positions:

```text
BigCore = F * A
BigTrend = F * B
SmallBase = F * C
```

## Required invariants

### 1. Big net exposure exceeds Far

```text
A + B - C > 1
```

With baseline values:

```text
1.60 + 0.25 - 0.60 = 1.25 > 1
```

### 2. Reserve grows faster than new Far loss

```text
ReserveShare * (A + B - C) > 1
```

Baseline:

```text
0.90 * 1.25 = 1.125 > 1
```

### 3. New Far is smaller after Small transition

```text
A * M < 1
```

Baseline:

```text
1.60 * 0.60 = 0.96 < 1
```

## DynamicReverseSmall formula

After a confirmed reverse and BigTrend close:

```text
ProjectedClosedCoreLoss = ProjectedCloseLoss(BigCoreTicket, BigCoreLot * CloseBigCoreOnSmall, FarTouchPrice)
ProjectedSmallBaseProfit = ProjectedCloseProfit(SmallBaseTicket, SmallBaseLot, FarTouchPrice)
MoneyDeficit = max(0, ProjectedClosedCoreLoss - ProjectedSmallBaseProfit - ActualBigTrendNet + ReverseSmallSafetyMoney)
ReverseSmallLotMoney = MoneyDeficit / ProjectedProfitPerLotToFar
DirectionBufferLot = OldFarLot * ReverseDirectionBufferRatio
ReverseSmallLotDirection = BigCoreLot - OldFarLot - SmallBaseLot + DirectionBufferLot
ReverseSmallLot = NormalizeLotUp(max(ReverseSmallLotMoney, ReverseSmallLotDirection, SymbolMinLot))
```

Stage 1 adds the inputs, persisted context and validation for these formulas. Trading-state rewiring is intentionally staged separately.
