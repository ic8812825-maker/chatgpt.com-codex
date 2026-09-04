import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];src=json.loads((ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R10_POSITIVE_BASES.json').read_text())['fixtures'];base=next(copy.deepcopy(x['scenarioInput']) for x in src if x.get('scenarioInput',{}).get('phase')=='COMMITTED');out=[]
def add(i,t,change):
 r=copy.deepcopy(base);change(r);out.append({'scenarioInput':r,'testContract':{'fixtureId':i,'targetPredicate':t,'classification':'NEGATIVE','positiveBase':'R10 committed','changedPaths':[]}})
for t in ('POSITION_VALIDATION','INTENT_VALIDATION','DEAL_EVENT_UNIQUENESS','DEAL_POSITION_INTENT_BINDING','PERSISTED_LEDGER_REVALIDATION','BATCH_ATOMICITY','PER_TICKET_FILL'):out.append({'scenarioInput':copy.deepcopy(base),'testContract':{'fixtureId':'R12-'+t+'-POS','targetPredicate':t,'classification':'POSITIVE','positiveBase':'R10 committed','changedPaths':[]}})
add('R12-POSITION-VOLUME','POSITION_VALIDATION',lambda r:r['positions'][0].__setitem__('volume','0'))
add('R12-INTENT-EXPIRY','INTENT_VALIDATION',lambda r:r['intents'][0].__setitem__('requestedVolume','0'))
add('R12-DUP-DEAL','DEAL_EVENT_UNIQUENESS',lambda r:r['deals'].append(copy.deepcopy(r['deals'][0])))
add('R12-ORPHAN-POSITION','DEAL_POSITION_INTENT_BINDING',lambda r:r['deals'][0].__setitem__('positionTicket','NO-TICKET'))
add('R12-DUP-CONSUMED','PERSISTED_LEDGER_REVALIDATION',lambda r:r['persistedState'].__setitem__('consumedDealIds',['X','X']))
add('R12-MISSING-FILL','BATCH_ATOMICITY',lambda r:r.__setitem__('deals',[]))
out.append({'scenarioInput':copy.deepcopy(base),'testContract':{'fixtureId':'R12-POSITION-BOUNDARY','targetPredicate':'POSITION_VALIDATION','classification':'POSITIVE','positiveBase':'R10 committed','changedPaths':[]}})
add('R12-OVERFILL','PER_TICKET_FILL',lambda r:r['deals'][0].__setitem__('volume','99'))
(ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R12_SECOND_BLOCK_CAUSAL.json').write_text(json.dumps({'fixtures':out},indent=2,sort_keys=True)+'\n');print(len(out))
