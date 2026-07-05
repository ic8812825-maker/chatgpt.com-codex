from pathlib import Path

root = Path(__file__).resolve().parents[1]
preset_dir = root / 'Sets' / 'Optimization_Presets'
main_atr_sets = {
    'Recommended.set',
    'Universal.set',
    'Minimum_Big_Levels.set',
    'Adaptive_ATR_SAFE.set',
    'Adaptive_ATR_BALANCED.set',
    'Adaptive_ATR_PROFIT.set',
    'Aggressive_Recovery.set',
    'Trend.set',
    'Anti_Trend.set',
    'Multi_Symbol.set',
    'Maximum_Recovery.set',
    'Low_Volatility.set',
    'High_Volatility.set',
}
conservative_sets = {'Conservative.set', 'Ultra_Conservative.set', 'ATR_Conservative.set'}

def read_value(path: Path, key: str) -> str:
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith(key + '='):
            return line.split('=', 1)[1].strip()
    raise AssertionError((path.name, key))

for name in main_atr_sets:
    path = preset_dir / name
    assert path.exists(), path
    assert read_value(path, 'ATRPeriod') == '14', (name, read_value(path, 'ATRPeriod'))
    assert read_value(path, 'ATRTimeframe') in {'0', 'PERIOD_CURRENT'}, (name, read_value(path, 'ATRTimeframe'))

for path in preset_dir.glob('*.set'):
    period = read_value(path, 'ATRPeriod')
    timeframe = read_value(path, 'ATRTimeframe')
    if period == '20':
        assert path.name in conservative_sets, f'ATRPeriod=20 is only allowed for conservative presets: {path.name}'
    if path.name not in conservative_sets:
        assert timeframe != '60', f'ATRTimeframe=60 is forbidden for primary presets: {path.name}'

for path in (root / 'Sets').glob('USDJPY_M30_*.set'):
    assert read_value(path, 'ATRPeriod') == '14', path.name
    assert read_value(path, 'ATRTimeframe') in {'0', 'PERIOD_CURRENT'}, path.name

print('ATR_SET_FILES_STANDARD_CHECK PASS')
