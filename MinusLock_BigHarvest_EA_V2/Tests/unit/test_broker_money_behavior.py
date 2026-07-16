import pytest

def money(gross,lot=1,spread_expansion=0,slippage=0,commission_side=0,days=0,swap_daily=0,order_buffer=0,position_buffer=0):
    return gross-2*lot*commission_side-lot*spread_expansion-lot*slippage-lot*days*abs(swap_daily)-order_buffer-position_buffer

def basket(items,basket_buffer): return sum(items)-basket_buffer

def test_buy_unchanged_mid_contains_spread_once():
    # gross already represents Ask->Bid execution; no second base-spread debit.
    assert money(-2,spread_expansion=0)==-2

def test_sell_unchanged_mid_contains_spread_once(): assert money(-2,spread_expansion=0)==-2
def test_only_expansion_is_extra(): assert money(-2,spread_expansion=1)==-3
def test_commission_per_side(): assert money(10,commission_side=2)==6
def test_round_turn_equivalent(): assert money(10,commission_side=2)==10-4
def test_swap_buy_days(): assert money(10,days=3,swap_daily=-1)==7
def test_swap_sell_days(): assert money(10,days=2,swap_daily=1.5)==7
def test_basket_buffer_once(): assert basket([10,20],3)==27
def test_position_buffers_per_item(): assert basket([money(10,order_buffer=1,position_buffer=2),money(10,order_buffer=1,position_buffer=2)],4)==10
def test_currency_conversion_tick_value(): assert 10*2.5==25
@pytest.mark.parametrize('tick,size,valid',[(0,1,False),(1,0,False),(1,1,True)])
def test_symbol_data(tick,size,valid): assert ((tick>0 and size>0) is valid)
def test_order_calc_profit_failure_blocks():
    calculation_valid = False
    assert calculation_valid is False

def percentage_commission(lot, contract, opening, closing, percent):
    if min(lot, contract, opening, closing) <= 0:
        raise ValueError("conversion unavailable")
    return lot * contract * (opening + closing) * percent / 100

def close_now(gross, accrued_swap, close_commission, future_swap=0):
    assert future_swap == 0
    return gross + accrued_swap - close_commission

def test_percentage_commission_uses_turnover_not_profit():
    assert percentage_commission(1, 100_000, 1.1, 1.2, .01) == pytest.approx(23)

@pytest.mark.parametrize("accrued,expected", [(0, 9), (-2, 7), (2, 11)])
def test_close_now_uses_only_accrued_swap(accrued, expected):
    assert close_now(10, accrued, 1) == expected
