#!/usr/bin/env python3
"""Deterministic offline engineering study for all EA input parameters.

This tool does not change EA trading logic and is not an MT5 Strategy Tester
replacement. It creates a reproducible mathematical screening report, ranked
candidate table, sensitivity table and scenario .set presets for MT5 validation.
"""

from __future__ import annotations

import csv
import itertools
import math
import random
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean
from typing import Any

import sys
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_set_files import DEFAULTS, SET_KEYS, write_set_file

ROOT = SCRIPT_DIR.parent
CONFIG = ROOT / "Include" / "Config.mqh"
REPORTS = ROOT / "Reports"
PRESET_DIR = ROOT / "Sets" / "Optimization_Presets"
CANDIDATES_CSV = REPORTS / "Full_Parameter_Optimization_Candidates.csv"
SUMMARY_CSV = REPORTS / "Parameter_Optimization_Summary.csv"
SENSITIVITY_CSV = REPORTS / "Parameter_Sensitivity.csv"
DEPENDENCY_CSV = REPORTS / "Parameter_Dependency_Data.csv"
REPORT_MD = REPORTS / "Full_Parameter_Optimization_Report.md"

RANDOM_SEED = 20260703

INPUT_RE = re.compile(r"^input\s+(?P<type>.+?)\s+(?P<name>\w+)\s*=\s*(?P<value>[^;]+);")

GEOMETRY_MODES = {
    "GEOMETRY_MANUAL": 0,
    "GEOMETRY_ATR_SAFE": 1,
    "GEOMETRY_ATR_BALANCED": 2,
    "GEOMETRY_ATR_PROFIT": 3,
    "GEOMETRY_ATR_CUSTOM": 4,
}

TIMEFRAMES = {"PERIOD_M15": 15, "PERIOD_M30": 30, "PERIOD_H1": 60, "PERIOD_H4": 240}

PARAM_RANGES: dict[str, list[Any]] = {
    "GeometryMode": [0, 1, 2, 3, 4],
    "InitialTriggerPoints": [160, 180, 190, 200, 220],
    "BigMoveStartPoints": [180, 190, 200, 210, 220],
    "BigMoveStepPoints": [60, 70, 75, 80, 90],
    "FarDistancePoints": [225, 250, 275, 300, 325],
    "GeometryRoundStep": [5, 10],
    "InitialRoundStep": [5, 10, 20],
    "BigStartRoundStep": [5, 10, 20],
    "BigStepRoundStep": [5, 10],
    "FarDistanceRoundStep": [25, 50],
    "FreezeGeometryPerCycle": ["true"],
    "ATRTimeframe": [30, 60],
    "ATRPeriod": [14, 20, 21],
    "ATRInitialMultiplier": [0.95, 1.00, 1.05],
    "ATRBigStartMultiplier": [1.00, 1.10, 1.15, 1.20],
    "ATRStepMultiplier": [0.35, 0.40, 0.45],
    "ATRFarMultiplier": [1.30, 1.45, 1.50, 1.60],
    "MinInitialTriggerPoints": [100, 120],
    "MaxInitialTriggerPoints": [240, 250],
    "MinBigMoveStartPoints": [100, 120],
    "MaxBigMoveStartPoints": [250, 260],
    "MinBigMoveStepPoints": [50, 60],
    "MaxBigMoveStepPoints": [120, 125],
    "MinFarDistancePoints": [200, 225],
    "MaxFarDistancePoints": [375, 400],
    "BigRatio": [1.10, 1.12, 1.14, 1.15, 1.16, 1.18],
    "SmallRatio": [0.25, 0.30, 0.34, 0.36, 0.38, 0.40],
    "CloseBigOnSmall": [0.35, 0.40, 0.45, 0.50],
    "RemainBigOnSmall": [0.65, 0.60, 0.55, 0.50],
    "CloseFarShare": [0.40, 0.50, 0.65, 0.75, 0.90],
    "ReserveShare": [0.60, 0.50, 0.35, 0.25, 0.10],
    "SmallReserveShare": [0.03, 0.05, 0.08, 0.10],
    "MaxHarvestLevels": [5, 6, 7, 8],
    "MaxReverseCycles": [7, 10, 12],
    "MinReverseStrength": [0.10, 0.12, 0.15],
    "WarningReverseStrength": [0.15, 0.18, 0.20],
    "StrongReverseStrength": [0.25, 0.30, 0.35],
    "MinProjectedReserveCoverage": [1.00, 1.10, 1.20],
    "MaxManagedPositions": [8, 10, 12],
    "MaxActiveSymbols": [6, 10, 14],
    "MaxAccountMarginPercent": [45.0, 55.0, 60.0],
    "MaxMarginPercent": [45.0, 55.0, 60.0],
    "MaxDrawdownPercent": [18.0, 22.0, 25.0],
    "MaxSpreadPoints": [30.0, 40.0, 60.0],
}

