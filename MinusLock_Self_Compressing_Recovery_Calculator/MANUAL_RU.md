# MANUAL_RU
1. Назначение системы: самосжимающееся разруливание замка.
2. Логика DOWN: Start BUY, Big BUY, Small SELL, частичный close Start BUY.
3. Логика UP: Start SELL, Big SELL, Small BUY, частичный close Start SELL.
4. Формулы: Big 90%, Small 40%, Close 30%, NextNearStart=Near-Big+Small, NextBase=min(NewNear,NewFar).
5. Параметры: блок ПАРАМЕТРЫ на листе «Калькулятор».
6. Таблицы StartLot 1/2/5 подтверждают геометрию сжатия x0.5.
7. Risk/Margin: маржа, нагрузка, Margin Level, worst-case risk status.
8. Human Summary: текст на уровне каждой итерации.
9. Stop-условия: по лотшагу, марже, stopout и истощению дальнего старта.
10. Вердикт: пригодно для аналитики сценариев DOWN/UP.
