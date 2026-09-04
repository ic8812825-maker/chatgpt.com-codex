import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];reg=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R6_PREDICATE_REGISTRY.json').read_text())['predicates'][:14]
extra={
'NUMERIC_FINITE':['ALL_SCHEMA_NUMERIC_NODES'],
'RUNTIME_IDENTITY':['scenarioInput.context.accountId','scenarioInput.context.cycleId','scenarioInput.context.transactionId','scenarioInput.context.actionId','scenarioInput.intents[*].transactionId','scenarioInput.intents[*].actionId','scenarioInput.deals[*].accountId','scenarioInput.deals[*].cycleId','scenarioInput.deals[*].transactionId','scenarioInput.deals[*].actionId','scenarioInput.events[*].accountId','scenarioInput.events[*].cycleId','scenarioInput.events[*].transactionId','scenarioInput.events[*].actionId'],
'SYMBOL_MAGIC_OWNERSHIP':['scenarioInput.context.symbol','scenarioInput.context.magic','scenarioInput.positions[*].symbol','scenarioInput.positions[*].magic','scenarioInput.deals[*].symbol','scenarioInput.deals[*].magic','scenarioInput.events[*].symbol','scenarioInput.events[*].magic'],
'BROKER_PROPERTIES':['scenarioInput.broker.digits','scenarioInput.broker.point','scenarioInput.broker.tickSize','scenarioInput.broker.tickValue','scenarioInput.broker.contractSize','scenarioInput.broker.volumeMin','scenarioInput.broker.volumeMax','scenarioInput.broker.volumeStep','scenarioInput.broker.bid','scenarioInput.broker.ask','scenarioInput.broker.maximumDeviation'],
'SNAPSHOT_CONTEXT':['scenarioInput.snapshot.symbol','scenarioInput.snapshot.magic','scenarioInput.snapshot.revision','scenarioInput.context.symbol','scenarioInput.context.magic','scenarioInput.context.snapshotRevision'],
'TEMPORAL_WINDOW':['scenarioInput.snapshot.timestamp','scenarioInput.temporalPolicy.validFrom','scenarioInput.temporalPolicy.validUntil','scenarioInput.temporalPolicy.minimumTimestamp','scenarioInput.temporalPolicy.allowedUpperBound','scenarioInput.intents[*].createdTimestamp','scenarioInput.intents[*].expiresTimestamp','scenarioInput.deals[*].timestamp']}
out=[]
for p in reg:
 q=dict(p);q['exactInputPaths']=extra.get(q['predicateId'],q['exactInputPaths']);q['dataDependencies']=q['exactInputPaths'];q['evaluatorFunction']='evaluate_'+q['predicateId'].lower();out.append(q)
(ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R12_PREDICATE_CONTRACT.json').write_text(json.dumps({'predicates':out,'coverage':{x['predicateId']:x['exactInputPaths'] for x in out}},indent=2,sort_keys=True)+'\n')
