# Hybrid Split Big — решения, требующие Администратора

Ни один вопрос ниже не решён Математиком. Рекомендация — безопасная стартовая позиция, а не изменение торгового кода.

| ID | Решение | Варианты | Рекомендация Математика | Последствия | Блокирует кодирование |
|---|---|---|---|---|---|
| ADMIN-Q01 | `MaximumAllowedTransitionLoss` | 0; положительный money cap | 0 на первом профиле | positive cap требует ledger loss | Да |
| ADMIN-Q02 | `MaxCumulativeTransitionLoss` | 0; money; % InitialFarRisk | 0 на первом профиле | определяет допустимость серии переходов | Да |
| ADMIN-Q03 | `FutureSmallDepth` | local; depth D; analytic bound | depth=1 + q bound | глубина повышает CPU, не доказывает рынок | Да |
| ADMIN-Q04 | `TerminalSafeStatePolicy` | manual hold; emergency close | manual hold без новых рисков | определяет fate residual exposure | Да |
| ADMIN-Q05 | Worst Case profile | broker-specific values | values from broker and admin | TBD blocks normative Worst Case PASS | Да |
| ADMIN-Q06 | BigTrend optional | strict T>0; optional T=0 | strict | optional mode меняет gates/tests | Да |
| ADMIN-Q07 | SmallBase optional | strict S>0; optional S=0 | strict | optional mode меняет slope/flow | Да |
| ADMIN-Q08 | Harvest shares α/β/γ | any nonnegative sum=1 | explicit approved profile | governs all money buckets | Да |
| ADMIN-Q09 | Final Close buffers | money/tolerance values | nonzero broker-derived buffers | determines false-positive close risk | Да |
| ADMIN-Q10 | conservative margin policy | upper bound only; broker-aware+upper | both, upper is mandatory fallback | affects opening eligibility | Да |
