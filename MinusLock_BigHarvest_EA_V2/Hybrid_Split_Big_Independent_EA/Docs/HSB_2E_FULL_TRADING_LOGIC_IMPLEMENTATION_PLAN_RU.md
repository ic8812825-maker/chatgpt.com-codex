# HSB.2E — полный план будущей торговой реализации

> Статус: `READY_FOR_ADMIN_REVIEW`. Реализация и broker dispatch не начаты.

## 1–7. Цель, граница, baseline, файлы и зависимости

Цель — simulation-first реализация полного цикла после административной приёмки R5 и HSB.2D-V2. Baseline будет отдельно утверждён. Разрешаются только заранее назначенные файлы из file map; торговая математика, нормативные контракты и исторические evidence не переписываются. Новые production-файлы создаются лишь в соответствующем 2E-подэтапе. Направление: Core → Planning/Money/Risk → Scenario decisions → Execution intent → Persistence journal → Simulated adapter → Reconciliation → FSM commit.

## 8. Sequence diagram полного цикла

Initial Lock → подтверждение двух позиций → закрытие положительной (прибыль игнорируется) → отрицательная становится Far → geometry Big/Small → позиции → Big level → Big/Small close 100% → deals confirmed → net realized → Final Close или Partial Far без Reserve → allocation/Reserve → Small Transition → old Small/Far close → partial Big → residual Big=new Far (new<old) → повтор → Final Close → reconciliation → persisted completed cycle.

## 9–17. Платформенные контуры

FSM изменяется только после persisted external outcome и reconciliation. Persistence — append-only intent/outcome/commit с action id. Broker-money использует runtime properties и conservative conversion. Discovery фильтрует account/symbol/magic/cycle, Far — identifier+ticket. Ownership fail-closed. Transaction engine имеет intent, dispatch, acknowledgement, fills, reconciliation, commit. Сначала доступен только simulated adapter; demo и real-limited отсутствуют до отдельных gates.

## 18–26. Сценарии

Initial Lock, Big Harvest, Partial Far, Reserve, Final Close, Small Transition, NewFar promotion, Future Small и Catch-Up реализуются отдельными decision engines без прямых broker calls. Partial Far не использует Reserve; Reserve разрешён только Final Close. Allocation выполняется после подтверждённых deals.

## 27–40. Надёжность и приёмка

Risk gates выполняются до intent. Restart восстанавливает persisted barrier. Partial fill не освобождает barrier. Retry сохраняет ActionId. Timeout и unknown outcome требуют reconciliation. Duplicate/out-of-order events идемпотентны. Critical unresolved error переводит terminal-safe без auto-resume. Логи содержат requirement/action/event/digest. Acceptance включает unit, integration, adversarial, Strategy Tester, stress и demo-forward; реальные сделки запрещены.

## Неприкосновенные invariants

```text
MULTI_CURRENCY_PRESERVED=YES
FILTER_BY_ACCOUNT_SYMBOL_MAGIC_CYCLE=YES
FAR_OPERATIONS_BY_IDENTIFIER_AND_TICKET=YES
INITIAL_POSITIVE_PROFIT_IGNORED=YES
BIG_CLOSE_AT_LEVEL=100_PERCENT
SMALL_CLOSE_AT_BIG_LEVEL=100_PERCENT
PARTIAL_FAR_USES_RESERVE=NO
RESERVE_USED_FOR_FINAL_CLOSE_ONLY=YES
RESERVE_SHARE_PLUS_CLOSE_FAR_SHARE=1
FINAL_CLOSE_REQUIRES_RECOVERY_PL_POSITIVE=YES
REAL_CLOSE_DEALS_REQUIRED_BEFORE_ALLOCATION=YES
COMMISSION_SWAP_FEE_SPREAD_SLIPPAGE_INCLUDED=YES
NEW_FAR_LESS_THAN_OLD_FAR=YES
DUAL_TAIL_ALLOWED=NO
NEW_LEVEL_BEFORE_TRANSITION_RESOLVED=NO
ONLY_COMPLETED_FILL_RELEASES_BARRIER=YES
RETRY_REUSES_ACTION_ID=YES
UNKNOWN_OUTCOME_RECONCILIATION_REQUIRED=YES
UNRESOLVED_CRITICAL_ERROR_TERMINAL_SAFE=YES
AUTO_RESUME_AFTER_TERMINAL_SAFE=NO
REAL_TRADING_ALLOWED=NO
```

## Поэтапный backlog и commit gates

### HSB.2E.0 — baseline и pre-implementation audit

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.0 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.0.

### HSB.2E.1 — production persistence

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.1 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.1.

### HSB.2E.2 — broker snapshot и broker-money runtime

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.2 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.2.

### HSB.2E.3 — position/deal discovery и ownership

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.3 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.3.

### HSB.2E.4 — reconciliation engine

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.4 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.4.

### HSB.2E.5 — transaction intent и simulated dispatch

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.5 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.5.

### HSB.2E.6 — Initial Lock

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.6 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.6.

### HSB.2E.7 — Big Harvest

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.7 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.7.

### HSB.2E.8 — Partial Far и Reserve allocation

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.8 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.8.

### HSB.2E.9 — Final Close

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.9 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.9.

### HSB.2E.10 — Small Transition

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.10 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.10.

### HSB.2E.11 — NewFar promotion и Catch-Up

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.11 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.11.

### HSB.2E.12 — restart/exactly-once

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.12 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.12.

### HSB.2E.13 — demo-only broker dispatch

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.13 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.13.

### HSB.2E.14 — Strategy Tester и stress matrix

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.14 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.14.

### HSB.2E.15 — demo forward

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.15 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.15.

### HSB.2E.16 — production readiness review

- **INPUTS:** accepted previous gate and immutable contracts.
- **OUTPUTS:** stage-specific code, tests and sealed evidence.
- **FILES:** only entries assigned to 2E.16 in production file map.
- **FUNCTIONS:** public API declared by the owner component.
- **INVARIANTS:** all global invariants plus stage contracts.
- **FAIL_CLOSED_RULES:** unknown broker/state/money outcome blocks commit.
- **TESTS:** reserved range from HSB.2E test plan.
- **EVIDENCE:** compile, deterministic tests, logs, manifest.
- **COMMIT_BOUNDARY:** one auditable implementation unit.
- **ROLLBACK_RULE:** no state rollback; disable new path and reconcile.
- **NEXT_GATE:** explicit admin acceptance of 2E.16.
