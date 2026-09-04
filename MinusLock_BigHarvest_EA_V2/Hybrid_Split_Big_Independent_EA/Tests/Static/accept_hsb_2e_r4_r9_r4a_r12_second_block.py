import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import run_hsb_2e_r4_r9_r4a_r10_regressions as r10
import verify_hsb_2e_r4_r9_r4a_r10 as v10
import run_hsb_2e_r4_r9_r4a_r11_first_block as first
import run_hsb_2e_r4_r9_r4a_r12_second_block as second
OUT=ROOT/'Tests/Evidence/R4A_R12/acceptance.json'
def main():
 a=argparse.ArgumentParser();a.add_argument('--publish-evidence',action='store_true');q=a.parse_args();find=[];old=r10.run();f=first.run();s=second.run();
 if old['required']!=67 or old['wrongFailures'] or old['unexpectedInfrastructureErrors']:find.append('R10_REGRESSION')
 try:v10.execute()
 except Exception:find.append('R10_POSITIVE')
 if f['result']!='PASS':find.append('R11_FIRST_BLOCK')
 if s['result']!='PASS' or not all(x['accepted'] for x in s['sensitivity']):find.append('R12_SECOND_BLOCK')
 cp=subprocess.run([sys.executable,'Tests/Static/verify_hsb_2e_r4_r9_r4a_r12_alignment.py'],cwd=ROOT,text=True,stdout=subprocess.PIPE)
 if cp.returncode:find.append('ALIGNMENT')
 out={'R10':old['executed'],'firstBlockFixtures':f['fixtures'],'secondBlockFixtures':s['fixtures'],'secondBlockSensitivity':sum(x['accepted'] for x in s['sensitivity']),'findings':find,'result':'PASS' if not find else 'FAIL'}
 if q.publish_evidence:OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(f"RESULT={out['result']} R10={out['R10']} SECOND={out['secondBlockFixtures']} SENS={out['secondBlockSensitivity']}/7 FINDINGS={len(find)}");return 0 if not find else 1
if __name__=='__main__':raise SystemExit(main())
