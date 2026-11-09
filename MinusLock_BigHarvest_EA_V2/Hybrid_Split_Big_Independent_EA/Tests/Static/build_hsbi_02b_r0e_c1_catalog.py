#!/usr/bin/env python3
"""Required inventory derives from versioned executable specifications, NEVER result evidence."""
import ast,hashlib,json
from pathlib import Path
import check_hsbi_02b_r0e_c1_contracts as t
import check_hsbi_02b_r0e_c1_mutations as mu
ROOT=t.ROOT
CATALOG='Tests/Contracts/NEXT_STAGE_02B_R0E_C1_REQUIRED_CATALOG.json'
MATRIX='Tests/Contracts/NEXT_STAGE_02B_R0E_C1_VERIFICATION_MATRIX.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def expected_catalog():
 cases=t.cases();mutations=mu.catalog();functions={n.name:n.lineno for n in ast.walk(ast.parse((ROOT/mu.TARGET).read_text())) if isinstance(n,ast.FunctionDef)}
 tests=[]
 for c in cases:
  tests.append(dict(TestID=c['TestID'],GuardGroup=c['GuardID'],Operation=c['Operation'],SourceFile=mu.TARGET,SourceFunction=c['Operation'],SourceLine=functions[c['Operation']],TestFile=str(Path(t.__file__).relative_to(ROOT)),TestImplementation='cases',IndependentExpected=t.view(c['IndependentExpected']),Classes=c['Classes'],ProofBoundary='C1 PROPOSED fixture API only; no broker/durable/global-economic/NewFar evidence'))
 guards=[];ms=[];byid={c['TestID']:c for c in cases}
 for m in mutations:
  mid=m['MutationID'];gid=mid.replace('C1-MUT-','C1-GUARD-');neg=byid[m['NegativeTestID']]
  guards.append(dict(GuardID=gid,ContractID='C1-'+neg['GuardID'],SubjectFunction=m['TargetFunction'],PositiveTestID=m['PositiveTestID'],NegativeTestID=m['NegativeTestID'],MutationID=mid,ExpectedScope=neg['GuardID'],RedundantAllowed=m['KillClass']=='REDUNDANT_GUARD_SURVIVOR'))
  ms.append(dict(MutationID=mid,GuardID=gid,TargetFile=mu.TARGET,TargetFunction=m['TargetFunction'],PositiveTestID=m['PositiveTestID'],NegativeTestID=m['NegativeTestID'],ExactEdit=[dict(old=a,new=b,count=1) for a,b in m['Edits']],ExpectedVerdict=m['KillClass'],RedundancyProof=m['RedundancyProof']))
 pins={**t.hashes(),str(Path(mu.__file__).relative_to(ROOT)):sha(Path(mu.__file__)),str(Path(__file__).relative_to(ROOT)):sha(Path(__file__))}
 return dict(BaseSHA=t.BASE,CatalogVersion=t.CATALOG_VERSION,SourcePins=pins,RequiredTestIDs=[r['TestID'] for r in tests],RequiredGuardIDs=[r['GuardID'] for r in guards],RequiredMutationIDs=[r['MutationID'] for r in ms],Tests=tests,Guards=guards,Mutations=ms)
def canonical_digest(data):return hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def expected_matrix(cat=None):
 cat=cat or expected_catalog();cases=[]
 for c in cat['Tests']:
  r=dict(c);r['GuardIDs']=[g['GuardID'] for g in cat['Guards'] if c['TestID'] in (g['PositiveTestID'],g['NegativeTestID'])];r['MutationIDs']=[g['MutationID'] for g in cat['Guards'] if g['GuardID'] in r['GuardIDs']];r['EvidencePath']='Tests/Evidence/NEXT_STAGE_02B_R0E_C1_TEST_RESULTS.json#'+c['TestID'];cases.append(r)
 return dict(BaseSHA=t.BASE,CatalogVersion=cat['CatalogVersion'],CatalogDigest=canonical_digest(cat),ScenarioIDs=cat['RequiredTestIDs'],Cases=cases,Guards=cat['Guards'],ExternalDependencies=dict(GlobalEconomicFunding='UNPROVEN',BrokerAuthenticity='UNPROVEN',ProductionDurableEnforcement='UNPROVEN',FullNewFarIntegration='UNPROVEN'))
def main():
 c=expected_catalog();t.save(ROOT/CATALOG,c);t.save(ROOT/MATRIX,expected_matrix(c));print('CATALOG',len(c['Tests']),len(c['Guards']),len(c['Mutations']),canonical_digest(c))
if __name__=='__main__':main()
