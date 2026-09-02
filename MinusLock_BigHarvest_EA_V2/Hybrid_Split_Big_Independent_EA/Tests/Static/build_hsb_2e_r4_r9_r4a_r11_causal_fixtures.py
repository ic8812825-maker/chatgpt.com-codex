#!/usr/bin/env python3
import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R10_POSITIVE_BASES.json';OUT=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R11_FIRST_BLOCK_CAUSAL.json'
def main():
 fs=json.loads(SRC.read_text())['fixtures'];base=next(copy.deepcopy(f['scenarioInput']) for f in fs if f.get('scenarioInput',{}).get('phase')=='COMMITTED');rows=[]
 def add(fid,target,kind,paths,change,expected):
  r=copy.deepcopy(base);change(r);rows.append({'scenarioInput':r,'testContract':{'fixtureId':fid,'classification':kind,'positiveBase':'R10 committed positive','changedPaths':paths,'targetPredicate':target,'expectedOutcome':expected}})
 add('R11-BASE-POSITIVE','SCHEMA','POSITIVE',[],lambda r:None,'PASS_ALL')
 add('R11-SCHEMA-MISSING-PHASE','SCHEMA','NEGATIVE',['scenarioInput.phase'],lambda r:r.pop('phase'),'FAIL')
 add('R11-NUMERIC-NAN','NUMERIC_FINITE','NEGATIVE',['scenarioInput.economic.availableMoney'],lambda r:r['economic'].__setitem__('availableMoney','NaN'),'FAIL')
 add('R11-IDENTITY-EMPTY-TX','RUNTIME_IDENTITY','NEGATIVE',['scenarioInput.context.transactionId'],lambda r:r['context'].__setitem__('transactionId',''),'FAIL')
 add('R11-OWNERSHIP-POSITION-MAGIC','SYMBOL_MAGIC_OWNERSHIP','NEGATIVE',['scenarioInput.positions[0].magic'],lambda r:r['positions'][0].__setitem__('magic',1),'FAIL')
 add('R11-BROKER-ZERO-TICK','BROKER_PROPERTIES','NEGATIVE',['scenarioInput.broker.tickSize'],lambda r:r['broker'].__setitem__('tickSize','0'),'FAIL')
 add('R11-SNAPSHOT-FOREIGN-SYMBOL','SNAPSHOT_CONTEXT','NEGATIVE',['scenarioInput.snapshot.symbol'],lambda r:r['snapshot'].__setitem__('symbol','GBPUSD'),'FAIL')
 add('R11-TEMPORAL-CONTRADICTION','TEMPORAL_WINDOW','NEGATIVE',['scenarioInput.temporalPolicy.validUntil'],lambda r:r['temporalPolicy'].__setitem__('validUntil',1),'FAIL')
 add('R11-SCHEMA-ENUM-BOUNDARY','SCHEMA','BOUNDARY',['scenarioInput.phase'],lambda r:r.__setitem__('phase','COMMITTED'),'PASS_ALL')
 add('R11-NUMERIC-LARGE-FINITE','NUMERIC_FINITE','BOUNDARY',['scenarioInput.economic.availableMoney'],lambda r:r['economic'].__setitem__('availableMoney','1E+1000'),'PASS_ALL')
 add('R11-IDENTITY-UNICODE','RUNTIME_IDENTITY','BOUNDARY',['scenarioInput.context.actionId'],lambda r:[x.__setitem__('actionId','ДЕЙСТВИЕ-1') for x in [r['context'],*r['intents'],*r['deals'],*r['events']]],'PASS_ALL')
 add('R11-OWNERSHIP-LARGE-MAGIC','SYMBOL_MAGIC_OWNERSHIP','BOUNDARY',['context/positions/deals/events.magic'],lambda r:[x.__setitem__('magic',9007199254740993) for x in [r['context'],r['snapshot'],*r['positions'],*r['deals'],*r['events']]],'PASS_ALL')
 def broker_boundary(r):r['broker']['bid']=r['broker']['ask'];r['broker']['volumeStep']=r['broker']['volumeMin']
 add('R11-BROKER-EQUAL-QUOTE','BROKER_PROPERTIES','BOUNDARY',['scenarioInput.broker.bid','scenarioInput.broker.volumeStep'],broker_boundary,'PASS_ALL')
 def snapshot_boundary(r):r['snapshot']['revision']=0;r['context']['snapshotRevision']=0
 add('R11-SNAPSHOT-ZERO-REVISION','SNAPSHOT_CONTEXT','BOUNDARY',['snapshot.revision','context.snapshotRevision'],snapshot_boundary,'PASS_ALL')
 def temporal_boundary(r):
  p=r['temporalPolicy'];i=r['intents'][0];lo=max(r['snapshot']['timestamp'],p['validFrom'],i['createdTimestamp'],p['minimumTimestamp']);r['deals'][0]['timestamp']=lo
 add('R11-TEMPORAL-INCLUSIVE-LOWER','TEMPORAL_WINDOW','BOUNDARY',['scenarioInput.deals[0].timestamp'],temporal_boundary,'PASS_ALL')
 OUT.write_text(json.dumps({'contract':'R4A_R11_FIRST_BLOCK','fixtures':rows},indent=2,sort_keys=True)+'\n');print(len(rows))
if __name__=='__main__':main()
