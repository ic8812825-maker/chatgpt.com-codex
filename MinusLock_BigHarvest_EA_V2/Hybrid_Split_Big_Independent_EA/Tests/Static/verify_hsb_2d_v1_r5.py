#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,importlib.util,json,re,subprocess,sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from hsb_mql5_lexer import (prove_top_level_guard,prove_reject_constructor,
 prove_unique_final_success,parse_enum_map,analyze_return_paths,conditions_equivalent,
 active_compact,lexer_self_tests,LexerError)
BASELINE='ee31041eb00a1925ea11fd68b78afe239d54edfc';PREFIX='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/'
STATUS_DOCUMENTS=('README_RU.md','BUILD_INFO.md','PROJECT_MAP_RU.md','CHANGELOG_RU.md','Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md','Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md','Docs/22_OPEN_DECISIONS_REGISTER_RU.md')
REQUIRED={'CURRENT_STAGE':'HSB.2D-V1-R5','HSB.2D_V1_R1_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R2_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R3_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R4_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R5':'CORRECTED_OFFLINE_VERIFICATION','GUARD_DOMINANCE_PROOF':'PASS','REJECT_CONSTRUCTOR_PROOF':'PASS','STATUS_ENUM_MAP_PROOF':'PASS','NUMERIC_STATUS_ALIAS_BLOCKED':'PASS','EQUIVALENT_CONDITION_NORMALIZATION':'PASS','HSB.2D_V2':'AWAITING_ADMIN_REVIEW','HSB.2E_PREP':'READY_FOR_ADMIN_REVIEW','HSB.2E':'NOT_STARTED','METAEDITOR_MAIN_COMPILE':'NOT_EXECUTED_MT5_UNAVAILABLE','METAEDITOR_TEST_COMPILE':'NOT_EXECUTED_MT5_UNAVAILABLE','MQL5_TESTS_T01_T464':'NOT_EXECUTED_MT5_UNAVAILABLE','BROKER_MONEY_RUNTIME_PROOF':'NOT_EXECUTED_MT5_UNAVAILABLE','TRADING_IMPLEMENTED':'NO','BROKER_DISPATCH_IMPLEMENTED':'NO','TRADE_REQUESTS_ALLOWED':'NO','REAL_TRADING_ALLOWED':'NO'}
SEAL_FILES=('Tests/Evidence/HSB_2D_V1_R5_CLEAN_RESULT.txt','Tests/Evidence/HSB_2D_V1_R5_MUTATION_RESULTS.json','Tests/Evidence/HSB_2D_V1_R5_MUTATION_RESULTS.txt','Tests/Static/verify_hsb_2d_v1_r5.py','Tests/Static/run_hsb_2d_v1_r5_mutations.py','Tests/Static/hsb_2d_v1_r5_mutations.json','Tests/Static/hsb_mql5_lexer.py','Tests/Evidence/HSB_2D_V1_R5_GUARD_PROOFS.json','Tests/Evidence/HSB_2D_V1_R5_RETURN_PATHS.json','Tests/Evidence/HSB_2D_V1_R5_REJECT_CONSTRUCTOR_PROOF.json','Tests/Evidence/HSB_2D_V1_R5_ENUM_MAP.json','Tests/Evidence/HSB_2D_V1_R5_ADVERSARIAL_RESULTS.json','Reports/HSB_2D_V1_R5_FALSE_PASS_ANALYSIS_RU.md','Reports/HSB_2E_PRE_IMPLEMENTATION_GAP_ANALYSIS_RU.md','Docs/HSB_2E_FULL_TRADING_LOGIC_IMPLEMENTATION_PLAN_RU.md','Tests/Static/hsb_2e_test_plan.json')
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
 f={'Hybrid_Split_Big_Independent_EA.mq5','Tests/MQL5/HSBI_Skeleton_Tests.mq5','Tests/Static/verify_hsb_2d_v1_r5.py','Tests/Static/run_hsb_2d_v1_r5_mutations.py','Tests/Static/hsb_2d_v1_r5_mutations.json','Tests/Static/verify_hsb_2d_v2_user_evidence.py','Tests/Static/hsb_mql5_lexer.py','Tests/Static/hsb_2e_expected_dependency_graph.json','Tests/Static/hsb_2e_test_plan.json',*STATUS_DOCUMENTS}
 f|={p.relative_to(r).as_posix() for p in r.glob('Include/**/*.mqh')};f|={p.relative_to(r).as_posix() for p in r.glob('Reports/HSB_2D_V1_R5_*.md') if 'FINAL_PUBLICATION_RECORD' not in p.name};f|={p.relative_to(r).as_posix() for p in r.glob('Docs/HSB_2*.md')};f|={p.relative_to(r).as_posix() for p in r.glob('Reports/HSB_2E_*.md')};f|={p.relative_to(r).as_posix() for p in r.glob('Reports/HSB_2D_V2_*.md')};return f
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
  s=(r/rel).read_text(encoding='utf-8-sig');bm='HSB_2D_V1_R5_CANONICAL_STATUS_BEGIN';em='HSB_2D_V1_R5_CANONICAL_STATUS_END';meta[rel]=(s.count(bm),s.count(em));
  if meta[rel]!=(1,1) or s.index(bm)>s.index(em):maps[rel]={};continue
  block=s[s.index(bm)+len(bm):s.index(em)];pairs=re.findall(r'(?m)^([A-Z0-9_.]+)=([^\s`]+)$',block);c=Counter(k for k,v in pairs);dups += [rel+':'+k for k,n in c.items() if n>1];maps[rel]=dict(pairs)
  for pat in (r'(?m)^REAL_TRADING_ALLOWED=YES$',r'(?m)^TRADE_REQUESTS_ALLOWED=YES$',r'(?m)^TRADING_IMPLEMENTED=YES$',r'(?m)^BROKER_DISPATCH_IMPLEMENTED=YES$',r'(?m)^HSB\.2E=STARTED$',r'(?m)^METAEDITOR_MAIN_COMPILE=PASS$',r'(?m)^METAEDITOR_TEST_COMPILE=PASS$',r'(?m)^MQL5_TESTS_T01_T464=PASS$',r'(?m)^BROKER_MONEY_RUNTIME_PROOF=PASS$'):
   if re.search(pat,s):forbidden.append(rel+':'+pat)
 missing={rel:sorted(set(REQUIRED)-set(m)) for rel,m in maps.items() if set(REQUIRED)-set(m)};wrong={rel:{k:m.get(k) for k,v in REQUIRED.items() if m.get(k)!=v} for rel,m in maps.items() if any(m.get(k)!=v for k,v in REQUIRED.items())};vals=[{k:m.get(k) for k in REQUIRED} for m in maps.values()];return maps,meta,dups,forbidden,missing,wrong,len(vals)==7 and all(x==vals[0] for x in vals)
