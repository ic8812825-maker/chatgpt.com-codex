"""C2 PROPOSED contracts; copied from frozen C1; derived from frozen R0E, fixture-only. No broker IO, durable backend or trading.

Reuse frozen R0D exact arithmetic, never use its outcomes as expected test values.
All authority/history completeness inputs are independent FIXTURE assumptions.
"""
import copy
import hsbi_02b_r0e_c2_evidence as evidence
import hsbi_02b_r0e_c2_schemas as dto
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
    dto.validate({'map':'EconomicRecord'},history)
    dto.validate('source',source)
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
    old_source=state['sources'].get(key(source))
    if old_source and old_source['recordDigest']!=digest(r):return 'CONFLICT',copy.deepcopy(state)  # C1: immutable authority before replay
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


def _apply_registry_delta(state,history,source,allocation,event,kind,bucket,amount,intent,purpose,revision,complete):
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


def _operate_for_registry_replay(state,history,source,allocation,event,kind,bucket,amount,intent='I1',purpose='CatchUp',revision=None,complete=True):
    try:return _apply_registry_delta(state,history,source,allocation,event,kind,bucket,amount,intent,purpose,state['revision'] if revision is None else revision,complete)
    except Malformed:return 'REJECT',copy.deepcopy(state)
    except Unsupported:return 'UNAVAILABLE',copy.deepcopy(state)


def _arithmetic_reserve_balance(state,history,account,complete=True):
    if history is None or not complete or not state['journalComplete']:return 'UNAVAILABLE',None
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


def _selected_fill_aggregate(fills,independent_history,planned_volume,cap,complete=True):
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


def _verify_source_context(presented,history,source,context,allocation,complete=True):
    try:
        r=economic_record(history,source,complete)
        if allocation is None or context is None:return 'UNAVAILABLE'
        exact.fields(allocation,('source','PolicyVersion','allocationEvent'));exact.fields(context,('Plan','Revision','Snapshot','fresh'))
        require(allocation['source']==source and exact.uid(allocation['PolicyVersion']) and exact.uid(allocation['allocationEvent']))
        require(all(exact.uid(context[k]) for k in ('Plan','Revision','Snapshot')) and type(context['fresh']) is bool)
        if not context['fresh']:return 'UNAVAILABLE'
        expected={k:r['identity'][k] for k in SOURCE_IDENTITY}
        expected.update({k:context[k] for k in ('Plan','Revision','Snapshot')});expected['PolicyVersion']=allocation['PolicyVersion']
        require(type(presented) is dict and set(presented)==set(expected))
        return 'PASS' if all(type(presented[k]) is type(expected[k]) and presented[k]==expected[k] for k in expected) else 'REJECT'
    except Malformed:return 'REJECT'
    except Unsupported:return 'UNAVAILABLE'


def far_loss(close_now_net,baseline=None,current_basis=None):
    absolute=max(Fraction(0),-number(close_now_net))
    if baseline is None or baseline['basis']!=current_basis or not baseline['fresh']:return dict(absolute=absolute,incremental=None,incrementalStatus='UNAVAILABLE',workingMetric='ABSOLUTE_PROPOSED')
    return dict(absolute=absolute,incremental=max(Fraction(0),absolute-number(baseline['absolute'])),incrementalStatus='DIAGNOSTIC_ONLY',workingMetric='ABSOLUTE_PROPOSED')


def _cost_row_checks(rows,basis_registry):
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
                status,rebuilt=_operate_for_registry_replay(rebuilt,history,payload['source'],payload['allocation'],payload['event'],payload['kind'],payload['bucket'],payload['amount'],payload['intent'],payload['purpose'],payload['revision'],complete)
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

