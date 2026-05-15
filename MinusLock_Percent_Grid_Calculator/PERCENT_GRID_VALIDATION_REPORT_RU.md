# Отчёт полной проверки MinusLock Percent Grid Calculator

1. Файл открыт: **ДА** (`projects/minus-lock-system/MinusLock_Percent_Grid_Calculator.xlsx`).
2. Все листы есть: **ДА**.
3. Settings: **OK** (параметры присутствуют: StartLot, PointStep, MaxLevels, LotStep, RoundMode, TargetSkewMin%, TargetSkewMax%, UseRounding, Direction).
4. Базовая сетка: **OK** (1..5 = 90/30, 30/15, 20/15, 10/10, 5/5; Big>=Small соблюдено).
5. DownTrend (эталон StartLot=1.00): **OK**.
6. UpTrend зеркальность: **OK**.
7. Формула закрытия (MIN/MAX) по уровням 1..3: **OK**.
8. ManualClose override (L1=50%): **OK**.
9. Реальные лоты StartLot=0.10 (без округления): **OK**. Расчёт: [(0.09, 0.03, 0.06, 0.04, 0.13, 0.13), (0.03, 0.015, 0.03, 0.01, 0.13, 0.145), (0.02, 0.015, 0.0, 0.01, 0.15, 0.16)].
10. Ограничения: **OK** (добавлены явные проверки StartLot, MaxLevels, LotStep, неотрицательных процентов и лимитов закрытия).
11. Округление: **OK** (защитное: Big округляется вниз, Small вверх; Close округляется вниз для сохранения баланса).
12. Summary: **OK** (поля есть, финал для базового DOWN: BUY=165, SELL=175, Skew=10, id1=10, Status=OK).
13. Графики: **OK** (найдено 3 графика(ов)).

## Вердикт
**Работает с базовым сценарием и зеркальным UP, включая защитные входные проверки и защитное округление.**

