# HSBI-DEC-007 — Maximum Transition Loss

Статус: `DEFERRED_WITH_SAFE_CONTRACT`.

`TransitionNet=ΣActualClosingDealNet` по SmallBase, OldFar, BigTrend и staged BigCore close; money, account currency. `TransitionLossMoney=max(0,-TransitionNet)`.

До плана проверяются одновременно: абсолютный лимит, процент текущей equity, процент OldFar adverse risk и cumulative cycle limit. Нормативный допустимый предел — минимум четырёх рассчитанных caps. Конкретные caps являются конфигурацией, строго положительны, валидируются и не имеют real default. Превышение projected cap блокирует transition; превышение actual cap переводит в RECONCILIATION/TERMINAL_SAFE и запрещает новые открытия.

Owner: `Money/TransitionBudget` и `Risk/BasketRisk`. Tests: four-cap minimum, actual costs, cumulative limit, partial fills, BUY/SELL symmetry.
