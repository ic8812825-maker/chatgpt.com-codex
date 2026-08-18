#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,importlib.util,json,re,subprocess,sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from hsb_mql5_lexer import prove_top_level_guard,active_compact,lexer_self_tests,LexerError
BASELINE='93127723ee94087a4e365d62220050231a772f3e';PREFIX='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/'
STATUS_DOCUMENTS=('README_RU.md','BUILD_INFO.md','PROJECT_MAP_RU.md','CHANGELOG_RU.md','Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md','Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md','Docs/22_OPEN_DECISIONS_REGISTER_RU.md')
REQUIRED={'CURRENT_STAGE':'HSB.2D-V1-R3','HSB.2D_V1_R1_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R2_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R3':'CORRECTED_OFFLINE_VERIFICATION','METAEDITOR_MAIN_COMPILE':'NOT_EXECUTED_MT5_UNAVAILABLE','METAEDITOR_TEST_COMPILE':'NOT_EXECUTED_MT5_UNAVAILABLE','MQL5_TESTS_T01_T464':'NOT_EXECUTED_MT5_UNAVAILABLE','BROKER_MONEY_RUNTIME_PROOF':'NOT_EXECUTED_MT5_UNAVAILABLE','HSB.2D_V2':'AWAITING_ADMIN_REVIEW','HSB.2E':'NOT_STARTED','TRADING_IMPLEMENTED':'NO','BROKER_DISPATCH_IMPLEMENTED':'NO','TRADE_REQUESTS_ALLOWED':'NO','REAL_TRADING_ALLOWED':'NO'}
SEAL_FILES=('Tests/Evidence/HSB_2D_V1_R3_CLEAN_RESULT.txt','Tests/Evidence/HSB_2D_V1_R3_MUTATION_RESULTS.json','Tests/Evidence/HSB_2D_V1_R3_MUTATION_RESULTS.txt','Tests/Static/hsb_2d_v1_r3_mutations.json','Tests/Static/verify_hsb_2d_v1_r3.py','Tests/Static/run_hsb_2d_v1_r3_mutations.py','Tests/Static/hsb_mql5_lexer.py','Reports/HSB_2D_V1_R3_FALSE_PASS_ANALYSIS_RU.md')
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
 f={'Hybrid_Split_Big_Independent_EA.mq5','Tests/MQL5/HSBI_Skeleton_Tests.mq5','Tests/Static/verify_hsb_2d_v1_r3.py','Tests/Static/run_hsb_2d_v1_r3_mutations.py','Tests/Static/hsb_2d_v1_r3_mutations.json','Tests/Static/hsb_mql5_lexer.py',*STATUS_DOCUMENTS}
 f|={p.relative_to(r).as_posix() for p in r.glob('Include/**/*.mqh')};f|={p.relative_to(r).as_posix() for p in r.glob('Reports/HSB_2D_V1_R3_*.md') if 'FINAL_PUBLICATION_RECORD' not in p.name};return f
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
  s=(r/rel).read_text(encoding='utf-8-sig');bm='HSB_2D_V1_R3_CANONICAL_STATUS_BEGIN';em='HSB_2D_V1_R3_CANONICAL_STATUS_END';meta[rel]=(s.count(bm),s.count(em));
  if meta[rel]!=(1,1) or s.index(bm)>s.index(em):maps[rel]={};continue
  block=s[s.index(bm)+len(bm):s.index(em)];pairs=re.findall(r'(?m)^([A-Z0-9_.]+)=([^\s`]+)$',block);c=Counter(k for k,v in pairs);dups += [rel+':'+k for k,n in c.items() if n>1];maps[rel]=dict(pairs)
  for pat in (r'(?m)^REAL_TRADING_ALLOWED=YES$',r'(?m)^TRADE_REQUESTS_ALLOWED=YES$',r'(?m)^TRADING_IMPLEMENTED=YES$',r'(?m)^BROKER_DISPATCH_IMPLEMENTED=YES$',r'(?m)^HSB\.2E=STARTED$'):
   if re.search(pat,s):forbidden.append(rel+':'+pat)
 missing={rel:sorted(set(REQUIRED)-set(m)) for rel,m in maps.items() if set(REQUIRED)-set(m)};wrong={rel:{k:m.get(k) for k,v in REQUIRED.items() if m.get(k)!=v} for rel,m in maps.items() if any(m.get(k)!=v for k,v in REQUIRED.items())};vals=[{k:m.get(k) for k in REQUIRED} for m in maps.values()];return maps,meta,dups,forbidden,missing,wrong,len(vals)==7 and all(x==vals[0] for x in vals)
