#!/usr/bin/env python3
"""Corrected PREP-R4-R1 Decimal oracle. Produces serializable offline intents only."""
from decimal import Decimal,InvalidOperation,ROUND_FLOOR,ROUND_HALF_UP
import argparse,copy,hashlib,json
D=lambda x:Decimal(str(x));Q=Decimal('0.01')
def finite(x):
 try:return D(x).is_finite()
 except (InvalidOperation,ValueError,TypeError):return False
def ser(x):
 if isinstance(x,Decimal):return format(x,'f')
 if isinstance(x,dict):return {k:ser(v) for k,v in x.items()}
 if isinstance(x,list):return [ser(v) for v in x]
 return x
def dg(x):return hashlib.sha256(json.dumps(ser(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def res(inp,status='PASS',reason='OK',output=None,intents=None,ledger=None,records=None,phase=''):
 r={'status':status,'reason':reason,'valid':status=='PASS','output':ser(output or {}),'futureBrokerIntents':ser(intents or []),'ledgerDelta':ser(ledger or []),'persistenceRecords':records or [],'transactionPhase':phase,'inputDigest':dg(inp)};r['outputDigest']=dg({k:v for k,v in r.items() if k!='outputDigest'});return r
def validate_context(c):
 required=('accountLogin','symbol','magic','cycleId','actionId','stateRevision','snapshotId','snapshotVersion','snapshotTimestamp','minimumTimestamp','bid','ask','tickSize','volumeMin','volumeMax','volumeStep')
 if any(k not in c for k in required):return 'MISSING_FIELD'
 if any(not finite(c[k]) for k in ('accountLogin','magic','stateRevision','snapshotVersion','snapshotTimestamp','minimumTimestamp','bid','ask','tickSize','volumeMin','volumeMax','volumeStep')):return 'NONFINITE_NUMBER'
 if not c['symbol'] or D(c['accountLogin'])<=0 or D(c['magic'])<=0:return 'IDENTITY'
 if D(c['snapshotTimestamp'])<D(c['minimumTimestamp']):return 'STALE_SNAPSHOT'
 if D(c['tickSize'])<=0 or D(c['ask'])<D(c['bid']):return 'INVALID_BID_ASK'
 return 'OK'
def directional_close_price(direction,c):
 if direction=='BUY':return D(c['bid'])
 if direction=='SELL':return D(c['ask'])
 return None
def position_error(c,p):
 if p.get('ticket',0)<=0:return 'UNKNOWN_POSITION_TICKET'
 if p.get('direction') not in ('BUY','SELL'):return 'UNKNOWN_DIRECTION'
 if p.get('symbol')!=c['symbol']:return 'SYMBOL_MISMATCH'
 if p.get('magic')!=c['magic'] or p.get('cycleId')!=c['cycleId']:return 'OWNERSHIP'
 if not finite(p.get('volume')) or D(p['volume'])<=0:return 'INVALID_VOLUME'
 return 'OK'
def volume_floor(v,c):
 if not finite(v):return None
 n=(D(v)/D(c['volumeStep'])).to_integral_value(rounding=ROUND_FLOOR)*D(c['volumeStep'])
 return n if n==0 or D(c['volumeMin'])<=n<=D(c['volumeMax']) else None
def money_round(v):return D(v).quantize(Q,rounding=ROUND_HALF_UP)
def policy_error(p):
 keys=('CloseFarShare','ReserveShare','PolicyVersion','PolicyRevision','PolicySnapshotId','PolicyTimestamp','PolicyDigest','Fresh')
 if any(k not in p for k in keys):return 'ALLOCATION_POLICY_INVALID'
 if not all(finite(p[k]) for k in ('CloseFarShare','ReserveShare','PolicyVersion','PolicyRevision','PolicyTimestamp')):return 'ALLOCATION_POLICY_INVALID'
 a,b=D(p['CloseFarShare']),D(p['ReserveShare'])
 expected=dg({k:p[k] for k in keys if k!='PolicyDigest'})
 return 'OK' if 0<=a<=1 and 0<=b<=1 and a+b==1 and D(p['PolicyVersion'])>0 and p['Fresh'] is True and p['PolicyDigest']==expected else 'ALLOCATION_POLICY_INVALID'
def deal_error(c,d,position,intent=None):
 required=('dealId','orderId','positionTicket','accountLogin','symbol','magic','cycleId','actionId','eventId','direction','volume','price','confirmed','timestamp')
 if any(k not in d for k in required):return 'DEAL_SCHEMA'
 if not d['confirmed']:return 'DEAL_UNCONFIRMED'
 if d['accountLogin']!=c['accountLogin'] or d['symbol']!=c['symbol'] or d['magic']!=c['magic'] or d['cycleId']!=c['cycleId'] or d['actionId']!=c['actionId']:return 'DEAL_OWNERSHIP'
 if d['positionTicket']!=position['ticket'] or d['direction']!=position['direction']:return 'DEAL_OWNERSHIP'
 if intent and D(d['volume'])>D(intent['normalizedVolume']):return 'DEAL_VOLUME_EXCEEDS_INTENT'
 if directional_close_price(position['direction'],c)!=D(d['price']):return 'PRICE_SIDE_MISMATCH'
 return 'OK'
def position_pnl(c,p):
 price=directional_close_price(p.get('direction'),c)
 if price is None:return None
 sign=D(1) if p['direction']=='BUY' else D(-1)
 return (price-D(p['openPrice']))*sign*D(p['volume'])*D(p.get('moneyPerPriceLot',100))
def net_deals(c,deals,positions,intents):
 seen=set();out={};errors=[];pm={p['ticket']:p for p in positions};im={i['positionTicket']:i for i in intents}
 for d in deals:
  key=(d.get('dealId'),d.get('eventId'))
  if key in seen:errors.append('DUPLICATE_DEAL');continue
  seen.add(key);p=pm.get(d.get('positionTicket'))
  if not p:errors.append('DEAL_OWNERSHIP');continue
  e=deal_error(c,d,p,im.get(p['ticket']))
  if e!='OK':errors.append(e);continue
  out[p['ticket']]=out.get(p['ticket'],D(0))+D(d.get('profit',0))+D(d.get('commission',0))+D(d.get('swap',0))+D(d.get('fee',0))
 return out,errors
def make_intent(c,p,kind,vol,parent='',dependency=None):
 n=volume_floor(vol,c);base={'actionId':c['actionId'],'ticket':p['ticket'],'kind':kind,'volume':str(n)}
 return {'intentId':dg(base)[:20],'accountLogin':c['accountLogin'],'symbol':c['symbol'],'magic':c['magic'],'cycleId':c['cycleId'],'actionId':c['actionId'],'stateRevision':c['stateRevision'],'positionTicket':p['ticket'],'positionRole':p['role'],'actionType':kind,'direction':p['direction'],'normalizedVolume':str(n),'expectedPriceSide':'BID' if p['direction']=='BUY' else 'ASK','parentIntentId':parent,'dependency':dependency or {},'inputDigest':dg(c)}
def initial_lock(x):
 c=x['context'];e=validate_context(c)
 if e!='OK':return res(x,'REJECT',e)
 ps=x.get('positions',[])
 if len(ps)!=2:return res(x,'REJECT','AMBIGUOUS_INITIAL_LOCK')
 if {p.get('direction') for p in ps}!={'BUY','SELL'}:return res(x,'REJECT','AMBIGUOUS_INITIAL_LOCK')
 for p in ps:
  e=position_error(c,p)
  if e!='OK':return res(x,'REJECT',e)
 values=[position_pnl(c,p) for p in ps]
 if not (max(values)>0 and min(values)<0):return res(x,'REJECT','AMBIGUOUS_INITIAL_LOCK')
 winner=values.index(max(values));loser=1-winner;deals=x.get('deals',[]);it=make_intent(c,ps[winner],'CLOSE_POSITION_FULL',ps[winner]['volume']);nets,errs=net_deals(c,deals,ps,[it])
 if errs or ps[winner]['ticket'] not in nets:return res(x,'UNAVAILABLE','RECONCILIATION_REQUIRED',intents=[it],records=['INTENT_PREPARED'],phase='INITIAL_WAIT_CLOSE_CONFIRMATION')
 ignored=nets[ps[winner]['ticket']]
 return res(x,output={'buyCount':1,'sellCount':1,'ignoredInitialPositiveProfit':ignored,'recoveryBudgetWithInitialProfit':'0','recoveryBudgetWithoutInitialProfit':'0','farTicket':ps[loser]['ticket'],'farAssignedAfterConfirmation':True},ledger=[{'source':'IGNORED_INITIAL_POSITIVE_PROFIT','amount':ignored,'consumable':False,'dealIds':[d['dealId'] for d in deals]}],records=['DEAL_CONFIRMED','FAR_ASSIGNED'],phase='INITIAL_COMMITTED')
def execute_big_level_scenario(x):
 c=x['context'];e=validate_context(c)
 if e!='OK':return res(x,'REJECT',e)
 policy=x.get('allocationPolicy',{});e=policy_error(policy)
 if e!='OK':return res(x,'REJECT',e)
 roles={p.get('role'):p for p in x.get('positions',[])}
 if set(('BIG','SMALL','FAR'))-set(roles):return res(x,'REJECT','POSITION_ROLE')
 for p in roles.values():
  e=position_error(c,p)
  if e!='OK':return res(x,'REJECT',e)
 big,small,far=roles['BIG'],roles['SMALL'],roles['FAR'];bi=make_intent(c,big,'CLOSE_POSITION_FULL',big['volume']);si=make_intent(c,small,'CLOSE_POSITION_FULL',small['volume'],bi['intentId'])
 if not x.get('bigSmallIntentsPersisted'):return res(x,output={'phase':'BIG_PHASE_2_PREPARE_BIG_SMALL_INTENTS'},intents=[bi,si],records=['INTENT_PREPARED'],phase='BIG_PHASE_2_PREPARE_BIG_SMALL_INTENTS')
 nets,errs=net_deals(c,x.get('deals',[]),[big,small],[bi,si])
 if errs or big['ticket'] not in nets or small['ticket'] not in nets:return res(x,'UNAVAILABLE','RECONCILIATION_REQUIRED',output={'phase':'BIG_PHASE_4_CONFIRM_BIG_SMALL_DEALS'},intents=[],records=['INTENTS_PERSISTED'],phase='BIG_PHASE_4_CONFIRM_BIG_SMALL_DEALS')
 bn,sn=nets[big['ticket']],nets[small['ticket']];available=max(D(0),bn+sn);raw_close=available*D(policy['CloseFarShare']);raw_reserve=available*D(policy['ReserveShare']);budget=money_round(raw_close);reserve_add=money_round(raw_reserve);remainder=available-budget-reserve_add
 farloss=max(D(0),-position_pnl(c,far));reserve=D(x.get('reserveBefore',0));recovery=bn+sn+reserve-farloss;final=farloss<=bn+sn+reserve and recovery>0
 loss_per_lot=farloss/D(far['volume']) if D(far['volume']) else D(0);partial=D(0) if final or loss_per_lot<=0 else (volume_floor(min(D(far['volume']),budget/loss_per_lot),c) or D(0));consumption=D(0) if final else money_round(partial*loss_per_lot);remainder=available-consumption-reserve_add
 dep={'PARENT_CONFIRMATION_DIGEST':dg(x['deals']),'BIG_DEAL_IDS':[d['dealId'] for d in x['deals'] if d['positionTicket']==big['ticket']],'SMALL_DEAL_IDS':[d['dealId'] for d in x['deals'] if d['positionTicket']==small['ticket']],'ALLOCATION_DIGEST':dg({'budget':budget,'reserveAdd':reserve_add})};fi=make_intent(c,far,'CLOSE_POSITION_FULL' if final else 'CLOSE_POSITION_PARTIAL',far['volume'] if final else partial,si['intentId'],dep) if final or partial else None
 key=x.get('allocationKey');consumed=set(x.get('consumedAllocations',[]));applied_reserve=D(0) if key in consumed else reserve_add
 out={'phase':'BIG_PHASE_7_PREPARE_FAR_INTENT','buyClosePrice':str(directional_close_price('BUY',c)),'sellClosePrice':str(directional_close_price('SELL',c)),'bigNet':bn,'smallNet':sn,'availableProfit':available,'closeFarShare':policy['CloseFarShare'],'reserveShare':policy['ReserveShare'],'rawCloseFarBudget':raw_close,'rawReserveAdd':raw_reserve,'closeFarBudget':budget,'reserveAdd':applied_reserve,'alreadyConsumed':key in consumed,'reserveBefore':reserve,'reserveAfter':reserve+applied_reserve,'unallocatedRemainder':available-consumption-applied_reserve,'actualPartialFarConsumption':consumption,'farLoss':farloss,'recoveryPL':recovery,'finalFarCloseAllowed':final,'partialFarAllowed':not final and partial>0,'partialFarVolume':partial,'reserveUsedForPartialFar':'0','farPriceSource':'SNAPSHOT_DIRECTIONAL_CLOSE'}
 return res(x,output=out,intents=[fi] if fi else [],ledger=[{'allocationKey':key,'reserveAdd':applied_reserve,'alreadyConsumed':key in consumed}],records=['BIG_SMALL_DEALS_CONFIRMED','ALLOCATION_PREPARED'],phase='BIG_PHASE_7_PREPARE_FAR_INTENT')
def execute_small_reversal_scenario(x):
 c=x['context'];e=validate_context(c)
 if e!='OK':return res(x,'REJECT',e)
 roles={p.get('role'):p for p in x.get('positions',[])}
 if set(('BIG','SMALL','FAR'))-set(roles):return res(x,'REJECT','POSITION_ROLE')
 for p in roles.values():
  e=position_error(c,p)
  if e!='OK':return res(x,'REJECT',e)
 close,remain,share=D(x.get('CloseBigOnSmall',-1)),D(x.get('RemainBigOnSmall',-1)),D(x.get('SmallReserveShare',-1))
 if not (0<=close<=1 and 0<=remain<=1 and close+remain==1 and 0<=share<=1):return res(x,'REJECT','SMALL_SHARE_INVALID')
 big,small,far=roles['BIG'],roles['SMALL'],roles['FAR'];sint=make_intent(c,small,'CLOSE_POSITION_FULL',small['volume']);fint=make_intent(c,far,'CLOSE_POSITION_FULL',far['volume'],sint['intentId'])
 if not x.get('smallFarIntentsPersisted'):return res(x,output={'phase':'SMALL_PHASE_2_PREPARE_SMALL_OLD_FAR_INTENTS'},intents=[sint,fint],records=['INTENT_PREPARED'],phase='SMALL_PHASE_2_PREPARE_SMALL_OLD_FAR_INTENTS')
 nets,errs=net_deals(c,x.get('smallFarDeals',[]),[small,far],[sint,fint])
 if errs or small['ticket'] not in nets or far['ticket'] not in nets:return res(x,'UNAVAILABLE','RECONCILIATION_REQUIRED',phase='SMALL_PHASE_4_CONFIRM_SMALL_OLD_FAR_DEALS')
 raw=D(big['volume'])*close;bigclose=volume_floor(raw,c) or D(0);newfar=D(big['volume'])-bigclose;expected=D(big['volume'])*remain
 if abs(newfar-expected)>D(c['volumeStep']) or newfar>=D(far['volume']):return res(x,'REJECT','SMALL_SHARE_CONSERVATION')
 bint=make_intent(c,big,'CLOSE_POSITION_PARTIAL',bigclose,fint['intentId'],{'PARENT_CONFIRMATION_DIGEST':dg(x['smallFarDeals'])})
 bn,berrs=net_deals(c,x.get('bigDeals',[]),[big],[bint])
 if berrs or big['ticket'] not in bn:return res(x,'UNAVAILABLE','RECONCILIATION_REQUIRED',output={'phase':'SMALL_PHASE_7_CONFIRM_BIG_DEAL','rawBigCloseVolume':raw,'bigCloseVolume':bigclose},intents=[bint],phase='SMALL_PHASE_7_CONFIRM_BIG_DEAL')
 source=max(D(0),nets[small['ticket']]);rawadd=source*share;rounded=money_round(rawadd);key=x.get('allocationKey');consumed=key in set(x.get('consumedAllocations',[]));add=D(0) if consumed else rounded
 out={'phase':'SMALL_PHASE_9_APPLY_RESERVE','smallClosedVolume':small['volume'],'oldFarClosedVolume':far['volume'],'bigVolumeBefore':big['volume'],'closeBigOnSmall':close,'remainBigOnSmall':remain,'rawBigCloseVolume':raw,'bigClosedVolume':bigclose,'newFarVolume':newfar,'expectedRemainVolume':expected,'smallReserveSourceMoney':source,'smallReserveShare':share,'rawSmallReserveAdd':rawadd,'roundedSmallReserveAdd':add,'allocationKey':key,'alreadyConsumed':consumed,'reserveBefore':x.get('reserveBefore','0'),'reserveAfter':D(x.get('reserveBefore',0))+add,'newFarAssignedAfterBigConfirmation':True}
 return res(x,output=out,ledger=[{'allocationKey':key,'reserveAdd':add}],records=['SMALL_FAR_DEALS_CONFIRMED','BIG_DEAL_CONFIRMED','NEW_FAR_ASSIGNED','RESERVE_APPLIED'],phase='SMALL_PHASE_9_APPLY_RESERVE')
FUNCTIONS={'initial_lock':initial_lock,'execute_big_level_scenario':execute_big_level_scenario,'execute_small_reversal_scenario':execute_small_reversal_scenario}
def execute(n,x):return FUNCTIONS[n](copy.deepcopy(x)) if n in FUNCTIONS else res(x,'ERROR','UNKNOWN_FUNCTION')
def self_test():
 c={'bid':'1.1','ask':'1.2','volumeStep':'0.1','volumeMin':'0.1','volumeMax':'10'};checks=[directional_close_price('BUY',c)==D('1.1'),directional_close_price('SELL',c)==D('1.2'),directional_close_price('X',c) is None,volume_floor('1.29',c)==D('1.2')]
 print('\n'.join(f'R4R1_MODEL_{i}={"PASS" if x else "FAIL"}' for i,x in enumerate(checks,1)));print(f'REFERENCE_MODEL_R4_R1_SELF_TESTS={sum(checks)}/{len(checks)}');return all(checks)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