# C1 public composed fixture API. The private core above is mathematical only.
REQUEST_FIELDS=('schema','source','allocation','allocationEvent','consumptionEvent','identity','PrincipalAmount','bucket','purpose','intent','revision','BatchID','CostSetID','costClaims')
ALLOCATION_FIELDS=('AllocationID','source','allocationEvent','PolicyVersion','currency','digits','grants')
CONTEXT_FIELDS=('Plan','Revision','Snapshot','ConsumptionEventID','AllocationID','BatchID','CostSetID','PrincipalAmount','bucket','purpose','intent','fresh')
BATCH_FIELDS=('schema','BatchID','Broker','Server','Account','Symbol','Cycle','Order','Position','currency','digits','expectedVolume','RequiredDeals','historyComplete','NettingPolicy','cap')
FILL_FIELDS=('source','BatchID','Symbol','Cycle','Order','Position','currency','digits','volume','net')
COST_FIELDS=('CostID','Applicability','Amount','AmountBasis','currency','RiskBasis','Window','AlreadyIncluded','AdditionalDeduction','PolicyVersion')


def _answer(status,**kw):return dict(status=status,**kw)


def request_shape(q):
    exact.fields(q,REQUEST_FIELDS)
    if q['schema']!='HSBI-C1-REQUEST-1':raise Unsupported('unknown C1 request schema')
    require(type(q['source']) is tuple);exact.source_shape(q['source'])
    for k in ('allocation','bucket','purpose','intent','BatchID','CostSetID'):exact.text(q[k])
    require(all(exact.uid(q[k]) for k in ('allocationEvent','consumptionEvent','revision')))
    require(type(q['identity']) is dict and type(q['costClaims']) is list)
    require(number(q['PrincipalAmount'])>0)
    canonical(q)


def _allocation_shape(a):
    exact.fields(a,ALLOCATION_FIELDS);exact.text(a['AllocationID']);exact.source_shape(a['source'])
    require(exact.uid(a['allocationEvent']) and exact.uid(a['PolicyVersion']))
    exact.text(a['currency']);exact.unit(a['digits']);require(type(a['grants']) is dict and set(a['grants'])==set(BUCKETS))
    require(all(number(v)>=0 and exact.grid(v,a['digits']) for v in a['grants'].values()))


def verify_allocation_identity(presented,history,source,context,allocation):
    try:
        dto.validate("Identity",presented)
        dto.validate("source",source)
        if history is not None:dto.validate({"map":"EconomicRecord"},history)
        if context is not None:dto.validate("EvaluationContext",context)
        if allocation is not None:dto.validate("Allocation",allocation)
        r=economic_record(history,source)
        if context is None or allocation is None:return 'UNAVAILABLE'
        _allocation_shape(allocation);exact.fields(context,CONTEXT_FIELDS)
        require(type(presented) is dict and allocation['source']==source)
        require(all(exact.uid(context[k]) for k in ('Plan','Revision','Snapshot','ConsumptionEventID')) and type(context['fresh']) is bool)
        for k in ('AllocationID','BatchID','CostSetID','bucket','purpose','intent'):exact.text(context[k])
        require(number(context['PrincipalAmount'])>0)
        if not context['fresh']:return 'UNAVAILABLE'
        require(context['AllocationID']==allocation['AllocationID'])
        expected={k:r['identity'][k] for k in SOURCE_IDENTITY if k!='Event'}
        expected.update(EconomicEventID=r['identity']['Event'],AllocationEventID=allocation['allocationEvent'],ConsumptionEventID=context['ConsumptionEventID'],AllocationID=allocation['AllocationID'],PolicyVersion=allocation['PolicyVersion'])
        expected.update({k:context[k] for k in ('Plan','Revision','Snapshot')})
        require(set(presented)==set(expected))
        return 'PASS' if all(type(presented[k]) is type(expected[k]) and presented[k]==expected[k] for k in expected) else 'REJECT'  # GUARD:C1-IDENTITY
    except Malformed:return 'REJECT'
    except Unsupported:return 'UNAVAILABLE'


