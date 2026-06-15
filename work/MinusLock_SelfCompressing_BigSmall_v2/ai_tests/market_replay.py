from __future__ import annotations

try:
    from .minuslock_model import BIG, SMALL, ModelConfig, SimulationResult, simulate_sequence
except ImportError:  # pragma: no cover
    from minuslock_model import BIG, SMALL, ModelConfig, SimulationResult, simulate_sequence

SCENARIOS: dict[str, list[str]] = {
    "BIG/BIG/BIG": [BIG, BIG, BIG],
    "SMALL/SMALL/SMALL": [SMALL, SMALL, SMALL, SMALL, SMALL],
    "REAL_REPORT_SEQUENCE": [BIG, SMALL, SMALL, BIG, SMALL],
    "STRONG_BIG": [BIG, BIG, BIG, BIG, BIG],
    "CHOPPY": [BIG, SMALL, BIG, SMALL, BIG],
    "BAD_MARKET": [SMALL, SMALL, BIG, SMALL, SMALL],
}

# Observed MT5 deal result supplied by the task. It is not used to claim profitability;
# it is a calibration target showing that the real report failed via STOP_MAX_LEVELS.
OBSERVED_MT5_NET_PROFIT = -63.69
OBSERVED_MT5_STATE = "STATE_UNCLOSED_CYCLE"
OBSERVED_MT5_REASON = "STOP_MAX_LEVELS"


def run_named_scenarios(cfg: ModelConfig) -> dict[str, SimulationResult]:
    return {name: simulate_sequence(cfg, seq) for name, seq in SCENARIOS.items()}


def observed_failure_summary() -> dict[str, object]:
    return {
        "state": OBSERVED_MT5_STATE,
        "stop_reason": OBSERVED_MT5_REASON,
        "net_profit": OBSERVED_MT5_NET_PROFIT,
        "diagnosis": "MT5 report reaches STOP_MAX_LEVELS; Python model is used to inspect reserve/Far-loss math before MT5 retest.",
    }
