# HSB.2E-PREP-R4-R9-R4A-R4-AUDIT — независимый аудит

## Исходная точка

```text
AUDIT_TARGET_SHA=77743d39fc572eefcceaa65b129d9d6cfcb8b098
IMPLEMENTATION_BASELINE_SHA=f44b7e5cae314fced0f8d519e1e5d70f3c49c35d
BASELINE_GATE=PASS
DUPLICATE_RUN=STOPPED_ON_STALE_BASELINE
PUBLISHED_R4A_R4_ACCEPTANCE=VERIFIED_AS_FAILED
```

## Итог

Аудит завершён технически, но опубликованный этап не принят: обнаружены воспроизводимые нормативные дефекты. Штатные проверки проходят, однако две независимые adversarial проверки расходятся с требуемым поведением, а 20 positive bases содержат несогласованную роль `persistedState.farState`.

```text
R4A_R4_AUDIT=FAIL
QUALIFICATION_CORE_READY=NO
ORACLE_V3_FINAL_ACCEPTANCE=NOT_GRANTED
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```

## Матрица требований

| REQUIREMENT | IMPLEMENTING_FILES | IMPLEMENTING_COMMITS | EXECUTED_CHECK | OBSERVED_RESULT | VERDICT |
|---|---|---|---|---|---|
| closed typed schema | Tests/Contracts/HSB_2E_R4_R9_R4A_R4_SCENARIO_INPUT_SCHEMA_V3.json | 98b957f | independent schema walk | {'NOT_APPLICABLE_WITH_RULE': 0, 'OPTIONAL_WITH_RULE': 0, 'REQUIRED': 186, 'nodes': 186, 'openOrUntypedObjects': 0, 'untypedArrays': 0} | PARTIAL |
| exact Registry paths | Tests/Contracts/HSB_2E_R4_R9_R4_PREDICATE_REGISTRY.json | 6ddaa95, d930576 | independent wildcard resolver | 69/69 | PASS |
| 28 positive bases | Tests/Vectors/HSB_2E_R4_R9_R4A_R4_POSITIVE_BASES_V3_INITIAL_BIG.json<br>Tests/Vectors/HSB_2E_R4_R9_R4A_R4_POSITIVE_BASES_V3_RESTART_REPLAY_LIFECYCLE.json<br>Tests/Vectors/HSB_2E_R4_R9_R4A_R4_POSITIVE_BASES_V3_SMALL_FINAL.json | da6bb22, 034f95c, f89746d | inventory and semantic variation audit | {'BIG': 4, 'FINAL': 4, 'INITIAL': 4, 'LIFECYCLE': 4, 'REPLAY_COMMITTED': 4, 'RESTART_CONTINUATION': 4, 'SMALL': 4} | FAIL |
| fail-closed validator | Tests/Static/verify_hsb_2e_r4_r9_r4a_r4_schema.py | 6e171da, 77743d3 | 22 independent adversarial probes | failed=2 | FAIL |

## Подтверждённые части

- История `f44b7e5..77743d3` линейна; оба объекта существуют, implementation baseline является предком audit target.
- Все изменения implementation находятся под разрешённым project prefix. `SCOPE_VIOLATIONS=0`, `PRODUCTION_DIFF_PATHS=0`, native model и historical oracles не изменены.
- Schema закрывает вложенные objects (`additionalProperties=false`), типизирует array items, отклоняет Boolean как integer и проверяет Decimal finiteness.
- Независимый wildcard resolver разрешил все 69 Registry paths в конкретные типизированные узлы.
- Загружены ровно 28 fixtures, семь групп по четыре; runtime SHA-256 уникальны.
- Все 28 опубликованных certificate bodies/digests независимо пересчитаны и внутренне согласованы в исходных fixtures. Это не устраняет дефект validator, принимающего подменённый digest.
- Replay fixtures содержат непустые consumed deal/event registries.

## Воспроизводимые дефекты

### 1. Certificate digest не проверяется семантически

Подмена `certificate.digest` строкой из 64 нулей сохраняет правильный тип и длину. Published validator возвращает `ACCEPTED`, хотя ожидался `NORMATIVE_REJECTION`. Реализация проверяет только непустоту certificate fields и не пересчитывает digest.

### 2. Нет фазовой применимости certificate

Все 186 schema nodes имеют `requiredState=REQUIRED`; `OPTIONAL_WITH_RULE=0`, `NOT_APPLICABLE_WITH_RULE=0`. Удаление certificate в pre-commit `INITIAL` приводит к общему missing-field rejection. Формального правила применимости по phase нет.

