"""R0B PROPOSED contract oracle. No R0A/production imports, broker IO or trading.

Authority/history/journal are independently assembled test fixtures. They are not
evidence of an actual broker account. In-memory commit is NOT durable persistence.
"""
import copy
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from hashlib import sha256
import json
import math
import struct

BUCKETS=('FinalReserve','PartialFar','Transition','Carry','ResidualHeld')
ID_FIELDS=('Broker','Server','Account','Symbol','Magic','Deal','Order','Position',
           'Cycle','Plan','StateRevision','AllocationEvent','PolicyVersion','SnapshotID')


def number(v):
    if isinstance(v,(float,bool)):
        raise ValueError('binary float/bool forbidden')
    d=Decimal(v)
    if not d.is_finite():
        raise ValueError('nonfinite money')
    return d


def unit(digits):
    if type(digits) is not int or not 0<=digits<=8:
        raise ValueError('unknown precision')
    return Decimal(1).scaleb(-digits)


def canonical(value):
    def convert(x):
        if isinstance(x,Decimal):
            return '0' if x==0 else format(number(x).normalize(),'f')
        if isinstance(x,float):
            raise ValueError('float in payload')
        if isinstance(x,dict):return {k:convert(v) for k,v in sorted(x.items())}
        if isinstance(x,(list,tuple)):return [convert(v) for v in x]
        return x
    return json.dumps(convert(value),sort_keys=True,separators=(',',':'),ensure_ascii=False)


def digest(value):return sha256(canonical(value).encode()).hexdigest()


def raw64(value):
    """Proposed source codec, NOT monetary arithmetic or posted conversion."""
    if type(value) is not float or not math.isfinite(value):raise ValueError('invalid raw binary64')
    return struct.pack('>d',0.0 if value==0.0 else value).hex()


def candidate_round(raw,digits):
    return number(raw).quantize(unit(digits),rounding=ROUND_HALF_EVEN)


def posted(raw,currency,digits,receipt,mode='BROKER_POSTED',verified_local_policy=False):
    if not currency or digits is None or receipt is None:
        return 'UNAVAILABLE',None
    q=unit(digits);raw=number(raw)
    if receipt['currency']!=currency or receipt['digits']!=digits or number(receipt['raw'])!=raw:
        return 'UNAVAILABLE',None
    value=number(receipt['posted'])
    if value.quantize(q)!=value:
        return 'UNAVAILABLE',None
    if mode=='BROKER_POSTED':return 'POSTED',value
    if mode=='LOCAL_VERIFIED' and verified_local_policy and candidate_round(raw,digits)==value:
        return 'POSTED',value
    return 'UNAVAILABLE',None


def allocate(posted_net,shares,digits,role='BigCore'):
    n=max(Decimal(0),number(posted_net));q=unit(digits)
    s=[number(v) for v in shares]
    if len(s)!=4 or any(v<0 or v>1 for v in s) or sum(s)>1 or n.quantize(q)!=n:
        raise ValueError('invalid allocation input')
    values=[(n*v).quantize(q,rounding=ROUND_FLOOR) for v in s] if role in ('BigCore','BigTrend') else [Decimal(0)]*4
    return dict(zip(BUCKETS,values+[n-sum(values)]))


def balance(state):
    q=unit(state['digits']);g=state['grant'];r=state['remaining'];c=state['consumed'];v=state['reserved']
    if any(set(x)!=set(BUCKETS) for x in (g,r,c,v)):return False
    vals=[number(state['net']),number(state['unallocated'])]+[number(x[b]) for x in (g,r,c,v) for b in BUCKETS]
    if any(x<0 or x.quantize(q)!=x for x in vals):return False
    if state['phase'] not in ('PREPARED','COMMITTED'):return False
    if state['phase']=='COMMITTED' and state['unallocated']!=0:return False
    if sum(g.values())+state['unallocated']!=state['net']:return False
    for b in BUCKETS:
        if r[b]+c[b]!=g[b]:return False
        if v[b]>r[b]:return False
    return True


