"""Independent exact pre-action eligibility with a gross hedging model."""
from fractions import Fraction as F
import json
from pathlib import Path

C=json.loads(Path(__file__).with_name("contract.json").read_text())
POINT=F(C["point"])
LOT_UNIT=F(C["lot_unit"])
CONTRACT_UNITS=100000
FEE=F(C["commission_half_cents_per_unit_one_side"],C["half_cents_per_dollar"])/LOT_UNIT
FULL_CAPACITY_UNITS=1000


def assess(entry,activation,orientation,capacity=FULL_CAPACITY_UNITS,available=True):
    """Only the inherited tickets and the quote available before any action."""
    s,t=tuple(entry),tuple(activation)
    reasons=[]
    if (len(s)!=3 or len(t)!=3 or orientation not in (-1,1) or
            any(type(x) is not int for x in (*s,*t))):
        return {"eligible":False,"reasons":["DATA"],"execution":"BROKER_ELIGIBILITY_UNKNOWN"}
    a,bid0,ask0=s
    now,bid,ask=t
    if not (0<=a<now and 0<bid0<=ask0 and 0<bid<=ask):
        reasons.append("DATA")
    gross=2*F(1)
    net=0
    historical_cost=(ask0-bid0)*CONTRACT_UNITS*POINT+2*FEE
    reserve=(ask-bid)*CONTRACT_UNITS*POINT+2*FEE
    balance=F(C["capital"])-historical_cost
    # Buy and sell at a common mid have cancelling midpoint gains.
    mark=-historical_cost-reserve
    quoted_equity=F(C["capital"])+mark
    used=gross*CONTRACT_UNITS*ask*POINT/C["leverage"]
    free=quoted_equity-used
    level=100*quoted_equity/used if used>0 else None
    if used<=0 or quoted_equity<=0 or C["margin_level_bps"]*used>10000*quoted_equity:
        reasons.append("MARGIN")
    if gross>LOT_UNIT*C["max_gross_units"]:
        reasons.append("GROSS")
    if abs(net)>LOT_UNIT*C["max_net_units"]:
        reasons.append("NET")
    if mark>=0 or -mark>C["full_loss_usd"]:
        reasons.append("LOSS")
    if reserve>C["new_cost_usd"]:
        reasons.append("COST")
    if not available or capacity<gross/LOT_UNIT or C["max_net_units"]<=0:
        reasons.append("EXECUTION")
    return dict(eligible=not reasons,reasons=reasons,execution="MODEL_ELIGIBLE" if not reasons else "MODEL_EXCLUDED",
                broker_execution="BROKER_ELIGIBILITY_UNKNOWN",
                balance=float(balance),liquidation_equity=float(quoted_equity),used_margin=float(used),
                free_margin=float(free),margin_level_percent=float(level) if level is not None else None,
                gross=float(gross),net=net,mark=float(mark),exit_reserve=float(reserve),
                historical_cost=float(historical_cost),
                ask=str(F(ask)*POINT),margin_largest_leg_diagnostic=float(used/2),
                stopout_model=bool(used>0 and C["stopout_bps"]*used>=10000*quoted_equity))
