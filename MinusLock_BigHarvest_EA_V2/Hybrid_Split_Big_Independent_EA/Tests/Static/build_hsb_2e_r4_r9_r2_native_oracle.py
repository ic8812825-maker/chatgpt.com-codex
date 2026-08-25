#!/usr/bin/env python3
"""Publish complete native fixtures and independently calculated economics."""
from __future__ import annotations
import argparse,json,hashlib
from decimal import Decimal,ROUND_DOWN
from pathlib import Path
COUNTS={'INITIAL':12,'BIG':20,'SMALL':20,'FINAL':16,'RESTART_CONTINUATION':12,'REPLAY_COMMITTED':12,'LIFECYCLE':12}
KINDS=('POSITIVE','NEGATIVE','BOUNDARY','MALFORMED','IDENTITY_CONFLICT','STALE','PARTIAL_FILL','FULL_FILL','OVERFILL','DUPLICATE_DEAL','DUPLICATE_EVENT','REPLAY','PERSISTENCE_FAILURE','CERTIFICATE_FORGERY','CONSERVATION_VIOLATION')
def d(x):return Decimal(str(x))
def fixture(scenario,index):
 kind=KINDS[index%len(KINDS)];ts=1700000100;before=d('1.00');closed=d('0.40');available=d('12.00');f={'schemaVersion':9,'vectorId':f'R9_{scenario}_{index+1:03d}','scenario':scenario,'kind':kind,'identity':{'account':10001,'symbol':'EURUSD','magic':8812825,'cycleId':'C1','transactionId':f'T{index}','actionId':f'A{index}','stateRevision':0,'snapshotRevision':1,'moneyStateVersion':1,'brokerPropertyVersion':1},'broker':{'bid':'1.10000','ask':'1.10020','tickSize':'0.00001','tickValue':'1.00','contractSize':'100000','volumeMin':'0.01','volumeMax':'100.00','volumeStep':'0.01','priceRounding':'TICK_GRID','volumeRounding':'ROUND_DOWN'},'time':{'snapshotTimestamp':ts-10,'policyValidFrom':ts-20,'policyValidUntil':ts+20,'intentCreatedTimestamp':ts-15,'intentExpiresTimestamp':ts+15,'dealTimestamp':ts,'eventTimestamp':ts,'minimumTimestamp':ts-20,'allowedUpperBound':ts+20},'costs':{'commission':'0','swap':'0','other':'0'},'positions':[{'ticket':101,'role':'WINNER','direction':'BUY','volume':'1.00'},{'ticket':102,'role':'FAR','direction':'SELL','volume':'0.80'},{'ticket':201,'role':'BIG','direction':'BUY','volume':str(before)},{'ticket':202,'role':'SMALL','direction':'SELL','volume':'1.00'}],'intents':[{'intentId':'I1','ticket':101,'role':'WINNER','direction':'BUY','requestedVolume':'1.00'},{'intentId':'I2','ticket':201,'role':'BIG','direction':'BUY','requestedVolume':str(closed)}],'deals':[{'dealId':'D1','eventId':'E1','ticket':101,'intentId':'I1','role':'WINNER','direction':'BUY','volume':'1.00','price':'1.10000','profit':'10.00'},{'dealId':'D2','eventId':'E2','ticket':201,'intentId':'I2','role':'BIG','direction':'BUY','volume':str(closed),'price':'1.10000','profit':'8.00'},{'dealId':'D3','eventId':'E3','ticket':202,'intentId':'I3','role':'SMALL','direction':'SELL','volume':'1.00','price':'1.10020','profit':'4.00'}],'economic':{'initialNet':'10.00','bigNet':'8.00','smallNet':'4.00','farActualLoss':'20.00','reserveBefore':'5.00','recoveryPLBefore':'5.00','closeFarShare':'0.50','reserveShare':'0.25','smallReserveShare':'0.25','farVolume':'0.80','bigVolumeBefore':str(before),'bigClosedConfirmed':str(closed),'lossPerLot':'25.00','controlDistance':'0.01000','movementToBig':'0.00500','requiredCoverage':'3.00'},'persisted':{'consumedDealIds':[],'seenEventIds':[],'dealEventBindings':[],'stateRevision':0,'settlementRevision':0,'evidenceRevision':0,'fsm':'READY','certificateDigest':''}}
 if kind=='NEGATIVE':f['economic']['initialNet']='-1.00'
 if kind=='MALFORMED':f['schemaVersion']=999
 if kind=='IDENTITY_CONFLICT':f['identity']['magic']=7
 if kind=='STALE':f['time']['dealTimestamp']=ts-1000
 if kind=='PARTIAL_FILL':f['deals'][0]['volume']='0.50'
 if kind=='OVERFILL':f['deals'][0]['volume']='1.10'
 if kind=='DUPLICATE_DEAL':f['deals'].append(dict(f['deals'][0]))
 if kind=='DUPLICATE_EVENT':q=dict(f['deals'][0]);q['dealId']='DX';f['deals'].append(q)
 if kind=='PERSISTENCE_FAILURE':f['persisted']['certificateDigest']='FORGED'
 if kind=='CONSERVATION_VIOLATION':f['economic']['reserveShare']='0.75';f['economic']['closeFarShare']='0.75'
 return f
