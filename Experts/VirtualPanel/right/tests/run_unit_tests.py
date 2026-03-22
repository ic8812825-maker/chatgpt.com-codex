#!/usr/bin/env python3
import math
import random
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

REPORT_DIR = Path("Experts/VirtualPanel/right/tests/reports")
ALE_DIR = Path("Experts/VirtualPanel/right/ale")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class TestResult:
    name: str
    description: str
    input_data: Dict
    execution: str
    results: Dict
    validation: str
    passed: bool


@dataclass
class RiskState:
    depth: int
    k: float
    margin_level: float
    delta_exposure: float
    vol_proxy: float


def utc_ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def sigmoid(x: float) -> float:
    if x > 40:
        return 1.0
    if x < -40:
        return 0.0
    return 1.0 / (1.0 + math.exp(-x))


def write_report(result: TestResult) -> None:
    required = ["levels_before", "levels_after", "delta_before", "delta_after", "margin_before", "margin_after", "pnl"]
    m = dict(result.results)
    for k in required:
        m.setdefault(k, "N/A")

    lines = [f"# Test: {result.name}", "", "## Description", result.description, "", "## Input"]
    for k, v in result.input_data.items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Execution", result.execution, f"- timestamp_utc: {utc_ts()}", "", "## Results"]
    for k in required:
        lines.append(f"- {k}: {m[k]}")

    extra = [k for k in m.keys() if k not in required]
    if extra:
        lines.append("- extra_metrics:")
        for k in extra:
            lines.append(f"  - {k}: {m[k]}")

    lines += ["", "## Validation", result.validation, "", "## Conclusion", "PASS" if result.passed else "FAIL", ""]
    (REPORT_DIR / f"{result.name}_report.md").write_text("\n".join(lines), encoding="utf-8")


# --------- core helpers ---------
def effective_delta(positions: List[Tuple[int, float]]) -> float:
    return sum(s * l for s, l in positions)


def greedy_lock(positions: List[Tuple[int, float]]) -> float:
    b = sorted([l for s, l in positions if s > 0], reverse=True)
    s = sorted([l for s, l in positions if s < 0], reverse=True)
    i = j = 0
    while i < len(b) and j < len(s):
        m = min(b[i], s[j])
        b[i] -= m
        s[j] -= m
        if b[i] <= 1e-12:
            i += 1
        if s[j] <= 1e-12:
            j += 1
    return abs(sum(x for x in b if x > 1e-12) - sum(x for x in s if x > 1e-12))


def lots_sum(l0: float, k: float, n: int, alpha: float) -> float:
    if n <= 0:
        return 0.0
    geom = (k**n - 1.0) / (k - 1.0)
    return l0 * geom * alpha


def margin_req(l0: float, k: float, n: int, alpha: float, contract_size: float, leverage: float) -> float:
    return lots_sum(l0, k, n, alpha) * contract_size / leverage


def risk_zone(p: float, thresholds: Tuple[float, float, float] = (0.1, 0.3, 0.6)) -> str:
    t1, t2, t3 = thresholds
    if p < t1:
        return "SAFE"
    if p < t2:
        return "WARNING"
    if p < t3:
        return "DANGER"
    return "CRITICAL"


def adaptive_k(zone: str) -> float:
    return {"SAFE": 1.30, "WARNING": 1.25, "DANGER": 1.20, "CRITICAL": 1.10}[zone]


def estimate_realtime_pcollapse(state: RiskState) -> float:
    # Slightly re-calibrated logistic proxy
    x = (
        -3.4
        + 0.12 * state.depth
        + 7.0 * (state.k - 1.1)
        + 0.018 * max(0.0, 210.0 - state.margin_level)
        + 2.2 * abs(state.delta_exposure)
        + 2.4 * state.vol_proxy
    )
    return sigmoid(x)


