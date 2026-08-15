# HSB.2C-R1-P1: runtime policy

| Режим | Расчёт | injected | static preflight | terminal completion | dispatch |
|---|---:|---:|---:|---:|---:|
| UNSPECIFIED | нет | нет | нет | нет | нет |
| DISABLED | нет | нет | нет | нет | нет |
| UNIT_TEST | да | только harness | нет | нет | нет |
| STRATEGY_TESTER_DRY_RUN | да | нет | нет | нет | нет |
| SHADOW | да | нет | да | нет | нет |
| PRODUCTION | да | нет | да | только полная reconciliation | нет |
| ADMIN_VERIFICATION | да | нет | да | только terminal source | нет |

`runtimeConfirmed=true` самостоятельно не подтверждает источник. Legacy real modes fail-closed. Context/FSM/ledger не изменяются. `HSB.2C_R1_PRODUCTION_DISPATCH=DISABLED`, `HSB.2C_R1_PRODUCTION_TRADING=FORBIDDEN`, `HSB.2C_R1_PRODUCTION_STATIC_PREFLIGHT=ALLOWED`.
