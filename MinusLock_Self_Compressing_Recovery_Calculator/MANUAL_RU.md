# Руководство: самосжимающееся разруливание замка

## 1. Назначение системы
Система рассчитывает пошаговое разруливание локированной позиции с уменьшением рабочей базы на каждом уровне.

## 2. Отличие новой модели от старой
Старая модель считала уровни от неизменного StartLot. Новая модель использует self-compressing логику: следующий уровень рассчитывается от уменьшенного NearStart.

## 3. Логика DOWN
- Дальний старт: Start BUY
- Big: BUY
- Small: SELL
- Close: частичное закрытие Start BUY

## 4. Логика UP
- Дальний старт: Start SELL
- Big: SELL
- Small: BUY
- Close: частичное закрытие Start SELL

## 5. Формулы 90/40/30
- Big Raw = NearStart × 90%
- Small Raw = NearStart × 40%
- Max Close Far = NearStart × 30%
- NewNearStart = NearStart - BigRaw + SmallRaw = NearStart × 50%
- NewFarRemaining = FarRemainingBefore - ActualCloseFar
- NextBaseLot = MIN(NewNearStart, NewFarRemaining)

## 6. Max Close Far vs Actual Close Far
- Max Close Far — верхний лимит закрытия.
- Actual Close Far — реальное закрытие, зависит от выбранного режима.

## 7. Режим THEORETICAL
`ActualCloseFar = MIN(MaxCloseFar, FarRemainingBefore)`.
Это режим для обязательной показательной проверки 30% close.

## 8. Режим SAFE_PROFIT_BUDGET
`ActualCloseFar = MIN(MaxCloseFar, CloseByProfitBudget, FarRemainingBefore)`.
Если бюджета недостаточно, допускается `ActualCloseFar = 0`, `Close Status = NO CLOSE`.

## 9. Таблица StartLot=1 (ожидаемые close)
0.30 / 0.15 / 0.075 / 0.0375 / 0.01875.

## 10. Таблица StartLot=2 (ожидаемые close)
0.60 / 0.30 / 0.15 / 0.075 / 0.0375.

## 11. Таблица StartLot=5 (ожидаемые close)
1.50 / 0.75 / 0.375 / 0.1875 / 0.09375.

## 12. Блок Risk / Margin
Отдельный лист `РИСК_АНАЛИЗ` содержит:
уровень, накопленные Big/Small, open lots, net lot, margin, margin load, floating DD, equity, free margin, margin level и итоговый Risk Status.

## 13. Stop-условия
STOP при:
- BigRounded < LotStep
- SmallRounded < LotStep
- CloseRounded < LotStep
- NextBaseLot < LotStep
- Margin Load > 100%
- Margin Level < StopOutPercent
- FarRemaining <= 0

## 14. Human Summary
Для каждого уровня даётся комментарий с фактическими значениями операций (Big, Small, Actual Close, NewNearStart, NewFarRemaining).

## 15. Ограничения модели
Калькулятор аналитический; он не учитывает спред, своп, проскальзывание и изменение стоимости пункта по рынку.

## 16. Вердикт
Модель пригодна для сценарного анализа с разделением режимов THEORETICAL и SAFE_PROFIT_BUDGET и контролем маржинальной нагрузки.
