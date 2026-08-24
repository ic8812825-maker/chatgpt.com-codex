"""Deterministic builders; fixtures are derived and never production sources."""
from dataclasses import asdict
from hsb_2e_provenance_model_r4_r5 import *
ROLES={"INITIAL":[("WINNER","BUY","1")],"BIG":[("BIG","BUY","1"),("SMALL","SELL",".5")],"SMALL":[("SMALL","BUY",".25"),("OLD_FAR","SELL","1"),("BIG","BUY",".5")],"FINAL":[("FAR","SELL","1")]}
def scenario_input(scenario,money="9"):
 c={"accountLogin":1,"symbol":"EURUSD","magic":7,"cycleId":"C","transactionId":"TX","actionId":"A","stateRevision":3,"snapshotId":"S","snapshotVersion":2,"volumeStep":".01","tickSize":".00001"}
 ps=[];its=[];records=[];proofs=[]
 for n,(role,direction,volume) in enumerate(ROLES[scenario],1):
  ticket=100+n;price=D("1.10000" if direction=="BUY" else "1.20000");side="BID" if direction=="BUY" else "ASK";proof=HSBI_ExecutionPriceProof(f"P{ticket}",1,"EURUSD",7,"C","TX","A",3,"S",2,ticket,direction,D("1.1"),D("1.2"),side,D(".00001"),price,price,1900,2200,"EXACT_SIDE","SNAPSHOT").sealed();proofs.append(proof)
  net=D(money);record=HSBI_DealEvidenceRecord(1,1,"EURUSD",7,"C","TX","A",3,"S",2,f"D{ticket}",f"E{ticket}",f"O{ticket}",ticket,role,direction,D(volume),price,net,D(0),D(0),D(0),net,True,2000,n,proof.proofId,"BROKER").sealed();records.append(record)
  ps.append({"positionTicket":ticket,"role":role,"direction":direction,"positionVolume":volume});its.append({"positionTicket":ticket,"intentId":f"I{ticket}","intentKind":"FULL_CLOSE","requestedVolume":volume})
 state={"acceptedDealRecords":[],"consumedDealIds":[],"seenEventIds":[],"dealEventBindings":{},"cumulativeFills":{},"moneyByDeal":{},"moneyByTicket":{},"evidenceRevision":0,"settlementRevision":0,"persistenceSchemaVersion":1,"settlementCommitted":False}
 policy={"farLossBefore":"10","farVolumeBefore":"1","reserveBefore":"20" if scenario=="FINAL" else "0","recoveryPLBefore":"1","closeFarShare":".1","reserveShare":".9","smallReserveShare":".05","fullCloseProven":True,"newFarTicketSource":103,"newFarVolume":".5","oldFarRemains":False,"pendingReconciliation":False,"dualTail":False}
 return {"scenario":scenario,"context":c,"positions":ps,"intents":its,"dealRecords":records,"priceProofs":proofs,"persistedState":state,"economicPolicy":policy}
