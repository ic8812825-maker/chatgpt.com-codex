# 02B-R1 — атомарный план после отдельного утверждения

Проверенная база подготовки `cb5e55cb38aa4f2eb5b58e5218462c6738f3097a`. `IMPLEMENTATION_ALLOWED=NO`. Это план будущей работы; никакой production-файл сейчас не разрешён к изменению этим документом. Перед R1 требуется явное утверждение D-01–D-08, scope фаз и соответствующих schema/migration choices; CR-09/geometry только отдельными решениями. Новый baseline проверяется отдельно, не выбирается автоматически.

Каждый этап имеет отдельный commit и review. Успешный subset gate не скрывает отложенные FAIL/UNPROVEN. Старые R0 tests/evidence не переписываются для зелёного результата. При известном defer тест остаётся BLOCKED с owner/next gate; production state не считается готовым.

## R1.1. Economic Record

**RequiredApprovedContracts:** D-01,D-02,D-08; canonicalization/account namespace schema.

**AllowedProductionFiles:** Include/Money/HSBI_EconomicLedgerTypes.mqh; новый Include/Money/HSBI_EconomicAuthorityTypes.mqh (interface-only). Имена новых файлов — предлагаемый allowlist после утверждения, не файлы, созданные R0A.

**ForbiddenChanges:** Не менять allocation formulas, geometry, NewFar, dispatch или historical evidence.

**EntryGate:** Утверждённые identity/schema/precision и clean baseline; read-only authority interface имеет UNAVAILABLE по умолчанию.

**ExitGate:** Полный immutable economic payload, independent namespace, canonical equality и versioned serialization; foreign/missing source fail-closed. Проверка должна выполняться на approved scope, без повышения full economic correctness.

**Tests:** D01-components-sum-mismatch; L01-component-digest; D08-namespace-*; exact duplicate и altered components/order/position/role; актуальные R8/R10/R12/R12A плюс scoped negative/mutation tests. MetaEditor/MQL5 checks отдельно; отсутствие инструмента => NOT_RUN.

**RollbackProcedure:** остановить зависимые consumers; сохранить snapshots/journal read-only; при явном решении администратора отдельным git revert вернуть собственный атомарный phase commit. Не использовать reset/rebase/amend. Downgrade новой schema без отдельно проверенной обратной миграции запрещён; старый код не должен принимать неизвестную schema. Поскольку trading остаётся запрещённым, rollback не создаёт компенсирующих сделок.

**CommitBoundary:** один production+tests commit строго R1.1; не объединять с другими фазами. Отдельный review/diff/source-hash gate до перехода к следующей фазе.

**RemainingBlockers:** Нет реального history provider/durable journal; брокерская подлинность остаётся UNPROVEN.

## R1.2. Allocation Ledger

**RequiredApprovedContracts:** D-01,D-02,D-03,D-07; R1.1 receipt schema.

**AllowedProductionFiles:** Include/Money/HSBI_AllocationLedgerTypes.mqh; Include/Money/HSBI_ReserveAllocationTypes.mqh; новый Include/Money/HSBI_AllocationBalanceTypes.mqh. Имена новых файлов — предлагаемый allowlist после утверждения, не файлы, созданные R0A.

**ForbiddenChanges:** Не менять Big/Small geometry, solver objective, costs, dispatch.

**EntryGate:** R1.1 принят отдельно; явно задано original/remaining у каждого legacy поля; неизвестное не мигрируется.

**ExitGate:** Immutable grant и balance разделены; committed equality и bucket isolation; replay per-bucket/policy; no hidden Residual spend. Проверка должна выполняться на approved scope, без повышения full economic correctness.

**Tests:** D01-*; L02-bucket-digest; D03-*; policy-version/replay/residual/negative/nonfinite vectors; актуальные R8/R10/R12/R12A плюс scoped negative/mutation tests. MetaEditor/MQL5 checks отдельно; отсутствие инструмента => NOT_RUN.

**RollbackProcedure:** остановить зависимые consumers; сохранить snapshots/journal read-only; при явном решении администратора отдельным git revert вернуть собственный атомарный phase commit. Не использовать reset/rebase/amend. Downgrade новой schema без отдельно проверенной обратной миграции запрещён; старый код не должен принимать неизвестную schema. Поскольку trading остаётся запрещённым, rollback не создаёт компенсирующих сделок.