### 3. Full lifecycle не является последовательностью

Каждая из четырёх `LIFECYCLE` fixtures содержит один runtime object и единственный переход `SMALL -> FINAL`. Последовательность `INITIAL/BIG/SMALL/FINAL/COMMITTED` или список операций отсутствует.

### 4. Far role несогласован в positive bases

В 20 из 28 fixtures `persistedState.farState.ticket` указывает на единственную position с ролью `NEAR`, `BIG` или `SMALL`, а не `FAR`. Published validator сопоставление `farState.ticket -> position.role` не проверяет.

### 5. Self-tests имеют риск ложного CAUGHT

Published self-test считает успехом не только нормативный `ValidationError`, но также `KeyError` и `TypeError`. Это смешивает нормативный отказ с инфраструктурным падением и противоречит audit contract.

### 6. Содержательное разнообразие ограничено

Внутри каждой scenario group варианты имеют одинаковые structure, grid case и экономическую формулу. Отличаются BUY/SELL direction, скалярные volume/price, identifiers, revisions и timestamps. Отдельные broker-boundary/economic-boundary формы не представлены.

## Таблица 28 positive bases

| FIXTURE_ID | SCENARIO | STATE_PHASE | POSITION_DIRECTIONS | VOLUMES | GRID_CASE | ECONOMIC_CASE | PERSISTED_STATE_CASE | MEANINGFUL_DIFFERENCE |
|---|---|---|---|---|---|---|---|---|
| V3-INITIAL-1 | INITIAL | INITIAL->BIG | BUY | 0.11 | STANDARD_TICK_AND_STEP | 101=61+40 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-INITIAL-2 | INITIAL | INITIAL->BIG | SELL | 0.12 | STANDARD_TICK_AND_STEP | 102=62+40 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-INITIAL-3 | INITIAL | INITIAL->BIG | BUY | 0.13 | STANDARD_TICK_AND_STEP | 103=63+40 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-INITIAL-4 | INITIAL | INITIAL->BIG | SELL | 0.14 | STANDARD_TICK_AND_STEP | 104=64+40 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-BIG-1 | BIG | BIG->SMALL | BUY | 0.11 | STANDARD_TICK_AND_STEP | 105=61+44 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-BIG-2 | BIG | BIG->SMALL | SELL | 0.12 | STANDARD_TICK_AND_STEP | 106=62+44 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-BIG-3 | BIG | BIG->SMALL | BUY | 0.13 | STANDARD_TICK_AND_STEP | 107=63+44 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-BIG-4 | BIG | BIG->SMALL | SELL | 0.14 | STANDARD_TICK_AND_STEP | 108=64+44 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-RESTART_CONTINUATION-1 | RESTART_CONTINUATION | BIG->SMALL | BUY | 0.11 | STANDARD_TICK_AND_STEP | 117=61+56 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-RESTART_CONTINUATION-2 | RESTART_CONTINUATION | BIG->SMALL | SELL | 0.12 | STANDARD_TICK_AND_STEP | 118=62+56 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-RESTART_CONTINUATION-3 | RESTART_CONTINUATION | BIG->SMALL | BUY | 0.13 | STANDARD_TICK_AND_STEP | 119=63+56 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-RESTART_CONTINUATION-4 | RESTART_CONTINUATION | BIG->SMALL | SELL | 0.14 | STANDARD_TICK_AND_STEP | 120=64+56 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-REPLAY_COMMITTED-1 | REPLAY_COMMITTED | COMMITTED->COMMITTED | BUY | 0.11 | STANDARD_TICK_AND_STEP | 121=61+60 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-REPLAY_COMMITTED-2 | REPLAY_COMMITTED | COMMITTED->COMMITTED | SELL | 0.12 | STANDARD_TICK_AND_STEP | 122=62+60 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-REPLAY_COMMITTED-3 | REPLAY_COMMITTED | COMMITTED->COMMITTED | BUY | 0.13 | STANDARD_TICK_AND_STEP | 123=63+60 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-REPLAY_COMMITTED-4 | REPLAY_COMMITTED | COMMITTED->COMMITTED | SELL | 0.14 | STANDARD_TICK_AND_STEP | 124=64+60 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-LIFECYCLE-1 | LIFECYCLE | SMALL->FINAL | BUY | 0.11 | STANDARD_TICK_AND_STEP | 125=61+64 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-LIFECYCLE-2 | LIFECYCLE | SMALL->FINAL | SELL | 0.12 | STANDARD_TICK_AND_STEP | 126=62+64 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-LIFECYCLE-3 | LIFECYCLE | SMALL->FINAL | BUY | 0.13 | STANDARD_TICK_AND_STEP | 127=63+64 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-LIFECYCLE-4 | LIFECYCLE | SMALL->FINAL | SELL | 0.14 | STANDARD_TICK_AND_STEP | 128=64+64 | NONEMPTY_REPLAY_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-SMALL-1 | SMALL | SMALL->FINAL | BUY | 0.11 | STANDARD_TICK_AND_STEP | 109=61+48 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-SMALL-2 | SMALL | SMALL->FINAL | SELL | 0.12 | STANDARD_TICK_AND_STEP | 110=62+48 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-SMALL-3 | SMALL | SMALL->FINAL | BUY | 0.13 | STANDARD_TICK_AND_STEP | 111=63+48 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-SMALL-4 | SMALL | SMALL->FINAL | SELL | 0.14 | STANDARD_TICK_AND_STEP | 112=64+48 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-FINAL-1 | FINAL | FINAL->COMMITTED | BUY | 0.11 | STANDARD_TICK_AND_STEP | 113=61+52 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-FINAL-2 | FINAL | FINAL->COMMITTED | SELL | 0.12 | STANDARD_TICK_AND_STEP | 114=62+52 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-FINAL-3 | FINAL | FINAL->COMMITTED | BUY | 0.13 | STANDARD_TICK_AND_STEP | 115=63+52 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |
| V3-FINAL-4 | FINAL | FINAL->COMMITTED | SELL | 0.14 | STANDARD_TICK_AND_STEP | 116=64+52 | EMPTY_FRESH_STATE | DIRECTION_VOLUME_PRICE_AND_IDENTIFIERS_ONLY_WITHIN_GROUP |

