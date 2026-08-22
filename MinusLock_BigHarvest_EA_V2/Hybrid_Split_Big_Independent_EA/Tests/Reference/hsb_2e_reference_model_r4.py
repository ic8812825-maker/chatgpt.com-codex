#!/usr/bin/env python3
"""PREP-R4 executable Decimal oracle. It creates offline intents; it never dispatches."""
from decimal import Decimal,InvalidOperation,ROUND_FLOOR
from dataclasses import dataclass,asdict
import argparse,copy,hashlib,json
D=lambda v:Decimal(str(v))
CONTEXT=('accountLogin','symbol','magic','cycleId','planId','actionId','eventId','stateRevision','snapshotId','snapshotVersion','snapshotTimestamp','minimumTimestamp','currency','moneyDigits','point','tickSize','volumeMin','volumeMax','volumeStep','bid','ask','spreadPoints')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
def dec(v):
 try:
  x=D(v);return x if x.is_finite() else None
 except (InvalidOperation,ValueError,TypeError):return None
def serial(x):
 if isinstance(x,Decimal):return format(x,'f')
 if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
 if isinstance(x,list):return [serial(v) for v in x]
 return x
def result(inp,status='PASS',reason='OK',output=None,positionDelta=None,ledgerDelta=None,reserveDelta='0',farDelta='0',persistenceRecords=None,futureBrokerIntents=None,logEvents=None):
 r={'status':status,'reason':reason,'valid':status=='PASS','output':serial(output or {}),'positionDelta':serial(positionDelta or []),'ledgerDelta':serial(ledgerDelta or []),'reserveDelta':str(reserveDelta),'farDelta':str(farDelta),'persistenceRecords':persistenceRecords or [],'futureBrokerIntents':serial(futureBrokerIntents or []),'logEvents':logEvents or [],'inputDigest':digest(inp)};r['outputDigest']=digest({k:v for k,v in r.items() if k!='outputDigest'});return r
def validate_context(x):
 missing=[k for k in CONTEXT if k not in x]
 if missing:return result(x,'REJECT','MISSING_FIELD',{'missing':missing})
 nums=[x[k] for k in ('accountLogin','magic','stateRevision','snapshotVersion','snapshotTimestamp','minimumTimestamp','point','tickSize','volumeMin','volumeMax','volumeStep','bid','ask','spreadPoints')]
 if any(dec(v) is None for v in nums):return result(x,'REJECT','NONFINITE_NUMBER')
 if not x['symbol'] or not x['cycleId'] or D(x['accountLogin'])<=0 or D(x['magic'])<=0:return result(x,'REJECT','IDENTITY')
 if D(x['snapshotTimestamp'])<D(x['minimumTimestamp']) or D(x['snapshotVersion'])<=0:return result(x,'REJECT','STALE_SNAPSHOT')
 if D(x['tickSize'])<=0 or D(x['volumeStep'])<=0 or D(x['ask'])<D(x['bid']):return result(x,'REJECT','INVALID_GEOMETRY')
 return result(x)
def validate_position(c,p,role=None):
 if p.get('direction') not in ('BUY','SELL'):return 'INVALID_DIRECTION'
 if p.get('ticket',0)<=0:return 'UNKNOWN_POSITION_TICKET'
 if p.get('symbol')!=c['symbol'] or p.get('magic')!=c['magic'] or p.get('cycleId')!=c['cycleId']:return 'OWNERSHIP'
 if role and p.get('role')!=role:return 'POSITION_ROLE'
 v=dec(p.get('volume'));return 'INVALID_VOLUME' if v is None or v<=0 else 'OK'
def normalize_volume(v,c):
 v=dec(v)
 if v is None or v<0:return None
 step=D(c['volumeStep']);n=(v/step).to_integral_value(rounding=ROUND_FLOOR)*step
 if n and not D(c['volumeMin'])<=n<=D(c['volumeMax']):return None
 return n
def directional_close_price(direction,c):
 if direction=='BUY':return D(c['bid']) # MUTATION_R4M010
 if direction=='SELL':return D(c['ask']) # MUTATION_R4M011
 return None # MUTATION_R4M012
def deal_money(deals):
 seen=set();grossProfit=grossLoss=commission=swap=fee=D(0)
 for d in deals:
  if not d.get('confirmed'):continue
  key=(d.get('dealId'),d.get('eventId'))
  if key in seen:return None
  seen.add(key);p=D(d['profit']);grossProfit+=max(p,D(0));grossLoss+=min(p,D(0));commission+=D(d.get('commission',0)) # MUTATION_R4M014
  swap+=D(d.get('swap',0)) # MUTATION_R4M015
  fee+=D(d.get('fee',0)) # MUTATION_R4M016
 return {'grossProfit':grossProfit,'grossLoss':grossLoss,'commission':commission,'swap':swap,'fee':fee,'net':grossProfit+grossLoss+commission+swap+fee}
