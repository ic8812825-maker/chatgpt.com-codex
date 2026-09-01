#!/usr/bin/env python3
"""Executable, read-only reproductions of the targeted R7 audit findings."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r7 as v7
from build_hsb_2e_r4_r9_r4a_r5_assets import recert

def sha(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def outcome(fn):
 try: fn(); return {'class':'ACCEPTED','checkId':'','reason':''}
 except v7.NormativeError as e:return {'class':'NORMATIVE_REJECTION','checkId':e.checkId,'reason':e.reason}
 except Exception as e:return {'class':'INFRASTRUCTURE_ERROR','checkId':type(e).__name__,'reason':str(e)}
def main():
 fs=v7.fixtures(); runs=[copy.deepcopy(x['scenarioInput']) for x in fs if 'scenarioInput' in x]
 c=next(x for x in runs if x['phase']=='COMMITTED' and x['persistedState']['farState'].get('active'))
 rep=next(x for x in runs if x['phase']=='REPLAY')
 cases=[]
 def add(cid,src,path,change):
  x=copy.deepcopy(src);before=sha(x);change(x);after=sha(x);actual=outcome(lambda:v7.runtime(x));cases.append({'caseId':cid,'positiveSourceSha256':before,'changedPath':path,'mutatedInputSha256':after,'historicalActual':actual,'requiredCorrectBehavior':'NORMATIVE_REJECTION'})
 def resealed(change):
  def f(x):change(x);recert(x)
  return f
 add('R7_POSITION_FOREIGN_MAGIC',c,'positions[0].magic',resealed(lambda x:x['positions'][0].__setitem__('magic',1)))
 add('R7_EVENT_FOREIGN_MAGIC',c,'events[0].magic',resealed(lambda x:x['events'][0].__setitem__('magic',1)))
 add('R7_FAR_UNKNOWN_TICKET',c,'persistedState.farState.ticket',resealed(lambda x:x['persistedState']['farState'].__setitem__('ticket','NO-SUCH-TICKET')))
 add('R7_COMMIT_REVISION_JUMP',c,'fsm.outputRevision',resealed(lambda x:x['fsm'].__setitem__('outputRevision',x['fsm']['inputRevision']+99)))
 def downgrade(x):x['phase']='PRE_COMMIT';x.pop('certificate')
 add('R7_PHASE_DOWNGRADE_EVIDENCE',c,'phase/certificate',downgrade)
 add('R7_ORPHAN_DEAL_INTENT',c,'deals[0].intentId',resealed(lambda x:x['deals'][0].__setitem__('intentId','NO-SUCH-INTENT')))
 def rev999(x):
  for p in ('inputRevision','outputRevision'):x['fsm'][p]=999
  x['persistedState']['stateRevision']=999;x['replayContract']['currentRevisionBefore']=999;x['replayContract']['currentRevisionAfter']=999
 add('R7_REPLAY_ARBITRARY_CURRENT_REVISION',rep,'fsm/replayContract.currentRevision',rev999)
 # Infrastructure defect is executable against acceptance in-memory, not a runtime mutation.
 import accept_hsb_2e_r4_r9_r4a_r7 as accept
 original=accept.regress.run
 try:
  accept.regress.run=lambda fs=None:{'required':0,'executed':0,'wrongFailures':0,'unexpectedInfrastructureErrors':0,'cases':[]}
  a=accept.run(fs)
  cases.append({'caseId':'R7_ACCEPTANCE_EMPTY_0_OF_0','positiveSourceSha256':sha(fs),'changedPath':'regression runner return value','mutatedInputSha256':sha({'required':0,'executed':0,'cases':[]}),'historicalActual':{'class':'ACCEPTED' if a['result']=='PASS' else 'NORMATIVE_REJECTION','checkId':'','reason':a['result']},'requiredCorrectBehavior':'INFRASTRUCTURE_REJECTION'})
 finally:accept.regress.run=original
 out={'historicalTargetSha':'4a4bd1fd4d41d0b8394e48d34dfb28316351c04d','cases':cases,'reproduced':sum(x['historicalActual']['class'] in ('ACCEPTED','INFRASTRUCTURE_ERROR') for x in cases)}
 print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
