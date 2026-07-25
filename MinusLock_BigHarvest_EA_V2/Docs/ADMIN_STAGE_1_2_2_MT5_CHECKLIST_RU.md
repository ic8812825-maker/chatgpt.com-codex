# Проверка Stage 1.2.2 Администратором

1. Откройте `Tests/MQL5/HybridSplitBig/HybridCatchUpRouteHardeningTests.mq5`.
2. Скопируйте проект с сохранением относительных путей либо поместите runner в `MQL5/Scripts/HybridSplitBig`; `Include` проекта должен быть доступен по путям `../../../Include`.
3. Откройте файл в MetaEditor и выполните Compile.
4. Ожидаемый, но не подтверждённый программистом результат: `0 errors, 0 warnings`.
5. В MT5 Navigator обновите Scripts и запустите runner на символе с доступными Bid/Ask и volume properties.
6. Откройте Toolbox → Experts/Journal.
7. Каждая строка `ROUTE_HARDENING_TEST|ID=...|PASS` означает локальный PASS.
8. Итог должен быть `ROUTE_HARDENING_TEST|SUMMARY|Passed=...|Failed=0`.
9. Передайте полный compile log и все строки `ROUTE_HARDENING_TEST` для следующего анализа; не ограничивайтесь итоговой строкой.
