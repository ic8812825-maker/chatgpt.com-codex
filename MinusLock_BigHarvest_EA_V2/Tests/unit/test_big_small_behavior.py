from dataclasses import dataclass, field, replace
import math, random
import pytest

@dataclass
class Position:
    role: str
    lot: float
    pnl: float = 0.0

@dataclass
class Engine:
    far: float = 1.0
    reserve: float = 0.0
    carry: float = 0.0
    recovery: float = 0.0
    state: str = "BIG"
    positions: dict = field(default_factory=lambda: {"FAR": Position("FAR", 1.0)})
    ledger: list = field(default_factory=list)

    def open(self, role, lot, accepted=True, margin=10, free_margin=100):
        if not accepted or lot <= 0 or margin > free_margin or role in self.positions:
            return False
        self.positions[role] = Position(role, lot); return True

    def close(self, role, accepted=True, fill=1.0, net=0.0):
        if not accepted or role not in self.positions or not 0 < fill <= 1:
            return False
        p = self.positions[role]; actual = p.lot * fill
        p.lot -= actual; self.recovery += net
        if p.lot < 1e-9: del self.positions[role]
        return True

    def harvest(self, event, amount, reserve_share=.6):
        if any(row[0] == event for row in self.ledger): return False
        add = amount * reserve_share
        self.reserve += add; self.carry += amount - add
        self.ledger.append((event, amount, self.reserve)); return True

    def big_level(self, event, recovery_delta, far_loss_before, far_loss_after):
        before = (self.reserve + self.carry) / far_loss_before
        if self.state != "BIG" or recovery_delta <= 0: return False
        self.harvest(event, recovery_delta)
        after = (self.reserve + self.carry) / far_loss_after
        if after <= before: return False
        self.recovery += recovery_delta; return True

    def small(self, ratio, accepted=True):
        if self.state != "BIG" or not 0 < ratio < 1: return False
        self.state = "SMALL"
        target = math.floor(self.far * ratio * 100) / 100
        if not accepted or target <= 0 or target >= self.far:
            self.state = "SMALL_RECONCILIATION_FAILED"; return False
        self.far = target; self.positions["FAR"].lot = target; self.state = "BIG"; return True

    def restart(self):
        return replace(self, positions={k: replace(v) for k,v in self.positions.items()}, ledger=list(self.ledger))

def test_rejected_open_keeps_positions_and_state():
    e=Engine(); assert not e.open("CORE", 1.2, accepted=False); assert set(e.positions)=={"FAR"} and e.state=="BIG"

def test_margin_rejection_is_atomic():
    e=Engine(); before=e.restart(); assert not e.open("CORE", 1.2, margin=101); assert e.positions==before.positions

def test_rejected_close_does_not_realize_money():
    e=Engine(); assert not e.close("FAR", accepted=False, net=-20); assert e.recovery==0 and e.far==1

def test_partial_fill_uses_actual_volume():
    e=Engine(); assert e.close("FAR", fill=.25, net=-3); assert e.positions["FAR"].lot==.75 and e.recovery==-3

def test_restart_preserves_pending_phase_and_ledger():
    e=Engine(state="SMALL"); e.harvest(7,10); restored=e.restart(); assert restored.state=="SMALL" and restored.ledger==[(7,10,6)]

def test_harvest_is_exactly_once():
    e=Engine(); assert e.harvest(1,10); assert not e.harvest(1,10); assert (e.reserve,e.carry)==(6,4)

def test_big_requires_strict_recovery_and_coverage_growth():
    e=Engine(); assert e.big_level(1,10,10,15); assert e.recovery==10 and (e.reserve+e.carry)/15 > 0
    zero=Engine(); assert not zero.big_level(1,0,10,10)

def test_small_actual_far_compresses():
    e=Engine(); assert e.small(.9); assert e.far==.9 and e.positions["FAR"].lot==.9

def test_failed_small_enters_reconciliation_state():
    e=Engine(far=.01, positions={"FAR":Position("FAR",.01)}); assert not e.small(.97); assert e.state=="SMALL_RECONCILIATION_FAILED"

def test_false_reverse_cannot_open_second_tail():
    e=Engine(state="SMALL", positions={"FAR":Position("FAR",1),"REVERSE":Position("REVERSE",.5)})
    assert not e.open("REVERSE",.5) and len(e.positions)==2

def test_random_execution_sequences_preserve_nonnegative_accounting():
    random.seed(7)
    for _ in range(200):
        e=Engine(); amount=random.uniform(0,100); share=random.uniform(0,1); e.harvest(1,amount,share)
        assert e.reserve>=0 and e.carry>=0 and math.isclose(e.reserve+e.carry,amount)

def open_split_atomically(engine, legs, margins, free_margin, volume_limit):
    planned=sum(lot for _,lot in legs)
    if sum(margins)>free_margin or planned>volume_limit: return 0
    snapshot=engine.restart()
    for role,lot in legs:
        if not engine.open(role,lot,margin=0):
            engine.positions=snapshot.positions; return 0
    return len(legs)

