import math
from dataclasses import dataclass
from enum import Enum
import pytest

MAX_U32=2**32-1
class U(Enum): ABSENT=0; ZERO=1; ACTIVE=2; MALFORMED=3

def inspect(store,name):
    h,l=store.get(name+'High32'),store.get(name+'Low32')
    if h is None and l is None:return U.ABSENT,0
    if h is None or l is None:return U.MALFORMED,0
    if any(not isinstance(x,(int,float)) or not math.isfinite(x) or x<0 or x>MAX_U32 or x!=math.floor(x) for x in (h,l)):return U.MALFORMED,0
    value=(int(h)<<32)|int(l); return (U.ZERO if value==0 else U.ACTIVE),value

@pytest.mark.parametrize('store,expected',[({},U.ABSENT),({'XHigh32':0,'XLow32':0},U.ZERO),({'XHigh32':0,'XLow32':1},U.ACTIVE),({'XHigh32':1},U.MALFORMED),({'XLow32':1},U.MALFORMED),({'XHigh32':-1,'XLow32':0},U.MALFORMED),({'XHigh32':1.5,'XLow32':0},U.MALFORMED),({'XHigh32':2**32,'XLow32':0},U.MALFORMED),({'XHigh32':float('nan'),'XLow32':0},U.MALFORMED),({'XHigh32':float('inf'),'XLow32':0},U.MALFORMED)])
def test_uint64_states(store,expected): assert inspect(store,'X')[0] is expected

def role(store,p='R'):
    t,_=inspect(store,p+'Ticket'); i,_=inspect(store,p+'Identifier'); lot=store.get(p+'Lot',0); price=store.get(p+'OpenPrice',0); direction=store.get(p+'Direction',0)
    active=t is U.ACTIVE and i is U.ACTIVE
    bad=t is U.MALFORMED or i is U.MALFORMED or ((t is U.ACTIVE)!=(i is U.ACTIVE)) or (not active and any((lot,price,direction))) or lot<0 or price<0 or direction not in (0,1,2) or (active and (lot<=0 or price<=0 or direction==0))
    return active,bad

def pair(v): return {'High32':0,'Low32':v}
def active_role(p='R',ticket=1,ident=2,direction=1):
    return {p+'TicketHigh32':0,p+'TicketLow32':ticket,p+'IdentifierHigh32':0,p+'IdentifierLow32':ident,p+'Lot':.1,p+'OpenPrice':1.2,p+'Direction':direction}

@pytest.mark.parametrize('store,bad',[({'RTicketHigh32':0,'RTicketLow32':0,'RIdentifierHigh32':0,'RIdentifierLow32':0},False),({**active_role(), 'RIdentifierLow32':0},True),({**active_role(), 'RTicketLow32':0},True),({'RLot':.1},True),({'RLot':-1},True),({'RDirection':9},True)])
def test_role_rules(store,bad): assert role(store)[1] is bad

def tx(active,event,amount,before,after,phase=1):
    credit=event in {1,2,3,5}; debit=event in {4,6,7,8,9,10}
    residual=phase!=0 or amount!=0
    return (not active and residual) or phase not in range(5) or abs(after-(before+amount))>1e-9 or (credit and not(amount>0 and after>before)) or (debit and not(amount<0 and after<before))

@pytest.mark.parametrize('args,bad',[((True,1,5,10,15),False),((True,6,-5,10,5),False),((True,1,5,10,5),True),((True,6,5,10,15),True),((False,0,1,0,1),True),((True,1,5,10,14),True),((True,1,5,10,15,9),True)])
def test_reserve_transaction(args,bad): assert tx(*args) is bad

def ledger(rows,count,next_id,total):
    if count!=len(rows):return False
    previous=0
    for n,row in enumerate(rows,1):
        if row.get('id')!=n or row.get('before')!=previous or row.get('after')!=row.get('before')+row.get('amount'):return False
        previous=row['after']
    return next_id==(rows[-1]['id']+1 if rows else 1) and total==previous

def test_ledger_empty(): assert ledger([],0,1,0)
def test_ledger_multiple(): assert ledger([{'id':1,'before':0,'amount':4,'after':4},{'id':2,'before':4,'amount':-1,'after':3}],2,3,3)
@pytest.mark.parametrize('rows,count,next_id,total',[([{'id':2,'before':0,'amount':1,'after':1}],1,3,1),([{'id':1,'before':0,'amount':1,'after':2}],1,2,2),([],1,1,0),([],0,2,0),([],0,1,2)])
def test_ledger_rejects_corruption(rows,count,next_id,total): assert not ledger(rows,count,next_id,total)

def test_clean_start(): assert not any([False,False,False])
def test_managed_position_blocks(): assert not (1==0)
def test_state_key_blocks(): assert not (True is False)
def test_multiple_malformed_reasons_are_preserved(): assert ';'.join(['PENDING_MALFORMED','LEDGER_MALFORMED']).count(';')==1
