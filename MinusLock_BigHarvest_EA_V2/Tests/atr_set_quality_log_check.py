from pathlib import Path
text = (Path(__file__).resolve().parents[1] / 'Include' / 'GeometryEngine.mqh').read_text(encoding='utf-8')
for token in [
    'ATR_SET_QUALITY',
    'InitialClampUsed=',
    'BigStartClampUsed=',
    'StepClampUsed=',
    'FarClampUsed=',
    'AnyClampUsed=',
    'GeometryTooWide=',
    'GeometryTooTight=',
    'WARNING_ATR_GEOMETRY_WIDE',
    'WARNING_ATR_GEOMETRY_TOO_TIGHT',
    'Ctx.workInitialTriggerPoints >= 220',
    'Ctx.workBigMoveStartPoints >= 220',
    'Ctx.workBigMoveStepPoints >= 90',
    'Ctx.workFarDistancePoints >= 300',
    'Ctx.workInitialTriggerPoints <= 120',
    'Ctx.workBigMoveStartPoints <= 120',
    'Ctx.workBigMoveStepPoints <= 45',
    'Ctx.workFarDistancePoints <= 180',
]:
    assert token in text, token
print('ATR_SET_QUALITY_LOG_CHECK PASS')