def test_core_individually_valid_but_basket_margin_failure_opens_zero():
    e=Engine(); legs=[('CORE',.6),('TREND',.3),('BASE',.2)]
    assert 40<100 and sum([40,40,40])>100
    assert open_split_atomically(e,legs,[40,40,40],100,2)==0
    assert set(e.positions)=={'FAR'}

def test_directional_planned_volume_is_aggregated_before_open():
    e=Engine(); assert open_split_atomically(e,[('CORE',.7),('TREND',.5),('BASE',.2)],[1,1,1],100,1.0)==0

@dataclass
class HarvestTxn:
    phase: str='CALCULATED'; reserve: float=0; carry: float=0; ledger: list=field(default_factory=list)
    def resume(self,event,amount,reserve_add,carry_after):
        if self.phase=='CALCULATED': self.phase='LEDGER_PREPARED'
        if self.phase=='LEDGER_PREPARED':
            if event not in self.ledger: self.ledger.append(event); self.reserve+=reserve_add
            self.phase='LEDGER_WRITTEN'
        if self.phase=='LEDGER_WRITTEN': self.phase='RESERVE_UPDATED'
        if self.phase=='RESERVE_UPDATED': self.carry=carry_after; self.phase='CARRY_UPDATED'
        if self.phase=='CARRY_UPDATED': self.phase='DISTRIBUTED'
        return self

def test_harvest_resume_after_every_phase_is_exactly_once():
    phases=['CALCULATED','LEDGER_PREPARED','LEDGER_WRITTEN','RESERVE_UPDATED','CARRY_UPDATED','DISTRIBUTED']
    for crash in phases:
        tx=HarvestTxn(phase=crash)
        if crash in {'LEDGER_WRITTEN','RESERVE_UPDATED','CARRY_UPDATED','DISTRIBUTED'}: tx.ledger=[7];tx.reserve=6
        if crash in {'CARRY_UPDATED','DISTRIBUTED'}: tx.carry=4
        restored=replace(tx,ledger=list(tx.ledger)).resume(7,10,6,4).resume(7,10,6,4)
        assert restored.reserve==6 and restored.carry==4 and restored.ledger==[7]

def choose_false_reverse(options, minimum=1, margin_min=200):
    safe=[o for o in options if o['recovery']>=minimum and o['margin']>=margin_min and o['reserve_impact']<=0]
    return max(safe,key=lambda o:o['net'])['action'] if safe else 'MANUAL'

def test_false_reverse_selects_only_safe_best_money_option():
    options=[{'action':'WAIT','net':-2,'recovery':2,'margin':300,'reserve_impact':0}, {'action':'CLOSE_REVERSE','net':1,'recovery':3,'margin':300,'reserve_impact':0}, {'action':'CLOSE_ALL','net':5,'recovery':-1,'margin':300,'reserve_impact':0}]
    assert choose_false_reverse(options)=='CLOSE_REVERSE'

def test_false_reverse_uses_manual_when_no_option_safe():
    assert choose_false_reverse([{'action':'WAIT','net':1,'recovery':-2,'margin':300,'reserve_impact':0}])=='MANUAL'

def directional_snapshot(positions, magic, planned_buy, planned_sell):
    managed_buy=sum(p['lot'] for p in positions if p['symbol']=='X' and p['magic']==magic and p['side']=='BUY')
    managed_sell=sum(p['lot'] for p in positions if p['symbol']=='X' and p['magic']==magic and p['side']=='SELL')
    broker_buy=sum(p['lot'] for p in positions if p['symbol']=='X' and p['side']=='BUY')
    broker_sell=sum(p['lot'] for p in positions if p['symbol']=='X' and p['side']=='SELL')
    return managed_buy,managed_sell,broker_buy,broker_sell,planned_buy,planned_sell

def projected_margin(equity,current_margin,new_margin,commission,spread,slippage,buffers):
    projected_equity=equity-commission-spread-slippage-buffers
    projected_total_margin=current_margin+new_margin
    return projected_equity,projected_total_margin,projected_equity/projected_total_margin*100,projected_total_margin/projected_equity*100

def test_magic_volume_is_separate_from_broker_total_limit():
    positions=[{'symbol':'X','magic':7,'side':'BUY','lot':.2},{'symbol':'X','magic':8,'side':'BUY','lot':.5},{'symbol':'Y','magic':7,'side':'BUY','lot':9}]
    managed_buy,_,broker_buy,_,planned,_=directional_snapshot(positions,7,.4,0)
    assert managed_buy==.2 and broker_buy==.7 and broker_buy+planned>1

def test_projected_margin_includes_current_margin_and_open_costs():
    equity,margin,level,percent=projected_margin(1000,300,250,10,20,5,15)
    assert equity==950 and margin==550 and level==pytest.approx(172.7272727) and percent==pytest.approx(57.8947368)
    assert level<200

@dataclass
class SmallAudit:
    role:str; requested:float; filled:float; residual:float; net:float; completed:bool=True

