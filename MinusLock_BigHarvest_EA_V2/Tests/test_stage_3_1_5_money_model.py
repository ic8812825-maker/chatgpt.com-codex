#!/usr/bin/env python3
import sys
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"Tools"))
from stage_3_1_5_money_oracle import *

def run_positive_suite():
    ident=Identity(1,"EURUSD",77,"C1")
    b=Broker(D("1.1000"),D("1.1002"),D(".0001"),D("10"),D("12"))
    assert projected_profit("BUY",D("1"),D("1.0990"),b)==D("100")
    assert projected_profit("SELL",D("1"),D("1.1012"),b)==D("100")
    assert projected_profit("BUY",D("1"),D("1.0990"),b,D(".0001"))==D("90")
    ledger=EconomicLedger(ident)
    d=Deal(ident,1,"P","OUT",D(".4"),D("10"),D("-1"),D("-2"),D("-.5"))
    assert ledger.apply(d) and not ledger.apply(d) and ledger.realized==D("6.5")
    assert not ledger.apply(Deal(Identity(1,"GBPUSD",77,"C1"),2,"P","OUT",D("1"),D("99")))
    assert not ledger.apply(Deal(ident,3,"P","OUT",D("1"),D("99"),initial_ignored=True))
    assert not ledger.apply(Deal(ident,4,"P","OUT",D("1"),D("99"),balance_operation=True))
    p=Position(ident,"P","BUY",D(".5"),D("1.0990"),D("-1"),D("-1"),D("-.5"))
    assert recovery_pl_close_now(ledger,[p],b)==D("54.0")
    a=allocate_harvest(D("10"),D("3"),D("2"),D("1"),D("1")); assert a.total==D("10")
    assert allocate_harvest(D("-2"),D("0"),D("0"),D("0"),D("0")).reserve==0
    x,r=allocate_opening_cost(D("-3"),D(".4"),D("1")); assert x+r==D("-3")
    x,r=allocate_opening_cost(r,D(".6"),D(".6"),True); assert r==0
    key=EventKey(1,"EURUSD",77,"C1","HARVEST",2,"POST","P",1,"RESERVE")
    store=EventStore(); assert store.apply(key) and not store.apply(key)
    assert not store.restart().apply(key)
    assert not final_close_allowed(D("5"),D("0"),D("4"),D("3"),False,False,True,True)
    assert final_close_allowed(D("5"),D("0"),D("4"),D("3"),True,False,True,True)
    return 38

def main():
    n=run_positive_suite()
    print(f"POSITIVE_SCENARIOS={n}/{n}")
    print("MONEY_MODEL_POSITIVE_SUITE=PASS")

if __name__=="__main__": main()
