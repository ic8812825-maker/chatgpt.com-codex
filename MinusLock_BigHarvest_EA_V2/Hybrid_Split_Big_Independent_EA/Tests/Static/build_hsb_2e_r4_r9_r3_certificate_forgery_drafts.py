#!/usr/bin/env python3
"""Derive twelve genuine forgeries from one valid committed state."""
import argparse,copy,json,hashlib
from pathlib import Path
from build_hsb_2e_r4_r9_r3_draft_fixtures import base,h
def setp(v,path,value):
 cur=v
 for key in path.split('.')[:-1]:cur=cur[int(key)] if isinstance(cur,list) else cur[key]
 key=path.split('.')[-1];cur[int(key) if isinstance(cur,list) else key]=value
CASES=[('BROKER_RECORD',['ledger.records.0.money']),('BROKER_RECORD_REHASHED',['ledger.records.0.money','brokerProposal.ledgerRoot']),('BROKER_PROPOSAL',['brokerProposal.totalMoney']),('ECONOMIC_PROPOSAL',['economicProposal.availableMoney']),('ALLOCATION',['allocation.reserveAddition']),('PERSISTENCE',['persistence.stateRevision']),('FSM',['fsm.outputRevision']),('OUTPUT_STATE',['persistence.previousStateDigest']),('REVISION',['certificate.body.outputRevision']),('CERT_BODY',['certificate.body.inputRevision']),('CERT_BODY_REHASHED',['certificate.body.inputRevision','certificate.digest']),('MUTUAL_ALL',['ledger.records.0.money','brokerProposal.totalMoney','economicProposal.availableMoney','allocation.reserveAddition','persistence.stateRevision','fsm.outputRevision','certificate.body.outputRevision','certificate.digest'])]
def build(root):
 b=base();rows=[]
 for i,(name,paths) in enumerate(CASES):
  n=copy.deepcopy(b)
  for p in paths:
   if p.endswith('digest'):setp(n,p,'REHASHED_'+name)
   elif 'money' in p.lower() or 'reserve' in p.lower() or 'available' in p.lower() or 'totalMoney' in p:setp(n,p,'99.00')
   elif p.endswith('ledgerRoot'):setp(n,p,h(n['ledger']))
   elif p.endswith('previousStateDigest'):setp(n,p,'FORGED_STATE')
   else:setp(n,p,9)
  rows.append({'testMetadata':{'fixtureId':'CERT_FORGERY_'+name,'tags':['certificate','negative']},'baseFixtureId':'VALID_COMMITTED_S1','targetProperty':name,'allowedChangedPaths':paths,'scenarioInput':n,'authoritativeAnchor':b['authoritativeAnchor'],'expectedCheckId':'R9_CERT_'+name,'expectedReason':'CERTIFICATE_PROVENANCE_MISMATCH'})
 (root/'Tests/Vectors/HSB_2E_R4_R9_R3_CERTIFICATE_FORGERY_DRAFTS.json').write_text(json.dumps({'schemaVersion':1,'validBase':b,'cases':rows},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);build(Path(p.parse_args().root))
