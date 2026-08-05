# Роли и identity Hybrid Split Big

Версия 1.0. Статус: нормативный.

## Роли

| Роль | Направление | Создание | Закрытие | Может стать Far |
|---|---|---|---|---|
| INITIAL_BUY | BUY | Initial Lock | как INITIAL_PLUS либо остаётся FAR | только если минусовая нога |
| INITIAL_SELL | SELL | Initial Lock | как INITIAL_PLUS либо остаётся FAR | только если минусовая нога |
| INITIAL_PLUS | любая | классификация прибыльной initial leg | закрывается 100% | нет |
| FAR | против Big | после actual close INITIAL_PLUS или commit NEW_FAR | Partial/Final/Small | уже Far |
| BIG_CORE | Big | basket open | Harvest либо staged Small close | да, только actual residual |
| BIG_TREND | Big | basket open | 100% Harvest/Small | нет |
| SMALL_BASE | сторона Far | basket open | 100% Harvest/Small | нет |
| NEW_FAR | направление BIG_CORE | только после Small validation | сразу commit как FAR | переходная роль |

## Identity tuple

`ManagedIdentity = Symbol + Magic + CycleID + PositionIdentifier + Role`.
Ticket используется как адрес текущей позиции, но ownership подтверждается всем tuple.

- `HSBI-ID-010`: перед каждой irreversible action проверяются Symbol, Magic, CycleID, ticket, identifier, role, direction, expected/actual volume, StateRevision, PlanID и ActionID.
- `HSBI-ID-011`: comment не является source of truth.
- `HSBI-ID-012`: в одном cycle существует не более одного FAR/NEW_FAR candidate.
- `HSBI-ID-013`: foreign position никогда не принимается managed по одному Magic.
- `HSBI-ID-014`: role promotion сохраняет исходный BIG_CORE identifier.
- `HSBI-ID-015`: mismatch блокирует action и переводит систему в reconciliation.

## Preconditions / Postconditions

Preconditions: reconciled snapshot и уникальный CycleID. Postconditions: каждая managed position имеет одну роль и одного owner. Запрещено: duplicate role ownership, missing identifier, generic Big/Small, два Far.

## Restart и errors

При restart роли сопоставляются по persisted snapshot + actual identifier + deals; угадывание запрещено. Неоднозначность → `CONFLICT` → `STATE_TERMINAL_SAFE`. Будущий owner: `Core/Identity`, `Execution/OwnershipGuard`, `Persistence/Reconciliation`. Тесты: same Magic different symbols, stale ticket, reused ticket, altered volume, duplicate Far. Открытые вопросы: формат Magic namespaces и лимит параллельных cycles.