#!/usr/bin/env python3
"""R4-R6 broker contour: immutable evidence with position/intent binding."""
from dataclasses import dataclass,asdict,is_dataclass
from decimal import Decimal,InvalidOperation
import copy,hashlib,json

D=lambda x:Decimal(str(x))
def canon(x):
    if is_dataclass(x):return canon(asdict(x))
    if isinstance(x,Decimal):return str(x)
    if isinstance(x,dict):return {str(k):canon(v) for k,v in sorted(x.items(),key=lambda p:str(p[0]))}
    if isinstance(x,(list,tuple)):return [canon(v) for v in x]
    return x
def digest(x):return hashlib.sha256(json.dumps(canon(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def integer(v,positive=False):return type(v) is int and v>=(1 if positive else 0)
def grid(v,step):
    try:return D(step)>0 and D(v)>0 and D(v)%D(step)==0 and D(v).is_finite()
    except (InvalidOperation,TypeError,ValueError):return False

@dataclass(frozen=True)
class HSBI_QuoteSnapshot:
    schemaVersion:int;accountLogin:int;symbol:str;magic:int;cycleId:str;stateRevision:int;snapshotId:str;snapshotRevision:int;bid:Decimal;ask:Decimal;timestamp:int;digestValue:str=''
    def body(self):return {k:v for k,v in asdict(self).items() if k!='digestValue'}
    def sealed(self):return self.__class__(**{**self.body(),'digestValue':digest(self.body())})

@dataclass(frozen=True)
class HSBI_ExecutionPricePolicy:
    schemaVersion:int;symbol:str;digits:int;tickSize:Decimal;deviationTicks:int;buyCloseSide:str;sellCloseSide:str;quoteSource:str;snapshotId:str;snapshotRevision:int;validFrom:int;validUntil:int;policyId:str;normativeSourceId:str;policyDigest:str=''
    def body(self):return {k:v for k,v in asdict(self).items() if k!='policyDigest'}
    def sealed(self):return self.__class__(**{**self.body(),'policyDigest':digest(self.body())})

@dataclass(frozen=True)
class HSBI_DealEvidenceRecord:
    schemaVersion:int;accountLogin:int;symbol:str;magic:int;cycleId:str;transactionId:str;actionId:str;stateRevision:int;snapshotId:str;snapshotRevision:int;dealId:str;eventId:str;orderId:str;positionTicket:int;positionRole:str;direction:str;intentId:str;volume:Decimal;price:Decimal;profit:Decimal;commission:Decimal;swap:Decimal;fee:Decimal;netMoney:Decimal;confirmed:bool;dealTimestamp:int;receivedSequence:int;sourceDigest:str;recordDigest:str=''
    def body(self):return {k:v for k,v in asdict(self).items() if k!='recordDigest'}
    def sealed(self):return self.__class__(**{**self.body(),'recordDigest':digest(self.body())})

IDENTITY=('accountLogin','symbol','magic','cycleId','transactionId','actionId','stateRevision')
ROLES={'WINNER','BIG','SMALL','OLD_FAR','FAR'}
def price_bounds(snapshot,policy,direction):
    if snapshot.digestValue!=digest(snapshot.body()) or policy.policyDigest!=digest(policy.body()):raise ValueError('PRICE_TRUST_DIGEST_INVALID')
    if policy.snapshotId!=snapshot.snapshotId or policy.snapshotRevision!=snapshot.snapshotRevision or policy.symbol!=snapshot.symbol:raise ValueError('PRICE_TRUST_IDENTITY_INVALID')
    side=policy.buyCloseSide if direction=='BUY' else policy.sellCloseSide if direction=='SELL' else None
    if side not in {'BID','ASK'}:raise ValueError('PRICE_SIDE_INVALID')
    center=snapshot.bid if side=='BID' else snapshot.ask;deviation=policy.tickSize*policy.deviationTicks
    return center-deviation,center+deviation

def validate_binding(record,context,positions,intents,snapshot,policy):
    if not isinstance(record,HSBI_DealEvidenceRecord):return 'DEAL_SCHEMA_INVALID'
    if record.recordDigest!=digest(record.body()):return 'SOURCE_RECORD_DIGEST_MISMATCH'
    if type(record.confirmed)is not bool or not record.confirmed:return 'DEAL_CONFIRMED_INVALID'
    if any(getattr(record,k)!=context.get(k) for k in IDENTITY):return 'DEAL_IDENTITY_MISMATCH'
    if record.snapshotId!=snapshot.snapshotId or record.snapshotRevision!=snapshot.snapshotRevision:return 'DEAL_SNAPSHOT_MISMATCH'
    p=next((p for p in positions if p.get('ticket')==record.positionTicket),None)
    if p is None:return 'ORPHAN_DEAL'
    if record.positionRole not in ROLES or p.get('role')!=record.positionRole:return 'DEAL_ROLE_MISMATCH'
    if p.get('direction')!=record.direction:return 'DEAL_DIRECTION_MISMATCH'
    i=next((i for i in intents if i.get('intentId')==record.intentId),None)
    if i is None:return 'DEAL_INTENT_MISSING'
    if i.get('positionTicket')!=p['ticket'] or i.get('positionRole')!=p['role'] or i.get('direction')!=p['direction']:return 'DEAL_INTENT_BINDING_MISMATCH'
    if i.get('executable') is not True:return 'DEAL_INTENT_NOT_EXECUTABLE'
    if record.netMoney!=record.profit+record.commission+record.swap+record.fee:return 'DEAL_MONEY_RECORD_MISMATCH'
    if not integer(record.schemaVersion,True) or not integer(record.stateRevision):return 'REVISION_INVALID'
    if not grid(record.volume,context['volumeStep']):return 'VOLUME_GRID_INVALID'
    if not grid(record.price,policy.tickSize):return 'PRICE_GRID_INVALID'
    if record.dealTimestamp<max(snapshot.timestamp,policy.validFrom) or record.dealTimestamp>policy.validUntil:return 'DEAL_TIMESTAMP_INVALID'
    try:lo,hi=price_bounds(snapshot,policy,record.direction)
    except ValueError as e:return str(e)
    if not lo<=record.price<=hi:return 'EXECUTION_PRICE_OUTSIDE_TRUSTED_POLICY'
    return None

def derive(records,positions):
    out={'consumedDealIds':[],'seenEventIds':[],'dealEventBindings':{},'cumulativeFills':{},'moneyByDeal':{},'moneyByTicket':{},'moneyByRole':{},'volumeByTicket':{}}
    roles={str(p['ticket']):p['role'] for p in positions}
    for r in records:
        t=str(r.positionTicket);out['consumedDealIds'].append(r.dealId);out['seenEventIds'].append(r.eventId);out['dealEventBindings'][r.dealId]=r.eventId;out['cumulativeFills'][t]=out['cumulativeFills'].get(t,D(0))+r.volume;out['volumeByTicket'][t]=out['cumulativeFills'][t];out['moneyByDeal'][r.dealId]=r.netMoney;out['moneyByTicket'][t]=out['moneyByTicket'].get(t,D(0))+r.netMoney;role=roles[t];out['moneyByRole'][role]=out['moneyByRole'].get(role,D(0))+r.netMoney
    return out

def revalidate_persisted(state,context,positions,intents,snapshot,policy):
    records=state.get('acceptedDealRecords',[]);deal_ids=set();event_ids=set()
    for r in records:
        e=validate_binding(r,context,positions,intents,snapshot,policy)
        if e:return e
        if r.dealId in deal_ids:return 'DEAL_DUPLICATE'
        if r.eventId in event_ids:return 'EVENT_DUPLICATE'
        deal_ids.add(r.dealId);event_ids.add(r.eventId)
    expected=derive(records,positions)
    if any(canon(state.get(k,{} if isinstance(v,dict) else []))!=canon(v) for k,v in expected.items()):return 'PERSISTED_DERIVED_STATE_MISMATCH'
    return None

def validate_all_then_apply(state,new_records,context,positions,intents,snapshot,policy):
    error=revalidate_persisted(state,context,positions,intents,snapshot,policy)
    if error:return state,error
    existing_d=set(state['consumedDealIds']);existing_e=set(state['seenEventIds']);batch_d=set();batch_e=set()
    for r in new_records:
        e=validate_binding(r,context,positions,intents,snapshot,policy)
        if e:return state,e
        if r.dealId in existing_d|batch_d:return state,'DEAL_DUPLICATE'
        if r.eventId in existing_e|batch_e:return state,'EVENT_DUPLICATE'
        batch_d.add(r.dealId);batch_e.add(r.eventId)
    if not new_records:return state,'EMPTY_BATCH'
    out=copy.deepcopy(state);out['acceptedDealRecords']=list(state['acceptedDealRecords'])+list(new_records);out.update(derive(out['acceptedDealRecords'],positions));out['evidenceRevision']=state['evidenceRevision']+1
    return out,None
