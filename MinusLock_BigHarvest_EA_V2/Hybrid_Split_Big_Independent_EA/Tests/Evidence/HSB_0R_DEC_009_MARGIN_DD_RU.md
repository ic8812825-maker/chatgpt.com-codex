# HSBI-DEC-009 — margin и drawdown

Статус: `DEFERRED_WITH_SAFE_CONTRACT`.

Обязательные параметры: MaxProjectedMarginPercent, MinimumProjectedMarginLevel, MaximumCycleDrawdownPercent, MaximumAccountDrawdownPercent, MinimumFreeMarginMoney, MaximumGrossExposure, MaximumManagedPositions. Все проходят finite/range validation; real defaults отсутствуют.

До нового открытия gate order фиксирован: Ownership → snapshot freshness → spread → broker volume → OrderCalcMargin/projected margin → free margin → cycle/account drawdown → gross exposure → worst-case/gap → decision. Любой неизвестный расчёт — fail-closed. Закрывающие risk-reducing actions не блокируются обычным entry gate, но остаются ownership/transaction-safe.

Research caps явно маркируются RESEARCH_ONLY. Owner: `Risk/MarginModel`, `Risk/DrawdownGate`, `Risk/BasketRisk`. Tests: low margin, zero equity, gap, spread expansion, multi-symbol aggregate, fail-closed.