def far_loss(p):
 price=D(p['currentClosePrice']);op=D(p['openPrice']);sign=D(1) if p['direction']=='BUY' else D(-1);return max(D(0),-(price-op)*sign*D(p['volume'])*D(p.get('moneyPerPriceLot',100))) # MUTATION_R4M013
@dataclass(frozen=True)
class HSBI_ReferenceBrokerIntent:
 intentId:str;accountLogin:int;symbol:str;magic:int;cycleId:str;planId:str;actionId:str;stateRevision:int;positionTicket:int;positionRole:str;actionType:str;direction:str;requestedVolume:str;normalizedVolume:str;expectedPriceSide:str;deviationPoints:int;fillingPolicy:str;comment:str;parentIntentId:str;inputDigest:str
def intent(c,p,kind,volume,parent=''):
 n=normalize_volume(volume,c);side='BID' if p['direction']=='BUY' else 'ASK';raw={'action':c['actionId'],'ticket':p['ticket'],'kind':kind,'volume':str(n)}
 return asdict(HSBI_ReferenceBrokerIntent(digest(raw)[:20],c['accountLogin'],c['symbol'],c['magic'],c['cycleId'],c['planId'],c['actionId'],c['stateRevision'],p['ticket'],p['role'],kind,p['direction'],str(volume),str(n),side,10,'FOK','R4 offline',parent,digest(c)))
def initial_lock(x):
 c=x['context'];v=validate_context(c)
 if not v['valid']:return v
 ps=x.get('positions',[])
 if len(ps)!=2:return result(x,'REJECT','INITIAL_PAIR_REQUIRED')
 for p in ps:
  e=validate_position(c,p)
  if e!='OK':return result(x,'REJECT',e)
 profits=[D(p.get('unrealizedPnL',0)) for p in ps]
 if profits[0]==profits[1]:return result(x,'REJECT','AMBIGUOUS_INITIAL_RESULT')
 win=0 if profits[0]>profits[1] else 1;far=1-win
 ignored=max(profits[win],D(0));out={'ignoredInitialPositiveProfit':ignored,'recoveryBudgetWithInitialProfit':'0','recoveryBudgetWithoutInitialProfit':'0','farTicket':ps[far]['ticket'],'farVolume':ps[far]['volume']}
 i=intent(c,ps[win],'CLOSE_POSITION_FULL',ps[win]['volume'])
 return result(x,output=out,ledgerDelta=[{'source':'IGNORED_INITIAL_POSITIVE_PROFIT','amount':str(ignored),'consumable':False}],futureBrokerIntents=[i],persistenceRecords=['INTENT_PREPARED'],logEvents=['INITIAL_PROFIT_IGNORED'])
