#!/usr/bin/env python3
"""Economic contour consuming only a sealed broker settlement proposal."""
import argparse
from dataclasses import dataclass,asdict
from decimal import Decimal
from hsb_2e_provenance_model_r4_r5 import D,digest

@dataclass(frozen=True)
class HSBI_EconomicSettlementProposal:
    scenario:str;cycleId:str;actionId:str;transactionId:str;stateRevision:int;actualMoneyByTicket:dict;actualMoneyByRole:dict;totalActualNetMoney:Decimal
    farLossBefore:Decimal;farVolumeBefore:Decimal;reserveBefore:Decimal;recoveryPLBefore:Decimal;closeFarBudget:Decimal;reserveAddition:Decimal;smallReserveAddition:Decimal;partialFarVolume:Decimal
    farVolumeAfter:Decimal;reserveAfter:Decimal;recoveryPLAfter:Decimal;newFarTicketSource:int;newFarVolume:Decimal;dualTail:bool;finalCloseAllowed:bool
    brokerProposalDigest:str;formulaContractIds:tuple;allocationPolicyDigest:str;economicProposalDigest:str=""
    def body(self):return {k:v for k,v in asdict(self).items() if k!="economicProposalDigest"}
    def sealed(self):return self.__class__(**{**self.body(),"economicProposalDigest":digest(self.body())})

def build_economic_proposal(broker,policy):
    if type(broker) is not dict or broker.get("sealed") is not True or broker.get("brokerProposalDigest")!=digest({k:v for k,v in broker.items() if k!="brokerProposalDigest"}):return None,"BROKER_PROPOSAL_UNSEALED"
    scenario=broker["scenario"];by_ticket=broker["moneyByTicket"];by_role=broker["moneyByRole"];total=sum(map(D,by_ticket.values()),D(0))
    if D(policy.get("reserveUsedForPartialFar",0))!=0:return None,"RESERVE_USED_FOR_PARTIAL_FAR"
    far_loss=D(policy["farLossBefore"]);far_volume=D(policy["farVolumeBefore"]);reserve=D(policy["reserveBefore"]);recovery=D(policy["recoveryPLBefore"])
    close_share=D(policy["closeFarShare"]);reserve_share=D(policy["reserveShare"]);small_share=D(policy["smallReserveShare"])
    close_budget=reserve_add=small_add=partial=D(0);far_after=far_volume;new_ticket=0;new_volume=D(0);dual=False;final=False
    if scenario=="INITIAL":
        if total<=0:return None,"INITIAL_NET_NOT_POSITIVE"
    elif scenario=="BIG":
        if set(by_role)!={"BIG","SMALL"}:return None,"BIG_MANDATORY_LEGS_INVALID"
        if far_loss<=total+reserve and recovery+total-far_loss>0:final=True
        else:close_budget=max(D(0),total)*close_share;reserve_add=max(D(0),total)*reserve_share
    elif scenario=="SMALL":
        if not {"SMALL","OLD_FAR","BIG"}.issubset(by_role):return None,"SMALL_MANDATORY_LEGS_INVALID"
        small_add=max(D(0),total)*small_share;new_ticket=int(policy["newFarTicketSource"]);new_volume=D(policy["newFarVolume"]);far_after=new_volume;dual=bool(policy.get("oldFarRemains",False))
        if dual:return None,"DUAL_TAIL"
        if new_volume<=0 or new_volume>=far_volume:return None,"NEW_FAR_COMPRESSION_INVALID"
    elif scenario=="FINAL":
        final=bool(policy["fullCloseProven"]) and recovery+total>0 and reserve>=far_loss and not policy.get("pendingReconciliation",False) and not policy.get("dualTail",False)
        if not final:return None,"FINAL_ECONOMIC_GATES_FAILED"
        far_after=D(0)
    else:return None,"UNKNOWN_SCENARIO"
    after_recovery=recovery+total-close_budget;after_reserve=reserve+reserve_add+small_add
    p=HSBI_EconomicSettlementProposal(scenario,broker["cycleId"],broker["actionId"],broker["transactionId"],broker["stateRevision"],by_ticket,by_role,total,far_loss,far_volume,reserve,recovery,close_budget,reserve_add,small_add,partial,far_after,after_reserve,after_recovery,new_ticket,new_volume,dual,final,broker["brokerProposalDigest"],("DEAL_NET_ACTUAL","ALLOC_R4_R3","RECOVERY_ACTUAL"),digest(policy)).sealed()
    return p,None

def self_test():
    base={"scenario":"INITIAL","cycleId":"C","actionId":"A","transactionId":"T","stateRevision":1,"moneyByTicket":{"1":D(1)},"moneyByRole":{"WINNER":D(1)},"sealed":True};base["brokerProposalDigest"]=digest(base)
    policy={"farLossBefore":"10","farVolumeBefore":"1","reserveBefore":"0","recoveryPLBefore":"0","closeFarShare":".1","reserveShare":".9","smallReserveShare":".05","fullCloseProven":True}
    p,e=build_economic_proposal(base,policy);base2=dict(base);base2["moneyByTicket"]={"1":D(-1)};base2["moneyByRole"]={"WINNER":D(-1)};base2["brokerProposalDigest"]=digest({k:v for k,v in base2.items() if k!="brokerProposalDigest"})
    checks=[e is None,p.totalActualNetMoney==1,build_economic_proposal(base2,policy)[1]=="INITIAL_NET_NOT_POSITIVE"]
    print(f"ECONOMIC_R4_R5_SELF_TESTS={sum(checks)}/{len(checks)}");return all(checks)
if __name__=="__main__":p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
