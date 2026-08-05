# Risk и Margin contract

Версия 1.0. Статус: нормативный.

До каждого open/promotion проверяются ProjectedMarginAfter, MarginLevelAfter, FreeMarginAfter, WorstCaseLossMoney, GapLoss, spread/slippage/commission/swap, gross/net exposure и drawdown.

`RiskOld=LossMoney(CurrentBasket→ControlPrice)`; `RiskNext=LossMoney(ProjectedNextBasket→ControlPrice)`. Требование: `RiskNext<RiskOld-RiskTolerance`, если пользователь не утвердил иной безопасный contract.

- `HSBI-RISK-001`: risk рассчитывается в money через broker model, не только ratio.
- `HSBI-RISK-002`: `OrderCalcMargin` и executable market side обязательны.
- `HSBI-RISK-003`: Worst Case PASS обязателен вместе с Base PASS.
- `HSBI-RISK-004`: risk gate не изменяет roles и не отправляет сделки.
- `HSBI-RISK-005`: emergency policy отделена от profitable Final Close.
- `HSBI-RISK-006`: stale prices, invalid margin mode или non-finite result блокируют action.

Контракт: вход — reconciled/current/projected baskets, control snapshots и account state; выход — typed PASS/REJECT/ERROR с provenance. Preconditions: fresh symbol properties. Postconditions: accepted plan содержит immutable risk proof. Restart: proof fingerprint сверяется заново перед execution. Owner: Risk/* и Money/BrokerMoneyModel. Тесты: low margin, gap, spread, asymmetric ticks, commissions, swaps, drawdown. Открытые решения: limits, control price и emergency actions.