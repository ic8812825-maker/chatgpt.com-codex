"""Offline confirmed-order simulation with explicit service-window contracts."""
from dataclasses import asdict,dataclass,replace
from enum import Enum
from random import Random

from pinned import source
source()
from execution import Quote
from runner import Cycle
from a3rc import sign


class State(str,Enum):
    CREATED="CREATED"
    SUBMITTED="SUBMITTED"
    ACCEPTED="ACCEPTED"
    PARTIAL="PARTIAL"
    FILLED="FILLED"
    REJECTED="REJECTED"
    CANCEL_PENDING="CANCEL_PENDING"
    CANCELLED="CANCELLED"
    EXPIRED="EXPIRED"
    UNKNOWN="UNKNOWN"


DONE={State.FILLED,State.REJECTED,State.CANCELLED,State.EXPIRED}


@dataclass(slots=True)
class Order:
    key:str
    intent:object
    remaining:int
    due:int
    expiry:int
    state:State=State.CREATED
    cancellation:int|None=None


class Venue:
    def __init__(self, book,journal=None):
        self.book=book
        self.journal=journal
        self.orders={}
        self.failures=0
        self.cursor=0

    @property
    def active(self):
        return tuple(order for order in self.orders.values() if order.state not in DONE)

    def emit(self,name,order=None,**payload):
        if self.journal is not None:
            self.journal.append(dict(step=self.step,mid=self.quote.mid,event=name,
                                     order=order.key if order else None,**payload))

    def set_state(self,o,new):
        o.state=new
        self.emit(new.value,o,remaining=o.remaining)

    def advance(self,step,quote):
        self.previous_mid=getattr(self,"quote",quote).mid
        self.step,self.quote=step,quote
        self.capacity,self.rejects=quote.capacity,quote.rejects
        self.emit("QUOTE",spread=quote.spread,slip=quote.slip,capacity=quote.capacity,
                  carry=quote.carry,delay=quote.delay,rejects=quote.rejects,
                  unknown=quote.unknown,cancel_race=quote.cancel_race)
        if step:
            self.book.apply_carry(quote)
        self.book.observe(quote)
        for order in self.active:
            self.service(order)

    def submit(self,intent,key=None,ttl=4):
        if key is None:
            self.cursor+=1
            key=f"halr03-{self.cursor}"
        o=self.orders.get(key)
        if o:
            if intent!=o.intent:
                raise ValueError("client key belongs to different intent")
            self.emit("DUPLICATE_QUERY",o,remaining=o.remaining)
            return o
        o=Order(key,intent,intent.units,self.step+self.quote.delay,self.step+ttl)
        self.orders[key]=o
        self.emit("CREATED",o,side=intent.side,units=intent.units,ticket=intent.ticket)
        self.set_state(o,State.SUBMITTED)
        if self.rejects:
            self.rejects-=1
            self.failures+=1
            self.set_state(o,State.REJECTED)
        elif self.quote.unknown:
            self.failures+=1
            self.set_state(o,State.UNKNOWN)
        else:
            self.set_state(o,State.ACCEPTED)
            self.service(o)
        return o

    def cancel(self,o):
        if o.state not in DONE and o.cancellation is None:
            o.cancellation=self.step+1
            self.set_state(o,State.CANCEL_PENDING)

    def service(self,o):
        if o.state in DONE or self.quote.unknown:
            return
        due_cancel=o.cancellation is not None and self.step>=o.cancellation
        if due_cancel and not self.quote.cancel_race:
            self.set_state(o,State.CANCELLED)
            return
        if self.step>o.expiry:
            self.failures+=1
            self.set_state(o,State.EXPIRED)
            return
        if self.step<o.due or self.capacity<=0:
            if due_cancel:
                self.set_state(o,State.CANCELLED)
            return
        if o.state==State.UNKNOWN:
            self.set_state(o,State.ACCEPTED)
        n=self.book.fill(o.intent,min(o.remaining,self.capacity),self.quote)
        if n:
            self.capacity-=n
            o.remaining-=n
            self.emit("FILL",o,units=n,side=o.intent.side,ticket=o.intent.ticket,
                      pnl=self.book.mark(self.quote),net=self.book.net,gross=self.book.gross)
        if not o.remaining:
            self.set_state(o,State.FILLED)
        elif due_cancel:
            self.set_state(o,State.CANCELLED)
        elif not n:
            self.failures+=1
            self.set_state(o,State.REJECTED)
        else:
            self.set_state(o,State.PARTIAL if o.cancellation is None else State.CANCEL_PENDING)


