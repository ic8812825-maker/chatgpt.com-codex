# Коррекция Этапа 3.1.5

Предыдущий PASS superseded. Исполняемая модель теперь использует строгие enums и broker grid,
неизменяемый EventSnapshot, последовательную reconciliation machine, Economic Ledger из unique
actual deals, tagged Allocation Ledger, Decimal partial-fill allocation, JSON round-trip/replay и
Final Close evaluator, самостоятельно читающий ledger/snapshot.

Positive matrix формируется как список структурированных результатов; pytest действительно собирает
параметризованные cases. Mutations меняют Policy и вычисленные Observables; независимый evaluator
не получает имя mutation/blocker. Validator агрегирует владельцев статусов и возвращает nonzero при
любом вычисленном blocker. Source guards являются только дополнительной защитой.

Production mapping остаётся PARTIAL: runtime MQL5 не изменялся, exact MT5 execution не доказан.