def execute_big_level_scenario(x):
 c=x['context'];v=validate_context(c)
 if not v['valid']:return v
 if x.get('fsmState')!='BIG_LEVEL_REACHED':return result(x,'REJECT','FSM_STATE')
 roles={p.get('role'):p for p in x.get('positions',[])}
 if set(('BIG','SMALL','FAR'))-set(roles):return result(x,'REJECT','POSITION_ROLE')
 for role in ('BIG','SMALL','FAR'):
  e=validate_position(c,roles[role],role)
  if e!='OK':return result(x,'REJECT',e)
 big,small,far=roles['BIG'],roles['SMALL'],roles['FAR'];bi=intent(c,big,'CLOSE_POSITION_FULL',big['volume']);si=intent(c,small,'CLOSE_POSITION_FULL',small['volume'],bi['intentId'])
 deals=x.get('deals',[]);dm=deal_money(deals)
 if dm is None:return result(x,'REJECT','TRANSACTION_CONFLICT') # MUTATION_R4M027
 confirmed={d['positionTicket']:D(d['volume']) for d in deals if d.get('confirmed')}
 bc=confirmed.get(big['ticket'],D(0));sc=confirmed.get(small['ticket'],D(0));bigfull=bc==D(big['volume']);smallfull=sc==D(small['volume'])
 if not (bigfull and smallfull):return result(x,'UNAVAILABLE','PARTIAL_FILL',{'bigCloseVolume':bc,'smallCloseVolume':sc},futureBrokerIntents=[bi,si]) # MUTATION_R4M032
 bn=sum((D(d['profit'])+D(d.get('commission',0))+D(d.get('swap',0))+D(d.get('fee',0)) for d in deals if d.get('confirmed') and d['positionTicket']==big['ticket']),D(0));sn=sum((D(d['profit'])+D(d.get('commission',0))+D(d.get('swap',0))+D(d.get('fee',0)) for d in deals if d.get('confirmed') and d['positionTicket']==small['ticket']),D(0));fl=far_loss(far);reserve=D(x.get('reserve','0'));recovery=bn+sn+reserve-fl;coverage=bn+sn+reserve-fl
 final=fl<=bn+sn+reserve and recovery>0 # MUTATION_R4M033 MUTATION_R4M034
 budget=max(D(0),bn+sn) # MUTATION_R4M018
 loss_per_lot=fl/D(far['volume']) if D(far['volume']) else D(0);partial=D(0) if final or loss_per_lot<=0 else (normalize_volume(min(D(far['volume']),budget/loss_per_lot),c) or D(0))
 fi=intent(c,far,'CLOSE_POSITION_FULL' if final else 'CLOSE_POSITION_PARTIAL',far['volume'] if final else partial,si['intentId']) if final or partial else None
 far_after=D(0) if final else D(far['volume'])-partial;reserve_add=max(D(0),bn+sn-budget);out={'bigCloseVolume':bc,'smallCloseVolume':sc,'bigNetMoney':bn,'smallNetMoney':sn,'farLossBefore':fl,'recoveryPL':recovery,'reserveCoverage':coverage,'finalCloseAllowed':final,'closeFarBudget':budget,'partialFarVolume':partial,'farVolumeAfter':far_after,'farLossAfter':fl*(far_after/D(far['volume'])),'reserveBefore':reserve,'reserveAddition':reserve_add,'reserveAfter':reserve+reserve_add,'sourceMoney':max(D(0),bn+sn),'allocatedPartialFar':min(budget,partial*loss_per_lot),'allocatedReserve':reserve_add,'allocatedOther':'0','unallocatedRemainder':max(D(0),bn+sn)-min(budget,partial*loss_per_lot)-reserve_add,'bigVolumeBefore':D(big['volume']),'bigVolumeClosed':bc,'bigVolumeRemaining':D(big['volume'])-bc,'smallVolumeBefore':D(small['volume']),'smallVolumeClosed':sc,'smallVolumeRemaining':D(small['volume'])-sc}
 intents=[bi,si]+([fi] if fi else []);return result(x,output=out,positionDelta=[{'ticket':big['ticket'],'closed':str(bc)},{'ticket':small['ticket'],'closed':str(sc)},{'ticket':far['ticket'],'closed':str(D(far['volume'])-far_after)}],ledgerDelta=[{'source':'CONFIRMED_DEALS','amount':str(bn+sn)}],reserveDelta=reserve_add,farDelta=far_after-D(far['volume']),persistenceRecords=['INTENT_PREPARED','DEALS_CONFIRMED','ALLOCATION_APPLIED','FSM_COMMIT'],futureBrokerIntents=intents,logEvents=['BIG_SETTLED'])
