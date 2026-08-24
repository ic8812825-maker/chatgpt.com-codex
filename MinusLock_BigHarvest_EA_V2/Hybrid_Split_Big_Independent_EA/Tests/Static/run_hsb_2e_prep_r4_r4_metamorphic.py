#!/usr/bin/env python3
import argparse,copy,json,random,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'Reference'));import hsb_2e_reference_model_r4_r4 as m
SEED=8812825
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--write-evidence',action='store_true');a=p.parse_args();r=Path(a.root).resolve();v=json.loads((r/'Tests/Vectors/HSB_2E_R4_R4_VECTORS.json').read_text())['vectors'];base=copy.deepcopy(next(x for x in v if x['VECTOR_ID']=='R4_VALID_BIG')['INPUT']);cases=[]
 def add(n,ok,detail):cases.append({'PROPERTY_ID':n,'RESULT':'PASS' if ok else 'FAIL','DETAIL':detail})
 original=m.execute_scenario(base);perm=copy.deepcopy(base);random.Random(SEED).shuffle(perm['deals']);rp=m.execute_scenario(perm);add('PERMUTATION',original['output']['moneyByTicket']==rp['output']['moneyByTicket'] and original['outputDigest']==rp['outputDigest'],'deal order canonicalized')
 split=copy.deepcopy(base);d=split['deals'][0];a1=copy.deepcopy(d);a2=copy.deepcopy(d);a1.update(dealId='D-S1',eventId='E-S1',orderId='O-S1',volume='.4',profit='4',commission='-.4');a2.update(dealId='D-S2',eventId='E-S2',orderId='O-S2',volume='.6',profit='6',commission='-.6');split['deals']=[a1,a2,split['deals'][1]];rs=m.execute_scenario(split);add('SPLIT_EQUIVALENCE',rs['status']=='PASS' and all(m.D(rs['output']['confirmedVolumeByTicket'][k])==m.D(v) for k,v in original['output']['confirmedVolumeByTicket'].items()) and all(m.D(rs['output']['moneyByTicket'][k])==m.D(v) for k,v in original['output']['moneyByTicket'].items()),'1 == .4+.6')
 dup=copy.deepcopy(split);dup['deals'][1]['dealId']=dup['deals'][0]['dealId'];rd=m.execute_scenario(dup);add('DUPLICATE_NON_EQUIVALENCE',rd['status']!='PASS','duplicate blocked')
 iso=copy.deepcopy(base);iso['deals'][0]['positionTicket']=iso['positions'][1]['positionTicket'];ri=m.execute_scenario(iso);add('TICKET_ISOLATION',ri['status']!='PASS','cross-ticket move blocked')
 scale=copy.deepcopy(base)
 for p0,i0,d0 in zip(scale['positions'],scale['intents'],scale['deals']):p0['positionVolume']=str(float(p0['positionVolume'])*2);i0['requestedVolume']=str(float(i0['requestedVolume'])*2);d0['volume']=str(float(d0['volume'])*2);d0['profit']=str(float(d0['profit'])*2);d0['commission']=str(float(d0['commission'])*2)
 add('SCALE_SANITY',m.execute_scenario(scale)['status']=='PASS','grid-preserving scale')
 boundary=copy.deepcopy(base);boundary['positions'][0]['positionVolume']='1.005';boundary['intents'][0]['requestedVolume']='1.005';boundary['deals'][0]['volume']='1.005';add('BOUNDARY_MOVEMENT',m.execute_scenario(boundary)['status']=='REJECT','half-step rejected')
 partial=copy.deepcopy(base);partial['deals'][0]['volume']='.4';pr=m.execute_scenario(partial);state=m.persisted_from_partial(pr);duplicate=m.restart_reconcile(state,base,[partial['deals'][0]]);cont=copy.deepcopy(base['deals'][0]);cont.update(dealId='D-CONT',eventId='E-CONT',orderId='O-CONT',volume='.6',profit='6',commission='-.6');full=m.restart_reconcile(state,base,[cont]);committed=m.persisted_from_partial(full);replay=m.restart_reconcile(committed,base,base['deals']);add('RESTART_EQUIVALENCE',pr['reason']=='PARTIAL_FILL' and duplicate['status']!='PASS' and full['phase']=='FSM_COMMITTED','partial→duplicate→continuation');add('IDEMPOTENCE',replay['reason']=='ALREADY_COMMITTED' and replay['output']['settlementApplied'] is False,'no second settlement')
 ok=all(x['RESULT']=='PASS' for x in cases);out=f'PROPERTY_SEED={SEED}\n'+''.join(f'{x["PROPERTY_ID"]}|{x["RESULT"]}\n' for x in cases)+f'METAMORPHIC_RESULT={"PASS" if ok else "FAIL"}\n';print(out,end='')
 if a.write_evidence:
  (r/'Tests/Evidence/HSB_2E_PREP_R4_R4_METAMORPHIC_RESULTS.json').write_text(json.dumps({'seed':SEED,'cases':cases,'result':'PASS' if ok else 'FAIL'},indent=2,sort_keys=True)+'\n');(r/'Tests/Evidence/HSB_2E_PREP_R4_R4_GENERATED_PROPERTY_RESULTS.json').write_text(json.dumps({'seed':SEED,'generatedCases':cases},indent=2,sort_keys=True)+'\n');(r/'Tests/Evidence/HSB_2E_PREP_R4_R4_RESTART_SEQUENCE_RESULTS.json').write_text(json.dumps({'partial':pr,'duplicate':duplicate,'continuation':full,'replay':replay,'result':'PASS' if ok else 'FAIL'},indent=2,sort_keys=True)+'\n')
 return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
