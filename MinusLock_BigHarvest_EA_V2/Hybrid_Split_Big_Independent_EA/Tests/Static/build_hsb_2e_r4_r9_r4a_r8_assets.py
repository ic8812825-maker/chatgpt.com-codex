#!/usr/bin/env python3
"""Build R8 lifecycle declarations causally, from each current operation only."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r8 as v
from build_hsb_2e_r4_r9_r4a_r5_assets import digest
from build_hsb_2e_r4_r9_r4a_r7_assets import replay,cert
SRC=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R7_POSITIVE_BASES.json';OUT=v.VECTORS
def state(b):return {'stateBody':b,'stateDigest':digest(b)}
def main():
 fs=json.loads(SRC.read_text())['fixtures']
 for f in fs:
  if 'lifecycleSequence' not in f:continue
  steps=f['lifecycleSequence']['steps']
  for i,st in enumerate(steps):
   r=st['operationInput'];st['inputState']=state(v.state_body(r,r['fsm']['inputState'],r['fsm']['inputRevision']));st['declaredOutputState']=state(v.expected_output(st))
   if i+1<len(steps):
    n=steps[i+1]['operationInput'];b=st['declaredOutputState']['stateBody'];n['persistedState']['consumedDealIds']=copy.deepcopy(b['consumedDealIds']);n['persistedState']['seenEventIds']=copy.deepcopy(b['seenEventIds'])
    if steps[i+1]['operation']=='REPLAY':
     # Replay the immediately preceding operation rather than unrelated future IDs.
     deal_ids=[d['dealId'] for d in r.get('deals',[])];event_ids=[e['eventId'] for e in r.get('events',[])]
     for j,d in enumerate(n['deals']):d['dealId']=deal_ids[min(j,len(deal_ids)-1)];d['eventId']=event_ids[min(j,len(event_ids)-1)]
     for j,e in enumerate(n['events']):e['dealId']=deal_ids[min(j,len(deal_ids)-1)];e['eventId']=event_ids[min(j,len(event_ids)-1)]
     n['persistedState']['dealEventBindings']=[{'dealId':d,'eventId':event_ids[min(j,len(event_ids)-1)]} for j,d in enumerate(deal_ids)]
     q=n['replayContract'];q['consumedDealIdsBefore']=copy.deepcopy(b['consumedDealIds']);q['consumedDealIdsAfter']=copy.deepcopy(b['consumedDealIds']);q['historicalRevisionAfter']=b['revision'];q['historicalRevisionBefore']=b['revision']-1;q['currentRevisionBefore']=b['revision'];q['currentRevisionAfter']=b['revision'];n['fsm']['inputRevision']=b['revision'];n['fsm']['outputRevision']=b['revision'];n['persistedState']['stateRevision']=b['revision'];replay(n)
    steps[i+1]['inputState']=copy.deepcopy(st['declaredOutputState'])
  # Recompute certificates and declarations after causal state propagation.
  for st in steps:
   r=st['operationInput']
   if r['phase']=='COMMITTED':r['certificate']=cert(r)
   st['inputState']=state(v.state_body(r,r['fsm']['inputState'],r['fsm']['inputRevision']))
   st['declaredOutputState']=state(v.expected_output(st))
  for i in range(1,len(steps)):steps[i]['inputState']=copy.deepcopy(steps[i-1]['declaredOutputState'])
 OUT.write_text(json.dumps({'schemaVersion':'3.3.0','fixtures':fs},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