def assess_batch(refs,history,expected):
    try:
        dto.validate({"list":"source"},refs)
        if history is not None:dto.validate({"map":"FillRecord"},history)
        if expected is not None:dto.validate("BatchExpectedContext",expected)
        if history is None or expected is None:return _answer('UNAVAILABLE')
        exact.fields(expected,BATCH_FIELDS);require(expected['schema']=='HSBI-C1-BATCH-1')
        require(type(history) is dict and type(refs) is list and type(expected['RequiredDeals']) is tuple)
        for k in ('BatchID','Broker','Server','Symbol','currency'):exact.text(expected[k])
        exact.unit(expected['digits']);require(type(expected['Account']) is int and 1<=expected['Account']<2**63)
        require(all(exact.uid(expected[k]) for k in ('Cycle','Order','Position')) and type(expected['historyComplete']) is bool)
        if not expected['historyComplete'] or expected['NettingPolicy']!='PROPOSED_SIGNED_BATCH_NET_V1':return _answer('UNAVAILABLE')
        required=expected['RequiredDeals'];require(required and all(type(k) is tuple for k in required));[exact.source_shape(k) for k in required]
        require(len(set(required))==len(required))
        for k in refs:require(type(k) is tuple);exact.source_shape(k)
        require(set(refs)<=set(required))
        unique=set();volume=Fraction(0);net=Fraction(0)
        for k in refs:
            if k in unique:continue
            fill=history.get(key(k))
            if fill is None:return _answer('UNAVAILABLE')
            exact.fields(fill,FILL_FIELDS);require(type(fill['source']) is tuple);exact.source_shape(fill['source']);require(fill['source']==k)
            require(k[:3]==(expected['Broker'],expected['Server'],expected['Account']))  # GUARD:C1-BATCH-NAMESPACE
            require(all(type(fill[f]) is type(expected[f]) and fill[f]==expected[f] for f in ('BatchID','Symbol','Cycle','Order','Position','currency','digits')))  # GUARD:C1-BATCH-LINEAGE
            require(number(fill['volume'])>0 and exact.grid(fill['net'],expected['digits']))
            volume=exact.checked(volume+number(fill['volume']));net=exact.checked(net+number(fill['net']));unique.add(k)
        planned=number(expected['expectedVolume']);cap=number(expected['cap']);require(planned>0 and cap>=0)
        require(volume<=planned);loss=max(Fraction(0),-net)
        if loss>cap:return _answer('OVER_CAP',loss=loss,volume=volume)
        if unique!=set(required) or volume!=planned:return _answer('PENDING',loss=loss,volume=volume)  # GUARD:C1-BATCH-COMPLETE
        return _answer('CONFIRMED',loss=loss,volume=volume,scope='BATCH_MEMBERSHIP_VERIFIED_FIXTURE')
    except Malformed:return _answer('CONFLICT')
    except Unsupported:return _answer('UNAVAILABLE')