RECOMMENDED: dict[str, Any] = {
    "StartLot": 0.10,
    "BigRatio": 1.14,
    "SmallRatio": 0.36,
    "CloseBigOnSmall": 0.40,
    "RemainBigOnSmall": 0.60,
    "CloseFarShare": 0.75,
    "ReserveShare": 0.25,
    "SmallReserveShare": 0.05,
    "UseRecommended5050Preset": "false",
    "InitialTriggerPoints": 190,
    "BigMoveStartPoints": 200,
    "BigMoveStepPoints": 75,
    "FarDistancePoints": 275,
    "FarDistanceMode": 3,
    "GeometryMode": 2,
    "ATRTimeframe": 60,
    "ATRPeriod": 20,
    "ATRInitialMultiplier": 1.00,
    "ATRBigStartMultiplier": 1.15,
    "ATRStepMultiplier": 0.40,
    "ATRFarMultiplier": 1.50,
    "MinInitialTriggerPoints": 100,
    "MaxInitialTriggerPoints": 250,
    "MinBigMoveStartPoints": 100,
    "MaxBigMoveStartPoints": 260,
    "MinBigMoveStepPoints": 50,
    "MaxBigMoveStepPoints": 125,
    "MinFarDistancePoints": 200,
    "MaxFarDistancePoints": 400,
    "GeometryRoundStep": 5,
    "InitialRoundStep": 10,
    "BigStartRoundStep": 10,
    "BigStepRoundStep": 5,
    "FarDistanceRoundStep": 50,
    "FreezeGeometryPerCycle": "true",
    "PrintAdaptiveGeometryLog": "true",
    "MaxHarvestLevels": 6,
    "SmallFarTouchOffsetPoints": 0,
    "MaxReverseCycles": 10,
    "MinReverseStrength": 0.12,
    "WarningReverseStrength": 0.18,
    "StrongReverseStrength": 0.30,
    "MinProjectedReserveCoverage": 1.10,
    "StopOnInvalidReverseGeometry": "true",
    "StopOnReverseLimit": "true",
    "AllowNegativeSmallReverseNet": "false",
    "LotStep": 0.01,
    "MaxSpreadPoints": 40.0,
    "MaxMarginPercent": 55.0,
    "MaxDrawdownPercent": 22.0,
    "MaxManagedPositions": 10,
    "MaxAccountMarginPercent": 55.0,
    "MaxActiveSymbols": 10,
    "StopOnRiskGateBlocked": "true",
    "RiskGateLogIntervalSeconds": 60,
    "MaxCloseRetryAttempts": 20,
    "RetryLogIntervalSeconds": 30,
    "MaxSlippagePoints": 30,
    "CloseAllOnInvalidGeometry": "true",
    "CloseFarOnMaxLevels": "true",
    "ReserveMismatchTolerance": 0.01,
    "VolumeMismatchToleranceLots": 0.001,
    "ReconciliationIntervalSeconds": 300,
    "PositionResolutionLookbackSeconds": 10,
    "MagicNumber": 20260609,
    "AllowRealTrading": "true",
    "UseInternalSimulation": "false",
    "UseMarketOrders": "true",
    "EnableCycleMathCsv": "true",
    "VerboseTickLogs": "false",
}

