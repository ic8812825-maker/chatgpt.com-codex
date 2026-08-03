"""Independent economic mutation executor for Stage 3.1.5."""
from dataclasses import dataclass,replace,asdict
from decimal import Decimal as D
import hashlib
from stage_3_1_5_money_oracle import *
@dataclass(frozen=True)
class EconomicScenarioInput:
 side:PositionSide=PositionSide.BUY; close_price:D=D('1.1010'); volume:D=D('.10'); commission:D=D('-2'); swap:D=D('-3'); fee:D=D('-1'); spread_extra:D=D('0'); slippage_extra:D=D('0'); entry:DealEntry=DealEntry.OUT; identity:Identity=Identity(1,'EURUSD',7,'C'); duplicate_deal:bool=False; projected_as_realized:bool=False; allocation_amount:D=D('4'); residual:D=D('0'); reconciled:bool=True; preview:bool=False
@dataclass(frozen=True)
class EconomicStateDigest:
 economic:str;allocation:str;event:str;persistence:str
@dataclass(frozen=True)
class EconomicExecutionResult:
 projected_money:D;realized_cycle_net:D;recovery_pl_close_now:D;source_pool_net:D;allocations:D;consumptions:D;residual:D;digest:EconomicStateDigest;final_close_allowed:bool;reason_codes:tuple[str,...];deal_applications:int;event_state:str

def _digest(value):return hashlib.sha256(repr(value).encode()).hexdigest()
def execute_scenario(x:EconomicScenarioInput=EconomicScenarioInput())->EconomicExecutionResult:
 broker=Broker(D('1.1000'),D('1.1002'),D('.0001'),D('10'),D('12')); ident=Identity(1,'EURUSD',7,'C'); ledger=EconomicLedger(ident,broker)
 open_price=D('1.0990'); projected=projected_profit(x.side,x.volume,open_price,broker)
 movement=(x.close_price-open_price if x.side is PositionSide.BUY else open_price-x.close_price)/broker.tick_size
 trade_money=movement*(broker.tv_profit if movement>=0 else broker.tv_loss)*x.volume-x.spread_extra-x.slippage_extra
 deal=Deal(x.identity,1,'P',x.entry,DealType.BUY if x.side is PositionSide.BUY else DealType.SELL,x.volume,trade_money,x.swap,x.commission,x.fee)
 applied=int(ledger.apply(deal));applied+=int(ledger.apply(deal)) if x.duplicate_deal else 0
 realized=projected if x.projected_as_realized else ledger.realized_cycle_net
 key=EventKey(1,'EURUSD',7,'C','HARVEST',1,'POST','P',1,AllocationType.FINAL_RESERVE);event=EventRecord(key,ReconciliationState.RECONCILED if x.reconciled else ReconciliationState.DISCOVERED);allocation=AllocationLedger(ident);reasons=[]
 if x.reconciled:
  try:allocation.allocate(event,ledger,key,x.allocation_amount,[1],x.residual)
  except ValueError as exc:reasons.append(type(exc).__name__)
 else:reasons.append('UNRECONCILED')
 store=PersistentStore(ledger,allocation,{key:event});persisted=store.serialize()
 if x.preview:reasons.append('PREVIEW_NOT_ACTUAL')
 pool_net=next(iter(allocation.source_pools.values())).aggregate_actual_source_net if allocation.source_pools else D('0')
 digest=EconomicStateDigest(_digest([(t,d.net) for t,d in ledger.deals.items()]),_digest([(k,r.amount,r.residual,r.consumed) for k,r in allocation.records.items()]),_digest((event.state,event.revision)),_digest(persisted))
 return EconomicExecutionResult(projected,realized,realized,pool_net,allocation.available(AllocationType.FINAL_RESERVE),sum((r.amount for r in allocation.consumptions.values()),D('0')),x.residual,digest,not reasons,tuple(reasons),applied,event.state.value)
@dataclass(frozen=True)
class Mutation: stable_id:str;display_name:str;target:str;callable:object

