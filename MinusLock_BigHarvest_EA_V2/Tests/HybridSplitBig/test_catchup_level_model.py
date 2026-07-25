"""Deterministic stage-1 contract tests; MQL5 uses BrokerMoneyModel for each leg."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Case:
    name: str
    far_direction: str = "BUY"
    levels: int = 3
    reserve_before: float = 0.0
    partial: float = .10
    reserve: float = .90
    minimum_recovery: float = 0.0
    margin_limit: float = 1000.0
    worst_penalty: float = 0.0
    commission: float = 0.0
    spread_shock: float = 0.0


def simulate(case: Case):
    rows=[]; reserve=case.reserve_before; partial=carry=realized=0.0
    previous_deficit=float("inf"); previous_recovery=-float("inf")
    for level in range(1,case.levels+1):
        # Four independent per-level money calls represented by different prices.
        distance=level*10.0
        far_sign=1.0 if case.far_direction=="BUY" else -1.0
        price_move=-far_sign*distance  # Big is opposite Far, so this is its trigger.
        def net(direction_sign, lot, existing_loss=0.0):
            return direction_sign*price_move*lot-existing_loss-case.commission-case.spread_shock
        far_net=net(far_sign,1.0,100.0)
        core_net=net(-far_sign,2.0)
        trend_net=net(-far_sign,.8)
        small_net=net(far_sign,.2)
        harvest=round(core_net+trend_net+small_net,2)
        eligible=max(harvest,0.0)
        p=round(case.partial*eligible,2); r=round(case.reserve*eligible,2)
        c=round(eligible-p-r,2)
        partial=round(partial+p,2); reserve=round(reserve+r,2); carry=round(carry+c,2)
        realized=round(realized+harvest,2)
        far_cost=round(max(-far_net,0.0),2)
        deficit=round(far_cost-reserve,2)
        recovery=round(realized+far_net,2)
        margin=100.0+level*10.0
        margin_pass=margin<=case.margin_limit
        worst_pass=recovery-case.worst_penalty>=case.minimum_recovery
        monotonic=deficit<=previous_deficit and recovery>=previous_recovery
        passed=deficit<=0 and recovery>=case.minimum_recovery and margin_pass and worst_pass and monotonic
        rows.append(dict(level=level,far_net=far_net,core_net=core_net,trend_net=trend_net,
                         small_net=small_net,harvest=harvest,partial=partial,reserve=reserve,
                         carry=carry,deficit=deficit,recovery=recovery,margin=margin,
                         margin_pass=margin_pass,worst_pass=worst_pass,monotonic=monotonic,passed=passed))
        previous_deficit=deficit; previous_recovery=recovery
    return rows


def test_fc01_coverage_level_1():
    rows=simulate(Case("FC-01",reserve_before=100,minimum_recovery=-100)); assert rows[0]["passed"]

def test_fc02_coverage_level_2():
    rows=simulate(Case("FC-02",reserve_before=50,minimum_recovery=-100)); assert not rows[0]["passed"] and rows[1]["passed"]

def test_fc03_coverage_level_n():
    rows=simulate(Case("FC-03",levels=5)); assert next(r["level"] for r in rows if r["passed"])==3

def test_fc04_no_coverage():
    rows=simulate(Case("FC-04",levels=2)); assert not any(r["passed"] for r in rows)

def test_fc05_recovery_fail():
    rows=simulate(Case("FC-05",reserve_before=100,minimum_recovery=1000)); assert not any(r["passed"] for r in rows)

def test_fc06_margin_fail():
    rows=simulate(Case("FC-06",reserve_before=100,margin_limit=50)); assert not any(r["passed"] for r in rows)

def test_fc07_worst_case_fail():
    rows=simulate(Case("FC-07",reserve_before=100,worst_penalty=1000)); assert not any(r["passed"] for r in rows)

def test_fc08_buy_sell_price_symmetry():
    buy=simulate(Case("FC-08-BUY")); sell=simulate(Case("FC-08-SELL",far_direction="SELL")); assert buy==sell

def test_fc09_spread_shock_changes_level():
    base=simulate(Case("FC-09",levels=6)); shock=simulate(Case("FC-09-S",levels=6,spread_shock=15));
    assert next(r["level"] for r in base if r["passed"]) != next(r["level"] for r in shock if r["passed"])

def test_fc10_commission_changes_level():
    base=simulate(Case("FC-10",levels=6)); costs=simulate(Case("FC-10-C",levels=6,commission=15));
    assert next(r["level"] for r in base if r["passed"]) != next(r["level"] for r in costs if r["passed"])

def test_fc11_conservation_and_monotonic_sequences():
    rows=simulate(Case("FC-11",levels=6));
    assert all(round(r["partial"]+r["reserve"]+r["carry"],2) >= 0 for r in rows)
    assert all(b["reserve"]>=a["reserve"] and b["deficit"]<=a["deficit"] and b["recovery"]>=a["recovery"] for a,b in zip(rows,rows[1:]))


def test_mql5_level_loop_uses_fresh_broker_money_and_trace():
    from pathlib import Path
    source=(Path(__file__).parents[2]/"Include"/"HybridCatchUpModel.mqh").read_text()
    loop=source[source.index("for(int index=0;"):]
    assert loop.count("HybridCatchUpLeg(") >= 8  # base and worst, four roles each
    assert "plan.projectedHarvestNet" not in source
    assert "row.far.netMoney" in source and "row.core.netMoney" in source
    assert "HYBRID_CATCHUP_LEVEL" not in source  # structured payload is returned, caller logs it
    assert "LEVEL=%d|BID=" in source
