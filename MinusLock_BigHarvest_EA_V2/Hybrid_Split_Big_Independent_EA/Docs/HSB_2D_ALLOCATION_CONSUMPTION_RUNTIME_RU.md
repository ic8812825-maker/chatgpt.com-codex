# HSB.2D — Allocation и Consumption Runtime

Runtime использует подтверждённый `HSBI_ReserveAllocationSource` и `HSBI_ReserveConsumptionKey`. Conservation проверяет сумму allocation buckets и alreadyConsumed относительно allocatableNet. Запрещены foreign plan/revision, projected-only source, повторный ReserveShare, double count и conflicting duplicate. Общая RecoveryMoney не заменяет независимые reserve/far proofs.
