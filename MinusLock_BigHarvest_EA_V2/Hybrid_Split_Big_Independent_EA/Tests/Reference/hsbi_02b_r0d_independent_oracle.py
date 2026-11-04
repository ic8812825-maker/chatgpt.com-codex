"""PROPOSED R0D fixture oracle. Exact Fraction math; NO broker IO/trading.

Authorization structure derives from R0C; arithmetic/codec/snapshot are new.
No historical/production imports. Fixtures are not broker authenticity or durability.
"""
import copy
from decimal import Decimal
from fractions import Fraction
from hashlib import sha256
import json
import re

BUCKETS=('FinalReserve','PartialFar','Transition','Carry','ResidualHeld')
ID_FIELDS=('Broker','Server','Account','Symbol','Magic','Deal','Order','Position','Cycle','Plan','StateRevision','AllocationEvent','PolicyVersion','SnapshotID')
SNAPSHOT_FIELDS=('schemaVersion','id','validUntil','clockDomain','timeUnit','marketFingerprint')
LIMIT=10**65
SCALE=10**64


class Malformed(ValueError):pass
class Unsupported(ValueError):pass


def require(ok):
    if not ok:raise Malformed('invalid typed DTO')


def fields(value,required,optional=()):
    require(type(value) is dict and set(required)<=value.keys() and value.keys()<=set(required)|set(optional))


def uid(x):return type(x) is int and 1<=x<=2**64-1


def checked(x):
    if abs(x)>=LIMIT or (x*SCALE).denominator!=1:raise Unsupported('outside finite decimal fixture domain')
    return x


def number(value):
    if type(value) is Fraction:return checked(value)
    if type(value) is int:return checked(Fraction(value))
    if type(value) is Decimal:
        require(value.is_finite())
        parts=value.as_tuple();digits=list(parts.digits);exponent=parts.exponent
        if not any(digits):return Fraction(0)
        while digits[-1]==0:digits.pop();exponent+=1
        if exponent < -64 or len(digits)+exponent-1>64:raise Unsupported('outside decimal value domain')
        coefficient=int(''.join(map(str,digits)))*(-1 if parts.sign else 1)
        return checked(Fraction(coefficient*10**max(exponent,0),10**max(-exponent,0)))
    if type(value) is str:
        match=re.fullmatch(r'([+-]?)(?:(\d+)(?:\.(\d*))?|\.(\d+))(?:[eE]([+-]?\d+))?',value)
        require(match is not None)
        sign,whole,frac,leading,exp=match.groups();digits=(whole or '0')+(frac if frac is not None else leading or '')
        require(len(digits)<=256 and len(exp or '')<=4)
        exponent=int(exp or '0')-len(frac if frac is not None else leading or '')
        if abs(exponent)>256:raise Unsupported('unsupported decimal exponent')
        coefficient=int(digits)*(-1 if sign=='-' else 1)
        return checked(Fraction(coefficient*10**max(exponent,0),10**max(-exponent,0)))
    raise Malformed('float/bool/unsupported numeric type')


def unit(digits):
    if digits is None:raise Unsupported('unknown precision fact')
    require(type(digits) is int)
    if not 0<=digits<=8:raise Unsupported('unknown precision profile')
    return Fraction(1,10**digits)


def grid(value,digits):return (number(value)/unit(digits)).denominator==1


def money_shape(value):
    require(type(value) in (int,Decimal,Fraction));number(value)


def text(value):
    require(type(value) is str and bool(value))
    try:value.encode('utf-8')
    except UnicodeEncodeError as e:raise Malformed('invalid unicode') from e


def canonical(value):
    def token(x,depth=0):
        require(depth<=64)
        if x is None:return ['null']
        if type(x) is bool:return ['bool',x]
        if type(x) is int:return ['int',str(x)]
        if type(x) in (Decimal,Fraction):
            n=number(x);return ['number',str(n.numerator),str(n.denominator)]
        if type(x) is str:
            # Empty strings are encodable, but DTO schema can forbid them.
            try:x.encode('utf-8')
            except UnicodeEncodeError as e:raise Malformed('invalid unicode') from e
            return ['str',x]
        if type(x) in (list,tuple):return ['list' if type(x) is list else 'tuple',[token(v,depth+1) for v in x]]
        if type(x) is dict:
            require(all(type(k) is str for k in x))
            for k in x:token(k,depth+1)
            return ['map',[[k,token(v,depth+1)] for k,v in sorted(x.items())]]
        raise Malformed('unserializable payload')
    return json.dumps(['HSBI-R0D-TYPED-1',token(value)],ensure_ascii=False,separators=(',',':'))


