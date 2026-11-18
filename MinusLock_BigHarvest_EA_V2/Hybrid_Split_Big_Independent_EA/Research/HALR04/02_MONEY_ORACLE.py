"""Independent monetary replay at actual bid/ask in $0.005 units."""
from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class Position:
    sign:int
    amount:int
    entry_twice_point:int


class MoneyOracle:
    def __init__(self,orientation,commission=9,initial_mid=0,initial_spread=20,
                 initial_entry=None):
        e=(initial_mid-300*orientation) if initial_entry is None else initial_entry
        self.positions=OrderedDict((
            (0,Position(1,100,int(2*e+initial_spread))),
            (1,Position(-1,100,int(2*e-initial_spread)))))
        self.commission=commission
        self.realized_cash=-200*commission
        self.actual_incremental_cost=0
        self.next_ticket=2
        self.active=set()
        self.history=[]

    def replay(self,events):
        for record in events:
            category=record["event"]
            key=record.get("order")
            if category=="QUOTE":
                mid=record["mid"]
                spread=record["spread"]
                slip=record["slip"]
                self.mid_twice=int(2*mid)
                self.half_spread_twice=spread+2*slip
                if record["step"]:
                    carry=sum(t.amount for t in self.positions.values())*record["carry"]
                    self.realized_cash-=carry
                    self.actual_incremental_cost+=carry
            elif category in ("CREATED","SUBMITTED","ACCEPTED","PARTIAL","UNKNOWN","CANCEL_PENDING"):
                self.active.add(key)
            elif category in ("REJECTED","CANCELLED","EXPIRED","FILLED"):
                self.active.discard(key)
            elif category=="FILL":
                self.apply_fill(record["side"],record["units"],record["ticket"])
                assert self.mark()==record["pnl"],record
                assert self.exposure()==(record["gross"],record["net"]),record
            else:
                continue
            self.history.append((record["step"],category,self.mark(),self.exposure(),len(self.active)))
        return self

    def exposure(self):
        return (sum(t.amount for t in self.positions.values()),
                sum(t.amount*t.sign for t in self.positions.values()))

    def apply_fill(self,side,amount,ticket):
        cost=self.half_spread_twice+self.commission
        self.actual_incremental_cost+=amount*cost
        self.realized_cash-=amount*self.commission
        px=self.mid_twice+side*self.half_spread_twice
        if ticket is None:
            self.positions[self.next_ticket]=Position(side,amount,px)
            self.next_ticket+=1
        else:
            t=self.positions[ticket]
            assert t.sign==-side and 0<amount<=t.amount
            self.realized_cash+=t.sign*(px-t.entry_twice_point)*amount
            t.amount-=amount
            if t.amount==0:
                del self.positions[ticket]

    def mark(self):
        total=self.realized_cash
        for t in self.positions.values():
            exit_price=self.mid_twice-t.sign*self.half_spread_twice
            total+=t.amount*(t.sign*(exit_price-t.entry_twice_point)-self.commission)
        return total

    @property
    def flat(self):
        return not self.positions and not self.active
