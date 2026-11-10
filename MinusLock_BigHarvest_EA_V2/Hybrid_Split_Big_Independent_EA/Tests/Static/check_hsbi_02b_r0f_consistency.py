#!/usr/bin/env python3
"""Executable ballot/schema/DAG/scope consistency checks; no administrative approval."""
import sys,json,hashlib
from pathlib import Path
import check_hsbi_02b_r0f_common as a
import hsbi_02b_r0f_decisions as proposals
import hsbi_02b_r0f_independent_fixtures as fixture

def topological(edges):
 nodes={n for e in edges for n in e};done=set()
 while len(done)<len(nodes):
  ready={n for n in nodes-done if all(u in done for u,v in edges if v==n)}
  if not ready:return False
  done|=ready
 return True

def main():
 started=a.now();folder=a.ROOT/'Tests/Contracts';admin=json.loads((folder/'NEXT_STAGE_02B_R0F_ADMIN_DECISIONS.json').read_text());matrix=json.loads((folder/'NEXT_STAGE_02B_R0F_CONTRACT_MATRIX.json').read_text());r1=json.loads((folder/'NEXT_STAGE_02B_R0F_R1_ACCEPTANCE_MATRIX.json').read_text());expected=('D-01','D-02','D-03','D-04','D-05','D-06','D-07','D-08','CR-09','NUM-EXACT-1','NUM-DOMAIN-1','NUM-CODEC','SNAP-FIXTURE-1','FUNDING-GLOBAL-ATTRIBUTION','MQL-DOMAIN','BALANCE-SCHEMA-MAPPING');rows=[]
 def check(i,actual,expected_value=True):rows.append(dict(TestID=i,Expected=expected_value,Actual=actual,Result='PASS' if actual==expected_value else 'FAIL'))
 required={'DecisionID','CurrentContract','Conflict','RecommendedChoice','AlternativeChoice','MathematicalJustification','Counterexample','ProductionImpact','MigrationImpact','Dependencies','RequiredEvidence','ApprovalReadiness','AdministratorDecision','ApprovalStatus','ShortApprovalStatement'}
 check('ADMIN-16',tuple(r['DecisionID'] for r in admin['Rows']),expected);check('ADMIN-COMPLETE-FIELDS',all(required<=set(r) and all(r[k] for k in required-{'AdministratorDecision','Dependencies'}) for r in admin['Rows']));check('ADMIN-NO-APPROVAL',all(r['AdministratorDecision']=='' and r['ApprovalStatus']=='AWAITING_ADMIN_APPROVAL' for r in admin['Rows']) and admin['Approved']==0)
 check('ADMIN-READINESS',all(r['ApprovalReadiness'] in ('SEMANTIC_CHOICE_READY','NEEDS_EXTERNAL_EVIDENCE','BLOCKED_BY_DEPENDENCY') for r in admin['Rows']))
 check('APPROVAL-DAG',topological(matrix['ApprovalDefinitionEdges']));check('RUNTIME-DAG',topological(matrix['RuntimeEvidenceEdges']));check('CYCLE-NEGATIVE-CONTROL',topological([('a','b'),('b','a')]),False)
 check('DEPENDENCIES-KNOWN',all(d in expected for row in admin['Rows'] for d in row['Dependencies']));check('D05-NOT-SELECTED',matrix['TransitionPolicySelected'] is None and 'НЕ ВЫБРАНО' in next(r for r in admin['Rows'] if r['DecisionID']=='D-05')['RecommendedChoice']);check('CODEC-NOT-SELECTED',matrix['CodecSelected'] is None)
 check('FIELD-ORDER',tuple(r['Field'] for r in matrix['EconomicFields']),fixture.ORDER);check('FIELD-IMMUTABLE',all(r['Required'] and r['ImmutableEquality'] and r['MayChangeDuringReconciliation'] is False and r['Authority'] and r['Migration'] and r['Serialization'] for r in matrix['EconomicFields']))
 check('SOURCE-KEY-FIELDS',[r['Field'] for r in matrix['EconomicFields'] if r['SourceKey']],['Broker','Server','AccountLogin','DealTicket']);check('TIMESTAMP-SIGNED', '2^63-1' in next(r['ExactType'] for r in matrix['EconomicFields'] if r['Field']=='TimestampMsc'))
 check('ALLOCATION-STATE-SEPARATED',not(set(matrix['AllocationImmutableFields'])&set(matrix['AllocationMutableState'])) and 'OriginalBucketGrants' in matrix['AllocationImmutableFields'] and 'Consumed' in matrix['AllocationMutableState'])
 check('MONEY-TYPE-REGISTRY',[r['Name'] for r in matrix['MoneyTypes']],['ProjectedBasketNet','ProjectedCloseNowNet','ActualRealizedDealNet','ReconciledEconomicNet','EligibleSourceGrant','AvailableReserve']);check('NO-IMPLICIT-CONVERSION',all(r['ImplicitConversionsAllowed'] is False for r in matrix['MoneyTypes']) and all(r['Spendability']=='NEVER_DIRECT' for r in matrix['MoneyTypes'] if r['Projected']))
 check('R1-SCOPE',r1['Variants'][0]['ProductionAllowlist'],['Include/Money/HSBI_EconomicLedgerTypes.mqh']);check('R1-NO-AUTHORIZATION',r1['R1_1_START_ALLOWED'] is False and all(v['ProductionImplementationAllowed'] is False for v in r1['Variants']));check('R1-CRITERIA',len(r1['Criteria']),20)
 check('EXTENDED-JUSTIFIED',len(r1['Variants'][1]['ProductionAllowlist'])==4 and 'not logically required' in r1['Variants'][1]['SingleFileFeasibility']);check('PROPOSED-DATA-MATCH',admin['Rows']==proposals.rows())
 out=dict(a.meta(__file__),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=a.now(),SourceInputs={str(p.relative_to(a.ROOT)):a.sha(p) for p in (Path(proposals.__file__),Path(fixture.__file__))},Rows=rows,Pass=sum(r['Result']=='PASS' for r in rows),Fail=sum(r['Result']=='FAIL' for r in rows));out['ExitCode']=int(out['Fail']>0);a.save('CONSISTENCY',out);print('CONSISTENCY',out['Pass'],out['Fail']);print([r for r in rows if r['Result']!='PASS']);return out['ExitCode']
if __name__=='__main__':raise SystemExit(main())