def cost_coverage(rows,expected):
    try:
        dto.validate({"list":"CostClaim"},rows)
        if expected is not None:dto.validate("CostSet",expected)  # GUARD:C2-COST-SHAPE
        if expected is None:return _answer('UNAVAILABLE')
        exact.fields(expected,('schema','Complete','currency','digits','PolicyVersion','Authority','items'))
        require(expected['schema']=='HSBI-C1-COSTSET-1' and type(expected['Complete']) is bool and type(expected['items']) is list and type(rows) is list)
        exact.text(expected['Authority']);exact.text(expected['currency']);exact.unit(expected['digits']);require(exact.uid(expected['PolicyVersion']))
        if not expected['Complete']:return _answer('UNAVAILABLE')
        facts={}
        for fact in expected['items']:
            exact.fields(fact,tuple(k for k in COST_FIELDS if k!='AdditionalDeduction')+('OverlapKnown',))
            exact.text(fact['CostID']);require(fact['CostID'] not in facts)
            require(fact['Applicability'] in ('REQUIRED','NOT_APPLICABLE','KNOWN_ZERO','UNKNOWN'))
            if fact['Applicability']=='UNKNOWN' or fact['OverlapKnown'] is not True:return _answer('UNAVAILABLE')
            require(type(fact['AlreadyIncluded']) is bool and fact['currency']==expected['currency'] and fact['PolicyVersion']==expected['PolicyVersion'])
            for f in ('RiskBasis','Window'):exact.text(fact[f])
            require(fact['AmountBasis'] in ('SIGNED_COMPONENT','NONNEGATIVE_RISK'))
            n=number(fact['Amount']);require(exact.grid(n,expected['digits']))
            if fact['AmountBasis']=='NONNEGATIVE_RISK':require(n>=0)
            if fact['Applicability']=='KNOWN_ZERO':require(n==0)
            if fact['Applicability']=='NOT_APPLICABLE':require(n==0)
            if fact['Applicability']=='REQUIRED':require(n!=0)
            facts[fact['CostID']]=fact
        ids=[];total=Fraction(0);coverage=set()
        for row in rows:
            exact.fields(row,COST_FIELDS);exact.text(row['CostID']);ids.append(row['CostID'])
            require(type(row['AlreadyIncluded']) is bool and type(row['AdditionalDeduction']) is bool)
        require(len(set(ids))==len(ids) and set(ids)==set(facts))  # GUARD:C1-COST-INVENTORY
        for row in rows:
            fact=facts[row['CostID']]
            require(all(type(row[f]) is type(fact[f]) and row[f]==fact[f] for f in COST_FIELDS if f!='AdditionalDeduction'))
            required=fact['Applicability']=='REQUIRED'
            needed=required and not fact['AlreadyIncluded']
            if needed and fact['AmountBasis']!='NONNEGATIVE_RISK':return _answer('UNAVAILABLE')
            require(row['AdditionalDeduction']==needed)  # GUARD:C1-COST-ONCE
            if required:
                basis=(fact['RiskBasis'],fact['Window'],fact['currency']);require(basis not in coverage);coverage.add(basis)
            if needed:total=exact.checked(total+number(fact['Amount']))
        return _answer('COVERED',AdditionalRisk=total,scope='COMPLETE_APPLICABLE_FIXTURE_COSTSET')
    except Malformed:return _answer('CONFLICT')
    except Unsupported:return _answer('UNAVAILABLE')


def new_store():return dict(schema='HSBI-C1-STORE-1',ledger=new_registry(),receipts={})


def _store_shape(store):
    exact.fields(store,('schema','ledger','receipts'));require(store['schema']=='HSBI-C1-STORE-1' and type(store['receipts']) is dict)
    ledger=store['ledger'];exact.fields(ledger,('schema','revision','sources','allocations','events','journalComplete'))
    require(exact.uid(ledger['revision']) and type(ledger['journalComplete']) is bool and all(type(ledger[k]) is dict for k in ('sources','allocations','events')))


def _validate_core_journal(journal):
    require(type(journal) is dict)
    for k,entry in journal.items():
        exact.text(k);exact.fields(entry,('sequence','payload','digest'));require(exact.uid(entry['sequence']))
        require(type(entry['digest']) is str and len(entry['digest'])==64)
        payload=entry['payload'];require(type(payload) is dict)
        kind=payload.get('kind')
        if kind=='FUND':
            exact.fields(payload,('kind','source','allocation','event','grants','commit'));require(type(payload['commit']) is bool and type(payload['grants']) is dict and set(payload['grants'])==set(BUCKETS))
        elif kind=='CONSUME_FREE':
            exact.fields(payload,('kind','source','allocation','event','bucket','amount','intent','purpose','revision'));require(exact.uid(payload['revision']) and number(payload['amount'])>0)
        else:raise Unsupported('unsupported journal operation')
        require(type(payload['source']) is tuple);exact.source_shape(payload['source']);exact.text(payload['allocation']);require(exact.uid(payload['event']))