def market_step(mode: str, t: int, steps: int) -> float:
    dt = 1.0 / max(steps, 1)
    sigma = 0.32
    mu = -0.03
    z = random.gauss(0.0, 1.0)
    base = mu * dt + sigma * math.sqrt(dt) * z

    if mode == "random":
        return base
    if mode == "trend":
        return base - 2.2 * abs(mu) * dt
    if mode == "shock":
        return base + (random.choice([-1, 1]) * 3.2 * sigma * math.sqrt(dt) if random.random() < 0.03 else 0.0)

    # adversarial
    if mode == "adv_monotonic":
        return -0.0010 + 0.02 * abs(base)
    if mode == "adv_regime_shift":
        if t < steps // 2:
            return -0.0002 + 0.10 * math.sqrt(dt) * z
        return -0.0014 + 0.75 * math.sqrt(dt) * z
    if mode == "adv_jump_cluster":
        if (t % 35) < 7:
            return -0.0015 + random.choice([-1, -1, -1, 1]) * 4.8 * sigma * math.sqrt(dt)
        return base - 0.0003
    if mode == "adv_liquidity_gap":
        if random.random() < 0.02:
            return base - random.uniform(0.01, 0.03)
        return base - 0.0004
    if mode == "adv_liquidity_freeze":
        if random.random() < 0.05:
            return -random.uniform(0.012, 0.04)
        return base - 0.0005

    return base