**CommitBoundary:** один production+tests commit строго R1.2; не объединять с другими фазами. Отдельный review/diff/source-hash gate до перехода к следующей фазе.

**RemainingBlockers:** Реальная атомарная запись balances и history reconstruction пока отсутствуют.

## R1.3. Consumption Authorization

**RequiredApprovedContracts:** D-01,D-02,D-07,D-08; R1.2 balance schema.

**AllowedProductionFiles:** Include/Money/HSBI_ReserveAllocationTypes.mqh; Include/Money/HSBI_ReserveCatchUpEvaluator.mqh; новый Include/Money/HSBI_ConsumptionAuthorization.mqh. Имена новых файлов — предлагаемый allowlist после утверждения, не файлы, созданные R0A.

**ForbiddenChanges:** Не реализовывать broker dispatch, реальные сделки, durable backend или новую экономическую формулу.

**EntryGate:** R1.1/R1.2 приняты; purpose/amount/policy/current revision и authority completeness typed.

**ExitGate:** Foreign source/owner/plan/revision не дают eligibility; exact NO_OP и changed CONFLICT; unknown registry UNAVAILABLE; eligibility не мутирует баланс. Проверка должна выполняться на approved scope, без повышения full economic correctness.

**Tests:** D07-*; M01 foreign/replay/restart/spent; reserved40/41; stale proof; mutation удаления binding; актуальные R8/R10/R12/R12A плюс scoped negative/mutation tests. MetaEditor/MQL5 checks отдельно; отсутствие инструмента => NOT_RUN.

**RollbackProcedure:** остановить зависимые consumers; сохранить snapshots/journal read-only; при явном решении администратора отдельным git revert вернуть собственный атомарный phase commit. Не использовать reset/rebase/amend. Downgrade новой schema без отдельно проверенной обратной миграции запрещён; старый код не должен принимать неизвестную schema. Поскольку trading остаётся запрещённым, rollback не создаёт компенсирующих сделок.

**CommitBoundary:** один production+tests commit строго R1.3; не объединять с другими фазами. Отдельный review/diff/source-hash gate до перехода к следующей фазе.

**RemainingBlockers:** Durable CAS/concurrency/crash correctness UNPROVEN; unsupported provider всегда UNAVAILABLE.

## R1.4. Independent Money Proof Identity

**RequiredApprovedContracts:** D-02,D-04,D-06,D-08; R1.3; отдельное разрешение менять NewFar assembly.

**AllowedProductionFiles:** Include/Money/HSBI_MoneyProofIdentity.mqh; Include/Money/HSBI_ReserveCatchUpEvaluator.mqh; Include/Planning/HSBI_NewFarSolver.mqh — только assembly expected/source boundary. Имена новых файлов — предлагаемый allowlist после утверждения, не файлы, созданные R0A.

**ForbiddenChanges:** Не менять NewFar objective/tie-break/enumeration, geometry, WORST_CASE selector или risk formula.

**EntryGate:** Утверждён independent lookup interface; Reserve/Far proof branches и current context источники определены.

**ExitGate:** Self-copy удалена; expected из independent receipts; full source/digest validation; отсутствующий provider исключает candidate fail-closed. Проверка должна выполняться на approved scope, без повышения full economic correctness.

**Tests:** D08-self-copy-*; missing/stale history; foreign magic/cycle/position/deal/event/plan/revision/snapshot; digest/net/reused allocation; source mutation self-copy; актуальные R8/R10/R12/R12A плюс scoped negative/mutation tests. MetaEditor/MQL5 checks отдельно; отсутствие инструмента => NOT_RUN.

**RollbackProcedure:** остановить зависимые consumers; сохранить snapshots/journal read-only; при явном решении администратора отдельным git revert вернуть собственный атомарный phase commit. Не использовать reset/rebase/amend. Downgrade новой schema без отдельно проверенной обратной миграции запрещён; старый код не должен принимать неизвестную schema. Поскольку trading остаётся запрещённым, rollback не создаёт компенсирующих сделок.

**CommitBoundary:** один production+tests commit строго R1.4; не объединять с другими фазами. Отдельный review/diff/source-hash gate до перехода к следующей фазе.

**RemainingBlockers:** Полный broker-driven NewFar integration ещё NOT_RUN; zero-Core/WORST_CASE dependencies сохраняются.

