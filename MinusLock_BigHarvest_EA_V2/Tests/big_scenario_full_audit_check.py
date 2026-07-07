from pathlib import Path
root = Path(__file__).resolve().parents[1]
audit = root / 'Docs' / 'BIG_SCENARIO_FULL_AUDIT.md'
text = audit.read_text(encoding='utf-8')
required = [
    'Full Big-scenario map', 'Function/file table', 'BigScenarioNet = ClosedBigNet + ClosedSmallNet',
    'CloseFarBudget = BigScenarioNet × CloseFarShare', 'ReserveAdd = BigScenarioNet × ReserveShare',
    'Reserve is not used for partial Far close', 'Файл: `Include/StateMachine.mqh`',
    'Файл: `Include/RecoveryMath.mqh`', '```mql5', 'ProcessBigHarvestCalcNet',
    'ProcessBigHarvestCloseFar', 'ProcessBigHarvestCheckFinal', 'NormalizeLotDown',
    'BigRatio² × RemainBigOnSmall', 'Final verdict'
]
for token in required:
    assert token in text, token
for path in [
    'MinusLock_BigHarvest_EA.mq5', 'Include/TradeEngine.mqh', 'Include/PositionUtils.mqh',
    'Include/LotUtils.mqh', 'Include/GeometryEngine.mqh', 'Include/RiskManager.mqh',
    'Include/Logger.mqh', 'Include/Types.mqh', 'Include/Config.mqh',
    'Tools/optimize_big_scenario_min_levels.py'
]:
    assert path in text, path
print('BIG_SCENARIO_FULL_AUDIT_CHECK PASS')