def digest(value):return sha256(canonical(value).encode('utf-8')).hexdigest()


def candidate_round(raw,digits):
    n=number(raw)/unit(digits);sign=-1 if n<0 else 1
    q,r=divmod(abs(n.numerator),n.denominator)
    if 2*r>n.denominator or (2*r==n.denominator and q%2):q+=1
    return checked(sign*q*unit(digits))


def posted(raw,currency,digits,receipt,mode='BROKER_POSTED',verified_local_policy=False):
    try:
        text(currency);q=unit(digits);raw=number(raw)
        if receipt is None:return 'UNAVAILABLE',None
        fields(receipt,('currency','digits','raw','posted'))
        text(receipt['currency']);unit(receipt['digits'])
        if receipt['currency']!=currency or receipt['digits']!=digits or number(receipt['raw'])!=raw:return 'UNAVAILABLE',None
        value=number(receipt['posted'])
        if (value/q).denominator!=1:return 'UNAVAILABLE',None  # MUT:posted-grid
        if mode=='BROKER_POSTED':return 'POSTED',value
        require(type(verified_local_policy) is bool)
        if mode=='LOCAL_VERIFIED' and verified_local_policy and candidate_round(raw,digits)==value:return 'POSTED',value  # MUT:verified-local
        return 'UNAVAILABLE',None
    except Malformed:return 'REJECT',None
    except Unsupported:return 'UNAVAILABLE',None


def allocate(posted_net,shares,digits,role='BigCore'):
    n=max(Fraction(0),number(posted_net));q=unit(digits)
    require(type(shares) in (list,tuple) and len(shares)==4)
    weights=[number(v) for v in shares]
    require(all(0<=v<=1 for v in weights) and sum(weights)<=1 and grid(n,digits))
    if role not in ('BigCore','BigTrend','Small'):raise Unsupported('unknown source role')
    grants=[(n*w/q).__floor__()*q for w in weights] if role in ('BigCore','BigTrend') else [Fraction(0)]*4
    return dict(zip(BUCKETS,[checked(v) for v in grants]+[checked(n-sum(grants))]))


def identity_shape(identity):
    fields(identity,ID_FIELDS)
    for k,v in identity.items():
        if k in ('Broker','Server','Symbol'):text(v)
        elif k=='Account':require(type(v) is int and 1<=v<=2**63-1)
        elif k=='Magic':require(type(v) is int and -2**63<=v<=2**63-1 and v!=0)
        else:require(uid(v))


def source_shape(source):
    require(type(source) is tuple and len(source)==4)
    text(source[0]);text(source[1]);require(type(source[2]) is int and 1<=source[2]<=2**63-1 and uid(source[3]))


def state_shape(state):
    fields(state,('allocation','source','currency','digits','net','unallocated','grant','remaining','consumed','reserved','phase','revision'))
    text(state['allocation']);text(state['currency']);source_shape(state['source']);unit(state['digits']);require(uid(state['revision']))
    money_shape(state['net']);money_shape(state['unallocated']);require(type(state['phase']) is str)
    for k in ('grant','remaining','consumed','reserved'):
        require(type(state[k]) is dict and set(state[k])==set(BUCKETS))
        for value in state[k].values():money_shape(value)


def balance(state):
    try:
        state_shape(state);digits=state['digits']
        g,r,c,v=({b:number(state[k][b]) for b in BUCKETS} for k in ('grant','remaining','consumed','reserved'))
        n,u=number(state['net']),number(state['unallocated'])
        vals=[n,u]+[x[b] for x in (g,r,c,v) for b in BUCKETS]
        if any(x<0 or not grid(x,digits) for x in vals):return False
        if state['phase'] not in ('PREPARED','COMMITTED'):return False
        if state['phase']=='COMMITTED' and u!=0:return False
        if sum(g.values())+u!=n:return False
        for b in BUCKETS:
            if r[b]+c[b]!=g[b]:return False
            if v[b]>r[b]:return False
        return True
    except (Malformed,Unsupported):return False


