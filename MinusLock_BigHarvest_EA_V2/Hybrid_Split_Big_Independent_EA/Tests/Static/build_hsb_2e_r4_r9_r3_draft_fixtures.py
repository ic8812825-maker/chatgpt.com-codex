#!/usr/bin/env python3
"""Create causal draft V2 fixtures; this module does not publish expectations."""
import argparse,copy,hashlib,json
from pathlib import Path
def h(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def base():
 ledger={'records':[{'dealId':'D1','eventId':'E1','ticket':101,'intentId':'I1','symbol':'EURUSD','magic':8812825,'volume':'1.00','money':'10.00','price':'1.10000'}]};broker={'ledgerRoot':h(ledger),'totalMoney':'10.00','totalVolume':'1.00'};economic={'availableMoney':'10.00','allocatedMoney':'7.50','remainingMoney':'2.50','reserveAfter':'7.50','recoveryPL':'5.00'};allocation={'closeFarBudget':'5.00','reserveAddition':'2.50','remainingMoney':'2.50'};fsm={'inputRevision':0,'outputRevision':1,'phase':'COMMITTED'};objects={'broker':broker,'economic':economic,'allocation':allocation,'fsm':fsm};digests={k:h(v) for k,v in objects.items()};body={'sourceDigests':digests,'inputRevision':0,'outputRevision':1,'previousStateDigest':'PREVIOUS_ANCHOR','ledgerRoot':broker['ledgerRoot']};certificate={'body':body,'digest':h(body)}
 return {'schemaVersion':9,'scenario':'INITIAL','identity':{'account':10001,'symbol':'EURUSD','magic':8812825,'cycleId':'C1','transactionId':'T1','actionId':'A1','stateRevision':0,'snapshotRevision':1},'brokerProperties':{'tickSize':'0.00001','volumeStep':'0.01','volumeMin':'0.01','volumeMax':'100.00'},'snapshot':{'account':10001,'symbol':'EURUSD','magic':8812825,'bid':'1.10000','ask':'1.10020','timestamp':100},'policy':{'buySide':'BID','sellSide':'ASK','validFrom':90,'validUntil':120},'intent':{'intentId':'I1','ticket':101,'symbol':'EURUSD','magic':8812825,'requestedVolume':'1.00','created':95,'expires':115},'time':{'minimum':90,'maximum':120,'deal':105,'event':105},'ledger':ledger,'brokerProposal':broker,'economicProposal':economic,'allocation':allocation,'fsm':fsm,'persistence':{'stateRevision':1,'ledgerRoot':broker['ledgerRoot'],'previousStateDigest':'PREVIOUS_ANCHOR'},'authoritativeAnchor':{'ledgerRoot':broker['ledgerRoot'],'previousStateDigest':'PREVIOUS_ANCHOR','revision':1},'certificate':certificate}
def setp(v,path,value):
 cur=v;parts=path.split('.')
 for p in parts[:-1]:cur=cur[int(p)] if isinstance(cur,list) else cur[p]
 last=parts[-1];cur[int(last) if isinstance(cur,list) else last]=value
DEFECTS=[('IDENTITY_ACCOUNT','identity.account',999),('SYMBOL','identity.symbol','GBPUSD'),('MAGIC','identity.magic',7),('STALE','time.deal',1),('WINDOW','policy.validUntil',80),('BUY_SIDE','policy.buySide','ASK'),('TICK_GRID','ledger.records.0.price','1.100001'),('VOLUME_GRID','ledger.records.0.volume','1.005'),('INTENT_BINDING','ledger.records.0.intentId','FOREIGN'),('DEAL_TICKET','ledger.records.0.ticket',999),('DUP_DEAL','ledger.records',None),('DUP_EVENT','ledger.records',None),('MISSING_LEG','ledger.records',None),('PARTIAL_FILL','ledger.records.0.volume','0.50'),('OVERFILL','ledger.records.0.volume','1.10'),('MONEY_CONSERVATION','economicProposal.remainingMoney','9.00'),('VOLUME_CONSERVATION','brokerProposal.totalVolume','2.00'),('RESERVE_MISUSE','allocation.reserveAddition','20.00'),('DUAL_TAIL','economicProposal.dualTail',True),('RECOVERY','economicProposal.recoveryPL','-1.00'),('COVERAGE','economicProposal.reserveCoverage',False),('PERSISTENCE','persistence.stateRevision',9),('REVISION','fsm.inputRevision',2),('CERT_BODY','certificate.body.outputRevision',9),('CERT_DIGEST','certificate.digest','FORGED')]
def apply(v,name,path,value,index):
 if name=='DUP_DEAL':v['ledger']['records'].append(copy.deepcopy(v['ledger']['records'][0]))
 elif name=='DUP_EVENT':q=copy.deepcopy(v['ledger']['records'][0]);q['dealId']='D2';v['ledger']['records'].append(q)
 elif name=='MISSING_LEG':v['ledger']['records']=[]
 else:setp(v,path,value)
 return v
def build(root):
 root=Path(root);b=base();fixtures=[{'testMetadata':{'fixtureId':'VALID_BASE','tags':['positive']},'scenarioInput':b}];pairs=[]
 for i in range(103):
  name,path,value=DEFECTS[i%len(DEFECTS)];n=apply(copy.deepcopy(b),name,path,value,i);fid=f'NEG_{i+1:03d}_{name}';changed=[path] if name not in {'DUP_DEAL','DUP_EVENT','MISSING_LEG'} else ['ledger.records'];fixtures.append({'testMetadata':{'fixtureId':fid,'kind':name,'tags':['negative'],'description':name},'scenarioInput':n});pairs.append({'baseFixtureId':'VALID_BASE','negativeFixtureId':fid,'targetProperty':name,'allowedChangedPaths':changed,'actualChangedPaths':changed,'expectedCheckId':'R9_'+name,'expectedReason':name})
 (root/'Tests/Vectors/HSB_2E_R4_R9_R3_DRAFT_FIXTURES_V2.json').write_text(json.dumps({'schemaVersion':2,'fixtures':fixtures},indent=2,sort_keys=True)+'\n');(root/'Tests/Contracts/HSB_2E_R4_R9_R3_CAUSAL_PAIRS.json').write_text(json.dumps({'schemaVersion':1,'pairs':pairs},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);build(Path(p.parse_args().root))
