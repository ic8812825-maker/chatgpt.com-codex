# Canonical Runtime Policy HSB.2C-R1-P2

Единственная структура и builder находятся в `Include/Core/HSBI_RuntimePolicy.mqh`. `HSBI_RuntimeMode.mqh` — compatibility facade без реализации policy.

Матрица: UNSPECIFIED/DISABLED и legacy SHADOW_REAL/REAL_LIMITED fail-closed; UNIT_TEST допускает injected fixture, но не production preflight/completion; dry-run допускает расчёт; SHADOW допускает расчёт и static preflight без completion; PRODUCTION/ADMIN допускают terminal source после reconciliation; dispatch во всех режимах запрещён.

```text
STRUCT_DEFINITIONS=1
BUILDER_DEFINITIONS=1
BROKER_DISPATCH_ALLOWED=NO
```