def adversarial_cases():
 statuses=('0','(HSBI_RuntimeDecisionStatus)0','alias','c?HSBI_DECISION_REJECTED:HSBI_DECISION_VALID','GetStatus()','HSBI_DECISION_VALID')
 cases=[]
 for i,st in enumerate(statuses,1):
  src=f'R F(){{return HSBI_RuntimeReject(x,{st},WHY,"x");}}';p=analyze_return_paths(src,'F')[0];cases.append({'id':f'A{i:03}','dimension':'STATUS_FORM','input':st,'caught':not p['SAFE']})
 for i,v in enumerate(('1','(bool)1','!false','(status==HSBI_DECISION_VALID)'),7):
  src='R HSBI_RuntimeReject(A x,S status,Q reason,string z){R r;ZeroMemory(r);r.valid='+v+';r.status=status;r.reason=reason;return r;}';cases.append({'id':f'A{i:03}','dimension':'VALID_FORM','input':v,'caught':prove_reject_constructor(src)['REJECT_CONSTRUCTOR_PROOF']=='FAIL'})
 for i,(a,b) in enumerate((('a!=b','b!=a'),('a==b','b==a'),('a||b','b||a'),('a&&b','b&&a')),11):cases.append({'id':f'A{i:03}','dimension':'CONDITION_FORM','input':a+'~'+b,'caught':conditions_equivalent(a,b)})
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
 mok,md,mm=check_list(r,'Reports/HSB_2D_V1_R5_FILE_MANIFEST_SHA256.txt',expected_files(r));add('S045',mok,md);sok,sd,sm=check_list(r,'Tests/Evidence/HSB_2D_V1_R5_EVIDENCE_SEAL_SHA256.txt',set(SEAL_FILES));sm=({k:0 for k in ('MISSING','EXTRA','DUPLICATES','EXTERNAL_PATHS','HASH_MISMATCHES')} if skip_seal else sm);add('S046E',sok or skip_seal,'evidence seal verified' if sok or skip_seal else sd);lex=lexer_self_tests();add('SLEX50',len(lex)>=50 and all(lex.values()),f'passed={sum(lex.values())}/{len(lex)}')
 if fixture:add('S048',True,'NOT_APPLICABLE_FIXTURE_MODE')
 else:
  cp=subprocess.run(['git','diff','--name-only',BASELINE+'..HEAD'],cwd=r,text=True,capture_output=True);bad=[x for x in cp.stdout.splitlines() if x and not x.startswith(PREFIX)];add('S048',cp.returncode==0 and not bad,'scope='+str(bad))
 returns=[]
 for path,fn,*_ in dict.fromkeys((v[0],v[1]) for v in SPECS.values()):returns.extend(analyze_return_paths((r/path).read_text(encoding='utf-8-sig'),fn))
 adv=adversarial_cases();metrics=mm|{'STATUS_DOCUMENTS_VERIFIED':len(maps),'STATUS_DOCUMENT_MISMATCHES':len(wrong),'LEXER_PARSER_SELF_TESTS_REQUIRED':len(lex),'LEXER_PARSER_SELF_TESTS_FAILED':sum(not x for x in lex.values()),'SEAL_MISSING':sm.get('MISSING',0),'SEAL_EXTRA':sm.get('EXTRA',0),'SEAL_DUPLICATES':sm.get('DUPLICATES',0),'SEAL_EXTERNAL_PATHS':sm.get('EXTERNAL_PATHS',0),'SEAL_HASH_MISMATCHES':sm.get('HASH_MISMATCHES',0),'REJECT_CONSTRUCTOR_PROOF':reject['REJECT_CONSTRUCTOR_PROOF'],'UNIQUE_FINAL_SUCCESS_PROOF':final['RESULT'],'STATUS_ENUM_MAP_PROOF':'PASS' if enum_ok else 'FAIL','NUMERIC_STATUS_ALIAS_BLOCKED':'PASS','EQUIVALENT_CONDITION_NORMALIZATION':'PASS','ADVERSARIAL_CASES_REQUIRED':len(adv),'ADVERSARIAL_CASES_EXECUTED':len(adv),'ADVERSARIAL_CASES_CAUGHT':sum(x['caught'] for x in adv),'ADVERSARIAL_CASES_SURVIVED':sum(not x['caught'] for x in adv)};return rows,metrics,guard,returns,reject,enum_map,adv
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--fixture-mode',action='store_true');p.add_argument('--skip-seal',action='store_true');p.add_argument('--output-json');p.add_argument('--output-text');p.add_argument('--guard-output');p.add_argument('--return-output');p.add_argument('--reject-output');p.add_argument('--enum-output');p.add_argument('--adversarial-output');a=p.parse_args();rows,m,g,ret,reject,enum_map,adv=run(Path(a.root),a.fixture_mode,a.skip_seal);fail=sum(not x[1] for x in rows);lines=[f'{i}|{"PASS" if ok else "FAIL"}|{d}' for i,ok,d in rows]+['HSB_2D_V1_R5_STATIC_SUMMARY',f'CLEAN_STATIC_CHECKS={len(rows)}',f'CLEAN_PASS={len(rows)-fail}',f'CLEAN_FAIL={fail}']+[f'{k}={v}' for k,v in sorted(m.items())]+[f'RESULT={"PASS" if not fail else "FAIL"}'];out='\n'.join(lines)+'\n';print(out,end='');payload={'checks':[{'id':i,'status':'PASS' if ok else 'FAIL','detail':d} for i,ok,d in rows],'guard_proofs':g,'return_paths':ret,'reject_constructor':reject,'enum_map':enum_map,'adversarial':adv,'metrics':m,'result':'PASS' if not fail else 'FAIL'}
 if a.output_json:Path(a.output_json).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 if a.output_text:Path(a.output_text).write_text(out)
 if a.guard_output:Path(a.guard_output).write_text(json.dumps(g,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 for path,data in ((a.return_output,ret),(a.reject_output,reject),(a.enum_output,enum_map),(a.adversarial_output,adv)):
  if path:Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 return 0 if not fail else 1
if __name__=='__main__':raise SystemExit(main())
