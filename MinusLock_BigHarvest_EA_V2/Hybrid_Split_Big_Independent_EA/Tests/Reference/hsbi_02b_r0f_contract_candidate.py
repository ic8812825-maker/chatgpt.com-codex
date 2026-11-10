"""PROPOSED R0F contract fixture. No production imports, broker IO or persistence.

Settled state uses integer minor units. Raw codec uses finite binary64 observations,
never creates posted money. All policy/context/completeness facts are FIXTURES.
"""
import copy,math,hashlib
class Invalid(ValueError):pass
class Unavailable(ValueError):pass
I64MIN=-(2**63);I64MAX=2**63-1;U64MAX=2**64-1
BUCKETS=('FinalReserve','PartialFar','Transition','Carry','Residual')
RAW=('Volume','Price','Profit','Swap','Commission','Fee','DealNet')
FIELDS=('SchemaVersion','Broker','Server','AccountLogin','Symbol','Magic','CycleID','DealTicket','OrderTicket','PositionIdentifier','ActionID','EventID','Role','EntryType','DealType','TimestampMsc','Volume','Price','Profit','Swap','Commission','Fee','DealNet','Currency','Precision','SourcePlanApplicable','SourcePlan','SourcePolicyApplicable','SourcePolicyVersion')

def require(ok):
 if not ok:raise Invalid('malformed or conflicting contract DTO')
def uid(x):return type(x) is int and 1<=x<=U64MAX
def text(x):
 require(type(x) is str and bool(x) and '\x00' not in x)
 try:
  raw=x.encode('utf-8')
  if len(raw)>0xffffffff:raise Unavailable('wire length outside uint32; native resource cap separately required')
  return raw
 except UnicodeEncodeError as e:raise Invalid('invalid UTF-8 source') from e

def raw64_bits(x):
 require(type(x) is float and math.isfinite(x))
 if x==0:return 0 # Z profile: explicit zero equivalence, requires approval.
 sign=1 if x<0 else 0;n=abs(x);exponent=0
 while n>=2:
  n/=2;exponent+=1
  if exponent>1023:raise Unavailable('unsupported raw normalization')
 while n<1:
  n*=2;exponent-=1
  if exponent < -1074:raise Unavailable('unsupported subnormal runtime')
 if exponent < -1022:
  for _ in range(exponent+1074):n*=2
  mantissa=int(n);biased=0
 else:
  fraction=n-1;mantissa=0
  for _ in range(52):
   fraction*=2;bit=1 if fraction>=1 else 0;fraction-=bit;mantissa=(mantissa<<1)|bit
  require(fraction==0);biased=exponent+1023
 return (sign<<63)|(biased<<52)|mantissa

def text17(x):
 require(type(x) is float and math.isfinite(x));x=0.0 if x==0 else x
 significand,exponent=format(x,'.16e').split('e');return significand+'e'+('-' if int(exponent)<0 else '+')+str(abs(int(exponent))).zfill(3)

def token(value,profile):
 if value is None:return b'n' if profile=='B' else b'n0:'
 if type(value) is bool:return b'b'+(b'1' if value else b'0')
 if type(value) is str:
  b=text(value);return b's'+(len(b).to_bytes(4,'big') if profile=='B' else str(len(b)).encode()+b':')+b
 if type(value) is int:
  require(I64MIN<=value<=U64MAX)
  if profile=='B':return (b'i'+value.to_bytes(8,'big',signed=True)) if value<0 else b'u'+value.to_bytes(8,'big')
  b=str(value).encode();return b'i'+str(len(b)).encode()+b':'+b
 if type(value) is float:
  if profile=='B':return b'd'+raw64_bits(value).to_bytes(8,'big')
  b=text17(value).encode();return b'd'+str(len(b)).encode()+b':'+b
 raise Invalid('unsupported raw codec type')

def record_shape(r):
 require(type(r) is dict and set(r)==set(FIELDS));require(uid(r['SchemaVersion']))
 if r['SchemaVersion']!=1:raise Unavailable('unknown economic schema')
 for k in ('Broker','Server','Symbol','Role','EntryType','DealType'):text(r[k])
 require(type(r['AccountLogin']) is int and 1<=r['AccountLogin']<=I64MAX)
 require(type(r['Magic']) is int and I64MIN<=r['Magic']<=I64MAX and r['Magic']!=0)
 for k in ('CycleID','DealTicket','OrderTicket','PositionIdentifier','ActionID','EventID'):require(uid(r[k]))
 require(type(r['TimestampMsc']) is int and 1<=r['TimestampMsc']<=I64MAX)
 require(r['Role'] in ('BigCore','BigTrend','Small','Far','Initial') and r['EntryType'] in ('IN','OUT','INOUT','OUT_BY') and r['DealType'] in ('BUY','SELL'))
 for k in RAW:require(type(r[k]) is float and math.isfinite(r[k]))
 require(r['Volume']>0 and r['Price']>0)
 if r['Currency'] is None or r['Precision'] is None:raise Unavailable('unknown money units')
 text(r['Currency']);require(type(r['Precision']) is int)
 if not 0<=r['Precision']<=8:raise Unavailable('fixture precision domain, MQL production domain not approved')
 for flag,name in (('SourcePlanApplicable','SourcePlan'),('SourcePolicyApplicable','SourcePolicyVersion')):
  require(type(r[flag]) is bool)
  if r[flag] and r[name] is None:raise Unavailable('unknown applicable origin association')
  require(uid(r[name]) if r[flag] else r[name] is None)