def source_key(identity):return tuple(identity[k] for k in ('Broker','Server','Account','Deal'))
def event_key(request):return tuple(request['identity'][k] for k in ('Broker','Server','Account'))+(request['event'],)


def proof_bundle(record,allocation,expected):
    return {'record':record,'allocation':allocation,'expected':expected}


def authorize(request,state,journal,authority):
    if authority is None or journal is None or not authority['complete'] or authority['history'] is None:
        return 'UNAVAILABLE'
    now=authority['now'];snapshot=authority['snapshot']
    if now-authority['historyObservedAt']>authority['historyMaxAge']:
        return 'UNAVAILABLE'
    if now>snapshot['validUntil']:
        return 'UNAVAILABLE'
    expected=authority['identity']
    if any(request['identity'][k]!=expected[k] for k in ('Broker','Server','Account')):
        return 'REJECT'
    ek=event_key(request)
    if ek in journal:
        return 'NO_OP' if journal[ek]==canonical(request) else 'CONFLICT'
    # Single independent identity comparison, not copied from submitted proof.
    if any(request['identity'][k]!=expected[k] for k in ID_FIELDS):
        return 'REJECT'
    if any(type(request['identity'][k]) is not int or (request['identity'][k]==0 if k=='Magic' else request['identity'][k]<=0) for k in ID_FIELDS if k not in ('Broker','Server','Symbol')):
        return 'REJECT'
    if request['identity']['StateRevision']!=state['revision'] or request['event']<=0:
        return 'REJECT'
    allocation=authority['allocations'].get(request['allocation'])
    if allocation is None:return 'REJECT'
    if allocation['policyVersion']!=expected['PolicyVersion'] or allocation['event']!=expected['AllocationEvent']:return 'CONFLICT'
    if state['allocation']!=request['allocation']:return 'REJECT'
    if state['source']!=allocation['source']:return 'REJECT'
    record=authority['history'].get(allocation['source'])
    if record is None:return 'REJECT'
    if not record['closingConfirmed']:return 'REJECT'
    if record['role'] not in ('BigCore','BigTrend'):return 'REJECT'
    if source_key(record['identity'])!=allocation['source']:return 'CONFLICT'
    if any(record['identity'][k]!=expected[k] for k in ('Broker','Server','Account','Symbol','Magic','Deal','Order','Position','Cycle')):
        return 'REJECT'
    raw=sum((number(record[k]) for k in ('profit','swap','commission','fee')),Decimal(0))
    if raw!=number(record['rawNet']):return 'CONFLICT'
    status,actual=posted(raw,record['currency'],record['digits'],record['receipt'])
    if status!='POSTED':return 'UNAVAILABLE'
    if max(Decimal(0),actual)!=state['net']:return 'CONFLICT'
    if state['grant']!=allocation['grant']:return 'CONFLICT'
    if request['currency']!=state['currency'] or state['currency']!=record['currency']:return 'REJECT'
    if request['digits']!=state['digits'] or state['digits']!=record['digits']:return 'REJECT'
    if request['consumptionPolicy']!=authority['consumptionPolicy']:return 'REJECT'
    if request['identity']['PolicyVersion'] not in authority['approvedPolicies']:return 'UNAVAILABLE'
    if not balance(state) or state['phase']!='COMMITTED':return 'REJECT'
    if request['bucket']!='FinalReserve' or request['purpose']!='CatchUp':return 'REJECT'
    amount=number(request['amount'])
    if amount.quantize(unit(state['digits']))!=amount:return 'REJECT'
    if amount<=0 or amount>state['remaining']['FinalReserve']-state['reserved']['FinalReserve']:return 'REJECT'
    if request['proofDigest']!=digest(proof_bundle(record,allocation,expected)):return 'REJECT'
    return 'ELIGIBLE_FOR_COMMIT'


