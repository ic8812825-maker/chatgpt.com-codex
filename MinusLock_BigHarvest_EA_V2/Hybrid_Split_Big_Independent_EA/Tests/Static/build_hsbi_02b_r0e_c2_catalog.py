#!/usr/bin/env python3
"""Independent C2 executable catalog; never infer required inventory from result rows."""
import ast,hashlib,json
from pathlib import Path
import check_hsbi_02b_r0e_c2_contracts as t
import check_hsbi_02b_r0e_c2_mutations as mu
CATALOG='Tests/Contracts/NEXT_STAGE_02B_R0E_C2_REQUIRED_CATALOG.json';MATRIX='Tests/Contracts/NEXT_STAGE_02B_R0E_C2_VERIFICATION_MATRIX.json';SCHEMAS='Tests/Contracts/NEXT_STAGE_02B_R0E_C2_DTO_SCHEMAS.json';VERSION='HSBI-C2-REQUIRED-1'
def canonical_digest(d):return hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def expected_catalog():
 tests=[]
 for c in t.cases():
  file=t.SCHEMA if c['Operation']=='validate' else 'Tests/Reference/hsbi_02b_r0e_c2_evidence.py' if c['Operation']=='loads' else t.TARGET
  funcs={n.name:n.lineno for n in ast.walk(ast.parse((t.ROOT/file).read_text())) if isinstance(n,ast.FunctionDef)}
  tests.append(dict(TestID=c['TestID'],GuardGroup=c['GuardID'],Operation=c['Operation'],SourceFile=file,SourceFunction=c['Operation'],SourceLine=funcs[c['Operation']],TestFile='Tests/Static/check_hsbi_02b_r0e_c1_contracts.py' if c['TestID'].startswith('C2-BASE-') else 'Tests/Static/check_hsbi_02b_r0e_c2_contracts.py',TestImplementation='cases',IndependentExpected=t.view(c['IndependentExpected']),Classes=c['Classes'],ProofBoundary='C2 DTO/fixture composition; no broker/durable/global funding proof'))
 guards=[];mutations=[]
 for m in mu.catalog():
  gid=m['MutationID'].replace('MUT','GUARD');guards.append(dict(GuardID=gid,ClauseID=m['MutationID'],ContractID='C2-SCHEMA-AND-BINDING',SubjectFunction=m['TargetFunction'],PositiveTestID=m['PositiveTestID'],NegativeTestID=m['NegativeTestID'],MutationID=m['MutationID'],ExpectedScope='causal public API or mathematical schema helper',RedundancyProof=m['RedundancyProof']))
  mutations.append(dict(MutationID=m['MutationID'],GuardID=gid,TargetFile=m['TargetFile'],TargetFunction=m['TargetFunction'],PositiveTestID=m['PositiveTestID'],NegativeTestID=m['NegativeTestID'],ExactEdit=[dict(old=a,new=b) for a,b in m['Edits']],ExpectedVerdict='REDUNDANT_GUARD_SURVIVOR' if m['RedundancyProof'] else 'KILL',RedundancyProof=m['RedundancyProof']))
 pins={**t.hashes(),str(Path(mu.__file__).relative_to(t.ROOT)):t.sha(Path(mu.__file__)),str(Path(__file__).relative_to(t.ROOT)):t.sha(Path(__file__))}
 return dict(BaseSHA=t.BASE,CatalogVersion=VERSION,SourcePins=pins,RequiredTestIDs=[c['TestID'] for c in tests],RequiredSchemaProbeIDs=[s['TestID'] for s in t.schema_specs()],RequiredGuardIDs=[g['GuardID'] for g in guards],RequiredMutationIDs=[m['MutationID'] for m in mutations],Tests=tests,Guards=guards,Mutations=mutations,SchemaProbeSpecDigest=canonical_digest(t.view(t.schema_specs())))
def expected_matrix(cat=None):
 cat=cat or expected_catalog();rows=[]
 for c in cat['Tests']:
  r=dict(c);r['GuardIDs']=[g['GuardID'] for g in cat['Guards'] if c['TestID'] in (g['PositiveTestID'],g['NegativeTestID'])];r['MutationIDs']=[g['MutationID'] for g in cat['Guards'] if g['GuardID'] in r['GuardIDs']];r['EvidencePath']='Tests/Evidence/NEXT_STAGE_02B_R0E_C2_TEST_RESULTS.json#'+c['TestID'];rows.append(r)
 return dict(BaseSHA=t.BASE,CatalogVersion=VERSION,CatalogDigest=canonical_digest(cat),ScenarioIDs=cat['RequiredTestIDs'],SchemaProbeIDs=cat['RequiredSchemaProbeIDs'],Cases=rows,Guards=cat['Guards'],ExternalDependencies=dict(GlobalEconomicFunding='UNPROVEN',BrokerAuthenticity='UNPROVEN',ProductionDurableEnforcement='UNPROVEN',FullNewFarIntegration='UNPROVEN'))
def main():
 cat=expected_catalog();t.save(t.ROOT/CATALOG,cat);t.save(t.ROOT/MATRIX,expected_matrix(cat));t.save(t.ROOT/SCHEMAS,t.schema.inventory());print('catalog',len(cat['Tests']),len(cat['Guards']),len(cat['RequiredSchemaProbeIDs']))
if __name__=='__main__':main()