def request_shape(q):
    fields(q,('identity','event','allocation','currency','digits','consumptionPolicy','bucket','purpose','amount','proofDigest'),('presentedRecord',))
    identity_shape(q['identity']);require(uid(q['event']) and uid(q['consumptionPolicy']))
    for k in ('allocation','currency','bucket','purpose','proofDigest'):text(q[k])
    unit(q['digits']);money_shape(q['amount']);canonical(q)


def snapshot_shape(s):
    fields(s,SNAPSHOT_FIELDS)
    text(s['schemaVersion'])
    if s['schemaVersion']!='HSBI-SNAPSHOT-FIXTURE-1':raise Unsupported('unknown snapshot schema')
    require(uid(s['id']) and type(s['validUntil']) is int and s['validUntil']>=0)
    if s['marketFingerprint'] is None:raise Unsupported('unknown fingerprint')
    text(s['marketFingerprint'])  # MUT:snapshot-type
    text(s['clockDomain']);text(s['timeUnit'])
    if s['clockDomain']!='FIXTURE_MONOTONIC' or s['timeUnit']!='tick':raise Unsupported('unknown snapshot clock')


def record_shape(r):
    fields(r,('identity','closingConfirmed','role','profit','swap','commission','fee','rawNet','currency','digits','receipt'))
    identity_shape(r['identity']);require(type(r['closingConfirmed']) is bool);text(r['role']);text(r['currency']);unit(r['digits'])
    for k in ('profit','swap','commission','fee','rawNet'):money_shape(r[k])
    if r['receipt'] is not None:
        fields(r['receipt'],('currency','digits','raw','posted'))
        text(r['receipt']['currency']);unit(r['receipt']['digits']);money_shape(r['receipt']['raw']);money_shape(r['receipt']['posted'])


def source_key(ids):return tuple(ids[k] for k in ('Broker','Server','Account','Deal'))
def event_key(q):return tuple(q['identity'][k] for k in ('Broker','Server','Account'))+(q['event'],)
def proof_bundle(record,allocation,expected):return dict(record=record,allocation=allocation,expected=expected)


def authorize(q,state,journal,a):
    try:return _authorize(q,state,journal,a)
    except Malformed:return 'REJECT'
    except Unsupported:return 'UNAVAILABLE'


