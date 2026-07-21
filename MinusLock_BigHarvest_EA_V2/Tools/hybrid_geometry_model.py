"""Independent, conservative model for Hybrid Split Big research.

It deliberately does not import the EA.  The model is a screening and proof
tool: candidates must pass here *and* in MetaTrader before they can be used.
All monetary buckets are mutually exclusive by construction.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from math import ceil, log
from typing import Dict, Iterable, List, Tuple


ARCHITECTURES = ("core_target", "core_budget", "trend_funded", "two_stage", "dynamic")


@dataclass(frozen=True)
class Broker:
    lot_step: float = 0.01
    min_lot: float = 0.01
    point_value: float = 1.0
    margin_per_lot: float = 1000.0
    equity: float = 10000.0
    max_margin_percent: float = 60.0
    spread_points: float = 20.0
    commission_per_lot: float = 2.0
    slippage_points: float = 2.0
    swap_per_lot: float = 0.0
    execution_buffer: float = 1.0


@dataclass(frozen=True)
class Candidate:
    architecture: str
    core_ratio: float
    trend_ratio: float
    small_ratio: float
    reserve_share: float
    target_far_ratio: float
    safety_factor: float = 1.10
    min_net_exposure: float = 0.05
    max_new_big_ratio: float = 0.99
    minimum_improvement: float = 0.01


@dataclass
class Evaluation:
    candidate: Candidate
    accepted: bool
    reject_reason: str
    core_lot: float
    trend_lot: float
    small_lot: float
    new_far_lot: float
    net_big_exposure: float
    recovery_slope: float
    reserve_slope: float
    far_loss_slope: float
    catchup_ratio: float
    new_far_ratio: float
    new_big_gross_ratio: float
    new_big_directional_ratio: float
    margin_percent: float
    transition_gross: float
    transition_costs: float
    transition_net: float
    reserve_credit: float
    transition_budget: float
    reverse_bound: int
    score: float

    def row(self) -> Dict[str, object]:
        d = asdict(self.candidate)
        d.update(asdict(self))
        d.pop("candidate", None)
        return d


def floor_step(value: float, broker: Broker) -> float:
    if value <= 0:
        return 0.0
    return int((value + 1e-12) / broker.lot_step) * broker.lot_step


def close_cost(lot: float, broker: Broker, cost_multiplier: float = 1.0) -> float:
    return lot * (broker.spread_points + broker.slippage_points) * broker.point_value * cost_multiplier + lot * (broker.commission_per_lot + broker.swap_per_lot) * cost_multiplier + broker.execution_buffer


def reverse_count(far: float, q: float, broker: Broker) -> int:
    if far <= broker.min_lot or not (0 < q < 1):
        return 0
    # Conservative discrete bound: include one extra rounded transition.
    return max(0, ceil(log(broker.min_lot / far) / log(q))) + 1


def evaluate(c: Candidate, broker: Broker = Broker(), far_lot: float = 1.0,
             far_distance: float = 200.0, cost_multiplier: float = 1.0) -> Evaluation:
    """Evaluate one rounded candidate using the mandatory hard gates.

    At the reverse point OldFar, SmallBase and BigTrend are closed.  The
    remaining BigCore is explicitly targeted to NewFar; it is never financed
    by Final Reserve.  `transition_budget` is diagnostic only and cannot be
    credited to reserve a second time.
    """
    core = floor_step(c.core_ratio * far_lot, broker)
    trend = floor_step(c.trend_ratio * far_lot, broker)
    small = floor_step(c.small_ratio * far_lot, broker)
    target = floor_step(c.target_far_ratio * far_lot, broker)
    # The reverse leaves only BigCore; no BigTrend can become Far.
    new_far = min(core, target)
    net = core + trend - small - far_lot
    recovery_slope = net * broker.point_value
    # Harvestable closed basket slope at a Big close, excluding Far.
    harvest_slope = core + trend - small
    reserve_slope = c.reserve_share * harvest_slope * broker.point_value
    far_slope = far_lot * broker.point_value
    catchup = reserve_slope / far_slope if far_slope else 0.0
    q = new_far / far_lot if far_lot else 1.0
    # Gross Big explicitly excludes SmallBase; directional exposure is a
    # separate mandatory metric, matching the design document and MQL5 plan.
    next_gross = (c.core_ratio + c.trend_ratio) * q
    next_directional = (c.core_ratio + c.trend_ratio - c.small_ratio - 1.0) * q
    margin_percent = (far_lot + core + trend + small) * broker.margin_per_lot / broker.equity * 100.0

    # Conservative transition estimate: closes Far and small at adverse
    # distance, closes trend at breakeven, and preserves core remainder.
    # The target-new-Far architecture explicitly closes the excess winning
    # BigCore.  Its realised money finances the transition; only the rounded
    # remainder is promoted, so no invisible reserve borrowing is possible.
    transition_gross = (trend + max(0.0, core - new_far)) * far_distance * broker.point_value - (far_lot + small) * far_distance * broker.point_value
    transition_costs = close_cost(far_lot + small + trend + max(0.0, core - new_far), broker, cost_multiplier)
    transition_net = transition_gross - transition_costs
    # Only positive confirmed Big harvest gets a final-reserve credit.
    reserve_credit = max(0.0, c.reserve_share * (harvest_slope * far_distance * broker.point_value - close_cost(core + trend + small, broker, cost_multiplier)))
    transition_budget = max(0.0, transition_net)  # separate from reserve_credit

    reason = ""
    if c.architecture not in ARCHITECTURES: reason = "UNKNOWN_ARCHITECTURE"
    elif core < broker.min_lot or trend <= 0 or small <= 0: reason = "INVALID_BROKER_VOLUME"
    elif net < c.min_net_exposure * far_lot: reason = "NET_BIG_EXPOSURE"
    elif recovery_slope < c.minimum_improvement: reason = "RECOVERY_NON_MONOTONIC"
    elif catchup < c.safety_factor: reason = "RESERVE_CATCHUP"
    elif not (0 < q < 1): reason = "FAR_COMPRESSION"
    elif next_directional >= 1.0: reason = "NEW_BIG_DIRECTIONAL_EXPOSURE"
    elif next_gross > c.max_new_big_ratio: reason = "NEW_BIG_GROSS_EXPOSURE"
    elif margin_percent > broker.max_margin_percent: reason = "MARGIN_GATE"
    elif transition_net < 0.0: reason = "TRANSITION_LOSS"
    elif new_far < broker.min_lot: reason = "NEW_FAR_BELOW_MIN_LOT"
    accepted = not reason
    bound = reverse_count(far_lot, q, broker) if accepted else 0
    score = (3.0 * catchup + 2.0 * recovery_slope + (1.0 - q) * 4.0 + (1.0 - next_gross) - margin_percent / 100.0 - bound * .02) if accepted else -1e9
    return Evaluation(c, accepted, reason or "PASS", core, trend, small, new_far, net, recovery_slope,
                      reserve_slope, far_slope, catchup, q, next_gross, next_directional,
                      margin_percent, transition_gross, transition_costs, transition_net,
                      reserve_credit, transition_budget, bound, score)


def select_minimum_safe_new_far(c: Candidate, broker: Broker = Broker(), far_lot: float = 1.0,
                                far_distance: float = 200.0, cost_multiplier: float = 1.0) -> Evaluation:
    """Mirror MQL5 BuildHybridReversePlan's ascending broker-step scan.

    The configured target is an upper bound, not a fixed remainder.  The
    first accepted rounded lot is therefore the smallest safe NewFar.
    """
    upper = floor_step(min(c.target_far_ratio * far_lot, c.core_ratio * far_lot - broker.lot_step), broker)
    target = broker.min_lot
    last = evaluate(c, broker, far_lot, far_distance, cost_multiplier)
    while target <= upper + broker.lot_step * .25:
        candidate = replace(c, target_far_ratio=target / far_lot)
        result = evaluate(candidate, broker, far_lot, far_distance, cost_multiplier)
        if result.accepted:
            return result
        last = result
        target = floor_step(target + broker.lot_step, broker)
    last.accepted = False
    last.reject_reason = "NO_SAFE_NEW_FAR"
    return last


def monotonicity_trace(c: Candidate, broker: Broker, far_lot: float, points: Iterable[float], cost_multiplier: float = 1.0) -> List[float]:
    e = evaluate(c, broker, far_lot, cost_multiplier=cost_multiplier)
    # Costs are constants per basket; linear signed exposure makes this a
    # conservative projected full-close recovery trace.
    initial_cost = close_cost(far_lot + e.core_lot + e.trend_lot + e.small_lot, broker, cost_multiplier)
    return [e.net_big_exposure * p * broker.point_value - initial_cost for p in points]


def all_start_lot_bounds(c: Candidate, broker: Broker) -> Dict[float, int]:
    return {lot: reverse_count(lot, c.target_far_ratio, broker) for lot in (0.01, .05, .10, .50, 1., 2., 5., 10.)}
