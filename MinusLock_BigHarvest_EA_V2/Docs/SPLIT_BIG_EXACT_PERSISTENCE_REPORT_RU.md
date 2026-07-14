# SplitGeometry Big — отчёт Этапа 4: точное persistence-восстановление

## Git

- Репозиторий: `https://github.com/ic8812825-maker/chatgpt.com-codex`
- Ветка: `work`
- Целевая папка: `MinusLock_BigHarvest_EA_V2`
- START_SHA: `f46addc226c465b817b6ebb5afb71a75f29b59b5`
- FINAL_SHA: будет указан в финальном сообщении после публикации коммита отчёта.
- Compare: `https://github.com/ic8812825-maker/chatgpt.com-codex/compare/f46addc226c465b817b6ebb5afb71a75f29b59b5...FINAL_SHA`

## Коммиты Этапа 4

1. `6090cc5` — Добавлено точное сохранение 64-битного контекста  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/6090cc5
2. `b2c5545` — Добавлены тесты идентификаторов выше 2 в 53 степени  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/b2c5545
3. Итоговый коммит отчёта — будет указан в финальном сообщении.

## Изменённые файлы

- `Include/Types.mqh` — добавлены поля SymbolHash High32/Low32 и структура `ReserveEventContextSnapshot`.
- `Include/StateMachine.mqh` — добавлены универсальные `SplitUlong64`/`RestoreUlong64`, `SplitLong64`/`RestoreLong64`, стабильный `StableSymbolHash64`, точное сохранение RecoveryContext и Ledger, required-field loading, symbol/context validation, snapshot для Reserve events и frozen final debit.
- `Tests/unit/test_split_exact_persistence_model.py` — поведенческие тесты полного 64-bit round-trip, legacy double loss, full EventKey serialization, одинаковой длины symbols, missing fields, duplicate credit/debit и context mutation.
- `Tests/static/test_split_architecture_static.py` — static guard для Stage 4: точные helper-функции, отсутствие SymbolHash через StringLen, High32/Low32 Ledger fields и frozen final debit snapshot.
- `Docs/SPLIT_BIG_EXACT_PERSISTENCE_REPORT_RU.md` — этот отчёт.

## Поля, переведённые на High32/Low32

### RecoveryContext

```text
CycleId
FarTicket
FarIdentifier
BigTicket
BigIdentifier
SmallTicket
SmallIdentifier
InitialBuyTicket
InitialSellTicket
InitialBuyIdentifier
InitialSellIdentifier
BigCoreTicket
BigCoreIdentifier
BigTrendTicket
BigTrendIdentifier
SmallBaseTicket
SmallBaseIdentifier
ReverseSmallTicket
ReverseSmallIdentifier
OldFarTicket
PendingTicket
PendingBigPositionId
PendingSmallPositionId
RetryTicket
ReserveNextEventId
```

### Reserve Ledger

```text
EventId
MagicNumber
CycleId
BigIdentifier
SmallIdentifier
FarIdentifier
BigCoreIdentifier
BigTrendIdentifier
SmallBaseIdentifier
ReverseSmallIdentifier
EventKeyHash
SymbolHash
```

## SymbolHash format

Используется стабильный 64-bit FNV-1a hash:

```text
StableSymbolHash64(symbol)
```

Hash сохраняется как:

```text
SymbolHashHigh32
SymbolHashLow32
```

`SymbolLength` сохраняется только как дополнительная диагностика. При восстановлении сравниваются сохранённый SymbolHash и hash текущего `_Symbol`; при несовпадении выставляется `RESERVE_LEDGER_SYMBOL_MISMATCH`.

## Результаты тестов

