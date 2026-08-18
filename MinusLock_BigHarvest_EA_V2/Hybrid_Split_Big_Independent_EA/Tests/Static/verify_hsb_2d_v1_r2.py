#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,importlib.util,json,re,subprocess,sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from hsb_mql5_lexer import active_compact,extract_function,lexer_self_tests,LexerError
BASELINE='5587cf766ac08e66d301549d35ecc8d03b86477a';PREFIX='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/'
STATUS_DOCUMENTS=('README_RU.md','BUILD_INFO.md','PROJECT_MAP_RU.md','CHANGELOG_RU.md','Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md','Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md','Docs/22_OPEN_DECISIONS_REGISTER_RU.md')
REQUIRED={'CURRENT_STAGE':'HSB.2D-V1-R2','HSB.2D_V1_R1_PREVIOUS_ACCEPTANCE':'HISTORICAL_SUPERSEDED','HSB.2D_V1_R2':'CORRECTED_OFFLINE_VERIFICATION','METAEDITOR_MAIN_COMPILE':'NOT_EXECUTED_MT5_UNAVAILABLE','METAEDITOR_TEST_COMPILE':'NOT_EXECUTED_MT5_UNAVAILABLE','MQL5_TESTS_T01_T464':'NOT_EXECUTED_MT5_UNAVAILABLE','BROKER_MONEY_RUNTIME_PROOF':'NOT_EXECUTED_MT5_UNAVAILABLE','HSB.2D_V2':'AWAITING_ADMIN_REVIEW','HSB.2E':'NOT_STARTED','TRADING_IMPLEMENTED':'NO','BROKER_DISPATCH_IMPLEMENTED':'NO','TRADE_REQUESTS_ALLOWED':'NO','REAL_TRADING_ALLOWED':'NO'}
SEAL_FILES=('Tests/Evidence/HSB_2D_V1_R2_CLEAN_RESULT.txt','Tests/Evidence/HSB_2D_V1_R2_MUTATION_RESULTS.json','Tests/Evidence/HSB_2D_V1_R2_MUTATION_RESULTS.txt','Tests/Static/hsb_2d_v1_r2_mutations.json','Tests/Static/verify_hsb_2d_v1_r2.py','Tests/Static/run_hsb_2d_v1_r2_mutations.py','Tests/Static/hsb_mql5_lexer.py')
def load_r1():
 p=HERE/'verify_hsb_2d_v1_r1.py';s=importlib.util.spec_from_file_location('r1',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def expected_files(r):
 fixed={'Hybrid_Split_Big_Independent_EA.mq5','Tests/MQL5/HSBI_Skeleton_Tests.mq5','Tests/Static/verify_hsb_2d_v1.py','Tests/Static/verify_hsb_2d_v1_r1.py','Tests/Static/run_hsb_2d_v1_r1_mutations.py','Tests/Static/hsb_2d_v1_r1_mutations.json','Tests/Static/verify_hsb_2d_v1_r2.py','Tests/Static/run_hsb_2d_v1_r2_mutations.py','Tests/Static/hsb_2d_v1_r2_mutations.json','Tests/Static/hsb_mql5_lexer.py','Tests/Static/hsb_2d_v1_include_graph.json',*STATUS_DOCUMENTS,'Docs/HSB_2D_V2_METAEDITOR_USER_VERIFICATION_RU.md'}
 fixed|={p.relative_to(r).as_posix() for p in r.glob('Include/**/*.mqh')};fixed|={p.relative_to(r).as_posix() for p in r.glob('Reports/HSB_2D_V1_R2_*.md') if 'FINAL_PUBLICATION_RECORD' not in p.name};return fixed
def parse_manifest(r):
 p=r/'Reports/HSB_2D_V1_R2_FILE_MANIFEST_SHA256.txt';paths=[];bad=[];ext=[]
 if not p.is_file():return False,'missing',{}
 for line in p.read_text().splitlines():
  if not line or line.startswith('#'):continue
  m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
  if not m:bad.append('format');continue
  h,rel=m.groups();paths.append(rel);q=(r/rel).resolve()
  try:q.relative_to(r)
  except ValueError:ext.append(rel);continue
  if not q.is_file():bad.append('missing:'+rel)
  elif hashlib.sha256(q.read_bytes()).hexdigest()!=h:bad.append('hash:'+rel)
 exp=expected_files(r);got=set(paths);dup=[x for x,n in Counter(paths).items() if n>1];metrics={'EXPECTED_FILES':len(exp),'MANIFEST_FILES':len(got),'MISSING':len(exp-got),'EXTRA':len(got-exp),'DUPLICATES':len(dup),'HASH_MISMATCHES':sum(x.startswith('hash:') for x in bad)}
 return not(exp-got or got-exp or dup or ext or bad),f'missing={sorted(exp-got)} extra={sorted(got-exp)} duplicates={dup} external={ext} bad={bad}',metrics
def parse_status(r):
 maps={};meta={};parse_ok=True;dups=[]
 for rel in STATUS_DOCUMENTS:
  s=(r/rel).read_text(encoding='utf-8-sig');bm='HSB_2D_V1_R2_CANONICAL_STATUS_BEGIN';em='HSB_2D_V1_R2_CANONICAL_STATUS_END';bc=s.count(bm);ec=s.count(em);ok=bc==ec==1 and s.index(bm)<s.index(em) if bc and ec else False;meta[rel]=(bc,ec,ok)
  if not ok:parse_ok=False;maps[rel]={};continue
  block=s[s.index(bm)+len(bm):s.index(em)];pairs=re.findall(r'(?m)^([A-Z0-9_.]+)=([^\s`]+)\s*$',block);c=Counter(k for k,v in pairs);dups += [rel+':'+k for k,n in c.items() if n>1];maps[rel]=dict(pairs)
 return maps,meta,parse_ok,dups
def seal_check(r):
 p=r/'Tests/Evidence/HSB_2D_V1_R2_EVIDENCE_SEAL_SHA256.txt'
 if not p.is_file():return False,'seal missing',0
 entries={}
 for line in p.read_text().splitlines():
  m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
  if m:entries[m.group(2)]=m.group(1)
 miss=set(SEAL_FILES)-set(entries);extra=set(entries)-set(SEAL_FILES);bad=[]
 for rel,h in entries.items():
  q=r/rel
  if not q.is_file() or hashlib.sha256(q.read_bytes()).hexdigest()!=h:bad.append(rel)
 return not(miss or extra or bad),f'missing={sorted(miss)} extra={sorted(extra)} mismatch={bad}',len(entries)
def run(root,fixture=False,skip_seal=False):
 r=root.resolve();r1=load_r1();base=r1.run(r,fixture,BASELINE);drop={'S023','S024','S025','S026','S027','S028','S029','S030','S031','S032','S033','S034','S035','S036','S037','S038','S038R','S039','S039D','S040','S041','S042','S043','S044','S045','S048'};rows=[x for x in base.rows if x[0] not in drop]
 def add(i,ok,d):rows.append((i,ok,d))
 paths={'D':'Include/Runtime/HSBI_RuntimeDecisionValidator.mqh','T':'Include/Runtime/HSBI_RuntimeDecisionTypes.mqh','R':'Include/Runtime/HSBI_RuntimeRestartValidator.mqh','B':'Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh'}
 try:act={k:active_compact((r/v).read_text(encoding='utf-8-sig')) for k,v in paths.items()};fn=active_compact(extract_function((r/paths['D']).read_text(encoding='utf-8-sig'),'HSBI_ValidateRuntimeDecisionContext'))
 except LexerError as e:act={};fn='';add('SLEX',False,'UNABLE_TO_PROVE:'+str(e))
 proofs={
 'S023':('D','if(!x.immutable||!HSBI_IsProductionPreflightAllowed(x.runtimeMode))returnHSBI_RuntimeReject'),
 'S026':('D','if(x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||x.planId!=plan)returnHSBI_RuntimeReject'),
 'S027':('D','if(!x.positionActuallyRead||!x.ownershipConfirmed)returnHSBI_RuntimeReject'),
 'S028':('D','if(x.stateRevision!=revision)returnHSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH'),
 'S029':('D','if(x.eventId==0||x.actionId==0)returnHSBI_RuntimeReject'),
 'S030':('B','if(b.context.actionId!=b.expectedActionId)returnHSBI_RuntimeReject'),
 'S031':('D','if(x.schemaVersion!=HSBI_SCHEMA_VERSION)returnHSBI_RuntimeReject'),
 'S032':('D','if(x.moneyStateVersion!=HSBI_MONEY_STATE_VERSION)returnHSBI_RuntimeReject'),
 'S033':('D','if(!x.marketFresh||!x.costFresh||!x.allocationPolicy.fresh)returnHSBI_RuntimeReject'),
 'S034':('D','if(x.reconciliationConflict)returnHSBI_RuntimeReject'),
 'S035':('D','if(!x.residualActual||!HSBI_RuntimePositionMatches'),
 'S036':('D','if(!HSBI_ValidateAllocationPolicy(x.allocationPolicy)||!HSBI_ValidateReserveAllocationSource(x.allocationSource))returnHSBI_RuntimeReject'),
 'S037':('R','if(s.duplicateConsumption)returnHSBI_RuntimeReject'),
 'S038':('D','if(!x.persistencePrepared)returnHSBI_RuntimeReject'),
 'S038R':('R','if(!s.snapshotPresent||s.persistedDigest=="")returnHSBI_RuntimeReject'),
 'S039':('T','HSBI_UlongToString(x.stateRevision)'),
 'S039D':('D','if(x.inputDigest==""||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x))returnHSBI_RuntimeReject'),
 'S025':('B','if(b.context.eventId<=b.expectedEventId)returnHSBI_RuntimeReject'),
 'S024':('R','if(!s.historyUnchanged||s.sourceReused||s.payloadConflict)returnHSBI_RuntimeReject')}
 # literals are excluded; digest empty quotes disappear, normalize expected accordingly
 proofs['S038R']=('R','if(!s.snapshotPresent||s.persistedDigest==)returnHSBI_RuntimeReject');proofs['S039D']=('D','if(x.inputDigest==||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x))returnHSBI_RuntimeReject')
 for cid,(k,p) in proofs.items():add(cid,k in act and p in act.get(k,''),f'ACTIVE_CODE {paths[k]} token-proof')
 # explicit bypass protection
 add('S028B',bool(fn) and not any(x in fn for x in ('if(false&&x.stateRevision','if(0&&x.stateRevision','if(true||x.stateRevision','if(1||x.stateRevision','if(x.stateRevision==revision')) and 'valid=true;return' not in fn[:fn.find('if(x.stateRevision!=revision')], 'revision bypass proof')
 maps,meta,pok,dups=parse_status(r);doclist=','.join(STATUS_DOCUMENTS);forbidden=[]
 for rel,m in maps.items():
  for k,v in m.items():
   if (k in {'REAL_TRADING_ALLOWED','TRADE_REQUESTS_ALLOWED','BROKER_DISPATCH_IMPLEMENTED','TRADING_IMPLEMENTED'} and v=='YES') or (k=='HSB.2E' and v=='STARTED') or (k in {'METAEDITOR_MAIN_COMPILE','METAEDITOR_TEST_COMPILE','MQL5_TESTS_T01_T464','BROKER_MONEY_RUNTIME_PROOF'} and v=='PASS'):forbidden.append(rel+':'+k)
 add('S040A',not forbidden,'documents='+doclist+' forbidden='+str(forbidden));missing={rel:sorted(set(REQUIRED)-set(m)) for rel,m in maps.items() if set(REQUIRED)-set(m)};add('S040B',not missing,'documents='+doclist+' missing='+str(missing));wrong={rel:{k:m.get(k) for k,v in REQUIRED.items() if m.get(k)!=v} for rel,m in maps.items() if any(m.get(k)!=v for k,v in REQUIRED.items())};add('S040C',not wrong,'wrong='+str(wrong));add('S044A',all(x[0]==x[1]==1 for x in meta.values()),'markers='+str(meta));add('S044B',pok,'parseable='+str(pok));add('S044C',not dups,'duplicates='+str(dups));vals=[{k:m.get(k) for k in REQUIRED} for m in maps.values()];add('S044D',len(vals)==7 and all(x==vals[0] for x in vals),'maps=7 equal');add('S044E',tuple(maps)==STATUS_DOCUMENTS,'documents='+doclist)
 mok,mdetail,metrics=parse_manifest(r);add('S045',mok,mdetail)
 sok,sdetail,sealed=seal_check(r);add('S046E',sok or skip_seal,('BOOTSTRAP ' if skip_seal else '')+sdetail)
 lex=lexer_self_tests();add('SLEX10',all(lex.values()),'LEXER_SELF_TESTS='+str(sum(lex.values()))+'/10')
 if fixture:add('S048',True,'GIT_PUBLICATION_CHECK=NOT_APPLICABLE_FIXTURE_MODE')
 else:
  cp=subprocess.run(['git','diff','--name-only',BASELINE+'..HEAD'],cwd=r,text=True,capture_output=True);bad=[x for x in cp.stdout.splitlines() if x and not x.startswith(PREFIX)];add('S048',cp.returncode==0 and not bad,'scope='+str(bad))
 return rows,metrics|{'STATUS_DOCUMENTS_REQUIRED':7,'STATUS_DOCUMENTS_VERIFIED':len(maps),'STATUS_DOCUMENT_MISMATCHES':len(wrong),'LEXER_SELF_TESTS':sum(lex.values()),'EVIDENCE_FILES_SEALED':sealed}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--fixture-mode',action='store_true');p.add_argument('--skip-seal',action='store_true');p.add_argument('--output-json');p.add_argument('--output-text');a=p.parse_args();rows,metrics=run(Path(a.root),a.fixture_mode,a.skip_seal);lines=[f'{i}|{"PASS" if ok else "FAIL"}|{d}' for i,ok,d in rows];fail=sum(not ok for _,ok,_ in rows);lines+=['HSB_2D_V1_R2_STATIC_SUMMARY',f'CLEAN_STATIC_CHECKS={len(rows)}',f'CLEAN_PASS={len(rows)-fail}',f'CLEAN_FAIL={fail}']+[f'{k}={v}' for k,v in sorted(metrics.items())]+[f'RESULT={"PASS" if fail==0 else "FAIL"}'];out='\n'.join(lines)+'\n';print(out,end='');payload={'checks':[{'id':i,'status':'PASS' if ok else 'FAIL','detail':d} for i,ok,d in rows],'metrics':metrics,'result':'PASS' if fail==0 else 'FAIL'}
 if a.output_json:Path(a.output_json).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 if a.output_text:Path(a.output_text).write_text(out)
 return 0 if fail==0 else 1
if __name__=='__main__':raise SystemExit(main())
