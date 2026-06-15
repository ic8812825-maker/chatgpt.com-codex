from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from minuslock_model import BIG, SMALL, FIXED_200, INITIAL_PLUS_CURRENT, INITIAL_PLUS_CUMULATIVE, ModelConfig, floor_lot, round_lot_nearest, simulate_sequence, validate_reverse_geometry


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


def test_recommended_5050_preset_closes_profit():
    from market_replay import SCENARIOS
    from minuslock_model import recommended_5050_config
    result = simulate_sequence(recommended_5050_config(), SCENARIOS["REAL_REPORT_SEQUENCE"])
    assert result.state == "STATE_CLOSED_PROFIT"
    assert result.cycle_final_pl > 0


def test_9010_real_report_sequence_records_initial_distance():
    from market_replay import SCENARIOS
    cfg = ModelConfig(max_harvest_levels=5, max_reverse_cycles=10)
    result = simulate_sequence(cfg, SCENARIOS["REAL_REPORT_SEQUENCE"])
    assert result.rows[0].EffectiveFarDistancePoints == 200
    assert result.rows[0].InitialFarDistancePoints == 100


def test_5050_reverse_geometry_valid():
    from minuslock_model import recommended_5050_config
    cfg = recommended_5050_config()
    old_far = 1.00
    big = round_lot_nearest(old_far * cfg.big_ratio, cfg.lot_step)
    small = round_lot_nearest(big * cfg.small_ratio, cfg.lot_step)
    close_big = round_lot_nearest(big * cfg.close_big_on_small, cfg.lot_step)
    new_far = floor_lot(big - close_big, cfg.lot_step)
    new_big = round_lot_nearest(new_far * cfg.big_ratio, cfg.lot_step)
    new_small = round_lot_nearest(new_big * cfg.small_ratio, cfg.lot_step)
    valid, reason, strength = validate_reverse_geometry(cfg, old_far, new_far, new_big, new_small)
    assert (big, small, close_big, new_far, new_big, new_small) == (1.30, 0.47, 0.46, 0.84, 1.09, 0.39)
    assert valid, reason
    assert new_far < old_far
    assert new_big > new_far
    assert new_small < new_big
    assert strength > cfg.strong_reverse_strength


def test_5050_small_at_far_not_broken():
    from minuslock_model import recommended_5050_config
    cfg = recommended_5050_config()
    result = simulate_sequence(cfg, [SMALL, SMALL, SMALL])
    first = result.rows[0]
    assert first.State in {"STATE_SMALL_SCENARIO", "STATE_CLOSED_PROFIT"}
    assert first.FarRemainLot < first.FarLotBefore
    assert first.ReverseStrength >= cfg.min_reverse_strength
    assert first.NetProfit > 0


def test_5050_final_close_allowed():
    from market_replay import SCENARIOS
    from minuslock_model import recommended_5050_config
    result = simulate_sequence(recommended_5050_config(), SCENARIOS["REAL_REPORT_SEQUENCE"])
    assert result.rows[-1].FinalCloseAllowed
    assert result.state == "STATE_CLOSED_PROFIT"


def test_initial_100_points_are_counted():
    cfg = ModelConfig(far_distance_mode=INITIAL_PLUS_CURRENT)
    result = simulate_sequence(cfg, [BIG])
    assert result.rows[0].InitialFarDistancePoints == 100
    assert result.rows[0].CurrentBigMovePoints == 100
    assert result.rows[0].EffectiveFarDistancePoints == 200


def test_level1_effective_far_distance_200():
    cfg = ModelConfig(far_distance_mode=INITIAL_PLUS_CURRENT)
    first = simulate_sequence(cfg, [BIG]).rows[0]
    assert first.BigLot == 1.30
    assert first.SmallLot == 0.48
    assert first.NetProfit == 82.0
    assert first.CloseFarBudget == 73.8
    assert round(first.CloseFarLotRaw, 3) == 0.369
    assert first.CloseFarLotRounded == 0.36
    assert first.FarRemainLot == 0.64
    assert first.FarRemainLoss == 128.0
    assert not first.FinalCloseAllowed


def test_fixed_200_matches_old_model():
    cfg = ModelConfig(far_distance_mode=FIXED_200)
    first = simulate_sequence(cfg, [BIG]).rows[0]
    assert first.EffectiveFarDistancePoints == 200
    assert first.CloseFarLotRounded == 0.36


def test_initial_plus_current_mode():
    cfg = ModelConfig(far_distance_mode=INITIAL_PLUS_CURRENT)
    result = simulate_sequence(cfg, [BIG, BIG, BIG])
    distances = [row.EffectiveFarDistancePoints for row in result.rows if row.Scenario == BIG]
    assert distances[:3] == [200, 250, 300]


def test_initial_plus_cumulative_mode():
    cfg = ModelConfig(far_distance_mode=INITIAL_PLUS_CUMULATIVE, max_harvest_levels=5)
    result = simulate_sequence(cfg, [BIG, BIG, BIG])
    distances = [row.EffectiveFarDistancePoints for row in result.rows if row.Scenario == BIG]
    assert distances[:3] == [200, 350, 550]


def test_small_at_far_resets_far_distance():
    cfg = ModelConfig(far_distance_mode=INITIAL_PLUS_CUMULATIVE, max_harvest_levels=5)
    result = simulate_sequence(cfg, [BIG, SMALL, BIG])
    small_row = next(row for row in result.rows if row.Scenario == SMALL)
    assert small_row.EffectiveFarDistancePoints == 0
    assert small_row.FarRemainLoss == 0
    if len(result.rows) > 2:
        next_big = result.rows[2]
        assert next_big.InitialFarDistancePoints == 0


