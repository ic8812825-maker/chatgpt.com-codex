#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys
from collections import Counter
from pathlib import Path
BASELINE='974792307c0cd2a736fca8edfa1befa8d347c556'
PREFIX='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/'
class V:
 def __init__(self,root,fixture): self.r=root.resolve(); self.fixture=fixture; self.rows=[]; self.metrics={}
 def add(self,i,ok,detail,req='HSBI-2D-V1-R1'): self.rows.append({'id':i,'status':'PASS' if ok else 'FAIL','detail':detail,'requirement':req})
 def read(self,p): return (self.r/p).read_text(encoding='utf-8-sig')
 def exact(self,i,p,need,forbid=()):
  s=self.read(p); ok=all(x in s for x in need) and not any(x in s for x in forbid); self.add(i,ok,f'{p}: structural alternatives={"proved" if ok else "unable_to_prove"}')

def expected_files(r):
 fixed={'Hybrid_Split_Big_Independent_EA.mq5','Tests/MQL5/HSBI_Skeleton_Tests.mq5','Tests/Static/verify_hsb_2d_v1.py','Tests/Static/verify_hsb_2d_v1_r1.py','Tests/Static/run_hsb_2d_v1_r1_mutations.py','Tests/Static/hsb_2d_v1_r1_mutations.json','Tests/Static/hsb_2d_v1_include_graph.json','README_RU.md','BUILD_INFO.md','PROJECT_MAP_RU.md','CHANGELOG_RU.md','Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md','Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md','Docs/22_OPEN_DECISIONS_REGISTER_RU.md','Docs/HSB_2D_V2_METAEDITOR_USER_VERIFICATION_RU.md'}
 fixed|={p.relative_to(r).as_posix() for p in r.glob('Include/**/*.mqh')}
 fixed|={p.relative_to(r).as_posix() for p in r.glob('Reports/HSB_2D_V1_R1_*.md') if 'FINAL_PUBLICATION_RECORD' not in p.name}
 return fixed

def manifest(v):
 p=v.r/'Reports/HSB_2D_V1_R1_FILE_MANIFEST_SHA256.txt'; expected=expected_files(v.r); paths=[]; bad=[]; external=[]
 if not p.is_file(): v.add('S045',False,'manifest missing'); return
 for n,line in enumerate(v.read(p.relative_to(v.r)).splitlines(),1):
  if line.startswith('#') or not line: continue
  m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
  if not m: bad.append(f'format:{n}'); continue
  h,rel=m.groups(); paths.append(rel); q=(v.r/rel).resolve()
  try:q.relative_to(v.r)
  except ValueError: external.append(rel); continue
  if not q.is_file(): bad.append(f'missing:{rel}')
  elif hashlib.sha256(q.read_bytes()).hexdigest()!=h: bad.append(f'hash:{rel}')
 c=Counter(paths); dup=sorted(k for k,n in c.items() if n>1); got=set(paths); missing=sorted(expected-got); extra=sorted(got-expected)
 v.metrics.update(EXPECTED_FILES=len(expected),MANIFEST_FILES=len(got),MISSING=len(missing),EXTRA=len(extra),DUPLICATES=len(dup),HASH_MISMATCHES=sum(x.startswith('hash:') for x in bad))
 v.add('S045',not(missing or extra or dup or external or bad),f'expected={len(expected)} manifest={len(got)} missing={missing} extra={extra} duplicates={dup} external={external} errors={bad}')

