# 15. Risk, Margin, Drawdown и Emergency contract

Версия HSB.0R-C.16. Статус: нормативный source of truth.

## Configurable limits
MaxProjectedMarginPercent (0..100), MinimumProjectedMarginLevel (>0), MinimumFreeMarginMoney (≥0), MaximumCycleDrawdownPercent (0..100), MaximumAccountDrawdownPercent (0..100), MaximumGrossExposure (>0), MaximumManagedPositions (integer>0), RiskToleranceMoney (≥0). Research-only values не являются production defaults. Invalid/missing/out-of-range input = fail-closed.

## Gate order
Ownership→snapshot freshness→spread→broker volume→ProjectedMarginAfter/OrderCalcMargin→FreeMarginAfter→cycle/account drawdown→gross/net exposure→WorstCase/GapStress→Transition caps→decision. Gate не меняет state/roles и не отправляет request.

## Risk money
`RiskOld=LossMoney(CurrentBasket→AdverseRiskControlPrice)`; `RiskNext=LossMoney(ProjectedNextBasket→same control basis)`. Обязательно `RiskNext<RiskOld-RiskToleranceMoney`, если не применяется более строгий terminal contract. BUY/SELL используют executable side и asymmetric tick values, commissions, swap, spread/slippage.

## Transition caps
AllowedTransitionLoss=min(absolute money cap,equity percent cap,OldFar risk percent cap,cumulative cycle cap). Failed cap запрещает Small Transition.

## Emergency
Triggers: margin emergency, drawdown emergency, identity conflict, persistence corruption, unknown position, duplicate Far, repeated broker failure, manual kill. Emergency отделена от Final Close, может фиксировать loss, не получает recovery PASS, блокирует новые actions и переводит terminal-safe/manual review. Auto-resume запрещён.

## REAL_LIMITED
Даже валидные limits не разрешают real trading. REAL_LIMITED требует whitelist, one cycle per Symbol+Magic, all readiness gates, Demo Forward PASS, daily/cycle/account loss caps, kill switch, evidence и explicit administrator approval.

Owner Risk/*+Money/BrokerMoneyModel. Tests: low margin, spread/gap, asymmetric ticks, drawdown thresholds, transition caps, emergency/no auto-resume, REAL_LIMITED refusal.