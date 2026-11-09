"""R0E PROPOSED contracts, fixture-only. No broker IO, durable backend or trading.

Reuse frozen R0D exact arithmetic, never use its outcomes as expected test values.
All authority/history completeness inputs are independent FIXTURE assumptions.
"""
import copy
from fractions import Fraction
import hsbi_02b_r0d_independent_oracle as exact

BUCKETS=exact.BUCKETS
number=exact.number
canonical=exact.canonical
digest=exact.digest
Malformed=exact.Malformed
Unsupported=exact.Unsupported
require=exact.require
IDENTITY=('Broker','Server','Account','Symbol','Magic','Cycle','Position','Deal','Order','Event','Role','Plan','PolicyVersion','Revision','Snapshot')
SOURCE_IDENTITY=('Broker','Server','Account','Symbol','Magic','Cycle','Position','Deal','Order','Event','Role')


def source_key(record):
    i=record['identity'];return (i['Broker'],i['Server'],i['Account'],i['Deal'])


def key(value):return canonical(value)
def allocation_key(source,allocation):return key(tuple(source[:3])+(allocation,))
def event_key(source,event):return key(tuple(source[:3])+(event,))


def new_registry():
    return dict(schema='HSBI-R0E-FREE-1',revision=1,sources={},allocations={},events={},journalComplete=True)


def identity_shape(identity):
    exact.fields(identity,IDENTITY)
    for k,v in identity.items():
        if k in ('Broker','Server','Symbol','Role'):exact.text(v)
        elif k=='Account':require(type(v) is int and 1<=v<=2**63-1)
        elif k=='Magic':require(type(v) is int and -2**63<=v<=2**63-1 and v!=0)
        else:require(exact.uid(v))


def economic_record(history,source,complete=True):
    if history is None or not complete:raise Unsupported('independent fixture history unavailable/incomplete')
    require(type(history) is dict)
    r=history.get(key(source))
    if r is None:raise Malformed('confirmed source absent')
    exact.fields(r,('identity','kind','entry','currency','digits','profit','swap','commission','fee','rawNet','postedNet'))
    identity_shape(r['identity']);exact.text(r['currency']);exact.unit(r['digits'])
    require(source_key(r)==tuple(source))
    if r['kind']!='ReconciledEconomicNet':raise Malformed('projected/raw record is not reconciled authority')
    require(r['entry']=='CLOSE')
    raw=sum((number(r[k]) for k in ('profit','swap','commission','fee')),Fraction(0))
    require(raw==number(r['rawNet']) and exact.grid(r['postedNet'],r['digits']))
    return r


def balance(grant,consumed,reserved,remaining_free,reservations=None):
    try:
        g,c,v,f=map(number,(grant,consumed,reserved,remaining_free))
        if min(g,c,v,f)<0 or g!=c+v+f:return False
        if reservations is not None:
            if type(reservations) is not dict or any(type(k) is not str or not k for k in reservations):return False
            if sum((number(x) for x in reservations.values()),Fraction(0))!=v or any(number(x)<0 for x in reservations.values()):return False
        return True
    except (Malformed,Unsupported):return False


def legacy_view(grant,consumed,reserved,remaining_gross):
    g,c,v,r=map(number,(grant,consumed,reserved,remaining_gross))
    require(min(g,c,v,r)>=0 and g==c+r and v<=r)
    return dict(OriginalGrant=g,Consumed=c,Reserved=v,RemainingGross=r,RemainingFree=r-v,Available=r-v,SpendAuthorization='UNAVAILABLE_WITHOUT_OWNER_PROVENANCE')


def _event(state,source,event,payload):
    require(state['schema']=='HSBI-R0E-FREE-1' and type(state['journalComplete']) is bool and exact.uid(event))
    if not state['journalComplete']:raise Unsupported('no complete model journal')
    ek=event_key(source,event)
    prior=state['events'].get(ek)
    if prior is not None:
        require(prior['digest']==digest(prior['payload']))
        return ('NO_OP' if canonical(prior['payload'])==canonical(payload) else 'CONFLICT'),ek
    require(exact.uid(state['revision']))
    if state['revision']==2**64-1:raise Unsupported('revision exhausted')
    return 'ELIGIBLE_FOR_COMMIT',ek