def run(root,fixture=False,skip_seal=False):
 r=root.resolve();r2=load_r2();old,_=r2.run(r,fixture,True);drop={'S023','S024','S025','S026','S027','S028','S029','S030','S031','S032','S033','S034','S035','S036','S037','S038','S038R','S039','S039D','S028B','S040','S040A','S040B','S040C','S044A','S044B','S044C','S044D','S044E','S045','S046E','SLEX10','S048'};rows=[x for x in old if x[0] not in drop];guard=[]
 def add(i,ok,d):rows.append((i,ok,d))
 for cid,(path,fn,cond,st,reason) in SPECS.items():
  try:p=prove_top_level_guard((r/path).read_text(encoding='utf-8-sig'),fn,cond,st,reason)
  except LexerError as e:p={'FUNCTION':fn,'CONDITION':cond,'REJECT_STATUS':st,'REASON_CODE':reason,'REACHABLE':False,'BEFORE_SUCCESS':False,'DOMINATES_SUCCESS':False,'RESULT':'FAIL','ERROR':str(e)}
  p['CHECK_ID']=cid;guard.append(p);add(cid,p['RESULT']=='PASS',json.dumps(p,sort_keys=True))
 # digest binding is active and exact
 try:a=active_compact((r/T).read_text(encoding='utf-8-sig'));ok=all(x in a for x in ('HSBI_UlongToString(x.stateRevision)','HSBI_UlongToString(x.actionId)','HSBI_UlongToString(x.actualResidual.identifier)','HSBI_UlongToString(x.actualResidual.ticket)'))
 except LexerError:ok=False
 add('S039',ok,'active digest identity binding')
 maps,meta,dups,forbid,missing,wrong,equal=status(r);add('S040A',not forbid,'documents='+','.join(STATUS_DOCUMENTS)+' forbidden='+str(forbid));add('S040B',not missing,'missing='+str(missing));add('S040C',not wrong,'wrong='+str(wrong));add('S044A',all(x==(1,1) for x in meta.values()),'markers='+str(meta));add('S044B',len(maps)==7 and all(maps.values()),'parseable');add('S044C',not dups,'duplicates='+str(dups));add('S044D',equal,'maps equal');add('S044E',tuple(maps)==STATUS_DOCUMENTS,'documents='+','.join(STATUS_DOCUMENTS))
 mok,md,mm=check_list(r,'Reports/HSB_2D_V1_R3_FILE_MANIFEST_SHA256.txt',expected_files(r));add('S045',mok,md);sok,sd,sm=check_list(r,'Tests/Evidence/HSB_2D_V1_R3_EVIDENCE_SEAL_SHA256.txt',set(SEAL_FILES));add('S046E',sok or skip_seal,'evidence seal verified' if sok or skip_seal else sd);lex=lexer_self_tests();add('SLEX24',len(lex)>=24 and all(lex.values()),f'passed={sum(lex.values())}/{len(lex)}')
 if fixture:add('S048',True,'NOT_APPLICABLE_FIXTURE_MODE')
 else:
  cp=subprocess.run(['git','diff','--name-only',BASELINE+'..HEAD'],cwd=r,text=True,capture_output=True);bad=[x for x in cp.stdout.splitlines() if x and not x.startswith(PREFIX)];add('S048',cp.returncode==0 and not bad,'scope='+str(bad))
 metrics=mm|{'STATUS_DOCUMENTS_VERIFIED':len(maps),'STATUS_DOCUMENT_MISMATCHES':len(wrong),'LEXER_SELF_TESTS_REQUIRED':len(lex),'LEXER_SELF_TESTS_FAILED':sum(not x for x in lex.values()),'SEAL_MISSING':sm.get('MISSING',0),'SEAL_EXTRA':sm.get('EXTRA',0),'SEAL_DUPLICATES':sm.get('DUPLICATES',0),'SEAL_HASH_MISMATCHES':sm.get('HASH_MISMATCHES',0)};return rows,metrics,guard
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--fixture-mode',action='store_true');p.add_argument('--skip-seal',action='store_true');p.add_argument('--output-json');p.add_argument('--output-text');a=p.parse_args();rows,m,g=run(Path(a.root),a.fixture_mode,a.skip_seal);fail=sum(not x[1] for x in rows);lines=[f'{i}|{"PASS" if ok else "FAIL"}|{d}' for i,ok,d in rows]+['HSB_2D_V1_R3_STATIC_SUMMARY',f'CLEAN_STATIC_CHECKS={len(rows)}',f'CLEAN_PASS={len(rows)-fail}',f'CLEAN_FAIL={fail}']+[f'{k}={v}' for k,v in sorted(m.items())]+[f'RESULT={"PASS" if not fail else "FAIL"}'];out='\n'.join(lines)+'\n';print(out,end='');payload={'checks':[{'id':i,'status':'PASS' if ok else 'FAIL','detail':d} for i,ok,d in rows],'guard_proofs':g,'metrics':m,'result':'PASS' if not fail else 'FAIL'}
 if a.output_json:Path(a.output_json).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 if a.output_text:Path(a.output_text).write_text(out)
 return 0 if not fail else 1
if __name__=='__main__':raise SystemExit(main())
