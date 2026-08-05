# Критерии production-готовности

Версия 1.0. Статус: нормативный.

Реальная торговля запрещена до одновременного PASS:

```text
NORMATIVE_DOCUMENTATION
MQL5_MAPPING
METAEDITOR_COMPILE
ON_TRADE_TRANSACTION
OWNERSHIP_GUARD
ECONOMIC_LEDGER
ALLOCATION_LEDGER
PERSISTENCE
RECONCILIATION
FINAL_CLOSE
PARTIAL_FAR
SMALL_TRANSITION
STRATEGY_TESTER
STRESS_TESTS
DEMO_FORWARD
REAL_LIMITED_APPROVAL=EXPLICIT
```

- `HSBI-PROD-001`: любой FAIL/UNPROVEN блокирует real.
- `HSBI-PROD-002`: compile без tester не означает readiness.
- `HSBI-PROD-003`: demo forward требует predefined limits и evidence.
- `HSBI-PROD-004`: limited real требует отдельного решения пользователя после demo.
- `HSBI-PROD-005`: emergency policy, broker/symbol whitelist и max exposure должны быть утверждены.
- `HSBI-PROD-006`: PASS не наследуется от старого проекта или Python.

Для каждого gate сохраняются owner, commit SHA, build hash, test data, timestamp и evidence links. Expired/stale evidence переводится UNPROVEN.

Контракт: вход — полный набор evidence. Выход — BLOCKED/DEMO_ALLOWED/REAL_LIMITED_ALLOWED. Preconditions: no open P0/P1. Postconditions: explicit signed status. Restart не применим; owner: Reports/ProductionReadiness. Тест: independent acceptance. Открытые вопросы: demo duration, risk limits, broker/symbol scope.