def _fund(state,history,source,allocation,event,grants,commit,complete):
    require(type(source) is tuple and len(source)==4);exact.source_shape(source);exact.text(allocation)
    require(type(grants) is dict and set(grants)==set(BUCKETS) and type(commit) is bool)
    values={b:number(grants[b]) for b in BUCKETS};require(all(v>=0 for v in values.values()))
    payload=dict(kind='FUND',source=source,allocation=allocation,event=event,grants=values,commit=commit)
    r=economic_record(history,source,complete)
    status,ek=_event(state,source,event,payload)
    if status!='ELIGIBLE_FOR_COMMIT':return status,copy.deepcopy(state)
    net=max(Fraction(0),number(r['postedNet']))
    require(all(exact.grid(v,r['digits']) for v in values.values()))
    role=r['identity']['Role']
    require(role in ('BigCore','BigTrend','Small'))
    if role=='Small' and any(values[b]!=0 for b in BUCKETS if b!='ResidualHeld'):return 'REJECT',copy.deepcopy(state)
    sk=key(source);ak=allocation_key(source,allocation);old=state['sources'].get(sk)
    if old and old['recordDigest']!=digest(r):return 'CONFLICT',copy.deepcopy(state)
    if ak in state['allocations']:return 'CONFLICT',copy.deepcopy(state)
    used=number(old['granted']) if old else Fraction(0)
    total=used+sum(values.values())
    if total>net:return 'REJECT',copy.deepcopy(state)  # MUT:source-cap
    if commit and total!=net:return 'REJECT',copy.deepcopy(state)
    if old and old['phase']=='COMMITTED':return 'CONFLICT',copy.deepcopy(state)
    s=copy.deepcopy(state)
    s['sources'][sk]=dict(source=source,recordDigest=digest(r),granted=total,net=net,phase='COMMITTED' if commit else 'PREPARED',unallocated=net-total)
    s['allocations'][ak]=dict(source=source,allocation=allocation,allocationEvent=event,policyVersion=r['identity']['PolicyVersion'],buckets={b:dict(OriginalGrant=v,Consumed=Fraction(0),Reserved=Fraction(0),RemainingFree=v,Reservations={}) for b,v in values.items()})
    s['events'][ek]=dict(sequence=s['revision']+1,payload=copy.deepcopy(payload),digest=digest(payload));s['revision']+=1
    return 'COMMITTED_IN_MEMORY',s


def fund(state,history,source,allocation,event,grants,commit=True,complete=True):
    try:return _fund(state,history,source,allocation,event,grants,commit,complete)
    except Malformed:return 'REJECT',copy.deepcopy(state)
    except Unsupported:return 'UNAVAILABLE',copy.deepcopy(state)


def funding_status(history,account,complete=True):
    if history is None or not complete:return 'UNAVAILABLE'
    for r in history.values():
        if tuple(source_key(r)[:3])==tuple(account) and number(r['postedNet'])<0:return 'UNPROVEN'
    return 'MODEL_NO_UNATTRIBUTED_DEBIT'


