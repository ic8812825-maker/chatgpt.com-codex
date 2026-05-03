from pathlib import Path
from simple_random_test import run

def test_simple_random_synthetic_outputs():
    status, stats, report, log = run()
    assert status in ['PASS','MODIFY','FAIL']
    assert Path(report).exists()
    assert Path(log).exists()
    assert stats['open_sell'] >= 0
    assert stats['vol_block'] > 0
    assert stats['max_total'] <= 0.30 + 1e-9
