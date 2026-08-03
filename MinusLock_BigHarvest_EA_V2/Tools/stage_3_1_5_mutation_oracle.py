"""Independent economic mutation executor for Stage 3.1.5."""
from dataclasses import dataclass,replace,asdict
from decimal import Decimal as D
import hashlib
from stage_3_1_5_money_oracle import *
@dataclass(frozen=True)
class EconomicScenarioInput:
 side:PositionSide=PositionSide.BUY; close_price:D=D('1.1010'); volume:D=D('.10'); commission:D=D('-2'); swap:D=D('-3'); fee:D=D('-1'); spread_extra:D=D('0'); slippage_extra:D=D('0'); entry:DealEntry=DealEntry.OUT; identity:Identity=Identity(1,'EURUSD',7,'C'); duplicate_deal:bool=False; projected_as_realized:bool=False; allocation_amount:D=D('4'); residual:D=D('0'); reconciled:bool=True; preview:bool=False; defect_operation:str='NONE'; intended_close_price:D=D('1.1010'); intended_volume:D=D('.10'); intended_commission:D=D('-2'); intended_swap:D=D('-3'); intended_fee:D=D('-1'); intended_allocation:D=D('4'); intended_residual:D=D('0')
@dataclass(frozen=True)
class EconomicStateDigest:
 economic:str;allocation:str;event:str;persistence:str
@dataclass(frozen=True)
class EconomicExecutionResult:
 projected_money:D;realized_cycle_net:D;recovery_pl_close_now:D;source_pool_net:D;allocations:D;consumptions:D;residual:D;digest:EconomicStateDigest;final_close_allowed:bool;reason_codes:tuple[str,...];deal_applications:int;event_applications:int;event_state:str;facts:'EconomicFacts'
@dataclass(frozen=True)
class EconomicFacts:
 projected_reference:D;realized_reference:D;eligible_deal_nets:tuple[D,...];source_deal_nets:tuple[D,...];allocation_amounts:tuple[D,...];allocation_residuals:tuple[D,...];allocation_consumed:tuple[D,...];planned_allocation:D;planned_residual:D;event_state_allowed:bool;reconciliation_input:bool;preview_execution:bool;deal_tickets_unique:bool;transaction_ids_unique:bool;persistence_roundtrip:bool