def _reconcile_store(store,authority):
    dto.validate("Store",store)
    if authority is not None:dto.validate("Authority",authority)
    _store_shape(store)
    if authority is None:raise Unsupported('independent authority absent')
    exact.fields(authority,('history','coreJournal','receipts','complete','allocations','context','batches','fillHistory','costSets'))
    require(type(authority['complete']) is bool)
    if not authority['complete'] or authority['history'] is None or authority['coreJournal'] is None or authority['receipts'] is None or not store['ledger']['journalComplete']:raise Unsupported('complete independent journals required')  # GUARD:C1-JOURNAL
    require(type(authority['coreJournal']) is dict and type(authority['receipts']) is dict)
    _validate_core_journal(authority['coreJournal'])  # GUARD:C1-JOURNAL-DTO
    if canonical(store['receipts'])!=canonical(authority['receipts']):raise Unsupported('receipt journal mismatch')
    restored=recover(snapshot(store['ledger']),None,authority['coreJournal'],authority['history'])
    if restored['status']!='RECONCILED_MODEL_ONLY':raise Unsupported('core journal reconstruction failed')
    events=store['ledger']['events'];needed={k for k,e in events.items() if e['payload']['kind']!='FUND'}
    require(set(store['receipts'])==needed)  # GUARD:C1-RECEIPT-INVENTORY
    for k,receipt in store['receipts'].items():
        exact.fields(receipt,('request','digest','DebitAmount','RequiredBalance','AdditionalRisk','sourceDigest','allocationDigest','batchDigest','costDigest','evaluationContext'))
        q=receipt['request'];request_shape(q);require(receipt['digest']==digest(q) and k==event_key(q['source'],q['consumptionEvent']))
        e=events[k]['payload'];require(e['kind']=='CONSUME_FREE' and e['source']==q['source'] and e['allocation']==q['allocation'] and e['event']==q['consumptionEvent'])
        require(e['bucket']==q['bucket'] and e['purpose']==q['purpose'] and e['intent']==q['intent'] and e['revision']==q['revision'])
        require(number(receipt['AdditionalRisk'])>=0 and number(receipt['DebitAmount'])==number(q['PrincipalAmount']) and number(receipt['RequiredBalance'])==number(receipt['DebitAmount'])+number(receipt['AdditionalRisk']) and number(e['amount'])==number(receipt['DebitAmount']))
        require(receipt['sourceDigest']==store['ledger']['sources'][key(q['source'])]['recordDigest'])
        for field in ('sourceDigest','allocationDigest','batchDigest','costDigest'):require(type(receipt[field]) is str and len(receipt[field])==64 and all(c in '0123456789abcdef' for c in receipt[field]))
        core_allocation=store['ledger']['allocations'][allocation_key(q['source'],q['allocation'])]
        er=economic_record(authority['history'],q['source'])
        historical=dict(AllocationID=core_allocation['allocation'],source=core_allocation['source'],allocationEvent=core_allocation['allocationEvent'],PolicyVersion=core_allocation['policyVersion'],currency=er['currency'],digits=er['digits'],grants={b:v['OriginalGrant'] for b,v in core_allocation['buckets'].items()})
        require(q['allocationEvent']==historical['allocationEvent'] and receipt['allocationDigest']==digest(historical))  # GUARD:C1-HISTORICAL-ALLOCATION
        ctx=receipt['evaluationContext']
        require(verify_allocation_identity(q['identity'],authority['history'],q['source'],ctx,historical)=='PASS')  # GUARD:C1-HISTORICAL-IDENTITY
        require((ctx['ConsumptionEventID'],ctx['Revision'],number(ctx['PrincipalAmount']),ctx['bucket'],ctx['purpose'],ctx['intent'],ctx['BatchID'],ctx['CostSetID'])==(q['consumptionEvent'],q['revision'],number(q['PrincipalAmount']),q['bucket'],q['purpose'],q['intent'],q['BatchID'],q['CostSetID']))  # GUARD:C1-HISTORICAL-PLAN

    return True


def available(store,authority,account):
    try:
        require(type(account) is tuple and len(account)==3 and type(account[2]) is int and 1<=account[2]<2**63);exact.text(account[0]);exact.text(account[1])
        _reconcile_store(store,authority)
        return _arithmetic_reserve_balance(store['ledger'],authority['history'],account)
    except Malformed:return 'CONFLICT',None
    except Unsupported:return 'UNAVAILABLE',None