def _authorize(q,state,journal,a):
    request_shape(q)
    if a is None or journal is None:return 'UNAVAILABLE'
    fields(a,('identity','complete','journalComplete','history','historyObservedAt','historyMaxAge','snapshot','snapshotReceipts','now','clockDomain','timeUnit','consumptionPolicy','approvedPolicies','allocations'))
    identity_shape(a['identity']);require(type(a['complete']) is bool and type(a['journalComplete']) is bool)
    require(type(journal) is dict)
    for k,v in journal.items():source_shape(k);require(type(v) is str)
    if not a['complete'] or not a['journalComplete']:return 'UNAVAILABLE'
    expected=a['identity']
    if any(q['identity'][k]!=expected[k] for k in ('Broker','Server','Account')):return 'REJECT'
    key=event_key(q)
    if key in journal:return 'NO_OP' if journal[key]==canonical(q) else 'CONFLICT'  # MUT:replay
    state_shape(state)
    if a['history'] is None:return 'UNAVAILABLE'
    require(type(a['history']) is dict and type(a['allocations']) is dict and type(a['snapshotReceipts']) is dict)
    for k,v in a['snapshotReceipts'].items():require(uid(k) and type(v) is str)
    require(uid(a['consumptionPolicy']) and type(a['approvedPolicies']) is list and all(uid(v) for v in a['approvedPolicies']))
    for k in ('now','historyObservedAt','historyMaxAge'):require(type(a[k]) is int and a[k]>=0)
    snapshot_shape(a['snapshot'])
    s=a['snapshot']
    if a['clockDomain']!=s['clockDomain'] or a['timeUnit']!=s['timeUnit']:return 'UNAVAILABLE'
    if not 0<=a['now']-a['historyObservedAt']<=a['historyMaxAge'] or a['now']>s['validUntil']:return 'UNAVAILABLE'
    if s['id']!=expected['SnapshotID']:return 'REJECT'
    receipt=a['snapshotReceipts'].get(s['id'])
    if receipt is None:return 'UNAVAILABLE'
    if canonical(s)!=receipt:return 'CONFLICT'  # MUT:snapshot-receipt
    if any(q['identity'][k]!=expected[k] for k in ID_FIELDS):return 'REJECT'
    if q['identity']['StateRevision']!=state['revision']:return 'REJECT'
    if state['revision']==2**64-1:return 'UNAVAILABLE'
    allocation=a['allocations'].get(q['allocation'])
    if allocation is None:return 'REJECT'
    fields(allocation,('allocation','source','grant','policyVersion','event'));source_shape(allocation['source'])
    require(uid(allocation['policyVersion']) and uid(allocation['event']))
    require(type(allocation['grant']) is dict and set(allocation['grant'])==set(BUCKETS))
    for v in allocation['grant'].values():money_shape(v)
    if allocation['allocation']!=q['allocation'] or allocation['event']!=expected['AllocationEvent'] or allocation['policyVersion']!=expected['PolicyVersion']:return 'CONFLICT'
    if state['allocation']!=q['allocation'] or state['source']!=allocation['source']:return 'REJECT'
    record=a['history'].get(allocation['source'])
    if record is None:return 'REJECT'
    record_shape(record)
    if not record['closingConfirmed'] or record['role'] not in ('BigCore','BigTrend'):return 'REJECT'
    if source_key(record['identity'])!=allocation['source']:return 'CONFLICT'
    if any(record['identity'][k]!=expected[k] for k in ('Broker','Server','Account','Symbol','Magic','Deal','Order','Position','Cycle')):return 'REJECT'
    raw=sum((number(record[k]) for k in ('profit','swap','commission','fee')),Fraction(0))
    if raw!=number(record['rawNet']):return 'CONFLICT'
    status,actual=posted(raw,record['currency'],record['digits'],record['receipt'])
    if status!='POSTED':return status
    if max(Fraction(0),actual)!=number(state['net']):return 'CONFLICT'
    if any(number(state['grant'][b])!=number(allocation['grant'][b]) for b in BUCKETS):return 'CONFLICT'
    if q['currency']!=state['currency'] or state['currency']!=record['currency'] or q['digits']!=state['digits'] or state['digits']!=record['digits']:return 'REJECT'
    if q['consumptionPolicy']!=a['consumptionPolicy']:return 'REJECT'
    if q['identity']['PolicyVersion'] not in a['approvedPolicies']:return 'UNAVAILABLE'
    if not balance(state) or state['phase']!='COMMITTED':return 'REJECT'
    if q['bucket']!='FinalReserve' or q['purpose']!='CatchUp':return 'REJECT'
    amount=number(q['amount'])
    if not grid(amount,state['digits']):return 'REJECT'
    if amount<=0:return 'REJECT'  # MUT:positive-amount
    if amount>number(state['remaining']['FinalReserve'])-number(state['reserved']['FinalReserve']):return 'REJECT'  # MUT:available
    if q['proofDigest']!=digest(proof_bundle(record,allocation,expected)):return 'REJECT'
    return 'ELIGIBLE_FOR_COMMIT'


def debit_for_test(state,amount):
    state['remaining']['FinalReserve']=number(state['remaining']['FinalReserve'])-amount
    state['consumed']['FinalReserve']=number(state['consumed']['FinalReserve'])+amount


def apply_for_test(q,state,journal,a):
    status=authorize(q,state,journal,a)
    s,j,aa=copy.deepcopy(state),copy.deepcopy(journal),copy.deepcopy(a)
    if status!='ELIGIBLE_FOR_COMMIT':return status,s,j,aa
    payload=canonical(q);amount=number(q['amount'])
    debit_for_test(s,amount)
    s['revision']+=1;aa['identity']['StateRevision']=s['revision']
    if not balance(s):return 'UNAVAILABLE',copy.deepcopy(state),copy.deepcopy(journal),copy.deepcopy(a)  # MUT:post-state
    j[event_key(q)]=payload
    return 'COMMITTED_IN_MEMORY',s,j,aa


def classify_grant(existing,incoming):
    if existing['allocation']!=incoming['allocation']:return 'NEW'
    return 'NO_OP' if canonical(existing)==canonical(incoming) else 'CONFLICT'