## R1.5. MoneyState и recovery interface

**RequiredApprovedContracts:** D-01,D-02,D-07,D-08; R1.1–R1.4; explicit known revision semantics.

**AllowedProductionFiles:** Include/Money/HSBI_MoneyState.mqh; Include/Persistence/HSBI_PersistenceInterface.mqh — только typed interface; новый Include/Money/HSBI_MoneyAvailabilityTypes.mqh. Имена новых файлов — предлагаемый allowlist после утверждения, не файлы, созданные R0A.

**ForbiddenChanges:** Не выдавать in-memory backend за durable; не реализовывать торговые переходы или auto-resume.

**EntryGate:** Schema migration и unknown/zero revision outcomes утверждены; actual source types отделены от projected.

**ExitGate:** Finite values/current revision/availability typed; restart интерфейс требует complete restored authority и otherwise UNAVAILABLE; сохранён no-trade. Проверка должна выполняться на approved scope, без повышения full economic correctness.

**Tests:** FINITE-*; D07-missing-registry; D07-binding-revision; typed conversion tests; replay после in-memory state evolution отдельно от durable; актуальные R8/R10/R12/R12A плюс scoped negative/mutation tests. MetaEditor/MQL5 checks отдельно; отсутствие инструмента => NOT_RUN.

**RollbackProcedure:** остановить зависимые consumers; сохранить snapshots/journal read-only; при явном решении администратора отдельным git revert вернуть собственный атомарный phase commit. Не использовать reset/rebase/amend. Downgrade новой schema без отдельно проверенной обратной миграции запрещён; старый код не должен принимать неизвестную schema. Поскольку trading остаётся запрещённым, rollback не создаёт компенсирующих сделок.

**CommitBoundary:** один production+tests commit строго R1.5; не объединять с другими фазами. Отдельный review/diff/source-hash gate до перехода к следующей фазе.

**RemainingBlockers:** Durable IO и crash recovery не реализованы; R1 не даёт end-to-end exactly-once.

## F-PERSIST. Durable persistence / crash recovery

**RequiredApprovedContracts:** D-07,D-08 и approved storage protocol.