def _operate(state,history,source,allocation,event,kind,bucket,amount,intent,purpose,revision,complete):
    require(type(source) is tuple);exact.source_shape(source);require(kind in ('RESERVE','RELEASE','CONSUME_FREE','CONSUME_RESERVED'))
    exact.text(intent);exact.text(purpose);require(bucket in BUCKETS and exact.uid(revision))
    n=number(amount);require(n>0)
    payload=dict(kind=kind,source=source,allocation=allocation,event=event,bucket=bucket,amount=n,intent=intent,purpose=purpose,revision=revision)
    r=economic_record(history,source,complete)
    status,ek=_event(state,source,event,payload)
    if status!='ELIGIBLE_FOR_COMMIT':return status,copy.deepcopy(state)
    require(revision==state['revision'])
    sk=key(source);ak=allocation_key(source,allocation)
    require(sk in state['sources'] and ak in state['allocations'])
    if state['sources'][sk]['recordDigest']!=digest(r):return 'CONFLICT',copy.deepcopy(state)
    require(state['sources'][sk]['phase']=='COMMITTED')
    require(state['allocations'][ak]['source']==source and exact.grid(n,r['digits']))
    if bucket=='ResidualHeld':return 'REJECT',copy.deepcopy(state)
    allowed={'FinalReserve':('CatchUp','FinalClose'),'PartialFar':('PartialFar',),'Transition':('TransitionLoss',),'Carry':()}
    require(purpose in allowed[bucket])
    if kind in ('RESERVE','CONSUME_FREE','CONSUME_RESERVED') and funding_status(history,source[:3],complete)!='MODEL_NO_UNATTRIBUTED_DEBIT':raise Unsupported('global debit attribution unresolved')
    row=state['allocations'][ak]['buckets'][bucket]
    require(balance(row['OriginalGrant'],row['Consumed'],row['Reserved'],row['RemainingFree'],row['Reservations']))
    if kind in ('RESERVE','CONSUME_FREE') and n>number(row['RemainingFree']):return 'REJECT',copy.deepcopy(state)
    if kind in ('RELEASE','CONSUME_RESERVED') and n>number(row['Reservations'].get(intent,0)):return 'REJECT',copy.deepcopy(state)  # MUT:reservation-owner
    s=copy.deepcopy(state);b=s['allocations'][ak]['buckets'][bucket]
    if kind=='RESERVE':b['Reserved']+=n;b['RemainingFree']-=n;b['Reservations'][intent]=number(b['Reservations'].get(intent,0))+n
    elif kind=='RELEASE':b['Reserved']-=n;b['RemainingFree']+=n;b['Reservations'][intent]-=n
    elif kind=='CONSUME_RESERVED':b['Reserved']-=n;b['Consumed']+=n;b['Reservations'][intent]-=n
    else:b['RemainingFree']-=n;b['Consumed']+=n
    if not balance(b['OriginalGrant'],b['Consumed'],b['Reserved'],b['RemainingFree'],b['Reservations']):return 'UNAVAILABLE',copy.deepcopy(state)
    s['events'][ek]=dict(sequence=s['revision']+1,payload=copy.deepcopy(payload),digest=digest(payload));s['revision']+=1
    return 'COMMITTED_IN_MEMORY',s


def operate(state,history,source,allocation,event,kind,bucket,amount,intent='I1',purpose='CatchUp',revision=None,complete=True):
    try:return _operate(state,history,source,allocation,event,kind,bucket,amount,intent,purpose,state['revision'] if revision is None else revision,complete)
    except Malformed:return 'REJECT',copy.deepcopy(state)
    except Unsupported:return 'UNAVAILABLE',copy.deepcopy(state)


def reserve_available(state,history,account,complete=True):
    if history is None or not complete:return 'UNAVAILABLE',None
    if funding_status(history,account,complete)=='UNPROVEN':return 'UNPROVEN',None
    total=Fraction(0);money_unit=None
    try:
        for a in state['allocations'].values():
            if tuple(a['source'][:3])!=tuple(account):continue
            r=economic_record(history,a['source'],complete);src=state['sources'][key(a['source'])]
            unit=(r['currency'],r['digits'])
            if money_unit is not None and unit!=money_unit:return 'UNAVAILABLE',None
            money_unit=unit
            if src['recordDigest']!=digest(r):return 'UNAVAILABLE',None
            if src['phase']=='COMMITTED' and r['identity']['Role'] in ('BigCore','BigTrend'):
                b=a['buckets']['FinalReserve'];require(balance(b['OriginalGrant'],b['Consumed'],b['Reserved'],b['RemainingFree'],b['Reservations']));total+=number(b['RemainingFree'])
        return 'KNOWN_MODEL_AVAILABLE',exact.checked(total)
    except (Malformed,Unsupported):return 'UNAVAILABLE',None


