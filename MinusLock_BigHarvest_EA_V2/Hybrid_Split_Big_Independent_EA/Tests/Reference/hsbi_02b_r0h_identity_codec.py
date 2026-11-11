"""R0H TEST-ONLY identity/strict codecs, no broker IO/state/money.
Shape/type profile from frozen R0F; independently tested byte codec and lookup.
Z canonical zero; native resource profile4096bytes/string,65536bytes/record.
"""
import math
import hsbi_02b_r0f_contract_candidate as shape
FIELDS=shape.FIELDS
Invalid=shape.Invalid
Unavailable=shape.Unavailable
HEAD_B=b'HSBI-F64Z-1\0';HEAD_A=b'HSBI-T17Z-1\n'

def source_key(r):return (r['Broker'],r['Server'],r['AccountLogin'],r['DealTicket'])
def equal_body(a,b):
 for name in FIELDS:
  if a[name]!=b[name]:return False
 return True

def bits(x):
 if type(x) is not float or not math.isfinite(x):raise Invalid('finite float required')
 if x==0:return 0
 sign=1 if x<0 else 0;n=abs(x);e=0
 while n>=2:n/=2;e+=1
 while n<1:n*=2;e-=1
 if not -1074<=e<=1023:raise Unavailable('native binary64 domain')
 if e < -1022:
  for _ in range(e+1074):n*=2
  return (sign<<63)|int(n)
 m=0;n-=1
 for _ in range(52):
  n*=2;bit=int(n>=1);n-=bit;m=(m<<1)|bit
 if n!=0:raise Invalid('non binary64')
 return (sign<<63)|((e+1023)<<52)|m

def unbits(u):
 sign=-1 if u>>63 else 1;e=(u>>52)&2047;m=u&((1<<52)-1)
 if e==2047:raise Invalid('nonfinite binary64')
 if e==0 and m==0:
  if sign<0:raise Invalid('noncanonical negative zero')
  return 0.0
 coeff=m if e==0 else (1<<52)+m;power=-1074 if e==0 else e-1075
 x=float(coeff)
 while power>0:x*=2;power-=1
 while power<0:x/=2;power+=1
 return sign*x

def token(value,profile):
 if value is None:return b'n' if profile=='B' else b'n0:'
 if type(value) is bool:return b'b'+(b'1' if value else b'0')
 if type(value) is str:
  raw=value.encode('utf-8')
  if not raw or b'\0' in raw:raise Invalid('empty/nul string')
  if len(raw)>4096:raise Unavailable('string cap')
  return b's'+(len(raw).to_bytes(4,'big') if profile=='B' else str(len(raw)).encode()+b':')+raw
 if type(value) is int:
  if not -(1<<63)<=value<(1<<64):raise Invalid('integer domain')
  if profile=='B':return b'i'+value.to_bytes(8,'big',signed=True) if value<0 else b'u'+value.to_bytes(8,'big')
  raw=str(value).encode();return b'i'+str(len(raw)).encode()+b':'+raw
 if type(value) is float:
  if profile=='B':return b'd'+bits(value).to_bytes(8,'big')
  raw=shape.text17(value).encode();return b'd'+str(len(raw)).encode()+b':'+raw
 raise Invalid('unsupported token type')

def encode(r,profile='B'):
 shape.record_shape(r)
 if profile not in ('A','B'):raise Unavailable('unknown codec')
 out=(HEAD_B if profile=='B' else HEAD_A)+b''.join(token(k,profile)+token(r[k],profile) for k in FIELDS)
 if len(out)>65536:raise Unavailable('record cap')
 return out

def decode(raw,profile='B'):
 if type(raw) is not bytes:raise Invalid('wire bytes required')
 if profile not in ('A','B'):raise Unavailable('unknown codec')
 if len(raw)>65536:raise Unavailable('record cap')
 head=HEAD_B if profile=='B' else HEAD_A
 if not raw.startswith(head):raise Invalid('codec header')
 at=len(head)
 def take(n):
  nonlocal at
  if n<0 or n>len(raw)-at:raise Invalid('truncated')
  v=raw[at:at+n];at+=n;return v
 def read():
  nonlocal at
  tag=take(1)
  if tag==b'b':
   b=take(1)
   if b not in (b'0',b'1'):raise Invalid('bool tag')
   return b==b'1'
  if profile=='B':
   if tag==b'n':return None
   if tag==b's':
    n=int.from_bytes(take(4),'big')
    if n>4096:raise Unavailable('string cap')
    try:s=take(n).decode('utf-8')
    except UnicodeDecodeError as e:raise Invalid('UTF8') from e
    if not s or '\0' in s:raise Invalid('string shape')
    return s
   if tag in (b'u',b'i',b'd'):
    body=take(8)
    if tag==b'd':return unbits(int.from_bytes(body,'big'))
    v=int.from_bytes(body,'big',signed=tag==b'i')
    if tag==b'i' and v>=0:raise Invalid('noncanonical signed tag')
    return v
   raise Invalid('unknown type tag')
  # Strict length grammar; bounded before reading large payloads.
  start=at
  while at<len(raw) and raw[at:at+1]!=b':':
   if not 48<=raw[at]<=57 or at-start>=5:raise Invalid('text length')
   at+=1
  length=raw[start:at];take(1)
  if not length or len(length)>1 and length.startswith(b'0'):raise Invalid('noncanonical length')
  n=int(length)
  if n>4096:raise Unavailable('text token cap')
  value=take(n)
  if tag==b'n':
   if n!=0:raise Invalid('absent value')
   return None
  try:
   if tag==b's':v=value.decode('utf-8')
   elif tag==b'i':v=int(value)
   elif tag==b'd':v=float(value)
   else:raise Invalid('text tag')
  except (UnicodeError,ValueError,OverflowError) as e:raise Invalid('text value') from e
  if token(v,'A')!=tag+length+b':'+value:raise Invalid('noncanonical text')
  return v
 result={}
 for expected in FIELDS:
  name=read()
  if type(name) is not str or name!=expected:raise Invalid('field order/name/duplicate')
  result[name]=read()
 if at!=len(raw):raise Invalid('trailing bytes')
 shape.record_shape(result)
 return result

def classify(incoming,authority,registry,codec='B'):
 try:
  shape.record_shape(incoming)
  shape.require(type(codec) is str)
  if codec not in ('A','B'):return 'UNAVAILABLE'
  if authority is None or registry is None:return 'UNAVAILABLE'
  shape.require(type(authority) is dict and set(authority)=={'Complete','Record'})
  shape.require(type(registry) is dict and set(registry)=={'Complete','Records'})
  shape.require(type(authority['Complete']) is bool and type(registry['Complete']) is bool and type(registry['Records']) is list)
  if not authority['Complete'] or not registry['Complete'] or authority['Record'] is None:return 'UNAVAILABLE'
  shape.record_shape(authority['Record'])
  if source_key(incoming)!=source_key(authority['Record']):return 'UNAVAILABLE'
  if not equal_body(incoming,authority['Record']):return 'CONFLICT'
  indexed={}
  for row in registry['Records']:
   if row is None:return 'UNAVAILABLE'
   shape.record_shape(row);key=source_key(row)
   if key in indexed:return 'CONFLICT'
   indexed[key]=row
  prior=indexed.get(source_key(incoming))
  if prior is None:return 'NEW'
  return 'NO_OP' if equal_body(prior,incoming) else 'CONFLICT'
 except Invalid:return 'REJECT'
 except Unavailable:return 'UNAVAILABLE'
