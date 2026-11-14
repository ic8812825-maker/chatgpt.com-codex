"""PROPOSED finite test-only model. No broker, file durability or dispatch."""
import copy, math
from decimal import Decimal, ROUND_HALF_EVEN, InvalidOperation
I64_MAX=9223372036854775807

def integer(x):return type(x) is int and -I64_MAX-1<=x<=I64_MAX

def minor(value,digits=2):
 if type(digits) is not int or digits not in (0,2,3,8):raise ValueError('unsupported fixture precision')
 try:
  d=Decimal(str(value))
  if not d.is_finite():raise ValueError('nonfinite')
  v=int((d*10**digits).quantize(Decimal(1),rounding=ROUND_HALF_EVEN))
  if not integer(v):raise ValueError('overflow')
  return v
 except (InvalidOperation,OverflowError) as e:raise ValueError('outside domain') from e

def valid_record(r):
 required={'broker','server','account','symbol','magic','cycle','deal','order','position','action','event','role','entry','direction','volume','price','profit','swap','commission','fee','net','time','schema','currency','digits'}
 if set(r)!=required:return False
 if any(not integer(r[k]) or r[k]<=0 for k in ('account','cycle','deal','order','position','action','event','time')):return False
 if not r['broker'] or not r['server'] or not r['symbol'] or r['schema']!=1:return False
 if r['role'] not in ('BigCore','BigTrend','Small','Far') or r['entry'] not in ('OUT','OUT_BY') or r['direction'] not in ('BUY','SELL'):return False
 if any(not integer(r[k]) for k in ('profit','swap','commission','fee','net')):return False
 if sum(r[k] for k in ('profit','swap','commission','fee'))!=r['net']:return False
 if r['currency']!='USD' or r['digits']!=2:return False
 return all(type(r[k]) in (int,float) and math.isfinite(r[k]) and r[k]>0 for k in ('volume','price'))

def key(r):return (r['broker'],r['server'],r['account'],r['deal']) # abstract identity; not approved wire format
class Ledger:
 def __init__(self):self.sources={};self.events={}
 def snapshot(self):return copy.deepcopy((self.sources,self.events))
 @classmethod
 def restore_trusted(cls,s):
  x=cls();x.sources,x.events=copy.deepcopy(s);return x
 def fund(self,r,authority,vector,event):
  if not valid_record(r):return 'REJECT'
  if authority is None:return 'UNAVAILABLE'
  if r!=authority:return 'CONFLICT'
  if not isinstance(vector,tuple) or len(vector)!=5 or any(not integer(v) or v<0 for v in vector):return 'REJECT'
  if r['net']<=0 or sum(vector)!=r['net']:return 'REJECT'
  k=key(r);body=('FUND',k,copy.deepcopy(r),vector)
  if event in self.events:return 'NO_OP' if self.events[event]==body else 'CONFLICT'
  if k in self.sources:return 'CONFLICT'
  self.sources[k]={'record':copy.deepcopy(r),'vector':vector,'free':list(vector),'consumed':[0]*5,'reserved':[0]*5,'revision':1}
  self.events[event]=body;return 'FUNDED'
 def consume(self,k,bucket,amount,event,revision,operation='CONSUME'):
  body=(operation,k,bucket,amount,revision)
  if event in self.events:return 'NO_OP' if self.events[event]==body else 'CONFLICT'
  if k not in self.sources or type(bucket) is not int or bucket not in range(5):return 'REJECT'
  s=self.sources[k]
  if revision!=s['revision'] or not integer(revision) or revision==I64_MAX:return 'REJECT'
  if not integer(amount) or amount<=0 or amount>s['free'][bucket]:return 'REJECT'
  if operation not in ('CONSUME','RESERVE'):return 'REJECT'
  s['free'][bucket]-=amount;s['consumed' if operation=='CONSUME' else 'reserved'][bucket]+=amount;s['revision']+=1
  self.events[event]=body;return 'APPLIED'

def risk(values,limits):return all(math.isfinite(v) for v in values+limits) and all(0<=v<=cap for v,cap in zip(values,limits))
def grid(v,minimum,maximum,step):
 try:
  v,minimum,maximum,step=map(lambda x:Decimal(str(x)),(v,minimum,maximum,step))
  return all(x.is_finite() for x in (v,minimum,maximum,step)) and step>0 and minimum<=v<=maximum and v%step==0
 except InvalidOperation:return False

def final_close(realized,unrealized,remaining,threshold,positions_fresh=True,risk_ok=True):
 return all(integer(v) for v in (realized,unrealized,remaining,threshold)) and remaining>=0 and threshold>=0 and positions_fresh and risk_ok and realized+unrealized-remaining>=threshold

def barrier(outcome,actual,expected,revision,expected_revision,confirmed):
 return outcome=='COMPLETED' and all(math.isfinite(v) for v in (actual,expected)) and expected>0 and actual==expected and revision==expected_revision and confirmed

def topology(slots):
 allowed={'far':'Far','core':'BigCore','trend':'BigTrend','small':'Small','initialBuy':'InitialBuy','initialSell':'InitialSell','candidate':'Candidate'}
 if any(slot not in allowed or role!=allowed[slot] for slot,role in slots):return False
 return sum(role=='Far' for slot,role in slots)<=1 and len({slot for slot,role in slots})==len(slots)

def catchup(eligible,source_proof,far_loss,far_proof,buffer,available,projected=False):
 vals=(eligible,source_proof,far_loss,far_proof,buffer,available)
 if not all(integer(v) for v in vals):return 'REJECT'
 if projected:return 'PREVIEW_ONLY'
 if eligible!=source_proof or far_loss!=max(0,-far_proof):return 'REJECT'
 if min(eligible,far_loss,buffer,available)<0 or eligible>available:return 'REJECT'
 return 'PASS' if eligible-far_loss-buffer>0 else 'REJECT'
