"""UMLRS-01. Reproducible EURUSD/USD event simulator, standard library only."""
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import product
from pathlib import Path
from random import Random
from statistics import mean, median
import csv
import json
import math

ROOT = Path(__file__).resolve().parent
PROFILES = {"Conservative": 20, "Balanced": 50, "Aggressive": 100}
FAMILIES = tuple("ABCDEFGHIJK")
CAPITAL = 15000
GROSS = 500


@dataclass(frozen=True)
class Event:
    x: int
    spread: int = 20
    slip: int = 0
    carry: float = 0
    reject: int = 0  # 1-based attempt within this event, single rejection


@dataclass(frozen=True)
class Policy:
    family: str
    cap: int
    size: int
    level: int = 80
    limit: int = 8
    horizon: int = 12
    budget: int = 300


@dataclass
class Book:
    cap: int
    legs: list = field(default_factory=list)
    realized: float = 0
    fees: float = 0
    swaps: float = 0
    attempt: int = 0
    fills: int = 0
    rejects: int = 0
    bad: int = 0
    forced: bool = False
    peak: float = 0
    dd: float = 0
    low: float = 0
    margin_max: float = 0
    gross_max: int = 0
    net_max: int = 0
    rows: list = field(default_factory=list)
    ledger: bool = False
    harvest: bool = False

    @property
    def gross(self):
        return sum(q for _, q, _ in self.legs)

    @property
    def net(self):
        return sum(s * q for s, q, _ in self.legs)

    def mark(self, e):
        floating = sum((s * (e.x - p) - e.spread / 2) * q / 100
                       for s, q, p in self.legs)
        liquidation_fee = .045 * self.gross
        return round(self.realized + floating - liquidation_fee, 9)

    def margin(self, e):
        # Gross initial margin, 30:1, synthetic USD value with a quote-side buffer.
        return self.gross * (110000 + e.x + e.spread / 2) / 3000

    def record(self, t, e, action, qty=0, price=None, cash=0, forecast=None, budget=None):
        pnl, margin = self.mark(e), self.margin(e)
        self.peak = max(self.peak, pnl)
        self.dd = max(self.dd, self.peak - pnl)
        self.low = min(self.low, pnl)
        self.margin_max = max(self.margin_max, margin)
        self.gross_max = max(self.gross_max, self.gross)
        self.net_max = max(self.net_max, abs(self.net))
        self.bad += int(self.gross > GROSS or abs(self.net) > self.cap)
        self.forced |= bool(margin and CAPITAL + pnl < .5 * margin)
        if self.ledger:
            forecast = forecast or {}
            self.rows.append(dict(t=t, midpoint=e.x, spread=e.spread, action=action,
                                  quantity=qty / 100, fill=price, cash=round(cash, 8),
                                  realized=round(self.realized, 8),
                                  floating_less_exit_fee=round(pnl-self.realized, 8),
                                  cycle=pnl, gross=self.gross / 100, net=self.net / 100,
                                  margin=round(margin, 8),
                                  risk_remaining=round(budget+pnl,8) if budget is not None else None,
                                  forecast_up=forecast.get("up"), forecast_down=forecast.get("down"),
                                  forecast_reverse_up=forecast.get("reverse_up"),
                                  forecast_reverse_down=forecast.get("reverse_down"),
                                  forecast_flat=forecast.get("flat")))

    def fill(self, t, e, quantity, index=None):
        """Signed quantity opens a position. Positive quantity closes a ticket."""
        self.attempt += 1
        if self.attempt == e.reject:
            self.rejects += 1
            self.record(t, e, "reject", quantity)
            return False
        if index is None:
            sign = 1 if quantity > 0 else -1
            q = abs(quantity)
            price = e.x + sign * (e.spread / 2 + e.slip)
            self.legs.append((sign, q, price))
            cash = -.045 * q
            action = "open_buy" if sign > 0 else "open_sell"
        else:
            sign, available, entry = self.legs[index]
            q = quantity
            price = e.x - sign * (e.spread / 2 + e.slip)
            if available == q:
                self.legs.pop(index)
            else:
                self.legs[index] = sign, available - q, entry
            cash = q * (sign * (price-entry) / 100 - .045)
            action = "close_buy" if sign > 0 else "close_sell"
        self.realized += cash
        self.fees += .045 * q
        self.fills += 1
        self.record(t, e, action, q, price, cash)
        return True

    def trim(self, t, e, target, retain=0):
        """Reduce both sides without crossing net cap at any intermediate fill."""
        wanted = {1: retain + max(target, 0), -1: retain + max(-target, 0)}
        while self.legs:
            for i, (s, q, _) in enumerate(self.legs):
                excess = sum(v for side, v, _ in self.legs if side == s) - wanted[s]
                volume = min(excess, q, self.cap + s * self.net)
                if volume > 0:
                    if not self.fill(t, e, volume, i):
                        return False
                    break
            else:
                return True
        return True

    def set_net(self, t, e, target):
        """Close opposite tickets first, then open residual directional volume."""
        if not self.trim(t, e, target):
            return False
        delta = target - self.net
        if delta:
            added = (abs(delta) / 100)
            gross = self.gross + abs(delta)
            pnl = self.mark(e) - added * (e.spread + e.slip + 9)
            margin = gross * (110000 + e.x + e.spread / 2) / 3000
            if gross > GROSS or CAPITAL + pnl < 2 * margin:
                return False
            return self.fill(t, e, delta)
        return True


