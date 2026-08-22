#!/usr/bin/env python3
"""Fail-closed compatibility gate for the immutable, accepted R7 baseline."""
import argparse, hashlib, subprocess, sys
from pathlib import Path

ACCEPTED = "df306557e4b228731b13280ab89ebfa140fed965"
ALLOWED = {"S040B", "S040C", "S044A", "S044B", "S045"}
CORE = {"S023","S024","S025","S026","S027","S028","S029","S030","S031","S032","S033","S034","S035","S036","S037","S038","S038R","S039","S039D","SREJECT","SENUM","SNUMERIC","SFINAL","S046E","SLEX85","S048"}
PROTECTED = (
 "Tests/Static/verify_hsb_2d_v1_r7.py","Tests/Static/run_hsb_2d_v1_r7_mutations.py","Tests/Static/hsb_2d_v1_r7_mutations.json","Tests/Static/hsb_mql5_lexer.py",
 "Tests/Evidence/HSB_2D_V1_R7_EVIDENCE_SEAL_SHA256.txt","Tests/Evidence/HSB_2D_V1_R7_ADVERSARIAL_RESULTS.json","Tests/Evidence/HSB_2D_V1_R7_TERMINAL_PATH_PROOFS.json","Tests/Evidence/HSB_2D_V1_R7_GUARD_OUTCOME_PROOFS.json","Tests/Evidence/HSB_2D_V1_R7_NO_OP_AUTHORIZATION.json","Tests/Evidence/HSB_2D_V1_R7_CONDITION_NORMALIZATION.json",
 "Include/Runtime/HSBI_RuntimeDecisionTypes.mqh","Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","Include/Runtime/HSBI_RuntimeRestartValidator.mqh","Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh")
REQUIRED_METRICS={"LEXER_PARSER_SELF_TESTS_FAILED":"0","ADVERSARIAL_FAILED":"0","GLOBAL_TERMINAL_PATH_ANALYSIS":"PASS","UNAUTHORIZED_NO_OP_GLOBAL_BLOCK":"PASS","S037_NO_OP_EXACT_AUTHORIZATION":"PASS","GUARD_EXECUTION_DOMINANCE":"PASS","GUARD_OUTCOME_DOMINANCE":"PASS","CONDITION_NORMALIZATION":"PASS"}

def parse(text):
 passed=set(); failed=set(); metrics={}
 for line in text.splitlines():
  p=line.split('|',2)
  if len(p)>=2 and p[1] in {"PASS","FAIL"}:(passed if p[1]=="PASS" else failed).add(p[0])
  if '=' in line and '|' not in line:
   k,v=line.split('=',1);metrics[k]=v
 return passed,failed,metrics
def sha(b): return hashlib.sha256(b).hexdigest()
def protected(root):
 rows=[]
 for rel in PROTECTED:
  old=subprocess.run(["git","show",f"{ACCEPTED}:{rel}"],cwd=root,capture_output=True).stdout
  cur=(root/rel).read_bytes() if (root/rel).is_file() else b""
  rows.append((rel,sha(old),sha(cur),bool(old) and old==cur))
 return rows
def evaluate(passed,failed,metrics,protected_ok):
 unexpected=failed-ALLOWED; missing=CORE-passed
 metrics_ok=all(metrics.get(k)==v for k,v in REQUIRED_METRICS.items())
 return not unexpected and not missing and metrics_ok and protected_ok,unexpected,missing
def self_tests():
 base_pass=set(CORE); base_metrics=dict(REQUIRED_METRICS)
 cases=[]
 cases.append(evaluate(base_pass,{"S044A","S045"},base_metrics,True)[0])
 cases.append(evaluate(base_pass,{"S040B","S045"},base_metrics,True)[0])
 cases.append(not evaluate(base_pass,{"S028"},base_metrics,True)[0])
 cases.append(not evaluate(base_pass,{"SLEX85"},base_metrics,True)[0])
 bad=dict(base_metrics);bad["ADVERSARIAL_FAILED"]="1";cases.append(not evaluate(base_pass,set(),bad,True)[0])
 cases.append(not evaluate(base_pass,{"S999"},base_metrics,True)[0])
 cases.append(not evaluate(base_pass-{"S028"},set(),base_metrics,True)[0])
 cases.append(not evaluate(base_pass,set(),base_metrics,False)[0])
 return cases
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--self-test',action='store_true');a=ap.parse_args();root=Path(a.root).resolve()
 tests=self_tests()
 if a.self_test:
  for i,x in enumerate(tests,1):print(f'RC{i:03d}|{"PASS" if x else "FAIL"}')
  print(f'R7_COMPAT_SELF_TESTS_REQUIRED=8\nR7_COMPAT_SELF_TESTS_EXECUTED=8\nR7_COMPAT_SELF_TESTS_PASS={sum(tests)}\nR7_COMPAT_SELF_TESTS_FAIL={8-sum(tests)}')
  return 0 if all(tests) else 1
 cp=subprocess.run([sys.executable,str(root/'Tests/Static/verify_hsb_2d_v1_r7.py'),'--root',str(root)],capture_output=True,text=True)
 passed,failed,metrics=parse(cp.stdout);files=protected(root);ok,unexpected,missing=evaluate(passed,failed,metrics,all(x[3] for x in files))
 print(f'R7_HISTORICAL_FULL_RESULT={"EXPECTED_FAIL" if cp.returncode else "PASS"}')
 print('R7_ACTUAL_FAILURE_IDS='+','.join(sorted(failed)));print('R7_UNEXPECTED_FAILURE_IDS='+','.join(sorted(unexpected)));print('R7_MISSING_REQUIRED_CORE_PASS_IDS='+','.join(sorted(missing)))
 for rel,old,cur,same in files: print(f'R7_PROTECTED|{rel}|{old}|{cur}|{"UNCHANGED" if same else "CHANGED"}')
 print(f'R7_PROTECTED_FILES_UNCHANGED={"YES" if all(x[3] for x in files) else "NO"}')
 print(f'R7_COMPAT_SELF_TESTS={sum(tests)}/8');print(f'R7_CURRENT_COMPAT_RESULT={"PASS" if ok and all(tests) else "FAIL"}')
 return 0 if ok and all(tests) else 1
if __name__=='__main__':raise SystemExit(main())
