"""Evaluate policies with common causal quotes and intermediate fills."""
from dataclasses import dataclass, replace
from money import Ledger, Config
from preserve import Params, Preserve, sign
from rebuild import Rebuild
from balanced import Balanced
from meta import Meta
from scenarios import quote


@dataclass(frozen=True)
class Outcome:
    pnl: float
    low: float
    drawdown: float
    turnover: float
    costs: float
    margin_stress: float
    stopout: int
    violations: int
    failures: int
    recovered_at: int | None
    remaining: float
    spread: float
    commission: float
    swap: float
    slippage: float


def run(variant, scenario, p=Params(), budget=180, config=Config(), trace=None):
    orientation, path, name = scenario
    horizon = min(len(path), p.horizon)
    p = replace(p, horizon=horizon)
    book = Ledger(orientation, config)
    strict = variant.endswith("-strict")
    if variant.startswith("A"):
        policy = Preserve(variant[:2], p, orientation, strict)
    elif variant == "J Balanced":
        if name not in ("stochastic", "exhaustive") or config != Config() or budget != 180:
            raise ValueError("J adapter is validated only on the nominal execution model")
        policy = Balanced(p)
    elif variant.startswith("B"):
        policy = Rebuild(variant, p)
    elif variant.startswith("M"):
        policy = Meta(p, budget, variant[2:])
    else:
        policy = None

    mid = 0
    stopout = 0
    closing = variant == "K"
    recovered_at = None
    for step in range(horizon + 1):
        q = quote(mid, name, step)
        if step:
            book.carry(q)
        if book.observe(q):
            stopout = 1
            closing = True
        mark = book.snapshot(q)["pnl"]
        target = mark > 1e-9
        if target or step == horizon:
            closing = True
        if not variant.startswith("M") and variant != "J Balanced":
            room = mark - 3 * abs(book.net) - p.reserve
            if room < -budget - 1e-9:
                closing = True
        if closing:
            book.flatten(q, policy.floors if strict and not target else None)
        else:
            policy.act(book, q, step)
        if trace is not None:
            action = "EXIT" if closing else getattr(policy, "action", variant)
            trace.append((step, book.net, book.gross, book.snapshot(q)["pnl"], action))
        if not book.gross and (closing or getattr(policy, "stopped", False)):
            if book.snapshot(q)["pnl"] > 1e-9:
                recovered_at = step
            break
        if step < horizon:
            move = path[step]
            if name == "adaptive":
                move = -300 * sign(book.net)
            mid += move
    s = book.snapshot(q)
    return Outcome(s["pnl"], book.low, book.drawdown, book.turnover, book.costs,
                   book.margin_stress, stopout, int(book.low < -budget - 1e-9),
                   book.failures, recovered_at, book.gross/100, book.spread_cost,
                   book.commission, book.swap, book.slippage)