def worst(levels,required,variant='A'):
    try:return _worst(levels,required,variant)
    except Malformed:return 'REJECT',None,None
    except Unsupported:return 'UNAVAILABLE',None,None


def _worst(levels,required,variant):
    require(type(levels) is list and type(required) in (list,tuple) and all(uid(i) for i in required))
    if len(required)<2 or len(set(required))!=len(required) or len(levels)!=len(required):return 'UNPROVEN',None,None
    for row in levels:
        fields(row,('id','available','loss','buffer','transitionLoss','currency','digits','sourceFresh','snapshotFresh','complete','share','bnet','far'))
        require(uid(row['id']));text(row['currency']);unit(row['digits'])
        for k in ('sourceFresh','snapshotFresh','complete'):require(type(row[k]) is bool)
    if {r['id'] for r in levels}!=set(required):return 'UNPROVEN',None,None
    if any(not r[k] for r in levels for k in ('sourceFresh','snapshotFresh','complete')):return 'UNPROVEN',None,None
    if len({(r['currency'],r['digits']) for r in levels})!=1:return 'UNAVAILABLE',None,None
    margins=[]
    for r in levels:
        text(r['currency']);unit(r['digits'])
        av,loss,buf,share,bnet,far=(number(r[k]) for k in ('available','loss','buffer','share','bnet','far'))
        if min(av,loss,buf,share,bnet,far)<0 or not grid(av,r['digits']) or not 0<=share<=1:return 'REJECT',None,None
        if share*bnet<=far:return 'REJECT',None,None
        margins.append((checked(av-loss-buf),r['id']))  # MUT:margin-exact
    value,index=min(margins)
    if variant=='B':
        index=max(levels,key=lambda r:(number(r['transitionLoss']),-r['id']))['id'];value=next(v for v,i in margins if i==index)
    elif variant!='A':raise Malformed('unknown aggregation variant')
    return (('ALL_LEVEL_POSITIVE' if variant=='A' else 'SINGLE_LEVEL_POSITIVE') if value>0 else 'REJECT'),index,value


def sequential(reserve,consumptions,currency='USD',digits=2):
    result=dict(status='UNPROVEN',initial=None,remaining=None,appliedCount=0,rejectedIndex=None,trace=[],currency=currency,digits=digits)
    if reserve is None or consumptions is None:return result
    try:
        text(currency);unit(digits);require(type(consumptions) in (list,tuple))
        current=number(reserve);require(current>=0 and grid(current,digits));result.update(initial=current,remaining=current)
        for index,x in enumerate(consumptions,1):
            result['rejectedIndex']=index
            if x is None:result.update(status='UNPROVEN',rejectedIndex=index);return result
            amount=number(x)
            if amount<=0 or not grid(amount,digits) or amount>current:result.update(status='REJECT',rejectedIndex=index);return result
            after=checked(current-amount)  # MUT:sequential-exact
            result['trace'].append(dict(level=index,ReserveBefore=current,Consumption=amount,ReserveAfter=after))
            current=after;result.update(remaining=current,appliedCount=index,rejectedIndex=None)
        result['status']='CONSERVATION_ONLY';return result
    except Malformed:result['status']='REJECT';return result
    except Unsupported:result['status']='UNAVAILABLE';return result


def geometry(far,rc,rt,rs,vmin,vmax,step):
    try:
        f,c,t,s,lo,hi,g=map(number,(far,rc,rt,rs,vmin,vmax,step))
        if min(f,c,s,lo,g)<=0 or t<0 or hi<lo:return {'status':'REJECT'}
        if (lo/g).denominator!=1:return {'status':'UNPROVEN'}
        core=checked((f*c/g).__floor__()*g);trend=checked((f*t/g).__floor__()*g);small=checked((f*s/g).__ceil__()*g)
        ongrid=lambda v:lo<=v<=hi and (v/g).denominator==1
        slope=checked(core+trend-small-f)
        valid=ongrid(f) and ongrid(core) and (trend==0 or ongrid(trend)) and ongrid(small) and slope>0
        return dict(status='GEOMETRY_ONLY' if valid else 'REJECT',Core=core,Trend=trend,Small=small,slope=slope)
    except Malformed:return {'status':'REJECT'}
    except Unsupported:return {'status':'UNAVAILABLE'}
