from __future__ import annotations

import math
import random
from dataclasses import dataclass
from statistics import mean
from typing import Dict, List

ACTIONS = ("EXPAND", "SOFT", "COMPRESS", "PARTIAL", "HARD", "SAFE", "HOLD")
EXPOSURE_THRESHOLD = 0.32
V_HIGH = 1.05
DELAY_SUBOPTIMAL_THRESHOLD = 90


@dataclass
class SimConfig:
    scenario: str
    steps: int = 220
    seed: int = 1
    control_delay: int = 0
    slippage: float = 1.0
    spread: float = 1.0
    dual_flow: bool = False
    latency_jitter: int = 0
    mpc_horizon: int = 8


@dataclass
class EngineState:
    exposure: float
    margin: float
    risk: float
    vol: float
    v: float


@dataclass
class SimResult:
    values: List[float]
    deltas: List[float]
    actions: List[str]
    control_strength: List[float]
    latency_response: float
    collapse: bool
    states: List[EngineState]


def _shock(scenario: str, t: int, steps: int) -> float:
    z = random.gauss(0.0, 1.0)
    base = 0.001 * z
    if scenario == "trend":
        return -0.001 * (1 + t / max(1, steps)) + base
    if scenario == "jump":
        return base - (0.014 if (t % 35 == 0) else 0.0)
    if scenario == "freeze":
        return -0.007 if (t % 40) < 7 else base - 0.0005
    if scenario == "dual-flow":
        drift = -0.0003 if t < steps // 2 else 0.0004
        return drift + base
    if scenario == "flash_crash":
        return base - (0.03 if t == steps // 3 else 0.0)
    if scenario == "spread_explosion":
        return -0.001 + 0.0015 * z
    if scenario == "margin_cascade":
        return -0.0014 + 0.0012 * z
    if scenario == "fake_stability_trap":
        return 0.0001 * z if t < steps * 0.6 else (-0.03 + 0.001 * z)
    if scenario == "opposite_signal_trap":
        return (0.0014 + 0.0006 * z) if t < steps * 0.55 else (-0.0022 + 0.001 * z)
    return base


def _risk_value(exposure: float, margin: float, risk: float, vol: float) -> float:
    return 1.5 * abs(exposure) + 1.0 * max(0.0, 1.0 - margin) + 1.2 * risk + 0.45 * vol


def _control_strength(action: str) -> float:
    return {
        "EXPAND": 0.20,
        "HOLD": 0.05,
        "SAFE": 0.25,
        "SOFT": 0.45,
        "COMPRESS": 0.65,
        "PARTIAL": 0.82,
        "HARD": 1.0,
    }[action]


def _tail_mean(values: List[float], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = max(0, int(len(s) * q))
    tail = s[idx:] if idx < len(s) else [s[-1]]
    return mean(tail)


def _entropy_penalty(counts: Dict[str, int]) -> float:
    n = sum(counts.values())
    if n <= 1:
        return 1.0
    h = 0.0
    for c in counts.values():
        if c > 0:
            p = c / n
            h -= p * math.log(max(1e-12, p))
    return 1.0 - h / math.log(len(counts))


def _compression_action(v: float, dv_pred: float, cvar_proxy: float = 0.0) -> str:
    if v > 1.45 or cvar_proxy > 0.08 or dv_pred > 0.09:
        return "HARD"
    if v > 1.2 or dv_pred > 0.05:
        return "PARTIAL"
    if v > 0.95 or dv_pred > 0.025:
        return "COMPRESS"
    return "SOFT"


def _candidate_actions(v: float) -> List[str]:
    base = ["SOFT", "COMPRESS", "PARTIAL", "SAFE", "HOLD", "HARD"]
    if v < 0.60:
        base.insert(0, "EXPAND")
    if v > 1.2:
        return ["SOFT", "COMPRESS", "PARTIAL", "HARD", "SAFE", "HOLD"]
    return base


def _apply_action(state: EngineState, action: str, shock: float, cfg: SimConfig, t: int) -> EngineState:
    exposure, margin, risk, vol = state.exposure, state.margin, state.risk, state.vol

    if action == "EXPAND":
        exposure *= 1.04
        margin = max(0.05, margin - 0.02)
        risk *= 1.05
    elif action == "SOFT":
        exposure *= 0.96
        margin = min(1.05, margin + 0.01)
        risk *= 0.95
    elif action == "COMPRESS":
        exposure *= 0.86
        margin = min(1.12, margin + 0.05)
        risk *= 0.88
    elif action == "PARTIAL":
        exposure *= 0.76
        margin = min(1.16, margin + 0.075)
        risk *= 0.83
    elif action == "HARD":
        exposure *= 0.60
        margin = min(1.2, margin + 0.11)
        risk *= 0.77
    elif action == "SAFE":
        exposure *= 0.92
        risk *= 0.94

    slip = cfg.slippage * abs(shock) * 0.22
    spr = cfg.spread * 0.001
    exposure = max(0.01, exposure + shock * 2.0 + slip)
    margin = max(0.0, min(1.2, margin - abs(shock) * 1.7 - spr + (0.02 if action in ("COMPRESS", "PARTIAL", "HARD") else 0.0)))
    risk = max(0.0, min(2.3, risk + abs(shock) * (1.0 + cfg.slippage * 0.35) - (0.04 if action in ("COMPRESS", "PARTIAL", "HARD") else 0.0)))
    vol = 0.88 * vol + 0.12 * min(1.0, abs(shock) * 55)

    if cfg.dual_flow:
        exposure = max(0.01, exposure + 0.06 * math.sin(t / 7))

    v = _risk_value(exposure, margin, risk, vol)
    return EngineState(exposure=exposure, margin=margin, risk=risk, vol=vol, v=v)


def emergency_layer(state: EngineState, shock: float) -> str | None:
    # limited emergency: only real critical conditions
    if state.margin < 0.14 or state.v > 1.55:
        return "HARD"
    if abs(shock) > 0.034 and state.v > 1.2:
        return "SAFE"
    return None


def evaluate_action_objective(
    state: EngineState,
    action: str,
    cfg: SimConfig,
    t: int,
    history: List[str],
    rng_seed: int,
    last_real_dv: float,
) -> float:
    rng = random.Random(rng_seed)
    horizon = max(2, cfg.mpc_horizon)
    trial_dv: List[float] = []
    trial_v: List[float] = []
    controls: List[float] = []

    sim_state = EngineState(**state.__dict__)
    local_hist = list(history)

    for h in range(horizon):
        shock = _shock(cfg.scenario, t + h, cfg.steps) + rng.gauss(0.0, 1.0) * 0.00025
        cvar_proxy = _tail_mean(trial_dv, 0.8) if trial_dv else 0.0
        act = action if h == 0 else _compression_action(sim_state.v, shock + cfg.control_delay * 0.0012, cvar_proxy)
        sim_state = _apply_action(sim_state, act, shock, cfg, t + h)
        prev = state.v if h == 0 else trial_v[-1]
        trial_dv.append(sim_state.v - prev)
        trial_v.append(sim_state.v)
        controls.append(_control_strength(act))
        local_hist.append(act)

    e_dv = mean(trial_dv)
    cvar95 = _tail_mean(trial_dv, 0.95)
    max_spike = max(trial_dv) if trial_dv else 0.0
    vmax = max(trial_v) if trial_v else state.v
    var = mean((x - e_dv) ** 2 for x in trial_dv)

    counts = {a: local_hist.count(a) for a in ACTIONS}
    ent_pen = _entropy_penalty(counts)
    safe_bias = max(0.0, (counts["SAFE"] / max(1, len(local_hist))) - 0.30)
    hard_bias = max(0.0, (counts["HARD"] / max(1, len(local_hist))) - 0.20)

    realized_penalty = 2.0 * abs(e_dv - last_real_dv)
    positive_drift_penalty = 35.0 * (max(0.0, e_dv) ** 2)
    hold_pen = 0.9 if action == "HOLD" else 0.0
    if action == "HOLD" and abs(e_dv) > 0.01:
        hold_pen += 3.0

    rare_boost = 0.55 if (counts[action] / max(1, len(local_hist))) < 0.06 else 0.0
    expand_reward = 0.10 if action == "EXPAND" and state.v < 0.55 and state.margin > 0.7 else 0.0
    delay_penalty = cfg.control_delay * max(0.0, e_dv + 0.002) * 0.5
    cross_penalty = 0.45 * abs(state.exposure)
    exposure_after = state.exposure * (1.04 if action == "EXPAND" else 1.0)
    expand_penalty = 6.0 * max(0.0, exposure_after - state.exposure)

    return (
        2.1 * e_dv
        + 1.3 * cvar95
        + 1.1 * max_spike
        + 0.9 * vmax
        + 0.7 * var
        + 0.25 * mean(abs(x) for x in controls)
        + 1.8 * ent_pen
        + 2.1 * safe_bias
        + 1.9 * hard_bias
        + realized_penalty
        + positive_drift_penalty
        + hold_pen
        + delay_penalty
        + cross_penalty
        + expand_penalty
        - rare_boost
        - expand_reward
    )


def choose_mpc_action(state: EngineState, cfg: SimConfig, t: int, history: List[str], seed: int, last_real_dv: float, explore: bool = True) -> str:
    dv_pred = 0.02 * state.vol + 0.03 * (state.v - 0.8) + cfg.control_delay * 0.001
    predicted_dv = dv_pred + 0.0006 * cfg.control_delay

    candidates = _candidate_actions(state.v)
    if "EXPAND" in candidates:
        allow_expand = (state.v < 0.45 and predicted_dv < -0.01 and state.exposure < 0.20)
        if not allow_expand:
            candidates.remove("EXPAND")
    if state.v < 1.15 and "HARD" in candidates:
        candidates.remove("HARD")  # no premature hard-close
    if abs(dv_pred) > 0.012 and "HOLD" in candidates:
        candidates.remove("HOLD")

    if explore and len(history) > 10 and "EXPAND" in candidates:
        if history.count("EXPAND") / len(history) > 0.35:
            candidates.remove("EXPAND")

    scores = {
        a: evaluate_action_objective(state, a, cfg, t, history, seed + 19 * i, last_real_dv)
        for i, a in enumerate(candidates)
    }
    best = min(scores, key=scores.get)

    # risk accumulation detector (N=4)
    if len(history) > 4 and predicted_dv > 0.01 and state.v > 0.95:
        return "COMPRESS"

    if explore and len(history) > 20:
        freq = {a: history.count(a) / len(history) for a in ACTIONS}
        if freq["HARD"] < 0.06 and state.v > 1.05:
            return "HARD"
        if freq["HOLD"] < 0.06 and state.v < 0.65 and abs(dv_pred) < 0.006:
            return "HOLD"
        if freq["SAFE"] > 0.30 and best == "SAFE":
            return "SOFT"
    return best


def run_closed_loop(cfg: SimConfig, force_action: str | None = None, disable_action: str | None = None) -> SimResult:
    random.seed(cfg.seed)
    state = EngineState(exposure=0.35, margin=0.75, risk=0.2, vol=0.1, v=_risk_value(0.35, 0.75, 0.2, 0.1))
    values = [state.v]
    deltas: List[float] = []
    actions: List[str] = []
    control_strength: List[float] = []
    states: List[EngineState] = [state]
    response_ticks: List[int] = []
    collapse = False
    pending_action = "SOFT"
    pending_until = 0
    last_real_dv = -0.001

    for t in range(1, cfg.steps + 1):
        shock = _shock(cfg.scenario, t, cfg.steps)
        emergency = emergency_layer(state, shock)
        action = emergency or force_action or choose_mpc_action(state, cfg, t, actions, cfg.seed, last_real_dv, explore=True)
        if last_real_dv > 0 and state.v > 1.0:
            action = "COMPRESS"
        if disable_action and action == disable_action:
            action = "SOFT"

        dly = cfg.control_delay + (random.randint(0, cfg.latency_jitter) if cfg.latency_jitter > 0 else 0)
        if dly > 0 and emergency is None:
            if t >= pending_until:
                pending_action = action
                pending_until = t + dly
            effective = pending_action if t >= pending_until else ("COMPRESS" if state.v > 1.0 else "SOFT")
        else:
            effective = action

        if cfg.control_delay > DELAY_SUBOPTIMAL_THRESHOLD and random.random() < 0.45 and emergency is None:
            # soft failure realism under high delay
            effective = random.choice(["SOFT", "HOLD", "EXPAND"])

        new_state = _apply_action(state, effective, shock, cfg, t)
        dV = new_state.v - state.v
        last_real_dv = dV
        if dV > 0.015 and effective in ("COMPRESS", "PARTIAL", "HARD"):
            response_ticks.append(t)

        values.append(new_state.v)
        deltas.append(dV)
        actions.append(effective)
        control_strength.append(_control_strength(effective))
        states.append(new_state)
        state = new_state

        if state.v > 3.0 or state.margin <= 0.01:
            collapse = True
            break

    return SimResult(values, deltas, actions, control_strength, mean(response_ticks) if response_ticks else 0.0, collapse, states)


def run_closed_loop_fast(cfg: SimConfig) -> SimResult:
    random.seed(cfg.seed)
    state = EngineState(exposure=0.35, margin=0.75, risk=0.2, vol=0.1, v=_risk_value(0.35, 0.75, 0.2, 0.1))
    values = [state.v]
    deltas: List[float] = []
    actions: List[str] = []
    strengths: List[float] = []
    states: List[EngineState] = [state]
    for t in range(1, cfg.steps + 1):
        shock = _shock(cfg.scenario, t, cfg.steps)
        base_action = _compression_action(state.v, 0.02 * state.vol + 0.0006 * cfg.control_delay) if state.v > 0.7 else "SOFT"
        if state.exposure > EXPOSURE_THRESHOLD and base_action == "EXPAND":
            base_action = "SOFT"
        action = emergency_layer(state, shock) or base_action
        nxt = _apply_action(state, action, shock, cfg, t)
        deltas.append(nxt.v - state.v)
        values.append(nxt.v)
        actions.append(action)
        strengths.append(_control_strength(action))
        states.append(nxt)
        state = nxt
        if state.v > 3.0 or state.margin <= 0.01:
            break
    return SimResult(values, deltas, actions, strengths, 0.0, (state.v > 3.0 or state.margin <= 0.01), states)


def summarize(result: SimResult) -> Dict[str, float]:
    deltas = result.deltas or [0.0]
    action_dist = {a: result.actions.count(a) / max(1, len(result.actions)) for a in ACTIONS}
    counts = {a: result.actions.count(a) for a in ACTIONS}
    return {
        "E_dV": mean(deltas),
        "P_dV_le_0": sum(1 for x in deltas if x <= 0) / len(deltas),
        "max_V": max(result.values) if result.values else 0.0,
        "latency_response": result.latency_response,
        "collapse": 1.0 if result.collapse else 0.0,
        "entropy": 1.0 - _entropy_penalty(counts),
        "cvar_95": _tail_mean(deltas, 0.95),
        **{f"action_{k.lower()}": v for k, v in action_dist.items()},
    }


def percentile(values: List[float], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = min(len(s) - 1, max(0, int(q * (len(s) - 1))))
    return s[idx]


def markdown_table(rows: List[Dict[str, float]], keys: List[str]) -> str:
    header = "| " + " | ".join(keys) + " |"
    sep = "|" + "|".join(["---"] * len(keys)) + "|"
    body = ["| " + " | ".join(f"{row.get(k, '')}" for k in keys) + " |" for row in rows]
    return "\n".join([header, sep, *body])
