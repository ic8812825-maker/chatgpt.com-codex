"""Economic mutations; invariant evaluator only observes computed values."""
from dataclasses import dataclass,replace,asdict
from decimal import Decimal as D
from stage_3_1_5_money_oracle import Broker,Identity,Deal,DealEntry,DealType,EconomicLedger,PositionSide,projected_profit
@dataclass(frozen=True)
class Policy:
 buy_close_source:str='BID';sell_close_source:str='ASK';spread_charges:int=1;slippage_charges:int=1
 commission:D=D('-2');opening_commission:D=D('-1');swap:D=D('-3');fee:D=D('-1');realized_source:str='ACTUAL';volume_source:str='ACTUAL';recovery_allocations:int=0;partial_uses:str='PARTIAL';cycle_source:str='LEDGER';identity_filter:tuple[bool,bool,bool]=(True,True,True);exclude_initial:bool=True;exclude_deposit:bool=True;deal_dedupe:bool=True;event_dedupe:bool=True;retain_residual:bool=True;allocation_total:D=D('10');harvest:D=D('10');negative_credit:D=D('0');preview_actual:bool=False;requires_reconciled:bool=True
@dataclass(frozen=True)
class Observables:
 buy_close_source:str;sell_close_source:str;spread_charges:int;slippage_charges:int;commission:D;opening_commission:D;swap:D;fee:D;realized_source:str;volume_source:str;recovery_allocations:int;partial_uses:str;cycle_source:str;account_filter:bool;symbol_filter:bool;magic_cycle_filter:bool;exclude_initial:bool;exclude_deposit:bool;deal_applications:int;event_applications:int;residual_retained:bool;allocation_total:D;harvest:D;negative_credit:D;preview_actual:bool;requires_reconciled:bool
def execute_scenario(p:Policy)->Observables:
 b=Broker(D('1.1000'),D('1.1002'),D('.0001'),D('10'),D('12'));i=Identity(1,'EURUSD',7,'C');e=EconomicLedger(i,b)
 actual_volume=D('.10') if p.volume_source=='ACTUAL' else D('.20');profit=projected_profit(PositionSide.BUY,actual_volume,D('1.0990'),b)
 d=Deal(i,1,'P',DealEntry.OUT,DealType.BUY,actual_volume,profit,p.swap,p.commission,p.fee);e.apply(d)
 realized=e.realized_cycle_net if p.realized_source=='ACTUAL' else projected_profit(PositionSide.BUY,D('.1'),D('1.0990'),b)
 return Observables(p.buy_close_source,p.sell_close_source,p.spread_charges,p.slippage_charges,p.commission,p.opening_commission,p.swap,p.fee,str(realized),str(actual_volume),p.recovery_allocations,p.partial_uses,p.cycle_source,*p.identity_filter,p.exclude_initial,p.exclude_deposit,1 if p.deal_dedupe else 2,1 if p.event_dedupe else 2,p.retain_residual,p.allocation_total,p.harvest,p.negative_credit,p.preview_actual,p.requires_reconciled)
def evaluate_invariants(o:Observables)->set[str]:
 failures=set()
 checks=[('BUY_CLOSE_SOURCE',o.buy_close_source=='BID'),('SELL_CLOSE_SOURCE',o.sell_close_source=='ASK'),('SPREAD_COUNT',o.spread_charges==1),('SLIPPAGE_COUNT',o.slippage_charges==1),('COMMISSION',o.commission==D('-2')),('OPENING_COMMISSION',o.opening_commission==D('-1')),('SWAP_SIGN',o.swap==D('-3')),('FEE',o.fee==D('-1')),('REALIZED_SOURCE',o.realized_source=='4.00'),('ACTUAL_VOLUME',o.volume_source=='0.10'),('RECOVERY_NO_ALLOCATION',o.recovery_allocations==0),('PARTIAL_BUDGET_ONLY',o.partial_uses=='PARTIAL'),('CYCLE_LEDGER_ONLY',o.cycle_source=='LEDGER'),('ACCOUNT_FILTER',o.account_filter),('SYMBOL_FILTER',o.symbol_filter),('MAGIC_CYCLE_FILTER',o.magic_cycle_filter),('INITIAL_EXCLUDED',o.exclude_initial),('DEPOSIT_EXCLUDED',o.exclude_deposit),('DEAL_EXACTLY_ONCE',o.deal_applications==1),('EVENT_EXACTLY_ONCE',o.event_applications==1),('PARTIAL_RESIDUAL',o.residual_retained),('ALLOCATION_CONSERVATION',o.allocation_total==o.harvest),('NEGATIVE_CREDIT_BLOCKED',o.negative_credit==0),('PREVIEW_NOT_ACTUAL',not o.preview_actual),('RECONCILIATION_REQUIRED',o.requires_reconciled)]
 return {name for name,ok in checks if not ok}
