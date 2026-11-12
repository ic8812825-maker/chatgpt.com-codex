# AUDIT 02 — независимая перепроверка P0
База: `707f51d82217b13613c5d56d9d51d10bac5a2412`. Изменений production нет. 9 локальных source-дефектов; FSA-010 — UNIMPLEMENTED independent-provider boundary. Все 10 не являются достижимыми торговыми обходами текущего EA.
Новые first-attempt fixtures воспроизведены без изменения expected. FSA010 имеет positive independent reject и copied-expected observation; полный NewFar solver/broker не исполнялся.

## FSA-001 — P0 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Money/HSBI_EconomicLedgerTypes.mqh', 'SHA256': 'd9bcbef0fa7b6c5da61e7bafa6a6314458601252a2e580aac21396daadf95ed4', 'Function': 'HSBI_SameEconomicRecord', 'Line': 9, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/08:6,9,15; D08; L01
- **Actual**: Сравнение не включает Profit/Swap/Commission/Fee и другие immutable поля.
- **Expected**: Сопоставлять полный утверждённый immutable payload.
- **Counterexample**: P50/C0 против P70/C-20, Net50. Компоненты различны при неизменном ключе.
- **TestID**: FSA001_COMPONENTS
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: D-08, NUM-CODEC, MQL-DOMAIN
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-002 — P0 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Money/HSBI_AllocationLedgerTypes.mqh', 'SHA256': 'b539c3c52089e22c2e5cba5a95b81bdc5267b59402bf0f3662f48e80dc1b155c', 'Function': 'HSBI_ClassifyAllocationDuplicate', 'Line': 8, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/08:12,15; L02
- **Actual**: Равенство суммы ошибочно заменяет равенство вектора.
- **Expected**: Тот же allocation event, изменённый bucket vector → CONFLICT.
- **Counterexample**: Reserve50/PF0 против Reserve0/PF50.
- **TestID**: FSA002_VECTOR
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: D-01, D-08
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-003 — P0 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Money/HSBI_ReserveCatchUpEvaluator.mqh', 'SHA256': '5d967cf22e7d0fdc3d37aae6077b15c4330526dcef4c5b8eda74340a64ff174d', 'Function': 'HSBI_EvaluateReserveCatchUp', 'Line': 35, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/08:15; Docs/32:7; M01
- **Actual**: Consumption key проверен по форме/plan/revision, но не по sourceAllocationKey/sourceDealKey authority.
- **Expected**: Сверять оба namespace с независимой allocation.
- **Counterexample**: Источник TEST-D101/ALLOC-A, consumption OTHER-ACCOUNT/OTHER-ALLOC.
- **TestID**: FSA003_FOREIGN_ALLOCATION
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: D-07, D-08
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-004 — P0 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Money/HSBI_ReserveCatchUpEvaluator.mqh', 'SHA256': '5d967cf22e7d0fdc3d37aae6077b15c4330526dcef4c5b8eda74340a64ff174d', 'Function': 'HSBI_EvaluateReserveCatchUp', 'Line': 35, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/08:24; Docs/32:3-7; reserve consumption
- **Actual**: В ветке not alreadyAllocated отсутствует вычитание/запрет alreadyConsumed.
- **Expected**: Исчерпанный source не создаёт новый grant; global uniqueness требует реестра.
- **Counterexample**: Allocatable50, consumed50, reserveAllocated0, eligible50, share.8 → gain40.
- **TestID**: FSA004_EXHAUSTED
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: FUNDING-GLOBAL-ATTRIBUTION
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-005 — P0 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Risk/HSBI_RiskGateResult.mqh', 'SHA256': 'd0d7072973dac81be9284562046b7227ecfafbe14962c9ad05a3f8e2c73585c8', 'Function': 'HSBI_ValidateRiskInput', 'Line': 6, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/15:6,9; Docs/24:11
- **Actual**: Сравнения с NaN ложны; нет finite/domain validation.
- **Expected**: Malformed/nonfinite не даёт passed. Отрицательная projected margin требует явного domain.
- **Counterexample**: projectedMargin=NaN либо -1 при согласованных остальных gates.
- **TestID**: FSA005_NAN
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: MQL-DOMAIN
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-006 — P0 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Execution/HSBI_TransactionTypes.mqh', 'SHA256': '1b244dc72cd345f0f032dde14eb89227db20a7333cbc2c72afa2046c4720d8c9', 'Function': 'HSBI_TransactionBarrierPassed', 'Line': 9, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/07:15,21; actual fill validation
- **Actual**: abs(NaN-expected)>epsilon ложно, completion может пройти.
- **Expected**: Конечный положительный объём и подтверждённые факты до completion.
- **Counterexample**: expected1, accumulatedNaN, COMPLETED, ownership=true.
- **TestID**: FSA006_NAN
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: D-08, MQL-DOMAIN
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-007 — P0 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Money/HSBI_AllocationLedgerTypes.mqh', 'SHA256': 'b539c3c52089e22c2e5cba5a95b81bdc5267b59402bf0f3662f48e80dc1b155c', 'Function': 'HSBI_ValidateAllocationConservation', 'Line': 7, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/08:12,24; D01
- **Actual**: Неотрицательность отдельных bucket не проверяется.
- **Expected**: Каждая grant component >=0. Полное COMMITTED равенство отдельно pending D-01.
- **Counterexample**: Reserve-50/PF100 при source50; сумма50.
- **TestID**: FSA007_NEGATIVE_BUCKET
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: D-01
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-008 — P0 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Money/HSBI_MoneyState.mqh', 'SHA256': '0faeebfc6781198ead86e8cffac7e154947f1830e6b38d27d7900d069ac38396', 'Function': 'HSBI_ValidateMoneyState', 'Line': 5, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/08:12,24; fail-closed money state
- **Actual**: Infinity >=0 принимается; valid и revision игнорируются.
- **Expected**: Finite domain обязателен; правила valid/revision отдельно сформулировать.
- **Counterexample**: finalReserve=+Infinity. Дополнительно valid=false/revision0.
- **TestID**: MONEY_INF
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: BALANCE-SCHEMA-MAPPING, MQL-DOMAIN
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-009 — P0 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Core/HSBI_Context.mqh', 'SHA256': '7ae314b8f7e4183419943297885a6291afbf449a5d63490ca35757f737eb80ef', 'Function': 'HSBI_ValidateContext', 'Line': 33, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/00:12; Docs/02:25; exactly-oneFar
- **Actual**: FAR-count и проверка role-slot пропускают initialBuy/initialSell/newFarCandidate.
- **Expected**: Считать реальные активные FAR во всех слотах; отличать alias от двух позиций.
- **Counterexample**: farID100 и initialBuyID101 оба FAR, одинаковый owner.
- **TestID**: FSA009_INITIAL_SLOT
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: D-08, active-role schema
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-010 — P0 / UNIMPLEMENTED
- **Source**: {'File': 'Include/Planning/HSBI_NewFarSolver.mqh', 'SHA256': '9dcf60b6edc245a8a5ee3a05f35d4d8d26c12479f570a66aa5e4f0e703497cd2', 'Function': 'HSBI_SolveNewFar', 'Line': 94, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/31:3-7; D08; M02
- **Actual**: Caller переписывает proof identity, затем копирует её в expected. Независимый экономический provider отсутствует.
- **Expected**: Helper equality локально корректен; весь NewFar independent provenance не доказан.
- **Counterexample**: Helper отвергает чужой proof при независимом expected, принимает при copied expected.
- **TestID**: FSA010_INDEPENDENT_EXPECTED
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: D-02, D-08, provider reconciliation
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json