def reconcile_small(audits, old_far, new_far, remaining_roles, reserve, ledger_reserve, tolerance=.005):
    required={'BIG_TREND','SMALL_BASE','REVERSE','OLD_FAR','BIG_CORE'}
    if {a.role for a in audits}!=required or len(audits)!=5:return False,0
    if any(not a.completed or abs(a.requested-a.filled)>tolerance for a in audits):return False,0
    by={a.role:a for a in audits}
    if any(by[r].residual>tolerance for r in ('BIG_TREND','SMALL_BASE','REVERSE','OLD_FAR')):return False,0
    if remaining_roles!={'NEW_FAR'} or not 0<new_far<old_far:return False,0
    if abs(by['BIG_CORE'].residual-new_far)>tolerance or abs(reserve-ledger_reserve)>.01:return False,0
    return True,sum(a.net for a in audits)

def valid_small_audits():
    return [SmallAudit('BIG_TREND',.2,.2,0,3),SmallAudit('SMALL_BASE',.3,.3,0,2),SmallAudit('REVERSE',.4,.4,0,1),SmallAudit('OLD_FAR',1,1,0,-4),SmallAudit('BIG_CORE',.3,.3,.7,5)]

def test_full_small_post_trade_reconciliation():
    ok,net=reconcile_small(valid_small_audits(),1,.7,{'NEW_FAR'},10,10)
    assert ok and net==7

def test_partial_old_far_and_core_mismatch_fail_reconciliation():
    audits=valid_small_audits();audits[3].filled=.8
    assert not reconcile_small(audits,1,.7,{'NEW_FAR'},10,10)[0]
    audits=valid_small_audits();audits[4].residual=.8
    assert not reconcile_small(audits,1,.7,{'NEW_FAR'},10,10)[0]

def test_orphan_and_ledger_mismatch_fail_small_reconciliation():
    assert not reconcile_small(valid_small_audits(),1,.7,{'NEW_FAR','ORPHAN'},10,10)[0]
    assert not reconcile_small(valid_small_audits(),1,.7,{'NEW_FAR'},10,9)[0]

def full_false_option(action, realized, closed, floating, reserve, current_margin, released, equity, exposure, second_tail=False):
    recovery=realized+closed+floating; impact=max(0,-closed); margin_after=max(0,current_margin-released); level=(equity+closed)/margin_after*100 if margin_after else 999999
    return {'action':action,'net':closed+floating,'recovery':recovery,'reserve_impact':impact,'margin':level,'margin_after':margin_after,'exposure':exposure,'second_tail':second_tail,'safe':recovery>=1 and impact<=reserve and level>=200 and not second_tail}

def test_false_reverse_options_recalculate_recovery_reserve_and_margin():
    wait=full_false_option('WAIT',5,0,-8,10,500,0,1000,1,True)
    close_tail=full_false_option('CLOSE_REVERSE',5,-2,4,10,500,120,1000,.4)
    close_all=full_false_option('CLOSE_ALL',5,-12,0,10,500,500,1000,0)
    assert not wait['safe'] and close_tail['safe'] and not close_all['safe']
    assert close_tail['reserve_impact']==2 and close_tail['margin_after']==380 and close_tail['recovery']==7

def false_reverse_fsm(action, reject_at=None):
    sequences={'CLOSE_REVERSE':['DECISION','CLOSE_REVERSE','RECONCILIATION','COMPLETED'], 'CLOSE_BASE':['DECISION','CLOSE_BASE','RECONCILIATION','COMPLETED'], 'CLOSE_TAILS':['DECISION','CLOSE_TAILS_REVERSE','CLOSE_TAILS_BASE','RECONCILIATION','COMPLETED'], 'CLOSE_BASKET':['DECISION','CLOSE_BASKET','RECONCILIATION','COMPLETED']}
    path=sequences[action]
    if reject_at in path:return path[:path.index(reject_at)+1]+['FAILED']
    return path

def test_false_reverse_actions_have_distinct_execution_paths():
    assert false_reverse_fsm('CLOSE_REVERSE')!=false_reverse_fsm('CLOSE_BASE')
    assert false_reverse_fsm('CLOSE_TAILS')[1:3]==['CLOSE_TAILS_REVERSE','CLOSE_TAILS_BASE']
    assert false_reverse_fsm('CLOSE_BASKET',reject_at='CLOSE_BASKET')[-1]=='FAILED'

def test_all_harvest_phases_resume_without_duplicate_side_effects():
    phases=['CALCULATED','LEDGER_PREPARED','LEDGER_WRITTEN','RESERVE_UPDATED','CARRY_UPDATED','DISTRIBUTED','CONSUMED']
    for phase in phases:
        tx=HarvestTxn(phase=phase)
        if phase in phases[2:]:tx.ledger=[9];tx.reserve=6
        if phase in phases[4:]:tx.carry=4
        first=replace(tx,ledger=list(tx.ledger)).resume(9,10,6,4)
        second=first.resume(9,10,6,4)
        assert second.ledger==[9] and second.reserve==6 and second.carry==4