def apply_for_test(request,state,journal,authority):
    try:status=authorize(request,state,journal,authority)
    except ValueError:status='REJECT'  # malformed/nonfinite Decimal input, never a commit
    s,j,a=copy.deepcopy(state),copy.deepcopy(journal),copy.deepcopy(authority)
    if status=='ELIGIBLE_FOR_COMMIT':
        n=number(request['amount']);s['remaining']['FinalReserve']-=n;s['consumed']['FinalReserve']+=n
        s['revision']+=1;a['identity']['StateRevision']=s['revision']
        j[event_key(request)]=canonical(request)
        return 'COMMITTED_IN_MEMORY',s,j,a
    return status,s,j,a


def classify_grant(existing,incoming):
    if existing['allocation']!=incoming['allocation']:return 'NEW'
    return 'NO_OP' if canonical(existing)==canonical(incoming) else 'CONFLICT'


def worst(levels,required,variant='A'):
    if len(required)<2:return 'UNPROVEN',None,None
    if len(set(required))!=len(required) or len(levels)!=len(required) or {x['id'] for x in levels}!=set(required):
        return 'UNPROVEN',None,None
    if any(not x['sourceFresh'] or not x['snapshotFresh'] or not x['complete'] for x in levels):return 'UNPROVEN',None,None
    if len({x['currency'] for x in levels})!=1:return 'UNAVAILABLE',None,None
    if any(number(x[k])<0 for x in levels for k in ('available','loss','buffer')):return 'REJECT',None,None
    if any(number(x['share'])*number(x['bnet'])<=number(x['far']) for x in levels):return 'REJECT',None,None
    margins=[(number(x['available'])-number(x['loss'])-number(x['buffer']),x['id']) for x in levels]
    value,idx=min(margins)
    if variant=='B':
        idx=max(levels,key=lambda x:(number(x['transitionLoss']),-x['id']))['id']
        value=next(v for v,i in margins if i==idx)
    elif variant!='A':raise ValueError('invalid policy')
    return ('POSITIVE' if value>0 else 'REJECT'),idx,value


def sequential(reserve,consumptions):
    if reserve is None or any(x is None for x in consumptions):return 'UNPROVEN',[]
    balance_now=number(reserve);rows=[]
    if balance_now<0:raise ValueError('negative reserve')
    for index,x in enumerate(consumptions,1):
        n=number(x)
        if n<0:raise ValueError('negative consumption')
        if n>balance_now:return 'REJECT',rows
        rows.append({'level':index,'ReserveBefore':balance_now,'Consumption':n,'ReserveAfter':balance_now-n})
        balance_now-=n
    return 'CONSERVATION_ONLY',rows


def geometry(far,rc,rt,rs,vmin,vmax,step):
    f,c,t,s,lo,hi,g=map(number,(far,rc,rt,rs,vmin,vmax,step))
    if min(f,c,s,lo,g)<=0 or t<0 or hi<lo:return {'status':'REJECT'}
    # This candidate explicitly uses zero-origin step grid. Broker-specific
    # offset grids need separate evidence; unsupported grid is not normalized.
    if lo/g!=(lo/g).to_integral_value():return {'status':'UNPROVEN'}
    C=(f*c/g).to_integral_value(rounding=ROUND_FLOOR)*g
    T=(f*t/g).to_integral_value(rounding=ROUND_FLOOR)*g
    S=(f*s/g).to_integral_value(rounding=ROUND_CEILING)*g
    grid=lambda v:lo<=v<=hi and v/g==(v/g).to_integral_value()
    slope=C+T-S-f
    valid=grid(f) and grid(C) and (T==0 or grid(T)) and grid(S) and slope>0
    return {'status':'GEOMETRY_ONLY' if valid else 'REJECT','Core':C,'Trend':T,'Small':S,'slope':slope}
