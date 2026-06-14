from __future__ import annotations

from dataclasses import dataclass, replace
from math import floor
from typing import Sequence

try:
    from .cycle_math import CycleMathRow
except ImportError:  # pragma: no cover
    from cycle_math import CycleMathRow

BIG = "BIG_HARVEST"
SMALL = "SMALL_AT_FAR"
FIXED_200 = "FIXED_200"
INITIAL_PLUS_CURRENT = "INITIAL_PLUS_CURRENT"
INITIAL_PLUS_CUMULATIVE = "INITIAL_PLUS_CUMULATIVE"
REAL_PRICE_DISTANCE = "REAL_PRICE_DISTANCE"

@dataclass(frozen=True)
class ModelConfig:
    start_lot: float = 1.00
    big_ratio: float = 1.30
    small_ratio: float = 0.37
    close_big_on_small: float = 0.30
    remain_big_on_small: float = 0.70
    close_far_share: float = 0.90
    reserve_share: float = 0.10
    initial_trigger_points: int = 100
    big_move_level1: int = 100
    big_move_level2: int = 150
    big_move_level3: int = 200
    far_distance_points: int = 200
    max_harvest_levels: int = 5
    max_reverse_cycles: int = 10
    lot_step: float = 0.01
    min_reverse_strength: float = 0.10
    warning_reverse_strength: float = 0.15
    strong_reverse_strength: float = 0.25
    min_projected_reserve_coverage: float = 1.00
    allow_negative_small_reverse_net: bool = False
    use_real_costs: bool = False
    commission_per_lot: float = 0.0
    swap_per_lot: float = 0.0
    spread_cost_per_lot: float = 0.0
    small_at_far_move_points: int = 200
    point_value_per_lot: float = 1.0
    far_distance_mode: str = FIXED_200

    def with_params(self, **kwargs) -> "ModelConfig":
        return replace(self, **kwargs)


def recommended_5050_config(**overrides) -> ModelConfig:
    params = dict(
        small_ratio=0.36,
        close_big_on_small=0.35,
        remain_big_on_small=0.65,
        close_far_share=0.50,
        reserve_share=0.50,
        max_harvest_levels=5,
        max_reverse_cycles=10,
    )
    params.update(overrides)
    return ModelConfig(**params)

@dataclass
class SimulationResult:
    state: str
    cycle_final_pl: float
    total_reserve: float
    final_far_lot: float
    max_far_lot: float
    max_open_lots: float
    max_margin_estimate: float
    number_of_big_harvest: int
    number_of_small_at_far: int
    worst_level: int
    reason: str
    rows: list[CycleMathRow]
    initial_ignored_profit: float

    @property
    def closed_profit(self) -> bool:
        return self.state == "STATE_CLOSED_PROFIT"

    @property
    def max_drawdown_estimate(self) -> float:
        if not self.rows:
            return 0.0
        return max(r.FarRemainLoss for r in self.rows)


def floor_lot(value: float, step: float = 0.01) -> float:
    return round(floor((value + 1e-12) / step) * step, 2)


def round_lot_nearest(value: float, step: float = 0.01) -> float:
    return round(floor((value / step) + 0.5 + 1e-12) * step, 2)


def reverse_strength(new_far: float, new_big: float) -> float:
    if new_far <= 0:
        return 0.0
    return (new_big - new_far) / new_far


def big_move_points(cfg: ModelConfig, level: int) -> int:
    if level <= 1:
        return cfg.big_move_level1
    if level == 2:
        return cfg.big_move_level2
    return cfg.big_move_level3


def costs_for_lots(cfg: ModelConfig, *lots: float) -> float:
    if not cfg.use_real_costs:
        return 0.0
    per_lot = cfg.commission_per_lot + cfg.swap_per_lot + cfg.spread_cost_per_lot
    return sum(abs(x) for x in lots) * per_lot


def effective_far_distance(cfg: ModelConfig, initial_far_distance: float, current_big_move: float, cumulative_big_move: float) -> float:
    if cfg.far_distance_mode == FIXED_200:
        return float(cfg.far_distance_points)
    if cfg.far_distance_mode == INITIAL_PLUS_CURRENT:
        return float(initial_far_distance + current_big_move)
    if cfg.far_distance_mode in {INITIAL_PLUS_CUMULATIVE, REAL_PRICE_DISTANCE}:
        return float(initial_far_distance + cumulative_big_move)
    raise ValueError(f"unknown FarDistanceMode: {cfg.far_distance_mode}")


