# Small Transition и единственный NewFar

Версия 1.0. Статус: нормативный.

## Нормативный порядок

Revalidation → persist immutable TransitionPlan → close SMALL_BASE 100% → confirm deals → close OldFar 100% → confirm → close BIG_TREND 100% → confirm → close planned BIG_CORE part → confirm all fills → read actual remaining BIG_CORE → validate N → promote same ticket/identifier to NEW_FAR → persist next cycle → role FAR.

- `HSBI-SMALL-001`: порядок неизменяем.
- `HSBI-SMALL-002`: каждый close — отдельная persisted Action.
- `HSBI-SMALL-003`: partial fill блокирует следующий step.
- `HSBI-SMALL-004`: OldFar, SmallBase и BigTrend закрыты до promotion.
- `HSBI-NF-001`: NewFar создаётся только из actual BIG_CORE residual.
- `HSBI-NF-002`: original BIG_CORE ticket/identifier сохраняются.
- `HSBI-NF-003`: exactly one managed position remains.
- `HSBI-NF-004`: `0<N<F` после broker rounding.

## Запреты

DUAL_TAIL, сохранение OldFar, BigTrend/SmallBase как Far, requested residual как N, новый ticket без отдельной нормы, следующий basket до reconciliation, продолжение после mismatch запрещены.

## Пример

ДЕМОНСТРАЦИОННЫЙ ПРОФИЛЬ: OldFar=1.00, Core=1.60, planned residual candidate=0.50. После фактических fills actual Core=0.49 — solver валидирует именно 0.49; requested 0.50 не используется. Второй transition может дать, например, 0.24 только при полном повторном proof.

## Restart/errors

Restart на любом шаге восстанавливает TransitionPlan, completed ActionIDs и pending fills. Две позиции после ожидаемого завершения → CONFLICT. Missing deal или altered identifier → TERMINAL_SAFE.

## Контракт

Вход: active basket и Small trigger. Выход: один FAR нового cycle либо safe error. Preconditions: immutable plan, ownership/risk/reconciliation PASS. Postconditions: old roles closed, actual residual promoted, ledgers/persistence committed. Owner: Scenarios/SmallTransition + Planning/NewFarSolver. Тесты: both directions, every restart point, partial/reject/duplicate, actual residual deviation. Открытые вопросы: Small confirmation, transition budget и max loss.