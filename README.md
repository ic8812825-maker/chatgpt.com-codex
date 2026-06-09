# work

Внутри репозитория создан отдельный проект:

- `Adaptive-Lock-Expansion-ALE` — `Adaptive Lock Expansion (ALE)`.

Для ALE используется только одна выделенная ветка проекта: `ale` (опубликована в GitHub-репозитории).

## MQL5 проекты

- [MinusLock BigHarvest EA](MinusLock_BigHarvest_EA/) — MQL5-советник для разруливания минусовой позиции через Big-Harvest, реализованный на основе `manual/big_harvest_system_manual_ru.md`.

## Мануалы

- [Адаптивная Самосжимающаяся Система Разруливания Минусового Замка](manual/adaptive_self_compressing_minus_lock_manual_ru.md) — полный русский мануал по логике Big/Small, самосжатию хвоста, резерву, марже и аварийным режимам.
- [MinusLock SelfCompressing BigSmall v2](MinusLock_SelfCompressing_BigSmall_v2.xlsx) — новый Excel-калькулятор v2 с листами Settings, Calculator, Trend_UP, Trend_DOWN, Risk_Analysis, Tests, Manual и Examples.
- [TEST_REPORT MinusLock SelfCompressing BigSmall v2](TEST_REPORT_MinusLock_SelfCompressing_BigSmall_v2.md) — подробный отчёт тестирования Excel-калькулятора v2.

## Отчёты тестирования

- [Big-Harvest MQL5 EA final local verification](reports/tests/big_harvest_ea_final_report.md) — локальный отчёт статических и математических проверок советника; MetaEditor/Strategy Tester требуют отдельного запуска на Windows/MetaTrader.
