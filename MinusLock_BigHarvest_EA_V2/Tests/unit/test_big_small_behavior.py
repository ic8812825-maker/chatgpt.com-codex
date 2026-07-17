from dataclasses import dataclass, field, replace
import math, random

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
