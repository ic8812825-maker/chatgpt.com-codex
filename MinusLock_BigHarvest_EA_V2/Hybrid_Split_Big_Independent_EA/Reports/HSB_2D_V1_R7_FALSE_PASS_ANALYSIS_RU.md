# Анализ ложного PASS R6

R6 классифицировал ранний `HSBI_DECISION_NO_OP` как `UNAUTHORIZED_NO_OP`, однако включал его в dominance только после сопоставления condition с конкретным guard. Поэтому `< || >`, логически эквивалентное `!=`, могло не попасть в `NO_OP_PATHS` и S028 ошибочно проходил. R7 сначала строит function-level registry всех terminal paths и блокирует каждый unsafe outcome независимо от нормализации condition.

```text
R6_FALSE_PASS_REPRODUCED=YES
HSB.2D_V1_R6_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
SUPERSEDED_REASON=UNAUTHORIZED_NO_OP_NOT_INCLUDED_IN_GLOBAL_DOMINANCE
```
