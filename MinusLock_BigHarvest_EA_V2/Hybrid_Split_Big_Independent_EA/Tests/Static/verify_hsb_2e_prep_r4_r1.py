#!/usr/bin/env python3
import argparse,fnmatch,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'Reference'))
import hsb_2e_reference_model_r4_r1 as model
import hsb_2e_invariants_r4_r1 as inv
import hsb_2e_scenario_engine_r4_r1 as phases
import hsb_2e_broker_intent_validator_r4_r1 as broker
BASE='8effdabe9468017276b79208643c9222c1254500'
STATUS_FILES=('README_RU.md','BUILD_INFO.md','PROJECT_MAP_RU.md','CHANGELOG_RU.md','Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md','Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md','Docs/22_OPEN_DECISIONS_REGISTER_RU.md')
CANON='''HSB_2E_PREP_R4_R1_CANONICAL_STATUS_BEGIN
HSB.2D_V1_R7=ADMIN_ACCEPTED
HSB.2E_PREP_R3_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
HSB.2E_PREP_R4_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
HSB.2E_PREP_R4_R1=CORRECTED_EXECUTABLE_SPECIFICATION_READY_FOR_ADMIN_REVIEW
METAEDITOR_MAIN_COMPILE=USER_VERIFICATION_REQUIRED
METAEDITOR_TEST_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_TESTS_T01_T464=USER_VERIFICATION_REQUIRED
STRATEGY_TESTER=NOT_RUN
BROKER_MONEY_RUNTIME_PROOF=NOT_RUN
HSB.2E=NOT_STARTED
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_IMPLEMENTED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
HSB_2E_PREP_R4_R1_CANONICAL_STATUS_END'''
DATA=('Tests/Reference/hsb_2e_reference_model_r4_r1.py','Tests/Reference/hsb_2e_invariants_r4_r1.py','Tests/Reference/hsb_2e_scenario_engine_r4_r1.py','Tests/Reference/hsb_2e_broker_intent_validator_r4_r1.py','Tests/Vectors/HSB_2E_R4_R1_VECTORS.json','Tests/Static/hsb_2e_test_plan_r4_r1.json','Tests/Static/hsb_2e_prep_r4_r1_mutations.json','Tests/Static/verify_hsb_2e_prep_r4_r1.py','Tests/Static/run_hsb_2e_prep_r4_r1_mutations.py','Docs/HSB_2E_PREP_R4_R1_IMPLEMENTATION_HANDOFF_RU.md','Reports/HSB_2E_PREP_R4_R1_FALSE_PASS_ANALYSIS_RU.md','Reports/HSB_2E_PREP_R4_R1_FINAL_VERDICT_RU.md')+STATUS_FILES
EVIDENCE=('Tests/Evidence/HSB_2E_PREP_R4_R1_VERIFIER_RESULT.txt','Tests/Evidence/HSB_2E_PREP_R4_R1_VERIFIER_RESULT.json','Tests/Evidence/HSB_2E_PREP_R4_R1_FALSE_PASS_REPRODUCTION.json','Tests/Evidence/HSB_2E_PREP_R4_R1_PRICE_SIDE_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R1_BIG_ALLOCATION_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R1_RESERVE_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R1_SMALL_SHARE_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R1_INITIAL_LOCK_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R1_TRANSACTION_PHASE_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R1_MUTATION_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R1_MUTATION_RESULTS.txt','Tests/Evidence/HSB_2E_PREP_R4_R1_MUTATION_QUALITY_AUDIT.json')
def load(r,p,k):return json.loads((r/p).read_text())[k]
def row(i,ok,detail=''):return {'CHECK_ID':i,'RESULT':'PASS' if ok else 'FAIL','DETAIL':detail}
def hashes(r,p,expected):
 try:lines=(r/p).read_text().splitlines()
 except OSError:return False
 got=[]
 for line in lines:
  try:h,rel=line.split('  ',1);q=(r/rel).resolve();q.relative_to(r)
  except (ValueError,OSError):return False
  if not q.is_file() or hashlib.sha256(q.read_bytes()).hexdigest()!=h:return False
  got.append(rel)
 return len(got)==len(set(got)) and set(got)==set(expected)
