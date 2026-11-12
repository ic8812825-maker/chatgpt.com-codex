"""Independent proposed in-memory specification. Settled amounts are integer minor units.
No production imports, no broker, no persistence, no concurrency claim. Fixture source authority only.
"""
from copy import deepcopy
class Ledger:
 def __init__(self):self.sources={};self.events={};self.rev=0
 def fund(self,key,components,grants,event,history=True,currency='USD',digits=2):
  if not history:return 'UNAVAILABLE'
  if not isinstance(key,tuple) or len(key)!=4 or type(key[2]) is not int or type(key[3]) is not int or not 0<key[2]<=2**63-1 or not 0<key[3]<=2**64-1:return 'REJECT'
  if type(event) is not int or not 0<event<=2**64-1:return 'REJECT'
  if currency!='USD' or digits!=2:return 'UNAVAILABLE'
  if not all(type(x) is int and -(2**63)<=x<2**63 for x in (*components,*grants)):return 'REJECT'
  net=sum(components)
  if net<=0 or any(x<0 for x in grants) or sum(grants)!=net or net>=2**63:return 'REJECT'
  payload=(tuple(components),tuple(grants),currency,digits)
  if key in self.sources:return 'NO_OP' if self.sources[key]['payload']==payload else 'CONFLICT'
  if ('F',event) in self.events:return 'CONFLICT'
  self.sources[key]=dict(payload=payload,G=net,C=0,R=0,F=net,owner=None)
  self.events['F',event]=(key,payload);self.rev+=1;return 'FUNDED_IN_MEMORY'
 def op(self,key,event,action,amount,owner,complete=True):
  if not complete:return 'UNAVAILABLE'
  if key not in self.sources:return 'UNAVAILABLE'
  if type(event) is not int or not 0<event<=2**64-1 or type(amount) is not int or amount<=0 or not owner:return 'REJECT'
  payload=(key,action,amount,owner)
  if ('C',event) in self.events:return 'NO_OP' if self.events['C',event]==payload else 'CONFLICT'
  s=deepcopy(self.sources[key])
  if action=='reserve':
   if s['owner'] not in (None,owner) or amount>s['F']:return 'REJECT'
   s['F']-=amount;s['R']+=amount;s['owner']=owner
  elif action=='release':
   if s['owner']!=owner or amount>s['R']:return 'REJECT'
   s['R']-=amount;s['F']+=amount
  elif action=='consume_reserved':
   if s['owner']!=owner or amount>s['R']:return 'REJECT'
   s['R']-=amount;s['C']+=amount
  elif action=='consume':
   if amount>s['F']:return 'REJECT'
   s['F']-=amount;s['C']+=amount
  else:return 'REJECT'
  if s['R']==0:s['owner']=None
  assert s['G']==s['C']+s['R']+s['F'] and min(s['C'],s['R'],s['F'])>=0
  self.sources[key]=s;self.events['C',event]=payload;self.rev+=1;return 'APPLIED_IN_MEMORY'
 def reconstruct(self,snapshot):
  # Accounting reconstruction only, never historical funding eligibility.
  if not isinstance(snapshot,dict) or set(snapshot)!=set(('sources','events','rev')):return 'REJECT'
  for s in snapshot['sources'].values():
   if s['G']!=s['C']+s['R']+s['F'] or min(s['C'],s['R'],s['F'])<0:return 'CONFLICT'
  self.sources=deepcopy(snapshot['sources']);self.events=deepcopy(snapshot['events']);self.rev=snapshot['rev'];return 'ACCOUNTING_RECONSTRUCTED_ONLY'