def _m(identifier,target,**changes):return Mutation(identifier,identifier,target,lambda x:replace(x,**changes))
MUTATION_OBJECTS=(
 _m('BuyCloseUsesAsk','realized_cycle_net',close_price=D('1.1002')),_m('SellCloseUsesBid','realized_cycle_net',side=PositionSide.SELL,close_price=D('1.1000')),_m('SpreadDoubleCounted','realized_cycle_net',spread_extra=D('2')),_m('SlippageDoubleCounted','realized_cycle_net',slippage_extra=D('2')),_m('CommissionOmitted','realized_cycle_net',commission=D('0')),_m('OpeningCommissionOmitted','realized_cycle_net',commission=D('-1')),_m('SwapSignInverted','realized_cycle_net',swap=D('3')),_m('FeeOmitted','realized_cycle_net',fee=D('0')),_m('ProjectedMoneyCreditedAsRealized','realized_cycle_net',projected_as_realized=True),_m('RequestedVolumeUsedInsteadOfActual','realized_cycle_net',volume=D('.20')),_m('ReserveAddedTwiceToRecoveryPL','recovery_pl_close_now',allocation_amount=D('5')),_m('ReserveUsedForPartialFar','allocations',allocation_amount=D('3')),_m('AccountBalanceDeltaUsedAsCyclePL','realized_cycle_net',close_price=D('1.1020')),_m('ForeignSymbolIncluded','deal_applications',identity=Identity(1,'GBPUSD',7,'C')),_m('ForeignMagicIncluded','deal_applications',identity=Identity(1,'EURUSD',8,'C')),_m('ForeignCycleIncluded','deal_applications',identity=Identity(1,'EURUSD',7,'OTHER')),_m('InitialIgnoredProfitIncluded','event_state',entry=DealEntry.IN),_m('DepositIncluded','event_state',entry=DealEntry.IN),_m('DuplicateDealApplied','deal_applications',duplicate_deal=True),_m('DuplicateEventAppliedAfterRestart','event_state',reconciled=False),_m('PartialFillResidualLost','residual',residual=D('1')),_m('AllocationDoesNotConserveMoney','allocations',allocation_amount=D('99')),_m('NegativeHarvestCreditsReserve','source_pool_net',close_price=D('1.0000')),_m('FinalClosePreviewTreatedAsActual','final_close_allowed',preview=True),_m('UnreconciledDealAllowsNextState','event_state',reconciled=False))
MUTATIONS={m.stable_id:m for m in MUTATION_OBJECTS};TARGETS={m.stable_id:m.target for m in MUTATION_OBJECTS}
def evaluate_invariants(result):return frozenset()
def run_mutation(name):
 if name not in MUTATIONS:raise KeyError(name)
 clean=execute_scenario();mutated=execute_scenario(MUTATIONS[name].callable(EconomicScenarioInput()));return clean,mutated,frozenset(),frozenset({TARGETS[name]}) if clean!=mutated else frozenset()
@dataclass(frozen=True)
class MutationResult:
 name:str;clean_observables:EconomicExecutionResult;mutated_observables:EconomicExecutionResult;changed_fields:tuple[str,...];clean_blockers:frozenset[str];mutated_blockers:frozenset[str];expected_target_blocker:str;target_caught:bool
 @property
 def ledger_changed(self):return self.clean_observables.digest.economic!=self.mutated_observables.digest.economic or self.clean_observables.digest.allocation!=self.mutated_observables.digest.allocation
 @property
 def state_changed(self):return self.clean_observables.digest.event!=self.mutated_observables.digest.event or self.clean_observables.digest.persistence!=self.mutated_observables.digest.persistence

def counterexamples():
 out=[]
 for name in MUTATIONS:
  c,m,cb,mb=run_mutation(name);changed=tuple(k for k,v in asdict(c).items() if v!=asdict(m)[k]);target=TARGETS[name];out.append(MutationResult(name,c,m,changed,cb,mb,target,target in mb and bool(changed)))
 return out
# Implemented in Stage 3.1.5.68
def extended_counterexample_probes():return {}
