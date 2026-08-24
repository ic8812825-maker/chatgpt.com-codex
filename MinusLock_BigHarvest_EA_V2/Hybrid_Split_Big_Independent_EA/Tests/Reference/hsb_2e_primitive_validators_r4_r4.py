#!/usr/bin/env python3
"""Layer A: scenario-agnostic primitive validators."""
import argparse
from decimal import Decimal,InvalidOperation
D=lambda x:Decimal(str(x))
def decimal_value(v):
 try:x=D(v);return x if x.is_finite() else None
 except (InvalidOperation,ValueError,TypeError):return None
def validate_boolean(v):return None if type(v) is bool else 'BOOLEAN_TYPE_INVALID'
def validate_identifier(v):return None if isinstance(v,str) and 0<len(v.strip())<=128 else 'IDENTIFIER_INVALID'
def validate_revision(v,positive=False):
 x=decimal_value(v)
 return None if x is not None and x==x.to_integral_value() and x>=(1 if positive else 0) else 'REVISION_INVALID'
def validate_timestamp(v):return None if decimal_value(v) is not None and D(v)>=0 else 'TIMESTAMP_INVALID'
def on_grid(v,step):
 x,s=decimal_value(v),decimal_value(step);return x is not None and s is not None and s>0 and x%s==0
def validate_volume(v,step,vmin,vmax,positive=True):
 x,s,lo,hi=map(decimal_value,(v,step,vmin,vmax))
 if None in (x,s,lo,hi) or s<=0 or lo<=0 or hi<lo:return 'VOLUME_DOMAIN_INVALID'
 if x<lo or x>hi or positive and x<=0:return 'VOLUME_MIN_MAX_INVALID'
 return None if on_grid(x,s) else 'VOLUME_OFF_GRID'
def validate_price(v,tick):
 x,t=decimal_value(v),decimal_value(tick)
 if x is None or t is None or x<=0 or t<=0:return 'PRICE_INVALID'
 return None if on_grid(x,t) else 'PRICE_OFF_GRID'
def normalize_volume_grid(v,step):return (D(v)//D(step))*D(step)
def normalize_price_grid(v,tick):return (D(v)//D(tick))*D(tick)
def validate_collection_type(v,kind):return None if type(v) is kind else 'COLLECTION_TYPE_INVALID'
def self_test():
 cases={'BOOL_POS':validate_boolean(True) is None,'BOOL_NEG':validate_boolean('false') is not None,'ID_MALFORMED':validate_identifier(' ') is not None,'REV_BOUNDARY':validate_revision(0) is None,'REV_NEG':validate_revision(-1) is not None,'VOL_POS':validate_volume('1','.01','.01','10') is None,'VOL_ZERO':validate_volume('0','.01','.01','10') is not None,'VOL_GRID':validate_volume('1.005','.01','.01','10')=='VOLUME_OFF_GRID','PRICE_NEG':validate_price('-1','.00001') is not None,'PRICE_GRID':validate_price('1.000005','.00001')=='PRICE_OFF_GRID','COLL':validate_collection_type([],list) is None}
 for k,v in cases.items():print(f'R4_PRIMITIVE_{k}={"PASS" if v else "FAIL"}')
 print(f'PRIMITIVE_R4_R4_SELF_TESTS={sum(cases.values())}/{len(cases)}');return all(cases.values())
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