def _bind_allocation(q,store,a):
    record=a['allocations'].get(q['allocation'])
    if record is None:raise Unsupported('authoritative allocation absent')
    _allocation_shape(record)
    require(record['AllocationID']==q['allocation'] and record['allocationEvent']==q['allocationEvent'] and record['source']==q['source'])
    ledger=store['ledger']['allocations'].get(allocation_key(q['source'],q['allocation']))
    require(ledger is not None and ledger['source']==record['source'] and ledger['allocationEvent']==record['allocationEvent'] and ledger['policyVersion']==record['PolicyVersion'])
    require(all(number(ledger['buckets'][b]['OriginalGrant'])==number(record['grants'][b]) for b in BUCKETS))  # GUARD:C1-ALLOCATION-VECTOR
    economic=economic_record(a['history'],q['source']);require((record['currency'],record['digits'])==(economic['currency'],economic['digits']))
    return record


def authorize(q,store,authority):
    try:return _authorize(q,store,authority)
    except Malformed:return _answer('REJECT')
    except Unsupported:return _answer('UNAVAILABLE')


def _authorize(q,store,a):
    dto.validate("Request",q)  # GUARD:C2-AUTHORIZE-SHAPE
    dto.validate("Store",store)
    if a is not None:dto.validate("Authority",a)
    request_shape(q)
    _store_shape(store)
    if a is None:return _answer('UNAVAILABLE')
    require(type(a) is dict)
    if a.get('history') is None:return _answer('UNAVAILABLE')
    r=economic_record(a['history'],q['source'],a.get('complete',False))
    known=store['ledger']['sources'].get(key(q['source']))
    if known is not None:
        exact.fields(known,('source','recordDigest','granted','net','phase','unallocated'));require(type(known['recordDigest']) is str)
    if known is not None and known['recordDigest']!=digest(r):return _answer('CONFLICT')  # GUARD:C1-REPLAY-AUTHORITY
    _reconcile_store(store,a)
    prior=store['receipts'].get(event_key(q['source'],q['consumptionEvent']))
    if prior is not None:return _answer('NO_OP' if canonical(prior['request'])==canonical(q) else 'CONFLICT')  # GUARD:C1-REPLAY
    if any(a[k] is None for k in ('allocations','context','batches','fillHistory','costSets')):return _answer('UNAVAILABLE')
    require(all(type(a[k]) is dict for k in ('allocations','context','batches','fillHistory','costSets')))
    allocation=_bind_allocation(q,store,a);context=a['context']
    status=verify_allocation_identity(q['identity'],a['history'],q['source'],context,allocation)
    if status!='PASS':return _answer(status)
    require(context['ConsumptionEventID']==q['consumptionEvent'] and context['Revision']==q['revision']==store['ledger']['revision'])
    require(context['BatchID']==q['BatchID'] and context['CostSetID']==q['CostSetID'])
    require(number(context['PrincipalAmount'])==number(q['PrincipalAmount']) and all(context[k]==q[k] for k in ('bucket','purpose','intent')))  # GUARD:C1-PLANNED-OPERATION
    batch=a['batches'].get(q['BatchID'])
    if batch is None:return _answer('UNAVAILABLE')
    exact.fields(batch,('refs','expected'))
    if batch['expected'] is None:return _answer('UNAVAILABLE')
    require(batch['expected']['BatchID']==q['BatchID'])
    require((batch['expected']['Broker'],batch['expected']['Server'],batch['expected']['Account'])==q['source'][:3])
    require((batch['expected']['currency'],batch['expected']['digits'])==(r['currency'],r['digits']))
    assessment=assess_batch(batch['refs'],a['fillHistory'],batch['expected'])
    if assessment['status']!='CONFIRMED':return _answer('REJECT' if assessment['status'] in ('CONFLICT','OVER_CAP') else 'UNAVAILABLE')  # GUARD:C1-COMPOSITION-BATCH
    costs=cost_coverage(q['costClaims'],a['costSets'].get(q['CostSetID']))
    if costs['status']!='COVERED':return _answer('REJECT' if costs['status']=='CONFLICT' else 'UNAVAILABLE')  # GUARD:C1-COMPOSITION-COSTS
    costset=a['costSets'][q['CostSetID']];require((costset['currency'],costset['digits'])==(r['currency'],r['digits']))
    require(q['bucket']=='FinalReserve' and q['purpose'] in ('CatchUp','FinalClose'))
    value=exact.checked(number(q['PrincipalAmount'])+costs['AdditionalRisk'])
    require(exact.grid(q['PrincipalAmount'],r['digits']) and exact.grid(value,r['digits']))
    status,free=available(store,a,q['source'][:3])
    if status!='KNOWN_MODEL_AVAILABLE':return _answer('UNAVAILABLE')
    # available is account aggregate; allocation-local free must ALSO cover this debit.
    row=store['ledger']['allocations'][allocation_key(q['source'],q['allocation'])]['buckets'][q['bucket']]
    require(value<=free and value<=number(row['RemainingFree']))
    return _answer('ELIGIBLE_FOR_COMMIT',DebitAmount=number(q['PrincipalAmount']),RequiredBalance=value,AdditionalRisk=costs['AdditionalRisk'],sourceDigest=digest(r),allocationDigest=digest(allocation),batchDigest=digest(batch),costDigest=digest(costset))


