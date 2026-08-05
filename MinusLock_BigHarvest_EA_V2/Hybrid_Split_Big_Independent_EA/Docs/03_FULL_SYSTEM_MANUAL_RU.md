# Полный системный мануал Hybrid Split Big

Версия 1.0. Статус: нормативный. Документ самодостаточен.

## Назначение

Minus Lock начинается одновременными BUY и SELL. После движения рынка прибыльная initial leg закрывается и полностью исключается из recovery. Оставшаяся убыточная leg становится FAR. Для восстановления создаётся корзина: BIG_CORE и BIG_TREND в направлении восстановления, SMALL_BASE в направлении FAR. При движении к Big корзина собирает realized money, который распределяется между FinalReserve, PartialFarBudget, TransitionBudget/Carry. При развороте Small Transition закрывает SMALL_BASE, OldFar и BIG_TREND, уменьшает BIG_CORE и превращает только его фактический остаток в новый FAR.

## Жизненный цикл

```text
IDLE → Initial plan → BUY/SELL actual fills → Initial Lock
→ actual close profitable leg → FAR
→ immutable CandidatePlan → Core/Trend/Small actual fills
→ BASKET_ACTIVE
→ Big Harvest → allocation → Final Close или Partial Far → следующий level
или
→ Small Transition → actual BIG_CORE residual → NEW_FAR → FAR нового cycle
→ Final Close → CYCLE_CLOSED
```

- `HSBI-GEN-020`: каждый irreversible step имеет persisted action и actual transaction outcome.
- `HSBI-GEN-021`: следующий scenario запрещён при pending action.
- `HSBI-GEN-022`: Final Close и emergency liquidation — разные authorities.

## Тренд вверх: FAR SELL

FAR=SELL; BIG_CORE/ BIG_TREND=BUY; SMALL_BASE=SELL. Big levels расположены выше reference. При достижении уровня закрываются плановые Big Harvest legs только после revalidation. Их actual DealNet распределяется. Final Close проверяется первым; иначе Partial Far использует только свой budget. При возврате к Small trigger выполняется строгий Small Transition.

## Тренд вниз: FAR BUY

Полностью симметрично: FAR=BUY; BIG_CORE/BIG_TREND=SELL; SMALL_BASE=BUY; Big levels ниже reference. BUY закрывается по Bid, SELL — по Ask. Ни одна формула не меняется по смыслу, меняется только direction/market side.

## Развороты

Ложное касание не запускает transition без подтверждённого trigger и свежего snapshot. После persist transition plan повторный trigger — NO-OP. Partial fill блокирует продолжение до accumulation/reconciliation. Каждый завершённый transition обязан уменьшить Far на broker grid. При невозможности безопасного N система переходит terminal-safe, а не создаёт второй tail.

## Необратимые действия

Для open/close/partial/promotion обязательны: preconditions → immutable plan/action → persist → request → OnTradeTransaction → fills → actual position read → ledger → persist result → FSM advance. Reject/requote/timeout не продвигают FSM. Rollback Initial BUY разрешён только как отдельная action после неуспеха SELL и подтверждается actual deal.

## Демонстрационный профиль, не production default

```text
StartLot=1.00; broker min/step=0.01
F=1.00; C=1.60; T=0.25; S=0.60; Bnet=1.25
ReserveShare=0.90; PartialShare=0.10; Target example N=0.50
BigLevel1=100 points; BigLevel2=150 points
```

Это только пример размерностей. Production profile не утверждён.

Пример Far SELL: BUY legs растут при движении вверх; Big Harvest на L1/L2 формирует actual DealNet. При доступном PartialFarBudget=120 money и close-cost 400 money/lot: raw=0.30 lot, floor=0.30; FinalReserve не участвует. При Small Transition план закрывает S=0.60, F=1.00, T=0.25, затем часть C; actual residual, например 0.50, становится FAR. Второй transition может дать 0.25 при прохождении всех gates. Far BUY симметричен.

Final Close example: `RealizedCycleNet=500`, open close-now net `-450`, RecoveryPL=50; minimum=10. Coverage также обязана быть достаточной. Reserve не прибавляется повторно к 500.

## Контракт

Входы: reconciled state, market snapshot, broker properties, утверждённый profile. Выходы: plan/action/state. Preconditions: no pending, ownership valid, risk gates. Postconditions: ledgers conserved, один Far, state persisted. Запрещено: Legacy, DUAL_TAIL, requested residual как NewFar, state advance до actual. Restart: восстановление по snapshot + MT5 facts + event ledger. Owners: все архитектурные слои по PROJECT_MAP. Тесты: оба направления, уровни, reversals, partial fills, restart. Открытые числовые решения — реестр 22.