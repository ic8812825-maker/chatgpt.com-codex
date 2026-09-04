import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
C=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R12_PREDICATE_CONTRACT.json').read_text())['predicates'];R=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R12_PREDICATE_REGISTRY.json'
COVERAGE={x['predicateId']:x['exactInputPaths'] for x in C}
def main():
 reg=json.loads(R.read_text())['predicates'];find=[]
 for c,r in zip(C,reg):
  for k in ('predicateId','evaluationOrder','dataDependencies','exactInputPaths','prerequisitePredicates','failureCheckId','failureReason','passCondition','applicableScenarios'):
   if c[k]!=r[k]:find.append({'predicate':c['predicateId'],'field':k})
  if COVERAGE[c['predicateId']]!=c['exactInputPaths']:find.append({'predicate':c['predicateId'],'field':'evaluatorCoverage'})
 print(json.dumps({'R11_CONTRACT_EVALUATOR_ALIGNMENT':'PASS' if not find else 'FAIL','findings':find,'predicates':len(C)}));return 0 if not find else 1
if __name__=='__main__':raise SystemExit(main())