def seed(book, sign, partial=False, event=None):
    initial = Event(-sign * 300)
    left = 100
    while left:
        q = min(left, book.cap)
        book.fill(-1, initial, sign*q)
        book.fill(-1, initial, -sign*q)
        left -= q
    e = event or Event(0)
    book.attempt = 0
    retain = (100 - book.cap) // 2 if partial else 0
    book.harvest = book.trim(0, e, -sign * book.cap, retain)


def sign(x):
    return (x > 0) - (x < 0)


def rule(p, s, t, history, b, changes, reference):
    """Return desired net and updated reference price."""
    x = history[-1].x
    direction = sign(x - reference)
    triggered = abs(x - reference) >= p.level
    if p.family == "A":
        return -s * p.size, reference
    if p.family == "B":
        return s * p.size if s * x >= p.level or changes else b.net, reference
    if p.family == "C":
        return -s * p.size if s * x >= p.level or changes else 0, reference
    if p.family == "D" and triggered:
        return direction * p.size, x
    if p.family == "E" and abs(x) >= p.level and not changes:
        return sign(x) * p.size, reference
    if p.family == "F":
        return b.net, reference
    if p.family == "G" and triggered:
        return direction * (p.size // (2 ** changes)), x
    if p.family == "H" and triggered:
        return -sign(x) * min(p.size, abs(x) // p.level * max(1, p.size // 3)), x
    if p.family == "I":
        moves = [abs(a.x-z.x) for a, z in zip(history[-5:-1], history[-4:])] if len(history) >= 5 else []
        if abs(x-reference) >= max(p.level, 2 * mean(moves) if moves else 0):
            return direction * p.size, x
    if p.family == "J":
        # A single breakout with an explicit loss/continuation gate in run().
        return (sign(x) * p.size if abs(x) >= p.level else 0) if not changes else b.net, reference
    return b.net, reference


def run(p, path, orientation=1, ledger=False):
    b = Book(p.cap, ledger=ledger)
    seed(b, orientation, p.family == "F", path[0])
    state = "ACTIVE" if b.harvest else "SAFE"
    changes = 0
    reference = path[0].x
    executed_until = 0
    for t, e in enumerate(path):
        executed_until = t
        if t:
            b.attempt = 0
            carry = e.carry * b.gross / 100
            b.realized -= carry
            b.swaps += carry
            b.record(t, e, "quote", cash=-carry)
        value = b.mark(e)
        if b.forced or value <= -p.budget or t >= p.horizon or t == len(path)-1:
            state = "SAFE"
        if value - e.slip * b.gross / 100 > 0:
            state = "TARGET"
        if p.family == "K":
            state = "SAFE"
        if state in ("SAFE", "TARGET"):
            closed = b.trim(t, e, 0)
            if not closed:
                b.trim(t, e, 0)  # bounded same-quote retry in this model
            if not b.legs:
                break
            state = "SAFE"
            continue

        if p.family == "F" and changes < p.limit and abs(e.x-reference) >= p.level:
            retain = max(0, (b.gross-abs(b.net))//2 - p.size)
            if not b.trim(t, e, b.net, retain):
                state = "SAFE"
            reference = e.x
            changes += 1
            continue

        q, reference = rule(p, orientation, t, path[:t+1], b, changes, reference)
        if p.family == "J":
            # Probe monotone continuation, reversal and flat with two-event
            # liquidation allowance. Bound spread/carry even while flat.
            future_gross = abs(q) / 100
            entry = abs(q-b.net) / 100 * (e.spread + e.slip + 9)
            shocks = {"up": 600, "down": -600, "reverse_up": -300,
                      "reverse_down": 300, "flat": 0}
            scores = {k: value - entry + q/100*d - future_gross*48
                      for k, d in shocks.items()}
            margin = future_gross * (110000 + e.x + 650) / 30
            worst = min(scores.values())
            allowed = worst >= -p.budget and CAPITAL + worst >= 2*margin
            if b.ledger:
                b.record(t,e,"hold_or_enter" if allowed else "gate_to_safe",
                         forecast=scores,budget=p.budget)
            if not allowed:
                state = "SAFE"
                if b.trim(t, e, 0) or b.trim(t, e, 0):
                    break
                continue

        if q != b.net and changes < p.limit:
            previous = b.net
            if not b.set_net(t, e, q):
                state = "SAFE"
                if p.family == "J":
                    if b.trim(t, e, 0) or b.trim(t, e, 0):
                        break
            # J counts entries from flat, excluding liquidation of the inherited leg.
            changes += int(p.family != "J" or (previous == 0 and b.net != 0))
    return dict(pnl=b.mark(path[executed_until]), dd=b.dd, low=b.low,
                margin=b.margin_max, gross=b.gross_max/100, net=b.net_max/100,
                time=executed_until, fees=round(b.fees, 8), trades=b.fills,
                bad=b.bad, forced=b.forced, rejects=b.rejects, open=b.gross,
                funded=round(b.mark(path[executed_until])/CAPITAL, 9), rows=b.rows)


def path(xs):
    return tuple(Event(x) for x in xs)


def named():
    return {
        "up": path(range(0, 901, 75)),
        "down": path(range(0, -901, -75)),
        "reverse_up": path([0,-140,-260,-100,50,190,340,490,640]),
        "reverse_down": path([0,140,260,100,-50,-190,-340,-490,-640]),
        "reversals": path([0,110,-110]*4+[0]),
        "flat": path([0]*13),
        "tight": path([0,10,-10]*4+[0]),
        "wide": path([0,220,320,150,-20,-210,-320,-140,0,200,310,140,0]),
        "false_breakout": path([0,79,81,0,-79,-81,0,79,81,0]),
        "extended": path(range(0, 2401, 200)),
        "gaps": path([0,290,-10,-310,-10,290,-10]),
        "spread_swap": (Event(0),Event(90),Event(120,100,4,.02),
                        Event(-160,100,4,.02),Event(-170,100,4,.02)),
        "spread40": tuple(Event(x,20 if t == 0 else 40) for t,x in enumerate(range(0,901,75))),
        "spread100": tuple(Event(x,20 if t == 0 else 100) for t,x in enumerate(range(0,901,75))),
        "reject_harvest": (Event(0,reject=2),Event(300,100,4,.02),Event(0)),
        "reject_entry": (Event(0),Event(90,reject=1),Event(-200,100,4,.02),Event(0)),
        "reject_exit": (Event(0),Event(100),Event(400,100,4,.02,1),Event(100),Event(0)),
    }


def lattice():
    for changes in product((-100, 0, 100), repeat=5):
        x = 0
        xs = [x]
        for d in changes:
            x += d
            xs.append(x)
        yield path(xs + [x]*7)


def monte_carlo():
    rng = Random(20261118)
    for i in range(240):
        x = 0
        events = [Event(0)]
        drift = rng.choice((-55, 0, 55))
        for t in range(12):
            x += max(-300, min(300, round(rng.gauss(drift, 95))))
            events.append(Event(x, rng.choice((20,20,20,40,100)),
                                rng.choice((0,0,2,4)), .02, int(rng.random()<.03)))
        yield f"mc_{i}", tuple(events)


def cases(paths):
    return [(name, seq, side) for name, seq in paths for side in (1,-1)]


def loss_key(result):
    return int(result["bad"] > 0 or result["open"] > 0), max(0, -result["pnl"]), int(result["forced"])


def score(results):
    constraints, loss, forced = zip(*(loss_key(r) for r in results))
    return (max(constraints), max(loss), mean(forced),
            abs(mean(r["pnl"] for r in results[::2])-mean(r["pnl"] for r in results[1::2])),
            mean(r["dd"] for r in results), mean(r["fees"] for r in results),
            -mean(r["pnl"] for r in results), mean(r["time"] for r in results))


def search(candidates, suite, branch_bound=True):
    best = None
    pruned = 0
    simulated = 0
    for p in candidates:
        results = []
        bound = (0, 0)
        for _, seq, side in suite:
            r = run(p, seq, side)
            simulated += 1
            results.append(r)
            bound = tuple(map(max, zip(bound, loss_key(r)[:2])))
            if branch_bound and best and bound > best[0][:2]:
                pruned += 1
                break
        else:
            rank = score(results)
            if best is None or rank < best[0]:
                best = rank, p, results
    return best, pruned, simulated


def adversary(p, side):
    """Beam search choosing each next quote after simulating the prefix."""
    beam = [path([0])]
    for _ in range(6):
        extensions = []
        for seq in beam:
            for d in (-300,-100,-1,0,1,100,300):
                for spread, slip, reject in ((20,0,0),(100,4,0),(100,4,1)):
                    candidate = seq + (Event(seq[-1].x+d,spread,slip,.02,reject),)
                    padded = candidate + (Event(candidate[-1].x,spread,slip,.02),) * (13-len(candidate))
                    r = run(p, padded, side)
                    extensions.append(((loss_key(r),r["dd"],r["margin"]), candidate))
        extensions.sort(key=lambda item: item[0], reverse=True)
        beam = [candidate for _, candidate in extensions[:5]]
    return beam[0] + (Event(beam[0][-1].x,100,4,.02),)*6


def write_json(name, value):
    (ROOT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n")


def write_csv(name, rows):
    with (ROOT/name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def summarize(profile, policy, suite, results):
    losses = sorted(max(0, -r["pnl"]) for r in results)
    wins = [r for r in results if r["pnl"] > 0 and not r["open"]]
    group = defaultdict(list)
    for (name, _, _), r in zip(suite, results):
        group[name].append(r["pnl"])
    adv = [r["pnl"] for (name, _, _), r in zip(suite, results) if name.startswith("adv_")]
    return dict(profile=profile, family=policy.family, size=policy.size/100,
                level=policy.level, budget=policy.budget, horizon=policy.horizon, limit=policy.limit,
                up=mean(group["up"]), down=mean(group["down"]), flat=mean(group["flat"]),
                reversals=mean(group["reversals"]), wide=mean(group["wide"]),
                spread_swap=mean(group["spread_swap"]), spread40=mean(group["spread40"]),
                spread100=mean(group["spread100"]), adversarial_worst=min(adv),
                cycles=len(results), positive_pct=100*len(wins)/len(results),
                mean=mean(r["pnl"] for r in results), median=median(r["pnl"] for r in results),
                loss_p95=losses[math.ceil(len(losses)*.95)-1],
                loss_p99=losses[math.ceil(len(losses)*.99)-1], worst=-max(losses),
                dd=max(r["dd"] for r in results), gross=max(r["gross"] for r in results),
                net=max(r["net"] for r in results), margin=max(r["margin"] for r in results),
                max_time=max(r["time"] for r in results),
                max_recovery_time=max((r["time"] for r in wins),default=None),
                mean_trades=mean(r["trades"] for r in results), total_fees=sum(r["fees"] for r in results),
                forced_pct=100*mean(r["forced"] for r in results),
                incomplete=sum(bool(r["open"]) for r in results), violations=sum(r["bad"] for r in results))


def pareto(rows):
    def objectives(r):
        return (r["violations"] + r["incomplete"], -r["worst"], r["forced_pct"],
                r["total_fees"], -r["mean"], r["max_time"])
    return [r["family"] for r in rows if not any(
        all(a<=b for a,b in zip(objectives(other),objectives(r))) and objectives(other)!=objectives(r)
        for other in rows)]


def main():
    training = cases(list(named().items()) + [(f"grid_{i}",s) for i,s in enumerate(lattice())])
    benchmarks = named()
    holdout = list(monte_carlo())
    comparison, ledger, optimization, test_summary = [], [], {}, {}
    fixed = {}
    runs = 0
    for profile, cap in PROFILES.items():
        optimized = {}
        for family in FAMILIES:
            candidates = [Policy(family,cap,size,level,limit,horizon,budget)
                          for size,level,limit,horizon,budget in
                          (product(sorted({cap//4,cap//2,cap}), (80,140), (4,8), (8,12), (180,300))
                           if family != "K" else [(cap,80,8,12,300)])]
            # Predeclared conditional category requires profit on both trends under
            # both inherited-lock orientations. Keeps flattening as own baseline.
            def capable(p):
                return all(run(p, benchmarks[direction], side)["pnl"] > 0
                           for direction in ("up","down") for side in (1,-1))
            eligible = [p for p in candidates if capable(p)]
            (rank,p,_), pruned, simulations = search(eligible or candidates, training)
            optimized[family] = dict(policy=vars(p), score=rank, pruned=pruned,
                                     simulations=simulations, candidates=len(candidates),
                                     eligible=len(eligible), status="FINITE_SPACE_OPTIMUM")
            runs += simulations
            for side in (1,-1):
                fixed[f"adv_{profile}_{family}_{side}"] = adversary(p, side)
        optimization[profile] = optimized
    suite = cases(list(named().items()) + holdout + list(fixed.items()))
    for profile, cap in PROFILES.items():
        rows = []
        validated = {}
        for family in FAMILIES:
            p = Policy(**optimization[profile][family]["policy"])
            results = [run(p, seq, side) for _, seq, side in suite]
            row = summarize(profile,p,suite,results)
            rows.append(row)
            validated[family] = score(results)
            test_summary[f"{profile}:{family}"] = {
                "validation_score":validated[family],
                "named":{f"{name}:{side}":r for (name,_,side),r in zip(suite,results) if name in benchmarks}
            }
            if family in ("J","K"):
                for name, seq, side in suite:
                    if name in benchmarks or name == f"adv_{profile}_{family}_{side}":
                        for entry in run(p,seq,side,ledger=True)["rows"]:
                            ledger.append(dict(profile=profile,family=family,scenario=name,
                                               orientation=side,**entry))
        optimization[profile]["pareto_validation_finalists"] = pareto(rows)
        optimization[profile]["validation_minimax"] = min(FAMILIES,key=validated.get)
        eligible = [f for f in FAMILIES if optimization[profile][f]["eligible"]]
        optimization[profile]["validation_recovery"] = min(eligible,key=validated.get) if eligible else None
        comparison.extend(rows)
    controls = {}
    for side in (1,-1):
        b = Book(100,ledger=True)
        b.fill(-1,Event(-side*300),100)
        b.fill(-1,Event(-side*300),-100)
        before = b.realized
        entry = next(i for i,(s,_,_) in enumerate(b.legs) if s==side)
        b.fill(0,Event(0),100,entry)
        winner = b.realized-before-4.5
        controls[str(side)] = dict(cycle=b.mark(Event(0)), winner_net=winner,
                                  loser_net=b.mark(Event(0))-winner)
        for row in b.rows:
            ledger.append(dict(profile="Control", family="control", scenario="300_points",
                               orientation=side, **row))
    write_csv("ALGORITHMS_COMPARISON.csv",comparison)
    write_csv("MONEY_LEDGER.csv",ledger)
    write_json("OPTIMIZATION_RESULTS.json",dict(training_cycles=len(training),
               validation_cycles=len(suite), optimization_simulations=runs, profiles=optimization, status="BEST_FOUND"))
    write_json("TEST_RESULTS.json",dict(controls=controls, validation=test_summary,
               adversarial_paths={name:[vars(e) for e in seq] for name,seq in fixed.items()},
               broker="BROKER_EVIDENCE_UNAVAILABLE"))


if __name__ == "__main__":
    main()
