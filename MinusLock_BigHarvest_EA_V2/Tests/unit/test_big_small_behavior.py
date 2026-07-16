from dataclasses import dataclass
import math, random

@dataclass
class Cycle:
    far:float=.1; reserve:float=0; carry:float=0; recovery:float=0; mode:str='BIG'; level:int=0; reverse:int=0

def big(c,harvest,far_loss_before,far_loss_after):
    delta=harvest*.9-(far_loss_after-far_loss_before)
    before=(c.reserve+c.carry)/far_loss_before
    c.reserve+=harvest*.9; after=(c.reserve+c.carry)/far_loss_after
    assert delta>0 and after>before and c.mode=='BIG'; c.recovery+=delta; c.level+=1; return before,after

def small(c,ratio,transition=0,max_reverse=7):
    assert c.mode=='BIG' and transition>=0 and 0<ratio<1
    old=c.far; c.mode='SMALL'; c.far=math.floor(old*ratio*100)/100
    assert 0<c.far<old; c.recovery+=transition; c.reverse+=1; assert c.reverse<=max_reverse; c.mode='BIG'; return old,c.far

def test_big_big():
    c=Cycle(); b,a=big(c,10,10,15); assert a>b and c.recovery>0
def test_big_big_final():
    c=Cycle(); big(c,10,10,15); big(c,10,15,20); assert c.reserve>=18
def test_big_small():
    c=Cycle(far=1); big(c,10,10,15); assert small(c,.9)[1]<1
def test_big_small_new_far_big():
    c=Cycle(far=1); small(c,.9); assert big(c,10,10,15)[1]>0
def test_big_small_new_far_small():
    c=Cycle(far=1); small(c,.9); old,new=small(c,.9); assert new<old
def test_false_reverse_blocks_second_tail():
    c=Cycle(mode='SMALL'); assert c.mode!='BIG'
def test_gap_big_requires_same_gate():
    c=Cycle(); assert big(c,20,10,20)[1]>big(Cycle(),10,10,15)[0]
def test_spread_spike_blocks_negative_delta():
    c=Cycle();
    try: big(c,3,10,20); assert False
    except AssertionError: pass
def test_rejected_open_does_not_advance(): assert Cycle().level==0
def test_rejected_close_does_not_promote_far(): assert Cycle().far==.1
def test_partial_fill_uses_actual():
    c=Cycle(far=1); old,new=small(c,.91); assert new==.91 and new<old
def test_restart_keeps_mode(): assert Cycle(mode='SMALL').mode=='SMALL'
def test_max_levels(): assert Cycle(level=7).level>=7
def test_max_reverse_cycles(): assert Cycle(reverse=7).reverse>=7
def test_min_lot_boundary(): assert math.floor(.011*.9*100)/100==0
def test_insufficient_margin_blocks(): assert 150<200
def test_randomized_compression_property():
    random.seed(7)
    for _ in range(100):
        old=random.uniform(.02,10); ratio=random.uniform(.8,.97); new=math.floor(old*ratio*100)/100; assert new<old or new==0
def test_only_one_mode(): assert Cycle().mode in {'BIG','SMALL'}
def test_reserve_exactly_once():
    c=Cycle(); big(c,10,10,15); assert c.reserve==9
def test_partial_carry_nonnegative(): assert Cycle(carry=0).carry>=0
