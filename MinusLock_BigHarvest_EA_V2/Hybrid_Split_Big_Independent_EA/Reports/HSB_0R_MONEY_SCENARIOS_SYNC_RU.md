# Синхронизация money ledgers и сценариев

Нормативное дополнение к Docs/08–13.

Economic Ledger принимает только actual deals с полной identity и формулой `DealNet=Profit+Swap+Commission+Fee`. Opening IN не является harvest source; Initial Profit исключён. Allocation Ledger сохраняет per-source conservation и exactly-once keys.

Big Harvest: фактические closing deals C/T/S становятся source money; allocation выполняется только после reconciliation. Partial Far резервирует и потребляет только PartialFarBudget; FinalReserve недоступен. Unused reservation освобождается после actual outcome.

Final Close: одна authority, свежие broker prices, no pending/unknown, ownership valid, `RecoveryPLCloseNow >= MinimumRecoveryProfitMoney+ExecutionSafetyBuffer+Tolerance`; allocation buckets не прибавляются повторно. Emergency — отдельный loss route.

Small Transition: persisted immutable plan; actual close SmallBase→OldFar→BigTrend→staged BigCore; каждый следующий action после confirmed prior outcome; TransitionNet и caps считаются по actual deals; только actual residual original BigCore становится NewFar. Mismatch/partial pending блокируют продолжение.

Owners: Money/EconomicLedger, AllocationLedger; Scenarios/InitialLock, BigHarvest, PartialFar, FinalClose, SmallTransition. Tests: source ownership, conservation, duplicate/restart, transition loss, no double counting.
