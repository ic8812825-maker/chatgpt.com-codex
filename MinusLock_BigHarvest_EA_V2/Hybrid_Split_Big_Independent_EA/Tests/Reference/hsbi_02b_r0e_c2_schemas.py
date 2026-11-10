"""PROPOSED C2 schemas, independent of results. Formats inherit C1/R0E; no broker facts."""
import re
import hsbi_02b_r0d_independent_oracle as x
VERSION='HSBI-C2-SCHEMAS-1'
B=x.BUCKETS
ECON=('Broker','Server','Account','Symbol','Magic','Cycle','Position','Deal','Order','Event','Role','Plan','PolicyVersion','Revision','Snapshot')
PROOF=tuple(k for k in ECON if k!='Event')+('EconomicEventID','AllocationEventID','ConsumptionEventID','AllocationID')
def fields(names,default='text',**overrides):return {k:overrides.get(k,default) for k in names}
def ids(names):return fields(names,'uid')
def obj(**f):return {'object':f}
def seq(t,item):return {t:item}
def lit(v):return {'literal':v}
def enum(*v):return {'enum':list(v)}
def nullable(v):return {'nullable':v}
I=fields(ECON,'uid',Broker='text',Server='text',Symbol='text',Role='text',Account='account',Magic='magic')
P={k:v for k,v in I.items() if k!='Event'};P.update(ids(('EconomicEventID','AllocationEventID','ConsumptionEventID')));P['AllocationID']='text'
M={
 'EconomicIdentity':obj(**I),'Identity':obj(**P),
 'EconomicRecord':obj(identity='EconomicIdentity',kind='text',entry='text',currency='text',digits='digits',**fields(('profit','swap','commission','fee','rawNet','postedNet'),'money')),
 'Allocation':obj(AllocationID='text',source='source',allocationEvent='uid',PolicyVersion='uid',currency='text',digits='digits',grants='Grants'),
 'EvaluationContext':obj(**ids(('Plan','Revision','Snapshot','ConsumptionEventID')),**fields(('AllocationID','BatchID','CostSetID','bucket','purpose','intent')),PrincipalAmount='money',fresh='bool'),
 'Request':obj(schema=lit('HSBI-C1-REQUEST-1'),source='source',allocation='text',allocationEvent='uid',consumptionEvent='uid',identity='Identity',PrincipalAmount='money',bucket='text',purpose='text',intent='text',revision='uid',BatchID='text',CostSetID='text',costClaims=seq('list','CostClaim')),
 'BatchExpectedContext':obj(schema=lit('HSBI-C1-BATCH-1'),**fields(('BatchID','Broker','Server','Symbol','currency')),Account='account',**ids(('Cycle','Order','Position')),digits='digits',expectedVolume='money',RequiredDeals=seq('tuple','source'),historyComplete='bool',NettingPolicy=nullable('text'),cap='money'),
 'Batch':obj(refs=seq('list','source'),expected=nullable('BatchExpectedContext')),
 'FillRecord':obj(source='source',**fields(('BatchID','Symbol','currency')),**ids(('Cycle','Order','Position')),digits='digits',volume='money',net='money'),
 'CostSet':obj(schema=lit('HSBI-C1-COSTSET-1'),Complete='bool',currency='text',digits='digits',PolicyVersion='uid',Authority='text',items=seq('list','CostFact')),
 'BucketState':obj(**fields(('OriginalGrant','Consumed','Reserved','RemainingFree'),'money'),Reservations=seq('map','money')),
 'LedgerAllocation':obj(source='source',allocation='text',allocationEvent='uid',policyVersion='uid',buckets=obj(**{k:'BucketState' for k in B})),
 'LedgerSource':obj(source='source',recordDigest='hash',granted='money',net='money',phase=enum('COMMITTED','PREPARED'),unallocated='money'),
 'FundPayload':obj(kind=lit('FUND'),source='source',allocation='text',event='uid',grants='Grants',commit='bool'),
 'ConsumptionPayload':obj(kind=lit('CONSUME_FREE'),source='source',allocation='text',event='uid',bucket='text',amount='money',intent='text',purpose='text',revision='uid'),
 'JournalPayload':{'variant':{'FUND':'FundPayload','CONSUME_FREE':'ConsumptionPayload'}},
 'JournalEntry':obj(sequence='uid',payload='JournalPayload',digest='hash'),
 'Ledger':obj(schema=lit('HSBI-R0E-FREE-1'),revision='uid',sources=seq('map','LedgerSource'),allocations=seq('map','LedgerAllocation'),events=seq('map','JournalEntry'),journalComplete='bool'),
 'Receipt':obj(request='Request',**fields(('digest','sourceDigest','allocationDigest','batchDigest','costDigest'),'hash'),**fields(('DebitAmount','RequiredBalance','AdditionalRisk'),'money'),evaluationContext='EvaluationContext'),
 'Store':obj(schema=lit('HSBI-C1-STORE-1'),ledger='Ledger',receipts=seq('map','Receipt')),
 'RecoverySnapshot':obj(schema=lit('HSBI-C1-STORE-SNAPSHOT-1'),payload='Store',checksum='hash'),
 'CoreSnapshot':obj(schema=lit('HSBI-R0E-SNAPSHOT-1'),payload='Ledger',checksum='hash'),
 'Authority':obj(history=nullable(seq('map','EconomicRecord')),coreJournal=nullable(seq('map','JournalEntry')),receipts=nullable(seq('map','Receipt')),complete='bool',allocations=nullable(seq('map','Allocation')),context=nullable('EvaluationContext'),batches=nullable(seq('map','Batch')),fillHistory=nullable(seq('map','FillRecord')),costSets=nullable(seq('map','CostSet'))),
 'Grants':obj(**{k:'money' for k in B}),
}
common=dict(CostID='text',Applicability=enum('REQUIRED','NOT_APPLICABLE','KNOWN_ZERO','UNKNOWN'),Amount='money',AmountBasis=enum('SIGNED_COMPONENT','NONNEGATIVE_RISK'),currency='text',RiskBasis='text',Window='text',AlreadyIncluded='bool',PolicyVersion='uid')
M['CostFact']=obj(**common,OverlapKnown='bool');M['CostClaim']=obj(**common,AdditionalDeduction='bool')

