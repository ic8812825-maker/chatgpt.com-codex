#!/usr/bin/env python3
"""Детерминированная property-style матрица взаимно согласованных повреждений."""
import json
from exploit_regressions import payload
from stage_3_1_5_money_oracle import PersistentStore,OracleIntegrityError,IntegrityCode

def run():
 results=[]
 for allocation,residual in ((6,0),(5,1),(7,2),(10,1),(101,99)):
  x=payload();x['allocations'][0]['amount']=str(allocation);x['allocations'][0]['residual']=str(residual)
  x['source_pools'][0].update(allocated=str(allocation),residual=str(residual),available=str(5-allocation-residual),revision=x['allocations'][0]['revision'])
  actual=None
  try:PersistentStore.deserialize(json.dumps(x))
  except OracleIntegrityError as exc:actual=exc.code
  results.append(actual is IntegrityCode.SOURCE_POOL_CONSERVATION_FAILURE)
 return results
if __name__=='__main__':
 result=run();print(f'CORRELATED_CASES={len(result)}');print('CORRELATED_PERSISTENCE_ATTACKS='+('PASS' if all(result) else 'FAIL'));raise SystemExit(0 if all(result) else 1)