**AllowedProductionFiles:** Include/Persistence/* только в отдельном согласованном allowlist.

**ForbiddenChanges:** Не включать dispatch, не менять Money/Geometry без отдельного scope.

**EntryGate:** Утверждены schema/lock/CAS/marker/journal completeness и fault model.

**ExitGate:** Crash injection на каждой фазе сохраняет exactly-once и verified fallback; no auto-resume.

**Tests:** journal torn/temp/prepared/commit/ack, concurrent consumers, previous snapshot, history reconciliation.

**RollbackProcedure:** Остановить dependent scope; сохранить evidence; отдельный reviewed git revert без reset/rebase; schema rollback только по проверенной миграции, без compensating trades..

**CommitBoundary:** Отдельный atomic commit/review F-PERSIST; не включать в R1.1–R1.5..

**RemainingBlockers:** Broker execution correctness и trading approval остаются вне scope.


## F-CORE. Zero BigCore geometry

**RequiredApprovedContracts:** ZERO-CORE exact reject/normalization policy.

**AllowedProductionFiles:** Include/Planning/HSBI_GeometrySolver.mqh.

**ForbiddenChanges:** Не менять Small/NewFar economics/dispatch.

**EntryGate:** Отдельный geometry допуск; цена/volume grid исходные snapshots зафиксированы.

**ExitGate:** Core0 не accepted; все slope/grid/money/risk/margin последствия переоценены.

**Tests:** ZERO-raw-to-rounded/positive-control, min>step, plateau/rounding, source mutation zeroCore.

**RollbackProcedure:** Остановить dependent scope; сохранить evidence; отдельный reviewed git revert без reset/rebase; schema rollback только по проверенной миграции, без compensating trades..

**CommitBoundary:** Отдельный atomic commit/review F-CORE; не включать в R1.1–R1.5..

**RemainingBlockers:** Без broker calculation money consequence UNPROVEN.


## F-WORST. WORST_CASE selector

**RequiredApprovedContracts:** CR-09 variant/scope/tie/digest и D-01–08.

**AllowedProductionFiles:** Include/Planning/HSBI_FutureSmallProofAggregator.mqh + approved level DTO/digest files.

**ForbiddenChanges:** Не исключать негативные уровни, не менять geometry/dispatch.

**EntryGate:** RequiredLevels и источники available по пути независимо заданы.

**ExitGate:** A min margin covers all required; B SINGLE_LEVEL_ONLY; missing proof blocks guarantee.

**Tests:** CR09-*, all-level zero/negative/tie/stale/lot/source/currency/trajectory availability.

**RollbackProcedure:** Остановить dependent scope; сохранить evidence; отдельный reviewed git revert без reset/rebase; schema rollback только по проверенной миграции, без compensating trades..

**CommitBoundary:** Отдельный atomic commit/review F-WORST; не включать в R1.1–R1.5..

**RemainingBlockers:** All-level numeric proof не даёт broker reachability.


## F-MQL. MetaEditor/MQL5 runtime acceptance

**RequiredApprovedContracts:** Принятый test build/runtime plan без торговли.

**AllowedProductionFiles:** Production files read-only; разрешены новые test-only .mq5/harness/build outputs.

**ForbiddenChanges:** Не менять код автоматически ради компиляции; compiler errors требуют отдельного fix scope.

**EntryGate:** Доступны MetaEditor/MT5 и безопасный no-trade terminal.

**ExitGate:** Реальные compiler warnings/errors и assertions, counts/exit/logs сохранены.

**Tests:** Main+harness compile, MQL5 unit scripts, no broker dispatch.

**RollbackProcedure:** Остановить dependent scope; сохранить evidence; отдельный reviewed git revert без reset/rebase; schema rollback только по проверенной миграции, без compensating trades..

**CommitBoundary:** Отдельный atomic commit/review F-MQL; не включать в R1.1–R1.5..

**RemainingBlockers:** Strategy Tester/broker account behavior отдельно.


## F-BROKER. Broker money/margin verification

**RequiredApprovedContracts:** Approved target account/server/symbol/precision/cost policies.

**AllowedProductionFiles:** Broker Money/Margin исходники read-only; отдельный read-only provider adapter только по allowlist.

**ForbiddenChanges:** Никаких OrderSend/CTrade/реальных сделок.

**EntryGate:** Нужные credentials доступны через безопасную конфигурацию; symbol/account modes заданы.

**ExitGate:** OrderCalcProfit/OrderCalcMargin/history сравнения подтверждены на целевых свойствах.

**Tests:** BUY/Bid, SELL/Ask, asymmetric ticks, fees, swap, failed API, precision and history read.

**RollbackProcedure:** Остановить dependent scope; сохранить evidence; отдельный reviewed git revert без reset/rebase; schema rollback только по проверенной миграции, без compensating trades..

**CommitBoundary:** Отдельный atomic commit/review F-BROKER; не включать в R1.1–R1.5..

**RemainingBlockers:** Расчётные APIs не доказывают execution/fill/persistence.


## F-NEWFAR. Полный NewFar integration

**RequiredApprovedContracts:** R1.1–1.5 и отдельные F-PERSIST/F-CORE/F-WORST/F-MQL/F-BROKER evidence.

**AllowedProductionFiles:** Include/Planning/HSBI_NewFarSolver.mqh и утверждённые candidate integration files.

**ForbiddenChanges:** Не включать trading dispatch/auto-resume.

**EntryGate:** Все source/geometry/authority/market/risk/margin dependencies приняты отдельно.

**ExitGate:** Полный fail-closed source→candidate путь; неверный source исключается до tie-break.

**Tests:** unique Far, actual Core residual, owned history, stale/missing proofs, replay/restart/candidate list digest.

**RollbackProcedure:** Остановить dependent scope; сохранить evidence; отдельный reviewed git revert без reset/rebase; schema rollback только по проверенной миграции, без compensating trades..

**CommitBoundary:** Отдельный atomic commit/review F-NEWFAR; не включать в R1.1–R1.5..

**RemainingBlockers:** Торговый допуск остаётся отдельным административным решением.


## Межэтапные gates

[Лист утверждения](../Reports/NEXT_STAGE_02B_R0A_ADMIN_APPROVAL_SHEET_RU.md) и [кандидат контрактов](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md) задают решения, а не права исполнения. No-trade policy неизменна во всех фазах. Branch/remote parity и clean worktree перед каждым новым этапом обязательны. Ни один PASS не снимает `REAL_TRADING_ALLOWED=NO`.
