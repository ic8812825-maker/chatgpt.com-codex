from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass
class LyapunovState:
    drawdown: float
    exposure: float
    margin_usage: float
    depth: float
    distance_to_be: float
    unrealized_loss: float
    control_intensity: float = 0.0
    latency_ticks: float = 0.0
    compressions_triggered: float = 0.0


BASE_COEFFS = {
    "drawdown": 0.30,
    "exposure": 0.18,
    "margin_usage": 0.18,
    "depth": 0.12,
    "distance_to_be": 0.12,
    "unrealized_loss": 0.10,
}


IMPROVED_COEFFS = {
    "drawdown": 0.22,
    "exposure": 0.12,
    "margin_usage": 0.18,
    "depth": 0.10,
    "distance_to_be": 0.08,
    "unrealized_loss": 0.10,
    "control_intensity": 0.08,
    "latency": 0.04,
    "compression": 0.04,
    "corr_dd_margin": 0.04,
}


def _clamp01(v: float) -> float:
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def _safe_scale(v: float, scale: float) -> float:
    if scale <= 1e-12:
        return 0.0
    return _clamp01(abs(v) / scale)


def _log_feature(x: float, k: float = 6.0) -> float:
    x = _clamp01(x)
    return math.log1p(k * x) / math.log1p(k)


def lyapunov_value_baseline(s: LyapunovState) -> float:
    ndrawdown = _safe_scale(s.drawdown, 1.0)
    nexposure = _safe_scale(s.exposure, 10.0)
    nmargin = _safe_scale(s.margin_usage, 1.5)
    ndepth = _safe_scale(s.depth, 60.0)
    ndist = _safe_scale(s.distance_to_be, 5000.0)
    nloss = _safe_scale(s.unrealized_loss, 50000.0)

    return (
        BASE_COEFFS["drawdown"] * ndrawdown
        + BASE_COEFFS["exposure"] * nexposure
        + BASE_COEFFS["margin_usage"] * nmargin
        + BASE_COEFFS["depth"] * ndepth
        + BASE_COEFFS["distance_to_be"] * ndist
        + BASE_COEFFS["unrealized_loss"] * nloss
    )


def lyapunov_value_improved(s: LyapunovState, dynamic_ranges: dict[str, float] | None = None) -> float:
    ranges = dynamic_ranges or {}
    # dynamic ranges make shocks less dominant than fixed caps
    dd_scale = max(0.15, ranges.get("drawdown", 1.0))
    ex_scale = max(1.0, ranges.get("exposure", 10.0))
    mu_scale = max(0.2, ranges.get("margin_usage", 1.5))
    depth_scale = max(5.0, ranges.get("depth", 60.0))
    dist_scale = max(150.0, ranges.get("distance_to_be", 5000.0))
    loss_scale = max(1000.0, ranges.get("unrealized_loss", 50000.0))

    ndrawdown = _log_feature(_safe_scale(s.drawdown, dd_scale), k=8.0)
    nexposure = _log_feature(_safe_scale(s.exposure, ex_scale), k=8.0)
    nmargin = _log_feature(_safe_scale(s.margin_usage, mu_scale), k=6.0)
    ndepth = _log_feature(_safe_scale(s.depth, depth_scale), k=5.0)
    ndist = _log_feature(_safe_scale(s.distance_to_be, dist_scale), k=6.0)
    nloss = _log_feature(_safe_scale(s.unrealized_loss, loss_scale), k=8.0)

    nctrl = _log_feature(_safe_scale(s.control_intensity, 1.0), k=4.0)
    nlat = _log_feature(_safe_scale(s.latency_ticks, 20.0), k=4.0)
    ncomp = _log_feature(_safe_scale(s.compressions_triggered, 100.0), k=4.0)

    # correlation term drawdown<->margin captures coupled stress amplification
    corr_dd_margin = math.sqrt(max(0.0, ndrawdown * nmargin))

    return (
        IMPROVED_COEFFS["drawdown"] * ndrawdown
        + IMPROVED_COEFFS["exposure"] * nexposure
        + IMPROVED_COEFFS["margin_usage"] * nmargin
        + IMPROVED_COEFFS["depth"] * ndepth
        + IMPROVED_COEFFS["distance_to_be"] * ndist
        + IMPROVED_COEFFS["unrealized_loss"] * nloss
        + IMPROVED_COEFFS["control_intensity"] * nctrl
        + IMPROVED_COEFFS["latency"] * nlat
        + IMPROVED_COEFFS["compression"] * ncomp
        + IMPROVED_COEFFS["corr_dd_margin"] * corr_dd_margin
    )


# backward-compatible alias
lyapunov_value = lyapunov_value_improved
