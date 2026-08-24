"""Deterministic canonical R4-R6 fixtures."""
from hsb_2e_provenance_model_r4_r6 import *
from hsb_2e_economic_model_r4_r6 import HSBI_EconomicPolicy
ROLES={'INITIAL':[('WINNER','BUY','1')],'BIG':[('BIG','BUY','1'),('SMALL','SELL','.5')],'SMALL':[('SMALL','BUY','.25'),('OLD_FAR','SELL','1'),('BIG','BUY','.5')],'FINAL':[('FAR','SELL','1')]}
def broker_fixture(scenario='BIG',money='9'):
    c={'accountLogin':1,'symbol':'EURUSD','magic':7,'cycleId':'C','transactionId':'TX','actionId':'A','stateRevision':3,'volumeStep':'.01','volumeMin':'.01','volumeMax':'10'}
    snap=HSBI_QuoteSnapshot(1,1,'EURUSD',7,'C',3,'S',2,D('1.1'),D('1.2'),1900).sealed();policy=HSBI_ExecutionPricePolicy(1,'EURUSD',5,D('.00001'),0,'BID','ASK','TRUSTED_TERMINAL_SNAPSHOT','S',2,1900,2200,'EXACT_CLOSE_SIDE','HSBI-PRICE-R6').sealed()
    positions=[];intents=[];records=[]
    for n,(role,direction,volume) in enumerate(ROLES[scenario],1):
        ticket=100+n;intent=f'I{ticket}';positions.append({'ticket':ticket,'role':role,'direction':direction,'authoritativeVolume':volume,'residualVolume':'.5' if role=='BIG' else '0'})
        intents.append({'intentId':intent,'positionTicket':ticket,'positionRole':role,'direction':direction,'intentKind':'FULL_CLOSE','requestedVolume':volume,'executable':True})
        price=snap.bid if direction=='BUY' else snap.ask;net=D(money);records.append(HSBI_DealEvidenceRecord(1,1,'EURUSD',7,'C','TX','A',3,'S',2,f'D{ticket}',f'E{ticket}',f'O{ticket}',ticket,role,direction,intent,D(volume),price,net,D(0),D(0),D(0),net,True,2000,n,'TRUSTED_TERMINAL_DEAL').sealed())
    state={'acceptedDealRecords':[],'consumedDealIds':[],'seenEventIds':[],'dealEventBindings':{},'cumulativeFills':{},'moneyByDeal':{},'moneyByTicket':{},'moneyByRole':{},'volumeByTicket':{},'evidenceRevision':0,'stateRevision':3,'settlementRevision':0,'persistenceSchemaVersion':1,'commitCertificate':None}
    ep=HSBI_EconomicPolicy(1,scenario,'C','A','TX',3,2,'ACCOUNT_CURRENCY_AND_LOTS','ROUND_DOWN',D('.01'),D('.01'),D('10'),D('.1'),D('.9'),D('.05'),D('100'),D('1'),D('100') if scenario=='FINAL' else D(0),D('100') if scenario=='FINAL' else D(0),('DEAL_NET_ACTUAL','ALLOCATION_DISJOINT','RECOVERY_ACTUAL'),('Docs/08','Docs/11','Docs/12','Docs/13')).sealed()
    return {'scenario':scenario,'context':c,'positions':positions,'intents':intents,'snapshot':snap,'pricePolicy':policy,'economicPolicy':ep,'dealRecords':records,'persistedState':state}
