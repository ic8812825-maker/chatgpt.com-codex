#!/usr/bin/env python3
"""Sealed R4-R6 economic policy and money/volume-conserving settlement."""
from dataclasses import dataclass,asdict
from decimal import Decimal,ROUND_DOWN
from hsb_2e_provenance_model_r4_r6 import D,digest,grid

@dataclass(frozen=True)
class HSBI_EconomicPolicy:
    schemaVersion:int;scenario:str;cycleId:str;actionId:str;transactionId:str;stateRevision:int;snapshotRevision:int;units:str;roundingMode:str;volumeStep:Decimal;volumeMin:Decimal;volumeMax:Decimal;closeFarShare:Decimal;reserveShare:Decimal;smallReserveShare:Decimal;farLossBefore:Decimal;farVolumeBefore:Decimal;reserveBefore:Decimal;recoveryPLBefore:Decimal;formulaIds:tuple;normativeSourceIds:tuple;policyDigest:str=''
    def body(self):return {k:v for k,v in asdict(self).items() if k!='policyDigest'}
    def sealed(self):return self.__class__(**{**self.body(),'policyDigest':digest(self.body())})

@dataclass(frozen=True)
class HSBI_EconomicProposal:
    scenario:str;availableMoney:Decimal;allocatedMoney:Decimal;remainingMoney:Decimal;actualMoneyByTicket:dict;actualMoneyByRole:dict;closeFarBudget:Decimal;reserveAddition:Decimal;smallReserveAddition:Decimal;partialFarVolume:Decimal;reserveConsumed:Decimal;reserveAfter:Decimal;recoveryPLAfter:Decimal;farVolumeAfter:Decimal;newFarTicket:int;newFarVolume:Decimal;catchUpRatio:Decimal;dualTail:bool;finalCloseAllowed:bool;allocationAttribution:dict;brokerProposalDigest:str;policyDigest:str;proposalDigest:str=''
    def body(self):return {k:v for k,v in asdict(self).items() if k!='proposalDigest'}
    def sealed(self):return self.__class__(**{**self.body(),'proposalDigest':digest(self.body())})

def validate_policy(p,scenario,context,snapshot):
    if not isinstance(p,HSBI_EconomicPolicy) or p.policyDigest!=digest(p.body()):return 'ECONOMIC_POLICY_DIGEST_INVALID'
    if p.schemaVersion!=1 or p.scenario!=scenario or p.cycleId!=context['cycleId'] or p.actionId!=context['actionId'] or p.transactionId!=context['transactionId'] or p.stateRevision!=context['stateRevision'] or p.snapshotRevision!=snapshot.snapshotRevision:return 'ECONOMIC_POLICY_IDENTITY_INVALID'
    if p.units!='ACCOUNT_CURRENCY_AND_LOTS' or p.roundingMode!='ROUND_DOWN':return 'ECONOMIC_POLICY_UNITS_INVALID'
    shares=(p.closeFarShare,p.reserveShare,p.smallReserveShare)
    if any(not x.is_finite() or x<0 or x>1 for x in shares):return 'ALLOCATION_SHARE_RANGE_INVALID'
    active=(p.closeFarShare+p.reserveShare) if scenario=='BIG' else p.smallReserveShare if scenario=='SMALL' else D(0)
    if active>1:return 'ALLOCATION_SHARE_SUM_INVALID'
    monetary=(p.farLossBefore,p.reserveBefore,p.recoveryPLBefore)
    if any(not x.is_finite() for x in monetary) or p.farLossBefore<0 or p.reserveBefore<0:return 'ECONOMIC_MONEY_DOMAIN_INVALID'
    if not grid(p.farVolumeBefore,p.volumeStep) or p.farVolumeBefore<p.volumeMin or p.farVolumeBefore>p.volumeMax:return 'ECONOMIC_VOLUME_DOMAIN_INVALID'
    return None

def down_volume(value,p):
    v=(D(value)/p.volumeStep).to_integral_value(rounding=ROUND_DOWN)*p.volumeStep
    return D(0) if v<p.volumeMin else min(v,p.volumeMax)

