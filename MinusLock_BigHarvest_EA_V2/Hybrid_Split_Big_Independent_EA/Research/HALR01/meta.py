"""Receding-horizon controller with exact finite DP on its reduced continuation."""
from copy import deepcopy
from functools import lru_cache
from math import fsum
from preserve import target_net

D = (-300, -150, 0, 150, 300)
OBJECTIVES = ("minimax", "probability", "adjusted")


def weights(previous):
    # Mixture of one uniform draw and one trend-persistent draw.
    return tuple((1 + 5 * (d == previous)) / 10 for d in D)


def utility(pnl, objective):
    if objective == "minimax":
        return pnl / 100
    if objective == "probability":
        return float(pnl > 0)
    return 100 * (pnl > 0) + pnl / 200 - max(0, -pnl - 10000) / 100


def reduce_children(values, previous, objective):
    if objective == "minimax":
        return min(values)
    return fsum(v * w for v, w in zip(values, weights(previous)))


def continuation_actions(net, original, size):
    yield net, original, 0
    yield 0, False, 0
    if not original:
        for candidate in (-size, size):
            opening = abs(candidate) if net * candidate <= 0 else max(0, abs(candidate)-abs(net))
            yield candidate, False, opening * 29


@lru_cache(maxsize=200000)
def dp(depth, pnl, net, original, previous, size, budget, objective):
    if depth == 0 or pnl > 0:
        return utility(pnl, objective)
    best = utility(pnl, objective)  # immediate DONE at the present mark
    for target, stays_a, cost in continuation_actions(net, original, size):
        mark = pnl - cost
        if mark - 300 * abs(target) < -budget:
            continue
        values = [dp(depth-1, mark+target*d, target, stays_a, d, size, budget, objective)
                  for d in D]
        best = max(best, reduce_children(values, previous, objective))
    return best


class Meta:
    def __init__(self, p, budget, objective):
        self.p, self.budget, self.objective = p, budget, objective
        self.last = 0
        self.action = "WAIT"
        self.stopped = False

    def candidates(self, book, q):
        a = any(t.original for t in book.tickets.values())
        yield ("HOLD" if book.gross else "WAIT"), book
        closed = deepcopy(book)
        closed.flatten(q)
        yield "FULL_CLOSE", closed
        if not closed.gross:
            yield "SWITCH_TO_B" if a else "DONE", closed
        if a:
            for side in (-book.orientation, book.orientation):
                trial = deepcopy(book)
                target_net(trial, q, side*self.p.net)
                yield "PARTIAL_CLOSE", trial
                trial = deepcopy(book)
                target_net(trial, q, side*self.p.net,
                           {i: t.units for i, t in book.tickets.items() if t.original})
                yield "ADJUST_NET", trial
        else:
            for side in (-book.orientation, book.orientation):
                trial = deepcopy(book)
                target_net(trial, q, side*self.p.net)
                yield "OPEN_RECOVERY" if not book.gross else "ADJUST_NET", trial
        if book.net:
            for label, size in (("REHEDGE", 0), ("HARVEST", round(book.net/2))):
                trial = deepcopy(book)
                target_net(trial, q, size)
                yield label, trial

    def act(self, book, q, step):
        if self.stopped:
            book.flatten(q)
            return
        delta = q.mid - self.last
        self.last = q.mid
        previous = min(D, key=lambda d: abs(d - delta))
        depth = min(2, self.p.horizon - step)
        best = None
        for label, trial in self.candidates(book, q):
            state = trial.snapshot(q)
            mark = round(100 * state["pnl"])
            net = trial.net
            budget = round(100 * (self.budget-self.p.reserve))
            if trial.gross and mark - 300 * abs(net) < -budget:
                continue
            old = any(t.original for t in trial.tickets.values())
            cost = trial.costs - book.costs
            if not trial.gross and label == "FULL_CLOSE":
                score = utility(mark, self.objective)
            else:
                values = [dp(depth-1, mark+net*d, net, old, d,
                             self.p.net, budget, self.objective) for d in D]
                score = reduce_children(values, previous, self.objective)
            if self.objective == "adjusted":
                score -= .15 * cost
            key = score, -trial.gross, -cost, -abs(net),
            key += (self.objective != "minimax" and label != "FULL_CLOSE",)
            if best is None or key > best[0]:
                best = key, label, trial
        if best is None:
            self.action = "SAFE"
            self.stopped = True
            book.flatten(q)
        else:
            _, self.action, trial = best
            book.__dict__.update(trial.__dict__)
            if self.action == "FULL_CLOSE" and not book.gross:
                self.stopped = True
                self.action = "DONE"
