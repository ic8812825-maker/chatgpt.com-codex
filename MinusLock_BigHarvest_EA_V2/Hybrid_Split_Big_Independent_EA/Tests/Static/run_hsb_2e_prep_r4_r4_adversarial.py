#!/usr/bin/env python3
import argparse,copy,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'Reference'));import hsb_2e_reference_model_r4_r3 as old
BASE='c37cb942283371bbc95483244ff47607707f7a37'
def dg(x):return hashlib.sha256(json.dumps(x,sort_keys=True,default=str).encode()).hexdigest()
def cases(root):
 v=json.loads((root/'Tests/Vectors/HSB_2E_R4_R3_VECTORS.json').read_text())['vectors'];base=next(x for x in v if x['VECTOR_ID']=='VALID_BIG')['INPUT'];rows=[]
 def add(cid,fields,fn,expected):
  x=copy.deepcopy(base);fn(x)
  try:a=old.settle(x);unsafe=a.get('status')=='PASS' or cid=='FP-R4-07' and not a.get('output',{}).get('consumedDealIds')
  except Exception as e:a={'UNHANDLED_EXCEPTION':type(e).__name__};unsafe=True
  rows.append({'COUNTEREXAMPLE_ID':cid,'BASELINE_SHA':BASE,'SOURCE_VECTOR_ID':'VALID_BIG','MUTATED_FIELDS':fields,'HISTORICAL_ACTUAL':a,'NORMATIVE_EXPECTED':expected,'ROOT_CAUSE':'R4-R3 lost primitive/registry/partial-restart validation','INPUT_SHA256':dg(x),'OUTPUT_SHA256':dg(a),'EXIT_CODE':0 if unsafe else 1,'FALSE_PASS_REPRODUCED':unsafe})
 add('FP-R4-01','zero positions/requests; no deals',lambda x:([p.update(positionVolume='0') for p in x['positions']],[i.update(requestedVolume='0') for i in x['intents']],x.update(deals=[])),'POSITION_VOLUME_INVALID')
 add('FP-R4-02','off-grid 1.005',lambda x:(x['positions'][0].update(positionVolume='1.005'),x['intents'][0].update(requestedVolume='1.005'),x['deals'][0].update(volume='1.005')),'VOLUME_OFF_GRID')
 add('FP-R4-03','price=-1',lambda x:x['deals'][0].update(price='-1'),'DEAL_PRICE_INVALID')
 add('FP-R4-04','confirmed="false"',lambda x:x['deals'][0].update(confirmed='false'),'DEAL_CONFIRMED_TYPE_INVALID')
 add('FP-R4-05','second intent same ticket',lambda x:(x['intents'].append(copy.deepcopy(x['intents'][0])),x['intents'][-1].update(intentId='I-X')),'MULTIPLE_INTENTS_FOR_POSITION')
 add('FP-R4-06','revision=-5',lambda x:(x['context'].update(stateRevision=-5),[p.update(positionRevision=-5) for p in x['positions']],[i.update(stateRevision=-5) for i in x['intents']],[d.update(stateRevision=-5) for d in x['deals']]),'STATE_REVISION_INVALID')
 add('FP-R4-07','partial first deal',lambda x:x['deals'][0].update(volume='.4'),'PARTIAL_REGISTRY_PERSISTED')
 add('FP-R4-08','non-bijective persisted bindings',lambda x:x.update(consumedDealIds=['OLD1','OLD2'],seenEventIds=['SAME'],dealEventBindings={'OLD1':'SAME','OLD2':'SAME'}),'PERSISTED_BINDING_NOT_BIJECTIVE')
 add('FP-R4-09','registry wrong types',lambda x:x.update(consumedDealIds='D1',seenEventIds={'E1':True},dealEventBindings=[]),'PERSISTED_REGISTRY_SCHEMA_INVALID')
 return rows
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--write-evidence',action='store_true');a=p.parse_args();r=Path(a.root).resolve();rows=cases(r);n=sum(x['FALSE_PASS_REPRODUCED'] for x in rows);out='\n'.join(f'{x["COUNTEREXAMPLE_ID"]}|{"PASS" if x["FALSE_PASS_REPRODUCED"] else "FAIL"}' for x in rows)+f'\nFALSE_PASS_COUNTEREXAMPLES_REQUIRED=9\nFALSE_PASS_COUNTEREXAMPLES_REPRODUCED={n}\nFALSE_PASS_REPRODUCTION={"PASS" if n==9 else "FAIL"}\n';print(out,end='')
 if a.write_evidence:(r/'Tests/Evidence/HSB_2E_PREP_R4_R4_FALSE_PASS_REPRODUCTION.json').write_text(json.dumps({'cases':rows,'required':9,'reproduced':n,'result':'PASS' if n==9 else 'FAIL'},indent=2,sort_keys=True,default=str)+'\n')
 return 0 if n==9 else 1
if __name__=='__main__':raise SystemExit(main())