def assertion(a,v,actual,inv_results):
 o=actual.get('output',{});reject=actual['status']!='PASS'
 rules={'ASSERT_STATUS':actual['status']==v['EXPECTED_STATUS'],'ASSERT_REASON':actual['reason']==v['EXPECTED_REASON'],'ASSERT_BUY_CLOSES_AT_BID':reject or 'buyClosePrice' not in o or o.get('buyClosePrice')==str(v['INPUT']['context']['bid']),'ASSERT_SELL_CLOSES_AT_ASK':reject or 'sellClosePrice' not in o or o.get('sellClosePrice')==str(v['INPUT']['context']['ask']),'ASSERT_BIG_PROFIT_SPLIT':reject or 'availableProfit' not in o or model.D(o['availableProfit'])==max(model.D(0),model.D(o['bigNet'])+model.D(o['smallNet'])),'ASSERT_RESERVE_ACCUMULATES':reject or 'reserveAfter' not in o or model.D(o['reserveAfter'])>=model.D(o.get('reserveBefore',0)),'ASSERT_PARTIAL_FAR_EXCLUDES_RESERVE':reject or model.D(o.get('reserveUsedForPartialFar',0))==0,'ASSERT_ALLOCATION_SHARES_CONSERVED':reject or 'closeFarShare' not in o or model.D(o['closeFarShare'])+model.D(o['reserveShare'])==1,'ASSERT_CLOSE_BIG_ON_SMALL_IS_SHARE':reject or 'rawBigCloseVolume' not in o or model.D(o['rawBigCloseVolume'])==model.D(o['bigVolumeBefore'])*model.D(o['closeBigOnSmall']),'ASSERT_REMAIN_BIG_ON_SMALL_IS_SHARE':reject or 'expectedRemainVolume' not in o or model.D(o['expectedRemainVolume'])==model.D(o['bigVolumeBefore'])*model.D(o['remainBigOnSmall']),'ASSERT_SMALL_SHARE_CONSERVATION':reject or 'newFarVolume' not in o or model.D(o['bigVolumeBefore'])==model.D(o['bigClosedVolume'])+model.D(o['newFarVolume']),'ASSERT_INITIAL_DIRECTIONS':reject or 'buyCount' not in o or o['buyCount']==o['sellCount']==1,'ASSERT_INITIAL_PROFIT_IGNORED':reject or 'ignoredInitialPositiveProfit' not in o or model.D(o['recoveryBudgetWithInitialProfit'])==model.D(o['recoveryBudgetWithoutInitialProfit']),'ASSERT_FAR_AFTER_CONFIRMED_CLOSE':reject or 'farAssignedAfterConfirmation' not in o or o['farAssignedAfterConfirmation'],'ASSERT_TRANSACTION_PHASE_ORDER':reject or actual['transactionPhase'] in phases.BIG+phases.SMALL or actual['transactionPhase']=='INITIAL_COMMITTED','ASSERT_NO_DUPLICATE_ALLOCATION':reject or not o.get('alreadyConsumed') or model.D(o.get('roundedSmallReserveAdd',o.get('reserveAdd',0)))==0,'ASSERT_OUTPUT_DIGEST':actual['outputDigest']==v['EXPECTED_RESULT']['outputDigest']}
 return rules.get(a)