def run(root,fixture,baseline):
 v=V(root,fixture); r=v.r
 v.add('S001',r.name=='Hybrid_Split_Big_Independent_EA','explicit project root')
 # symlinks
 badlinks=[]
 for p in r.rglob('*'):
  if p.is_symlink():
   try:p.resolve().relative_to(r)
   except ValueError: badlinks.append(p.relative_to(r).as_posix())
 v.add('S002',not badlinks,f'external_symlinks={badlinks}')
 main='Hybrid_Split_Big_Independent_EA.mq5'; harness='Tests/MQL5/HSBI_Skeleton_Tests.mq5'; dec='Include/Runtime/HSBI_RuntimeDecisionValidator.mqh'; typ='Include/Runtime/HSBI_RuntimeDecisionTypes.mqh'; rst='Include/Runtime/HSBI_RuntimeRestartValidator.mqh'; bar='Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh'
 v.add('S003',(r/main).is_file(),'main'); v.add('S004',(r/harness).is_file(),'harness')
 # includes + cycles
 files=sorted((*r.rglob('*.mq5'),*r.rglob('*.mqh'))); edges={}; miss=[]; ext=[]
 for f in files:
  edges[f]=[]
  for inc in re.findall(r'^\s*#include\s+["<]([^">]+)[">]',f.read_text(encoding='utf-8-sig'),re.M):
   q=(f.parent/inc).resolve()
   try:q.relative_to(r)
   except ValueError: ext.append(f'{f.relative_to(r)}:{inc}'); continue
   if not q.is_file():miss.append(f'{f.relative_to(r)}:{inc}')
   else:edges[f].append(q)
 visiting=set();done=set();cycles=[]
 def dfs(n):
  if n in visiting:cycles.append(n);return
  if n in done:return
  visiting.add(n)
  for q in edges.get(n,[]):dfs(q)
  visiting.remove(n);done.add(n)
 for f in files:dfs(f)
 v.add('S005',not miss,f'missing={miss}');v.add('S006',not ext,f'external={ext}');v.add('S007',not cycles,f'cycles={len(cycles)}')
 guards=[];gm=[]
 for f in sorted(r.rglob('*.mqh')):
  s=f.read_text(encoding='utf-8-sig');m=re.search(r'^\s*#ifndef\s+(\w+)\s*\n\s*#define\s+\1\b',s,re.M)
  if not m or not re.search(r'^\s*#endif\b',s,re.M):gm.append(str(f.relative_to(r)))
  else:guards.append(m.group(1))
 v.add('S008',not gm,f'missing_guards={gm}');v.add('S009',len(guards)==len(set(guards)),f'guards={len(guards)} unique={len(set(guards))}')
 v.add('S010',all((r/x).is_file() for x in [dec,typ,rst,bar]),'runtime files')
 hs=v.read(harness);ids=[int(x) for x in re.findall(r'Check\s*\(\s*"T(\d{2,3})"',hs)]; missing_ids=sorted(set(range(1,465))-set(ids));dupes=sorted(k for k,n in Counter(ids).items() if n>1)
 v.add('S011',len(set(ids))==464,'unique=464');v.add('S012',not dupes,f'duplicates={dupes}');v.add('S013',not missing_ids,f'missing={missing_ids}');v.add('S014','HSBI_TEST_SUMMARY|TOTAL=' in hs,'summary');v.add('S015','g_fail++' in hs and 'g_pass+g_fail' in hs,'accounting')
 ms=v.read(main); prod='\n'.join(p.read_text(encoding='utf-8-sig') for p in files)
 v.add('S016','HSBI_RUNTIME_DISABLED' in ms and 'HSBI_SubmitActionStub()' in ms and 'HSBI_RUNTIME_PRODUCTION' not in ms,'disabled stub')
 pats=[r'\bCTrade\b',r'\bOrderSend\s*\(',r'\bMqlTradeRequest\b',r'\bTRADE_ACTION_'];hits=[p for p in pats if re.search(p,prod)]
 v.add('S017',not hits,f'forbidden={hits}');v.add('S018','Trade/Trade.mqh' not in prod,'Trade.mqh');v.add('S019','MqlTradeRequest' not in prod,'request');v.add('S020','TRADE_ACTION_' not in prod,'action');v.add('S021','WebRequest' not in prod,'web');v.add('S022',not re.search(r'#import[^\n]*\.dll',prod,re.I),'dll')
 # conservative exact branch proofs; ambiguity fails closed
 v.exact('S023',dec,['if(!x.immutable||!HSBI_IsProductionPreflightAllowed(x.runtimeMode))return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_CONTEXT_INVALID'],['if(false && !x.immutable','if(true || !x.immutable'])
 v.exact('S026',dec,['x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||x.planId!=plan','HSBI_RD_IDENTITY_MISMATCH'])
 v.exact('S027',dec,['p.identifier>0&&p.ticket>0','!x.positionActuallyRead||!x.ownershipConfirmed','HSBI_RD_POSITION_NOT_CONFIRMED'],['false && !x.ownershipConfirmed','||x.ownershipConfirmed'])
 v.exact('S028',dec,['if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH'],['false && x.stateRevision','if(false)','x.stateRevision==revision','true || x.stateRevision','r.valid=true;return r;if(x.stateRevision'])
 v.exact('S029',dec,['x.eventId==0||x.actionId==0','HSBI_RD_EVENT_NOT_FRESH'])
 v.exact('S030',bar,['b.context.actionId!=b.expectedActionId','HSBI_RD_ACTION_ID_MISMATCH'])
 v.exact('S031',dec,['x.schemaVersion!=HSBI_SCHEMA_VERSION','HSBI_RD_SCHEMA_VERSION_MISMATCH'])
 v.exact('S032',dec,['x.moneyStateVersion!=HSBI_MONEY_STATE_VERSION','HSBI_RD_MONEY_STATE_VERSION_MISMATCH'])
 v.exact('S033',dec,['!x.marketFresh||!x.costFresh||!x.allocationPolicy.fresh','HSBI_RD_STALE_SNAPSHOT'])
 v.exact('S034',dec,['if(x.reconciliationConflict)','if(!x.reconciliationConfirmed)','HSBI_RD_RECONCILIATION_CONFLICT','HSBI_RD_RECONCILIATION_REQUIRED'])
 v.exact('S035',dec,['!x.residualActual||!HSBI_RuntimePositionMatches(x.actualResidual,x,HSBI_ROLE_BIG_CORE)','HSBI_RD_ACTUAL_RESIDUAL_REQUIRED'])
 v.exact('S036',dec,['HSBI_ValidateAllocationPolicy(x.allocationPolicy)','HSBI_ValidateReserveAllocationSource(x.allocationSource)','HSBI_RD_ALLOCATION_CONFLICT'])
 v.exact('S037',rst,['if(s.duplicateConsumption)return HSBI_RuntimeReject','HSBI_DECISION_NO_OP','s.payloadConflict'])
 v.exact('S038',dec,['if(!x.persistencePrepared)return HSBI_RuntimeReject','HSBI_DECISION_PERSISTENCE_REQUIRED'],['false && !x.persistencePrepared','if(x.persistencePrepared)','return early;if(!x.persistencePrepared'])
 v.exact('S038R',rst,['if(!s.snapshotPresent||s.persistedDigest=="")return HSBI_RuntimeReject','if(s.unresolvedPending)return HSBI_RuntimeReject'],['if(false && !s.snapshotPresent','if(false && s.unresolvedPending'])
 v.exact('S039',typ,['HSBI_UlongToString(x.stateRevision)','HSBI_UlongToString(x.actionId)','HSBI_UlongToString(x.actualResidual.identifier)','HSBI_UlongToString(x.actualResidual.ticket)'])
 v.exact('S039D',dec,['if(x.inputDigest==""||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x))return HSBI_RuntimeReject','HSBI_RD_DIGEST_MISMATCH'],['false && x.inputDigest','x.inputDigest==HSBI_RuntimeDecisionContextDigest'])
 v.exact('S025',bar,['if(b.context.eventId<=b.expectedEventId)return HSBI_RuntimeReject','if(b.context.actionId!=b.expectedActionId)return HSBI_RuntimeReject','!b.moneyConfirmed||!b.marginConfirmed','!b.positionRead||!b.ticketConfirmed||!b.volumeConfirmed||!b.directionConfirmed||!b.ownershipConfirmed','if(!b.persistencePrepared)return HSBI_RuntimeReject','b.lastCompletedPayloadDigest==b.payloadDigest'],['false && b.context.eventId','false && !b.persistencePrepared'])
 v.exact('S024',rst,['!s.historyUnchanged||s.sourceReused||s.payloadConflict','s.persistedResidual.ticket!=s.current.actualResidual.ticket','s.persistedResidual.actualVolume!=s.current.actualResidual.actualVolume','s.persistedResidual.role!=s.current.actualResidual.role','s.persistedResidual.direction!=s.current.actualResidual.direction'],['false && s.sourceReused'])
 docs='\n'.join(v.read(x) for x in ['README_RU.md','BUILD_INFO.md','PROJECT_MAP_RU.md'])
 false_status=bool(re.search(r'(?m)^(REAL_TRADING_ALLOWED=YES|HSB\.2E=STARTED|METAEDITOR_MAIN_COMPILE=PASS|MQL5_TESTS_T01_T464=PASS|BROKER_MONEY_RUNTIME_PROOF=PASS)$',docs))
 v.add('S040',not false_status,'no false status');v.add('S041','HSB.2E=NOT_STARTED' in docs,'2E');v.add('S042','TRADING_IMPLEMENTED=NO' in docs,'trading');v.add('S043','REAL_TRADING_ALLOWED=NO' in docs,'real');v.add('S044','HSB_2D_V1_R1_CANONICAL_STATUS_BEGIN' in docs,'canonical marker')
 manifest(v)
 if fixture:v.add('S048',True,'GIT_PUBLICATION_CHECK=NOT_APPLICABLE_FIXTURE_MODE')
 else:
  cp=subprocess.run(['git','diff','--name-only',baseline+'..HEAD'],cwd=r,text=True,capture_output=True);bad=[x for x in cp.stdout.splitlines() if x and not x.startswith(PREFIX)];v.add('S048',cp.returncode==0 and not bad,f'scope={bad}')
 return v

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--baseline-sha',default=BASELINE);ap.add_argument('--output-json');ap.add_argument('--output-text');ap.add_argument('--fixture-mode',action='store_true');a=ap.parse_args();v=run(Path(a.root),a.fixture_mode,a.baseline_sha)
 lines=[f"{x['id']}|{x['status']}|{x['detail']}" for x in v.rows];fail=sum(x['status']=='FAIL' for x in v.rows);lines+=['HSB_2D_V1_R1_STATIC_SUMMARY',f'CLEAN_STATIC_CHECKS={len(v.rows)}',f'CLEAN_PASS={len(v.rows)-fail}',f'CLEAN_FAIL={fail}']+[f'{k}={val}' for k,val in sorted(v.metrics.items())]+[f"RESULT={'PASS' if fail==0 else 'FAIL'}"]
 out='\n'.join(lines)+'\n';sys.stdout.write(out)
 payload={'schema':'HSB.2D-V1-R1/verifier/1','fixture_mode':a.fixture_mode,'checks':v.rows,'metrics':v.metrics,'result':'PASS' if fail==0 else 'FAIL'}
 if a.output_json:Path(a.output_json).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 if a.output_text:Path(a.output_text).write_text(out,encoding='utf-8')
 return 0 if fail==0 else 1
if __name__=='__main__':raise SystemExit(main())
