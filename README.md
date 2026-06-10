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

## Small-at-Far Scenario

Small-сценарий больше не исполняется сразу при первом движении в сторону Small. Если Small достиг защитного движения, советник переводит цикл в `STATE_WAIT_SMALL_TO_FAR` и ждёт, пока текущая цена дойдёт до цены открытия старого `Far` с учётом `SmallFarTouchOffsetPoints`. Для `Small=BUY` условие касания: `CurrentPrice >= OldFarOpenPrice + offset`; для `Small=SELL`: `CurrentPrice <= OldFarOpenPrice - offset`.

После касания старого Far выполняется `ProcessSmallAtFarTouch`: Small закрывается на 100%, старый Far закрывается на 100%, Big закрывается только на `CloseBigOnSmall`, а остаток Big становится новым Far. Затем обязательно сначала проверяется `FinalCloseAllowed` для нового Far. Если резерва хватает, новый Far закрывается полностью и состояние становится `STATE_CLOSED_PROFIT`; если резерва не хватает, только тогда открывается новый Big/Small от нового Far. В нормальном Small-at-Far сценарии `DUAL_TAIL` не должен появляться, потому что старый Far ликвидируется до назначения нового Far.
