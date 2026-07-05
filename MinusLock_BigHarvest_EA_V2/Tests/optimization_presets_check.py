from pathlib import Path
root = Path(__file__).resolve().parents[1]
preset_dir = root / 'Sets' / 'Optimization_Presets'
required = [
    'Ultra_Conservative.set', 'Conservative.set', 'ATR_Conservative.set', 'Universal.set', 'Aggressive_Recovery.set',
    'High_Volatility.set', 'Low_Volatility.set', 'Trend.set', 'Anti_Trend.set',
    'Adaptive_ATR_SAFE.set', 'Adaptive_ATR_BALANCED.set', 'Adaptive_ATR_PROFIT.set',
    'Multi_Symbol.set', 'Maximum_Recovery.set', 'Minimum_Big_Levels.set', 'Recommended.set',
]
for name in required:
    path = preset_dir / name
    assert path.exists(), path
    text = path.read_text()
    for key in ['StartLot=', 'BigRatio=', 'SmallRatio=', 'CloseFarShare=', 'ReserveShare=', 'GeometryMode=', 'ATRPeriod=', 'MaxHarvestLevels=', 'MaxReverseCycles=', 'MaxAccountMarginPercent=', 'MagicNumber=']:
        assert key in text, (name, key)
recommended = (preset_dir / 'Recommended.set').read_text()
assert 'GeometryMode=2' in recommended
assert 'BigRatio=1.14' in recommended
assert 'CloseFarShare=0.75' in recommended
minimum = (preset_dir / 'Minimum_Big_Levels.set').read_text()
assert 'CloseFarShare=0.9' in minimum or 'CloseFarShare=0.90' in minimum
assert 'BigRatio=1.15' in minimum
print('OPTIMIZATION_PRESETS_CHECK PASS')