def source_key(r):
 record_shape(r);return (r['Broker'],r['Server'],r['AccountLogin'],r['DealTicket'])

def encode_record(r,profile):
 record_shape(r);require(profile in ('A','B'));head=b'HSBI-T17Z-1\n' if profile=='A' else b'HSBI-F64Z-1\x00'
 return head+b''.join(token(k,profile)+token(r[k],profile) for k in FIELDS)

def duplicate(old,incoming):
 try:
  k0,k1=source_key(old),source_key(incoming)
  if k0!=k1:return 'NEW_IDENTITY_ONLY'
  # Exact raw values with explicitly proposed zero equivalence; no epsilon/net-only equality.
  return 'NO_OP' if encode_record(old,'B')==encode_record(incoming,'B') else 'CONFLICT'
 except Invalid:return 'REJECT'
 except Unavailable:return 'UNAVAILABLE'

def allocation_duplicate(old,new):
 def valid(r):
  require(type(r) is dict and set(r)=={'Source','Event','Policy','Currency','Precision','Phase','EligibleNet','Unallocated','Grants'})
  require(type(r['Source']) is tuple and len(r['Source'])==4 and uid(r['Event']) and uid(r['Policy']));text(r['Source'][0]);text(r['Source'][1]);require(type(r['Source'][2]) is int and 1<=r['Source'][2]<=I64MAX and uid(r['Source'][3]));text(r['Currency']);require(type(r['Precision']) is int and 0<=r['Precision']<=8 and r['Phase'] in ('PREPARED','COMMITTED'))
  require(type(r['Grants']) is dict and set(r['Grants'])==set(BUCKETS))
  for x in list(r['Grants'].values())+[r['EligibleNet'],r['Unallocated']]:require(type(x) is int and 0<=x<=I64MAX)
  require(sum(r['Grants'].values())+r['Unallocated']==r['EligibleNet'])
  if r['Phase']=='COMMITTED':require(r['Unallocated']==0)
 try:
  valid(old);valid(new)
  if (old['Source'],old['Event'])!=(new['Source'],new['Event']):return 'NEW_IDENTITY_ONLY'
  return 'NO_OP' if old==new else 'CONFLICT'
 except Invalid:return 'REJECT'

def checked(n):
 if not I64MIN<=n<=I64MAX:raise Unavailable('int64 overflow')
 return n

def migration(grant,consumed,remaining_gross,reserved,currency,digits,owners_known):
 if currency is None or digits is None or not owners_known:return 'UNAVAILABLE',None
 try:
  text(currency);require(type(digits) is int and 0<=digits<=8)
  for n in (grant,consumed,remaining_gross,reserved):require(type(n) is int and 0<=n<=I64MAX)
  require(grant==consumed+remaining_gross and reserved<=remaining_gross)
  return 'MAPPED_FIXTURE_ONLY',dict(OriginalGrant=grant,Consumed=consumed,Reserved=reserved,Free=remaining_gross-reserved,RemainingGross=remaining_gross)
 except Invalid:return 'CONFLICT',None

def state(grant=5000):return dict(OriginalGrant=grant,Consumed=0,Reserved=0,Free=grant,Owners={},Journal={},Revision=1,Phase='COMMITTED',Currency='USD',Precision=2,HistoryComplete=True)
def valid_balance(s):
 require(type(s) is dict and set(s)=={'OriginalGrant','Consumed','Reserved','Free','Owners','Journal','Revision','Phase','Currency','Precision','HistoryComplete'})
 if s['Currency'] is None or s['Precision'] is None:raise Unavailable('unknown balance units')
 text(s['Currency']);require(type(s['Precision']) is int and 0<=s['Precision']<=8 and uid(s['Revision']) and s['Phase'] in ('PREPARED','COMMITTED'))
 for k in ('OriginalGrant','Consumed','Reserved','Free'):require(type(s[k]) is int and 0<=s[k]<=I64MAX)
 require(s['OriginalGrant']==s['Consumed']+s['Reserved']+s['Free']);require(type(s['Owners']) is dict and all(type(k) is str and bool(k) and type(v) is int and v>=0 for k,v in s['Owners'].items()) and sum(s['Owners'].values())==s['Reserved'])