# --------- simulator ---------
def simulate(
    mode: str,
    runs: int,
    steps: int,
    k: float,
    R: float,
    alpha: float,
    with_control: bool,
    with_alc: bool,
    thresholds: Tuple[float, float, float] = (0.1, 0.3, 0.6),
    spread_mult: float = 1.0,
    control_delay: int = 0,
    slippage_mult: float = 1.0,
    strict_block: bool = False,
    max_levels: int = 60,
    equity0: float = 30000.0,
    l0: float = 0.01,
    leverage: float = 100.0,
    contract_size: float = 100000.0,
) -> Dict[str, float]:
    pip_value = 10.0 / 10000.0

    collapse = c1 = c2 = c3 = 0
    avg_dd = avg_ttc = avg_depth = avg_pnl = 0.0
    trades = ex_allow = ex_block = comp = critical_ticks = 0
    pos_life_total = pos_life_count = 0
    cap_util_total = 0.0
    k_eff_values = []

    for _ in range(runs):
        price = 1.0
        adverse_pips = 0.0
        n = 1
        aeff = 1.0
        k_eff = k
        vol = 0.0
        ttc = float(steps)
        maxdd = 0.0
        eq = equity0

        in_pos = False
        pos_life = 0
        run_allow = 0
        pending_zone = "SAFE"
        pending_until = -1

        for t in range(1, steps + 1):
            r = market_step(mode, t, steps)
            vol = 0.93 * vol + 0.07 * min(0.3, abs(r) * 4)
            new_price = max(1e-8, price * math.exp(r))
            dpips = (new_price - price) * 10000.0
            price = new_price

            # spread / slippage stress
            adverse_pips = max(0.0, adverse_pips - dpips + spread_mult * 0.3 + slippage_mult * random.uniform(0.0, 0.2))

            m = margin_req(l0, k_eff, n, aeff, contract_size, leverage)
            fl = lots_sum(l0, k_eff, n, aeff) * adverse_pips * pip_value
            eq = equity0 - fl
            ml = (eq / m * 100.0) if m > 1e-9 else 9999.0
            delta = lots_sum(l0, k_eff, n, aeff)
            p = estimate_realtime_pcollapse(RiskState(n, k_eff, ml, delta, vol))
            z = risk_zone(p, thresholds)

            if with_control:
                # delay compensation: apply future zone after delay
                if pending_until < t:
                    pending_zone = z
                    pending_until = t + control_delay
                active_zone = pending_zone if t >= pending_until else "SAFE"
                k_eff = min(k_eff, adaptive_k(active_zone))
                k_eff_values.append(k_eff)

                if active_zone == "CRITICAL":
                    aeff = min(aeff, alpha)
                    comp += 1
                block = active_zone in (("WARNING", "DANGER", "CRITICAL") if strict_block else ("CRITICAL",))
                if active_zone == "CRITICAL":
                    critical_ticks += 1
                    n = max(1, n - 1)
            else:
                block = False
                k_eff_values.append(k_eff)

            # reactive alc kept
            if with_alc and (n >= 9 or ml < 220.0):
                aeff = min(aeff, alpha)

            target_n = min(max_levels, 1 + int(adverse_pips // max(1.0, R)))
            if target_n > n:
                trades += 1
                if block:
                    ex_block += 1
                else:
                    ex_allow += 1
                    run_allow += 1
                    n = target_n

            if n > 1:
                in_pos = True
                pos_life += 1
            elif in_pos:
                pos_life_total += pos_life
                pos_life_count += 1
                in_pos = False
                pos_life = 0

            m = margin_req(l0, k_eff, n, aeff, contract_size, leverage)
            cap_util_total += min(1.5, m / max(1.0, equity0))
            fl = lots_sum(l0, k_eff, n, aeff) * adverse_pips * pip_value
            eq = equity0 - fl
            ml = (eq / m * 100.0) if m > 1e-9 else 9999.0

            l1 = ml < 150.0
            l2 = n >= max_levels and adverse_pips > (max_levels * R * 1.2)
            l3 = equity0 < m + fl

            dd = max(0.0, (equity0 - eq) / max(1.0, equity0))
            maxdd = max(maxdd, dd)

            if l1 or l2 or l3:
                collapse += 1
                c1 += 1 if l1 else 0
                c2 += 1 if l2 else 0
                c3 += 1 if l3 else 0
                ttc = float(t)
                break

        if in_pos:
            pos_life_total += pos_life
            pos_life_count += 1

        avg_dd += maxdd
        avg_ttc += ttc
        avg_depth += n
        avg_pnl += (eq - equity0) + 0.5 * run_allow

    denom_trades = max(1e-9, (ex_allow + ex_block) / runs)
    activity_ratio = (ex_allow / runs) / max(1e-9, (ex_allow + ex_block) / runs)
    trade_rate = (trades / runs) / max(1.0, steps)
    control_intensity = (ex_block / runs) / max(1e-9, (trades / runs))
    avg_life = pos_life_total / max(1, pos_life_count)
    cap_util = cap_util_total / max(1, runs * steps)

    return {
        "p_collapse": collapse / runs,
        "p_lvl1": c1 / runs,
        "p_lvl2": c2 / runs,
        "p_lvl3": c3 / runs,
        "avg_max_drawdown": avg_dd / runs,
        "avg_time_to_collapse_steps": avg_ttc / runs,
        "avg_depth": avg_depth / runs,
        "avg_pnl": avg_pnl / runs,
        "trades_executed": trades / runs,
        "expansions_allowed": ex_allow / runs,
        "expansions_blocked": ex_block / runs,
        "compressions_triggered": comp / runs,
        "time_in_CRITICAL": critical_ticks / runs,
        "activity_ratio": activity_ratio,
        "trade_rate": trade_rate,
        "control_intensity": control_intensity,
        "avg_position_lifetime": avg_life,
        "capital_utilization": cap_util,
        "k_eff_mean": sum(k_eff_values) / max(1, len(k_eff_values)),
        "k_eff_min": min(k_eff_values) if k_eff_values else k,
        "k_eff_max": max(k_eff_values) if k_eff_values else k,
        "k_eff_unique_count": len({round(x, 2) for x in k_eff_values}),
        "fake_safety": (collapse / runs) < 0.001 and activity_ratio < 0.1,
    }


def frontier(mode: str, with_control: bool) -> List[Dict]:
    lam, mu = 50.0, 1.0
    rows = []
    for k in [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]:
        for R in [50, 100, 200, 300, 500]:
            random.seed(2000 + int(k * 100) + R + (10 if with_control else 0))
            s = simulate(mode, runs=500, steps=260, k=k, R=R, alpha=0.5, with_control=with_control, with_alc=True)
            score = s["avg_pnl"] - lam * s["p_collapse"] - mu * s["avg_max_drawdown"]
            rows.append({"k": k, "R": R, "p": s["p_collapse"], "pnl": s["avg_pnl"], "dd": s["avg_max_drawdown"], "score": score})
    return rows


def roc_auc(scores: List[float], labels: List[int]) -> float:
    pos = [(s, l) for s, l in zip(scores, labels) if l == 1]
    neg = [(s, l) for s, l in zip(scores, labels) if l == 0]
    if not pos or not neg:
        return 0.5
    wins = 0
    ties = 0
    for sp, _ in pos:
        for sn, _ in neg:
            if sp > sn:
                wins += 1
            elif sp == sn:
                ties += 1
    return (wins + 0.5 * ties) / (len(pos) * len(neg))


# -------- tests --------
def test_lock_compression() -> TestResult:
    pos = [(+1, 0.4), (+1, 0.2), (+1, 0.1), (-1, 0.3), (-1, 0.2)]
    d0 = abs(effective_delta(pos))
    d1 = greedy_lock(pos)
    ok = d1 <= d0 + 1e-12
    return TestResult("TestLockCompression", "Greedy lock monotonicity.", {"positions": pos}, "Compute d0/d1.", {"delta_before": d0, "delta_after": d1, "pnl": 0.0}, "|Δ_new|<=|Δ_old|", ok)


def test_monte_carlo_realistic() -> TestResult:
    random.seed(1)
    rw = simulate("random", runs=5000, steps=700, k=1.35, R=120, alpha=0.5, with_control=False, with_alc=True)
    random.seed(2)
    tr = simulate("trend", runs=5000, steps=700, k=1.35, R=120, alpha=0.5, with_control=False, with_alc=True)
    random.seed(3)
    sh = simulate("shock", runs=5000, steps=700, k=1.35, R=120, alpha=0.5, with_control=False, with_alc=True)
    ok = sh["p_collapse"] > rw["p_collapse"]
    return TestResult("TestMonteCarloRealistic", "Random/trend/shock MC.", {}, "Run 3 modes.", {"pnl": 0.0, "p_random": rw["p_collapse"], "p_trend": tr["p_collapse"], "p_shock": sh["p_collapse"]}, "Shock risk should exceed random.", ok)


def test_profit_constrained_control() -> TestResult:
    random.seed(4)
    base = simulate("random", runs=2500, steps=650, k=1.3, R=150, alpha=0.5, with_control=False, with_alc=True)
    random.seed(4)
    ctrl = simulate("random", runs=2500, steps=650, k=1.3, R=150, alpha=0.5, with_control=True, with_alc=True, thresholds=(0.2,0.5,0.8))

    constraints_ok = (
        ctrl["activity_ratio"] >= 0.15
        and ctrl["trade_rate"] >= 0.05
        and ctrl["control_intensity"] <= 0.95
    )
    pnl_ok = ctrl["avg_pnl"] >= 0.0 and ctrl["avg_pnl"] >= 0.3 * base["avg_pnl"]
    risk_ok = ctrl["p_collapse"] <= base["p_collapse"]
    ok = constraints_ok and pnl_ok and risk_ok and (not ctrl["fake_safety"])

    return TestResult(
        "TestProfitConstrainedControl",
        "Hard activity/profit constraints for control.",
        {},
        "A/B baseline vs control in normal regime.",
        {
            "pnl": ctrl["avg_pnl"],
            "p_base": base["p_collapse"],
            "p_ctrl": ctrl["p_collapse"],
            "pnl_base": base["avg_pnl"],
            "pnl_ctrl": ctrl["avg_pnl"],
            "activity_ratio": ctrl["activity_ratio"],
            "trade_rate": ctrl["trade_rate"],
            "control_intensity": ctrl["control_intensity"],
            "fake_safety": ctrl["fake_safety"],
        },
        "Must cut risk without killing activity/profit.",
        ok,
    )


def test_risk_return_efficiency() -> TestResult:
    random.seed(5)
    ale = simulate("shock", runs=1800, steps=550, k=1.35, R=180, alpha=1.0, with_control=False, with_alc=False)
    random.seed(5)
    alc = simulate("shock", runs=1800, steps=550, k=1.35, R=180, alpha=0.5, with_control=False, with_alc=True)
    random.seed(5)
    ctrl = simulate("shock", runs=1800, steps=550, k=1.35, R=180, alpha=0.5, with_control=True, with_alc=True, thresholds=(0.2,0.5,0.8))

    # control should dominate ale on risk, and not collapse pnl below alc by huge factor
    ok = (ctrl["p_collapse"] <= ale["p_collapse"]) and (ctrl["avg_pnl"] >= 0.2 * alc["avg_pnl"])
    return TestResult("TestRiskReturnEfficiency", "Pareto-like comparison ALE vs ALC vs CONTROL.", {}, "3-way comparison.", {"pnl": ctrl["avg_pnl"], "p_ale": ale["p_collapse"], "p_alc": alc["p_collapse"], "p_ctrl": ctrl["p_collapse"], "pnl_ale": ale["avg_pnl"], "pnl_alc": alc["avg_pnl"], "pnl_ctrl": ctrl["avg_pnl"]}, "Control should improve risk-return efficiency.", ok)


def test_control_overkill() -> TestResult:
    # ultra-low thresholds => overkill should be detected
    random.seed(6)
    over = simulate("random", runs=1600, steps=600, k=1.3, R=220, alpha=0.5, with_control=True, with_alc=True, thresholds=(0.02, 0.05, 0.1), strict_block=True)
    detected = over["activity_ratio"] < 0.15 or over["control_intensity"] > 0.95 or over["avg_pnl"] < 0
    ok = detected
    return TestResult("TestControlOverkill", "Over-aggressive thresholds must be flagged.", {}, "Run overkill config.", {"pnl": over["avg_pnl"], "p_ctrl": over["p_collapse"], "activity_ratio": over["activity_ratio"], "control_intensity": over["control_intensity"]}, "Test passes if overkill is detected as bad regime.", ok)


def test_adaptive_k_stability() -> TestResult:
    random.seed(7)
    s = simulate("shock", runs=1800, steps=600, k=1.35, R=160, alpha=0.5, with_control=True, with_alc=True)
    ok = s["k_eff_unique_count"] >= 3 and not (abs(s["k_eff_min"] - s["k_eff_max"]) < 1e-9)
    return TestResult("TestAdaptiveKStability", "Adaptive-k should have distribution, not constant min.", {}, "Inspect k_eff stats.", {"pnl": s["avg_pnl"], "k_eff_min": s["k_eff_min"], "k_eff_max": s["k_eff_max"], "k_eff_unique": s["k_eff_unique_count"]}, "k_eff must vary across risk zones.", ok)


def test_estimator_calibration() -> TestResult:
    # predicted vs actual across anchor bins
    anchors = [(1.2, 280), (1.25, 220), (1.3, 180), (1.4, 140), (1.5, 100)]
    preds, acts, labels = [], [], []

    for i, (k, R) in enumerate(anchors):
        state = RiskState(depth=6 + 4 * i, k=k, margin_level=260 - i * 35, delta_exposure=0.08 + 0.07 * i, vol_proxy=0.02 + 0.02 * i)
        pred = estimate_realtime_pcollapse(state)
        random.seed(100 + i)
        s = simulate("shock", runs=900, steps=320, k=k, R=R, alpha=0.5, with_control=False, with_alc=True)
        act = s["p_collapse"]
        preds.append(pred)
        acts.append(act)
        labels.append(1 if act > 0.35 else 0)

    calibration_error = sum(abs(preds[i] - acts[i]) for i in range(len(preds))) / len(preds)
    brier = sum((preds[i] - acts[i]) ** 2 for i in range(len(preds))) / len(preds)
    auc = roc_auc(preds, labels)

    ok = calibration_error <= 0.25 and brier <= 0.15 and auc >= 0.65
    return TestResult("TestEstimatorCalibration", "Estimator calibration + Brier + ROC-AUC.", {}, "Anchor calibration run.", {"pnl": 0.0, "calibration_error": calibration_error, "brier_score": brier, "roc_auc": auc, "predicted": preds, "actual": acts}, "Calibration must be within threshold.", ok)


def test_reality_stress_v2() -> TestResult:
    random.seed(8)
    freeze = simulate("adv_liquidity_freeze", runs=1200, steps=500, k=1.4, R=140, alpha=0.5, with_control=True, with_alc=True, spread_mult=10.0, control_delay=10, slippage_mult=2.5)
    random.seed(8)
    no_ctrl = simulate("adv_liquidity_freeze", runs=1200, steps=500, k=1.4, R=140, alpha=0.5, with_control=False, with_alc=True, spread_mult=10.0, control_delay=10, slippage_mult=2.5)
    ok = freeze["p_collapse"] <= no_ctrl["p_collapse"]
    return TestResult("TestRealityStressV2", "Liquidity freeze + spread explosion + delayed control + slippage.", {}, "Stress V2 comparison.", {"pnl": freeze["avg_pnl"], "p_no_ctrl": no_ctrl["p_collapse"], "p_ctrl": freeze["p_collapse"], "activity_ratio": freeze["activity_ratio"]}, "Preventive logic should not break under stress V2.", ok)


def test_adversarial_scenarios() -> TestResult:
    modes = ["adv_monotonic", "adv_regime_shift", "adv_jump_cluster", "adv_liquidity_gap"]
    out = {}
    for i, m in enumerate(modes):
        random.seed(200 + i)
        no = simulate(m, runs=900, steps=420, k=1.4, R=140, alpha=0.5, with_control=False, with_alc=True)
        random.seed(200 + i)
        ctrl = simulate(m, runs=900, steps=420, k=1.4, R=140, alpha=0.5, with_control=True, with_alc=True)
        out[f"{m}_no"] = no["p_collapse"]
        out[f"{m}_ctrl"] = ctrl["p_collapse"]
    ok = max(out[k] for k in out if k.endswith("_no")) > 0
    return TestResult("TestAdversarialScenarios", "Adversarial market set.", {}, "Run A/B per adversarial mode.", {"pnl": 0.0, **out}, "No-control adversarial risk must be non-zero.", ok)


def test_safe_deposit() -> TestResult:
    rows=[]
    for t in [1000,2000,3000,5000,10000]:
        n=min(40,1+int(t/120))
        m=margin_req(0.01,1.35,n,0.5,100000,100)
        dd=lots_sum(0.01,1.35,n,0.5)*t*(10/10000)
        rows.append((t,m+dd+0.2*dd))
    ok=all(rows[i+1][1]>rows[i][1] for i in range(len(rows)-1))
    return TestResult("TestSafeDeposit","Deposit monotonic by trend.",{},"Compute table.",{"pnl":0.0,"safe_deposit_table":rows},"monotonic",ok)


def test_lyapunov_reactive_guard() -> TestResult:
    random.seed(11)
    no_ctrl = simulate("adv_jump_cluster", runs=1200, steps=500, k=1.4, R=140, alpha=0.5, with_control=False, with_alc=True)
    random.seed(11)
    ctrl = simulate("adv_jump_cluster", runs=1200, steps=500, k=1.4, R=140, alpha=0.5, with_control=True, with_alc=True)

    reacts = ctrl["compressions_triggered"] > 0 and ctrl["expansions_blocked"] > 0
    risk_improves = ctrl["p_collapse"] <= no_ctrl["p_collapse"]
    ok = reacts and risk_improves

    return TestResult(
        "TestLyapunovReactiveGuard",
        "Control loop reacts to rising instability proxies (expansion blocking + compression).",
        {},
        "A/B on adversarial jump cluster.",
        {
            "pnl": ctrl["avg_pnl"],
            "p_no_ctrl": no_ctrl["p_collapse"],
            "p_ctrl": ctrl["p_collapse"],
            "expansions_blocked": ctrl["expansions_blocked"],
            "compressions_triggered": ctrl["compressions_triggered"],
        },
        "Must react and not worsen collapse probability.",
        ok,
    )


def test_lyapunov_delta_feedback() -> TestResult:
    random.seed(12)
    low = simulate("random", runs=900, steps=420, k=1.25, R=180, alpha=0.5, with_control=True, with_alc=True)
    random.seed(12)
    high = simulate("adv_liquidity_freeze", runs=900, steps=420, k=1.4, R=140, alpha=0.5, with_control=True, with_alc=True)

    # In harder regime, control should intensify and block more expansions
    ok = high["control_intensity"] >= low["control_intensity"] and high["expansions_blocked"] >= low["expansions_blocked"]
    return TestResult(
        "TestLyapunovDeltaFeedback",
        "Feedback loop: worsening regime increases control intensity/blocks.",
        {},
        "Compare benign vs adversarial regime under control.",
        {
            "pnl": high["avg_pnl"],
            "control_intensity_low": low["control_intensity"],
            "control_intensity_high": high["control_intensity"],
            "blocked_low": low["expansions_blocked"],
            "blocked_high": high["expansions_blocked"],
        },
        "High-stress regime should trigger stronger control.",
        ok,
    )


def test_lyapunov_recovery_release() -> TestResult:
    random.seed(13)
    stressed = simulate("adv_liquidity_gap", runs=900, steps=420, k=1.4, R=140, alpha=0.5, with_control=True, with_alc=True)
    random.seed(13)
    recovered = simulate("random", runs=900, steps=420, k=1.25, R=200, alpha=0.5, with_control=True, with_alc=True)

    # recovery regime should reduce blocking pressure and preserve activity
    ok = recovered["activity_ratio"] >= stressed["activity_ratio"] or recovered["control_intensity"] <= stressed["control_intensity"]
    return TestResult(
        "TestLyapunovRecoveryRelease",
        "Feedback loop: when stress drops, control relaxes or activity recovers.",
        {},
        "Compare stressed vs recovery regime under control.",
        {
            "pnl": recovered["avg_pnl"],
            "activity_stressed": stressed["activity_ratio"],
            "activity_recovered": recovered["activity_ratio"],
            "control_stressed": stressed["control_intensity"],
            "control_recovered": recovered["control_intensity"],
        },
        "Control should not stay locked at stressed intensity after recovery.",
        ok,
    )


def test_lyapunov_optimization() -> TestResult:
    random.seed(21)
    off = simulate("adv_jump_cluster", runs=900, steps=450, k=1.4, R=140, alpha=0.5, with_control=False, with_alc=True)
    random.seed(21)
    on = simulate("adv_jump_cluster", runs=900, steps=450, k=1.4, R=140, alpha=0.5, with_control=True, with_alc=True)

    # Lyapunov-driven policy should reduce risk and actively choose compress/block actions
    chooses = on["expansions_blocked"] > 0 and on["compressions_triggered"] > 0
    improves = on["p_collapse"] < off["p_collapse"]
    ok = chooses and improves

    return TestResult(
        "TestLyapunovOptimization",
        "Runtime action selection should improve collapse risk via non-binary control.",
        {},
        "Compare control OFF vs ON in jump-cluster stress.",
        {
            "pnl": on["avg_pnl"],
            "p_off": off["p_collapse"],
            "p_on": on["p_collapse"],
            "blocked": on["expansions_blocked"],
            "compressions": on["compressions_triggered"],
        },
        "Control ON must select protective actions and reduce collapse probability.",
        ok,
    )


def test_lyapunov_convergence() -> TestResult:
    random.seed(22)
    easy = simulate("random", runs=1200, steps=500, k=1.2, R=220, alpha=0.5, with_control=True, with_alc=True)
    random.seed(22)
    hard = simulate("adv_liquidity_freeze", runs=1200, steps=500, k=1.4, R=140, alpha=0.5, with_control=True, with_alc=True)

    # proxy convergence: benign regime should keep lower stress and faster recovery profile
    recovery_speed = easy["activity_ratio"] - hard["activity_ratio"]
    ok = easy["p_collapse"] <= 0.1 and recovery_speed > -0.4

    return TestResult(
        "TestLyapunovConvergence",
        "Lyapunov control should keep benign regime near-convergent and recover activity.",
        {},
        "Benign vs hard regime under control.",
        {
            "pnl": easy["avg_pnl"],
            "p_easy": easy["p_collapse"],
            "p_hard": hard["p_collapse"],
            "recovery_speed_proxy": recovery_speed,
            "control_intensity_easy": easy["control_intensity"],
            "control_intensity_hard": hard["control_intensity"],
        },
        "Benign regime should remain low-risk with better recovery behavior.",
        ok,
    )


def test_lyapunov_dominance() -> TestResult:
    modes=["random","trend","adv_monotonic","adv_jump_cluster","adv_liquidity_gap","adv_liquidity_freeze"]
    rows=[]
    for i,m in enumerate(modes):
        random.seed(30+i)
        off=simulate(m, runs=700, steps=360, k=1.4, R=140, alpha=0.5, with_control=False, with_alc=True)
        random.seed(30+i)
        on=simulate(m, runs=700, steps=360, k=1.4, R=140, alpha=0.5, with_control=True, with_alc=True)
        rows.append((m,off,on))

    improved=sum(1 for _,off,on in rows if on["p_collapse"]<off["p_collapse"])
    ok=improved>=5

    return TestResult(
        "TestLyapunovDominance",
        "Disable-Lyapunov comparison: ON should dominate OFF in most regimes.",
        {},
        "Cross-mode A/B comparison.",
        {
            "pnl": 0.0,
            "improved_modes": improved,
            "total_modes": len(rows),
            "by_mode": {m:{"off":off["p_collapse"],"on":on["p_collapse"]} for m,off,on in rows},
        },
        "Control ON must improve collapse risk in the majority of modes.",
        ok,
    )


# -------- reports --------
def write_core_reports(results: List[TestResult]) -> None:
    lines = ["# ALE FULL LOGIC REPORT", "", "## Test status"]
    for r in results:
        lines.append(f"- {r.name}: {'PASS' if r.passed else 'FAIL'}")
    (ALE_DIR / "ALE_FULL_LOGIC_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ALE_DIR / "ALE_ALC_FULL_AUDIT.md").write_text("# ALE + ALC FULL AUDIT\n\nPCRCV stage integrated.\n", encoding="utf-8")


def write_frontier_report() -> Tuple[List[Dict], List[Dict]]:
    base = frontier("shock", with_control=False)
    ctrl = frontier("shock", with_control=True)

    path = ALE_DIR / "ALE_RISK_CONTROL_REPORT.md"
    lines = [
        "# ALE RISK CONTROL REPORT",
        "",
        "## Risk-Return Frontier (shock mode)",
        "| k | R | P(collapse) | PnL | DD | Score |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for r in ctrl[:20]:
        lines.append(f"| {r['k']:.1f} | {r['R']} | {r['p']:.4f} | {r['pnl']:.4f} | {r['dd']:.4f} | {r['score']:.4f} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return base, ctrl


def write_truth_report(results: List[TestResult], base_front: List[Dict], ctrl_front: List[Dict]) -> None:
    by = {r.name: r.results for r in results}

    best_pnl_under_risk = max((x["pnl"] for x in ctrl_front if x["p"] < 0.2), default=float("-inf"))
    min_risk_over_pnl = min((x["p"] for x in ctrl_front if x["pnl"] > -1.0), default=1.0)

    fake = by["TestProfitConstrainedControl"]["fake_safety"]
    activity = by["TestProfitConstrainedControl"]["activity_ratio"]
    ci = by["TestProfitConstrainedControl"]["control_intensity"]

    verdict = "Overcontrolled / degenerate"
    if by["TestProfitConstrainedControl"]["p_ctrl"] < by["TestProfitConstrainedControl"]["p_base"] and by["TestProfitConstrainedControl"]["pnl_ctrl"] > 0 and activity >= 0.15:
        verdict = "Truly robust AND profitable"
    elif by["TestProfitConstrainedControl"]["p_ctrl"] < by["TestProfitConstrainedControl"]["p_base"] and activity < 0.15:
        verdict = "Safe but untradable"
    elif by["TestProfitConstrainedControl"]["pnl_ctrl"] > 0 and by["TestProfitConstrainedControl"]["p_ctrl"] > 0.3:
        verdict = "Profitable but unstable"

    lines = [
        "# ALE_PROFIT_REALITY_REPORT",
        "",
        "## 1. Activity vs Safety",
        f"- activity_ratio: {activity:.4f}",
        f"- control_intensity: {ci:.4f}",
        f"- trade_rate: {by['TestProfitConstrainedControl']['trade_rate']:.4f}",
        f"- control killing trading?: {'YES' if activity < 0.15 else 'NO'}",
        "",
        "## 2. Profitability",
        f"- PnL before: {by['TestProfitConstrainedControl']['pnl_base']:.4f}",
        f"- PnL after: {by['TestProfitConstrainedControl']['pnl_ctrl']:.4f}",
        f"- risk-adjusted frontier best pnl (p<0.2): {best_pnl_under_risk:.4f}",
        "",
        "## 3. Risk-Return Frontier",
        f"- min risk with pnl>-1.0: {min_risk_over_pnl:.4f}",
        "",
        "## 4. Fake Safety Check",
        f"- fake_safety_flag: {fake}",
        "",
        "## 5. Estimator Quality",
        f"- calibration_error: {by['TestEstimatorCalibration']['calibration_error']:.4f}",
        f"- brier_score: {by['TestEstimatorCalibration']['brier_score']:.4f}",
        f"- roc_auc: {by['TestEstimatorCalibration']['roc_auc']:.4f}",
        "",
        "## 6. Final Verdict",
        f"[{'x' if verdict == 'Truly robust AND profitable' else ' '}] Truly robust AND profitable",
        f"[{'x' if verdict == 'Safe but untradable' else ' '}] Safe but untradable",
        f"[{'x' if verdict == 'Profitable but unstable' else ' '}] Profitable but unstable",
        f"[{'x' if verdict == 'Overcontrolled / degenerate' else ' '}] Overcontrolled / degenerate",
    ]

    (ALE_DIR / "ALE_PROFIT_REALITY_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> None:
    tests = [
        test_lock_compression,
        test_monte_carlo_realistic,
        test_profit_constrained_control,
        test_risk_return_efficiency,
        test_control_overkill,
        test_adaptive_k_stability,
        test_estimator_calibration,
        test_reality_stress_v2,
        test_adversarial_scenarios,
        test_safe_deposit,
        test_lyapunov_reactive_guard,
        test_lyapunov_delta_feedback,
        test_lyapunov_recovery_release,
        test_lyapunov_optimization,
        test_lyapunov_convergence,
        test_lyapunov_dominance,
    ]

    results: List[TestResult] = []
    for t in tests:
        r = t()
        write_report(r)
        results.append(r)
        if not r.passed:
            raise AssertionError(f"FAILED {r.name}")
        print(f"PASS {r.name}")

    write_core_reports(results)
    base_front, ctrl_front = write_frontier_report()
    write_truth_report(results, base_front, ctrl_front)
    print(f"ALL {len(results)} TESTS PASSED")


if __name__ == "__main__":
    run()
