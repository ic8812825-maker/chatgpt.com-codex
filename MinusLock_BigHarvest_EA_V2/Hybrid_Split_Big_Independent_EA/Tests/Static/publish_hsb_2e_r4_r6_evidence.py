#!/usr/bin/env python3
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
EVIDENCE=('CLEAN_RESULT','FALSE_PASS_REPRODUCTION','EXACT_HISTORICAL_FIXTURES','ADAPTER_COVERAGE','CROSS_VERSION_RESULTS','INVARIANT_RESULTS','MUTATION_CATALOG','MUTATION_RESULTS','ECONOMIC_CONSERVATION','PERSISTED_PROVENANCE','CERTIFICATE_BINDING')
def run_json(root,script):
 p=subprocess.run([sys.executable,str(root/'Tests/Static'/script),'--root',str(root)],capture_output=True,text=True,check=True);return json.loads(p.stdout)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));ev=root/'Tests/Evidence';ev.mkdir(exist_ok=True)
 verifier=subprocess.run([sys.executable,str(root/'Tests/Static/verify_hsb_2e_prep_r4_r6.py'),'--root',str(root)],capture_output=True,text=True,check=True)
 payloads={'CLEAN_RESULT':{'stdout':verifier.stdout,'exitCode':0},'FALSE_PASS_REPRODUCTION':run_json(root,'run_hsb_2e_r4_r6_false_passes.py'),'EXACT_HISTORICAL_FIXTURES':run_json(root,'run_hsb_2e_r4_r6_exact_false_passes.py'),'CROSS_VERSION_RESULTS':run_json(root,'run_hsb_2e_r4_r6_cross_version.py'),'INVARIANT_RESULTS':{'checks':__import__('hsb_2e_invariants_r4_r6').run_checks()},'MUTATION_RESULTS':run_json(root,'run_hsb_2e_r4_r6_source_mutations.py'),'ECONOMIC_CONSERVATION':run_json(root,'run_hsb_2e_r4_r6_economic.py'),'PERSISTED_PROVENANCE':run_json(root,'run_hsb_2e_r4_r6_provenance.py')}
 payloads['ADAPTER_COVERAGE']={k:payloads['CROSS_VERSION_RESULTS'][k] for k in ('HISTORICAL_VECTORS_REQUIRED','HISTORICAL_VECTORS_ADAPTED_TO_R6','HISTORICAL_VECTORS_EXECUTED_ON_R6','HISTORICAL_MODELS_USED_AS_TEST_TARGET')};payloads['MUTATION_CATALOG']=json.loads((root/'Tests/Static/hsb_2e_r4_r6_source_mutations.json').read_text());payloads['CERTIFICATE_BINDING']={k:v for k,v in payloads['INVARIANT_RESULTS']['checks'].items() if 'CERTIFICATE' in k}
 for name in EVIDENCE:(ev/f'HSB_2E_PREP_R4_R6_{name}.json').write_text(json.dumps(payloads[name],indent=2,sort_keys=True,default=str)+'\n')
 artifacts=sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and ('R4_R6' in p.name or 'r4_r6' in p.name) and 'FILE_MANIFEST' not in p.name and 'EVIDENCE_SEAL' not in p.name)
 manifest=root/'Reports/HSB_2E_PREP_R4_R6_FILE_MANIFEST_SHA256.txt';manifest.write_text('\n'.join(f'{sha(p)}  {p.relative_to(root)}' for p in artifacts)+'\n')
 seal=ev/'HSB_2E_PREP_R4_R6_EVIDENCE_SEAL_SHA256.txt';files=[ev/f'HSB_2E_PREP_R4_R6_{n}.json' for n in EVIDENCE];seal.write_text('\n'.join(f'{sha(p)}  {p.relative_to(root)}' for p in files)+'\n')
 print('EVIDENCE_PUBLISHED=YES');return True
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if main(a.root) else 1)