@dataclass(frozen=True,slots=True)
class Contract:
    name:str
    move:int|None
    spread:int
    slip:int
    carry:int
    stride:int|None
    note:str
    window:int=1
    reserve:int=0

    def next_service(self,t):
        return None if self.stride is None else t+self.stride-t%self.stride


PROFILES={
    "E0":Contract("E0",300,20,0,0,1,"Nominal, full same-quote batches at every event"),
    "E1":Contract("E1",300,32,2,1,1,"Bounded spread/carry; confirmed service at every event"),
    "E2":Contract("E2",300,32,2,1,2,"Even events serve full batches; odd events have zero capacity"),
    "E3":Contract("E3",300,50,3,1,None,"Persistent rejection or UNKNOWN"),
    "E4":Contract("E4",4200,32,2,0,None,"Gap and interrupted execution; no assured service"),
    "E5":Contract("E5",300,40,4,1,None,"Adverse price after observed Net; patterned venue limits"),
    "E6":Contract("E6",None,100,4,1,None,"Zero capacity through the deadline"),
}


@dataclass(frozen=True,slots=True)
class Case:
    orientation:int
    moves:tuple
    profile:str="E0"
    spread_draws:tuple=()
    generator:str="markov"

    def quote(self,t,mid):
        name=self.profile
        if name=="E0":
            return Quote(mid)
        j=self.spread_draws[t] if self.spread_draws else t
        if name in ("E1","E2"):
            off=name=="E2" and t%2==1
            return Quote(mid,spread=20+(j%7)*2 if t else 20,slip=j%3 if t else 0,
                         carry=int(t>0 and j%3==0),capacity=0 if off else 1000,
                         delay=int(off))
        if name=="E3":
            return Quote(mid,spread=24 if t else 20,slip=2 if t else 0,
                         capacity=30 if t==0 else 0,unknown=t>=2,rejects=int(t==1))
        if name=="E4":
            return Quote(mid,spread=32 if t>=2 else 20,slip=2 if t>=2 else 0,
                         capacity=0 if t==2 else 1000)
        if name=="E5":
            return Quote(mid,spread=32 if t else 20,slip=4 if t else 0,
                         capacity=23,delay=int(t%3==0),rejects=int(t%3==1))
        return Quote(mid,capacity=0,unknown=t>0)

    def next_move(self,t,net):
        if self.profile=="E5":
            return -300*sign(net)
        if self.profile=="E4" and t==2:
            return -4200*(sign(self.moves[0]) or self.orientation)
        return self.moves[t]


class ExecutionCycle(Cycle):
    def __init__(self,*args,journal=None,**kwargs):
        super().__init__(*args,journal=None,**kwargs)
        self.v=Venue(self.book,journal)


def replay(name,case,limits,params,selector=None,journal=None,contract=None):
    from runner import ideal
    if name=="K-IDEAL":
        return ideal(limits)
    kwargs={"envelope":contract} if contract is not None else {}
    cycle=ExecutionCycle(name,case.orientation,limits,params,journal=journal,
                         selector=selector,**kwargs)
    mid=0
    for t in range(limits.horizon+1):
        cycle.step(t,case.quote(t,mid))
        if cycle.finish:
            break
        if t<limits.horizon:
            mid+=case.next_move(t,cycle.book.net)
    return cycle.result()


def catalog():
    return {k:dict(**asdict(v),evidence="ASSUMED",
                   full_batch_capacity=1000 if v.stride is not None else None)
            for k,v in PROFILES.items()}