def operate(s,event,kind,amount,owner='O1',revision=None):
 original=copy.deepcopy(s)
 try:
  valid_balance(s);require(uid(event) and kind in ('RESERVE','RELEASE','CONSUME_FREE','CONSUME_RESERVED') and type(amount) is int and amount>0);text(owner)
  require(type(s['HistoryComplete']) is bool and type(s['Journal']) is dict)
  if not s['HistoryComplete']:return 'UNAVAILABLE',original
  require(uid(s['Revision']))
  if s['Phase']!='COMMITTED':return 'REJECT',original
  request=(kind,amount,owner,s['Revision'] if revision is None else revision)
  prior=s['Journal'].get(event)
  if prior is not None:return ('NO_OP' if prior==request else 'CONFLICT'),original
  require(uid(request[-1]) and request[-1]==s['Revision'])
  if s['Revision']==U64MAX:return 'UNAVAILABLE',original
  if kind in ('RESERVE','CONSUME_FREE'):require(amount<=s['Free'])
  else:require(amount<=s['Owners'].get(owner,0))
  out=copy.deepcopy(s)
  if kind=='RESERVE':out['Free']-=amount;out['Reserved']+=amount;out['Owners'][owner]=out['Owners'].get(owner,0)+amount
  elif kind=='RELEASE':out['Free']+=amount;out['Reserved']-=amount;out['Owners'][owner]-=amount
  elif kind=='CONSUME_RESERVED':out['Reserved']-=amount;out['Consumed']+=amount;out['Owners'][owner]-=amount
  else:out['Free']-=amount;out['Consumed']+=amount
  out['Revision']+=1;out['Journal'][event]=request;valid_balance(out);return 'COMMITTED_IN_MEMORY',out
 except Invalid:return 'REJECT',original
 except Unavailable:return 'UNAVAILABLE',original

def transition(fills,cap,policy):
 require(type(fills) is list and all(type(n) is int for n in fills) and type(cap) is int and cap>=0)
 if policy not in ('A','B','C'):return dict(status='UNAVAILABLE',policy=None,trace=[])
 net=0;peak=0;sticky=False;rows=[]
 for n in fills:
  net+=n;loss=max(0,-net);peak=max(peak,loss);sticky|=loss>cap
  gate=loss<=cap if policy=='A' else not sticky if policy=='B' else peak<=cap
  rows.append(dict(Net=net,CurrentLoss=loss,PeakLoss=peak,StickyBreach=sticky,CapGate=gate))
 return dict(status='ASSESSED_FIXTURE_ONLY',policy=policy,trace=rows)

def eligible(role,posted,confirmed,closing=True):
 require(type(confirmed) is bool and type(closing) is bool)
 if not confirmed:return 'UNAVAILABLE',None
 require(type(posted) is int and role in ('BigCore','BigTrend','Small'))
 if not closing:return 'NOT_HARVEST_SOURCE',dict(BigReserve=0,SmallResidualHeld=0)
 amount=max(0,posted);return 'ALLOCATABLE_FIXTURE_ONLY',dict(BigReserve=amount if role!='Small' else 0,SmallResidualHeld=amount if role=='Small' else 0)

def cost_status(fact):
 if fact is None:return 'UNAVAILABLE'
 if type(fact) is not dict or set(fact)!={'OverlapKnown','Applicable','AlreadyIncluded','AdditionalDeduction'}:return 'CONFLICT'
 if any(type(v) is not bool for v in fact.values()):return 'CONFLICT'
 if not fact['OverlapKnown']:return 'UNAVAILABLE'
 expected=fact['Applicable'] and not fact['AlreadyIncluded']
 return 'COVERED_FIXTURE_ONLY' if fact['AdditionalDeduction']==expected else 'CONFLICT'


def confirm_source(record,authority):
 """Authority is independently supplied FIXTURE data, never real broker authentication."""
 if authority is None:return 'UNAVAILABLE',None
 try:
  record_shape(record);require(type(authority) is dict and set(authority)=={'Record','Currency','Precision','PostedComponents','PostedNet','PolicyVerified'})
  record_shape(authority['Record']);require(type(authority['PolicyVerified']) is bool)
  if not authority['PolicyVerified']:return 'UNAVAILABLE',None
  require(source_key(record)==source_key(authority['Record']) and encode_record(record,'B')==encode_record(authority['Record'],'B'))
  require((record['Currency'],record['Precision'])==(authority['Currency'],authority['Precision']))
  comp=authority['PostedComponents'];require(type(comp) is dict and set(comp)=={'Profit','Swap','Commission','Fee'})
  require(type(authority['PostedNet']) is int and all(type(v) is int and I64MIN<=v<=I64MAX for v in comp.values()))
  total=checked(sum(comp.values()));require(total==authority['PostedNet'])
  return 'RECONCILED_FIXTURE_ONLY',total
 except Invalid:return 'CONFLICT',None
 except Unavailable:return 'UNAVAILABLE',None

def raw_signed_sum(record):
 record_shape(record)
 ratios=[record[k].as_integer_ratio() for k in ('Profit','Swap','Commission','Fee')];denominator=max(d for _,d in ratios);numerator=sum(n*(denominator//d) for n,d in ratios);g=math.gcd(numerator,denominator)
 return numerator//g,denominator//g  # RAW_SIGNED_SUM only, not posted/available money.
