from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from minuslock_model import BIG, SMALL, ModelConfig, floor_lot, round_lot_nearest, simulate_sequence, validate_reverse_geometry


def test_big_small_lot_geometry():
    cfg = ModelConfig()
    big = round_lot_nearest(1.00 * cfg.big_ratio, cfg.lot_step)
    small = round_lot_nearest(big * cfg.small_ratio, cfg.lot_step)
    assert big == 1.30
    assert small == 0.48


def test_big_harvest_money_budget_and_reserve():
    cfg = ModelConfig(max_harvest_levels=3)
    result = simulate_sequence(cfg, [BIG, BIG, BIG])
    first = result.rows[0]
    assert first.ProfitBig == 130.0
    assert first.LossSmall == 48.0
    assert first.NetProfit == 82.0
    assert first.CloseFarBudget == 73.8
    assert first.ReserveAdd == 8.2
    assert first.CloseFarLotRounded == 0.36
    assert result.initial_ignored_profit == 100.0
    assert first.TotalReserveBefore == 0.0


def test_close_far_lot_rounds_down():
    assert floor_lot(0.369, 0.01) == 0.36
    assert floor_lot(0.351, 0.01) == 0.35


def test_reverse_geometry_new_far_shrinks():
    cfg = ModelConfig()
    old_far = 1.00
    big = round_lot_nearest(old_far * cfg.big_ratio)
    close_big = floor_lot(big * cfg.close_big_on_small)
    new_far = floor_lot(big - close_big)
    new_big = round_lot_nearest(new_far * cfg.big_ratio)
    new_small = round_lot_nearest(new_big * cfg.small_ratio)
    valid, reason, strength = validate_reverse_geometry(cfg, old_far, new_far, new_big, new_small)
    assert valid, reason
    assert new_far < old_far
    assert new_big > new_far
    assert strength >= cfg.min_reverse_strength


def test_final_close_allowed_and_closed_profit():
    cfg = ModelConfig(max_harvest_levels=3)
    result = simulate_sequence(cfg, [BIG, BIG, BIG])
    assert result.state == "STATE_CLOSED_PROFIT"
    assert result.rows[-1].FinalCloseAllowed


def test_stop_max_levels_works():
    cfg = ModelConfig(max_harvest_levels=1)
    result = simulate_sequence(cfg, [BIG, BIG, BIG])
    assert result.state == "STATE_UNCLOSED_CYCLE"
    assert "STOP_MAX_LEVELS" in result.reason


def test_initial_profit_never_enters_reserve():
    cfg = ModelConfig()
    result = simulate_sequence(cfg, [BIG])
    assert result.initial_ignored_profit == 100.0
    assert result.rows[0].TotalReserveBefore == 0.0
    assert result.rows[0].TotalReserveAfter == result.rows[0].ReserveAdd


def test_small_at_far_flow_records_rows():
    cfg = ModelConfig(max_harvest_levels=5)
    result = simulate_sequence(cfg, [SMALL, SMALL, SMALL, SMALL, SMALL])
    assert result.rows
    assert result.rows[0].Scenario == SMALL
    assert result.rows[0].FarRemainLot < result.rows[0].FarLotBefore
