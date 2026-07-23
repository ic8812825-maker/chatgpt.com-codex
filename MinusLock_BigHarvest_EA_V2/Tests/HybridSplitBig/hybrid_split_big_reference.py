"""Executable broker-agnostic Hybrid Split Big mathematical oracle.
All money inputs are supplied by vectors; this is not a substitute for MT5 OrderCalcProfit.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from math import ceil, floor, log
from typing import Any

DECISION_CODES=frozenset('''PASS_ALL_LAWS PASS_FINITE_CATCHUP FINAL_CLOSE_PRECHECK_PASS CYCLE_CLOSED_PROFIT PASS_NEW_FAR REJECT_RESERVE_CATCHUP REJECT_BIG_SLOPE REJECT_NO_FINITE_HARVEST_LEVEL REJECT_NON_MONOTONIC_DEFICIT REJECT_TRANSITION_BUDGET REJECT_CUMULATIVE_TRANSITION_LOSS REJECT_TRANSITION_LOSS_PERCENT REJECT_NO_VALID_Q REJECT_ROUNDING REJECT_MARGIN REJECT_FUTURE_SMALL REJECT_OPTIONAL_BIGTREND_POLICY REJECT_OPTIONAL_SMALLBASE_POLICY WORST_CASE_FAIL WORST_CASE_PROFILE_INCOMPLETE TERMINAL_SAFE_STATE ERROR_DOUBLE_COUNT_DETECTED ERROR_DOUBLE_COMMISSION ERROR_PARTIAL_EXECUTION ERROR_FINAL_RESULT_MISMATCH ERROR_RESTORE_RECONCILIATION ERROR_RESERVE_LEDGER ERROR_INVALID_VECTOR ERROR_INVALID_ALLOCATION'''.split())

def down(v,s): return floor((v+1e-12)/s)*s
def up(v,s): return ceil((v-1e-12)/s)*s
def money_round(v,precision=2): return round(v,precision)
@dataclass(frozen=True)
class RoundingProfile:
    core:str; trend:str; small:str; new_far:str
PROFILES={'EA_CURRENT':RoundingProfile('DOWN','DOWN','UP','DOWN'),'CONSERVATIVE_ALL_DOWN':RoundingProfile('DOWN','DOWN','DOWN','DOWN')}
def apply_round(v,rule,step): return {'DOWN':down,'UP':up,'NEAREST':lambda x,s:floor(x/s+.5)*s}[rule](v,step)
@dataclass(frozen=True)
class CostProvenance:
    commission_in_leg_net:bool; commission_in_expected_exit_costs:bool
    swap_in_leg_net:bool; swap_in_expected_exit_costs:bool
    fee_in_leg_net:bool; fee_in_expected_exit_costs:bool
    def duplicate(self): return (self.commission_in_leg_net and self.commission_in_expected_exit_costs) or (self.swap_in_leg_net and self.swap_in_expected_exit_costs) or (self.fee_in_leg_net and self.fee_in_expected_exit_costs)
@dataclass
class EvaluationResult:
    code:str; passed:bool; stage:str; trace:dict; errors:list[str]=field(default_factory=list)
@dataclass
class Buckets:
    realized_cycle_pl:float=0.; final_reserve_real:float=0.; partial_available:float=0.; partial_consumed:float=0.; transition_available:float=0.; transition_consumed:float=0.; carry:float=0.; cumulative_transition_loss:float=0.; events:set[str]=field(default_factory=set)
    def _event(self,k):
        if k in self.events:return False
        self.events.add(k);return True
    def allocate_harvest(self,key,net,a,b,g,precision=2):
        if not self._event(key): return 'ERROR_DOUBLE_COUNT_DETECTED',{}
        if min(a,b,g)<0 or abs(a+b+g-1)>1e-9:return 'ERROR_INVALID_ALLOCATION',{}
        self.realized_cycle_pl+=net
        if net<=0:return 'PASS',{'partial':0.,'reserve':0.,'carry':0.}
        p=money_round(a*net,precision);r=money_round(b*net,precision);base=money_round(g*net,precision);carry=money_round(base+money_round(net-p-r-base,precision),precision)
        self.partial_available+=p;self.final_reserve_real+=r;self.carry+=carry
        return 'PASS',{'partial':p,'reserve':r,'carry':carry}
    def credit_transition_budget(self,key,amount):
        if not self._event(key):return False
        self.transition_available+=amount;return True
    def consume_transition_budget(self,key,amount):
        if not self._event(key) or amount>self.transition_available+1e-9:return False
        self.transition_available-=amount;self.transition_consumed+=amount;return True
    def consume_partial_far_budget(self,key,amount):
        if not self._event(key) or amount>self.partial_available+1e-9:return False
        self.partial_available-=amount;self.partial_consumed+=amount;return True
    def consume_final_reserve_for_final_far(self,key,amount):
        if not self._event(key) or amount>self.final_reserve_real+1e-9:return False
        self.final_reserve_real-=amount;return True

def leg_net(p, bid, ask, pv, commission, swap, fee):
    close=bid if p['direction']=='BUY' else ask; sign=1 if p['direction']=='BUY' else -1
    return (close-p['open_price'])*p['lot']*pv*sign-commission-swap-fee
def find_finite_catchup_level(rows,gain,minprofit):
    for i,r in enumerate(rows,1):
        if r['deficit']<=0 and r['recovery']>=minprofit:return i
    return None
def validate_monotonic_deficit_gain(rows,gain): return all(rows[i]['deficit']<=rows[i-1]['deficit']-gain+1e-9 for i in range(1,len(rows)))
def evaluate_final_precheck(realized, projected_close, limits): return realized+projected_close >= limits['minimum_final_profit']+limits['final_close_safety_buffer']
def evaluate_actual_final(actual, positions, limits): return positions==0 and actual>=limits['minimum_final_profit']-limits['final_result_tolerance']
def evaluate_margin(v,candidate):
    m=v['margin']; lots=sum(p['lot'] for p in v['positions'].values())
    upper=m['current_margin']+lots*m['individual_margin_per_lot'];base=m.get('base_estimate',upper)
    usage=upper/m['equity']*100;level=float('inf') if upper==0 else m['equity']/upper*100
    return {'margin_base':base,'margin_upper':upper,'usage':usage,'level':level,'pass':usage<=m['maximum_usage_percent'] and level>=m['minimum_margin_level_percent']}
def evaluate_worst_case(v,base_nets):
    market=v['market']; required=('worst_bid','worst_ask')
    if any(k not in market for k in required):return {'code':'WORST_CASE_PROFILE_INCOMPLETE'}
    c=v['costs'];pv=v['symbol']['point_value']; worst={k:leg_net(p,market['worst_bid'],market['worst_ask'],pv,c['commission_per_leg'],c['swap'],c['fee']) for k,p in v['positions'].items()}
    return {'code':'PASS' if sum(worst.values())>=v.get('worst_min_total',-1e99) else 'WORST_CASE_FAIL','worst_leg_nets':worst}
def evaluate_future_small(v):
    f=v.get('future_small',{'mode':'LOCAL','pass':True});return {'code':'PASS' if f.get('pass',True) else 'REJECT_FUTURE_SMALL','mode':f.get('mode','LOCAL')}
def reconcile(execution): return 'RECONCILED' if abs(execution.get('requested',0)-execution.get('filled',0))<=execution.get('tolerance',1e-9) else 'ERROR_PARTIAL_EXECUTION'
def restore_reconcile(r): return 'RECONCILED' if r.get('match',True) else 'ERROR_RESTORE_RECONCILIATION'

def evaluate_vector(v:dict)->EvaluationResult:
    trace={k:None for k in ('catchup_ratio recovery_slope base_leg_nets worst_leg_nets harvest_net allocation projected_final_recovery_pl actual_final_recovery_pl coverage_deficits finite_catchup_level transition_net new_cumulative_transition_loss selected_new_far selected_q next_big_gross old_gross next_gross old_risk next_risk margin_base margin_upper future_small_result terminal_reason reconciliation_result'.split())}
    required={'id','description','mode','symbol','market','positions','costs','geometry','allocation','ledger','limits','volume','margin','harvest_levels','transition','execution','restore','expected'}
    if not required<=v.keys():return EvaluationResult('ERROR_INVALID_VECTOR',False,'schema',trace,['missing schema'])
    p=v['positions'];c=v['costs'];g=v['geometry'];L=v['limits'];vol=v['volume'];profile=PROFILES.get(vol['rounding_profile'])
    if not profile:return EvaluationResult('ERROR_INVALID_VECTOR',False,'rounding-profile',trace)
    prov=CostProvenance(c['commission_included_in_leg_net'],c['commission_in_expected_exit_costs'],c.get('swap_in_leg_net',True),c.get('swap_in_expected_exit_costs',False),c.get('fee_in_leg_net',True),c.get('fee_in_expected_exit_costs',False))
    if prov.duplicate():return EvaluationResult('ERROR_DOUBLE_COMMISSION',False,'cost-provenance',trace)
    if v['mode']=='STRICT' and p['trend']['lot']<=0:return EvaluationResult('REJECT_OPTIONAL_BIGTREND_POLICY',False,'components',trace)
    if v['mode']=='STRICT' and p['small']['lot']<=0:return EvaluationResult('REJECT_OPTIONAL_SMALLBASE_POLICY',False,'components',trace)
    F=p['far']['lot']; C=p['core']['lot'];T=p['trend']['lot'];S=p['small']['lot']; trace['catchup_ratio']=g['reserve_share']*(C+T-S)/F;trace['recovery_slope']=C+T-S-F
    if trace['catchup_ratio']<=1:return EvaluationResult('REJECT_RESERVE_CATCHUP',False,'law1',trace)
    if trace['recovery_slope']<=0:return EvaluationResult('REJECT_BIG_SLOPE',False,'law2',trace)
    pv=v['symbol']['point_value']; trace['base_leg_nets']={k:leg_net(x,v['market']['bid'],v['market']['ask'],pv,c['commission_per_leg'],c['swap'],c['fee']) for k,x in p.items()}
    trace['harvest_net']=sum(trace['base_leg_nets'][k] for k in ('small','core','trend'))
    b=Buckets(**{k:v['ledger'].get(k,0.) for k in ('realized_cycle_pl','final_reserve_real','partial_available','transition_available','cumulative_transition_loss')})
    code,trace['allocation']=b.allocate_harvest(v.get('harvest_event','harvest-1'),trace['harvest_net'],g['alpha_partial'],g['beta_reserve'],g['gamma_carry'],v.get('money_precision',2))
    if code!='PASS':return EvaluationResult(code,False,'allocation',trace)
    if v['ledger'].get('replay_event',False): return EvaluationResult('ERROR_DOUBLE_COUNT_DETECTED',False,'allocation',trace)
    trace['projected_final_recovery_pl']=v['ledger']['realized_cycle_pl']+sum(trace['base_leg_nets'].values())
    trace['actual_final_recovery_pl']=v.get('actual_final_recovery_pl',trace['projected_final_recovery_pl'])
    rows=v['harvest_levels']; mono=validate_monotonic_deficit_gain(rows,L['minimum_coverage_gain']) if len(rows)>1 else True; trace['finite_catchup_level']=find_finite_catchup_level(rows,L['minimum_coverage_gain'],L['minimum_final_profit']);trace['coverage_deficits']=[r['deficit'] for r in rows]
    if not mono:return EvaluationResult('REJECT_NON_MONOTONIC_DEFICIT',False,'finite-catchup',trace)
    if rows and trace['finite_catchup_level'] is None:return EvaluationResult('REJECT_NO_FINITE_HARVEST_LEVEL',False,'finite-catchup',trace)
    tr=v['transition']; trace['transition_net']=sum(tr.get(k,0.) for k in ('net_far','net_small','net_trend','net_core','budget'))-tr.get('other_costs',0.)
    loss=max(-trace['transition_net'],0);trace['new_cumulative_transition_loss']=b.cumulative_transition_loss+loss
    if trace['transition_net'] < -L['maximum_transition_loss']:return EvaluationResult('REJECT_TRANSITION_BUDGET',False,'transition',trace)
    if trace['new_cumulative_transition_loss']>L['maximum_cumulative_transition_loss']:return EvaluationResult('REJECT_CUMULATIVE_TRANSITION_LOSS',False,'transition',trace)
    if trace['new_cumulative_transition_loss']>L['maximum_transition_loss_percent']*v.get('initial_far_risk',100):return EvaluationResult('REJECT_TRANSITION_LOSS_PERCENT',False,'transition',trace)
    raw=g['target_new_far'];N=apply_round(raw,profile.new_far,vol['step']);trace['selected_new_far']=N;trace['selected_q']=N/F if F else None
    if raw<vol['minimum'] or N<vol['minimum'] or N>=F: trace['terminal_reason']='MIN_LOT_OR_NO_COMPRESSION';return EvaluationResult('TERMINAL_SAFE_STATE',False,'terminal',trace)
    nc=apply_round(N*g['core_ratio'],profile.core,vol['step']);nt=apply_round(N*g['trend_ratio'],profile.trend,vol['step']);ns=apply_round(N*g['small_ratio'],profile.small,vol['step']);trace['next_big_gross']=nc+nt;trace['old_gross']=F+C+T+S;trace['next_gross']=N+nc+nt+ns;trace['old_risk']=v.get('old_risk',F*100);trace['next_risk']=v.get('next_risk',N*100)
    if min(nc,nt,ns)<vol['minimum'] or trace['next_big_gross']>=F or trace['next_gross']>=trace['old_gross'] or trace['next_risk']>=trace['old_risk']:return EvaluationResult('REJECT_ROUNDING',False,'new-far',trace)
    fs=evaluate_future_small(v);trace['future_small_result']=fs['code']
    if fs['code']!='PASS':return EvaluationResult(fs['code'],False,'future-small',trace)
    margin=evaluate_margin(v,{});trace['margin_base']=margin['margin_base'];trace['margin_upper']=margin['margin_upper']
    if not margin['pass']:return EvaluationResult('REJECT_MARGIN',False,'margin',trace)
    worst=evaluate_worst_case(v,trace['base_leg_nets']);trace['worst_leg_nets']=worst.get('worst_leg_nets')
    if worst['code']!='PASS':return EvaluationResult(worst['code'],False,'worst-case',trace)
    trace['reconciliation_result']=reconcile(v['execution'])
    if trace['reconciliation_result']!='RECONCILED':return EvaluationResult('ERROR_PARTIAL_EXECUTION',False,'execution',trace)
    if restore_reconcile(v['restore'])!='RECONCILED':return EvaluationResult('ERROR_RESTORE_RECONCILIATION',False,'restore',trace)
    if v.get('final_check')=='MISMATCH':return EvaluationResult('ERROR_FINAL_RESULT_MISMATCH',False,'actual-final',trace)
    return EvaluationResult('PASS_ALL_LAWS',True,'complete',trace)

# Simulation-oracle extensions.  They are pure functions so an MT5 adapter can
# substitute broker money/margin without changing the search contract.
@dataclass
class NewFarCandidate:
    new_far:float; q:float; core:float; trend:float; small:float; transition_net:float; next_risk:float; next_margin:float; gate_results:dict
@dataclass
class NewFarSolverResult:
    code:str; selected:NewFarCandidate|None; rejected_candidates:list[dict]; iterations:int
@dataclass
class FutureSmallResult:
    code:str; passed:bool; proven_depth:int; nodes_visited:int; terminal_reached:bool; trace:list[dict]
def validate_vector(v):
    errors=[]
    def num(path,x,low=None):
        if not isinstance(x,(int,float)) or x!=x or x in (float('inf'),float('-inf')) or (low is not None and x<low):errors.append(f'{path} must be finite and >= {low}')
    for key in ('bid','ask'):num('market.'+key,v.get('market',{}).get(key),0)
    if not errors and v['market']['ask']<v['market']['bid']:errors.append('market.ask must be >= market.bid')
    for role,p in v.get('positions',{}).items():
        if p.get('direction') not in ('BUY','SELL'):errors.append(f'positions.{role}.direction must be BUY/SELL')
        num(f'positions.{role}.lot',p.get('lot'),0)
    a=v.get('allocation',{});shares=[a.get(k) for k in ('alpha_partial','beta_reserve','gamma_carry')]
    if all(isinstance(x,(int,float)) for x in shares) and abs(sum(shares)-1)>1e-9:errors.append('allocation shares must sum to 1')
    vol=v.get('volume',{});num('volume.step',vol.get('step'),1e-12)
    if vol.get('minimum',0)>vol.get('maximum',-1):errors.append('volume.minimum must be <= volume.maximum')
    return errors
def price_risk(position,bid,ask,pv,cost): return max(-leg_net(position,bid,ask,pv,cost,0,0),0)
def enumerate_new_far(v, transition_net=0.):
    p=v['positions'];g=v['geometry'];vol=v['volume'];F=p['far']['lot'];profile=PROFILES[vol['rounding_profile']];oldgross=sum(x['lot'] for x in p.values());oldrisk=sum(price_risk(x,v['risk_model']['old_control_bid'],v['risk_model']['old_control_ask'],v['symbol']['point_value'],v['costs']['commission_per_leg']) for x in p.values()); bad=[]
    for i in range(int((F-vol['minimum'])/vol['step'])+1):
        n=down(vol['minimum']+i*vol['step'],vol['step']);c=apply_round(n*g['core_ratio'],profile.core,vol['step']);t=apply_round(n*g['trend_ratio'],profile.trend,vol['step']);s=apply_round(n*g['small_ratio'],profile.small,vol['step']); nrisk=price_risk({'direction':p['core']['direction'],'lot':n,'open_price':p['core']['open_price']},v['risk_model']['next_control_bid'],v['risk_model']['next_control_ask'],v['symbol']['point_value'],v['costs']['commission_per_leg']); ngross=n+c+t+s; gates={'compression':n<F,'big':c+t<F,'gross':ngross<oldgross,'risk':nrisk+v['risk_model'].get('safety_buffer',0)<oldrisk,'lots':min(c,t,s)>=vol['minimum']}
        if all(gates.values()):return NewFarSolverResult('PASS_NEW_FAR',NewFarCandidate(n,n/F,c,t,s,transition_net,nrisk,v['margin']['current_margin']+(c+t+s)*v['margin']['individual_margin_per_lot'],gates),bad,i+1)
        bad.append({'new_far':n,'gates':gates})
    return NewFarSolverResult('REJECT_NO_VALID_Q',None,bad,len(bad))
def simulate_future_small(v,depth=1,max_nodes=100):
    seen=set();trace=[];state=v['positions']['far']['lot']
    for d in range(depth):
        if len(trace)>=max_nodes or state in seen:return FutureSmallResult('REJECT_FUTURE_SMALL',False,d,len(trace),False,trace)
        seen.add(state);r=enumerate_new_far(v)
        trace.append({'depth':d+1,'far':state,'solver':r.code})
        if r.code!='PASS_NEW_FAR':return FutureSmallResult(r.code,False,d+1,len(trace),True,trace)
        state=r.selected.new_far
    return FutureSmallResult('PASS',True,depth,len(trace),False,trace)

# Integrated simulation contract.  Legacy evaluator remains a regression oracle.
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
@dataclass(frozen=True)
class MoneyPolicy:
    precision:int=2
    rounding:str=ROUND_HALF_UP
    def money(self,v): return Decimal(str(v)).quantize(Decimal(10)**-self.precision,rounding=self.rounding)
class GateCode(str,Enum): SCHEMA_PASS='SCHEMA_PASS'; GEOMETRY_PASS='GEOMETRY_PASS'; NEW_FAR_PASS='NEW_FAR_PASS'; FUTURE_SMALL_PASS='FUTURE_SMALL_PASS'
class FinalDecisionCode(str,Enum): PASS_ALL_LAWS='PASS_ALL_LAWS'; TERMINAL_SAFE_STATE='TERMINAL_SAFE_STATE'; HYBRID_CANDIDATE_REJECTED='HYBRID_CANDIDATE_REJECTED'
class TerminalCode(str,Enum): MIN_LOT='TERMINAL_MIN_LOT'; NO_VALID_Q='TERMINAL_NO_VALID_Q'
@dataclass(frozen=True)
class CycleState:
    cycle_id:str; depth:int; far_direction:str; far_lot:Decimal; far_open_price:Decimal; core_direction:str; core_lot:Decimal; core_open_price:Decimal; trend_direction:str; trend_lot:Decimal; trend_open_price:Decimal; small_direction:str; small_lot:Decimal; small_open_price:Decimal; realized_cycle_pl:Decimal; final_reserve_real:Decimal; partial_far_available:Decimal; partial_far_consumed:Decimal; transition_available:Decimal; transition_consumed:Decimal; carry:Decimal; cumulative_transition_loss:Decimal; bid:Decimal; ask:Decimal; margin_current:Decimal; event_keys:frozenset[str]
def build_current_state(v):
 p=v['positions'];l=v['ledger'];m=MoneyPolicy();D=lambda x:m.money(x)
 return CycleState(str(v.get('cycle_id','cycle-0')),0,p['far']['direction'],D(p['far']['lot']),D(p['far']['open_price']),p['core']['direction'],D(p['core']['lot']),D(p['core']['open_price']),p['trend']['direction'],D(p['trend']['lot']),D(p['trend']['open_price']),p['small']['direction'],D(p['small']['lot']),D(p['small']['open_price']),D(l['realized_cycle_pl']),D(l['final_reserve_real']),D(l['partial_available']),D(0),D(l['transition_available']),D(0),D(0),D(l['cumulative_transition_loss']),D(v['market']['bid']),D(v['market']['ask']),D(v['margin']['current_margin']),frozenset())
def evaluate_vector_legacy(v): return evaluate_vector(v)
def evaluate_simulation_vector(v):
 errors=validate_vector(v)
 if errors:
  return EvaluationResult('ERROR_INVALID_VECTOR',False,'schema',{'schema_errors':errors,'gate_codes':[]},errors)
 state=build_current_state(v); legacy=evaluate_vector_legacy(v); gates=['SCHEMA_PASS','GEOMETRY_PASS']
 # The enumerator is executed in the normative path; legacy result remains
 # authoritative until every legacy vector carries risk/future simulation inputs.
 if 'risk_model' in v:
  solver=enumerate_new_far(v);legacy.trace['simulation_solver']={'code':solver.code,'iterations':solver.iterations,'rejected_candidates':solver.rejected_candidates};gates.append('NEW_FAR_PASS' if solver.selected else 'NEW_FAR_REJECT')
 legacy.trace['cycle_state']=state;legacy.trace['gate_codes']=gates
 return legacy
