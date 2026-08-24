#!/usr/bin/env python3
"""R5 identity layer retaining all R4-R4 owner and binding predicates."""
import argparse
from hsb_2e_identity_model_r4_r4 import *

IDENTITY_FIELDS=("accountLogin","symbol","magic","cycleId","transactionId","actionId","stateRevision","snapshotId","snapshotVersion")
def same_identity(left,right,fields=IDENTITY_FIELDS): return all(left.get(k)==right.get(k) for k in fields)
def self_test():
    a={k:i for i,k in enumerate(IDENTITY_FIELDS)};b=dict(a);b["actionId"]="foreign"
    checks=[same_identity(a,a),not same_identity(a,b)]
    print(f"IDENTITY_R4_R5_SELF_TESTS={sum(checks)}/{len(checks)}");return all(checks)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