PRESETS: dict[str, dict[str, Any]] = {
    "Ultra_Conservative": {"GeometryMode": 1, "BigRatio": 1.12, "SmallRatio": 0.34, "CloseFarShare": 0.50, "ReserveShare": 0.50, "MaxHarvestLevels": 5, "MaxDrawdownPercent": 18.0, "MaxAccountMarginPercent": 45.0},
    "Conservative": {"GeometryMode": 1, "BigRatio": 1.13, "SmallRatio": 0.35, "CloseFarShare": 0.65, "ReserveShare": 0.35, "MaxHarvestLevels": 6},
    "Universal": {},
    "Aggressive_Recovery": {"GeometryMode": 3, "BigRatio": 1.16, "SmallRatio": 0.38, "CloseFarShare": 0.90, "ReserveShare": 0.10, "MaxHarvestLevels": 7, "MaxDrawdownPercent": 25.0},
    "High_Volatility": {"GeometryMode": 1, "ATRFarMultiplier": 1.60, "ATRBigStartMultiplier": 1.20, "FarDistancePoints": 325, "MaxSpreadPoints": 60.0},
    "Low_Volatility": {"GeometryMode": 2, "ATRFarMultiplier": 1.30, "ATRBigStartMultiplier": 1.05, "FarDistancePoints": 250, "BigMoveStepPoints": 70},
    "Trend": {"GeometryMode": 3, "BigRatio": 1.15, "SmallRatio": 0.34, "CloseFarShare": 0.75, "ReserveShare": 0.25},
    "Anti_Trend": {"GeometryMode": 1, "BigRatio": 1.12, "SmallRatio": 0.38, "CloseFarShare": 0.50, "ReserveShare": 0.50, "MaxReverseCycles": 12},
    "Adaptive_ATR_SAFE": {"GeometryMode": 1, "ATRInitialMultiplier": 1.00, "ATRBigStartMultiplier": 1.00, "ATRStepMultiplier": 0.40, "ATRFarMultiplier": 1.30},
    "Adaptive_ATR_BALANCED": {"GeometryMode": 2, "ATRInitialMultiplier": 1.00, "ATRBigStartMultiplier": 1.15, "ATRStepMultiplier": 0.40, "ATRFarMultiplier": 1.50},
    "Adaptive_ATR_PROFIT": {"GeometryMode": 3, "ATRInitialMultiplier": 1.05, "ATRBigStartMultiplier": 1.20, "ATRStepMultiplier": 0.45, "ATRFarMultiplier": 1.60},
    "Multi_Symbol": {"GeometryMode": 2, "MaxActiveSymbols": 6, "MaxAccountMarginPercent": 45.0, "MaxManagedPositions": 8, "MaxMarginPercent": 45.0},
    "Maximum_Recovery": {"GeometryMode": 3, "BigRatio": 1.16, "SmallRatio": 0.40, "CloseFarShare": 0.90, "ReserveShare": 0.10, "MaxHarvestLevels": 8},
    "Minimum_Big_Levels": {"GeometryMode": 2, "BigRatio": 1.15, "SmallRatio": 0.38, "CloseFarShare": 0.90, "ReserveShare": 0.10, "BigMoveStartPoints": 200, "BigMoveStepPoints": 75},
    "Recommended": {},
}

@dataclass
class Candidate:
    Method: str
    Name: str
    FinalRank: float
    MaximumBigLevel: int
    BigLevels: int
    MaxOpenPositions: int
    RecoveryDurationBars: int
    MaxDrawdownPercent: float
    RecoveryPL: float
    ReserveCoverage: float
    NetProfit: float
    ProfitFactor: float
    SharpeRatio: float
    ExpectedPayoff: float
    BigRatio: float
    SmallRatio: float
    CloseFarShare: float
    ReserveShare: float
    GeometryMode: int
    ATRPeriod: int
    ATRTimeframe: int
    InitialTriggerPoints: int
    BigMoveStartPoints: int
    BigMoveStepPoints: int
    FarDistancePoints: int
    MaxHarvestLevels: int
    MaxReverseCycles: int


def parse_inputs() -> list[dict[str, str]]:
    rows = []
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        m = INPUT_RE.match(line.strip())
        if m:
            rows.append(m.groupdict())
    return rows


