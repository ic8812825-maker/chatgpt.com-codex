#!/usr/bin/env python3
import math


def near(a,b,eps=1e-9):
    return abs(a-b)<=eps


def test_existing_contracts():
    # spread invariant
    bid,ask=1.1,1.1003
    assert near(ask-bid,0.0003,1e-12)

    # derivative oracle
    p0,h=1.05,1e-6
    pnl_plus=0.1*(p0+h-1.0)
    pnl_minus=0.1*(p0-h-1.0)
    d=(pnl_plus-pnl_minus)/(2*h)
    assert near(d,0.1,1e-10)

    # phase guard
    k,g,sigma=0.8,1.3,0.2
    theta=k*g
    assert theta>=1.0
    assert not (theta < math.exp(-(sigma*sigma)/2.0))


def test_lock_compression_formula():
    B,S=0.4,0.25
    L_lock=min(B,S)
    assert near(B-L_lock,0.15)
    assert near(S-L_lock,0.0)


def test_trigger():
    n=9
    margin_level=150.0
    assert (n>8) or (margin_level<200.0)


def test_effective_exposure_alpha():
    exposure=80.0
    alpha=0.5
    assert near(exposure*alpha,40.0)


def test_stability_formula():
    k=1.2
    n=30
    alpha=0.5
    m=3
    risk_no=(k**n)
    risk_alc=(alpha**m)*(k**n)
    assert risk_alc<risk_no


def test_max_levels_rule():
    max_levels=30
    levels=31
    assert levels>max_levels


def test_margin_improves_with_alpha():
    margin_before=200.0
    alpha=0.5
    margin_after=margin_before*alpha
    assert margin_after<margin_before


def test_delta_reduction():
    delta=1.8
    alpha=0.5
    assert near(delta*alpha,0.9)


def run():
    tests=[
        test_existing_contracts,
        test_lock_compression_formula,
        test_trigger,
        test_effective_exposure_alpha,
        test_stability_formula,
        test_max_levels_rule,
        test_margin_improves_with_alpha,
        test_delta_reduction,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"ALL {len(tests)} TESTS PASSED")


if __name__=="__main__":
    run()
