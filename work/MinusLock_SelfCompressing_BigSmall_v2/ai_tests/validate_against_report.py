from __future__ import annotations

from pathlib import Path

try:
    from .market_replay import OBSERVED_MT5_NET_PROFIT, OBSERVED_MT5_REASON, SCENARIOS
    from .minuslock_model import ModelConfig, simulate_sequence
    from .report_parser import parse_report
except ImportError:  # pragma: no cover
    from market_replay import OBSERVED_MT5_NET_PROFIT, OBSERVED_MT5_REASON, SCENARIOS
    from minuslock_model import ModelConfig, simulate_sequence
    from report_parser import parse_report


def validate_sample_report(path: Path) -> dict[str, object]:
    deals = parse_report(path)
    parsed_profit = round(sum(d.profit + d.commission + d.swap for d in deals), 2)
    model = simulate_sequence(ModelConfig(max_harvest_levels=5, max_reverse_cycles=10), SCENARIOS["REAL_REPORT_SEQUENCE"])
    return {
        "report_path": str(path),
        "deals": len(deals),
        "parsed_net_profit": parsed_profit,
        "observed_mt5_net_profit": OBSERVED_MT5_NET_PROFIT,
        "observed_stop_reason": OBSERVED_MT5_REASON,
        "python_model_state": model.state,
        "python_model_cycle_final_pl": round(model.cycle_final_pl, 2),
        "note": "Exact MT5 match requires exported deal history with real spread/commission/swap. This compares state and failure mode first.",
    }


if __name__ == "__main__":
    print(validate_sample_report(Path(__file__).with_name("data") / "sample_mt5_report.csv"))
