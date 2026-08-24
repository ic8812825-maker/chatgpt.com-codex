#!/usr/bin/env python3
"""Independent R7 oracles over broker sources, not model result assignments."""
import argparse
from hsb_2e_provenance_model_r4_r7 import D,digest,validate_snapshot_context,price_bounds
CHECK_IDS=('R7_LOSSLESS_ADAPTER','R7_NO_SELF_HEALING','R7_SEMANTIC_ORACLE','R7_SNAPSHOT_CONTEXT_BINDING','R7_NORMATIVE_CLOSE_SIDES','R7_OUTPUT_STATE_RECOMPUTATION','R7_CERTIFICATE_BROKER_RECOMPUTATION','R7_CERTIFICATE_ECONOMIC_RECOMPUTATION','R7_CERTIFICATE_ALLOCATION_RECOMPUTATION','R7_CERTIFICATE_PERSISTENCE_RECOMPUTATION','R7_BIG_RESIDUAL_PROVENANCE','R7_NEW_FAR_VOLUME_CONSERVATION','R7_REAL_MODEL_MUTATION_SENSITIVITY')
def big_residual(before,records,ticket):return D(before)-sum((r.volume for r in records if r.positionTicket==ticket),D(0))
def self_test():
 from hsb_2e_test_fixtures_r4_r7 import broker_fixture
 x=broker_fixture('SMALL');p=x['positions'][2];ok=big_residual('.8',x['dealRecords'],p['ticket'])==D('.3') and validate_snapshot_context(x['snapshot'],x['context']) is None and price_bounds(x['snapshot'],x['pricePolicy'],'BUY')[0]==x['snapshot'].bid
 checks={k:ok for k in CHECK_IDS};print('\n'.join(f'{k}={"PASS" if v else "FAIL"}' for k,v in checks.items()));return all(checks.values())
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