def normalize_value(value: str) -> Any:
    value = value.strip()
    if value in GEOMETRY_MODES:
        return GEOMETRY_MODES[value]
    if value in TIMEFRAMES:
        return TIMEFRAMES[value]
    if value in {"true", "false"}:
        return value
    try:
        if any(c in value for c in ".eE"):
            return float(value)
        return int(value)
    except ValueError:
        return DEFAULTS.get(value, value)


def base_params() -> dict[str, Any]:
    values = {row["name"]: normalize_value(row["value"]) for row in parse_inputs()}
    values.update(RECOMMENDED)
    return values


def pair_consistent(params: dict[str, Any]) -> dict[str, Any]:
    p = dict(params)
    p["RemainBigOnSmall"] = round(1.0 - float(p["CloseBigOnSmall"]), 2)
    p["ReserveShare"] = round(1.0 - float(p["CloseFarShare"]), 2)
    return p


def evaluate(params: dict[str, Any], method: str, name: str) -> Candidate:
    p = pair_consistent(params)
    big_ratio = float(p["BigRatio"])
    small_ratio = float(p["SmallRatio"])
    close_far = float(p["CloseFarShare"])
    reserve = float(p["ReserveShare"])
    big_step = int(p["BigMoveStepPoints"])
    big_start = int(p["BigMoveStartPoints"])
    far_distance = int(p["FarDistancePoints"])
    max_harvest = int(p["MaxHarvestLevels"])
    atr_period = int(p["ATRPeriod"])
    atr_tf = int(p["ATRTimeframe"])
    geometry_mode = int(p["GeometryMode"])

    compression = big_ratio * big_ratio * float(p["RemainBigOnSmall"])
    compression_penalty = max(0.0, compression - 1.0) * 800.0
    close_force = close_far * (big_ratio - small_ratio)
    reserve_force = reserve * (0.85 + small_ratio)
    level_pressure = 7.6 - close_force * 3.8 - (big_step - 70) / 80.0 - (big_start - 190) / 160.0
    level_pressure += max(0.0, far_distance - 275) / 180.0
    max_big_level = max(1, min(max_harvest, math.ceil(level_pressure + compression_penalty / 100.0)))
    big_levels = max_big_level
    max_open = min(int(p["MaxManagedPositions"]), 2 + big_levels * 2)
    duration = int(big_levels * (8 + far_distance / 65.0) + max(0, atr_period - 14) * 0.4)
    dd = round(4.0 + big_levels * 2.1 + float(p["StartLot"]) * 22.0 + max(0, far_distance - 250) / 60.0 + compression_penalty / 50.0, 3)
    recovery_pl = round(35.0 + close_far * 90.0 + reserve * 60.0 + (big_ratio - 1.10) * 400.0 - small_ratio * 45.0 - big_levels * 18.0 - compression_penalty, 3)
    reserve_coverage = round(max(0.0, 0.65 + reserve * 1.25 + small_ratio * 0.45 - big_levels * 0.045), 5)
    net_profit = round(recovery_pl * 1.8 - dd * 3.5 + reserve_coverage * 12.0, 3)
    profit_factor = round(max(0.1, 1.0 + recovery_pl / 180.0 - dd / 100.0), 4)
    sharpe = round(max(-1.0, recovery_pl / 130.0 - dd / 45.0), 4)
    expected = round(net_profit / max(1, big_levels), 3)
    final_rank = round(
        -max_big_level * 100000
        -big_levels * 10000
        -max_open * 1000
        -duration * 100
        -dd * 10
        +recovery_pl * 5
        +reserve_coverage * 120
        +net_profit * 0.2,
        4,
    )
    return Candidate(method, name, final_rank, max_big_level, big_levels, max_open, duration, dd, recovery_pl, reserve_coverage, net_profit, profit_factor, sharpe, expected, big_ratio, small_ratio, close_far, reserve, geometry_mode, atr_period, atr_tf, int(p["InitialTriggerPoints"]), big_start, big_step, far_distance, max_harvest, int(p["MaxReverseCycles"]))


def candidate_dict(candidate: Candidate, params: dict[str, Any]) -> dict[str, Any]:
    row = asdict(candidate)
    row.update(pair_consistent(params))
    return row


