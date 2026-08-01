"""Independent Decimal oracle for the Stage 3.1.5 normative money contract."""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable

D = Decimal

@dataclass(frozen=True)
class Identity:
    account: int; symbol: str; magic: int; cycle: str

@dataclass(frozen=True)
class Broker:
    bid: D; ask: D; tick_size: D; tv_profit: D; tv_loss: D
    def __post_init__(self):
        assert self.ask >= self.bid and self.tick_size > 0
    @property
    def spread(self): return self.ask - self.bid

@dataclass(frozen=True)
class Position:
    identity: Identity; identifier: str; side: str; volume: D; open_price: D
    swap: D = D("0"); exit_commission: D = D("0"); exit_fee: D = D("0")

@dataclass(frozen=True)
class Deal:
    identity: Identity; ticket: int; position_id: str; entry: str; actual_volume: D
    profit: D; swap: D = D("0"); commission: D = D("0"); fee: D = D("0")
    initial_ignored: bool = False; balance_operation: bool = False
    @property
    def net(self): return self.profit + self.swap + self.commission + self.fee

@dataclass
class Allocation:
    partial_far: D = D("0"); reserve: D = D("0"); carry: D = D("0")
    transition: D = D("0"); residual: D = D("0")
    @property
    def total(self): return self.partial_far+self.reserve+self.carry+self.transition+self.residual

@dataclass
class EconomicLedger:
    identity: Identity
    deals: dict[int, Deal] = field(default_factory=dict)
    def apply(self, deal: Deal) -> bool:
        if deal.identity != self.identity or deal.initial_ignored or deal.balance_operation: return False
        if deal.ticket in self.deals: return False
        self.deals[deal.ticket] = deal; return True
    @property
    def realized(self): return sum((x.net for x in self.deals.values()), D("0"))

@dataclass(frozen=True)
class EventKey:
    account: int; symbol: str; magic: int; cycle: str; event_type: str; level: int
    phase: str; position_id: str; deal_ticket: int; allocation_type: str

@dataclass
class EventStore:
    applied: set[EventKey] = field(default_factory=set)
    states: dict[EventKey, str] = field(default_factory=dict)
    def apply(self, key: EventKey) -> bool:
        if key in self.applied: return False
        self.states[key] = "PERSISTED"; self.applied.add(key); return True
    def restart(self):
        return EventStore(set(self.applied), dict(self.states))

def adverse_prices(broker: Broker, slippage: D = D("0")) -> tuple[D,D]:
    return broker.bid-slippage, broker.ask+slippage

def projected_profit(side: str, lot: D, open_price: D, broker: Broker,
                     slippage: D = D("0")) -> D:
    bid, ask = adverse_prices(broker, slippage)
    close = bid if side == "BUY" else ask
    movement = close-open_price if side == "BUY" else open_price-close
    ticks = movement / broker.tick_size
    value = broker.tv_profit if ticks >= 0 else broker.tv_loss
    return ticks * value * lot

def floating_close_now(position: Position, broker: Broker, slippage: D = D("0")) -> D:
    return (projected_profit(position.side, position.volume, position.open_price, broker, slippage)
            + position.swap + position.exit_commission + position.exit_fee)

def recovery_pl_close_now(ledger: EconomicLedger, positions: Iterable[Position], broker: Broker,
                          slippage: D = D("0")) -> D:
    return ledger.realized + sum((floating_close_now(p, broker, slippage) for p in positions
                                  if p.identity == ledger.identity), D("0"))

def allocate_harvest(actual_reconciled_net: D, partial: D, reserve: D, carry: D,
                     transition: D) -> Allocation:
    if actual_reconciled_net <= 0:
        return Allocation(residual=actual_reconciled_net)
    used = partial+reserve+carry+transition
    if min(partial,reserve,carry,transition) < 0 or used > actual_reconciled_net:
        raise ValueError("allocation violates conservation")
    return Allocation(partial,reserve,carry,transition,actual_reconciled_net-used)

def allocate_opening_cost(unallocated: D, actual_closed: D, before: D, final: bool=False) -> tuple[D,D]:
    if not (D("0") < actual_closed <= before): raise ValueError("invalid actual fill")
    allocated = unallocated if final or actual_closed == before else unallocated*actual_closed/before
    return allocated, unallocated-allocated

def final_close_allowed(recovery: D, threshold: D, reserve: D, deficit: D,
                        reconciled: bool, pending: bool, risk_ok: bool, margin_ok: bool) -> bool:
    return all((reconciled, not pending, risk_ok, margin_ok, recovery > threshold, reserve >= deficit))

BLOCKERS = (
 "BUY_CLOSE_PRICE_FAIL","SELL_CLOSE_PRICE_FAIL","SPREAD_DOUBLE_COUNTED",
 "SLIPPAGE_DOUBLE_COUNTED","COMMISSION_OMITTED","OPENING_COMMISSION_OMITTED",
 "SWAP_SIGN_INVERTED","FEE_OMITTED","PROJECTED_CREDITED_AS_REALIZED",
 "REQUESTED_INSTEAD_OF_ACTUAL","RESERVE_DOUBLE_COUNTED","RESERVE_USED_FOR_PARTIAL_FAR",
 "ACCOUNT_BALANCE_CONTAMINATION","FOREIGN_SYMBOL_INCLUDED","FOREIGN_MAGIC_INCLUDED",
 "FOREIGN_CYCLE_INCLUDED","INITIAL_PROFIT_INCLUDED","DEPOSIT_INCLUDED",
 "DUPLICATE_DEAL_APPLIED","DUPLICATE_EVENT_AFTER_RESTART","PARTIAL_RESIDUAL_LOST",
 "BUDGET_CONSERVATION_FAIL","NEGATIVE_HARVEST_CREDIT","PREVIEW_TREATED_AS_ACTUAL",
 "UNRECONCILED_STATE_ADVANCE")

def causal_results(mutations: set[str] | None=None) -> dict[str,int]:
    mutations = mutations or set()
    return {name: int(name in mutations) for name in BLOCKERS}
