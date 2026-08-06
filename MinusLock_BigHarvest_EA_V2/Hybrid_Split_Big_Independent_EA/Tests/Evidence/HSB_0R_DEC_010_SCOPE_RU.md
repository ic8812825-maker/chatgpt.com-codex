# HSBI-DEC-010 — Symbol, Magic и Cycle scope

Статус: `RESOLVED`.

Identity каждой сущности: AccountLogin + Symbol + Magic + CycleID + PositionIdentifier + Role. Для generation 1: `MaximumActiveCyclesPerSymbol=1`. Несколько символов разрешены только при независимых context, snapshot, ledgers, reserve, action registry и persistence namespace.

Один Magic на разных символах допустим, потому что Symbol обязателен в каждом key. Запрещены два active cycles на Symbol, общий Far/Reserve между symbols/cycles, ticket search без полного identity, close чужого цикла и глобальное назначение роли по comment.

Owner: `Core/Identity`, `Core/Context`. Tests: same Magic different symbols, duplicate cycle on symbol, foreign ticket, restart isolation.