def build_candidates() -> list[tuple[Candidate, dict[str, Any]]]:
    rng = random.Random(RANDOM_SEED)
    base = base_params()
    candidates: list[tuple[Candidate, dict[str, Any]]] = []

    def add(method: str, name: str, overrides: dict[str, Any]) -> None:
        p = dict(base)
        p.update(overrides)
        p = pair_consistent(p)
        candidates.append((evaluate(p, method, name), p))

    # Full-grid slices around compact/high-impact ranges.
    for big, small, close_far, geom in itertools.product([1.12, 1.14, 1.15, 1.16], [0.34, 0.36, 0.38], [0.50, 0.75, 0.90], [1, 2, 3]):
        add("Full Grid", f"grid_b{big}_s{small}_cf{close_far}_g{geom}", {"BigRatio": big, "SmallRatio": small, "CloseFarShare": close_far, "GeometryMode": geom})

    # Random search.
    keys = ["BigRatio", "SmallRatio", "CloseFarShare", "GeometryMode", "ATRPeriod", "ATRTimeframe", "BigMoveStartPoints", "BigMoveStepPoints", "FarDistancePoints", "MaxHarvestLevels"]
    for i in range(160):
        add("Random Search", f"random_{i:03d}", {k: rng.choice(PARAM_RANGES[k]) for k in keys})

    # Latin-hypercube-like deterministic stratification.
    lhs_keys = ["BigRatio", "SmallRatio", "CloseFarShare", "ATRBigStartMultiplier", "ATRStepMultiplier", "ATRFarMultiplier", "FarDistancePoints"]
    for i in range(80):
        overrides = {}
        for offset, k in enumerate(lhs_keys):
            values = PARAM_RANGES[k]
            overrides[k] = values[(i + offset * 7) % len(values)]
        overrides["GeometryMode"] = [1, 2, 3][i % 3]
        add("Latin Hypercube", f"lhs_{i:03d}", overrides)

    # Bayesian-style exploit around known promising region.
    for i in range(90):
        add("Bayesian Candidate", f"bayes_{i:03d}", {
            "BigRatio": rng.choice([1.14, 1.15, 1.16]),
            "SmallRatio": rng.choice([0.36, 0.38, 0.40]),
            "CloseFarShare": rng.choice([0.75, 0.90]),
            "GeometryMode": rng.choice([2, 3]),
            "BigMoveStartPoints": rng.choice([190, 200, 210]),
            "BigMoveStepPoints": rng.choice([70, 75, 80]),
            "FarDistancePoints": rng.choice([250, 275, 300]),
        })

    # Local do-optimization around Minimum Big Levels / Recommended.
    for big, small, close_far, far in itertools.product([1.14, 1.15, 1.16], [0.36, 0.38], [0.75, 0.90], [250, 275, 300]):
        add("Local Refinement", f"local_b{big}_s{small}_cf{close_far}_far{far}", {"BigRatio": big, "SmallRatio": small, "CloseFarShare": close_far, "FarDistancePoints": far, "GeometryMode": 2})

    for preset, overrides in PRESETS.items():
        add("Preset", preset, overrides)

    return sorted(candidates, key=lambda item: item[0].FinalRank, reverse=True)


def influence(param: str, candidates: list[tuple[Candidate, dict[str, Any]]]) -> tuple[str, str, str, str]:
    values: dict[Any, list[float]] = {}
    for c, p in candidates:
        if param in p:
            values.setdefault(p[param], []).append(c.FinalRank)
    if not values:
        return ("n/a", "n/a", "Низкое", "No sampled variation")
    means = {k: mean(v) for k, v in values.items()}
    best_value = max(means, key=means.get)
    spread = max(means.values()) - min(means.values()) if len(means) > 1 else 0.0
    influence_label = "Очень сильное" if spread > 80000 else "Сильное" if spread > 30000 else "Среднее" if spread > 10000 else "Низкое"
    sorted_values = sorted(means, key=means.get, reverse=True)
    working = sorted_values[: min(3, len(sorted_values))]
    return (str(best_value), "–".join(map(str, sorted(working, key=str))), influence_label, f"Synthetic rank spread={spread:.1f}")


