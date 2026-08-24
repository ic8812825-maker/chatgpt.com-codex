#!/usr/bin/env python3
"""Immutable broker evidence, structured price proofs and derived-state provenance."""
import argparse, copy, hashlib, json
from dataclasses import dataclass, asdict, field, is_dataclass
from decimal import Decimal, InvalidOperation
from types import MappingProxyType
from hsb_2e_primitive_validators_r4_r5 import D, on_grid, strict_revision
from hsb_2e_identity_model_r4_r5 import same_identity

def canon(x):
    if is_dataclass(x): return canon(asdict(x))
    if isinstance(x,Decimal): return str(x)
    if isinstance(x,dict): return {str(k):canon(v) for k,v in sorted(x.items(),key=lambda i:str(i[0]))}
    if isinstance(x,(list,tuple,set)): return [canon(v) for v in x]
    return x
def digest(x): return hashlib.sha256(json.dumps(canon(x),sort_keys=True,separators=(",",":")).encode()).hexdigest()

@dataclass(frozen=True)
class HSBI_ExecutionPriceProof:
    proofId:str; accountLogin:int; symbol:str; magic:int; cycleId:str; transactionId:str; actionId:str; stateRevision:int; snapshotId:str; snapshotVersion:int; positionTicket:int; direction:str
    snapshotBid:Decimal; snapshotAsk:Decimal; expectedCloseSide:str; tickSize:Decimal; minimumAllowedPrice:Decimal; maximumAllowedPrice:Decimal
    proofTimestamp:int; expiresTimestamp:int; policyId:str; sourceId:str; proofDigest:str=""
    def body(self): return {k:v for k,v in asdict(self).items() if k!="proofDigest"}
    def sealed(self): return self.__class__(**{**self.body(),"proofDigest":digest(self.body())})

@dataclass(frozen=True)
class HSBI_DealEvidenceRecord:
    schemaVersion:int; accountLogin:int; symbol:str; magic:int; cycleId:str; transactionId:str; actionId:str; stateRevision:int; snapshotId:str; snapshotVersion:int
    dealId:str; eventId:str; orderId:str; positionTicket:int; positionRole:str; direction:str; volume:Decimal; price:Decimal; profit:Decimal; commission:Decimal; swap:Decimal; fee:Decimal; netMoney:Decimal
    confirmed:bool; dealTimestamp:int; receivedSequence:int; executionPriceProofId:str; sourceDigest:str; recordDigest:str=""
    def body(self): return {k:v for k,v in asdict(self).items() if k!="recordDigest"}
    def sealed(self): return self.__class__(**{**self.body(),"recordDigest":digest(self.body())})

@dataclass(frozen=True)
class HSBI_SettlementCommitCertificate:
    schemaVersion:int; settlementId:str; accountLogin:int; symbol:str; magic:int; cycleId:str; transactionId:str; actionId:str; inputStateRevision:int; outputStateRevision:int; snapshotId:str; snapshotVersion:int; scenario:str; requiredPositionTickets:tuple; fullFillProofDigest:str; dealLedgerDigest:str; economicProposalDigest:str; allocationDigest:str; persistenceDigest:str; fsmTransitionId:str; committedSequence:int; certificateDigest:str=""
    def body(self): return {k:v for k,v in asdict(self).items() if k!="certificateDigest"}
    def sealed(self): return self.__class__(**{**self.body(),"certificateDigest":digest(self.body())})

def validate_price_proof(proof,record):
    if not isinstance(proof,HSBI_ExecutionPriceProof) or proof.proofDigest!=digest(proof.body()): return "EXECUTION_PRICE_PROOF_INVALID"
    if not same_identity(asdict(proof),asdict(record)): return "EXECUTION_PRICE_PROOF_IDENTITY_MISMATCH"
    if proof.positionTicket!=record.positionTicket or proof.direction!=record.direction or proof.proofId!=record.executionPriceProofId:return "EXECUTION_PRICE_PROOF_IDENTITY_MISMATCH"
    if not proof.policyId or not proof.sourceId:return "EXECUTION_PRICE_POLICY_UNRESOLVED"
    if proof.proofTimestamp>record.dealTimestamp or record.dealTimestamp>proof.expiresTimestamp:return "EXECUTION_PRICE_PROOF_STALE"
    if proof.minimumAllowedPrice>record.price or record.price>proof.maximumAllowedPrice:return "EXECUTION_PRICE_PROOF_INVALID"
    if proof.expectedCloseSide != ("BID" if record.direction=="BUY" else "ASK"):return "EXECUTION_PRICE_PROOF_INVALID"
    return None

def validate_record(record,proof,ctx):
    if not isinstance(record,HSBI_DealEvidenceRecord):return "DEAL_SCHEMA_INVALID"
    if record.recordDigest!=digest(record.body()):return "SOURCE_RECORD_DIGEST_MISMATCH"
    if type(record.confirmed) is not bool or not record.confirmed:return "DEAL_NOT_CONFIRMED"
    if not same_identity(asdict(record),ctx):return "DEAL_IDENTITY_MISMATCH"
    if any(not strict_revision(getattr(record,k),k in {"snapshotVersion","schemaVersion"}) for k in ("stateRevision","snapshotVersion","schemaVersion")):return "REVISION_DOMAIN_INVALID"
    if record.netMoney != record.profit+record.commission+record.swap+record.fee:return "DEAL_MONEY_RECORD_MISMATCH"
    try:
        if record.volume<=0 or record.price<=0:return "NUMERIC_DOMAIN_INVALID"
        if not on_grid(record.volume,D(ctx["volumeStep"])):return "VOLUME_OFF_GRID"
        if not on_grid(record.price,D(ctx["tickSize"])):return "PRICE_OFF_GRID"
    except (KeyError,InvalidOperation,TypeError):return "NUMERIC_DOMAIN_INVALID"
    return validate_price_proof(proof,record)

