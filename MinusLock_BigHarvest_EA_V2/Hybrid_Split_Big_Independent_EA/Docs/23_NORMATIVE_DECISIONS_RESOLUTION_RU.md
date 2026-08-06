# 23. Единый реестр нормативных решений HSB.0R

Версия: HSB.0R.2
Статус: IN_PROGRESS

## Назначение

Документ является единственным реестром решений `HSBI-DEC-001..012`. Все решения проверены на возможность закрытия через точную архитектуру, допустимый диапазон, fail-closed validation и research-only конфигурацию без преждевременного объявления production optimum.

## Аудит критичности

| Decision | Тема | До HSB.0R | Итоговая критичность | Можно отложить конкретные значения? | Условие |
|---|---|---:|---:|---|---|
| HSBI-DEC-001 | ratios | P1 | P1 architecture / values deferrable | Да | диапазоны, три закона, rounding и gates фиксированы |
| HSBI-DEC-002 | allocation shares | P1 | P1 architecture / values deferrable | Да | conservation, source ownership, bucket isolation фиксированы |
| HSBI-DEC-003 | control prices | P1 | P1 | Нет | типы цен, Bid/Ask, freshness и proof grid обязательны |
| HSBI-DEC-004 | Future Small depth | P1 | P1 | Частично | exact recursion + conservative bound обязательны |
| HSBI-DEC-005 | NewFar objective | P1 | P1 | Нет | deterministic minimum-safe selection обязательна |
| HSBI-DEC-006 | emergency policy | P1 | P1 | Нет | отделена от recovery Final Close |
| HSBI-DEC-007 | transition loss | P1 | P1 architecture / limits configurable | Да | четыре одновременных limit gates |
| HSBI-DEC-008 | Final Close threshold | P1 | P1 architecture / value configurable | Да | money threshold + execution buffer обязательны |
| HSBI-DEC-009 | margin/drawdown | P1 | P1 architecture / values configurable | Да | fail-closed gate order обязательна |
| HSBI-DEC-010 | symbol/cycle scope | P1 | P1 | Нет | one cycle per symbol generation 1 |
| HSBI-DEC-011 | persistence backend | P1 | P1 | Нет | versioned file store + journal |
| HSBI-DEC-012 | future real limits | P1 | P1 | Нет | REAL_LIMITED contract; торговля остаётся запрещена |

## Общие владельцы и тесты

- Planning: ratios, control prices, Future Small, NewFar objective.
- Money: allocation, transition loss, Final Close threshold.
- Risk: margin, drawdown, emergency triggers.
- Core/Identity: Symbol, Magic, CycleID scope.
- Persistence: snapshot and journal backend.
- Execution: real-limited enforcement.

Все решения должны иметь unit, integration и Strategy Tester mapping в `19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md`.
