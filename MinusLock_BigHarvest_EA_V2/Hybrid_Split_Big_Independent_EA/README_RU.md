# Hybrid Split Big — независимый проект

Статус: `HSB.0 — нормативная документация`.

Проект создаётся с нуля как единственная система `HYBRID_SPLIT_BIG_ONLY`. Legacy Big/Small, отдельный Split Big, DUAL_TAIL, второй Far и старые execution-модули запрещены.

Главный мануал: `Docs/03_FULL_SYSTEM_MANUAL_RU.md`.
Карта проекта: `PROJECT_MAP_RU.md`.

```text
PRODUCTION_CODE_STARTED=NO
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=NOT_APPLICABLE
MT5_STRATEGY_TESTER=NOT_APPLICABLE
NEXT_ALLOWED_STAGE=NONE
```

Порядок работы: сначала завершить и принять HSB.0, затем только по отдельному разрешению Администратора начинать HSB.1. Любая будущая MQL5-функция обязана ссылаться на стабильный Requirement ID `HSBI-*`.