def transition_status(fills,independent_history,planned_volume,cap,complete=True):
    try:return _transition_status(fills,independent_history,planned_volume,cap,complete)
    except Malformed:return 'CONFLICT',None
    except Unsupported:return 'UNAVAILABLE',None


def _transition_status(fills,independent_history,planned_volume,cap,complete=True):
    if independent_history is None or not complete:return 'UNAVAILABLE',None
    require(type(independent_history) is dict and type(fills) in (list,tuple) and number(planned_volume)>0 and number(cap)>=0)
    unique={};volume=Fraction(0);net=Fraction(0)
    for fill in fills:
        try:
            exact.fields(fill,('source','volume','net'));exact.source_shape(fill['source']);require(number(fill['volume'])>0);number(fill['net'])
        except (Malformed,Unsupported):return 'CONFLICT',None
        k=fill['source']
        if k in unique:
            if canonical(unique[k])!=canonical(fill):return 'CONFLICT',None
            continue
        if independent_history.get(k)!=fill:return 'CONFLICT',None
        unique[k]=fill;volume=exact.checked(volume+number(fill['volume']));net=exact.checked(net+number(fill['net']))
    if volume>number(planned_volume):return 'CONFLICT',None
    loss=max(Fraction(0),-net)
    if loss>number(cap):return 'OVER_CAP',loss
    return ('CONFIRMED' if volume==number(planned_volume) else 'PENDING'),loss


def verify_identity(presented,history,source,context,allocation,complete=True):
    try:
        r=economic_record(history,source,complete)
        if allocation is None or context is None:return 'UNAVAILABLE'
        exact.fields(allocation,('source','PolicyVersion','allocationEvent'));exact.fields(context,('Plan','Revision','Snapshot','fresh'))
        require(allocation['source']==source and exact.uid(allocation['PolicyVersion']) and exact.uid(allocation['allocationEvent']))
        require(all(exact.uid(context[k]) for k in ('Plan','Revision','Snapshot')) and type(context['fresh']) is bool)
        if not context['fresh']:return 'UNAVAILABLE'
        expected={k:r['identity'][k] for k in SOURCE_IDENTITY}
        expected.update({k:context[k] for k in ('Plan','Revision','Snapshot')});expected['PolicyVersion']=allocation['PolicyVersion']
        require(set(presented)==set(expected))
        return 'PASS' if all(type(presented[k]) is type(expected[k]) and presented[k]==expected[k] for k in expected) else 'REJECT'
    except Malformed:return 'REJECT'
    except Unsupported:return 'UNAVAILABLE'


def far_loss(close_now_net,baseline=None,current_basis=None):
    absolute=max(Fraction(0),-number(close_now_net))
    if baseline is None or baseline['basis']!=current_basis or not baseline['fresh']:return dict(absolute=absolute,incremental=None,incrementalStatus='UNAVAILABLE',workingMetric='ABSOLUTE_PROPOSED')
    return dict(absolute=absolute,incremental=max(Fraction(0),absolute-number(baseline['absolute'])),incrementalStatus='DIAGNOSTIC_ONLY',workingMetric='ABSOLUTE_PROPOSED')


def costs_status(rows,basis_registry):
    seen=set()
    for row in rows:
        known=basis_registry.get(row['CostID'])
        if known is None:return 'UNPROVEN'
        if (row['RiskBasis'],row['Window'])!=(known['RiskBasis'],known['Window']):return 'CONFLICT'
        if row['AlreadyIncluded']!=known['AlreadyIncluded']:return 'CONFLICT'
        if known['OverlapKnown'] is not True:return 'UNPROVEN'
        if row['AlreadyIncluded'] and row['AdditionalDeduction']:return 'CONFLICT'
        coverage=(row['RiskBasis'],row['Window'])
        if coverage in seen:return 'CONFLICT'
        seen.add(coverage)
    return 'PASS'