def apply_for_test(q,store,authority):
    result=authorize(q,store,authority)  # GUARD:C1-APPLY-REVALIDATE
    if result['status']!='ELIGIBLE_FOR_COMMIT':return result,copy.deepcopy(store)
    s=copy.deepcopy(store)
    status,ledger=_operate_for_registry_replay(s['ledger'],authority['history'],q['source'],q['allocation'],q['consumptionEvent'],'CONSUME_FREE',q['bucket'],result['DebitAmount'],q['intent'],q['purpose'],q['revision'])
    if status!='COMMITTED_IN_MEMORY':return _answer(status),copy.deepcopy(store)
    for allocation in ledger['allocations'].values():
        for b in allocation['buckets'].values():
            if not balance(b['OriginalGrant'],b['Consumed'],b['Reserved'],b['RemainingFree'],b['Reservations']):return _answer('UNAVAILABLE'),copy.deepcopy(store)  # GUARD:C1-POSTSTATE
    s['ledger']=ledger;s['receipts'][event_key(q['source'],q['consumptionEvent'])]=dict(request=copy.deepcopy(q),digest=digest(q),evaluationContext=copy.deepcopy(authority['context']),**{k:result[k] for k in ('DebitAmount','RequiredBalance','AdditionalRisk','sourceDigest','allocationDigest','batchDigest','costDigest')})
    return _answer('COMMITTED_IN_MEMORY',DebitAmount=result['DebitAmount']),s


def snapshot_store(store):return dict(schema='HSBI-C1-STORE-SNAPSHOT-1',payload=copy.deepcopy(store),checksum=digest(store))


def recover_store(latest,previous,authority):
    try:
        chosen=None;fallback=False
        for i,s in enumerate((latest,previous)):
            if s is not None:dto.validate('RecoverySnapshot',s)  # GUARD:C2-SNAPSHOT-SHAPE
            if s is not None and s.get('schema')=='HSBI-C1-STORE-SNAPSHOT-1' and s.get('checksum')==digest(s['payload']):chosen=s['payload'];fallback=i==1;break
        if chosen is None:return _answer('UNAVAILABLE',store=None,fallbackUsed=False)
        _reconcile_store(chosen,authority)
        return _answer('RECONCILED_MODEL_ONLY',store=copy.deepcopy(chosen),fallbackUsed=fallback)
    except Malformed:return _answer('CONFLICT',store=None,fallbackUsed=False)
    except Unsupported:return _answer('UNAVAILABLE',store=None,fallbackUsed=False)
