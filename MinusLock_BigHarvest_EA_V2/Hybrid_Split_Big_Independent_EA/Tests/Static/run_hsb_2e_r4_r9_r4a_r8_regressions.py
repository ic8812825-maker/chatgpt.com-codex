#!/usr/bin/env python3
"""Fresh R8 cumulative regression catalog; evidence is output only when explicitly requested."""
import argparse,copy,json,sys
from pathlib import Path
import verify_hsb_2e_r4_r9_r4a_r8 as v
from build_hsb_2e_r4_r9_r4a_r5_assets import recert
OUT=v.ROOT/'Tests/Evidence/R4A_R8/regression_results.json'
def classify(fn):
 try:fn()
 except v.NormativeError as e:return 'NORMATIVE_REJECTION',e.checkId,e.reason
 except Exception as e:return 'INFRASTRUCTURE_ERROR',type(e).__name__,str(e)
 return 'ACCEPTED','',''
def run(fs=None):
 fs=copy.deepcopy(fs or v.fixtures());runs=[x for x in fs if 'scenarioInput'in x];comm=next(x['scenarioInput'] for x in runs if x['scenarioInput']['phase']=='COMMITTED');rep=next(x['scenarioInput'] for x in runs if x['scenarioInput']['phase']=='REPLAY');active=next(x['scenarioInput'] for x in runs if x['scenarioInput']['persistedState']['farState']['active']);life=next(x['lifecycleSequence'] for x in fs if 'lifecycleSequence'in x)
 cases=[]
 def add(cid,ec,check,reason,fn):cases.append((cid,ec,check,reason,fn))
 def mut(src,change,life_case=False):
  def f():x=copy.deepcopy(src);change(x);return v.lifecycle(x) if life_case else v.runtime(x)
  return f
 add('VALID','ACCEPTED','','',lambda:v.runtime(copy.deepcopy(comm)))
 def reseal(x):recert(x)
 def window(x):x['temporalPolicy']['validUntil']=1;reseal(x)
 add('CONTRADICTORY_WINDOW','NORMATIVE_REJECTION','R6_TEMPORAL','CONTRADICTORY_WINDOW',mut(comm,window))
 def stale(x):x['deals'][0]['timestamp']=x['snapshot']['timestamp']-1;x['events'][0]['timestamp']=x['deals'][0]['timestamp'];reseal(x)
 add('STALE_DEAL','NORMATIVE_REJECTION','R6_TEMPORAL','DEAL_OUTSIDE_WINDOW',mut(comm,stale))
 def future(x):x['deals'][0]['timestamp']=x['temporalPolicy']['allowedUpperBound']+1;x['events'][0]['timestamp']=x['deals'][0]['timestamp'];reseal(x)
 add('FUTURE_DEAL','NORMATIVE_REJECTION','R6_TEMPORAL','DEAL_OUTSIDE_WINDOW',mut(comm,future))
 add('MISSING_TIME','NORMATIVE_REJECTION','R5_SCHEMA','MISSING_REQUIRED',mut(comm,lambda x:x['deals'][0].pop('timestamp')))
 def samedir(x):x['intents'][0]['direction']=x['positions'][0]['direction'];reseal(x)
 add('SAME_CLOSE_DIRECTION','NORMATIVE_REJECTION','R6_DIRECTION','CLOSE_DIRECTION_OR_REVISION_MISMATCH',mut(comm,samedir))
 def magic(x):x['deals'][0]['magic']=1;x['events'][0]['magic']=1;reseal(x)
 add('FOREIGN_MAGIC','NORMATIVE_REJECTION','R8_IDENTITY','DEAL_CONTEXT_MISMATCH',mut(comm,magic))
 def tail(x):x['economic']['tailCount']=2;reseal(x)
 add('DUAL_TAIL','NORMATIVE_REJECTION','R6_DUAL_TAIL','TAIL_COUNT_MISMATCH',mut(comm,tail))
 def far2(x):p=copy.deepcopy(x['positions'][-1]);p['ticket']+='-2';x['positions'].append(p);reseal(x)
 add('SECOND_FAR','NORMATIVE_REJECTION','R8_FAR','MULTIPLE_ACTIVE_FAR',mut(active,far2))
 def badrep(x):x['persistedState']['consumedDealIds']=['NONEXISTENT'];x['persistedState']['seenEventIds']=['NONEXISTENT']
 add('FOREIGN_REPLAY_IDS','NORMATIVE_REJECTION','R7_REPLAY','REGISTRY_MUTATION',mut(rep,badrep))
 def repinc(x):x['fsm']['outputRevision']+=1
 add('REPLAY_REVISION_INCREMENT','NORMATIVE_REJECTION','R8_REVISION','REPLAY_CURRENT_NOT_HISTORICAL_OUTPUT',mut(rep,repinc))
 def unknown(x):x['steps'][0]['operation']='UNKNOWN'
 add('UNKNOWN_OPERATION','NORMATIVE_REJECTION','R8_LIFECYCLE','UNKNOWN_OPERATION',mut(life,unknown,True))
 def baddigest(x):x['steps'][0]['inputState']['stateDigest']='0'*64
 add('BAD_STATE_DIGEST','NORMATIVE_REJECTION','R7_LIFECYCLE','STATE_DIGEST_MISMATCH',mut(life,baddigest,True))
 def discontinuity(x):x['steps'][1]['inputState']['stateBody']['reserve']='999';x['steps'][1]['inputState']['stateDigest']=v.digest(x['steps'][1]['inputState']['stateBody'])
 add('LIFECYCLE_DISCONTINUITY','NORMATIVE_REJECTION','R8_LIFECYCLE','INPUT_BINDING_MISMATCH',mut(life,discontinuity,True))
 def certzero(x):x['certificate']['digest']='0'*64
 add('CERT_ZERO','NORMATIVE_REJECTION','CERTIFICATE_INTERNAL_INTEGRITY','CERTIFICATE_DIGEST_MISMATCH',mut(comm,certzero))
 add('BOOLEAN_ID','NORMATIVE_REJECTION','R5_TYPE','EXACT_INTEGER_REQUIRED',mut(comm,lambda x:x['context'].__setitem__('magic',True)))
 add('NAN','NORMATIVE_REJECTION','R5_NUMERIC','NONFINITE_DECIMAL',mut(comm,lambda x:x['economic'].__setitem__('availableMoney','NaN')))
 add('OFFGRID_VOLUME','NORMATIVE_REJECTION','R5_GRID','POSITION_OFF_GRID',mut(comm,lambda x:x['positions'][0].__setitem__('volume','0.015')))
 add('HARNESS_KEYERROR','INFRASTRUCTURE_ERROR','KeyError',"'missing'",lambda:({})['missing'])
 add('HARNESS_TYPEERROR','INFRASTRUCTURE_ERROR','TypeError',"unsupported operand type(s) for +: 'int' and 'str'",lambda:1+'x')
 add('INVALID_SCHEMA_VERSION','NORMATIVE_REJECTION','R5_ENUM','INVALID_ENUM',mut(comm,lambda x:x.__setitem__('schemaVersion','INVALID')))
 add('REPLAY_ZERO_CERT','NORMATIVE_REJECTION','R7_CERTIFICATE_INTEGRITY','CERTIFICATE_DIGEST_MISMATCH',mut(rep,lambda x:x['certificate'].__setitem__('digest','0'*64)))
 def histrev(x):x['replayContract']['historicalRevisionBefore']=900;x['replayContract']['historicalRevisionAfter']=1
 add('HISTORICAL_REVISION_REVERSED','NORMATIVE_REJECTION','R8_REVISION','HISTORICAL_INCREMENT_REQUIRED',mut(rep,histrev))
 def fakereserve(x):x['replayContract']['reserveBefore']='999';x['replayContract']['reserveAfter']='999'
 add('REPLAY_FAKE_RESERVE','NORMATIVE_REJECTION','R7_REPLAY','AUTHORITATIVE_STATE_BINDING_MISMATCH',mut(rep,fakereserve))
 add('EMPTY_LIFECYCLE','NORMATIVE_REJECTION','R8_LIFECYCLE','SEQUENCE_TOO_SHORT',mut({'sequenceId':'EMPTY','steps':[]},lambda x:None,True))
 def badlast(x):b=x['steps'][-1]['declaredOutputState']['stateBody'];b['revision']=999999;b['fsmState']='NOT_A_STATE';x['steps'][-1]['declaredOutputState']['stateDigest']=v.digest(b)
 add('BAD_LAST_OUTPUT','NORMATIVE_REJECTION','R7_LIFECYCLE','UNKNOWN_FSM_STATE',mut(life,badlast,True))
 add('CERT_BODY_CHANGED','NORMATIVE_REJECTION','CERTIFICATE_INTERNAL_INTEGRITY','CERTIFICATE_DIGEST_MISMATCH',mut(comm,lambda x:x['certificate'].__setitem__('body','0'*64)))
 def claim(x):x['certificate']['claimedEconomicDigest']='0'*64;x['certificate']['digest']=v.digest({k:z for k,z in x['certificate'].items() if k!='digest'})
 add('CERT_CLAIM_RESEALED','NORMATIVE_REJECTION','CERTIFICATE_SOURCE_BINDING','CERTIFICATE_SOURCE_MISMATCH',mut(comm,claim))
 other=next(copy.deepcopy(x['scenarioInput']['certificate']) for x in runs if x['scenarioInput']['phase']=='COMMITTED' and x['scenarioInput']['certificate']!=comm['certificate'])
 add('CERT_OTHER_OPERATION','NORMATIVE_REJECTION','CERTIFICATE_SOURCE_BINDING','CERTIFICATE_SOURCE_MISMATCH',mut(comm,lambda x:x.__setitem__('certificate',other)))
 add('CERT_MISSING_COMMITTED','NORMATIVE_REJECTION','R8_PHASE','COMMIT_EVIDENCE_REQUIRED',mut(comm,lambda x:x.pop('certificate')))
 add('CERT_PROVIDED_PRECOMMIT','NORMATIVE_REJECTION','R8_PHASE','CURRENT_EXECUTION_EVIDENCE_FORBIDDEN',mut(next(x['scenarioInput'] for x in runs if x['scenarioInput']['phase']=='PRE_COMMIT'),lambda x:x.__setitem__('certificate',copy.deepcopy(comm['certificate']))))
 add('UNKNOWN_NESTED','NORMATIVE_REJECTION','R5_SCHEMA','UNKNOWN_FIELD',mut(comm,lambda x:x['context'].__setitem__('unknown',1)))
 add('INFINITY','NORMATIVE_REJECTION','R5_NUMERIC','NONFINITE_DECIMAL',mut(comm,lambda x:x['economic'].__setitem__('availableMoney','Infinity')))
 add('OFFGRID_PRICE','NORMATIVE_REJECTION','R5_GRID','POSITION_OFF_GRID',mut(comm,lambda x:x['positions'][0].__setitem__('openPrice','1.00005')))
 add('DUPLICATE_DEAL','NORMATIVE_REJECTION','R8_COLLECTION','DUPLICATE_IDENTIFIER',mut(comm,lambda x:x['deals'].append(copy.deepcopy(x['deals'][0]))))
 add('MONEY_CONSERVATION','NORMATIVE_REJECTION','R5_MONEY','MONEY_CONSERVATION_MISMATCH',mut(comm,lambda x:x['allocationPolicy'].__setitem__('remainingMoney','999')))
 def vol(x):x['deals'][0]['volume']='0.02';x['events'][0]['volume']='0.02'
 add('VOLUME_CONSERVATION','NORMATIVE_REJECTION','R5_VOLUME','VOLUME_CONSERVATION_MISMATCH',mut(comm,vol))
 add('RESERVE_PARTIAL_FAR','NORMATIVE_REJECTION','R5_RESERVE','RESERVE_PARTIAL_FAR_FORBIDDEN',mut(comm,lambda x:(x['economic'].__setitem__('partialFarVolume','0.01'),x['economic'].__setitem__('reserveConsumption','1'))))
 add('POSITION_FOREIGN_MAGIC','NORMATIVE_REJECTION','R8_IDENTITY','POSITION_CONTEXT_MISMATCH',mut(comm,lambda x:(x['positions'][0].__setitem__('magic',1),reseal(x))))
 add('EVENT_FOREIGN_MAGIC','NORMATIVE_REJECTION','R8_IDENTITY','EVENT_DEAL_MISMATCH',mut(comm,lambda x:(x['events'][0].__setitem__('magic',1),reseal(x))))
 def farticket(x):x['persistedState']['farState']['ticket']='NO-SUCH-TICKET';reseal(x)
 add('FAR_TICKET_NOT_FOUND','NORMATIVE_REJECTION','R8_FAR','ACTIVE_FAR_TICKET_NOT_FOUND',mut(active,farticket))
 def commitjump(x):x['fsm']['outputRevision']=x['fsm']['inputRevision']+99;reseal(x)
 add('COMMIT_REVISION_JUMP','NORMATIVE_REJECTION','R8_REVISION','COMMIT_INCREMENT_REQUIRED',mut(comm,commitjump))
 def downgrade(x):x['phase']='PRE_COMMIT';x.pop('certificate')
 add('PHASE_DOWNGRADE_WITH_EVIDENCE','NORMATIVE_REJECTION','R8_PHASE','CURRENT_EXECUTION_EVIDENCE_FORBIDDEN',mut(comm,downgrade))
 def orphan(x):x['deals'][0]['intentId']='NO-SUCH-INTENT';reseal(x)
 add('ORPHAN_DEAL','NORMATIVE_REJECTION','R8_REFERENCE','DEAL_INTENT_NOT_FOUND',mut(comm,orphan))
 def current999(x):
  x['fsm']['inputRevision']=999;x['fsm']['outputRevision']=999;x['persistedState']['stateRevision']=999;x['replayContract']['currentRevisionBefore']=999;x['replayContract']['currentRevisionAfter']=999
 add('REPLAY_ARBITRARY_CURRENT_REVISION','NORMATIVE_REJECTION','R8_REVISION','REPLAY_CURRENT_NOT_HISTORICAL_OUTPUT',mut(rep,current999))
 add('DUPLICATE_TICKET','NORMATIVE_REJECTION','R8_COLLECTION','DUPLICATE_IDENTIFIER',mut(comm,lambda x:x['positions'].append(copy.deepcopy(x['positions'][0]))))
 def farforeign(x):x['positions'][-1]['magic']=1;reseal(x)
 add('FAR_FOREIGN_OWNERSHIP','NORMATIVE_REJECTION','R8_IDENTITY','POSITION_CONTEXT_MISMATCH',mut(active,farforeign))
 add('VALID_PRECOMMIT','ACCEPTED','','',lambda:v.runtime(copy.deepcopy(next(x['scenarioInput'] for x in runs if x['scenarioInput']['phase']=='PRE_COMMIT'))))
 rows=[]
 for cid,ec,ck,rs,fn in cases:
  ac,ak,ar=classify(fn);rows.append({'caseId':cid,'expectedClass':ec,'expectedCheckId':ck,'expectedReason':rs,'actualClass':ac,'actualCheckId':ak,'actualReason':ar,'result':'PASS' if (ec,ck,rs)==(ac,ak,ar) else 'FAIL'})
 return {'required':len(cases),'executed':len(rows),'wrongFailures':sum(x['result']=='FAIL' for x in rows),'unexpectedInfrastructureErrors':sum(x['actualClass']=='INFRASTRUCTURE_ERROR' and x['expectedClass']!='INFRASTRUCTURE_ERROR' for x in rows),'cases':rows}
def main():
 a=argparse.ArgumentParser();a.add_argument('--publish-evidence',action='store_true');args=a.parse_args();out=run();out['result']='PASS' if not out['wrongFailures'] and not out['unexpectedInfrastructureErrors'] else 'FAIL'
 if args.publish_evidence:OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(f"REQUIRED={out['required']} EXECUTED={out['executed']} WRONG={out['wrongFailures']} INFRASTRUCTURE_ERRORS={out['unexpectedInfrastructureErrors']} RESULT={out['result']}");return 0 if out['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
