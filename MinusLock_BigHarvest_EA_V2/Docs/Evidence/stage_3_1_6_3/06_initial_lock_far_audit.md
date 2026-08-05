# 3.1.6.3.6 — Initial Lock и создание Far

## Фактический маршрут

```text
STATE_IDLE
→ OpenInitialLock
→ OpenPosition BUY `MinusLock_INITIAL_BUY`
→ OpenPosition SELL `MinusLock_INITIAL_SELL`
→ при отказе SELL выполняется rollback BUY
→ STATE_INITIAL_LOCK_OPENED
→ CheckInitialPlusClose
→ close profitable initial leg
→ ConvertInitialLockToFar(remaining leg)
→ InitialProfitIgnored=true
→ TotalReserve=0
→ STATE_INITIAL_PLUS_CLOSED
→ compatibility transition STATE_FAR_ACTIVE
```

## Положительные элементы

- Есть rollback первой ноги при отказе второй.
- Комментарии BUY/SELL различаются.
- Исторический пересчёт Recovery пропускает deals, комментарий которых содержит `INITIAL_BUY` или `INITIAL_SELL`.
- После plus close явно выставляются `initialProfitIgnored`, `initialIgnoredProfit`, `totalReserve=0`, cycle P/L fields reset.
- Persistence содержит отдельные initial tickets и identifiers.

## Ограничения

- Открытие и закрытие подтверждаются synchronous return wrapper, а не `OnTradeTransaction`.
- При partial fill обеих Initial legs нет единого event-driven barrier равных фактических объёмов.
- Назначение Far вызывается сразу после успешного close wrapper; actual deal event не ожидается.
- Исключение Initial Profit по comment является дополнительной эвристикой; полный stable source ownership через deal EventKey в production runtime отсутствует.

## Замечания

| ID | Критичность | Содержание |
|---|---|---|
| INITLOCK-001 | P1 | Far может быть назначен после synchronous close success до отдельного actual deal event. |
| INITLOCK-002 | P1 | Partial fill Initial open/close не имеет общего transaction-state lifecycle. |
| INITLOCK-003 | P1 | Initial ignored exclusion зависит в том числе от comments/history scan, а не только от immutable managed source identity. |
| INITLOCK-004 | P2 | Переход `INITIAL_PLUS_CLOSED → FAR_ACTIVE` назван compatibility transition, что подтверждает legacy bridge в основном FSM. |

## Классификация

Initial Lock: `LEGACY_ACTIVE / PARTIAL`.
Initial Profit exclusion: `MAPPED_PARTIAL`.
Far assignment: `MAPPED_PARTIAL / UNSAFE`.
