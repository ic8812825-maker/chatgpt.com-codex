# Единый нормативный Final Close

Версия 1.0. Статус: нормативный.

## Единственная authority

Final Close разрешён только Scenarios/FinalClose через FinalCloseCalculator. Другие сценарии могут лишь запросить preview.

Обязательные условия:

`RecoveryPLCloseNow > MinimumRecoveryProfitMoney` и
`FinalReserveAvailable + OtherExplicitlyAllowedFinalSources >= RequiredFinalCloseCoverage`.

Дополнительно: NoPendingTransactions, PositionsReconciled, NoUnknownDeals, OwnershipValid, StateRevisionValid, fresh market snapshot, spread policy PASS, execution costs included.

- `HSBI-FC-001`: RecoveryPL=`RealizedCycleNet+ΣOpenCloseNowNet`, без повторного Reserve.
- `HSBI-FC-002`: theoretical Far loss не заменяет `OrderCalcProfit`/broker money.
- `HSBI-FC-003`: MaxLevel не является прибыльным close gate.
- `HSBI-FC-004`: отрицательный/недостаточный RecoveryPL запрещает Final Close.
- `HSBI-FC-005`: Final Close action завершается только actual deals и zero managed positions.
- `HSBI-FC-006`: emergency liquidation отделена и не маркируется успешным recovery.

## Пример

ДЕМОНСТРАЦИОННЫЙ ПРОФИЛЬ: RealizedCycleNet=500, open close-now=-450, RecoveryPL=50; minimum=10. При coverage requirement 430 и allowed sources 440 gate PASS. Reserve уже входит в allocation realized 500 и не делает RecoveryPL=490.

## Restart/errors

Persisted FinalClosePlan содержит snapshot/fingerprint, expected roles/actions и coverage. Partial fill удерживает executing state. Unknown deal/price stale/ownership mismatch → reconciliation; повторный send запрещён.

## Контракт

Вход: reconciled basket, ledgers, fresh prices. Выход: CYCLE_CLOSED либо typed reject/pending/conflict. Preconditions: all gates. Postconditions: positions closed, ledger consumed exactly once, final P/L reported. Owner: Money/FinalCloseCalculator + Scenarios/FinalClose. Тесты: negative PL, double counting, gaps, partial fills, restart, foreign position. Открытые вопросы: allowed final sources, safety buffer и minimum profit.