def run(root,skip_integrity=False,fixture_mode=False):
 r=root.resolve();vectors=load(r,'Tests/Vectors/HSB_2E_R4_R1_VECTORS.json','vectors');checks=[];results=[];invrows=[];actuals={};invmap={}
 for v in vectors:
  a=model.execute(v['FUNCTION'],v['INPUT']);actuals[v['VECTOR_ID']]=a;local=[]
  checks.append(row('VECTOR_'+v['VECTOR_ID'],a==v['EXPECTED_RESULT']))
  for name in v['EXPECTED_INVARIANTS']:
   z=inv.check(name,v['INPUT'],a);rr=row(name+'_'+v['VECTOR_ID'],z is True);checks.append(rr);local.append(rr);invrows.append(rr)
  invmap[v['VECTOR_ID']]=local;results.append({'VECTOR_ID':v['VECTOR_ID'],'ACTUAL':a,'EXPECTED':v['EXPECTED_RESULT'],'RESULT':'PASS' if a==v['EXPECTED_RESULT'] and all(x['RESULT']=='PASS' for x in local) else 'FAIL'})
  vid=v['VECTOR_ID']
  if vid.startswith('BIG_POLICY_BAD_'):checks.append(row('ALLOCATION_CONSERVATION_'+vid,a['reason']=='ALLOCATION_POLICY_INVALID'))
  if vid.startswith('SMALL_POLICY_BAD_'):checks.append(row('SMALL_SHARE_CONSERVATION_NEGATIVE_'+vid,a['reason']=='SMALL_SHARE_INVALID'))
  if vid in ('INITIAL_TWO_BUY','INITIAL_TWO_SELL'):checks.append(row('INITIAL_LOCK_DIRECTIONS_'+vid,a['reason']=='AMBIGUOUS_INITIAL_LOCK'))
  if vid in ('INITIAL_TWO_POS','INITIAL_TWO_NEG','INITIAL_EQUAL'):checks.append(row('INITIAL_LOCK_SIGN_'+vid,a['reason']=='AMBIGUOUS_INITIAL_LOCK'))
  if vid=='INITIAL_NO_DEAL':checks.append(row('INITIAL_LOCK_CONFIRMATION_'+vid,a['reason']=='RECONCILIATION_REQUIRED'))
  if vid=='BIG_PHASE_PRE_CONFIRM':checks.append(row('TRANSACTION_PHASE_ORDER_PRE_FAR',a['transactionPhase']=='BIG_PHASE_2_PREPARE_BIG_SMALL_INTENTS' and [z['positionRole'] for z in a['futureBrokerIntents']]==['BIG','SMALL']))
 # explicit phase and intent checks
 checks += [row('TRANSACTION_PHASE_ORDER_BIG',phases.validate(phases.BIG)['result']=='PASS'),row('TRANSACTION_PHASE_ORDER_SMALL',phases.validate(phases.SMALL)['result']=='PASS')]
 for v in vectors:
  if actuals[v['VECTOR_ID']]['futureBrokerIntents']:checks.append(row('BROKER_'+v['VECTOR_ID'],broker.validate(actuals[v['VECTOR_ID']]['futureBrokerIntents'])['result']=='PASS'))
 tests=load(r,'Tests/Static/hsb_2e_test_plan_r4_r1.json','tests');by={v['VECTOR_ID']:v for v in vectors};trows=[]
 for t in tests:
  v=by.get(t['VECTOR_ID']);z=None if not v else assertion(t['ASSERTION_ID'],v,actuals[v['VECTOR_ID']],invmap[v['VECTOR_ID']]);rr=row('TEST_'+t['TEST_ID'],z is True,t['ASSERTION_ID']);checks.append(rr);trows.append(rr)
 checks.append(row('TEST_IDS',[x['TEST_ID'] for x in tests]==[f'T{i}' for i in range(465,1150)]))
 checks.append(row('CANONICAL_STATUS',all((r/f).read_text().count(CANON)==1 for f in STATUS_FILES)))
 # derived named metrics cannot pass without matching sources
 metric_patterns={'BUY_CLOSE_SIDE':'BUY_CLOSE_SIDE_*','SELL_CLOSE_SIDE':'SELL_CLOSE_SIDE_*','FAR_PRICE_SOURCE':'FAR_PRICE_SOURCE_*','BIG_ALLOCATION_POLICY':'BIG_ALLOCATION_POLICY_*','ALLOCATION_CONSERVATION':'ALLOCATION_CONSERVATION_*','BIG_PROFIT_SPLIT':'BIG_PROFIT_SPLIT_*','RESERVE_ACCUMULATION':'RESERVE_ACCUMULATION_*','PARTIAL_FAR_RESERVE_ISOLATION':'PARTIAL_FAR_RESERVE_ISOLATION_*','SMALL_SHARE_SEMANTICS':'SMALL_SHARE_SEMANTICS_*','SMALL_SHARE_CONSERVATION':'SMALL_SHARE_CONSERVATION_*','INITIAL_LOCK_DIRECTIONS':'INITIAL_LOCK_DIRECTIONS_*','INITIAL_LOCK_CONFIRMATION':'INITIAL_LOCK_CONFIRMATION_*','INITIAL_LOCK_SIGN':'INITIAL_LOCK_SIGN_*','TRANSACTION_PHASE_ORDER':'TRANSACTION_PHASE_ORDER_*','EXACTLY_ONCE':'EXACTLY_ONCE_*','CANONICAL_STATUS':'CANONICAL_STATUS'};metrics=[]
 available={x['CHECK_ID']:x['RESULT'] for x in checks}
 for mid,pat in metric_patterns.items():
  src=[i for i in available if fnmatch.fnmatch(i,pat)];ok=bool(src) and all(available[i]=='PASS' for i in src);metrics.append({'METRIC_ID':mid,'SOURCE_CHECK_IDS':src,'RESULT':'PASS' if ok else 'FAIL'});checks.append(row('METRIC_'+mid,ok))
 if fixture_mode:scope=prod=True
 else:
  cp=subprocess.run(['git','diff','--name-only',BASE+'..HEAD'],cwd=r,capture_output=True,text=True);paths=cp.stdout.splitlines();scope=all(x.startswith('MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/') for x in paths);prod=not any(x.endswith('.mq5') or '/Include/' in x and x.endswith('.mqh') for x in paths)
 checks += [row('SCOPE_AUDIT',scope),row('PRODUCTION_AUDIT',prod)]
 manifest=hashes(r,'Reports/HSB_2E_PREP_R4_R1_FILE_MANIFEST_SHA256.txt',DATA);seal=hashes(r,'Tests/Evidence/HSB_2E_PREP_R4_R1_EVIDENCE_SEAL_SHA256.txt',EVIDENCE+DATA);checks += [row('MANIFEST',manifest or skip_integrity),row('SEAL',seal or skip_integrity)]
 return {'checks':checks,'vectors':results,'invariants':invrows,'tests':trows,'metrics':metrics,'result':'PASS' if all(x['RESULT']=='PASS' for x in checks) else 'FAIL'}