def validate_reverse_geometry(cfg: ModelConfig, old_far: float, new_far: float, new_big: float, new_small: float) -> tuple[bool, str, float]:
    strength = reverse_strength(new_far, new_big)
    if new_far >= old_far:
        return False, "NewFarLot >= OldFarLot", strength
    if new_big <= new_far:
        return False, "NewBigLot <= NewFarLot", strength
    if new_small >= new_big:
        return False, "NewSmallLot >= NewBigLot", strength
    if strength < cfg.min_reverse_strength:
        return False, "ReverseStrength below minimum", strength
    return True, "OK", strength


def simulate_sequence(cfg: ModelConfig, sequence: Sequence[str], initial_direction: str = "UP") -> SimulationResult:
    far_lot = round_lot_nearest(cfg.start_lot, cfg.lot_step)
    reserve = 0.0
    rows: list[CycleMathRow] = []
    initial_ignored_profit = cfg.start_lot * cfg.initial_trigger_points * cfg.point_value_per_lot
    max_far = far_lot
    max_open_lots = 2.0 * far_lot
    max_margin_estimate = max_open_lots
    reverse_cycles = 0
    initial_far_distance = float(cfg.initial_trigger_points)
    cumulative_big_move = 0.0
    synthetic_far_open_price = 0.0
    synthetic_current_price = float(cfg.initial_trigger_points)
    big_count = 0
    small_count = 0
    state = "RUNNING"
    reason = "Sequence exhausted without final close"
    cycle_final_pl = 0.0

    for level, raw_scenario in enumerate(sequence, start=1):
        if level > cfg.max_harvest_levels:
            far_loss = far_lot * cfg.far_distance_points * cfg.point_value_per_lot
            rows.append(CycleMathRow(level-1, "STOP_MAX_LEVELS", far_lot, InitialFarDistancePoints=initial_far_distance, CumulativeBigMovePoints=cumulative_big_move, EffectiveFarDistancePoints=far_loss / far_lot if far_lot else 0.0, FarDistanceMode=cfg.far_distance_mode, FarOpenPrice=synthetic_far_open_price, CurrentClosePrice=synthetic_current_price, TotalReserveBefore=reserve, TotalReserveAfter=reserve, FarRemainLot=far_lot, FarRemainLoss=far_loss, State="STATE_UNCLOSED_CYCLE", Action="CLOSE_RESIDUAL_FAR", StopReason="MaxHarvestLevels exceeded", MaxOpenLots=max_open_lots, MaxFarLot=max_far, InitialIgnoredProfit=initial_ignored_profit))
            return SimulationResult("STATE_UNCLOSED_CYCLE", reserve - far_loss, reserve, far_lot, max_far, max_open_lots, max_margin_estimate, big_count, small_count, level-1, "STOP_MAX_LEVELS", rows, initial_ignored_profit)

        scenario = BIG if raw_scenario.upper().startswith("BIG") else SMALL
        far_before = far_lot
        big_lot = round_lot_nearest(far_lot * cfg.big_ratio, cfg.lot_step)
        small_lot = round_lot_nearest(big_lot * cfg.small_ratio, cfg.lot_step)
        max_far = max(max_far, far_lot)
        max_open_lots = max(max_open_lots, far_lot + big_lot + small_lot)
        max_margin_estimate = max(max_margin_estimate, max_open_lots)
        reserve_before = reserve

        if scenario == BIG:
            big_count += 1
            move = big_move_points(cfg, level)
            cumulative_big_move += move
            synthetic_current_price = synthetic_far_open_price + initial_far_distance + cumulative_big_move
            effective_distance = effective_far_distance(cfg, initial_far_distance, move, cumulative_big_move)
            profit_big = big_lot * move * cfg.point_value_per_lot
            loss_small = small_lot * move * cfg.point_value_per_lot
            costs = costs_for_lots(cfg, big_lot, small_lot)
            net = profit_big - loss_small - costs
            close_far_budget = round(max(0.0, net * cfg.close_far_share), 2)
            reserve_add = round(max(0.0, net * cfg.reserve_share), 2)
            close_far_raw = close_far_budget / (effective_distance * cfg.point_value_per_lot) if effective_distance > 0 else 0.0
            close_far_rounded = min(far_lot, floor_lot(close_far_raw, cfg.lot_step))
            far_lot = round(max(0.0, far_lot - close_far_rounded), 2)
            reserve = round(reserve + reserve_add, 2)
            far_loss = round(far_lot * effective_distance * cfg.point_value_per_lot, 2)
            final_allowed = reserve >= far_loss
            cycle_final_pl = round(reserve - far_loss, 2)
            state = "STATE_CLOSED_PROFIT" if final_allowed else "STATE_BIG_HARVEST"
            action = "FINAL_CLOSE" if final_allowed else "REPEAT_HARVEST"
            if not final_allowed and level >= cfg.max_harvest_levels:
                state = "STATE_UNCLOSED_CYCLE"
                action = "CLOSE_RESIDUAL_FAR"
                reason = "STOP_MAX_LEVELS after Big-harvest"
            rows.append(CycleMathRow(level, scenario, far_before, BigLot=big_lot, SmallLot=small_lot, InitialFarDistancePoints=initial_far_distance, CurrentBigMovePoints=move, CumulativeBigMovePoints=cumulative_big_move, EffectiveFarDistancePoints=effective_distance, FarDistanceMode=cfg.far_distance_mode, FarOpenPrice=synthetic_far_open_price, CurrentClosePrice=synthetic_current_price, ProfitBig=profit_big, LossSmall=loss_small, NetProfit=net, CloseFarBudget=close_far_budget, ReserveAdd=reserve_add, TotalReserveBefore=reserve_before, TotalReserveAfter=reserve, CloseFarLotRaw=close_far_raw, CloseFarLotRounded=close_far_rounded, FarRemainLot=far_lot, FarRemainLoss=far_loss, FinalCloseAllowed=final_allowed, State=state, Action=action, StopReason="" if final_allowed or level < cfg.max_harvest_levels else reason, CycleFinalPL=cycle_final_pl, MaxOpenLots=max_open_lots, MaxFarLot=max_far, InitialIgnoredProfit=initial_ignored_profit))
            if final_allowed:
                return SimulationResult(state, cycle_final_pl, reserve, far_lot, max_far, max_open_lots, max_margin_estimate, big_count, small_count, level, "FinalCloseAllowed after Big-harvest", rows, initial_ignored_profit)
            if level >= cfg.max_harvest_levels:
                return SimulationResult(state, cycle_final_pl, reserve, far_lot, max_far, max_open_lots, max_margin_estimate, big_count, small_count, level, reason, rows, initial_ignored_profit)
        else:
            small_count += 1
            close_big = round_lot_nearest(big_lot * cfg.close_big_on_small, cfg.lot_step)
            new_far = floor_lot(max(0.0, big_lot - close_big), cfg.lot_step)
            new_big = round_lot_nearest(new_far * cfg.big_ratio, cfg.lot_step)
            new_small = round_lot_nearest(new_big * cfg.small_ratio, cfg.lot_step)
            move = cfg.small_at_far_move_points
            small_pl = small_lot * move * cfg.point_value_per_lot
            old_far_pl = 0.0
            closed_big_pl = -close_big * move * cfg.point_value_per_lot
            costs = costs_for_lots(cfg, small_lot, far_lot, close_big)
            small_reverse_net = small_pl + old_far_pl + closed_big_pl - costs
            valid, geom_reason, strength = validate_reverse_geometry(cfg, far_lot, new_far, new_big, new_small)
            effective_distance = 0.0
            projected_loss = new_far * effective_distance * cfg.point_value_per_lot
            expected_next_reserve = max(0.0, (new_big - new_small) * big_move_points(cfg, level + 1) * cfg.reserve_share)
            projected_coverage = 999.0 if projected_loss <= 0 else (reserve + expected_next_reserve) / projected_loss
            if not valid:
                rows.append(CycleMathRow(level, scenario, far_before, BigLot=big_lot, SmallLot=small_lot, InitialFarDistancePoints=initial_far_distance, CurrentBigMovePoints=0.0, CumulativeBigMovePoints=cumulative_big_move, EffectiveFarDistancePoints=effective_distance, FarDistanceMode=cfg.far_distance_mode, FarOpenPrice=synthetic_far_open_price, CurrentClosePrice=synthetic_current_price, SmallPL=small_pl, OldFarPL=old_far_pl, ClosedBigPL=closed_big_pl, NetProfit=small_reverse_net, TotalReserveBefore=reserve_before, TotalReserveAfter=reserve, CloseFarLotRounded=close_big, FarRemainLot=new_far, FarRemainLoss=projected_loss, ReverseStrength=strength, ProjectedReserveCoverage=projected_coverage, State="STATE_INVALID_REVERSE_GEOMETRY", Action="STOP", StopReason=geom_reason, CycleFinalPL=reserve-projected_loss, MaxOpenLots=max_open_lots, MaxFarLot=max_far, InitialIgnoredProfit=initial_ignored_profit))
                return SimulationResult("STATE_INVALID_REVERSE_GEOMETRY", reserve-projected_loss, reserve, new_far, max_far, max_open_lots, max_margin_estimate, big_count, small_count, level, geom_reason, rows, initial_ignored_profit)
            if small_reverse_net <= 0 and not cfg.allow_negative_small_reverse_net:
                rows.append(CycleMathRow(level, scenario, far_before, BigLot=big_lot, SmallLot=small_lot, InitialFarDistancePoints=initial_far_distance, CurrentBigMovePoints=0.0, CumulativeBigMovePoints=cumulative_big_move, EffectiveFarDistancePoints=effective_distance, FarDistanceMode=cfg.far_distance_mode, FarOpenPrice=synthetic_far_open_price, CurrentClosePrice=synthetic_current_price, SmallPL=small_pl, OldFarPL=old_far_pl, ClosedBigPL=closed_big_pl, NetProfit=small_reverse_net, TotalReserveBefore=reserve_before, TotalReserveAfter=reserve, CloseFarLotRounded=close_big, FarRemainLot=new_far, FarRemainLoss=projected_loss, ReverseStrength=strength, ProjectedReserveCoverage=projected_coverage, State="STATE_INVALID_SMALL_GEOMETRY", Action="STOP", StopReason="SmallReverseNet <= 0", CycleFinalPL=reserve-projected_loss, MaxOpenLots=max_open_lots, MaxFarLot=max_far, InitialIgnoredProfit=initial_ignored_profit))
                return SimulationResult("STATE_INVALID_SMALL_GEOMETRY", reserve-projected_loss, reserve, new_far, max_far, max_open_lots, max_margin_estimate, big_count, small_count, level, "SmallReverseNet <= 0", rows, initial_ignored_profit)
            reverse_cycles += 1
            far_lot = new_far
            initial_far_distance = 0.0
            cumulative_big_move = 0.0
            synthetic_far_open_price = synthetic_current_price
            final_allowed = reserve >= projected_loss
            cycle_final_pl = round(reserve - projected_loss, 2)
            action = "FINAL_CLOSE" if final_allowed else "OPEN_NEW_BIG_SMALL"
            state = "STATE_CLOSED_PROFIT" if final_allowed else "STATE_SMALL_SCENARIO"
            if reverse_cycles > cfg.max_reverse_cycles:
                state = "STATE_REVERSE_LIMIT"
                action = "STOP"
                reason = "MaxReverseCycles exceeded"
            elif not final_allowed and level >= cfg.max_harvest_levels:
                state = "STATE_UNCLOSED_CYCLE"
                action = "CLOSE_RESIDUAL_FAR"
                reason = "STOP_MAX_LEVELS after Small-at-Far"
            rows.append(CycleMathRow(level, scenario, far_before, BigLot=big_lot, SmallLot=small_lot, InitialFarDistancePoints=initial_far_distance, CurrentBigMovePoints=0.0, CumulativeBigMovePoints=cumulative_big_move, EffectiveFarDistancePoints=effective_distance, FarDistanceMode=cfg.far_distance_mode, FarOpenPrice=synthetic_far_open_price, CurrentClosePrice=synthetic_current_price, SmallPL=small_pl, OldFarPL=old_far_pl, ClosedBigPL=closed_big_pl, NetProfit=small_reverse_net, TotalReserveBefore=reserve_before, TotalReserveAfter=reserve, CloseFarLotRounded=close_big, FarRemainLot=far_lot, FarRemainLoss=projected_loss, FinalCloseAllowed=final_allowed, ReverseStrength=strength, ProjectedReserveCoverage=projected_coverage, State=state, Action=action, StopReason="" if state in {"STATE_SMALL_SCENARIO", "STATE_CLOSED_PROFIT"} else reason, CycleFinalPL=cycle_final_pl, MaxOpenLots=max_open_lots, MaxFarLot=max_far, InitialIgnoredProfit=initial_ignored_profit))
            if final_allowed or state in {"STATE_REVERSE_LIMIT", "STATE_UNCLOSED_CYCLE"}:
                return SimulationResult(state, cycle_final_pl, reserve, far_lot, max_far, max_open_lots, max_margin_estimate, big_count, small_count, level, reason if not final_allowed else "FinalCloseAllowed after Small-at-Far", rows, initial_ignored_profit)

    final_loss = far_lot * cfg.far_distance_points * cfg.point_value_per_lot
    final_state = "STATE_UNCLOSED_CYCLE"
    if reserve >= final_loss:
        final_state = "STATE_CLOSED_PROFIT"
        reason = "FinalCloseAllowed after sequence"
    else:
        reason = "Sequence ended before FinalCloseAllowed"
    return SimulationResult(final_state, round(reserve - final_loss, 2), reserve, far_lot, max_far, max_open_lots, max_margin_estimate, big_count, small_count, len(sequence), reason, rows, initial_ignored_profit)
