#!/usr/bin/env python3
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def guards():
 o=(ROOT/'Tools'/'stage_3_1_5_money_oracle.py').read_text();m=(ROOT/'Tools'/'stage_3_1_5_mutation_oracle.py').read_text();s=(ROOT/'Tests'/'stage_3_1_5'/'scenario_catalog.py').read_text();v=(ROOT/'Tests'/'validate_stage_3_1_5_money_model.py').read_text();r=(ROOT/'Tests'/'stage_3_1_5'/'restart_fixtures.py').read_text()
 return {'EXPECTED_ALIASES_ACTUAL':int('expected=actual' in s or 'expected_observables=actual_observables' in s),'HARDCODED_TOTALS':int(any(x in s for x in ('return 80','return 65','return 100'))),'UNCONDITIONAL_PASS':int('for status in STATUSES' in v),'PYTEST_OWNER_DEFAULT_TRUE':int("owner=='pytest' else True" in v),'BLOCKER_FROM_MUTATION_NAME':int('int(name in mutations)' in m),'MUTATION_MONEY_ORACLE_MISSING':int('projected_profit(' not in m or 'EconomicLedger(' not in m),'CONSUME_STATE_NOT_CHANGED':int('r.consumed+=amount' not in o),'ALLOCATION_NOT_SERIALIZED':int("'allocations':allocations" not in o),'EVENT_ALLOCATION_UNBOUND':int('event_identity_projection(event.event_id)' not in o),'CONSUME_IDENTITY_UNCHECKED':int("raise ValueError('foreign consume')" not in o),'FINAL_CLOSE_COMPETING_POSITIONS':int('def evaluate_final_close(snapshot:EventSnapshot,store:PersistentStore,positions' in o),'FINAL_CLOSE_BROKER_UNCHECKED':int("reasons.append('BROKER_MISMATCH')" not in o),'REVISION_NOT_UPDATED':int('self.revision+=1' not in o),'RESTART_MANUAL_RECORD_INSERT':int('.records[' in r)}
def main():
 g=guards();[print(f'{k}={x}') for k,x in g.items()];raise SystemExit(any(g.values()))
if __name__=='__main__':main()
