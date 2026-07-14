# SplitGeometry Big — финальный отчёт Этапа 3

## Git

- Репозиторий: `https://github.com/ic8812825-maker/chatgpt.com-codex`
- Ветка: `work`
- Целевая папка: `MinusLock_BigHarvest_EA_V2`
- START_SHA: `798619fd0cb7e5b0ec143ebb0108001063fabfa8`
- FINAL_SHA: будет указан в финальном сообщении после публикации коммита отчёта.
- Compare: `https://github.com/ic8812825-maker/chatgpt.com-codex/compare/798619fd0cb7e5b0ec143ebb0108001063fabfa8...FINAL_SHA`

## Коммиты Этапа 3

1. `e2827a4` — Исправлена проверка Split open-pending без ticket
2. `40aa6df` — Добавлено точное хранение Reserve EventKey
3. `20263af` — Добавлены поведенческие тесты restart-безопасности Split Big
4. Итоговый коммит отчёта — будет указан в финальном сообщении.

## Изменённые файлы

- `Include/StateIntegrityEngine.mqh` — добавлен `IsOpenPendingState`; open-pending больше не требует `pendingTicket`/`retryTicket`, но требует action, время, lot, direction, comment, next state и attempts.
- `Include/Types.mqh` — `ReserveLedgerEntry` расширен полями Symbol, MagicNumber, CycleId, Split identifiers и `eventKeyHashHigh/eventKeyHashLow`.
- `Include/StateMachine.mqh` — добавлено bit-exact split/restore для 64-bit EventKeyHash, сохранение High32/Low32, восстановление CycleId до проверки Ledger, проверка context/hash/chain/duplicates.
- `Tests/unit/test_split_final_safety_model.py` — поведенческая модель open/close pending, hash round-trip, ledger chain, restart idempotency, partial-history restart.
- `Tests/static/test_split_architecture_static.py` — static guard, подтверждающий отсутствие single-double хранения hash и отсутствие ticket-требования в open-pending ветке.
- `Scripts/compile_metaeditor_windows.ps1` — инструкция/скрипт компиляции MetaEditor для Windows/VPS.
- `Docs/SPLIT_BIG_FINAL_SAFETY_REPORT_RU.md` — этот отчёт.

## Что исправлено

- Split open-pending не блокируется отсутствующим ticket до исполнения.
- Close-pending остаётся строгим: требуется ticket или identifier закрываемой позиции и lot.
- 64-bit Reserve EventKeyHash не сохраняется через `double`; используется High32/Low32 round-trip.
- Ledger хранит полный Split-контекст: Symbol, MagicNumber, CycleId, Level, FarIdentifier, BigCoreIdentifier, BigTrendIdentifier, SmallBaseIdentifier.
- RecoverState восстанавливает CycleId до чтения и проверки Reserve Ledger.
- Reserve Ledger проверяет Symbol/Magic/CycleId, bit-exact hash, непрерывность reserveBefore/reserveAfter, дубли EventId/EventKey и отрицательный ReserveAfter.
- Добавлены поведенческие тесты restart/idempotency, которые проверяют значения и повторные операции, а не только наличие строк.

## Команды тестов и результаты

```text
pytest -q Tests/unit Tests/static Tests/scenario
33 passed
```

```text
python Tests/validate_v2_static.py
PASS
```

```text
python Tests/default_parameters_v241_check.py
PASS
```

```text
python Tests/fsm_integrity_check.py
PASS
```

```text
python Tests/terminal_states_separated_from_pending_check.py
PASS
```

## Hash round-trip

Проверены значения `0`, `1`, `2^53 - 1`, `2^53 + 1`, `LONG_MAX`, отрицательные long/hash значения и реальный 64-bit pattern. Для каждого сценария модель проверяет:

```text
restore(split(hash)) == hash
```

## Reserve Ledger chain

Проверены:

- корректная цепочка credit/debit;
- сломанный `reserveBefore`;
- сломанный `reserveAfter`;
- повторный `EventId`;
- повторный `EventKey`;
- неверный `CycleId`.

Ожидаемые нарушения отклоняются моделью с ошибкой Ledger.

## Open/close pending

- Open-pending для BigCore, SmallBase и BigTrend валиден при `ticket=0`, если есть action, lot, direction, start time, next state и comment.
- Open-pending невалиден без lot или direction.
- Close-pending невалиден без ticket/identifier.
- Close-pending валиден с ticket или identifier закрываемой позиции.

## Restart результаты

Поведенчески смоделированы:

- restart open-pending до результата: retry допускается;
- restart после фактического открытия позиции, но до записи ticket: существующая позиция разрешается, новый ордер не отправляется;
- Reserve credit после сериализованного restart: повторное начисление отклоняется;
- Reserve debit после сериализованного restart: повторное списание отклоняется;
- partial-history restart: Carry рассчитывается по actual loss, повторный Reserve credit отклоняется.

## MetaEditor

В Linux-контейнере MetaEditor/MT5 не обнаружены.

```text
METAEDITOR_COMPILE = NOT_RUN
MetaTrader 5 build = NOT_RUN
MetaEditor build = NOT_RUN
Главный mq5 = MinusLock_BigHarvest_EA.mq5
Compile log = NOT_RUN
```

Для Windows/VPS подготовлен скрипт:

```powershell
./Scripts/compile_metaeditor_windows.ps1 -MetaEditor "C:\Program Files\MetaTrader 5\metaeditor64.exe"
```

## MT5 Strategy Tester

MT5 Strategy Tester недоступен в контейнере.

```text
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

Python-тесты не заменяют реальную компиляцию MetaEditor и Strategy Tester.

## Известные ограничения

- MetaEditor compile и MT5 Strategy Tester должны быть выполнены отдельно на Windows/VPS.
- Split Small, DynamicReverseSmall, Small-пила, Small-разворот и BigCore remainder → NewFar не реализованы.
- До MT5 PASS режим остаётся `DEVELOPMENT / CONTROLLED TESTING ONLY`.

## Статусы

```text
SPLIT_OPEN_PENDING_WITHOUT_TICKET = PASS
SPLIT_CLOSE_PENDING_CONTRACT = PASS
RESERVE_EVENT_KEY_EXACT_RESTORE = PASS
RESERVE_LEDGER_CHAIN = PASS
RESERVE_CREDIT_IDEMPOTENCY = PASS
RESERVE_DEBIT_IDEMPOTENCY = PASS
SPLIT_RESTART_PENDING = PASS
PARTIAL_HISTORY_RESTART = PASS
SPLIT_FINAL_CLOSE_RESTART = PASS
LEGACY_REGRESSION = PASS
PYTHON_TESTS = PASS
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

## Итоговый вердикт

Этап 3 устраняет два критических остаточных дефекта: Split open-pending больше не требует ticket до исполнения, а Reserve EventKey/Ledger проходят bit-exact восстановление и idempotency после сериализованного restart на уровне кода и поведенческих Python-моделей. До реальной компиляции MetaEditor и MT5 Strategy Tester реальная торговля запрещена.