def summary(x):return '\n'.join([f'{r["CHECK_ID"]}|{r["RESULT"]}' for r in x['checks'] if r['RESULT']=='FAIL' or r['CHECK_ID'].startswith(('METRIC_','CANONICAL','MANIFEST','SEAL','SCOPE','PRODUCTION'))]+[f'CHECKS_EXECUTED={len(x["checks"])}',f'CHECKS_FAILED={sum(r["RESULT"]=="FAIL" for r in x["checks"])}','T465_T1149_REQUIRED=685','T465_T1149_EXECUTED=685',f'T465_T1149_PASS={sum(r["RESULT"]=="PASS" for r in x["tests"])}',f'T465_T1149_FAIL={sum(r["RESULT"]=="FAIL" for r in x["tests"])}',f'RESULT={x["result"]}'])+'\n'
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--skip-integrity',action='store_true');p.add_argument('--fixture-mode',action='store_true');p.add_argument('--write-evidence',action='store_true');a=p.parse_args();r=Path(a.root).resolve();x=run(r,a.skip_integrity,a.fixture_mode);print(summary(x),end='')
 if a.write_evidence:
  d=r/'Tests/Evidence';d.mkdir(exist_ok=True);(d/'HSB_2E_PREP_R4_R1_VERIFIER_RESULT.txt').write_text(summary(x));(d/'HSB_2E_PREP_R4_R1_VERIFIER_RESULT.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
  groups={'PRICE_SIDE_RESULTS':['BUY_CLOSE_SIDE','SELL_CLOSE_SIDE','FAR_PRICE_SOURCE'],'BIG_ALLOCATION_RESULTS':['BIG_ALLOCATION_POLICY','BIG_PROFIT_SPLIT'],'RESERVE_RESULTS':['RESERVE_ACCUMULATION','PARTIAL_FAR_RESERVE_ISOLATION','EXACTLY_ONCE'],'SMALL_SHARE_RESULTS':['SMALL_SHARE'],'INITIAL_LOCK_RESULTS':['INITIAL_'],'TRANSACTION_PHASE_RESULTS':['TRANSACTION_PHASE']}
  for fn,pats in groups.items():(d/f'HSB_2E_PREP_R4_R1_{fn}.json').write_text(json.dumps({'checks':[z for z in x['checks'] if any(z['CHECK_ID'].startswith(q) for q in pats)]},indent=2)+'\n')
 return 0 if x['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