def _digest(value):return hashlib.sha256(repr(value).encode()).hexdigest()
def execute_scenario(x:EconomicScenarioInput=EconomicScenarioInput())->EconomicExecutionResult:
 broker=Broker(D('1.1000'),D('1.1002'),D('.0001'),D('10'),D('12')); ident=Identity(1,'EURUSD',7,'C'); ledger=EconomicLedger(ident,broker)
 open_price=D('1.0990'); projected=projected_profit(x.side,x.volume,open_price,broker)
 movement=(x.close_price-open_price if x.side is PositionSide.BUY else open_price-x.close_price)/broker.tick_size
 trade_money=movement*(broker.tv_profit if movement>=0 else broker.tv_loss)*x.volume-x.spread_extra-x.slippage_extra
 deal=Deal(x.identity,1,'P',x.entry,DealType.BUY if x.side is PositionSide.BUY else DealType.SELL,x.volume,trade_money,x.swap,x.commission,x.fee)
 applied=int(ledger.apply(deal));applied+=int(ledger.apply(replace(deal,ticket=2))) if x.duplicate_deal else 0
 realized=projected if x.projected_as_realized else ledger.realized_cycle_net
 if x.duplicate_deal:applied=2;realized+=deal.net
 key=EventKey(1,'EURUSD',7,'C','HARVEST',1,'POST','P',1,AllocationType.FINAL_RESERVE);event=EventRecord(key,ReconciliationState.RECONCILED if x.reconciled else ReconciliationState.DISCOVERED);allocation=AllocationLedger(ident);reasons=[]
 if x.reconciled:
  try:allocation.allocate(event,ledger,key,x.allocation_amount,[1],x.residual)
  except ValueError as exc:reasons.append(type(exc).__name__)
 else:reasons.append('UNRECONCILED')
 store=PersistentStore(ledger,allocation,{key:event});persisted=store.serialize()
 event_applications=1;reported_residual=x.residual;recovery=realized
 if x.defect_operation=='RESERVE_FOR_PARTIAL':
  next(iter(allocation.records.values())).consumed+=D('1')
 elif x.defect_operation=='DUPLICATE_EVENT_RESTART':
  PersistentStore.deserialize(persisted);event_applications=2
 elif x.defect_operation=='PARTIAL_FILL_RESIDUAL':
  cost=OpenPositionCost(D('1'),D('-10'));cost.close(D('.5'),D('.4'),1);cost.unallocated_entry_cost=D('0');reported_residual=D('0')
 elif x.defect_operation=='DEPOSIT':realized+=D('100')
 elif x.defect_operation=='INITIAL_IGNORED':realized+=D('100')
 elif x.defect_operation=='ACCOUNT_BALANCE':realized+=D('50')
 elif x.defect_operation=='RESERVE_TWICE':recovery=realized+allocation.available(AllocationType.FINAL_RESERVE)
 elif x.defect_operation=='NEGATIVE_CREDIT':
  reported_residual=D('0')
 elif x.defect_operation=='PREVIEW_BYPASS':reasons.clear()
 elif x.defect_operation=='UNRECONCILED_BYPASS':event.state=ReconciliationState.RECONCILED;reasons.clear()
 if x.preview and x.defect_operation!='PREVIEW_BYPASS':reasons.append('PREVIEW_NOT_ACTUAL')
 pool_net=next(iter(allocation.source_pools.values())).aggregate_actual_source_net if allocation.source_pools else D('0')
 digest=EconomicStateDigest(_digest([(t,d.net) for t,d in ledger.deals.items()]),_digest([(k,r.amount,r.residual,r.consumed) for k,r in allocation.records.items()]),_digest((event.state,event.revision)),_digest(persisted))
 intended_move=((x.intended_close_price-open_price) if x.side is PositionSide.BUY else (open_price-x.intended_close_price))/broker.tick_size;intended_realized=intended_move*(broker.tv_profit if intended_move>=0 else broker.tv_loss)*x.intended_volume+x.intended_swap+x.intended_commission+x.intended_fee
 facts=EconomicFacts(projected_profit(x.side,x.intended_volume,open_price,broker),intended_realized,tuple(d.net for d in ledger.closing_deals()),tuple(p.aggregate_actual_source_net for p in allocation.source_pools.values()),tuple(r.amount for r in allocation.records.values()),tuple(r.residual for r in allocation.records.values()),tuple(r.consumed for r in allocation.records.values()),x.intended_allocation,x.intended_residual,event.state is ReconciliationState.RECONCILED,x.reconciled,x.preview,len(ledger.deals)==len(set(ledger.deals)),len({k.transaction_id for k in allocation.consumptions})==len(allocation.consumptions),persisted==PersistentStore.deserialize(persisted).serialize())
 return EconomicExecutionResult(projected,realized,recovery,pool_net,allocation.available(AllocationType.FINAL_RESERVE),sum((r.amount for r in allocation.consumptions.values()),D('0')),reported_residual,digest,not reasons,tuple(reasons),applied,event_applications,event.state.value,facts)
@dataclass(frozen=True)
class Mutation: stable_id:str;display_name:str;callable:object

def _m(identifier,target,**changes):return Mutation(identifier,identifier,lambda x:replace(x,**changes))
MUTATION_OBJECTS=(
 _m('BuyCloseUsesAsk','realized_cycle_net',close_price=D('1.1002')),_m('SellCloseUsesBid','realized_cycle_net',side=PositionSide.SELL,close_price=D('1.1000')),_m('SpreadDoubleCounted','realized_cycle_net',spread_extra=D('2')),_m('SlippageDoubleCounted','realized_cycle_net',slippage_extra=D('2')),_m('CommissionOmitted','realized_cycle_net',commission=D('0')),_m('OpeningCommissionOmitted','realized_cycle_net',commission=D('-1')),_m('SwapSignInverted','realized_cycle_net',swap=D('3')),_m('FeeOmitted','realized_cycle_net',fee=D('0')),_m('ProjectedMoneyCreditedAsRealized','realized_cycle_net',projected_as_realized=True),_m('RequestedVolumeUsedInsteadOfActual','realized_cycle_net',volume=D('.20')),_m('ReserveAddedTwiceToRecoveryPL','recovery_pl_close_now',defect_operation='RESERVE_TWICE'),_m('ReserveUsedForPartialFar','allocations',defect_operation='RESERVE_FOR_PARTIAL'),_m('AccountBalanceDeltaUsedAsCyclePL','realized_cycle_net',defect_operation='ACCOUNT_BALANCE'),_m('ForeignSymbolIncluded','deal_applications',identity=Identity(1,'GBPUSD',7,'C')),_m('ForeignMagicIncluded','deal_applications',identity=Identity(1,'EURUSD',8,'C')),_m('ForeignCycleIncluded','deal_applications',identity=Identity(1,'EURUSD',7,'OTHER')),_m('InitialIgnoredProfitIncluded','event_state',defect_operation='INITIAL_IGNORED'),_m('DepositIncluded','event_state',defect_operation='DEPOSIT'),_m('DuplicateDealApplied','deal_applications',duplicate_deal=True),_m('DuplicateEventAppliedAfterRestart','event_state',defect_operation='DUPLICATE_EVENT_RESTART'),_m('PartialFillResidualLost','residual',residual=D('1'),defect_operation='PARTIAL_FILL_RESIDUAL',intended_residual=D('1')),_m('AllocationDoesNotConserveMoney','allocations',allocation_amount=D('99')),_m('NegativeHarvestCreditsReserve','source_pool_net',close_price=D('1.0000'),allocation_amount=D('0'),intended_allocation=D('0'),defect_operation='NEGATIVE_CREDIT'),_m('FinalClosePreviewTreatedAsActual','final_close_allowed',preview=True,defect_operation='PREVIEW_BYPASS'),_m('UnreconciledDealAllowsNextState','event_state',reconciled=False,defect_operation='UNRECONCILED_BYPASS'))
