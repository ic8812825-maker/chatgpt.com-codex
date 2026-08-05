# 3.1.6.3.12 — persistence всех фаз Hybrid Split Big

## Фактическая реализация

Persistence сосредоточена главным образом в `StateMachine.mqh` и использует Terminal Global Variables через scoped `StateKey`. Сохраняются state, cycle context, role tickets/identifiers/lots/prices, pending operation fields, old Far, Hybrid reverse plan fields, Reserve ledger и Reserve transaction phases.

Положительные элементы:

- 64-bit values разбиваются на high/low 32-bit части.
- Reserve transaction имеет persisted phase и context identity.
- Initial BUY/SELL сохраняются отдельно.
- Pending actions и retry fields сохраняются.
- OldFar и Split/Hybrid role context сохраняются.
- Recovery после restart запускает position/state integrity и reconciliation.

## Неполнота по обязательным restart-точкам

- Нет единой schema/versioned atomic snapshot всего cycle state.
- Нет доказанного общего checksum всего persistence set.
- Запись множества Global Variables не атомарна; crash между отдельными `GlobalVariableSet` создаёт смешанную revision.
- StateRevision и PlanID не являются универсальными persisted guards каждого action.
- Нет общего persisted Deal Event Ledger с parent EventID для каждого open/close/fill.
- CandidatePlan целиком до первого open не доказан как immutable persisted object.
- Mid-transaction recovery зависит от pending text/type, position polling и history reconstruction.

## Оценка restart-точек

Initial phases, role openings, pending closes, Small transition и Reserve transaction имеют частичное покрытие. Точки `request sent → order placed → partial deal → final deal → allocation` не могут быть полностью восстановлены exactly-once без OnTradeTransaction/Event ledger.

## Замечания

- `PERSIST-001 P1`: persistence не является атомарным versioned cycle snapshot.
- `PERSIST-002 P1`: отсутствует общий persisted EventID/DealTicket lifecycle.
- `PERSIST-003 P1`: CandidatePlan/StateRevision binding неполон.
- `PERSIST-004 P1`: crash между GlobalVariable writes может создать mixed state.
- `PERSIST-005 P2`: checksum/fingerprint покрывает отдельные области, но не весь state.

Классификация: `MAPPED_PARTIAL / UNSAFE`.