def test_cycle_math_contains_effective_far_distance():
    cfg = ModelConfig(far_distance_mode=INITIAL_PLUS_CURRENT)
    row = simulate_sequence(cfg, [BIG]).rows[0].to_dict()
    for key in [
        "InitialFarDistancePoints",
        "CurrentBigMovePoints",
        "CumulativeBigMovePoints",
        "EffectiveFarDistancePoints",
        "FarDistanceMode",
    ]:
        assert key in row


def test_compression_ratio_formula():
    from geometry_sweep import compression_ratio
    assert compression_ratio(1.30, 0.70) == 0.91
    assert compression_ratio(1.30, 0.60) == 0.78


def test_big_net_power_formula():
    from geometry_sweep import big_net_power
    assert big_net_power(1.30, 0.37) == 0.819
    assert big_net_power(1.30, 0.42) == 0.754


def test_invalid_closebig_ge_smallratio_rejected():
    from geometry_sweep import is_valid_geometry_params
    valid, reason = is_valid_geometry_params(1.30, 0.40, 0.40)
    assert not valid
    assert reason == "CloseBigOnSmall >= SmallRatio"


def test_current_candidate_has_weak_compression():
    from geometry_sweep import compression_ratio, is_valid_geometry_params
    valid, reason = is_valid_geometry_params(1.30, 0.37, 0.30)
    assert not valid
    assert reason == "CompressionRatio >= 0.90"
    assert compression_ratio(1.30, 0.70) == 0.91


def test_balanced_candidate_valid_geometry():
    from geometry_sweep import compression_ratio, big_net_power, is_valid_geometry_params
    valid, reason = is_valid_geometry_params(1.30, 0.42, 0.40)
    assert valid, reason
    assert 0.70 <= compression_ratio(1.30, 0.60) <= 0.82
    assert big_net_power(1.30, 0.42) >= 0.70


def test_strong_compression_candidate_valid_geometry():
    from geometry_sweep import compression_ratio, big_net_power, is_valid_geometry_params
    valid, reason = is_valid_geometry_params(1.30, 0.45, 0.42)
    assert valid, reason
    assert 0.70 <= compression_ratio(1.30, 0.58) <= 0.82
    assert big_net_power(1.30, 0.45) >= 0.70


def test_geometry_sweep_outputs_reports():
    from geometry_sweep import MT5_PLAN_MD, REPORT_MD, SWEEP_CSV, TOP10_MD, run_geometry_sweep
    summary = run_geometry_sweep(write_reports=True)
    assert summary.raw_combinations == 17640
    assert summary.scenarios_per_combination == 7
    assert summary.tested_combinations > 0
    for path in [SWEEP_CSV, TOP10_MD, REPORT_MD, MT5_PLAN_MD]:
        assert path.exists()
        assert path.stat().st_size > 0
    assert "Таблица Top 10" in REPORT_MD.read_text(encoding="utf-8")
    assert "PASS criteria" in MT5_PLAN_MD.read_text(encoding="utf-8")


def test_refined_sweep_generates_reports():
    from refined_geometry_sweep import REFINED_CSV, REFINED_MT5_PLAN_MD, REFINED_REPORT_MD, REFINED_TOP10_MD, run_refined_sweep
    summary = run_refined_sweep(write_reports=True)
    assert summary.raw_combinations == 20160
    assert summary.scenarios_per_combination == 9
    assert summary.tested_combinations > 0
    for path in [REFINED_CSV, REFINED_TOP10_MD, REFINED_REPORT_MD, REFINED_MT5_PLAN_MD]:
        assert path.exists()
        assert path.stat().st_size > 0


def test_refined_sweep_keeps_previous_best():
    from refined_geometry_sweep import PREVIOUS_BEST, _params_from_dict, evaluate_params
    row = evaluate_params(_params_from_dict(PREVIOUS_BEST), "Previous Best")
    assert row["BigRatio"] == 1.25
    assert row["SmallRatio"] == 0.37
    assert row["CloseBigOnSmall"] == 0.35
    assert row["CloseFarShare"] == 0.40
    assert row["ReserveShare"] == 0.60
    assert row["MaxHarvestLevels"] == 7
    assert row["MaxReverseCycles"] == 3


def test_refined_sweep_filters_bad_compression():
    from refined_geometry_sweep import is_valid_refined_params
    valid, reason = is_valid_refined_params(1.30, 0.37, 0.30, 0.70, 0.30, 7)
    assert not valid
    assert reason == "CompressionRatio >= 0.86"


def test_refined_top_candidate_has_valid_geometry():
    from refined_geometry_sweep import is_valid_refined_params, run_refined_sweep
    summary = run_refined_sweep(write_reports=False)
    top = summary.top10[0]
    valid, reason = is_valid_refined_params(top["BigRatio"], top["SmallRatio"], top["CloseBigOnSmall"], top["CloseFarShare"], top["ReserveShare"], top["MaxHarvestLevels"])
    assert valid, reason
    assert 0.68 < top["CompressionRatio"] < 0.86
    assert top["BigNetPower"] >= 0.72
    assert top["SmallCoverageGap"] >= 0.015


def test_refined_top_candidate_not_weaker_than_previous_best():
    from refined_geometry_sweep import run_refined_sweep
    summary = run_refined_sweep(write_reports=False)
    top = summary.top10[0]
    previous = summary.previous_best
    assert top["Score"] >= previous["Score"]
    assert top["PassCount"] >= previous["PassCount"]
    assert top["StopMaxLevelsCount"] <= previous["StopMaxLevelsCount"]
