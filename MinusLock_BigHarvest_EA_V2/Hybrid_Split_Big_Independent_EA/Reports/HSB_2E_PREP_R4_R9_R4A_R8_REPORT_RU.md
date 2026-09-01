# HSB.2E-PREP-R4-R9-R4A-R8 — отчёт

## Граница результата

R8 проверяет только schema/replay/declared-lifecycle internal consistency. Он не исполняет native-модель, не доказывает полную экономическую корректность и не разрешает торговую реализацию.

## Исходная точка и история

- baseline: `4a4bd1fd4d41d0b8394e48d34dfb28316351c04d` (`work`, clean, origin/remote parity подтверждены);
- final SHA и remote parity фиксируются публикационным handoff после последнего коммита;
- historical R5–R7, production MQL5/MQH, native model и historical Oracle не изменялись.

## Дефект → исправление → исполнимый case

| Дефект R7 | Исправление R8 | Case |
|---|---|---|
| foreign position | независимая ownership-проверка | `POSITION_FOREIGN_MAGIC` |
| foreign event | полное event↔deal равенство | `EVENT_FOREIGN_MAGIC` |
| неизвестный Far ticket | точное разрешение active Far | `FAR_TICKET_NOT_FOUND` |
| commit `r→r+99` | обязательный `r→r+1` | `COMMIT_REVISION_JUMP` |
| phase downgrade | current evidence запрещён в PRE_COMMIT | `PHASE_DOWNGRADE_WITH_EVIDENCE` |
| orphan deal падал `KeyError` | ссылки разрешаются до индексирования | `ORPHAN_DEAL` |
| arbitrary replay revision | current revision связан с historical output | `REPLAY_ARBITRARY_CURRENT_REVISION` |
| acceptance `0/0` | независимый непустой catalog | `SENS_RUNNER_ZERO_OF_ZERO` |

Историческое воспроизведение: 8/8 дефектов R7 воспроизведены. R8 regression suite: 48/48, wrong failures 0, unexpected infrastructure errors 0. Независимый catalog содержит 48 case IDs и 86 version-qualified obligations (28 R5 + 20 R6 + 38 R7); missing IDs 0.

## Lifecycle и sensitivity

Expected output шага вычисляется только из его input state и records этой операции. Property `FUTURE_STEP_INDEPENDENCE` проходит; следующий replay проверяет уже объявленный результат. `LIFECYCLE_EXECUTED_BY_NATIVE_MODEL=NO`, `FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN`.

Все 10 sensitivity cases обнаружены: `0/0`, missing, duplicate, summary-only, отключение position/event/Far/revision/phase/output bindings. Metadata erasure не меняет результат; runtime duplicates обнаруживаются. Обычные runs read-only; evidence публикуется только явным флагом.

## Защита и scope

Protected registry содержит 52 Git-tracked historical/native source artifacts; `.pyc` и `__pycache__` исключены. Scope violations 0, production diff paths 0, native model changed NO. Python проверен фактически версией, указанной в финальных командах. MetaEditor/MT5: `NOT_RUN`.

## Статус

```text
RUNTIME_INTERNAL_CONSISTENCY_REGRESSIONS=PASS
REQUIRED_CASE_COMPLETENESS=PASS
ACCEPTANCE_SENSITIVITY=PASS
QUALIFICATION_CORE_READY=NO
ORACLE_V3_FINAL_ACCEPTANCE=NOT_GRANTED
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```
