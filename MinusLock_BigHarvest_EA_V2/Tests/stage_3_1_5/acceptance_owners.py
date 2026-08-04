"""Независимые executable acceptance owners восьмой коррекции."""
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from decimal import Decimal as D
from stage_3_1_5_money_oracle import *
from stage_3_1_5_reference_oracle import *
from stage_3_1_5_mutation_oracle import *
from exploit_regressions import run as exploit_regressions
from replay_opening_attacks import run as replay_attacks
from corrupted_store_final_close import run as corrupted_gates
from counter_audit import audit
from causal_negative_controls import run as negative_controls
from source_guard import guards
KNOWN={'adaptive_geometry_set_files_check.py','big_monetary_recovery_model_check.py','big_scenario_parameter_search_check.py','clean_start_split_context_check.py','frozen_geometry_persistence_check.py','full_parameter_optimization_study_check.py','initial_lock_save_restore_check.py','partial_close_no_theoretical_lot_subtraction_check.py','phase_state_matrix_check.py','state_requires_resolved_position_check.py'}
def _deal_event_idempotency():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));d=Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5'));e=EconomicLedger(i,b);return e.apply(d) and not e.apply(d) and e.revision==1
def _event_idempotency():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));k=EventKey(1,'X',2,'C','H',1,'P','P',1,AllocationType.RESIDUAL);r=EventRecord(k);s=PersistentStore(EconomicLedger(i,b),AllocationLedger(i));return s.apply_event(r) and not s.apply_event(r)
def _opening():
 c=OpenPositionCost(D('1'),D('-10'));c.close(D('.4'),D('.4'),1);c.close(D('.6'),D('.6'),2);c.validate_integrity(Broker(D('1'),D('1'),D('.01'),D('1'),D('1')));return c.volume==c.unallocated_entry_cost==0 and c.allocated_entry_cost==D('-10')
def _standalone(root):
 files=sorted((root/'Tests').rglob('*_check.py'))
 def one(p):return p.name,subprocess.run([sys.executable,str(p)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=90).returncode
 with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(one,files))
 failures={n for n,c in results if c};return len(files)==181 and failures==KNOWN

def run(root,with_project=True,with_standalone=False):
 replay=replay_attacks();exploits=exploit_regressions();gates=corrupted_gates();mutations,causal,_=audit();negative=negative_controls();reference=calculate_reference(REFERENCE_SCENARIO,ReferenceBroker(D('1.1000'),D('1.1002'),D('.0001'),D('10'),D('12')),D('1.0990'))
 stage=subprocess.run([sys.executable,'-m','pytest','-q',str(root/'Tests'/'test_stage_3_1_5_money_model.py')],capture_output=True,text=True) if with_project else None
 project=subprocess.run([sys.executable,'-m','pytest','-q',str(root/'Tests')],capture_output=True,text=True) if with_project else None
 deal={k:v for k,v in replay.items() if k.startswith('ALTERED_DEAL_')};event={k:v for k,v in replay.items() if k.startswith('SAME_STATE_')}
 owners={
 'DEAL_REPLAY_IDEMPOTENCY':_deal_event_idempotency(),'DEAL_REPLAY_CONFLICT_DETECTION':len(deal)==12 and all(deal.values()),'EVENT_REPLAY_IDEMPOTENCY':_event_idempotency(),'EVENT_REPLAY_CONFLICT_DETECTION':len(event)==5 and all(event.values()),'OPENING_COST_PROPORTIONAL_ALLOCATION':_opening(),'OPENING_COST_RESTART_INTEGRITY':replay['OPENING_COST_ALLOCATION_ATTACK'],'OPENING_COST_BROKER_GRID':_opening(),'FINAL_CLOSE_CORRUPTED_OPENING_COST_REJECTION':any(x['name']=='OPENING_COST_PROPORTIONAL_DISTORTION' and x['passed'] for x in gates),'INDEPENDENT_REFERENCE_ORACLE':reference['projected']==D('10.00') and reference['realized']==D('14.00'),'REAL_FAULT_ADAPTER_EXECUTION':all(r.mutated_observables.fault_evidence and r.mutated_observables.fault_evidence.called and r.mutated_observables.fault_evidence.operation_accepted for r in mutations),'FAULT_BOUNDARY_DIGEST_PROOF':all(r.mutated_observables.fault_evidence.before_digest!=r.mutated_observables.fault_evidence.after_digest for r in mutations),'REAL_ALGORITHMIC_MUTATIONS':all(r.target_caught for r in mutations),'SEMANTIC_CAUSAL_AUDIT':all(v==0 for v in causal.values()),'NEGATIVE_CAUSAL_CONTROLS':all(negative[k]==0 for k in ('MISSING_CAUSAL_RULES','INEFFECTIVE_CAUSAL_RULES','VACUOUS_CAUSAL_RULES')),'STRICT_PERSISTENCE_SCHEMA':all(r['passed'] for r in exploits if r['name'] in ('UNKNOWN_TOP_LEVEL_FIELD','UNKNOWN_NESTED_FIELD','DUPLICATE_JSON_OBJECT_KEY')),'SOURCE_GUARDS':not any(guards().values()),'PYTEST_INTEGRATION':stage is None or stage.returncode==0,'PROJECT_REGRESSION':project is None or project.returncode==0,'STANDALONE_FAILURE_MANIFEST':not with_standalone or _standalone(root),'REPOSITORY_SCOPE':not subprocess.run(['bash','-lc',"git diff --name-only c9e1efa1717ed5afe812739b6aae5fa0a65298c0..HEAD | awk '!/^MinusLock_BigHarvest_EA_V2\\/(Docs|Tests|Tools)\\//'"],capture_output=True,text=True).stdout.strip(),'PRODUCTION_UNCHANGED':not subprocess.run(['bash','-lc',"git diff --name-only c9e1efa1717ed5afe812739b6aae5fa0a65298c0..HEAD | awk '/\\.(mq5|mqh|set)$/'"],capture_output=True,text=True).stdout.strip()}
 return owners,stage,project
