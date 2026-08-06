# Include graph HSB.1

## Корневой граф

```text
Hybrid_Split_Big_Independent_EA.mq5
→ Core/Version, Enums, Types, ReasonCodes, RuntimeMode, Context, Invariants
→ Execution/NoTradeExecution
→ Diagnostics/Logger, Diagnostics
```

## Направления

```text
Core → только Core
Planning → Core
Money → Core types
Execution → Core, без broker API
Scenarios → Core contracts
Persistence → Core + Planning DTO + Execution DTO + Money DTO
Risk → Core reason types
Diagnostics → Core, read-only
Tests → все слои только для проверки
```

Проверено:

- циклические include не обнаружены;
- старые include не подключены;
- Legacy и Split runtime отсутствуют;
- `Trade/Trade.mqh` отсутствует;
- скрытый доступ к broker execution отсутствует;
- Diagnostics не меняет context/state;
- Money не зависит от Execution;
- Planning не меняет FSM;
- Core не зависит от Scenarios.

Статус:

```text
INCLUDE_GRAPH=PASS
FORBIDDEN_DEPENDENCIES=0
CYCLIC_INCLUDES=0
OLD_PROJECT_INCLUDES=0
TRADE_API_DEPENDENCIES=0
```