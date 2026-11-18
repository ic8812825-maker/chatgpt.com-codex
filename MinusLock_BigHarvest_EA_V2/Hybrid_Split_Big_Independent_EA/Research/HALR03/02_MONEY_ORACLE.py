"""Independent bid/ask cash-flow oracle in half-cent accounting units."""
from dataclasses import dataclass


@dataclass
class Leg:
    side: int
    amount: int
    entry_twice: int


class Oracle:
    def __init__(self, orientation, commission=9):
        e = -600*orientation
        self.legs = {0:Leg(1,100,e+20),1:Leg(-1,100,e-20)}
        self.commission = commission
        self.cash = -200*commission
        self.next_ticket = 2

    @staticmethod
    def execution_price(side, mid, spread, slip):
        return 2*mid+side*(spread+2*slip)

    def carry(self, rate):
        self.cash -= rate*sum(leg.amount for leg in self.legs.values())

    def confirmed(self, side, amount, ticket, mid, spread, slip):
        self.cash -= amount*self.commission
        price = self.execution_price(side,mid,spread,slip)
        if ticket is None:
            self.legs[self.next_ticket] = Leg(side,amount,price)
            self.next_ticket += 1
            return
        leg = self.legs[ticket]
        assert leg.side == -side and 0 < amount <= leg.amount
        self.cash += leg.side*amount*(price-leg.entry_twice)
        leg.amount -= amount
        if leg.amount == 0:
            del self.legs[ticket]

    def liquidation(self, mid, spread, slip):
        value = self.cash
        for leg in self.legs.values():
            price = self.execution_price(-leg.side,mid,spread,slip)
            value += leg.amount*(leg.side*(price-leg.entry_twice)-self.commission)
        return value
