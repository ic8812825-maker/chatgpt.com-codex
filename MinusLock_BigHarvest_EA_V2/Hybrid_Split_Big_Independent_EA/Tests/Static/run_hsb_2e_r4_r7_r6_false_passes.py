#!/usr/bin/env python3
"""Executable, exact-input audit of the eight R4-R6 false-pass families."""
import argparse,copy,hashlib,json,sys
from dataclasses import replace
from pathlib import Path

def canonical(value):
    from hsb_2e_provenance_model_r4_r6 import canon
    return json.dumps(canon(value),sort_keys=True,separators=(',',':'))

def run(root,write=False):
    root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'))
    from hsb_2e_reference_model_r4_r6 import execute_scenario
    from hsb_2e_test_fixtures_r4_r6 import broker_fixture
    from hsb_2e_provenance_model_r4_r6 import digest
    fixtures=[]
    # The first four execute the vulnerable R6 implementation directly.
    x=broker_fixture('INITIAL'); committed=execute_scenario(x)['state']; forged=copy.deepcopy(committed)
    cert=forged['commitCertificate']; fake='f'*64
    forged.update(economicProposalDigest=fake,allocationResultDigest=fake,persistenceRecordDigest=fake,committedOutputDigest=fake)
    forged['commitCertificate']=replace(cert,economicProposalDigest=fake,allocationResultDigest=fake,persistenceRecordDigest=fake,outputStateDigest=fake,certificateDigest='')
    forged['commitCertificate']=replace(forged['commitCertificate'],certificateDigest=digest(forged['commitCertificate'].body()))
    replay=broker_fixture('INITIAL');replay['persistedState']=forged;replay['context']['stateRevision']=forged['stateRevision']
    fixtures.append(('FP-R7-001',replay,execute_scenario(replay),'R7_OUTPUT_STATE_RECOMPUTATION'))
    a=broker_fixture('SMALL');b=copy.deepcopy(a);a['positions'][2]['residualVolume']='.10';b['positions'][2]['residualVolume']='.20'
    ra,rb=execute_scenario(a),execute_scenario(b);fixtures.append(('FP-R7-002',{'first':a,'second':b},{'status':'PASS' if ra.get('economicProposal') and rb.get('economicProposal') and ra['economicProposal'].newFarVolume!=rb['economicProposal'].newFarVolume else 'REJECT','reason':'UNSEALED_RESIDUAL_CHANGES_NEW_FAR'},'R7_BIG_RESIDUAL_PROVENANCE'))
    p=broker_fixture('INITIAL');object.__setattr__(p['pricePolicy'],'buyCloseSide','ASK');object.__setattr__(p['pricePolicy'],'sellCloseSide','BID');object.__setattr__(p['pricePolicy'],'policyDigest',digest(p['pricePolicy'].body()));r=p['dealRecords'][0];object.__setattr__(r,'price',p['snapshot'].ask);object.__setattr__(r,'recordDigest',digest(r.body()))
    fixtures.append(('FP-R7-003',p,execute_scenario(p),'R7_NORMATIVE_CLOSE_SIDES'))
    s=broker_fixture('INITIAL');snap=s['snapshot'];object.__setattr__(snap,'accountLogin',999);object.__setattr__(snap,'magic',999);object.__setattr__(snap,'cycleId','FOREIGN');object.__setattr__(snap,'stateRevision',999);object.__setattr__(snap,'digestValue',digest(snap.body()))
    fixtures.append(('FP-R7-004',s,execute_scenario(s),'R7_SNAPSHOT_CONTEXT_BINDING'))
    # Exact historical inputs demonstrate the lossy adapter and count-only oracle defects.
    requested=[('FP-R7-005','R4_R4','R4_BAD_BINDING'),('FP-R7-006','R4_R4','R4_DUAL_TAIL'),('FP-R7-007','R4_R3','MISSING_SMALL'),('FP-R7-008','R4_R3','MALFORMED_DEALS')]
    for cid,ver,vid in requested:
        data=json.loads((root/'Tests/Vectors'/f'HSB_2E_{ver}_VECTORS.json').read_text())['vectors'];v=next(q for q in data if q['VECTOR_ID']==vid)
        mod=__import__(f'hsb_2e_{ver.lower()}_to_r4_r6_adapter');adapted=mod.adapt(v);actual=execute_scenario(adapted['canonicalInput'])
        fixtures.append((cid,v,actual,'R7_LOSSLESS_ADAPTER' if cid=='FP-R7-005' else 'R7_SEMANTIC_ORACLE'))
    rows=[]
    for cid,inp,result,check in fixtures:
        blob=canonical(inp);rows.append({'caseId':cid,'historicalModel':'R4-R6','exactInput':json.loads(blob),'exactInputSHA256':hashlib.sha256(blob.encode()).hexdigest(),'historicalStatus':result['status'],'historicalReason':result['reason'],'falsePassReproduced':result['status']=='PASS','requiredR7CheckId':check})
    out={'schemaVersion':1,'cases':rows,'R6_FALSE_PASSES_REQUIRED':8,'R6_FALSE_PASSES_REPRODUCED':sum(r['falsePassReproduced'] for r in rows),'RESULT':'PASS' if all(r['falsePassReproduced'] for r in rows) else 'FAIL'}
    if write:
        (root/'Tests/Vectors/HSB_2E_R4_R7_R6_FALSE_PASSES.json').write_text(json.dumps({'schemaVersion':1,'cases':[{'caseId':r['caseId'],'exactInput':r['exactInput'],'exactInputSHA256':r['exactInputSHA256'],'requiredR7CheckId':r['requiredR7CheckId']} for r in rows]},indent=2,sort_keys=True)+'\n')
        (root/'Tests/Evidence/HSB_2E_PREP_R4_R7_R6_FALSE_PASS_REPRODUCTION.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'},sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--write',action='store_true');a=p.parse_args();raise SystemExit(0 if run(a.root,a.write) else 1)
