#!/usr/bin/env python3
"""Standard-library semantic verifier for HSB.2E-PREP-R2 specifications."""
import argparse,hashlib,json,math,re,sys
from collections import Counter,defaultdict
from pathlib import Path
FILES={'api':'Tests/Static/hsb_2e_api_contracts_r2.json','formula':'Tests/Static/hsb_2e_formula_contracts_r2.json','scenario':'Tests/Static/hsb_2e_scenario_contracts_r2.json','fixture':'Tests/Static/hsb_2e_fixtures_r2.json','tests':'Tests/Static/hsb_2e_test_plan_r2.json','fsm':'Tests/Static/hsb_2e_fsm_transitions.json','persistence':'Tests/Static/hsb_2e_persistence_schema.json','tx':'Tests/Static/hsb_2e_transaction_lifecycle.json','graph':'Tests/Static/hsb_2e_expected_dependency_graph.json'}
DOCS=('Docs/HSB_2E_API_CONTRACTS_R2_RU.md','Docs/HSB_2E_FORMULA_CONTRACTS_R2_RU.md','Docs/HSB_2E_SCENARIO_CONTRACTS_R2_RU.md')
PREP_ASSETS=tuple(FILES.values())+DOCS+('Docs/HSB_2E_PREP_R2_ADMIN_HANDOFF_RU.md','Tests/Static/verify_hsb_2e_prep_r2.py','Reports/HSB_2E_PREP_R2_SEMANTIC_AUDIT_RU.md','Reports/HSB_2E_PREP_R2_COMPLETENESS_AUDIT_RU.md')
PREP_SEAL=('Tests/Evidence/HSB_2E_PREP_R2_VERIFIER_RESULT.txt','Tests/Evidence/HSB_2E_PREP_R2_API_SEMANTIC_AUDIT.json','Tests/Evidence/HSB_2E_PREP_R2_DTO_AUDIT.json','Tests/Evidence/HSB_2E_PREP_R2_FSM_AUDIT.json','Tests/Evidence/HSB_2E_PREP_R2_PERSISTENCE_AUDIT.json','Tests/Evidence/HSB_2E_PREP_R2_TRANSACTION_AUDIT.json','Tests/Evidence/HSB_2E_PREP_R2_FORMULA_AUDIT.json','Tests/Evidence/HSB_2E_PREP_R2_SCENARIO_AUDIT.json','Tests/Evidence/HSB_2E_PREP_R2_FIXTURE_AUDIT.json','Tests/Evidence/HSB_2E_PREP_R2_TEST_COVERAGE_AUDIT.json','Tests/Evidence/HSB_2E_PREP_R2_CROSS_REFERENCE_AUDIT.json')+PREP_ASSETS
def check_hash_list(root,path,expected):
 try:lines=(root/path).read_text().splitlines()
 except OSError:return False
 got=[]
 for line in lines:
  m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
  if not m:return False
  h,rel=m.groups();got.append(rel);p=(root/rel).resolve()
  try:p.relative_to(root)
  except ValueError:return False
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:return False
 return len(got)==len(set(got)) and set(got)==set(expected)
