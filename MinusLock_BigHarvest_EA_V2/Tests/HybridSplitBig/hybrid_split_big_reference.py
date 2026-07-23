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