def execute_small_reversal_scenario(x):
 c=x['context'];v=validate_context(c)
 if not v['valid']:return v
 if x.get('fsmState')!='OLD_FAR_REACHED':return result(x,'REJECT','FSM_STATE')
 roles={p.get('role'):p for p in x.get('positions',[])}
 if set(('BIG','SMALL','FAR'))-set(roles):return result(x,'REJECT','POSITION_ROLE')
 for role in roles:
  e=validate_position(c,roles[role],role)
  if e!='OK':return result(x,'REJECT',e)
 big,small,old=roles['BIG'],roles['SMALL'],roles['FAR'];close_big=normalize_volume(x['closeBigOnSmall'],c)
 if close_big is None or close_big>D(big['volume']):return result(x,'REJECT','INVALID_VOLUME')
 rem=D(big['volume'])-close_big # MUTATION_R4M022
 if rem>=D(old['volume']):return result(x,'REJECT','NEW_FAR_NOT_COMPRESSED') # MUTATION_R4M023 R4M024
 if x.get('dualTail'):return result(x,'REJECT','DUAL_TAIL') # MUTATION_R4M025
 intents=[intent(c,small,'CLOSE_POSITION_FULL',small['volume']),intent(c,old,'CLOSE_POSITION_FULL',old['volume']),intent(c,big,'CLOSE_POSITION_PARTIAL',close_big)]
 deals=x.get('deals',[]);dm=deal_money(deals)
 if dm is None:return result(x,'REJECT','TRANSACTION_CONFLICT')
 vols={d['positionTicket']:D(d['volume']) for d in deals if d.get('confirmed')}
 sv=vols.get(small['ticket'],D(0));ov=vols.get(old['ticket'],D(0));bv=vols.get(big['ticket'],D(0))
 if sv!=D(small['volume']) or ov!=D(old['volume']) or bv!=close_big:return result(x,'UNAVAILABLE','PARTIAL_FILL',futureBrokerIntents=intents) # MUTATION_R4M019 R4M020 R4M021
 committed=bool(x.get('transitionCommitted'))
 if x.get('createNextLevel') and not committed:return result(x,'REJECT','TRANSITION_NOT_COMMITTED') # MUTATION_R4M026
 net=lambda t:sum((D(d['profit'])+D(d.get('commission',0))+D(d.get('swap',0))+D(d.get('fee',0)) for d in deals if d.get('confirmed') and d['positionTicket']==t),D(0));sn,on,bn=net(small['ticket']),net(old['ticket']),net(big['ticket']);key=x.get('allocationKey');consumed=set(x.get('consumedAllocations',[]));ra=D(0) if key in consumed else max(D(0),sn)*D(x.get('smallReserveShare','0')) # MUTATION_R4M028
 out={'smallClosedVolume':sv,'oldFarClosedVolume':ov,'bigClosedVolume':bv,'bigRemainingVolume':rem,'newFarVolume':rem,'oldFarVolume':D(old['volume']),'newFarCompression':D(old['volume'])-rem,'smallNetMoney':sn,'oldFarNetMoney':on,'bigNetMoney':bn,'reserveAddition':ra,'reserveAfter':D(x.get('reserve','0'))+ra,'dualTail':False,'transitionCommitted':committed,'bigVolumeBefore':D(big['volume']),'bigVolumeClosed':bv,'bigVolumeRemaining':rem}
 return result(x,output=out,positionDelta=[{'ticket':small['ticket'],'closed':str(sv)},{'ticket':old['ticket'],'closed':str(ov)},{'ticket':big['ticket'],'closed':str(bv),'newRole':'FAR'}],ledgerDelta=[{'allocationKey':key,'amount':str(ra)}],reserveDelta=ra,farDelta=rem-D(old['volume']),persistenceRecords=['DEALS_CONFIRMED','ALLOCATION_APPLIED','FSM_COMMIT'] if committed else ['DEALS_CONFIRMED','ALLOCATION_APPLIED'],futureBrokerIntents=intents,logEvents=['SMALL_SETTLED'])
def restart_replay(x):
 if x.get('outcome')=='UNKNOWN':return result(x,'UNAVAILABLE','RECONCILIATION_REQUIRED') # MUTATION_R4M031
 if x.get('actionId') in x.get('committedActions',[]):return result(x,'NO_OP','ALREADY_COMMITTED',{'actionId':x['actionId']})
 return result(x,output={'actionId':x['actionId'],'eventId':x['eventId'],'replayAction':x.get('expectedReplayAction','RECONCILE')},persistenceRecords=x.get('persistedRecords',[])) # MUTATION_R4M029 R4M030
FUNCTIONS={'validate_context':validate_context,'initial_lock':initial_lock,'execute_big_level_scenario':execute_big_level_scenario,'execute_small_reversal_scenario':execute_small_reversal_scenario,'restart_replay':restart_replay}
def execute(name,x):return FUNCTIONS[name](copy.deepcopy(x)) if name in FUNCTIONS else result(x,'ERROR','UNKNOWN_FUNCTION')
def self_test():
 checks={'direction':directional_close_price('X',{'bid':'1','ask':'2'}) is None,'grid':normalize_volume('0.26',{'volumeStep':'0.1','volumeMin':'0.1','volumeMax':'1'})==D('0.2'),'fee':deal_money([{'dealId':1,'eventId':1,'confirmed':True,'profit':'10','commission':'-1','swap':'-2','fee':'-3'}])['net']==D('4'),'digest':digest({'b':2,'a':1})==digest({'a':1,'b':2})}
 print('\n'.join(f'RM4_{k}={"PASS" if v else "FAIL"}' for k,v in checks.items()));print(f'REFERENCE_MODEL_R4_SELF_TESTS={sum(checks.values())}/{len(checks)}');return all(checks.values())
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
