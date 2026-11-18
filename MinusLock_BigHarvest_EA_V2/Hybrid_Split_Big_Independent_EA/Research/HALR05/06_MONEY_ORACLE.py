"""Independent confirmed-fill ledger, in exact half-cent accounting units."""
from dataclasses import dataclass


@dataclass(slots=True)
class Ticket:
    units:int
    side:int
    mid2:int
    paid_price2:int


class Money:
    def __init__(self,entry_mid2,entry_spread,commission=9):
        self.commission=commission
        self.initial_cost=200*(entry_spread+commission)
        self.cash=-200*commission
        self.realized_mid=0
        self.tickets={0:Ticket(100,1,entry_mid2,entry_mid2+entry_spread),
                      1:Ticket(100,-1,entry_mid2,entry_mid2-entry_spread)}
        self.next_id=2
        self.new_spread=self.new_slip=self.new_commission=self.swap=0
        self.pending={}
        self.done=set()

    @property
    def spent(self):
        return self.new_spread+self.new_slip+self.new_commission+self.swap

    @property
    def gross(self):
        return sum(t.units for t in self.tickets.values())

    @property
    def net(self):
        return sum(t.units*t.side for t in self.tickets.values())

    @property
    def flat(self):
        return not self.tickets and not self.pending

    @property
    def reserve(self):
        return self.gross*(self.spread+2*self.slip+self.commission)

    def mark(self):
        unrealized=sum(t.side*t.units*(self.mid2-t.mid2) for t in self.tickets.values())
        amount=self.realized_mid+unrealized-self.initial_cost-self.spent-self.reserve
        # Cross-check against side-specific entry and liquidation prices.
        actual=self.cash+sum(t.units*(t.side*(self.mid2-
            t.side*(self.spread+2*self.slip)-t.paid_price2)-self.commission)
            for t in self.tickets.values())
        if amount!=actual:
            raise AssertionError("Bid/ask cash and mark do not reconcile")
        return amount

    def observe(self,r):
        event=r["event"]
        key=r.get("order")
        if event=="QUOTE":
            self.mid2=int(2*r["mid"])
            self.spread,self.slip=r["spread"],r["slip"]
            carry=self.gross*r["carry"] if r["step"] else 0
            self.swap+=carry
            self.cash-=carry
        elif event=="CREATED":
            if key in self.pending or key in self.done:
                raise ValueError("reused request key")
            self.pending[key]=[r["side"],r["units"],r["ticket"]]
        elif event=="FILL":
            side,remaining,ticket=self.pending[key]
            units=r["units"]
            if not 0<units<=remaining or r["side"]!=side or r["ticket"]!=ticket:
                raise ValueError("inconsistent reported fill")
            self.pending[key][1]-=units
            self.new_spread+=self.spread*units
            self.new_slip+=2*self.slip*units
            self.new_commission+=self.commission*units
            self.cash-=self.commission*units
            actual_price=self.mid2+side*(self.spread+2*self.slip)
            if ticket is None:
                self.tickets[self.next_id]=Ticket(units,side,self.mid2,actual_price)
                self.next_id+=1
            else:
                t=self.tickets[ticket]
                if t.side!=-side or units>t.units:
                    raise ValueError("close exceeds actual ticket")
                self.realized_mid+=t.side*units*(self.mid2-t.mid2)
                self.cash+=t.side*units*(actual_price-t.paid_price2)
                t.units-=units
                if not t.units:
                    del self.tickets[ticket]
            if self.mark()!=r["pnl"] or self.gross!=r["gross"] or self.net!=r["net"]:
                raise AssertionError(r)
        elif event in ("REJECTED","FILLED","CANCELLED","EXPIRED"):
            if event=="FILLED" and self.pending[key][1]!=0:
                raise ValueError("FILLED with outstanding quantity")
            del self.pending[key]
            self.done.add(key)
        return event in ("QUOTE","FILL")
