# AUDIT 02 — денежные границы и сохранение

## Слои и authority

| Величина | Основание | Что не доказывает |
|---|---|---|
| ProjectedBasketNet | Quotes, proposed positions, cost model | Actual deal/funding |
| ProjectedCloseNowNet | Close-side Bid/Ask, costs, open positions | Реальный fill |
| ActualRealizedDealNet | Profit+Swap+Commission+Fee фактических deals | Полноту history/право harvest |
| ReconciledEconomicNet | Independent history + EA-origin mapping + component equality | Распределение/остаток источника |
| EligibleSourceGrant | Approved role/policy + positive posted reconciled source | Свободный Reserve |
| AvailableReserve | Grant reconciliation + consumed/reserved owners + complete journal | Durable/concurrent proof само по себе |

Отсутствие provider/history не ноль: UNAVAILABLE. Локальные production DTO-флаги projected/runtimeConfirmed/sourceReconciled не являются независимой broker authority. Whole-chain conversion и global ledger в production отсутствуют.

## Инварианты кандидата, не утверждение владельца

`G=C+R+F`, `RemainingGross=R+F`, `C,R,F>=0`. Reserve d: `(R,F)→(R+d,F-d)` при d<=F. Release owner d: `(R,F)→(R-d,F+d)`. Unreserved consume: `(C,F)→(C+d,F-d)`. Owner reserved consume: `(C,R)→(C+d,R-d)`. Все операции сохраняют G. Free не равно RemainingGross при R>0. `PREPARED sum grants+Unallocated=Eligible`; spending запрещён. `COMMITTED sum grants=Eligible,Unallocated=0` — pending D-01. ResidualHeld и Unallocated не расходуются без policy.

Проверки `HSBI_FULL_SYSTEM_AUDIT_02_ledger_tests.py` используют новый независимый integer-minor-unit fixture: 22 literal сценария funding/reserve/release/consume/replay/reconstruction; каждый отказ/NO_OP проверяет before==after. Это specification model одного source-level pool с immutable allocation vector, **не полная реализация отдельных spendable buckets**. Модель не импортирует production. Её PASS не доказывает production, broker, durable или concurrent свойства. Snapshot reconstruction подтверждает только accounting равенства по доверенному fixture, не историческую eligibility.

## Полная стоимость и контрпримеры

В точных rational fixtures учтено: positive Harvest +3.83 при CyclePnL -1.64; Balance1003.46 и Equity998.46 при стартовом1000; Small+10/Big-20; Big+20/Small-30; FarLoss50/Reserve30; Profit2 Commission-2 Swap-1; gap100→110 при step5 не доказывает два fill; текущий loss0 после -15,+100 не отменяет peak15>cap12. Opening commission .37 и future Far exit .10 не смешиваются с уже realised Harvest. Формула `CyclePnL=RealizedNet+UnrealizedCloseNowNet` верна лишь при согласованном учёте будущих costs. Reserve/allocation второй раз к PnL не добавляются.

Частичное закрытие Far с сохранением basket улучшает локальный slope, но дальнейшее закрытие Trend/Core может ухудшить exposure. Поэтому partial Far не гарантирует recovery geometry после всей последовательности. Например C1,T1,S.5,F1 slope.5; после Far.2 close и Trend1 close slope=-.3. Полный actual execution этого примера не выполнялся.

Local validator проверяет форму/суммы, но не global uniqueness одного broker deal в нескольких allocations, complete history, owner journal, restart/CAS. Production preservation не доказывает сохранение экономических средств. Global funding остаётся UNPROVEN.
