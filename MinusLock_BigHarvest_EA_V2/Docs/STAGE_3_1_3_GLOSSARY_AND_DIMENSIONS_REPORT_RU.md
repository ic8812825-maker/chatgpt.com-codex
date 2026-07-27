# Коррекция Этапа 3.1.3 — семантический glossary и identifier mapping

## Причина коррекции

Предыдущая версия была структурно полной, но использовала массовые определения/lifecycle и placeholder mapping. Коррекция сохраняет весь прежний словарь, добавляет требуемые canonical aliases и заменяет records term-specific инженерными определениями. Base commit: `065f579d64e4d970521543e7bfd29b682ad4fe73`.

## Исправленные критические замечания

- русские названия больше не равны canonical names;
- definitions, lifecycle, stale condition и authoritative replacement уникальны для term/stage;
- `Point`=`PRICE_POINT_SIZE`, `TickSize`=`PRICE_TICK_SIZE`, оба — SYMBOL PROPERTY;
- `InitialIgnoredProfit` использует confirmed initial-leg deals и `MoneyTolerance`;
- MONEY_REALIZED использует confirmed deals/ledger, не OrderCalcProfit;
- costs разделены на ExpectedExitCosts, CommissionCost, SwapCost, FeeCost, SpreadCost, SlippageCost;
- direction records имеют отдельные derivation rules и `EXACT ENUM MATCH`;
- mapping вынесен в `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json`, отсутствующие identifiers честно имеют MISSING.

## Метод MQL5 mapping

Просмотрены все `37` MQL5/MQH-файла. Identifier считается существующим только если exact token найден в указанном существующем файле. EXACT/SEMANTIC требуют identifier, semantic note и evidence; отсутствие оформляется MISSING с пустым массивом.

| File | IDENTIFIERS_REVIEWED | CANONICAL_MATCHES | PARTIAL/SEMANTIC_MATCHES | AMBIGUOUS_MATCHES | NOT_MAPPED_IN_THIS_FILE |
|---|---:|---:|---:|---:|---:|
| `MinusLock_BigHarvest_EA.mq5` | 346 | 0 | 0 | 0 | 230 |
| `Include/Config.mqh` | 235 | 0 | 14 | 0 | 216 |
| `Include/Types.mqh` | 1043 | 0 | 16 | 0 | 214 |
| `Include/RecoveryMath.mqh` | 184 | 0 | 8 | 0 | 222 |
| `Include/PositionUtils.mqh` | 112 | 0 | 2 | 0 | 228 |
| `Include/TradeEngine.mqh` | 166 | 0 | 0 | 0 | 230 |
| `Include/SimulationEngine.mqh` | 195 | 0 | 5 | 0 | 225 |
| `Include/RiskManager.mqh` | 109 | 0 | 0 | 0 | 230 |
| `Include/StateMachine.mqh` | 2755 | 0 | 14 | 0 | 216 |

## Метод Python mapping

Просмотрены все `257` Python-файла проекта в Tests/Tools/прочих каталогах, кроме самого glossary validator. Token evidence и существование path проверяются validator; приблизительный смысл не повышается до EXACT.

```text
PYTHON_FILES_REVIEWED=257
PYTHON_IDENTIFIERS_MAPPED=129
MQL5_FILES_REVIEWED=37
MQL5_IDENTIFIERS_MAPPED=162
```

## Проверенные source files

Полные списки находятся в machine-readable полях `mql5_files_reviewed` и `python_files_reviewed` mapping JSON. Обязательные MQL5-файлы из ТЗ включены в таблицу выше.

## Validator-generated statistics

`STATISTICS_SOURCE=validator generated`. Следующий блок является точным output validator для этого commit content:

```text
CANONICAL_TERMS=230
EXTENDED_RECORDS=230
DUPLICATE_CANONICAL_NAMES=0
RUSSIAN_NAME_EQUALS_CANONICAL=0
PLACEHOLDER_DEFINITIONS=0
DUPLICATE_DEFINITIONS=0
PLACEHOLDER_LIFECYCLES=0
DUPLICATE_LIFECYCLES=0
PLACEHOLDER_MAPPINGS=0
MAPPING_RECORDS_MISSING=0
DUPLICATE_MAPPING_RECORDS=0
MAPPING_STATUS_INVALID=0
MAPPING_IDENTIFIERS_MISSING=0
MAPPING_FILES_NOT_FOUND=0
MAPPING_WITHOUT_EVIDENCE=0
MAPPING_IDENTIFIER_NOT_IN_FILE=0
EXACT_MAPPING_WITHOUT_EVIDENCE=0
SEMANTIC_MAPPING_WITHOUT_NOTE=0
AMBIGUOUS_MAPPING_WITHOUT_EXPLANATION=0
MISSING_MAPPING_WITH_IDENTIFIER=0
INVALID_TYPE_UNIT=0
INVALID_TYPE_CLASS=0
INVALID_TYPE_TOLERANCE=0
INVALID_TYPE_SOURCE=0
TABLE_RECORD_MISMATCH=0
UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID=0
UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE=0
UNRESOLVED_POLICY_APPROVED=0
MQL5_SEMANTIC_MATCH=88
PYTHON_SEMANTIC_MATCH=73
MQL5_MISSING=142
PYTHON_MISSING=157
NEGATIVE_TESTS=PASS
SOURCE_OF_TRUTH_MATRIX=PASS
SIGN_MATRIX=PASS
TOLERANCE_MATRIX=PASS
ROUNDING_MATRIX=PASS
ARCHITECTURE_MATRIX=PASS
STAGE_3_1_3_SEMANTIC_VALIDATION=PASS
```

## Исправленные type/source/tolerance ошибки

```text
POINT_TYPE=PRICE_POINT_SIZE / PASS
TICK_SIZE_TYPE=PRICE_TICK_SIZE / PASS
INITIAL_IGNORED_PROFIT_SOURCE=CONFIRMED_FILTERED_INITIAL_DEALS / PASS
INITIAL_IGNORED_PROFIT_TOLERANCE=MoneyTolerance / PASS
MONEY_REALIZED_SOURCE=CONFIRMED_DEALS_OR_LEDGER / PASS
MONEY_COST_MODEL=DECOMPOSED / PASS
DIRECTION_SOURCES=TERM_SPECIFIC / PASS
DIRECTION_TOLERANCES=EXACT_ENUM_MATCH / PASS
```

## Negative validator tests

Validator выполняет 12 in-memory mutations: placeholder BigCore definition; invalid Point type; lot tolerance for InitialIgnoredProfit; projected-only source for MONEY_REALIZED; EXACT without identifier; MISSING with identifier; deleted Python mapping record; Russian name equal canonical; table/record drift; placeholder lifecycle; removed NewFar conflict; approved unresolved parameter. Все мутации обнаружены: `NEGATIVE_TESTS=PASS`.

## Оставшиеся unresolved terms и conflict control

Parameter conflicts 001–006, NewFar conflict 020, ratio policy 022, SmallReverseNet policy 023 и architecture routing 031 не разрешены. Production profile/business policy не выбраны. `NEW_CONFLICTS_FOUND=0`.

## Ограничения

Mapping не доказывает code conformance. MISSING допустим и явно учитывается. Три закона не доказывались; MQL5/MQH/runtime не менялись; MetaEditor/Strategy Tester/real readiness не заявлены; Этап 3.1.4 не выполнялся.

## Финальный статус

```text
STAGE_3_1_3_CORRECTION_STATUS=PASS
REAL_TRADING_ALLOWED=NO
```

Этап 3.1.3 ожидает повторную независимую проверку пользователя.
Этап 3.1.4 не выполнялся.
