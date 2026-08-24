#!/usr/bin/env python3
import argparse,copy,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'Reference'))
import hsb_2e_reference_model_r4_r2 as old

def dg(x):return hashlib.sha256(json.dumps(x,sort_keys=True,default=str).encode()).hexdigest()
def build(root):
 vs=json.loads((root/'Tests/Vectors/HSB_2E_R4_R2_VECTORS.json').read_text())['vectors'];one=next(x for x in vs if x['VECTOR_ID']=='FULL_ONE')['INPUT'];big=next(x for x in vs if x['VECTOR_ID']=='BIG_FULL')['INPUT'];cases=[]
 x=copy.deepcopy(one);x['deals'][0]['volume']='.5';z=copy.deepcopy(x['deals'][0]);z.update(eventId='EVENT-2',volume='.5');x['deals'].append(z);cases.append(('FP-R3-01','FULL_ONE','duplicate dealId with different eventId','classify_fill',x))
 x=copy.deepcopy(one);x['deals'][0]['timestamp']=1;cases.append(('FP-R3-02','FULL_ONE','deal timestamp below minimum','classify_fill',x))
 x=copy.deepcopy(one);x['intent'].update(transactionId='FOREIGN_TRANSACTION',actionId='FOREIGN_ACTION');cases.append(('FP-R3-03','FULL_ONE','foreign intent identity','classify_fill',x))
 x=copy.deepcopy(one);x['position'].update(symbol='GBPUSD',magic=99,cycleId='FOREIGN');cases.append(('FP-R3-04','FULL_ONE','foreign managed position','classify_fill',x))
 x=copy.deepcopy(big);x['positions']=x['positions'][:1];x['intents']=x['intents'][:1];x['deals']=x['deals'][:1];cases.append(('FP-R3-05','BIG_FULL','missing mandatory Small leg','big_settlement',x))
 x=copy.deepcopy(one);x['position']['volume']='9';cases.append(('FP-R3-06','FULL_ONE','requested volume below position volume','classify_fill',x))
 rows=[]
 for cid,vid,changed,fn,x in cases:
  a=old.execute(fn,x);passed=a['status']=='PASS';rows.append({'COUNTEREXAMPLE_ID':cid,'SOURCE_VECTOR_ID':vid,'CHANGED_FIELDS':changed,'BASELINE_ACTUAL_RESULT':a,'NORMATIVE_EXPECTED_RESULT':{'status':'NOT_PASS','settlementApplied':False},'EXIT_CODE':0 if passed else 1,'INPUT_SHA256':dg(x),'RESULT_SHA256':dg(a),'ROOT_CAUSE':'R4-R2 omitted independent broker-evidence trust-chain validation','FALSE_PASS_REPRODUCED':passed})
 return rows
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--write-evidence',action='store_true');a=p.parse_args();r=Path(a.root).resolve();rows=build(r);n=sum(x['FALSE_PASS_REPRODUCED'] for x in rows);out='\n'.join(f'{x["COUNTEREXAMPLE_ID"]}|{"PASS" if x["FALSE_PASS_REPRODUCED"] else "FAIL"}' for x in rows)+f'\nFALSE_PASS_COUNTEREXAMPLES_REQUIRED=6\nFALSE_PASS_COUNTEREXAMPLES_REPRODUCED={n}\nFALSE_PASS_REPRODUCTION={"PASS" if n==6 else "FAIL"}\n';print(out,end='')
 if a.write_evidence:(r/'Tests/Evidence/HSB_2E_PREP_R4_R3_FALSE_PASS_REPRODUCTION.json').write_text(json.dumps({'cases':rows,'required':6,'reproduced':n,'result':'PASS' if n==6 else 'FAIL'},indent=2,sort_keys=True,default=str)+'\n')
 return 0 if n==6 else 1
if __name__=='__main__':raise SystemExit(main())