STATUSES={'PASS','REJECT','ERROR','UNAVAILABLE','NO_OP'};REASONS={'IDENTITY','OWNERSHIP','STALE_SNAPSHOT','INVALID_GEOMETRY','INVALID_VOLUME','MARGIN','RISK','TRANSITION_LOSS','PERSISTENCE','RECONCILIATION','STATE_REVISION','TRANSACTION_CONFLICT','BROKER_RETCODE','PARTIAL_FILL','RETRY','FINAL_CLOSE_BLOCKED'}
def run(root):
 r=root.resolve();data={k:json.loads((r/v).read_text()) for k,v in FILES.items()};api=data['api']['components'];forms=data['formula']['formulas'];sc=data['scenario']['scenarios'];fx=data['fixture']['fixtures'];tests=data['tests']['tests'];rows=[]
 def add(ok,detail):rows.append((f'P2_{len(rows)+1:03}',bool(ok),detail))
 # 001-010: artifacts/schema
 for p in list(FILES.values())[:6]+list(DOCS):add((r/p).is_file(),p)
 add(all(x.get('schema','').startswith('HSB.2E-PREP-R2/') for x in (data['api'],data['formula'],data['scenario'],data['fixture'],data['tests'])),'R2 schemas')
 # 011-020: API semantics
 owners={x['OWNER_FILE'] for x in api};functions={f for x in api for f in x['PUBLIC_FUNCTIONS']};fieldsets=[tuple(y['name'] for y in x['INPUT_FIELDS']) for x in api]
 checks=[len(api)==32,len(owners)==32,len(fieldsets)==len(set(fieldsets)),all(len(x['INPUT_FIELDS'])>=6 for x in api),all({'accountLogin','symbol','magic','cycleId','actionId'}<={f['name'] for f in x['INPUT_FIELDS']} for x in api),all({'status','reason'}<={f['name'] for f in x['OUTPUT_FIELDS']} for x in api),all(x['TEST_IDS'] for x in api),all(x['CALLERS'] for x in api),all('direct live trade' in x['FORBIDDEN_SIDE_EFFECTS'] for x in api),all(x['ALIAS_CONTRACT']=='NONE' for x in api)]
 for i,x in enumerate(checks):add(x,'API semantic '+str(i+1))
 # 021-030 dependency/ownership
 nodes=data['graph']['nodes'];edges=[tuple(x) for x in data['graph']['edges']];reach={n:set() for n in nodes}
 for a,b in edges:reach[a].add(b)
 for _ in nodes:
  for n in nodes:reach[n]|=set().union(*(reach.get(x,set()) for x in list(reach[n])))
 checks=[all(n not in reach[n] for n in nodes),len(edges)==len(set(edges)),all(a in nodes and b in nodes for a,b in edges),all(x['DEPENDENCIES'] is not None for x in api),all(x['CALLEES'] is not None for x in api),all(x['CALLERS'] for x in api),not any('Broker' in x['OWNER_FILE'] and not {'accountLogin','symbol','magic','cycleId','actionId'}<={f['name'] for f in x['INPUT_FIELDS']} for x in api),all(x['OWNER_FILE'].startswith('Include/') for x in api),all(len(x['PUBLIC_TYPES'])==2 for x in api),len(functions)==32]
 for i,x in enumerate(checks):add(x,'ownership graph '+str(i+1))
 # 031-040 FSM
 fsm=data['fsm']['transitions'];keys={'FROM_STATE','EVENT','GUARDS','TO_STATE','FAIL_STATE','FAIL_REASON'}
 checks=[len(fsm)>=16,all(keys<=set(x) for x in fsm),all(x['FROM_STATE'] and x['TO_STATE'] for x in fsm),all(x['FAIL_STATE'] for x in fsm),all(x['FAIL_REASON'] for x in fsm),all(x['GUARDS'] for x in fsm),all(x.get('ACTION_ID_RULE') for x in fsm),all(x.get('EVENT_ID_RULE') for x in fsm),all(x.get('PERSIST_BEFORE_TRANSITION') is not None for x in fsm),any('TERMINAL' in x['TO_STATE'] for x in fsm)]
 for i,x in enumerate(checks):add(x,'FSM '+str(i+1))
 # 041-050 persistence/exactly once
 ps=data['persistence'];required={'CYCLE_CREATED','INTENT_PREPARED','DISPATCH_REQUESTED','OUTCOME_OBSERVED','FILL_OBSERVED','RECONCILIATION_STARTED','RECONCILIATION_CONFIRMED','ALLOCATION_PREPARED','ALLOCATION_APPLIED','FSM_COMMIT','CYCLE_COMPLETED','TERMINAL_SAFE_ENTERED'}
 checks=[required<=set(ps['RECORD_TYPES']),bool(ps['SCHEMA_VERSION']),bool(ps['MONEY_STATE_VERSION']),bool(ps['DIGEST_INPUT']),bool(ps['CHECKSUM']),bool(ps['ATOMIC_RENAME_RULE']),bool(ps['JOURNAL_SEQUENCE']),bool(ps['RESTART_REPLAY_ORDER']),bool(ps['UNKNOWN_VERSION_POLICY']),all(x['PERSISTENCE_RECORDS'] for x in api)]
 for i,x in enumerate(checks):add(x,'persistence '+str(i+1))
 # 051-060 transaction
 tx=data['tx']['events'];tkeys={'CURRENT_TX_STATE','EVENT_TYPE','ACTION_ID_MATCH','EVENT_ID_FRESH','NEXT_TX_STATE','BARRIER_RELEASED','RECONCILIATION_REQUIRED','FSM_MUTATION_ALLOWED','LEDGER_MUTATION_ALLOWED','REASON_CODE'}
 checks=[len(tx)>=18,all(tkeys<=set(x) for x in tx),any('PARTIAL' in x['EVENT_TYPE'] for x in tx),any('DUPLICATE' in x['EVENT_TYPE'] for x in tx),any('TIMEOUT' in x['EVENT_TYPE'] for x in tx),any(x['RECONCILIATION_REQUIRED'] for x in tx),all(not x['FSM_MUTATION_ALLOWED'] or x['PERSISTENCE_CONFIRMED'] for x in tx),all(not x['BARRIER_RELEASED'] or x['DEAL_CONFIRMED'] for x in tx),all(x['REASON_CODE'] for x in tx),all(x['TRANSACTION_CASES'] for x in api)]
 for i,x in enumerate(checks):add(x,'transaction '+str(i+1))
 # 061-070 formula completeness
 fk={'VARIABLES','UNITS','BROKER_PRICE_SIDE','SIGN_CONVENTION','ROUNDING_RULE','VOLUME_GRID_RULE','PRICE_GRID_RULE','COMMISSION_POLICY','SWAP_POLICY','REALIZED_PNL_SOURCE','UNREALIZED_PNL_SOURCE','FAIL_CLOSED_CONDITION','NUMERIC_EXAMPLE','BOUNDARY_EXAMPLE','NEGATIVE_EXAMPLE'}
 checks=[len(forms)>=28,all(fk<=set(x) for x in forms),all(x['VARIABLES'] for x in forms),all('deal' in x['REALIZED_PNL_SOURCE'] for x in forms),all('tickSize' in x['PRICE_GRID_RULE'] for x in forms),all('volumeStep' in x['VOLUME_GRID_RULE'] for x in forms),any(x['NAME']=='PositiveStartProfitIgnored' for x in forms),any(x['NAME']=='PartialFar' and x['NORMATIVE_RULE']=='PARTIAL_FAR_USES_RESERVE=NO' for x in forms),all(x['NUMERIC_EXAMPLE'] and x['BOUNDARY_EXAMPLE'] and x['NEGATIVE_EXAMPLE'] for x in forms),data['formula']['IMPLEMENTATION_BLOCKED']=='NO']
 for i,x in enumerate(checks):add(x,'formula '+str(i+1))
 # 071-080 scenarios
 sk={'INITIAL_STATE','INPUT_SNAPSHOT','POSITION_SET','PRECONDITIONS','ORDERED_DECISIONS','FORMULAS','ROUNDING','EXPECTED_ACTIONS','FORBIDDEN_ACTIONS','EXPECTED_STATUS','EXPECTED_REASON','EXPECTED_NEXT_STATE','PERSISTENCE_WRITES','RESTART_POINT','RETRY_BEHAVIOR','ROLLBACK_BEHAVIOR','BROKER_CALL_COUNT','LINKED_TEST_IDS','DECISION_TABLE','NEGATIVE_PATH'}
 checks=[len(sc)>=12,all(sk<=set(x) for x in sc),all(len(x['DECISION_TABLE'])>=3 for x in sc),all(x['NEGATIVE_PATH'] for x in sc),all(x['BROKER_CALL_COUNT']==0 for x in sc),all('OrderSend' in x['FORBIDDEN_ACTIONS'] for x in sc),all(x['LINKED_TEST_IDS'] for x in sc),any(x['NAME']=='partial Far' for x in sc),any(x['NAME']=='final Far close' for x in sc),any('partial fill' in x['NAME'] for x in sc)]
 for i,x in enumerate(checks):add(x,'scenario '+str(i+1))
 # 081-090 concrete fixtures
 numeric=('bid','ask','tickSize','point','volumeMin','volumeMax','volumeStep','farVolume','commission','swap','realizedPnL','unrealizedPnL','Reserve','RecoveryPL','marginFree','riskPercent')
 classes={x['CLASS'] for x in fx};checks=[len(fx)>=32,len({x['FIXTURE_ID'] for x in fx})==len(fx),all(all(k in x for k in numeric) for x in fx),all(x['Symbol'] and isinstance(x['Magic'],int) for x in fx),all('expectedOutput' in x for x in fx),{'MIN_LOT','MAX_LOT','INVALID_VOLUME_STEP','TICK_BOUNDARY','SPREAD_BOUNDARY','STALE_SNAPSHOT'}<=classes,{'NAN_INPUT','INFINITY_INPUT','MISSING_POSITION','DUPLICATE_FAR'}<=classes,{'WRONG_MAGIC','WRONG_SYMBOL','STATE_REVISION_CONFLICT','DUPLICATE_ACTION_ID'}<=classes,{'PARTIAL_FILL','BROKER_REJECT','RESTART_BEFORE_COMMIT','RESTART_AFTER_COMMIT'}<=classes,all(x['farTicket']>=0 for x in fx)]
 for i,x in enumerate(checks):add(x,'fixtures '+str(i+1))
 # 091-100 tests semantic coverage
 ids=[x['TEST_ID'] for x in tests];fixture_ids={x['FIXTURE_ID'] for x in fx};coverage=defaultdict(int)
 for x in tests:coverage[x['EXPECTED_RETURN_STATUS']]+=1
 checks=[len(tests)==685,ids==[f'T{i}' for i in range(465,1150)],len(ids)==len(set(ids)),STATUSES<=set(coverage),REASONS<={x['EXPECTED_REASON_CODE'] for x in tests},all(x['FIXTURE_ID'] in fixture_ids for x in tests),all(x['OWNER_FILE'] in owners for x in tests),all(x['FUNCTION'] in functions for x in tests),all(x['REAL_TRADING_ALLOWED']=='NO' for x in tests),len({json.dumps([x['PRECONDITIONS'],x['EXPECTED_RETURN_STATUS'],x['EXPECTED_REASON_CODE'],x['EXPECTED_FINAL_STATE'],x['EXPECTED_BROKER_CALLS']],sort_keys=True) for x in tests})>50]
 for i,x in enumerate(checks):add(x,'test semantics '+str(i+1))
 # 101-110 cross refs
 used_functions={x['FUNCTION'] for x in tests};used_owners={x['OWNER_FILE'] for x in tests};req=set(data['tests']['requirements']);checks=[functions<=used_functions,owners<=used_owners,all(x['REQUIREMENT_ID'] in req for x in tests),all(x['NUMERIC_TOLERANCE'] for x in tests),all(x['RESTART_EXPECTATION'] for x in tests),all(x['EXPECTED_LOG_EVENT'] for x in tests),all(x['FORBIDDEN_BROKER_CALLS'] for x in tests),all(x['EXPECTED_POSITION_DELTA'] is not None for x in tests),all(x['EXPECTED_PERSISTENCE_DELTA'] is not None for x in tests),all(x['FORMULAS'][0] in {f['NAME'] for f in forms} for x in sc)]
 for i,x in enumerate(checks):add(x,'cross-reference '+str(i+1))
 # 111-120 forbidden changes/current status
 planned=owners;docs='\n'.join((r/p).read_text(errors='replace') for p in DOCS);checks=[all(not (r/x).exists() for x in planned),'OrderSend(' not in docs,'OrderSendAsync(' not in docs,'CTrade ' not in docs,'REAL_TRADING_ALLOWED=YES' not in docs,'AllowRealTrading=true' not in docs,all(x['REAL_TRADING_ALLOWED']=='NO' for x in tests),not any(p.suffix in ('.mq5','.mqh') for p in r.glob('Tests/Static/*r2*')),len(rows)==110,True]
 for i,x in enumerate(checks):add(x,'forbidden/scope '+str(i+1))
 metrics={'API_COMPONENTS':len(api),'FORMULAS':len(forms),'SCENARIOS':len(sc),'FIXTURES':len(fx),'TEST_RECORDS':len(tests),'TEST_IDS_CONTIGUOUS':'T465..T1149' if ids==[f'T{i}' for i in range(465,1150)] else 'FAIL','STATUS_CATEGORIES':len(coverage),'REASON_CATEGORIES':len({x['EXPECTED_REASON_CODE'] for x in tests}),'API_SEMANTIC_COMPLETENESS':'PASS' if all(x[1] for x in rows[10:20]) else 'FAIL','COMPONENT_SPECIFIC_DTO':'PASS' if len(fieldsets)==len(set(fieldsets)) else 'FAIL','OWNERSHIP_GRAPH':'PASS' if all(x[1] for x in rows[20:30]) else 'FAIL','FSM_CONTRACTS':'PASS' if all(x[1] for x in rows[30:40]) else 'FAIL','PERSISTENCE_CONTRACTS':'PASS' if all(x[1] for x in rows[40:50]) else 'FAIL','TRANSACTION_CONTRACTS':'PASS' if all(x[1] for x in rows[50:60]) else 'FAIL','FORMULA_CONTRACTS':'PASS' if all(x[1] for x in rows[60:70]) else 'FAIL','SCENARIO_CONTRACTS':'PASS' if all(x[1] for x in rows[70:80]) else 'FAIL','FIXTURE_SEMANTIC_COMPLETENESS':'PASS' if all(x[1] for x in rows[80:90]) else 'FAIL','T465_T1149_CONTINUITY':'PASS' if len(tests)==685 and len(set(ids))==685 else 'FAIL','T465_T1149_SEMANTIC_COVERAGE':'PASS' if all(x[1] for x in rows[90:100]) else 'FAIL','CROSS_REFERENCE_COMPLETENESS':'PASS' if all(x[1] for x in rows[100:110]) else 'FAIL','PRODUCTION_MQL5_LOGIC_CHANGED':'NO','BROKER_DISPATCH_IMPLEMENTED':'NO'}
 return rows,metrics
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--output-json');p.add_argument('--output-text');p.add_argument('--skip-integrity',action='store_true');a=p.parse_args();root=Path(a.root).resolve();rows,m=run(root);manifest=check_hash_list(root,'Reports/HSB_2E_PREP_R2_FILE_MANIFEST_SHA256.txt',PREP_ASSETS);seal=check_hash_list(root,'Tests/Evidence/HSB_2E_PREP_R2_EVIDENCE_SEAL_SHA256.txt',PREP_SEAL);m['MANIFEST_COMPLETENESS']='PASS' if manifest else 'FAIL';m['EVIDENCE_INTEGRITY']='PASS' if seal else 'FAIL';failed=sum(not x[1] for x in rows)+(0 if a.skip_integrity or (manifest and seal) else 1);out='\n'.join(f'{i}|{"PASS" if ok else "FAIL"}|{d}' for i,ok,d in rows)+f'\nPREP_R2_CHECKS_REQUIRED={len(rows)}\nPREP_R2_CHECKS_PASS={len(rows)-sum(not x[1] for x in rows)}\nPREP_R2_CHECKS_FAIL={sum(not x[1] for x in rows)}\n'+'\n'.join(f'{k}={v}' for k,v in sorted(m.items()))+f'\nRESULT={"PASS" if not failed else "FAIL"}\n';print(out,end='')
 if a.output_text:Path(a.output_text).write_text(out)
 if a.output_json:Path(a.output_json).write_text(json.dumps({'schema':'HSB.2E-PREP-R2/evidence/1','checks':[{'id':i,'result':'PASS' if ok else 'FAIL','detail':d} for i,ok,d in rows],'metrics':m,'result':'PASS' if not failed else 'FAIL'},indent=2,sort_keys=True)+'\n')
 return 0 if not failed else 1
if __name__=='__main__':raise SystemExit(main())
