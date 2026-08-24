#!/usr/bin/env python3
"""PREP-R4-R2 cumulative-fill oracle. Pure Decimal functions; no broker dispatch."""
from decimal import Decimal,InvalidOperation
import argparse,copy,hashlib,json
D=lambda x:Decimal(str(x))
def finite(v):
 try:return D(v).is_finite()
 except (InvalidOperation,ValueError,TypeError):return False
def serial(v):
 if isinstance(v,Decimal):return format(v,'f')
 if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
 if isinstance(v,list):return [serial(x) for x in v]
 return v
def digest(v):return hashlib.sha256(json.dumps(serial(v),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def result(inp,status,reason,phase,output=None,records=None):
 r={'status':status,'reason':reason,'phase':phase,'output':serial(output or {}),'persistenceRecords':records or [],'inputDigest':digest(inp)};r['outputDigest']=digest({k:v for k,v in r.items() if k!='outputDigest'});return r
def grid(v,step):return finite(v) and finite(step) and D(step)>0 and D(v)>0 and D(v)%D(step)==0
def context_error(c):
 req=('accountLogin','symbol','magic','cycleId','actionId','transactionId','stateRevision','snapshotId','snapshotVersion','snapshotTimestamp','minimumTimestamp','bid','ask','tickSize','digits','volumeMin','volumeMax','volumeStep')
 if any(k not in c or c[k] in ('',None) for k in req):return 'CONTEXT_MISSING'
 for k in ('accountLogin','magic','stateRevision','snapshotVersion','snapshotTimestamp','minimumTimestamp','bid','ask','tickSize','digits','volumeMin','volumeMax','volumeStep'):
  if not finite(c[k]):return 'CONTEXT_NUMERIC_INVALID'
 if D(c['snapshotVersion'])<=0 or D(c['stateRevision'])<0:return 'REVISION_INVALID'
 if D(c['snapshotTimestamp'])<D(c['minimumTimestamp']):return 'STALE_SNAPSHOT'
 if D(c['volumeStep'])<=0 or D(c['volumeMin'])<=0 or D(c['volumeMax'])<D(c['volumeMin']):return 'VOLUME_GRID_INVALID'
 if D(c['tickSize'])<=0 or D(c['digits'])<0 or D(c['ask'])<D(c['bid']):return 'PRICE_GRID_INVALID'
 return 'OK'
def close_price(direction,c):return D(c['bid']) if direction=='BUY' else D(c['ask']) if direction=='SELL' else None
def deal_error(d,c,p,intent):
 req=('dealId','orderId','positionTicket','accountLogin','symbol','magic','cycleId','transactionId','actionId','eventId','stateRevision','direction','volume','price','profit','commission','swap','fee','confirmed','timestamp')
 if any(k not in d or d[k] in ('',None) for k in req):return 'DEAL_SCHEMA_INVALID'
 if not all(finite(d[k]) for k in ('volume','price','profit','commission','swap','fee','stateRevision','timestamp')):return 'DEAL_NUMERIC_INVALID'
 if D(d['volume'])<=0 or D(d['volume'])<D(c['volumeMin']):return 'DEAL_VOLUME_INVALID'
 if not grid(d['volume'],c['volumeStep']):return 'DEAL_VOLUME_OFF_GRID'
 if D(d['price'])<=0 or D(d['price'])%D(c['tickSize'])!=0:return 'DEAL_PRICE_OFF_GRID'
 if not d['confirmed']:return 'DEAL_UNCONFIRMED'
 if d['accountLogin']!=c['accountLogin'] or d['symbol']!=c['symbol'] or d['magic']!=c['magic'] or d['cycleId']!=c['cycleId']:return 'FOREIGN_FILL'
 if d['transactionId']!=c['transactionId'] or d['actionId']!=c['actionId'] or D(d['stateRevision'])!=D(c['stateRevision']):return 'STALE_FILL'
 if d['positionTicket']!=p['ticket'] or d['direction']!=p['direction']:return 'FOREIGN_FILL'
 if close_price(p['direction'],c) is None or D(d['price'])!=close_price(p['direction'],c):return 'DEAL_PRICE_SIDE_INVALID'
 if D(d['volume'])>D(intent['requestedVolume']):return 'OVERFILL'
 return 'OK'
def classify_fill(c,p,intent,deals,consumed=()):
 requested=D(intent['requestedVolume']);tol=D(c['volumeStep'])/D(2);valid=[];seen=set();errors=[]
 if not grid(requested,c['volumeStep']):return {'requestedVolume':requested,'confirmedVolume':D(0),'remainingVolume':requested,'overfillVolume':D(0),'fillState':'INVALID_FILL','errors':['REQUESTED_VOLUME_INVALID'],'consumedDealIds':[],'money':D(0)}
 for d in deals:
  key=(d.get('dealId'),d.get('eventId'))
  if key in seen or d.get('dealId') in consumed:errors.append('DUPLICATE_FILL');continue
  seen.add(key);e=deal_error(d,c,p,intent)
  if e!='OK':errors.append(e);continue
  valid.append(d)
 confirmed=sum((D(d['volume']) for d in valid),D(0));remaining=max(D(0),requested-confirmed);over=max(D(0),confirmed-requested)
 if 'OVERFILL' in errors:state='OVERFILL'
 elif 'DUPLICATE_FILL' in errors:state='DUPLICATE_FILL'
 elif any(e in ('FOREIGN_FILL',) for e in errors):state='FOREIGN_FILL'
 elif any(e in ('STALE_FILL',) for e in errors):state='STALE_FILL'
 elif errors:state='INVALID_FILL'
 elif confirmed==0:state='NO_FILL'
 elif over>tol:state='OVERFILL'
 elif abs(confirmed-requested)<=tol:state='FULL_FILL'
 else:state='PARTIAL_FILL'
 money=sum((D(d['profit'])+D(d['commission'])+D(d['swap'])+D(d['fee']) for d in valid),D(0))
 return {'requestedVolume':requested,'confirmedVolume':confirmed,'remainingVolume':remaining,'overfillVolume':over,'fillState':state,'errors':errors,'consumedDealIds':[d['dealId'] for d in valid],'money':money}
def gate(inp,fills,success_phase):
 states=[x['fillState'] for x in fills.values()]
 out={'fills':fills,'settlementApplied':False,'allocationApplied':False,'stateRevision':inp['context']['stateRevision'],'consumedDealIds':sum((x['consumedDealIds'] for x in fills.values()),[])}
 if any(x=='OVERFILL' for x in states):return result(inp,'CONFLICT','OVERFILL_RECONCILIATION','RECONCILIATION_BLOCKED',out,['FILL_EVIDENCE_PERSISTED'])
 if any(x in ('INVALID_FILL','DUPLICATE_FILL','FOREIGN_FILL','STALE_FILL') for x in states):return result(inp,'REJECT',next(x for x in states if x not in ('FULL_FILL','PARTIAL_FILL','NO_FILL')),'RECONCILIATION_BLOCKED',out,['FILL_EVIDENCE_PERSISTED'])
 if any(x!='FULL_FILL' for x in states):return result(inp,'UNAVAILABLE','PARTIAL_FILL_RECONCILIATION','WAITING_FOR_FULL_FILL',out,['CUMULATIVE_FILL_PERSISTED'])
 out.update(settlementApplied=True,allocationApplied=True,stateRevision=D(inp['context']['stateRevision'])+1,totalMoney=sum((x['money'] for x in fills.values()),D(0)))
 return result(inp,'PASS','OK',success_phase,out,['FULL_FILL_CONFIRMED','SETTLEMENT_PERSISTED','FSM_COMMIT'])
def initial_lock(inp):
 c=inp['context'];e=context_error(c)
 if e!='OK':return result(inp,'REJECT',e,'INITIAL_VALIDATE')
 p=inp['winner'];fill=classify_fill(c,p,inp['intent'],inp.get('deals',[]),inp.get('consumedDealIds',[]));r=gate(inp,{str(p['ticket']):fill},'INITIAL_COMMITTED')
 if r['status']=='PASS' and fill['money']<=0:return result(inp,'REJECT','INITIAL_NET_NOT_POSITIVE','INITIAL_REJECTED',{'fills':{str(p['ticket']):fill},'settlementApplied':False,'allocationApplied':False},['FILL_EVIDENCE_PERSISTED'])
 return r
def big_settlement(inp):
 c=inp['context'];e=context_error(c)
 if e!='OK':return result(inp,'REJECT',e,'BIG_VALIDATE')
 fills={str(p['ticket']):classify_fill(c,p,next(i for i in inp['intents'] if i['positionTicket']==p['ticket']),[d for d in inp.get('deals',[]) if d.get('positionTicket')==p['ticket']],inp.get('consumedDealIds',[])) for p in inp['positions']}
 return gate(inp,fills,'BIG_SETTLED')
def small_settlement(inp):
 if inp.get('dualTail'):return result(inp,'REJECT','DUAL_TAIL','SMALL_BLOCKED')
 r=big_settlement(inp)
 if r['status']=='PASS':r['phase']='SMALL_SETTLED';r['outputDigest']=digest({k:v for k,v in r.items() if k!='outputDigest'})
 return r
def restart_replay(inp):
 fills={k:classify_fill(inp['context'],v['position'],v['intent'],v['deals'],inp.get('consumedDealIds',[])) for k,v in inp['legs'].items()};r=gate(inp,fills,'RESTART_FULL_FILL_RECOVERED')
 if r['status']=='PASS' and set(r['output']['consumedDealIds']) & set(inp.get('consumedDealIds',[])):return result(inp,'CONFLICT','DUPLICATE_FILL','RECONCILIATION_BLOCKED')
 return r
FUNCTIONS={'classify_fill':lambda x:result(x,'PASS','OK','FILL_CLASSIFIED',classify_fill(x['context'],x['position'],x['intent'],x.get('deals',[]),x.get('consumedDealIds',[]))),'initial_lock':initial_lock,'big_settlement':big_settlement,'small_settlement':small_settlement,'restart_replay':restart_replay}
def execute(name,inp):return FUNCTIONS[name](copy.deepcopy(inp)) if name in FUNCTIONS else result(inp,'ERROR','UNKNOWN_FUNCTION','ERROR')
def self_test():
 c={'volumeStep':'.01','volumeMin':'.01','volumeMax':'10'};checks=[grid('1',c['volumeStep']),not grid('0',c['volumeStep']),not grid('NaN',c['volumeStep']),D('1')%D('.01')==0]
 print('\n'.join(f'R4R2_MODEL_{i}={"PASS" if x else "FAIL"}' for i,x in enumerate(checks,1)));print(f'REFERENCE_MODEL_R4_R2_SELF_TESTS={sum(checks)}/{len(checks)}');return all(checks)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
