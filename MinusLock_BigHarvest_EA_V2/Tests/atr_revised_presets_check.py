from pathlib import Path
base = Path('MinusLock_BigHarvest_EA_V2/Sets/Optimization_Presets')
expected = {
    'Adaptive_ATR_SAFE.set': {'GeometryMode':'1','ATRPeriod':'14','ATRTimeframe':'0','ATRInitialMultiplier':'0.90','ATRBigStartMultiplier':'0.90','ATRStepMultiplier':'0.34','ATRFarMultiplier':'1.10','MaxInitialTriggerPoints':'220','MaxBigMoveStartPoints':'220','MaxBigMoveStepPoints':'90','MaxFarDistancePoints':'300'},
    'Adaptive_ATR_BALANCED.set': {'GeometryMode':'2','ATRPeriod':'14','ATRTimeframe':'0','ATRInitialMultiplier':'0.82','ATRBigStartMultiplier':'0.82','ATRStepMultiplier':'0.30','ATRFarMultiplier':'1.00','MaxInitialTriggerPoints':'210','MaxBigMoveStartPoints':'210','MaxBigMoveStepPoints':'85','MaxFarDistancePoints':'275'},
    'Adaptive_ATR_PROFIT.set': {'GeometryMode':'3','ATRPeriod':'14','ATRTimeframe':'0','ATRInitialMultiplier':'0.72','ATRBigStartMultiplier':'0.72','ATRStepMultiplier':'0.26','ATRFarMultiplier':'0.90','MaxInitialTriggerPoints':'200','MaxBigMoveStartPoints':'200','MaxBigMoveStepPoints':'80','MaxFarDistancePoints':'250'},
    'ATR_Conservative.set': {'GeometryMode':'1','ATRPeriod':'20','ATRTimeframe':'0','ATRInitialMultiplier':'0.98','ATRBigStartMultiplier':'0.98','ATRStepMultiplier':'0.40','ATRFarMultiplier':'1.25'},
    'Recommended.set': {'GeometryMode':'2','ATRPeriod':'14','ATRTimeframe':'0'},
    'Minimum_Big_Levels.set': {'GeometryMode':'3','ATRPeriod':'14','ATRTimeframe':'0'},
}
for name, checks in expected.items():
    data = dict(line.split('=',1) for line in (base/name).read_text().splitlines() if '=' in line)
    for key, val in checks.items():
        assert data.get(key) == val, f'{name}: {key}={data.get(key)} expected {val}'
    assert data.get('TerminalStateLogIntervalSeconds') == '300'
print('ATR_REVISED_PRESETS_CHECK PASS')