def build_economic_proposal(scenario,broker,p,positions,full_fill):
    error=validate_policy(p,scenario,broker['context'],broker['snapshot'])
    if error:return None,error
    if not full_fill:return None,'FULL_FILL_REQUIRED'
    by_ticket=broker['moneyByTicket'];by_role=broker['moneyByRole'];available=sum(by_ticket.values(),D(0));close=reserve_add=small_add=partial=reserve_used=D(0);far_after=p.farVolumeBefore;new_ticket=0;new_volume=D(0);catch=D(0);dual=False;final=False;recovery=p.recoveryPLBefore
    attribution={}
    if scenario=='INITIAL':
        if available<=0:return None,'INITIAL_NET_NOT_POSITIVE'
        # Initial profit is intentionally excluded from RecoveryPL and allocation.
    elif scenario=='BIG':
        if set(by_role)!={'BIG','SMALL'}:return None,'BIG_MANDATORY_LEGS_INVALID'
        projected_recovery=p.recoveryPLBefore+available-p.farLossBefore
        if p.farLossBefore<=available+p.reserveBefore and projected_recovery>0:final=True
        else:
            positive=max(D(0),available);close=positive*p.closeFarShare;reserve_add=positive*p.reserveShare
            loss_per_lot=p.farLossBefore/p.farVolumeBefore if p.farVolumeBefore else D(0)
            partial=down_volume(close/loss_per_lot,p) if loss_per_lot>0 else D(0)
            if partial>=p.farVolumeBefore:partial=max(D(0),p.farVolumeBefore-p.volumeStep)
            far_after=p.farVolumeBefore-partial;attribution={'CLOSE_FAR':close,'RESERVE':reserve_add}
            recovery=p.recoveryPLBefore+available-close-reserve_add
    elif scenario=='SMALL':
        if not {'SMALL','OLD_FAR','BIG'}.issubset(by_role):return None,'SMALL_MANDATORY_LEGS_INVALID'
        big=next((q for q in positions if q['role']=='BIG'),None);old=next((q for q in positions if q['role']=='OLD_FAR'),None)
        if not big or not old:return None,'NEW_FAR_SOURCE_MISSING'
        new_volume=down_volume(big.get('residualVolume','0'),p);new_ticket=big['ticket'];far_after=new_volume;dual=old.get('remainingVolume','0') not in ('0',0,D(0))
        if new_volume<=0 or new_volume>=p.farVolumeBefore:return None,'NEW_FAR_COMPRESSION_INVALID'
        if dual:return None,'DUAL_TAIL'
        small_add=max(D(0),available)*p.smallReserveShare;attribution={'SMALL_RESERVE':small_add};recovery=p.recoveryPLBefore+available-small_add;catch=(p.reserveBefore+small_add)/p.farLossBefore if p.farLossBefore>0 else D(1)
    elif scenario=='FINAL':
        projected=p.recoveryPLBefore+available-p.farLossBefore
        reserve_used=max(D(0),p.farLossBefore-available)
        if projected<=0 or reserve_used>p.reserveBefore:return None,'FINAL_ECONOMIC_GATES_FAILED'
        final=True;far_after=D(0);recovery=projected;attribution={'FAR_LOSS_FROM_DEALS':min(available,p.farLossBefore),'FAR_LOSS_FROM_RESERVE':reserve_used}
    else:return None,'UNKNOWN_SCENARIO'
    allocated=close+reserve_add+small_add;remaining=available-allocated
    if allocated>available or remaining<0 or allocated+remaining!=available:return None,'MONEY_CONSERVATION_FAILED'
    reserve_after=p.reserveBefore+reserve_add+small_add-reserve_used
    proposal=HSBI_EconomicProposal(scenario,available,allocated,remaining,by_ticket,by_role,close,reserve_add,small_add,partial,reserve_used,reserve_after,recovery,far_after,new_ticket,new_volume,catch,dual,final,attribution,broker['brokerProposalDigest'],p.policyDigest).sealed()
    return proposal,None