def validate(name,value,path='$',depth=0):
    x.require(depth<48)
    spec=M[name] if type(name) is str and name in M else name
    if type(spec) is str:
        if spec=='text':x.text(value)
        elif spec=='money':x.number(value)
        elif spec=='uid':x.require(x.uid(value))  # GUARD:C2-EXACT-ID
        elif spec=='account':x.require(type(value) is int and 1<=value<2**63)
        elif spec=='magic':x.require(type(value) is int and -2**63<=value<2**63 and value!=0)
        elif spec=='bool':x.require(type(value) is bool)
        elif spec=='digits':x.unit(value)
        elif spec=='hash':x.require(type(value) is str and re.fullmatch('[0-9a-f]{64}',value) is not None)
        elif spec=='source':x.require(type(value) is tuple);x.source_shape(value)
        else:raise RuntimeError('Unknown programmer schema '+spec)
        return
    if 'nullable' in spec:
        if value is not None:validate(spec['nullable'],value,path,depth+1)
    elif 'object' in spec:
        x.fields(value,tuple(spec['object']))  # GUARD:C2-OBJECT-FIELDS
        for k,v in spec['object'].items():validate(v,value[k],path+'.'+k,depth+1)
    elif 'literal' in spec:
        if type(value) is not type(spec['literal']):raise x.Malformed(path+': wrong schema type')
        if value!=spec['literal']:raise x.Unsupported(path+': unknown schema/operation')
    elif 'enum' in spec:x.require(type(value) is str and value in spec['enum'])
    elif 'variant' in spec:
        x.require(type(value) is dict and type(value.get('kind')) is str)
        if value['kind'] not in spec['variant']:raise x.Unsupported('unsupported journal operation')
        validate(spec['variant'][value['kind']],value,path,depth+1)
    else:
        tag=next(iter(spec));typ={'list':list,'tuple':tuple,'map':dict}[tag];x.require(type(value) is typ)
        if tag=='map':
            for k,v in value.items():x.text(k);validate(spec[tag],v,path+'['+k+']',depth+1)
        else:
            for i,v in enumerate(value):validate(spec[tag],v,path+'['+str(i)+']',depth+1)

def inventory():
    rows=[]
    def walk(s,path):
        if type(s) is dict and 'object' in s:
            for k,v in s['object'].items():
                rows.append(dict(FieldPath=path+'.'+k,Required=True,ExactType=v,RangeOrEnum=v,Nullable=type(v) is dict and 'nullable' in v,Units='lots' if k in ('volume','expectedVolume') else 'account currency' if v=='money' else 'dimensionless/schema-defined',IdentityParticipation=k in I or k.endswith('ID') or k in ('source','allocationEvent','event','policyVersion'),AuthoritySource='independent fixture provider or declared request/store boundary',FailureOutcome='REJECT/CONFLICT; unsupported schema/domain UNAVAILABLE'))
    for n,s in M.items():walk(s,n)
    return dict(SchemaVersion=VERSION,UnknownFields='REJECT',Schemas=M,Fields=rows)