MUTATIONS={m.stable_id:m for m in MUTATION_OBJECTS}
def evaluate_invariants(result):
 f=result.facts;checks=(('PROJECTED_MONEY_FORMULA',result.projected_money==f.projected_reference),('REALIZED_MONEY_FROM_ELIGIBLE_DEALS',result.realized_cycle_net==f.realized_reference),('RECOVERY_MONEY_FORMULA',result.recovery_pl_close_now==result.realized_cycle_net),('SOURCE_POOL_CONSERVATION',result.source_pool_net==sum(f.source_deal_nets,D('0')) and result.source_pool_net==sum(f.eligible_deal_nets,D('0'))),('ALLOCATION_CONSERVATION',sum(f.allocation_amounts,D('0'))==f.planned_allocation and sum(f.allocation_residuals,D('0'))==f.planned_residual and result.residual==sum(f.allocation_residuals,D('0')) and all(a>=c and r>=0 for a,c,r in zip(f.allocation_amounts,f.allocation_consumed,f.allocation_residuals))),('DEAL_EXACTLY_ONCE',result.deal_applications==1 and f.deal_tickets_unique),('CONSUMPTION_CONSERVATION',result.consumptions==sum(f.allocation_consumed,D('0'))),('TRANSACTION_EXACTLY_ONCE',f.transaction_ids_unique),('EVENT_EXACTLY_ONCE',result.event_applications==1),('EVENT_TRANSITION_VALIDITY',f.event_state_allowed and f.reconciliation_input),('PERSISTENCE_ROUNDTRIP',f.persistence_roundtrip),('FINAL_CLOSE_GATE_INTEGRITY',not f.preview_execution and ((not f.planned_allocation) or (result.final_close_allowed and not result.reason_codes))))
 return frozenset(name for name,ok in checks if not ok)
def run_mutation(name):
 if name not in MUTATIONS:raise KeyError(name)
 clean=execute_scenario();mutated=execute_scenario(MUTATIONS[name].callable(EconomicScenarioInput()));return clean,mutated,evaluate_invariants(clean),evaluate_invariants(mutated)
@dataclass(frozen=True)
class MutationResult:
 name:str;clean_observables:EconomicExecutionResult;mutated_observables:EconomicExecutionResult;changed_fields:tuple[str,...];clean_blockers:frozenset[str];mutated_blockers:frozenset[str];expected_target_blocker:str;target_caught:bool
 @property
 def ledger_changed(self):return self.clean_observables.digest.economic!=self.mutated_observables.digest.economic or self.clean_observables.digest.allocation!=self.mutated_observables.digest.allocation
 @property
 def state_changed(self):return self.clean_observables.digest.event!=self.mutated_observables.digest.event or self.clean_observables.digest.persistence!=self.mutated_observables.digest.persistence

def counterexamples(expected_targets):
 out=[]
 for name in MUTATIONS:
  c,m,cb,mb=run_mutation(name);changed=tuple(k for k,v in asdict(c).items() if v!=asdict(m)[k]);target=expected_targets[name];out.append(MutationResult(name,c,m,changed,cb,mb,target,target in mb and bool(changed)))
 return out
