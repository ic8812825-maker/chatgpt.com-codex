from __future__ import annotations
from dataclasses import dataclass


@dataclass
class LyapunovState:
    drawdown: float
    exposure: float
    margin_usage: float
    depth: float
    distance_to_be: float
    unrealized_loss: float


COEFFS = {
    "drawdown": 0.30,
    "exposure": 0.18,
    "margin_usage": 0.18,
    "depth": 0.12,
    "distance_to_be": 0.12,
    "unrealized_loss": 0.10,
}


NORMALIZATION = {
    "drawdown": 1.0,
    "exposure": 10.0,
    "margin_usage": 1.5,
    "depth": 60.0,
    "distance_to_be": 5000.0,
    "unrealized_loss": 50000.0,
}


def _clamp01(v: float) -> float:
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def lyapunov_value(s: LyapunovState) -> float:
    ndrawdown = _clamp01(s.drawdown / NORMALIZATION["drawdown"])
    nexposure = _clamp01(abs(s.exposure) / NORMALIZATION["exposure"])
    nmargin = _clamp01(s.margin_usage / NORMALIZATION["margin_usage"])
    ndepth = _clamp01(s.depth / NORMALIZATION["depth"])
    ndist = _clamp01(s.distance_to_be / NORMALIZATION["distance_to_be"])
    nloss = _clamp01(abs(s.unrealized_loss) / NORMALIZATION["unrealized_loss"])

    return (
        COEFFS["drawdown"] * ndrawdown
        + COEFFS["exposure"] * nexposure
        + COEFFS["margin_usage"] * nmargin
        + COEFFS["depth"] * ndepth
        + COEFFS["distance_to_be"] * ndist
        + COEFFS["unrealized_loss"] * nloss
    )
