#!/usr/bin/env python3
"""R5 primitive layer: strict types and Decimal grids; strengthens R4-R4."""
import argparse
from decimal import Decimal, InvalidOperation
from hsb_2e_primitive_validators_r4_r4 import *  # retained implementation, not rewritten

def strict_revision(value, positive=False):
    return type(value) is int and value >= (1 if positive else 0)

def self_test():
    checks=[validate_boolean(True) is None,validate_boolean("true") is not None,strict_revision(0),not strict_revision(-1),not strict_revision(1.5),validate_volume(".10",D(".01"),D(".01"),D("10")) is None]
    print(f"PRIMITIVE_R4_R5_SELF_TESTS={sum(checks)}/{len(checks)}");return all(checks)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
