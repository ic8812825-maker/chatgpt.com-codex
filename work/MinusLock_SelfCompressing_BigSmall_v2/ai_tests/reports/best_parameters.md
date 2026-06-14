# Best Parameters — Python Model Candidates

> Python-модель показывает лучший кандидат. Финальное подтверждение обязательно через MT5 Strategy Tester.

## Top 10 лучших вариантов

1. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=3, State=STATE_CLOSED_PROFIT, PL=42.0
2. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=3, State=STATE_CLOSED_PROFIT, PL=42.0
3. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=3, State=STATE_CLOSED_PROFIT, PL=42.0
4. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=5, State=STATE_CLOSED_PROFIT, PL=42.0
5. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=5, State=STATE_CLOSED_PROFIT, PL=42.0
6. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=5, State=STATE_CLOSED_PROFIT, PL=42.0
7. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=7, State=STATE_CLOSED_PROFIT, PL=42.0
8. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=7, State=STATE_CLOSED_PROFIT, PL=42.0
9. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=7, State=STATE_CLOSED_PROFIT, PL=42.0
10. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.30, MaxLevels=3, State=STATE_CLOSED_PROFIT, PL=42.0

## Top 10 худших вариантов

1. CF/RS=0.90/0.10, SmallRatio=0.35, CloseBig=0.35, MaxLevels=3, State=STATE_INVALID_SMALL_GEOMETRY, PL=8.4, Reason=SmallReverseNet <= 0
2. CF/RS=0.90/0.10, SmallRatio=0.35, CloseBig=0.35, MaxLevels=3, State=STATE_INVALID_SMALL_GEOMETRY, PL=8.4, Reason=SmallReverseNet <= 0
3. CF/RS=0.90/0.10, SmallRatio=0.35, CloseBig=0.35, MaxLevels=3, State=STATE_INVALID_SMALL_GEOMETRY, PL=8.4, Reason=SmallReverseNet <= 0
4. CF/RS=0.90/0.10, SmallRatio=0.35, CloseBig=0.35, MaxLevels=5, State=STATE_INVALID_SMALL_GEOMETRY, PL=8.4, Reason=SmallReverseNet <= 0
5. CF/RS=0.90/0.10, SmallRatio=0.35, CloseBig=0.35, MaxLevels=5, State=STATE_INVALID_SMALL_GEOMETRY, PL=8.4, Reason=SmallReverseNet <= 0
6. CF/RS=0.90/0.10, SmallRatio=0.35, CloseBig=0.35, MaxLevels=5, State=STATE_INVALID_SMALL_GEOMETRY, PL=8.4, Reason=SmallReverseNet <= 0
7. CF/RS=0.90/0.10, SmallRatio=0.35, CloseBig=0.35, MaxLevels=7, State=STATE_INVALID_SMALL_GEOMETRY, PL=8.4, Reason=SmallReverseNet <= 0
8. CF/RS=0.90/0.10, SmallRatio=0.35, CloseBig=0.35, MaxLevels=7, State=STATE_INVALID_SMALL_GEOMETRY, PL=8.4, Reason=SmallReverseNet <= 0
9. CF/RS=0.90/0.10, SmallRatio=0.35, CloseBig=0.35, MaxLevels=7, State=STATE_INVALID_SMALL_GEOMETRY, PL=8.4, Reason=SmallReverseNet <= 0
10. CF/RS=0.80/0.20, SmallRatio=0.35, CloseBig=0.35, MaxLevels=3, State=STATE_INVALID_SMALL_GEOMETRY, PL=16.8, Reason=SmallReverseNet <= 0

## Почему текущий 90/10 проваливается

90/10 направляет большую часть Big-harvest NetProfit в частичное закрытие Far и оставляет слишком маленький резерв. После Small-at-Far переворотов новый Far может остаться достаточно большим, а TotalReserve не покрывает FarRemainLoss до MaxHarvestLevels.

## Какой вариант лучше: 70/30, 60/40 или 50/50

По Python-модели лучший кандидат из этой группы: CloseFarShare=0.50, ReserveShare=0.50, SmallRatio=0.36, CloseBigOnSmall=0.35, MaxHarvestLevels=5.

## Recommended Candidate for MT5 Confirmation

- BigRatio = 1.30
- SmallRatio = 0.36
- CloseBigOnSmall = 0.35
- RemainBigOnSmall = 0.65
- CloseFarShare = 0.50
- ReserveShare = 0.50
- MaxHarvestLevels = 5
- MaxReverseCycles = 10

Это не финальная победа стратегии. Это кандидат Python-модели. Финальное подтверждение обязательно через MT5 Strategy Tester.
