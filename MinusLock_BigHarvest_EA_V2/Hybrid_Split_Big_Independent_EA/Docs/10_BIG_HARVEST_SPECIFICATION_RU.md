# 10. Полная спецификация Big Harvest

Версия HSB.0R-C.11. Статус: нормативный source of truth.

Big trigger использует typed NextBigControlPrice и fresh snapshot. Перед action CandidatePlan binding проверяет Account+Symbol+Magic+CycleID+PlanID+StateRevision+roles+expected volumes. Risk gates fail-closed.

Порядок: revalidation→immutable HarvestPlan→persist actions→send requests→OnTradeTransaction→fill accumulation→actual role state→Economic Ledger source deals→exactly-once Allocation Ledger→единый Final Close→иначе Partial Far→reconciliation→следующий plan.

Actual DealNet включает profit, swap, commission, fee. Каждый source принадлежит текущему cycle/action; foreign, opening DEAL_ENTRY_IN, Initial Profit и duplicate source запрещены. Buckets FinalReserve, PartialFarBudget, TransitionBudget, Carry, Residual изолированы; negative DealNet не создаёт credit.

Partial fill не завершает role action. Retry использует same ActionID после history recheck; timeout ставит reconciliation barrier. Следующая role/level запрещена до settlement и reconciliation.

Final Close проверяется до Partial Far по единой authority. Partial Far никогда не потребляет FinalReserve. При failed final gate используется только допустимый PartialFarBudget.

Far SELL: closing BUY по Bid, SELL по Ask; Far BUY зеркален. Stale price, unknown deal, ownership mismatch, allocation conflict или risk uncertainty→RECONCILING/TERMINAL_SAFE.

Restart восстанавливает expected actions/source deals/consumptions; replay identical=NO-OP. Owner Scenarios/BigHarvest+Execution+Money. Tests: обе стороны, multideal partial fills, costs, retry/timeout, duplicate, restart before/after allocation, risk rejection.