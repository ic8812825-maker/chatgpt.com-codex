from real_market_backtest import fetch

def test_h1_uses_500d_window_data_presence():
    df = fetch('EURUSD','H1')
    assert len(df) > 1000
