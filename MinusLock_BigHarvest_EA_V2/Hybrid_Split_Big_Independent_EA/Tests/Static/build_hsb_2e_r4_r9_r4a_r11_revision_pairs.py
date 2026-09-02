#!/usr/bin/env python3
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r10 as v10
from build_hsb_2e_r4_r9_r4a_r5_assets import recert
OUT=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R11_REVISION_PAIRS.json'
def main():
 c=next(copy.deepcopy(f['scenarioInput']) for f in v10.fixtures() if f.get('scenarioInput',{}).get('phase')=='COMMITTED');rows=[]
 for domain,key in [('STATE','stateRevision'),('SNAPSHOT','snapshotRevision')]:
  positive=copy.deepcopy(c);negative=copy.deepcopy(c)
  for x in negative['deals']+negative['events']:x[key]=999
  recert(negative);rows.append({'pairId':f'R11_{domain}_REVISION_CONTEXT','positive':positive,'negative':negative,'changedPaths':[f'deals[*].{key}',f'events[*].{key}'],'cleanExpected':{'class':'NORMATIVE_REJECTION','checkId':'R9_EXECUTION_REVISION','reason':f'{domain}_REVISION_CONTEXT_MISMATCH'},'mutantExpected':'ACCEPTED'})
 OUT.write_text(json.dumps({'pairs':rows},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