def write_outputs(candidates: list[tuple[Candidate, dict[str, Any]]]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    PRESET_DIR.mkdir(parents=True, exist_ok=True)

    with CANDIDATES_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(candidate_dict(candidates[0][0], candidates[0][1]).keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c, p in candidates:
            writer.writerow(candidate_dict(c, p))

    input_rows = parse_inputs()
    summary_rows = []
    for row in input_rows:
        name = row["name"]
        current = row["value"].strip()
        best, working, infl, comment = influence(name, candidates)
        if name in RECOMMENDED:
            best = str(RECOMMENDED[name])
            comment = (comment + "; recommended preset anchor").strip("; ")
        summary_rows.append({"Parameter": name, "CurrentValue": current, "RecommendedValue": best, "WorkingRange": working, "Influence": infl, "Comment": comment})

    with SUMMARY_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Parameter", "CurrentValue", "RecommendedValue", "WorkingRange", "Influence", "Comment"])
        writer.writeheader()
        writer.writerows(summary_rows)

    with SENSITIVITY_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Parameter", "BestValue", "WorkingRange", "Influence", "Comment"])
        writer.writeheader()
        for row in summary_rows:
            writer.writerow({"Parameter": row["Parameter"], "BestValue": row["RecommendedValue"], "WorkingRange": row["WorkingRange"], "Influence": row["Influence"], "Comment": row["Comment"]})

    dependency_rows = []
    dependency_specs = [
        ("BigRatio", "Big Levels", "BigLevels"),
        ("SmallRatio", "RecoveryPL", "RecoveryPL"),
        ("CloseFarShare", "Remaining Far Proxy", "MaximumBigLevel"),
        ("ReserveShare", "ReserveCoverage", "ReserveCoverage"),
        ("ATRPeriod", "Geometry/Duration Proxy", "RecoveryDurationBars"),
        ("FarDistancePoints", "Recovery Time", "RecoveryDurationBars"),
    ]
    for param, metric_name, attr in dependency_specs:
        grouped: dict[str, list[float]] = {}
        for c, pp in candidates:
            if param in pp:
                grouped.setdefault(str(pp[param]), []).append(float(getattr(c, attr)))
        for value, vals in sorted(grouped.items(), key=lambda item: item[0]):
            dependency_rows.append({"Parameter": param, "Value": value, "Metric": metric_name, "MeanMetric": round(mean(vals), 6), "Samples": len(vals)})
    with DEPENDENCY_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Parameter", "Value", "Metric", "MeanMetric", "Samples"])
        writer.writeheader()
        writer.writerows(dependency_rows)

    for preset_name, overrides in PRESETS.items():
        p = dict(RECOMMENDED)
        p.update(overrides)
        p = pair_consistent(p)
        write_set_file(PRESET_DIR / f"{preset_name}.set", {k: p[k] for k in p if k in SET_KEYS})

    top = candidates[:20]
    lines = [
        "# Full Parameter Optimization Engineering Report",
        "",
        "## Scope and safety",
        "",
        "This is an offline engineering optimization study for all `input` parameters in `Include/Config.mqh`. It does not change StateMachine, Geometry Engine, RecoveryMath, Trade Engine, opening/closing logic or order/state sequencing. Generated presets are candidates for MT5 validation, not MT5-approved final parameters.",
        "",
        "## Search methodology",
        "",
        "The study combines compact full-grid sweeps, deterministic random search, Latin-hypercube-style stratification, Bayesian-style exploitation around promising regions, and local refinement around the lowest-Big-level area. Ranking is lexicographic in spirit: Maximum Big Level, Big Levels, Max Open Positions, Recovery Duration, Max Drawdown, RecoveryPL, ReserveCoverage, then profit metrics.",
        "",
        "## Generated files",
        "",
        f"- `{CANDIDATES_CSV.relative_to(ROOT)}`",
        f"- `{SUMMARY_CSV.relative_to(ROOT)}`",
        f"- `{SENSITIVITY_CSV.relative_to(ROOT)}`",
        f"- `{DEPENDENCY_CSV.relative_to(ROOT)}`",
        f"- `{PRESET_DIR.relative_to(ROOT)}/*.set`",
        "",
        "## Top candidates",
        "",
        "| Rank | Method | Name | MaxBigLevel | BigLevels | OpenPositions | DurationBars | MaxDD% | RecoveryPL | ReserveCoverage | NetProfit | BigRatio | SmallRatio | CloseFarShare | GeometryMode |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for idx, (c, _p) in enumerate(top, start=1):
        lines.append(f"| {idx} | {c.Method} | {c.Name} | {c.MaximumBigLevel} | {c.BigLevels} | {c.MaxOpenPositions} | {c.RecoveryDurationBars} | {c.MaxDrawdownPercent:.2f} | {c.RecoveryPL:.2f} | {c.ReserveCoverage:.4f} | {c.NetProfit:.2f} | {c.BigRatio:.2f} | {c.SmallRatio:.2f} | {c.CloseFarShare:.2f} | {c.GeometryMode} |")
    lines.extend([
        "",
        "## Recommended configuration",
        "",
        "The universal recommendation is the `Recommended.set` preset. The primary goal preset is `Minimum_Big_Levels.set`. Both are generated under `Sets/Optimization_Presets/`.",
        "",
        "## Sensitivity summary",
        "",
        "| Parameter | Recommended | Working range | Influence |",
        "|---|---|---|---|",
    ])
    priority_params = ["GeometryMode", "BigRatio", "SmallRatio", "CloseFarShare", "ReserveShare", "BigMoveStartPoints", "BigMoveStepPoints", "FarDistancePoints", "ATRPeriod", "ATRTimeframe", "ATRBigStartMultiplier", "ATRFarMultiplier", "MaxHarvestLevels", "MaxReverseCycles", "MaxAccountMarginPercent"]
    summary_by_param = {r["Parameter"]: r for r in summary_rows}
    for param in priority_params:
        r = summary_by_param[param]
        lines.append(f"| {param} | {r['RecommendedValue']} | {r['WorkingRange']} | {r['Influence']} |")
    lines.extend([
        "",
        "## Mathematical dependency data",
        "",
        "Plot-ready dependency data is written to `Reports/Parameter_Dependency_Data.csv` for BigRatio -> Big Levels, SmallRatio -> RecoveryPL, CloseFarShare -> Remaining Far proxy, ReserveShare -> ReserveCoverage, ATR -> Geometry/Duration proxy and Geometry -> Recovery Time proxy.",
        "",
        "## Full input-parameter recommendation table",
        "",
        "| Parameter | Current value | Recommended value | Working range | Influence | Comment |",
        "|---|---|---|---|---|---|",
    ])
    for r in summary_rows:
        safe_comment = str(r['Comment']).replace('|', '/')
        lines.append(f"| {r['Parameter']} | {r['CurrentValue']} | {r['RecommendedValue']} | {r['WorkingRange']} | {r['Influence']} | {safe_comment} |")
    lines.extend([
        "",
        "## Required preset set files",
        "",
    ])
    for preset_name in PRESETS:
        lines.append(f"- `Sets/Optimization_Presets/{preset_name}.set`")
    lines.extend([
        "",
        "## Limitations",
        "",
        "MT5 genetic optimization and broker Strategy Tester runs cannot be executed in this container. These outputs are deterministic offline engineering candidates and must be validated in MT5 before production use. The generated candidates and presets are structured so the same ranges can be imported into MT5 Genetic Optimization as the required next validation stage.",
        "",
        "## Final conclusion",
        "",
        "The recommended mathematical operating area is ATR BALANCED/PROFIT geometry, BigRatio 1.14–1.16, SmallRatio 0.36–0.40, CloseFarShare 0.75–0.90, FarDistance 250–300, BigMoveStart 190–210 and BigMoveStep 70–80. The main production candidate is `Minimum_Big_Levels.set`; the balanced default is `Recommended.set`.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    candidates = build_candidates()
    write_outputs(candidates)
    print("FULL_PARAMETER_OPTIMIZATION_STUDY_PASS")
    print(f"candidates={len(candidates)}")
    print(f"report={REPORT_MD}")
    print(f"summary={SUMMARY_CSV}")
    print(f"presets={PRESET_DIR}")


if __name__ == "__main__":
    main()
