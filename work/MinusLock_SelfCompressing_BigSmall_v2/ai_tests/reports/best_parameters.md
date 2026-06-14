# Best Parameters — Python Model Candidates

> Python-модель показывает лучший кандидат. Финальное подтверждение обязательно через MT5 Strategy Tester.

## Top 10 лучших вариантов

1. CF/RS=0.50/0.50, SmallRatio=0.36, CloseBig=0.35, MaxLevels=5, State=STATE_CLOSED_PROFIT, PL=21.5
2. CF/RS=0.50/0.50, SmallRatio=0.36, CloseBig=0.35, MaxLevels=7, State=STATE_CLOSED_PROFIT, PL=21.5
3. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.30, MaxLevels=5, State=STATE_CLOSED_PROFIT, PL=21.0
4. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.30, MaxLevels=7, State=STATE_CLOSED_PROFIT, PL=21.0
5. CF/RS=0.50/0.50, SmallRatio=0.36, CloseBig=0.30, MaxLevels=5, State=STATE_CLOSED_PROFIT, PL=19.5
6. CF/RS=0.50/0.50, SmallRatio=0.36, CloseBig=0.30, MaxLevels=7, State=STATE_CLOSED_PROFIT, PL=19.5
7. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=5, State=STATE_CLOSED_PROFIT, PL=18.0
8. CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.25, MaxLevels=7, State=STATE_CLOSED_PROFIT, PL=18.0
9. CF/RS=0.50/0.50, SmallRatio=0.37, CloseBig=0.35, MaxLevels=5, State=STATE_CLOSED_PROFIT, PL=18.0
10. CF/RS=0.50/0.50, SmallRatio=0.37, CloseBig=0.35, MaxLevels=7, State=STATE_CLOSED_PROFIT, PL=18.0

## Top 10 худших вариантов

1. CF/RS=0.70/0.30, SmallRatio=0.40, CloseBig=0.25, MaxLevels=3, State=STATE_UNCLOSED_CYCLE, PL=-118.6, Reason=STOP_MAX_LEVELS after Small-at-Far
2. CF/RS=0.90/0.10, SmallRatio=0.40, CloseBig=0.25, MaxLevels=3, State=STATE_UNCLOSED_CYCLE, PL=-118.2, Reason=STOP_MAX_LEVELS after Small-at-Far
3. CF/RS=0.50/0.50, SmallRatio=0.40, CloseBig=0.25, MaxLevels=3, State=STATE_UNCLOSED_CYCLE, PL=-117.0, Reason=STOP_MAX_LEVELS after Small-at-Far
4. CF/RS=0.60/0.40, SmallRatio=0.40, CloseBig=0.25, MaxLevels=3, State=STATE_UNCLOSED_CYCLE, PL=-116.8, Reason=STOP_MAX_LEVELS after Small-at-Far
5. CF/RS=0.80/0.20, SmallRatio=0.40, CloseBig=0.25, MaxLevels=3, State=STATE_UNCLOSED_CYCLE, PL=-116.4, Reason=STOP_MAX_LEVELS after Small-at-Far
6. CF/RS=0.90/0.10, SmallRatio=0.38, CloseBig=0.25, MaxLevels=3, State=STATE_UNCLOSED_CYCLE, PL=-115.9, Reason=STOP_MAX_LEVELS after Small-at-Far
7. CF/RS=0.90/0.10, SmallRatio=0.37, CloseBig=0.25, MaxLevels=3, State=STATE_UNCLOSED_CYCLE, PL=-115.8, Reason=STOP_MAX_LEVELS after Small-at-Far
8. CF/RS=0.60/0.40, SmallRatio=0.38, CloseBig=0.25, MaxLevels=3, State=STATE_UNCLOSED_CYCLE, PL=-115.6, Reason=STOP_MAX_LEVELS after Small-at-Far
9. CF/RS=0.60/0.40, SmallRatio=0.37, CloseBig=0.25, MaxLevels=3, State=STATE_UNCLOSED_CYCLE, PL=-115.2, Reason=STOP_MAX_LEVELS after Small-at-Far
10. CF/RS=0.60/0.40, SmallRatio=0.36, CloseBig=0.25, MaxLevels=3, State=STATE_UNCLOSED_CYCLE, PL=-114.8, Reason=STOP_MAX_LEVELS after Small-at-Far

## Почему текущий 90/10 проваливается

90/10 направляет большую часть Big-harvest NetProfit в частичное закрытие Far и оставляет слишком маленький резерв. После Small-at-Far переворотов новый Far может остаться достаточно большим, а TotalReserve не покрывает FarRemainLoss до MaxHarvestLevels.

## Какой вариант лучше: 70/30, 60/40 или 50/50

По Python-модели лучший кандидат из этой группы: CloseFarShare=0.50, ReserveShare=0.50, SmallRatio=0.36, CloseBigOnSmall=0.35, MaxHarvestLevels=5.