def derive(records):
    consumed=[];seen=[];bindings={};volume={};money_deal={};money_ticket={}
    for r in records:
        consumed.append(r.dealId);seen.append(r.eventId);bindings[r.dealId]=r.eventId;t=str(r.positionTicket)
        volume[t]=volume.get(t,D(0))+r.volume;money_deal[r.dealId]=r.netMoney;money_ticket[t]=money_ticket.get(t,D(0))+r.netMoney
    return {"consumedDealIds":consumed,"seenEventIds":seen,"dealEventBindings":bindings,"cumulativeFills":volume,"moneyByDeal":money_deal,"moneyByTicket":money_ticket}

def validate_persisted(state):
    records=state.get("acceptedDealRecords",[])
    cache_fields=("consumedDealIds","seenEventIds","dealEventBindings","cumulativeFills","moneyByDeal","moneyByTicket")
    if not records and any(state.get(k) for k in cache_fields):return "CUMULATIVE_FILL_PROVENANCE_MISSING"
    derived=derive(records)
    if any(canon(state.get(k,{} if k not in ("consumedDealIds","seenEventIds") else []))!=canon(derived[k]) for k in cache_fields):return "PERSISTED_DERIVED_STATE_MISMATCH"
    if set(derived["dealEventBindings"])!=set(derived["consumedDealIds"]) or set(derived["dealEventBindings"].values())!=set(derived["seenEventIds"]) or set(derived["moneyByDeal"])!=set(derived["consumedDealIds"]):return "PERSISTED_REGISTRY_BIJECTION_INVALID"
    return None

def validate_all_then_apply(state,records,proofs,ctx):
    before=digest(state); error=validate_persisted(state)
    if error:return state,error
    known_d=set(state.get("consumedDealIds",[]));known_e=set(state.get("seenEventIds",[]));batch_d=set();batch_e=set()
    proof_map={p.proofId:p for p in proofs}
    for r in records:
        if r.dealId in known_d|batch_d:return state,"DEAL_ALREADY_CONSUMED"
        if r.eventId in known_e|batch_e:return state,"EVENT_ALREADY_SEEN"
        error=validate_record(r,proof_map.get(r.executionPriceProofId),ctx)
        if error:return state,error
        batch_d.add(r.dealId);batch_e.add(r.eventId)
    if not records:return state,"EMPTY_BATCH"
    out=copy.deepcopy(state);out["acceptedDealRecords"]=list(state.get("acceptedDealRecords",[]))+list(records);out.update(derive(out["acceptedDealRecords"]));out["evidenceRevision"]=state.get("evidenceRevision",0)+1
    assert digest(state)==before
    return out,None

def validate_certificate(cert,expected):
    if not isinstance(cert,HSBI_SettlementCommitCertificate):return "COMMIT_CERTIFICATE_MISSING"
    if cert.certificateDigest!=digest(cert.body()):return "COMMIT_CERTIFICATE_DIGEST_INVALID"
    if cert.outputStateRevision!=cert.inputStateRevision+1:return "COMMIT_CERTIFICATE_REVISION_INVALID"
    for k,v in expected.items():
        if getattr(cert,k,None)!=v:return "COMMIT_CERTIFICATE_IDENTITY_MISMATCH"
    return None

def self_test():
    ctx={"accountLogin":1,"symbol":"EURUSD","magic":7,"cycleId":"C","transactionId":"TX","actionId":"A","stateRevision":3,"snapshotId":"S","snapshotVersion":2,"volumeStep":".01","tickSize":".00001"}
    p=HSBI_ExecutionPriceProof("P",1,"EURUSD",7,"C","TX","A",3,"S",2,1,"BUY",D("1.1"),D("1.2"),"BID",D(".00001"),D("1.1"),D("1.1"),1900,2200,"EXACT_SIDE","SNAPSHOT").sealed()
    r=HSBI_DealEvidenceRecord(1,1,"EURUSD",7,"C","TX","A",3,"S",2,"D","E","O",1,"BIG","BUY",D("1"),D("1.1"),D("10"),D("-1"),D(0),D(0),D(9),True,2000,1,"P","SRC").sealed()
    s={"acceptedDealRecords":[],"consumedDealIds":[],"seenEventIds":[],"dealEventBindings":{},"cumulativeFills":{},"moneyByDeal":{},"moneyByTicket":{},"evidenceRevision":0}
    out,e=validate_all_then_apply(s,[r],[p],ctx);bad=copy.deepcopy(s);bad["cumulativeFills"]={"1":D(1)}
    checks=[e is None,out["moneyByTicket"]["1"]==9,validate_persisted(out) is None,validate_persisted(bad)=="CUMULATIVE_FILL_PROVENANCE_MISSING"]
    print(f"PROVENANCE_R4_R5_SELF_TESTS={sum(checks)}/{len(checks)}");return all(checks)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
