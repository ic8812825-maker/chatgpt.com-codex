# R6 false-PASS analysis

R5 глобально считал `NO_OP+OK` безопасным и не нормализовал `!(a==b)` в `a!=b`. R6 считает NO_OP неразрешённым на prior paths и разрешает его только как целевой outcome S037 в `HSBI_ValidateRestartedRuntimeState` при `s.duplicateConsumption`. Guard proof сравнивает все эквивалентные matching paths и требует единственный нормативный status/reason.
