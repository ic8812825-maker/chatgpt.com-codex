"""DG01-LEDGER-1 proposed executable specification, not production.
Integer minor units; independent explicit fixture authority; per-bucket ownership;
serialized revision check only (NOT durable/concurrent CAS). No historical evaluator imports.
"""
from copy import deepcopy
I64_MIN=-(2**63);I64_MAX=2**63-1;U64_MAX=2**64-1
FIELDS={'broker','server','account','deal','symbol','magic','cycle','role','schema','currency','digits','kind','components','entry','policy'}
def uid(x):return type(x) is int and 1<=x<=U64_MAX
def signed(x):return type(x) is int and I64_MIN<=x<=I64_MAX
def shape(r):
 if type(r) is not dict or set(r)!=FIELDS:return 'REJECT'
 if not all(type(r[k]) is str and r[k] for k in ('broker','server','symbol','currency','kind','role','entry')):return 'REJECT'
 if type(r['account']) is not int or not 0<r['account']<=I64_MAX or not signed(r['magic']) or r['magic']==0 or not uid(r['cycle']) or not uid(r['deal']) or not uid(r['policy']) or type(r['schema']) is not int or type(r['digits']) is not int:return 'REJECT'
 if type(r['components']) is not tuple or len(r['components'])!=4 or not all(signed(x) for x in r['components']):return 'REJECT'
 if r['policy']!=1:return 'UNAVAILABLE'
 if r['entry']=='IN':return 'REJECT'
 if r['entry'] not in ('OUT','OUT_BY'):return 'UNAVAILABLE'
 if r['schema']!=1 or r['currency']!='USD' or r['digits']!=2 or r['kind']!='RECONCILED':return 'UNAVAILABLE'
 if r['role'] not in ('BigCore','BigTrend'):return 'REJECT'
 if not 0<sum(r['components'])<=I64_MAX:return 'REJECT'
 return 'VALID'
def valid_key(k):return type(k) is tuple and len(k)==4 and all(type(x) is str and x for x in k[:2]) and type(k[2]) is int and 0<k[2]<=I64_MAX and uid(k[3])
def key(r):return (r['broker'],r['server'],r['account'],r['deal'])
class Ledger:
 def __init__(self):self.sources={};self.journal={}
 def fund(self,presented,authority,grants,allocation,event,history='UNKNOWN',costs=None,precision=None):
  s=shape(presented)
  if s!='VALID':return s
  if not uid(event) or not uid(allocation) or type(grants) is not tuple or len(grants)!=5 or not all(type(x) is int and 0<=x<=I64_MAX for x in grants) or sum(grants)!=sum(presented['components']):return 'REJECT'
  if type(history) is not str or history not in ('COMPLETE','INCOMPLETE','UNKNOWN') or costs is not None and type(costs) is not bool or precision is not None and type(precision) is not bool:return 'REJECT'
  if authority is None or history!='COMPLETE' or costs is not True or precision is not True:return 'UNAVAILABLE'
  s=shape(authority)
  if s!='VALID':return s
  if presented!=authority:return 'CONFLICT' if key(presented)==key(authority) else 'UNAVAILABLE'
  k=key(presented);payload=(deepcopy(presented),grants,allocation);ek=('fund',presented['account'],event)
  if ek in self.journal and self.journal[ek]!=payload:return 'CONFLICT'
  if k in self.sources:
   return 'NO_OP' if self.sources[k]['immutable']==payload else 'CONFLICT'
  if ek in self.journal:return 'CONFLICT'
  self.sources[k]=dict(immutable=payload,revision=1,authority_bound=True,buckets=[dict(G=n,C=0,F=n,reservations={}) for n in grants]);self.journal[ek]=payload;return 'FUNDED_IN_MEMORY'
 def operation(self,k,allocation,event,action,bucket,amount,owner,context,expected_revision,history='COMPLETE'):
  if not valid_key(k) or type(context) is not tuple or len(context)!=3 or type(context[0]) is not int or not 0<context[0]<=I64_MAX or type(context[1]) is not str or not context[1] or not uid(context[2]) or type(owner) is not str or not owner or not uid(event) or not uid(allocation) or not uid(expected_revision) or type(bucket) is not int or not 0<=bucket<5 or type(amount) is not int or not 0<amount<=I64_MAX:return 'REJECT'
  if type(history) is not str or history not in ('COMPLETE','INCOMPLETE','UNKNOWN'):return 'REJECT'
  if history!='COMPLETE' or k not in self.sources:return 'UNAVAILABLE'
  source=self.sources[k]
  if source['authority_bound'] is not True:return 'UNAVAILABLE'
  record=source['immutable'][0]
  if context!=(record['account'],record['symbol'],record['cycle']) or allocation!=source['immutable'][2]:return 'CONFLICT'
  payload=(k,allocation,action,bucket,amount,owner,context)
  ek=('operation',record['account'],event)
  # Proposed profile: exact replay precedes current revision, but current completeness/scope is mandatory.
  if ek in self.journal:return 'NO_OP' if self.journal[ek]==payload else 'CONFLICT'
  if expected_revision!=source['revision']:return 'CONFLICT'
  if source['revision']==U64_MAX:return 'REJECT'
  candidate=deepcopy(source);b=candidate['buckets'][bucket];held=b['reservations'].get(owner,0)
  if action=='reserve':
   if amount>b['F']:return 'REJECT'
   b['F']-=amount;b['reservations'][owner]=held+amount
  elif action=='release':
   if amount>held:return 'REJECT'
   b['F']+=amount;b['reservations'][owner]=held-amount
  elif action=='consume_reserved':
   if amount>held:return 'REJECT'
   b['C']+=amount;b['reservations'][owner]=held-amount
  elif action=='consume':
   if amount>b['F']:return 'REJECT'
   b['F']-=amount;b['C']+=amount
  else:return 'REJECT'
  b['reservations']={o:n for o,n in b['reservations'].items() if n}
  for row in candidate['buckets']:
   assert row['G']==row['C']+sum(row['reservations'].values())+row['F'] and min(row['G'],row['C'],row['F'],*row['reservations'].values())>=0
  candidate['revision']+=1;self.sources[k]=candidate;self.journal[ek]=payload;return 'APPLIED_IN_MEMORY'
 def snapshot(self):return deepcopy(self.__dict__)
 @classmethod
 def from_trusted_snapshot(cls,snapshot):
  # Private fixture reconstruction, not untrusted DTO parser or historical reauthorization.
  new=cls();new.__dict__=deepcopy(snapshot);return new
