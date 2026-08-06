# CHANGELOG

## HSB.1

Создан независимый неторгующий MQL5-каркас: main EA shell, Core/Planning/Money/Execution/Scenarios/Persistence/Risk/Diagnostics interfaces, no-trade guard и MQL5 unit-test harness.

Static no-trade audit и include dependency audit: PASS. MetaEditor и MT5 недоступны, поэтому compile/tests честно отмечены NOT_RUN_ENVIRONMENT_UNAVAILABLE. Торговые сценарии и broker execution не реализованы.

HSB_STAGE_1_STATUS=READY_FOR_ACCEPTANCE; NEXT_ALLOWED_STAGE=NONE; REAL_TRADING_ALLOWED=NO.