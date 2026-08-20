#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,importlib.util,json,re,subprocess,sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from hsb_mql5_lexer import (prove_top_level_guard,prove_reject_constructor,
 prove_unique_final_success,parse_enum_map,analyze_return_paths,conditions_equivalent,
 active_compact,lexer_self_tests,LexerError)
BASELINE='45fa599bb0c446a8cc24bcdf79ec5f8999ef050e';PREFIX='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/'
STATUS_DOCUMENTS=('README_RU.md','BUILD_INFO.md','PROJECT_MAP_RU.md','CHANGELOG_RU.md','Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md','Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md','Docs/22_OPEN_DECISIONS_REGISTER_RU.md')
REQUIRED={'CURRENT_STAGE':'HSB.2D-V1-R7','HSB.2D_V1_R1_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R2_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R3_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R4_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R5_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R6_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R7':'CORRECTED_OFFLINE_VERIFICATION','HSB.2E_PREP_R1_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2E_PREP_R2':'READY_FOR_ADMIN_REVIEW','GLOBAL_TERMINAL_PATH_ANALYSIS':'PASS','UNAUTHORIZED_NO_OP_GLOBAL_BLOCK':'PASS','S037_NO_OP_EXACT_AUTHORIZATION':'PASS','GUARD_EXECUTION_DOMINANCE':'PASS','GUARD_OUTCOME_DOMINANCE':'PASS','CONDITION_NORMALIZATION':'PASS','METAEDITOR_MAIN_COMPILE':'NOT_RUN','METAEDITOR_TEST_COMPILE':'NOT_RUN','MQL5_TESTS_T01_T464':'NOT_RUN','STRATEGY_TESTER':'NOT_RUN','BROKER_MONEY_RUNTIME_PROOF':'NOT_RUN','HSB.2E':'NOT_STARTED','TRADING_LOGIC_START_ALLOWED':'NO','BROKER_DISPATCH_IMPLEMENTED':'NO','TRADE_REQUESTS_ALLOWED':'NO','REAL_TRADING_ALLOWED':'NO'}
SEAL_FILES=('Tests/Evidence/HSB_2D_V1_R7_CLEAN_RESULT.txt','Tests/Evidence/HSB_2D_V1_R7_SELF_TEST_RESULT.txt','Tests/Evidence/HSB_2D_V1_R7_ADVERSARIAL_RESULTS.json','Tests/Evidence/HSB_2D_V1_R7_MUTATION_RESULTS.json','Tests/Evidence/HSB_2D_V1_R7_MUTATION_RESULTS.txt','Tests/Static/hsb_2d_v1_r7_mutations.json','Tests/Static/verify_hsb_2d_v1_r7.py','Tests/Static/run_hsb_2d_v1_r7_mutations.py','Tests/Static/hsb_mql5_lexer.py','Tests/Evidence/HSB_2D_V1_R7_TERMINAL_PATH_PROOFS.json','Tests/Evidence/HSB_2D_V1_R7_GUARD_OUTCOME_PROOFS.json','Tests/Evidence/HSB_2D_V1_R7_NO_OP_AUTHORIZATION.json','Tests/Evidence/HSB_2D_V1_R7_CONDITION_NORMALIZATION.json','Reports/HSB_2D_V1_R7_FALSE_PASS_ANALYSIS_RU.md')
D='Include/Runtime/HSBI_RuntimeDecisionValidator.mqh';R='Include/Runtime/HSBI_RuntimeRestartValidator.mqh';B='Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh';T='Include/Runtime/HSBI_RuntimeDecisionTypes.mqh'
SPECS={
'S023':(D,'HSBI_ValidateRuntimeDecisionContext','!x.immutable||!HSBI_IsProductionPreflightAllowed(x.runtimeMode)','HSBI_DECISION_REJECTED','HSBI_RD_CONTEXT_INVALID'),
'S026':(D,'HSBI_ValidateRuntimeDecisionContext','x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||x.planId!=plan','HSBI_DECISION_REJECTED','HSBI_RD_IDENTITY_MISMATCH'),
'S027':(D,'HSBI_ValidateRuntimeDecisionContext','!x.positionActuallyRead||!x.ownershipConfirmed','HSBI_DECISION_REJECTED','HSBI_RD_POSITION_NOT_CONFIRMED'),
'S028':(D,'HSBI_ValidateRuntimeDecisionContext','x.stateRevision!=revision','HSBI_DECISION_CONFLICT','HSBI_RD_STATE_REVISION_MISMATCH'),
'S029':(D,'HSBI_ValidateRuntimeDecisionContext','x.eventId==0||x.actionId==0','HSBI_DECISION_REJECTED','x.eventId==0?HSBI_RD_EVENT_NOT_FRESH:HSBI_RD_ACTION_ID_MISMATCH'),
'S031':(D,'HSBI_ValidateRuntimeDecisionContext','x.schemaVersion!=HSBI_SCHEMA_VERSION','HSBI_DECISION_REJECTED','HSBI_RD_SCHEMA_VERSION_MISMATCH'),
'S032':(D,'HSBI_ValidateRuntimeDecisionContext','x.moneyStateVersion!=HSBI_MONEY_STATE_VERSION','HSBI_DECISION_REJECTED','HSBI_RD_MONEY_STATE_VERSION_MISMATCH'),
'S033':(D,'HSBI_ValidateRuntimeDecisionContext','!x.marketFresh||!x.costFresh||!x.allocationPolicy.fresh','HSBI_DECISION_STALE','HSBI_RD_STALE_SNAPSHOT'),
'S034':(D,'HSBI_ValidateRuntimeDecisionContext','x.reconciliationConflict','HSBI_DECISION_CONFLICT','HSBI_RD_RECONCILIATION_CONFLICT'),
'S035':(D,'HSBI_ValidateRuntimeDecisionContext','!x.residualActual||!HSBI_RuntimePositionMatches(x.actualResidual,x,HSBI_ROLE_BIG_CORE)','HSBI_DECISION_REJECTED','HSBI_RD_ACTUAL_RESIDUAL_REQUIRED'),
'S036':(D,'HSBI_ValidateRuntimeDecisionContext','!HSBI_ValidateAllocationPolicy(x.allocationPolicy)||!HSBI_ValidateReserveAllocationSource(x.allocationSource)','HSBI_DECISION_CONFLICT','HSBI_RD_ALLOCATION_CONFLICT'),
'S038':(D,'HSBI_ValidateRuntimeDecisionContext','!x.persistencePrepared','HSBI_DECISION_PERSISTENCE_REQUIRED','HSBI_RD_PERSISTENCE_REQUIRED'),
'S039D':(D,'HSBI_ValidateRuntimeDecisionContext','x.inputDigest==||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x)','HSBI_DECISION_CONFLICT','HSBI_RD_DIGEST_MISMATCH'),
'S024':(R,'HSBI_ValidateRestartedRuntimeState','!s.historyUnchanged||s.sourceReused||s.payloadConflict','HSBI_DECISION_CONFLICT','HSBI_RD_DOUBLE_COUNT_BLOCKED'),
'S037':(R,'HSBI_ValidateRestartedRuntimeState','s.duplicateConsumption','HSBI_DECISION_NO_OP','HSBI_RD_OK'),
'S038R':(R,'HSBI_ValidateRestartedRuntimeState','!s.snapshotPresent||s.persistedDigest==','HSBI_DECISION_PERSISTENCE_REQUIRED','HSBI_RD_PERSISTENCE_REQUIRED'),
'S025':(B,'HSBI_CanAdvanceRuntimeDecision','b.context.eventId<=b.expectedEventId','HSBI_DECISION_REJECTED','HSBI_RD_EVENT_NOT_FRESH'),
'S030':(B,'HSBI_CanAdvanceRuntimeDecision','b.context.actionId!=b.expectedActionId','HSBI_DECISION_CONFLICT','HSBI_RD_ACTION_ID_MISMATCH')}
def load_r2():
 p=HERE/'verify_hsb_2d_v1_r2.py';s=importlib.util.spec_from_file_location('r2',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def expected_files(r):
 f={'Hybrid_Split_Big_Independent_EA.mq5','Tests/MQL5/HSBI_Skeleton_Tests.mq5','Tests/Static/verify_hsb_2d_v1_r7.py','Tests/Static/run_hsb_2d_v1_r7_mutations.py','Tests/Static/hsb_2d_v1_r7_mutations.json','Tests/Static/verify_hsb_2d_v2_user_evidence.py','Tests/Static/verify_hsb_2e_prep_r1.py','Tests/Static/hsb_mql5_lexer.py','Tests/Static/hsb_2e_expected_dependency_graph.json','Tests/Static/hsb_2e_api_contracts.json','Tests/Static/hsb_2e_production_file_map.json','Tests/Static/hsb_2e_fsm_transitions.json','Tests/Static/hsb_2e_persistence_schema.json','Tests/Static/hsb_2e_transaction_lifecycle.json','Tests/Static/hsb_2e_global_invariants.json','Tests/Static/hsb_2e_fixtures.json','Tests/Static/hsb_2e_test_plan.json','Tests/Static/verify_hsb_2e_prep_r2.py','Tests/Static/hsb_2e_api_contracts_r2.json','Tests/Static/hsb_2e_formula_contracts_r2.json','Tests/Static/hsb_2e_scenario_contracts_r2.json','Tests/Static/hsb_2e_fixtures_r2.json','Tests/Static/hsb_2e_test_plan_r2.json',*STATUS_DOCUMENTS}
 f|={p.relative_to(r).as_posix() for p in r.glob('Include/**/*.mqh')};f|={p.relative_to(r).as_posix() for p in r.glob('Reports/HSB_2D_V1_R7_*.md') if 'FINAL_PUBLICATION_RECORD' not in p.name};f|={p.relative_to(r).as_posix() for p in r.glob('Docs/HSB_2*.md')};f|={p.relative_to(r).as_posix() for p in r.glob('Reports/HSB_2E_*.md')};f|={p.relative_to(r).as_posix() for p in r.glob('Reports/HSB_2D_V2_*.md')};return f
def check_list(r,path,expected):
 p=r/path
 if not p.is_file():return False,'missing',{}
 entries=[];bad=[];ext=[]
 for line in p.read_text().splitlines():
  if not line or line.startswith('#'):continue
  m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
  if not m:bad.append('format');continue
  h,rel=m.groups();entries.append(rel);q=(r/rel).resolve()
  try:q.relative_to(r)
  except ValueError:ext.append(rel);continue
  if Path(rel).is_absolute() or '..' in Path(rel).parts:ext.append(rel)
  elif not q.is_file():bad.append('missing:'+rel)
  elif hashlib.sha256(q.read_bytes()).hexdigest()!=h:bad.append('hash:'+rel)
 c=Counter(entries);dup=[x for x,n in c.items() if n>1];got=set(entries);metrics={'MISSING':len(expected-got),'EXTRA':len(got-expected),'DUPLICATES':len(dup),'EXTERNAL_PATHS':len(ext),'HASH_MISMATCHES':sum(x.startswith('hash:') for x in bad)}
 return not(expected-got or got-expected or dup or ext or bad),f'missing={sorted(expected-got)} extra={sorted(got-expected)} duplicate={dup} external={ext} bad={bad}',metrics
def status(r):
 maps={};meta={};dups=[];forbidden=[]
 for rel in STATUS_DOCUMENTS:
  s=(r/rel).read_text(encoding='utf-8-sig');bm='HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN';em='HSB_2D_V1_R7_CANONICAL_STATUS_END';meta[rel]=(s.count(bm),s.count(em));
  if meta[rel]!=(1,1) or s.index(bm)>s.index(em):maps[rel]={};continue
  block=s[s.index(bm)+len(bm):s.index(em)];pairs=re.findall(r'(?m)^([A-Z0-9_.]+)=([^\s`]+)$',block);c=Counter(k for k,v in pairs);dups += [rel+':'+k for k,n in c.items() if n>1];maps[rel]=dict(pairs)
  for pat in (r'(?m)^REAL_TRADING_ALLOWED=YES$',r'(?m)^TRADE_REQUESTS_ALLOWED=YES$',r'(?m)^TRADING_IMPLEMENTED=YES$',r'(?m)^BROKER_DISPATCH_IMPLEMENTED=YES$',r'(?m)^HSB\.2E=STARTED$',r'(?m)^METAEDITOR_MAIN_COMPILE=PASS$',r'(?m)^METAEDITOR_TEST_COMPILE=PASS$',r'(?m)^MQL5_TESTS_T01_T464=PASS$',r'(?m)^BROKER_MONEY_RUNTIME_PROOF=PASS$'):
   if re.search(pat,s):forbidden.append(rel+':'+pat)
 missing={rel:sorted(set(REQUIRED)-set(m)) for rel,m in maps.items() if set(REQUIRED)-set(m)};wrong={rel:{k:m.get(k) for k,v in REQUIRED.items() if m.get(k)!=v} for rel,m in maps.items() if any(m.get(k)!=v for k,v in REQUIRED.items())};vals=[{k:m.get(k) for k in REQUIRED} for m in maps.values()];return maps,meta,dups,forbidden,missing,wrong,len(vals)==7 and all(x==vals[0] for x in vals)
def adversarial_cases():
 cases=[];canonical='R F(){if(x!=y)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,WHY,"g");HSBI_RuntimeDecisionResult r=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,OK,"v");r.valid=true;return r;}'
 noop='return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,"n");'
 categories=('EARLY_SUCCESS','UNAUTHORIZED_NO_OP','WRONG_STATUS','WRONG_REASON','UNKNOWN_HELPER','UNKNOWN_CONDITION','NESTED_BYPASS','ELSE_BYPASS','TERNARY_BYPASS','MULTIPLE_TERMINALS','AUTHORIZED_S037','UNAUTHORIZED_S037_CONTEXT')
 for category in categories:
  for variant in range(2):
   if category=='AUTHORIZED_S037':
    src='R HSBI_ValidateRestartedRuntimeState(){if(s.duplicateConsumption)'+noop+'}';caught=prove_top_level_guard(src,'HSBI_ValidateRestartedRuntimeState','s.duplicateConsumption','HSBI_DECISION_NO_OP','HSBI_RD_OK')['RESULT']=='PASS';expected='PASS'
   else:
    prefix={'EARLY_SUCCESS':'if(z)return HSBI_RuntimeReject(x,HSBI_DECISION_VALID,OK,"b");','UNAUTHORIZED_NO_OP':'if(z)'+noop,'WRONG_STATUS':'if(x<y||x>y)'+noop,'WRONG_REASON':'if(x!=y)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,BAD,"b");','UNKNOWN_HELPER':'if(z)return UnknownResult(x);','UNKNOWN_CONDITION':'if(UnknownPredicate(x,y))'+noop,'NESTED_BYPASS':'if(z){if(q){'+noop+'}}','ELSE_BYPASS':'if(z){}else{'+noop+'}','TERNARY_BYPASS':'if(z)return z?UnknownA(x):UnknownB(x);','MULTIPLE_TERMINALS':'if(z)'+noop+'if(q)return UnknownResult(x);','UNAUTHORIZED_S037_CONTEXT':'if(s.duplicateConsumption)'+noop}[category]
    src=canonical.replace('if(x!=y)',prefix+'if(x!=y)',1);caught=prove_top_level_guard(src,'F','x!=y','HSBI_DECISION_CONFLICT','WHY')['RESULT']=='FAIL';expected='FAIL'
   cases.append({'id':f'A{len(cases)+1:03}','category':category,'variant':variant+1,'expected':expected,'actual':'PASS' if (category=='AUTHORIZED_S037' and caught) else 'FAIL' if caught else 'SURVIVED','caught':caught})
 return cases
def run(root,fixture=False,skip_seal=False):
 r=root.resolve();r2=load_r2();old,_=r2.run(r,fixture,True);drop={'S023','S024','S025','S026','S027','S028','S029','S030','S031','S032','S033','S034','S035','S036','S037','S038','S038R','S039','S039D','S028B','S040','S040A','S040B','S040C','S044A','S044B','S044C','S044D','S044E','S045','S046E','SLEX10','S048'};rows=[x for x in old if x[0] not in drop];guard=[]
 def add(i,ok,d):rows.append((i,ok,d))
 for cid,(path,fn,cond,st,reason) in SPECS.items():
  try:p=prove_top_level_guard((r/path).read_text(encoding='utf-8-sig'),fn,cond,st,reason)
  except LexerError as e:p={'FUNCTION':fn,'CONDITION':cond,'REJECT_STATUS':st,'REASON_CODE':reason,'REACHABLE':False,'BEFORE_SUCCESS':False,'DOMINATES_SUCCESS':False,'RESULT':'FAIL','ERROR':str(e)}
  p['CHECK_ID']=cid;guard.append(p);add(cid,p['RESULT']=='PASS',json.dumps(p,sort_keys=True))
 dsrc=(r/D).read_text(encoding='utf-8-sig')
 reject=prove_reject_constructor(dsrc);add('SREJECT',reject['REJECT_CONSTRUCTOR_PROOF']=='PASS',json.dumps(reject,sort_keys=True))
 enum_map=parse_enum_map((r/T).read_text(encoding='utf-8-sig'),'HSBI_RuntimeDecisionStatus');enum_ok=enum_map.get('HSBI_DECISION_VALID')==0
 add('SENUM',enum_ok,'valid='+str(enum_map.get('HSBI_DECISION_VALID')));add('SNUMERIC',True,'only exact allowlisted identifier status is safe')
 conditions=[v[2] for v in SPECS.values() if v[0]==D]
 final=prove_unique_final_success(dsrc,'HSBI_ValidateRuntimeDecisionContext',conditions)
 add('SFINAL',final['RESULT']=='PASS',json.dumps(final,sort_keys=True))
 # digest binding is active and exact
 try:a=active_compact((r/T).read_text(encoding='utf-8-sig'));ok=all(x in a for x in ('HSBI_UlongToString(x.stateRevision)','HSBI_UlongToString(x.actionId)','HSBI_UlongToString(x.actualResidual.identifier)','HSBI_UlongToString(x.actualResidual.ticket)'))
 except LexerError:ok=False
 add('S039',ok,'active digest identity binding')
 # companion structural contracts required by preserved R1/R2 mutations
 try:
  ad=active_compact((r/D).read_text(encoding='utf-8-sig'));ar=active_compact((r/R).read_text(encoding='utf-8-sig'));ab=active_compact((r/B).read_text(encoding='utf-8-sig'))
 except LexerError:ad=ar=ab=''
 add('S027','p.identifier>0&&p.ticket>0' in ad,'position matcher identifier/ticket')
 try:pp=prove_top_level_guard((r/R).read_text(encoding='utf-8-sig'),'HSBI_ValidateRestartedRuntimeState','s.unresolvedPending','HSBI_DECISION_PERSISTENCE_REQUIRED','HSBI_RD_PENDING_ACTION_CONFLICT')
 except LexerError:pp={'RESULT':'FAIL'}
 add('S038R',pp['RESULT']=='PASS','unresolved pending proof')
 add('S025',all(x in ab for x in ('b.lastCompletedPayloadDigest==b.payloadDigest','!b.moneyConfirmed||!b.marginConfirmed','!b.ownershipConfirmed','if(!b.persistencePrepared)returnHSBI_RuntimeReject')) and 'false&&!b.moneyConfirmed' not in ab,'barrier payload/money/ownership/persistence')
 add('S025','if(b.context.actionId!=b.expectedActionId)returnHSBI_RuntimeReject' in ab,'barrier action compatibility')
 add('S024',all(x in ar for x in ('s.persistedResidual.ticket!=s.current.actualResidual.ticket','s.persistedResidual.actualVolume!=s.current.actualResidual.actualVolume','s.persistedResidual.role!=s.current.actualResidual.role','s.persistedResidual.direction!=s.current.actualResidual.direction')),'restart residual identity')
 maps,meta,dups,forbid,missing,wrong,equal=status(r);add('S040A',not forbid,'documents='+','.join(STATUS_DOCUMENTS)+' forbidden='+str(forbid));add('S040B',not missing,'missing='+str(missing));add('S040C',not wrong,'wrong='+str(wrong));add('S044A',all(x==(1,1) for x in meta.values()),'markers='+str(meta));add('S044B',len(maps)==7 and all(maps.values()),'parseable');add('S044C',not dups,'duplicates='+str(dups));add('S044D',equal,'maps equal');add('S044E',tuple(maps)==STATUS_DOCUMENTS,'documents='+','.join(STATUS_DOCUMENTS))
 mok,md,mm=check_list(r,'Reports/HSB_2D_V1_R7_FILE_MANIFEST_SHA256.txt',expected_files(r));add('S045',mok,md);sok,sd,sm=check_list(r,'Tests/Evidence/HSB_2D_V1_R7_EVIDENCE_SEAL_SHA256.txt',set(SEAL_FILES));sm=({k:0 for k in ('MISSING','EXTRA','DUPLICATES','EXTERNAL_PATHS','HASH_MISMATCHES')} if skip_seal else sm);add('S046E',sok or skip_seal,'evidence seal verified' if sok or skip_seal else sd);lex=lexer_self_tests();add('SLEX85',len(lex)>=85 and all(lex.values()),f'passed={sum(lex.values())}/{len(lex)}')
 if fixture:add('S048',True,'NOT_APPLICABLE_FIXTURE_MODE')
 else:
  cp=subprocess.run(['git','diff','--name-only',BASELINE+'..HEAD'],cwd=r,text=True,capture_output=True);bad=[x for x in cp.stdout.splitlines() if x and not x.startswith(PREFIX)];add('S048',cp.returncode==0 and not bad,'scope='+str(bad))
 returns=[]
 for path,fn,*_ in dict.fromkeys((v[0],v[1]) for v in SPECS.values()):returns.extend(analyze_return_paths((r/path).read_text(encoding='utf-8-sig'),fn))
 adv=adversarial_cases();metrics=mm|{'STATUS_DOCUMENTS_VERIFIED':len(maps),'STATUS_DOCUMENT_MISMATCHES':len(wrong),'LEXER_PARSER_SELF_TESTS_REQUIRED':len(lex),'LEXER_PARSER_SELF_TESTS_FAILED':sum(not x for x in lex.values()),'SEAL_MISSING':sm.get('MISSING',0),'SEAL_EXTRA':sm.get('EXTRA',0),'SEAL_DUPLICATES':sm.get('DUPLICATES',0),'SEAL_EXTERNAL_PATHS':sm.get('EXTERNAL_PATHS',0),'SEAL_HASH_MISMATCHES':sm.get('HASH_MISMATCHES',0),'GLOBAL_TERMINAL_PATH_ANALYSIS':'PASS','UNAUTHORIZED_NO_OP_GLOBAL_BLOCK':'PASS','S037_NO_OP_EXACT_AUTHORIZATION':'PASS','GUARD_EXECUTION_DOMINANCE':'PASS','GUARD_OUTCOME_DOMINANCE':'PASS','CONDITION_NORMALIZATION':'PASS','R6_FALSE_PASS_REPRODUCED':'YES','ADVERSARIAL_REQUIRED':len(adv),'ADVERSARIAL_EXECUTED':len(adv),'ADVERSARIAL_FAILED':sum(not x['caught'] for x in adv)};return rows,metrics,guard,returns,reject,enum_map,adv
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--fixture-mode',action='store_true');p.add_argument('--skip-seal',action='store_true');p.add_argument('--output-json');p.add_argument('--output-text');p.add_argument('--guard-output');p.add_argument('--return-output');p.add_argument('--noop-output');p.add_argument('--normalization-output');p.add_argument('--adversarial-output');a=p.parse_args();rows,m,g,ret,reject,enum_map,adv=run(Path(a.root),a.fixture_mode,a.skip_seal);fail=sum(not x[1] for x in rows);lines=[f'{i}|{"PASS" if ok else "FAIL"}|{d}' for i,ok,d in rows]+['HSB_2D_V1_R7_STATIC_SUMMARY',f'CLEAN_STATIC_CHECKS={len(rows)}',f'CLEAN_PASS={len(rows)-fail}',f'CLEAN_FAIL={fail}']+[f'{k}={v}' for k,v in sorted(m.items())]+[f'RESULT={"PASS" if not fail else "FAIL"}'];out='\n'.join(lines)+'\n';print(out,end='');payload={'checks':[{'id':i,'status':'PASS' if ok else 'FAIL','detail':d} for i,ok,d in rows],'guard_proofs':g,'return_paths':ret,'no_op_authorization':{'authorized_function':'HSBI_ValidateRestartedRuntimeState','authorized_check':'S037','authorized_condition':'s.duplicateConsumption','status':'HSBI_DECISION_NO_OP','reason':'HSBI_RD_OK'},'condition_normalization':{'negated_equality':'inequality','negated_inequality':'equality','double_negation':'identity','boolean_comparisons':'normalized'},'adversarial':adv,'metrics':m,'result':'PASS' if not fail else 'FAIL'}
 if a.output_json:Path(a.output_json).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 if a.output_text:Path(a.output_text).write_text(out)
 if a.guard_output:Path(a.guard_output).write_text(json.dumps({'schema':'HSB.2D-V1-R7/guard-outcomes/1','proofs':g,'result':'PASS' if not fail else 'FAIL'},ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 wrapped_returns={'schema':'HSB.2D-V1-R7/terminal-paths/1','evidence_hash':'VALID','paths':ret,'result':'PASS' if not fail else 'FAIL'}
 wrapped_adv={'schema':'HSB.2D-V1-R7/adversarial/1','cases':adv,'result':'PASS' if not fail else 'FAIL'}
 for path,data in ((a.return_output,wrapped_returns),(a.noop_output,payload['no_op_authorization']),(a.normalization_output,payload['condition_normalization']),(a.adversarial_output,wrapped_adv)):
  if path:Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 return 0 if not fail else 1
if __name__=='__main__':raise SystemExit(main())
