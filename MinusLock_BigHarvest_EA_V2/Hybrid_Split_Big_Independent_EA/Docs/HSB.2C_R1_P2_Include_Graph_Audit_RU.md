# HSB.2C-R1-P2 — аудит include graph

Автоматически разобраны локальные `#include` для 69 headers и 110 рёбер.

```text
INCLUDE_CYCLES=0
DUPLICATE_INCLUDE_GUARDS=0
RUNTIME_POLICY_STRUCT_DEFINITIONS=1
RUNTIME_POLICY_BUILDER_DEFINITIONS=1
RUNTIME_MODE_COMPATIBILITY_HEADER=NO_POLICY_IMPLEMENTATION
MAIN_EA_CANONICAL_POLICY_INCLUDE=YES
TEST_HARNESS_CANONICAL_POLICY_REACHABLE=YES
```

`HSBI_RuntimeMode.mqh` зависит от canonical `HSBI_RuntimePolicy.mqh`; обратного include нет. Include guards уникальны.
