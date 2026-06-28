from pathlib import Path
root = Path(__file__).resolve().parents[1]
config = (root / 'Include' / 'Config.mqh').read_text()
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
logger = (root / 'Include' / 'Logger.mqh').read_text()
main = (root / 'MinusLock_BigHarvest_EA.mq5').read_text()
for token in ['input int InitialRoundStep = 10', 'input int BigStartRoundStep = 10', 'input int BigStepRoundStep = 5', 'input int FarDistanceRoundStep = 50']:
    assert token in config, token
for token in ['RoundToStep(atrPoints * initialMult, InitialRoundStep)', 'RoundToStep(atrPoints * bigStartMult, BigStartRoundStep)', 'RoundToStep(atrPoints * stepMult, BigStepRoundStep)', 'RoundToStep(atrPoints * farMult, FarDistanceRoundStep)']:
    assert token in geom, token
assert 'RoundToStep(atrPoints * farMult, GeometryRoundStep)' not in geom
for token in ['InitialRoundStep=', 'BigStartRoundStep=', 'BigStepRoundStep=', 'FarDistanceRoundStep=']:
    assert token in geom, token
    assert token[:-1] in logger, token
for token in ['InitialRoundStep < 1', 'BigStartRoundStep < 1', 'BigStepRoundStep < 1', 'FarDistanceRoundStep < 1']:
    assert token in main, token
print('ADAPTIVE_GEOMETRY_ROUND_STEPS_CHECK PASS')
