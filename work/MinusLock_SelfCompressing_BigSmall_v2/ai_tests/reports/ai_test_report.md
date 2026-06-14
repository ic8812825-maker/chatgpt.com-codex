# AI Test Report — MinusLock BigHarvest

> Python-модель не заменяет MT5 Strategy Tester. Она показывает кандидатов и диагностирует математику.

## Scenario Results
- **BIG/BIG/BIG**: State=STATE_CLOSED_PROFIT, CycleFinalPL=4.80, Reserve=20.80, FinalFar=0.08, Reason=FinalCloseAllowed after Big-harvest
- **SMALL/SMALL/SMALL**: State=STATE_UNCLOSED_CYCLE, CycleFinalPL=-128.00, Reserve=0.00, FinalFar=0.64, Reason=STOP_MAX_LEVELS after Small-at-Far
- **REAL_REPORT_SEQUENCE**: State=STATE_UNCLOSED_CYCLE, CycleFinalPL=-11.00, Reserve=17.00, FinalFar=0.14, Reason=STOP_MAX_LEVELS after Small-at-Far
- **STRONG_BIG**: State=STATE_CLOSED_PROFIT, CycleFinalPL=4.80, Reserve=20.80, FinalFar=0.08, Reason=FinalCloseAllowed after Big-harvest
- **CHOPPY**: State=STATE_CLOSED_PROFIT, CycleFinalPL=10.20, Reserve=20.20, FinalFar=0.05, Reason=FinalCloseAllowed after Big-harvest
- **BAD_MARKET**: State=STATE_UNCLOSED_CYCLE, CycleFinalPL=-24.40, Reserve=13.60, FinalFar=0.19, Reason=STOP_MAX_LEVELS after Small-at-Far

## Observed MT5 Failure
- Sample observed state: STATE_UNCLOSED_CYCLE / STOP_MAX_LEVELS / Net=-63.69
- Parser validation: {'report_path': '/workspace/chatgpt.com-codex/work/MinusLock_SelfCompressing_BigSmall_v2/ai_tests/data/sample_mt5_report.csv', 'deals': 17, 'parsed_net_profit': -63.69, 'observed_mt5_net_profit': -63.69, 'observed_stop_reason': 'STOP_MAX_LEVELS', 'python_model_state': 'STATE_UNCLOSED_CYCLE', 'python_model_cycle_final_pl': -11.0, 'note': 'Exact MT5 match requires exported deal history with real spread/commission/swap. This compares state and failure mode first.'}

## Parameter Sweep
- Variants tested: 225
- Best Python candidate: CF/RS=0.50/0.50, SmallRatio=0.36, CloseBig=0.35, MaxLevels=5, State=STATE_CLOSED_PROFIT, PL=21.5

## Math Diagnosis
- 90/10 fails when TotalReserve grows too slowly relative to FarRemainLoss after mixed Big-harvest and Small-at-Far transitions.
- Breaking level is scenario-dependent; inspect ai_cycle_math.csv rows where Scenario=STOP_MAX_LEVELS.
- Missing reserve is abs(CycleFinalPL) when state is STATE_UNCLOSED_CYCLE.
- Current 90/10 row: State=STATE_UNCLOSED_CYCLE, CycleFinalPL=-11.0, TotalReserve=17.0, FinalFarLot=0.14, Reason=STOP_MAX_LEVELS after Small-at-Far

## Recommendation
- Recommended BigRatio: 1.30 (unchanged candidate)
- Recommended SmallRatio: 0.36 (Python candidate)
- Recommended CloseBigOnSmall: 0.35 (Python candidate)
- Recommended CloseFarShare: 0.50 (Python candidate)
- Recommended ReserveShare: 0.50 (Python candidate)
- Recommended MaxHarvestLevels: 5 (Python candidate)
- Recommended MaxReverseCycles: 10 pending MT5 confirmation

Финальное подтверждение обязательно через MT5 Strategy Tester.
