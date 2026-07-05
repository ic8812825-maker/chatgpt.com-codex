from pathlib import Path
text = (Path(__file__).resolve().parents[1] / 'Include' / 'GeometryEngine.mqh').read_text(encoding='utf-8')
for token in [
    'ATR_SET_QUALITY',
    'InitialClampUsed=',
    'BigStartClampUsed=',
    'StepClampUsed=',
    'FarClampUsed=',
    'GeometryTooWide=',
    'WARNING_ATR_GEOMETRY_TOO_WIDE',
    'Ctx.workInitialTriggerPoints >= 240',
    'Ctx.workBigMoveStartPoints >= 250',
    'Ctx.workBigMoveStepPoints >= 110',
    'Ctx.workFarDistancePoints >= 350',
]:
    assert token in text, token
print('ATR_SET_QUALITY_LOG_CHECK PASS')