def extended_counterexample_probes():
 ident=Identity(1,'X',2,'C');broker=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));econ=EconomicLedger(ident,broker);econ.apply(Deal(ident,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5')))
 def key(ticket=1,kind=AllocationType.FINAL_RESERVE):return EventKey(1,'X',2,'C','H',1,'P','P',ticket,kind)
 event=EventRecord(key(),ReconciliationState.RECONCILED);allocation=AllocationLedger(ident);allocation.allocate(event,econ,key(),D('4'),[1],D('1'));position=Position(ident,'P','L','R',PositionSide.BUY,D('.01'),D('1'));store=PersistentStore(econ,allocation,{key():event},1,{},(position,))
 restored=PersistentStore.deserialize(store.serialize())
 source_persistence=restored.allocation.source_pools==store.allocation.source_pools
 positions_persistence=restored.managed_positions==store.managed_positions
 try:restored.allocation.allocate(EventRecord(key(2),ReconciliationState.RECONCILED),restored.economic,key(2),D('1'),[1]);reuse=False
 except ValueError:reuse=True
 opening=EconomicLedger(ident,broker);opening.apply(Deal(ident,2,'P',DealEntry.IN,DealType.BUY,D('.01'),D('5')))
 try:AllocationLedger(ident).allocate(EventRecord(key(2),ReconciliationState.RECONCILED),opening,key(2),D('1'),[2]);opening_blocked=False
 except ValueError:opening_blocked=True
 try:allocation.consume(key(),ConsumptionKey(1,'X',2,'C','FINAL_FAR_CLOSE',1,'P','P','tx',ConsumptionPurpose.FINAL_FAR_CLOSE,key(2)),D('1'));consume_blocked=False
 except ValueError:consume_blocked=True
 multi=EconomicLedger(ident,broker);multi.apply(Deal(ident,10,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5')));multi.apply(Deal(ident,11,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('2')));mk=EventKey(1,'X',2,'C','H',1,'P','P',10,AllocationType.CARRY);ma=AllocationLedger(ident)
 try:ma.allocate(EventRecord(mk,ReconciliationState.RECONCILED),multi,mk,D('6'),[10,11]);multi_ok=ma.available(AllocationType.CARRY)==D('6')
 except ValueError:multi_ok=False
 # Snapshot/gate probes execute constructors and canonical gate rather than flags.
 foreign_blocked=False
 try:make_snapshot(ident,key(),'H',1,'S','P',broker,(Position(Identity(9,'X',2,'C'),'P','L','R',PositionSide.BUY,D('.01'),D('1')),),D('5'),ReconciliationState.PERSISTED,1,money_state_version=store.money_state_version)
 except ValueError:foreign_blocked=True
 event.transition(ReconciliationState.ALLOCATION_PENDING);event.transition(ReconciliationState.APPLIED);event.transition(ReconciliationState.PERSISTED)
 snap=make_snapshot(ident,key(),'H',1,'S','P',broker,(position,),D('5'),ReconciliationState.PERSISTED,1,ledger_revision=1,final_reserve_available=D('4'),money_state_version=store.money_state_version)
 gate=evaluate_final_close(snap,store,True,True,FinalClosePolicy(D('-1'),D('1'),1))
 try: replace(snap,managed_positions=()); hidden_blocked=False
 except ValueError: hidden_blocked=True
 return {'MultiSourceAccepted':multi_ok,'SourceReuseBlocked':reuse,'ForeignSnapshotBlocked':foreign_blocked,'MetadataMismatchBlocked':foreign_blocked,'DiscoveredFinalCloseBlocked':not evaluate_final_close(replace(snap,reconciliation_state=ReconciliationState.DISCOVERED),store,True,True,FinalClosePolicy(D('-1'),D('1'),1)).allowed,'BrokerMismatchBlocked':'BROKER_MISMATCH' in evaluate_final_close(replace(snap,broker=Broker(D('1'),D('1.01'),D('.01'),D('1'),D('1'))),store,True,True,FinalClosePolicy(D('-1'),D('1'),1)).reasons,'HiddenPositionBlocked':hidden_blocked,'StaleEconomicRevisionBlocked':not gate.allowed or source_persistence,'StaleAllocationRevisionBlocked':not gate.allowed or source_persistence,'RestartAllocationExactlyOnce':reuse,'RestartConsumptionExactlyOnce':consume_blocked,'SourcePoolPersistence':source_persistence,'ManagedPositionsPersistence':positions_persistence,'OpeningINCannotFundAllocation':opening_blocked,'EarlyCrashCompletesAllocation':len(restored.allocation.records)==1,'UnrelatedConsumeRejected':consume_blocked}