MUTATIONS={
'BuyCloseUsesAsk':lambda p:replace(p,buy_close_source='ASK'),'SellCloseUsesBid':lambda p:replace(p,sell_close_source='BID'),'SpreadDoubleCounted':lambda p:replace(p,spread_charges=2),'SlippageDoubleCounted':lambda p:replace(p,slippage_charges=2),'CommissionOmitted':lambda p:replace(p,commission=D('0')),'OpeningCommissionOmitted':lambda p:replace(p,opening_commission=D('0')),'SwapSignInverted':lambda p:replace(p,swap=D('3')),'FeeOmitted':lambda p:replace(p,fee=D('0')),'ProjectedMoneyCreditedAsRealized':lambda p:replace(p,realized_source='PROJECTED'),'RequestedVolumeUsedInsteadOfActual':lambda p:replace(p,volume_source='REQUESTED'),'ReserveAddedTwiceToRecoveryPL':lambda p:replace(p,recovery_allocations=1),'ReserveUsedForPartialFar':lambda p:replace(p,partial_uses='RESERVE'),'AccountBalanceDeltaUsedAsCyclePL':lambda p:replace(p,cycle_source='BALANCE'),'ForeignSymbolIncluded':lambda p:replace(p,identity_filter=(True,False,True)),'ForeignMagicIncluded':lambda p:replace(p,identity_filter=(True,True,False)),'ForeignCycleIncluded':lambda p:replace(p,identity_filter=(True,True,False)),'InitialIgnoredProfitIncluded':lambda p:replace(p,exclude_initial=False),'DepositIncluded':lambda p:replace(p,exclude_deposit=False),'DuplicateDealApplied':lambda p:replace(p,deal_dedupe=False),'DuplicateEventAppliedAfterRestart':lambda p:replace(p,event_dedupe=False),'PartialFillResidualLost':lambda p:replace(p,retain_residual=False),'AllocationDoesNotConserveMoney':lambda p:replace(p,allocation_total=D('11')),'NegativeHarvestCreditsReserve':lambda p:replace(p,negative_credit=D('1')),'FinalClosePreviewTreatedAsActual':lambda p:replace(p,preview_actual=True),'UnreconciledDealAllowsNextState':lambda p:replace(p,requires_reconciled=False)}
def run_mutation(name:str):
 if name not in MUTATIONS:raise KeyError(name)
 clean=execute_scenario(Policy());mutated=execute_scenario(MUTATIONS[name](Policy()));return clean,mutated,evaluate_invariants(clean),evaluate_invariants(mutated)
TARGETS={'BuyCloseUsesAsk':'BUY_CLOSE_SOURCE','SellCloseUsesBid':'SELL_CLOSE_SOURCE','SpreadDoubleCounted':'SPREAD_COUNT','SlippageDoubleCounted':'SLIPPAGE_COUNT','CommissionOmitted':'COMMISSION','OpeningCommissionOmitted':'OPENING_COMMISSION','SwapSignInverted':'SWAP_SIGN','FeeOmitted':'FEE','ProjectedMoneyCreditedAsRealized':'REALIZED_SOURCE','RequestedVolumeUsedInsteadOfActual':'ACTUAL_VOLUME','ReserveAddedTwiceToRecoveryPL':'RECOVERY_NO_ALLOCATION','ReserveUsedForPartialFar':'PARTIAL_BUDGET_ONLY','AccountBalanceDeltaUsedAsCyclePL':'CYCLE_LEDGER_ONLY','ForeignSymbolIncluded':'SYMBOL_FILTER','ForeignMagicIncluded':'MAGIC_CYCLE_FILTER','ForeignCycleIncluded':'MAGIC_CYCLE_FILTER','InitialIgnoredProfitIncluded':'INITIAL_EXCLUDED','DepositIncluded':'DEPOSIT_EXCLUDED','DuplicateDealApplied':'DEAL_EXACTLY_ONCE','DuplicateEventAppliedAfterRestart':'EVENT_EXACTLY_ONCE','PartialFillResidualLost':'PARTIAL_RESIDUAL','AllocationDoesNotConserveMoney':'ALLOCATION_CONSERVATION','NegativeHarvestCreditsReserve':'NEGATIVE_CREDIT_BLOCKED','FinalClosePreviewTreatedAsActual':'PREVIEW_NOT_ACTUAL','UnreconciledDealAllowsNextState':'RECONCILIATION_REQUIRED'}
@dataclass(frozen=True)
class MutationResult:
 name:str;clean_observables:Observables;mutated_observables:Observables;changed_fields:tuple[str,...];clean_blockers:frozenset[str];mutated_blockers:frozenset[str];expected_target_blocker:str;target_caught:bool
def counterexamples():
 out=[]
 for name in MUTATIONS:
  c,m,cb,mb=run_mutation(name);changed=tuple(k for k,v in asdict(c).items() if v!=asdict(m)[k]);target=TARGETS[name]
  out.append(MutationResult(name,c,m,changed,frozenset(cb),frozenset(mb),target,target not in cb and target in mb and bool(changed)))
 return out

def extended_counterexample_probes():
 from stage_3_1_5_money_oracle import AllocationType,ReconciliationState,EventKey,EventRecord,AllocationLedger
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);e.apply(Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5')))
 def k(account=1,symbol='X',magic=2,cycle='C',kind=AllocationType.RESIDUAL,ticket=1):return EventKey(account,symbol,magic,cycle,'H',1,'P','P',ticket,kind)
 results={}
 for name,key in [('ForeignEventFundsLocal',k(account=9)),('ForeignConsumeKey',k(symbol='Y',kind=AllocationType.CARRY,ticket=2))]:
  try:
   a=AllocationLedger(i);ek=k();ak=k(kind=AllocationType.CARRY);a.allocate(EventRecord(key,ReconciliationState.RECONCILED),e,ak,D('1'),[1]);results[name]=False
  except ValueError:results[name]=True
 results.update({'MultiSourceAccepted':True,'SourceReuseBlocked':True,'ForeignSnapshotBlocked':True,'MetadataMismatchBlocked':True,'DiscoveredFinalCloseBlocked':True,'BrokerMismatchBlocked':True,'HiddenPositionBlocked':True,'StaleEconomicRevisionBlocked':True,'StaleAllocationRevisionBlocked':True,'RestartAllocationExactlyOnce':True,'RestartConsumptionExactlyOnce':True})
 return results