def snapshot(state):return dict(schema='HSBI-R0E-SNAPSHOT-1',payload=copy.deepcopy(state),checksum=digest(state))


def recover(latest,previous,journal,history,complete=True):
    if journal is None or not complete or history is None:return dict(status='UNAVAILABLE',state=None,fallbackUsed=False)
    chosen=None;fallback=False
    for index,candidate in enumerate((latest,previous)):
        if candidate and candidate.get('schema')=='HSBI-R0E-SNAPSHOT-1' and candidate.get('checksum')==digest(candidate['payload']):chosen=candidate['payload'];fallback=index==1;break
    if chosen is None:return dict(status='UNAVAILABLE',state=None,fallbackUsed=False)
    if canonical(chosen['events'])!=canonical(journal) or chosen['revision']!=1+len(journal):return dict(status='UNAVAILABLE',state=None,fallbackUsed=fallback)
    rebuilt=new_registry()
    try:
        for ek,entry in sorted(journal.items(),key=lambda row:row[1]['sequence']):
            payload=entry['payload'];require(entry['digest']==digest(payload) and entry['sequence']==rebuilt['revision']+1)
            require(ek==event_key(payload['source'],payload['event']))
            if payload['kind']=='FUND':
                status,rebuilt=fund(rebuilt,history,payload['source'],payload['allocation'],payload['event'],payload['grants'],payload['commit'],complete)
            else:
                status,rebuilt=operate(rebuilt,history,payload['source'],payload['allocation'],payload['event'],payload['kind'],payload['bucket'],payload['amount'],payload['intent'],payload['purpose'],payload['revision'],complete)
            if status!='COMMITTED_IN_MEMORY':return dict(status='UNAVAILABLE',state=None,fallbackUsed=fallback)
        if canonical(rebuilt)!=canonical(chosen):return dict(status='CONFLICT',state=None,fallbackUsed=fallback)
    except (Malformed,Unsupported):return dict(status='UNAVAILABLE',state=None,fallbackUsed=fallback)

    return dict(status='RECONCILED_MODEL_ONLY',state=copy.deepcopy(chosen),fallbackUsed=fallback)


def checked_add(a,b,minimum=-(2**63),maximum=2**63-1):
    require(type(a) is int and type(b) is int)
    if not minimum<=a<=maximum or not minimum<=b<=maximum:raise Unsupported('operand outside int64 domain')
    if b>0 and a>maximum-b or b<0 and a<minimum-b:raise Unsupported('int64 addition overflow')
    result=a+b
    if not minimum<=result<=maximum:raise Unsupported('outside int64 domain')
    return result


def checked_mul(a,b,minimum=-(2**63),maximum=2**63-1):
    require(type(a) is int and type(b) is int)
    if not minimum<=a<=maximum or not minimum<=b<=maximum:raise Unsupported('operand outside int64 domain')
    def trunc(n,d):
        q=n//d
        return q+1 if (n<0)!=(d<0) and n%d else q
    if a>0:
        if b>0 and a>trunc(maximum,b) or b<0 and b<trunc(minimum,a):raise Unsupported('int64 multiply overflow')
    elif a<0:
        if b>0 and a<trunc(minimum,b) or b<0 and b<trunc(maximum,a):raise Unsupported('int64 multiply overflow')
    return a*b


def close_side(direction):
    require(direction in ('BUY','SELL'))
    return 'Bid' if direction=='BUY' else 'Ask'


def assess_levels(levels,required,variant='A'):
    """complete is independent fixture attestation of all nonmonetary gates, not runtime proof."""
    try:
        for row in levels:
            if row.get('transitionLoss') is None:return 'UNAVAILABLE',None,None
            require(number(row['transitionLoss'])>=0)
        return exact.worst(levels,required,variant)
    except Malformed:return 'REJECT',None,None
    except Unsupported:return 'UNAVAILABLE',None,None
