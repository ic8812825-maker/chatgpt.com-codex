# Отчёт этапа HSB.0R — разрешение нормативных решений

## Исходное состояние

- Репозиторий: `ic8812825-maker/chatgpt.com-codex`.
- Ветка: `work`.
- Проект: `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA`.
- Исходный HEAD: `5e9668a6bccfd5913c656ba0d08e97de74d507fb`.
- Разрешён только документальный этап HSB.0R.
- HSB.1 не начат.
- Исполняемые `.mq5/.mqh` в новом проекте отсутствуют; каталоги Include содержат только `.gitkeep`.
- Python-разработка и торговые тесты не выполняются.

```text
HSB_STAGE_0R_STATUS=IN_PROGRESS
HSB_STAGE_0_DOCUMENTATION=BLOCKED
NEXT_ALLOWED_STAGE=HSB.1V
HSB_STAGE_1_STARTED=NO
PRODUCTION_CODE_STARTED=NO
REAL_TRADING_ALLOWED=NO
```

## Правило приёмки

Каждое HSBI-DEC-001..012 закрывается только после определения формул, размерностей, BUY/SELL-семантики, broker rounding, reject conditions, будущего MQL5 owner и тестов. Конкретные оптимизируемые значения допускается оставить конфигурацией только через `DEFERRED_WITH_SAFE_CONTRACT`.

Версия: HSB.0R.1
Статус: IN_PROGRESS
