# AI Test Report — MinusLock BigHarvest

> Python-модель не заменяет MT5 Strategy Tester. Она показывает кандидатов и диагностирует математику.

## Scenario Results
- **BIG/BIG/BIG**: State=STATE_CLOSED_PROFIT, CycleFinalPL=4.80, Reserve=20.80, FinalFar=0.08, Reason=FinalCloseAllowed after Big-harvest
- **SMALL/SMALL/SMALL**: State=STATE_UNCLOSED_CYCLE, CycleFinalPL=-126.00, Reserve=0.00, FinalFar=0.63, Reason=STOP_MAX_LEVELS after Small-at-Far
- **REAL_REPORT_SEQUENCE**: State=STATE_UNCLOSED_CYCLE, CycleFinalPL=-9.20, Reserve=16.80, FinalFar=0.13, Reason=STOP_MAX_LEVELS after Small-at-Far
- **STRONG_BIG**: State=STATE_CLOSED_PROFIT, CycleFinalPL=4.80, Reserve=20.80, FinalFar=0.08, Reason=FinalCloseAllowed after Big-harvest
- **CHOPPY**: State=STATE_CLOSED_PROFIT, CycleFinalPL=12.20, Reserve=20.20, FinalFar=0.04, Reason=FinalCloseAllowed after Big-harvest
- **BAD_MARKET**: State=STATE_UNCLOSED_CYCLE, CycleFinalPL=-22.40, Reserve=13.60, FinalFar=0.18, Reason=STOP_MAX_LEVELS after Small-at-Far

## Observed MT5 Failure
- Sample observed state: STATE_UNCLOSED_CYCLE / STOP_MAX_LEVELS / Net=-63.69
- Parser validation: {'report_path': '/workspace/chatgpt.com-codex/work/MinusLock_SelfCompressing_BigSmall_v2/ai_tests/data/sample_mt5_report.csv', 'deals': 17, 'parsed_net_profit': -63.69, 'observed_mt5_net_profit': -63.69, 'observed_stop_reason': 'STOP_MAX_LEVELS', 'python_model_state': 'STATE_UNCLOSED_CYCLE', 'python_model_cycle_final_pl': -9.2, 'note': 'Exact MT5 match requires exported deal history with real spread/commission/swap. This compares state and failure mode first.'}

## Parameter Sweep
- Variants tested: 225
- Sweep top row: CF/RS=0.50/0.50, SmallRatio=0.35, CloseBig=0.30, MaxLevels=5, State=STATE_CLOSED_PROFIT, PL=22.0
- Selected MT5-confirmation candidate: CF/RS=0.50/0.50, SmallRatio=0.36, CloseBig=0.35, MaxLevels=5

## Math Diagnosis
- 90/10 fails when TotalReserve grows too slowly relative to FarRemainLoss after mixed Big-harvest and Small-at-Far transitions.
- Breaking level is scenario-dependent; inspect ai_cycle_math.csv rows where Scenario=STOP_MAX_LEVELS.
- Missing reserve is abs(CycleFinalPL) when state is STATE_UNCLOSED_CYCLE.
- Current 90/10 row: State=STATE_UNCLOSED_CYCLE, CycleFinalPL=-9.2, TotalReserve=16.8, FinalFarLot=0.13, Reason=STOP_MAX_LEVELS after Small-at-Far

## Recommendation
- Recommended BigRatio: 1.30 (unchanged candidate)
- Recommended SmallRatio: 0.36 (selected Python candidate for MT5 confirmation)
- Recommended CloseBigOnSmall: 0.35 (selected Python candidate for MT5 confirmation)
- Recommended CloseFarShare: 0.50 (selected Python candidate for MT5 confirmation)
- Recommended ReserveShare: 0.50 (selected Python candidate for MT5 confirmation)
- Recommended MaxHarvestLevels: 5 (selected Python candidate for MT5 confirmation)
- Recommended MaxReverseCycles: 10 pending MT5 confirmation

Финальное подтверждение обязательно через MT5 Strategy Tester.