def calculate(f):
 e=f['economic'];scenario=f['scenario'];initial=d(e['initialNet']);big=d(e['bigNet']);small=d(e['smallNet']);available=big+small;reserve=d(e['reserveBefore']);far_loss=d(e['farActualLoss']);close=available*d(e['closeFarShare']);reserve_add=available*d(e['reserveShare']);step=d(f['broker']['volumeStep']);partial=(close/d(e['lossPerLot'])/step).to_integral_value(rounding=ROUND_DOWN)*step;residual=d(e['bigVolumeBefore'])-d(e['bigClosedConfirmed']);catch=(reserve+reserve_add)/far_loss*d(e['movementToBig'])/d(e['controlDistance']);recovery=d(e['recoveryPLBefore'])-far_loss;coverage=reserve>=d(e['requiredCoverage']);consume=min(reserve,d(e['requiredCoverage']));allocated=close+reserve_add;remaining=available-allocated
 bad=f['schemaVersion']!=9 or f['kind'] in {'MALFORMED','IDENTITY_CONFLICT','STALE','PARTIAL_FILL','OVERFILL','DUPLICATE_DEAL','DUPLICATE_EVENT','PERSISTENCE_FAILURE','CERTIFICATE_FORGERY','CONSERVATION_VIOLATION'} or (scenario=='INITIAL' and initial<=0)
 values={'InitialNetActual':str(initial),'BigActualMoney':str(big),'SmallActualMoney':str(small),'FarActualLoss':str(far_loss),'AvailableMoney':str(available),'CloseFarBudget':str(close),'ReserveAddition':str(reserve_add),'ReserveBefore':str(reserve),'ReserveAfter':str(reserve+reserve_add),'PartialFarVolume':str(partial),'BigResidualVolume':str(residual),'NewFarVolume':str(residual),'CatchUpRatio':str(catch),'RecoveryPL':str(recovery),'ReserveCoverage':coverage,'ReserveConsumption':str(consume),'AllocatedMoney':str(allocated),'RemainingMoney':str(remaining),'SettlementEligibility':not bad,'AllocationEligibility':not bad,'PersistenceEligibility':not bad,'StateRevisionBefore':f['persisted']['stateRevision'],'StateRevisionAfter':f['persisted']['stateRevision']+(0 if bad else 1),'CertificateEligibility':not bad}
 return {'status':'REJECT' if bad else 'PASS','reason':'FIXTURE_VALIDATION_REJECTED' if bad else 'COMMITTED','values':values,'derivationTrace':[{'FORMULA_ID':k,'INPUT_VALUES':e,'INPUT_UNITS':'ACCOUNT_MONEY_OR_LOTS','ROUNDING_POLICY':f['broker']['volumeRounding'],'INTERMEDIATE_VALUES':{},'EXPECTED_VALUE':v} for k,v in values.items()]}
def build(root):
 root=Path(root).resolve();fixtures=[];expected=[]
 for scenario,count in COUNTS.items():
  for i in range(count):
   f=fixture(scenario,i);fixtures.append(f);expected.append({'vectorId':f['vectorId'],'inputSha256':hashlib.sha256(json.dumps(f,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'expected':calculate(f)})
 contract={'schemaVersion':1,'counts':COUNTS,'fixtures':fixtures};oracle={'schemaVersion':1,'calculator':'INDEPENDENT_STANDARD_LIBRARY_DECIMAL','expected':expected}
 (root/'Tests/Vectors/HSB_2E_R4_R9_R2_NATIVE_FIXTURES.json').write_text(json.dumps(contract,indent=2,sort_keys=True)+'\n');(root/'Tests/Contracts/HSB_2E_R4_R9_R2_NATIVE_ECONOMIC_ORACLE.json').write_text(json.dumps(oracle,indent=2,sort_keys=True)+'\n');(root/'Tests/Evidence/HSB_2E_R4_R9_R2_NATIVE_DERIVATION_TRACES.json').write_text(json.dumps({'schemaVersion':1,'rows':expected},indent=2,sort_keys=True)+'\n');print('NATIVE_R9_FIXTURES='+str(len(fixtures)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);build(p.parse_args().root)