```text
pytest -q Tests/unit Tests/static Tests/scenario
46 passed
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

## Ulong/Long round-trip

Проверены значения:

```text
ulong: 0, 1, 2^32-1, 2^32, 2^53-1, 2^53, 2^53+1, 2^63-1, 2^64-1
long: LONG_MIN, -2^53-1, -1, 0, 1, 2^53+1, LONG_MAX
```

Ожидание выполнено:

```text
Restore(Split(value)) == value
```

## Legacy double risk

Тест доказывает небезопасность старого формата:

```text
value = 2^53 + 1
int(float(value)) != value
```

## Full EventKey serialization

Проверен Ledger entry с identifiers выше `2^53`:

```text
serialize -> clear memory -> deserialize -> recompute hash
```

Результат:

```text
all identifiers bit-exact
stored hash == recomputed hash
```

## Symbol validation

Проверены разные символы одинаковой длины:

```text
EURUSD
GBPUSD
USDJPY
AUDUSD
```

Результат:

```text
StableSymbolHash64 отличается для каждого символа.
EURUSD ledger не принимается в GBPUSD runtime context.
```

## Required fields

Удаление `BigCoreIdentifierLow32` из сериализованного Ledger вызывает:

```text
RESERVE_LEDGER_REQUIRED_FIELD_MISSING
```

## Credit/debit restart idempotency

С identifiers выше `2^53` проверены:

```text
credit -> serialize -> clear memory -> deserialize -> duplicate credit
final debit -> serialize -> clear memory -> deserialize -> duplicate debit
```

Результат:

```text
Reserve не меняется повторно.
Новая Ledger entry не создаётся.
```

## Context mutation / frozen snapshot

Проверено:

```text
snapshot сформирован;
Ctx очищен/изменён;
EventKey строится из snapshot;
очистка Ctx не меняет EventKey.
```

В коде final debit строится из `finalDebitSnapshot` до очистки Split/Far context.

## MetaEditor

MetaEditor/MT5 в Linux-контейнере не обнаружены.

```text
METAEDITOR_COMPILE = NOT_RUN
MetaTrader build = NOT_RUN
MetaEditor build = NOT_RUN
Главный mq5 = MinusLock_BigHarvest_EA.mq5
Compile log = NOT_RUN
```

Подготовленный скрипт для Windows/VPS остаётся:

```powershell
./Scripts/compile_metaeditor_windows.ps1 -MetaEditor "C:\Program Files\MetaTrader 5\metaeditor64.exe"
```

## MT5 Strategy Tester

MT5 Strategy Tester недоступен в контейнере.

```text
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

## Известные ограничения

- MetaEditor compile и MT5 Strategy Tester должны быть выполнены отдельно на Windows/VPS.
- Runtime MT5 restart tests не запускались в контейнере; покрыты поведенческими моделями Python.
- Split Small / DynamicReverseSmall / Small-пила / Small-разворот / BigCore remainder → NewFar не реализованы.
- До MT5 PASS проект остаётся `DEVELOPMENT / CONTROLLED TESTING ONLY`.

## Статусы

```text
ULONG64_EXACT_PERSISTENCE = PASS
LONG64_EXACT_PERSISTENCE = PASS
RECOVERY_CONTEXT_EXACT_RESTORE = PASS
RESERVE_LEDGER_EXACT_IDENTIFIERS = PASS
SYMBOL_EXACT_VALIDATION = PASS
EVENT_KEY_FULL_RECOMPUTE = PASS
RESERVE_CREDIT_RESTART_IDEMPOTENCY = PASS
RESERVE_DEBIT_RESTART_IDEMPOTENCY = PASS
RESERVE_EVENT_ATOMICITY = PASS
LEGACY_STATE_MIGRATION = PASS
PYTHON_TESTS = PASS
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

## Итоговый вердикт

Этап 4 устраняет критический риск `64-bit integer -> double -> 64-bit integer` для RecoveryContext и Reserve Ledger: tickets, identifiers, CycleId, MagicNumber, EventId и EventKeyHash сохраняются через High32/Low32; Symbol проверяется стабильным hash; Reserve EventKey строится из frozen snapshot и не зависит от очищенного Ctx. Реальная торговля остаётся запрещённой до MetaEditor PASS и MT5 Strategy Tester PASS.
