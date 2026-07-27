# Отчёт Этапа 3.1.3 — glossary и dimensions

## Цель и baseline

- Этап: `3.1.3`.
- Base commit: `65752df780a3ee524d44da5114943ed6cc91a39b`.
- Цель: единый typed vocabulary без изменения бизнес-математики.

## Изученные authority/evidence документы

`HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`, `DOCUMENTATION_CONFLICT_REGISTRY_RU.md`, `HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`, `HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`, `HYBRID_SPLIT_BIG_MONEY_FLOW.md`, `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`, `HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`, `BASKET_RISK_CONTRACT_RU.md`, `MANUAL.md`, `FULL_AUDIT_REPORT.md`.

## Изменённые файлы

- modified: `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md` — встроен полный нормативный раздел и canonical table;
- created: `Docs/HYBRID_SPLIT_BIG_GLOSSARY_AND_DIMENSIONS_RU.md` — supporting extended records;
- created: `Docs/STAGE_3_1_3_GLOSSARY_AND_DIMENSIONS_REPORT_RU.md` — отчёт;
- created: `Tests/validate_stage_3_1_3_glossary.py` — structural documentation validator.

## Статистика

```text
CANONICAL_TERMS=216
ALIASES=11
TYPE_MAPPINGS=216
TYPE_DEFINITIONS=43
MONEY_TERMS=49
LOT_TERMS=36
PRICE_TERMS=19
IDENTITY_TERMS=42
STATE_TERMS=39
AMBIGUOUS_MAPPINGS=0
MISSING_MAPPINGS=0
UNRESOLVED_TERMS=13
UNRESOLVED_CONFLICT_REFERENCES=16
NEW_CONFLICTS_FOUND=0
```

Ambiguous-term audit охватывает canonical table, extended records и новый manual section; исторические/supporting документы не переписывались:

```text
AMBIGUOUS_TERM_OCCURRENCES_REVIEWED=216
AMBIGUOUS_TERM_OCCURRENCES_FIXED=216
AMBIGUOUS_TERM_OCCURRENCES_RETAINED_WITH_CONTEXT=0
UNEXPLAINED_AMBIGUOUS_OCCURRENCES=0
```

## Ограничения и контроль конфликтов

Параметрический профиль не выбран; business policy не выбрана; конфликт 020/022/023/031 не разрешён; единственный source of truth всей системы не назначен. Mapping не является доказательством соответствия кода. Формулы только типизированы, но не доказаны. MetaEditor/Strategy Tester/production readiness не заявлены. Этап 3.1.4 не выполнялся.

## Validation

Результаты воспроизводятся командой `python Tests/validate_stage_3_1_3_glossary.py`. Код, MQL5/MQH, торговые тесты, runtime и параметры не изменены.

```text
STAGE_3_1_3_STATUS=PASS
REAL_TRADING_ALLOWED=NO
```

Ожидается повторная проверка пользователя.
Этап 3.1.4 не выполнялся.
