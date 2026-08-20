# Итоговый offline-verdict HSB.2D-V1-R7

R6 исторически заменён: его guard proof учитывал unauthorized NO_OP только после condition matching. R7 строит function-level terminal registry и блокирует unsafe outcomes независимо от normalizer; normalizer дополнительно поддерживает relational disjunction, subtraction-to-zero, negations и Boolean comparisons.

```text
BASELINE_SHA=45fa599bb0c446a8cc24bcdf79ec5f8999ef050e
R6_FALSE_PASS_REPRODUCED=YES
GLOBAL_TERMINAL_PATH_ANALYSIS=PASS
UNAUTHORIZED_NO_OP_GLOBAL_BLOCK=PASS
S037_NO_OP_EXACT_AUTHORIZATION=PASS
GUARD_EXECUTION_DOMINANCE=PASS
GUARD_OUTCOME_DOMINANCE=PASS
CONDITION_NORMALIZATION=PASS
SELF_TESTS=85/85
ADVERSARIAL=24/24
MUTATIONS_REQUIRED=185
MUTATIONS_EXECUTED=185
MUTATIONS_CAUGHT=185
MUTATIONS_SURVIVED=0
M166=CAUGHT
M166_M185=CAUGHT
PRODUCTION_MQL5_LOGIC_CHANGED=NO
REAL_TRADING_ALLOWED=NO
```
