"""Independent C3 mathematical oracle: integer coefficient/scale only, no subject imports."""
import re
I64_MIN=-(2**63);I64_MAX=2**63-1

def coefficient(text):
 text=str(text)
 if text.startswith('.'):text='0'+text
 if text.startswith('-.'):text='-0'+text[1:]
 if text.startswith('+.'):text='+0'+text[1:]
 m=re.fullmatch(r'([+-]?)(\d+)(?:\.(\d*))?(?:[eE]([+-]?\d+))?',str(text));assert m
 sign,whole,frac,exp=m.groups();frac=frac or '';scale=len(frac)-int(exp or 0);n=int(whole+frac)*(-1 if sign=='-' else 1)
 if scale<0:n*=10**(-scale);scale=0
 return n,scale

def units(text,digits=2):
 n,s=coefficient(text)
 if s<=digits:return n*10**(digits-s)
 d=10**(s-digits);assert n%d==0,'not on posted grid';return n//d

def money_state(grant,consumed,reserved,free):return min(grant,consumed,reserved,free)>=0 and grant==consumed+reserved+free

def transition(nets,cap):
 running=0;losses=[]
 for n in nets:running+=n;losses.append(max(0,-running))
 return dict(SignedBatchLoss=losses[-1] if losses else 0,PrefixLosses=losses,StickyBreach=any(n>cap for n in losses),PeakLoss=max(losses,default=0))

def sequential(initial,amounts):
 remaining=initial;trace=[]
 for i,n in enumerate(amounts):
  if n<=0 or n>remaining:return dict(remaining=remaining,trace=trace,rejected=i+1)
  trace.append((remaining,n,remaining-n));remaining-=n
 assert initial==remaining+sum(r[1] for r in trace)
 return dict(remaining=remaining,trace=trace,rejected=None)

def volume_valid(volume,minimum,maximum,step,origin='0'):
 values=[coefficient(v) for v in (volume,minimum,maximum,step,origin)];s=max(v[1] for v in values);v,lo,hi,g,o=[n*10**(s-d) for n,d in values]
 return g>0 and lo>0 and lo<=v<=hi and (v-o)%g==0

def checked(n):
 if not I64_MIN<=n<=I64_MAX:raise OverflowError('signed int64 overflow')
 return n
