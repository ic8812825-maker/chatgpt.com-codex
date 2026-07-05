from pathlib import Path
text = Path('MinusLock_BigHarvest_EA_V2/Include/GeometryEngine.mqh').read_text()
main = Path('MinusLock_BigHarvest_EA_V2/MinusLock_BigHarvest_EA.mq5').read_text()
assert 'bool g_atrIndicatorAdded = false;' in text
assert 'int g_atrIndicatorSubwindow = -1;' in text
assert 'IsATRIndicatorAlreadyVisible' in text
assert 'ChartIndicatorsTotal' in text and 'ChartIndicatorName' in text
assert 'ATR_INDICATOR_ADD_REQUEST' in text
assert 'ATR_INDICATOR_ALREADY_VISIBLE' in text
assert 'ATR_INDICATOR_ADD_OK' in text and 'ATR_INDICATOR_ADD_FAIL' in text
assert text.count('ChartIndicatorAdd') == 1, 'ChartIndicatorAdd must have one call site'
assert 'if(g_atrIndicatorAdded || IsATRIndicatorAlreadyVisible())' in text
assert 'EnsureATRIndicatorOnChart();' in main
print('ATR_INDICATOR_SINGLE_INSTANCE_CHECK PASS')
