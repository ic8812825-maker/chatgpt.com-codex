# Broker-valid minimum-safe NewFar Solver

Версия 1.0. Статус: нормативный.

## Кандидаты

Solver строит дискретный набор `N={VolumeMin, VolumeMin+Step,...,<F}` и оценивает только broker-valid lots. Простая формула `F×TargetRatio` может задавать ориентир, но не решение.

Для каждого N обязательны: compression, maximum ratio, minimum lot/step, NextBig, RecoveryPL monotonicity, Reserve Catch-Up money proof, margin, RiskNext, Future Small, finite catch-up и terminal-lot semantics.

- `HSBI-NF-010`: unsafe candidate никогда не выбирается.
- `HSBI-NF-011`: после rounding все gates пересчитываются.
- `HSBI-NF-012`: solver детерминирован на одном snapshot/profile.
- `HSBI-NF-013`: до утверждения objective policy автоматический production choice запрещён.
- `HSBI-NF-014`: chosen planned N не становится Far; Far создаётся только из actual residual и повторной validation.

## Selection

Предпочтительная политика-кандидат: минимальный безопасный N, уменьшающий tail максимально, но только если transition close lot и все future gates допустимы. Альтернативная Score-функция (`w1 Risk+w2 Margin+w3 reversals-w4 recovery`) остаётся OPEN DECISION.

## Граничные случаи

Нет кандидатов → terminal-safe. N=F или N=0 запрещены. Residual ниже min lot запрещён. Coarse step может сделать аналитический q недостижимым. Actual residual после fill проверяется заново и может быть rejected.

## Контракт

Вход: F, actual Core, broker grid, immutable snapshot, policy. Выход: ordered candidate proofs/chosen candidate/reason. Preconditions: transition plan not executing. Postconditions: deterministic fingerprint. Restart: plan/candidate set digest persisted. Owner: Planning/NewFarSolver. Тесты: min/step, both directions, no candidate, objective ties, coarse grid, actual deviation. Открытый вопрос: objective function и Future Small depth.