## Schema / fixture verdict boundaries

```text
SCHEMA_STRUCTURE_VALID=NO
FIXTURE_SCHEMA_VALID=YES
FIXTURE_INTERNAL_CONSISTENCY_VALID=NO
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
```

`FULL_ECONOMIC_CORRECTNESS` не доказывается: validator сверяет две conservation equalities, но не выводит экономические значения из execution inputs. Источник Initial positive profit/Recovery и нормативное объяснение денежных констант отсутствуют. Reserve/Partial Far probe работает, но этого недостаточно для полного economic proof.

## Штатные запуски

- Validator и self-tests запущены из project root и `Tests/Static`; exit code 0, stdout совпадает.
- Запуск с `--publish-evidence` выполнен в изолированной временной копии разрешённой папки; опубликованные evidence не перезаписывались.
- Хеши schema, Registry, fixtures и published runners до/после запусков совпали. Полные command/stdout/stderr/input/output hashes находятся в `execution_evidence.json`.

## Independent probes

Всего выполнено 22 probes; два дали нормативно неверный outcome. Инфраструктурные исключения не засчитывались как обнаружение.

| PROBE | EXPECTED | ACTUAL | RESULT |
|---|---|---|---|
| remove_nested_required | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| unknown_nested | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| boolean_numeric_id | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| decimal_nan | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| decimal_infinity | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| empty_positions | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| empty_intents | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| empty_deals | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| off_grid_price | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| off_grid_volume | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| duplicate_deal_id | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| orphan_deal | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| symbol_mismatch | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| invalid_time_window | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| money_conservation | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| volume_conservation | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| reserve_partial_far | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| metadata_in_runtime | NORMATIVE_REJECTION | NORMATIVE_REJECTION | PASS |
| large_exact_identifier | ACCEPTED | ACCEPTED | PASS |
| forged_certificate_digest_same_length | NORMATIVE_REJECTION | ACCEPTED | FAIL |
| precommit_certificate_absent | ACCEPTED | NORMATIVE_REJECTION | FAIL |
| metadata_only_wrapper_change | UNCHANGED_RUNTIME | UNCHANGED_RUNTIME | PASS |

## Scope и отложенные контуры

```text
SCOPE_VIOLATIONS=0
PRODUCTION_DIFF_PATHS=0
NATIVE_MODEL_CHANGED=NO
HISTORICAL_ORACLES_CHANGED=NO
QUALIFICATION_CORE_READY=NO
ORACLE_V3_FINAL_ACCEPTANCE=NOT_GRANTED
MODEL_CHANGES_ALLOWED=NO
```

Исправления schema, fixtures, validator, self-tests и canonical status этим аудитом намеренно не выполнялись. Требуется отдельное исправляющее задание. MetaEditor, MQL5 runtime, Strategy Tester и broker money runtime proof не запускались.
