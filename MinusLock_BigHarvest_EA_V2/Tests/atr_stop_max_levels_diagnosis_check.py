from pathlib import Path
text = Path('MinusLock_BigHarvest_EA_V2/Include/StateMachine.mqh').read_text()
for token in ['STOP_MAX_LEVELS_DIAGNOSIS', 'MaxHarvestLevels=', 'ActualHarvestLevel=', 'LastFarLot=', 'LastBigLot=', 'LastSmallLot=', 'TotalReserve=', 'RecoveryPL=', 'ReserveCoverage=', 'LastATRPoints=', 'LastWorkInitial=', 'LastWorkBigStart=', 'LastWorkBigStep=', 'LastWorkFar=', 'LikelyReason=']:
    assert token in text
for reason in ['GEOMETRY_TOO_WIDE_OR_RESERVE_TOO_LOW', 'MAX_LEVELS_TOO_LOW', 'BIG_LOT_COMPRESSION_TOO_FAST']:
    assert reason in text
assert text.count('LogStopMaxLevelsDiagnosis') >= 3
print('ATR_STOP_MAX_LEVELS_DIAGNOSIS_CHECK PASS')
