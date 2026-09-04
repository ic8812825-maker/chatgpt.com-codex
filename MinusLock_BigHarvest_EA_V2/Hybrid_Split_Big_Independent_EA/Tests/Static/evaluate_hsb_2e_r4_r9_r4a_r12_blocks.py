import copy,json,sys
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import evaluate_hsb_2e_r4_r9_r4a_r11_first_block as first
C=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R12_PREDICATE_CONTRACT.json').read_text())['predicates'];ORDER=[x['predicateId'] for x in C];BY={x['predicateId']:x for x in C}
def res(pid,status,deps,paths,reason=''):
 p=BY[pid];return {'predicateId':pid,'status':status,'checkId':p['failureCheckId'] if status=='FAIL' else '','reason':reason or (p['failureReason'] if status=='FAIL' else ''),'evaluatedPaths':paths,'dependencyResults':deps}
def fail(pid,d,p,r=''):return res(pid,'FAIL',d,p,r)
def ok(pid,d,p):return res(pid,'PASS',d,p)
def pos(r,d):
 b=r['broker'];paths=['scenarioInput.positions[*]']
 for x in r['positions']:
  if not x['ticket'] or x['direction'] not in ('BUY','SELL') or x['role'] not in ('NEAR','BIG','FAR') or Decimal(x['volume'])<=0 or Decimal(x['openPrice'])<=0:return fail('POSITION_VALIDATION',d,paths)
  if Decimal(x['volume'])<Decimal(b['volumeMin']) or Decimal(x['volume'])>Decimal(b['volumeMax']):return fail('POSITION_VALIDATION',d,paths)
 return ok('POSITION_VALIDATION',d,paths)
def intent(r,d):
 for x in r['intents']:
  if not x['intentId'] or x['direction'] not in ('BUY','SELL') or Decimal(x['requestedVolume'])<=0 or x['expiresTimestamp']<x['createdTimestamp']:return fail('INTENT_VALIDATION',d,['scenarioInput.intents[*]'])
 return ok('INTENT_VALIDATION',d,['scenarioInput.intents[*]'])
def unique(r,d):
 ds=r.get('deals',[]);es=r.get('events',[])
 if len({x['dealId'] for x in ds})!=len(ds) or len({x['eventId'] for x in es})!=len(es):return fail('DEAL_EVENT_UNIQUENESS',d,['scenarioInput.deals[*].dealId','scenarioInput.events[*].eventId'])
 if any(x['eventId'] not in {e['eventId'] for e in es} for x in ds):return fail('DEAL_EVENT_UNIQUENESS',d,['scenarioInput.deals[*].eventId'])
 return ok('DEAL_EVENT_UNIQUENESS',d,['scenarioInput.deals[*].dealId','scenarioInput.events[*].eventId'])
def binding(r,d):
 ps={x['ticket'] for x in r['positions']};ins={x['intentId']:x for x in r['intents']}
 for x in r.get('deals',[]):
  if x['positionTicket'] not in ps or x['intentId'] not in ins or ins[x['intentId']]['positionTicket']!=x['positionTicket']:return fail('DEAL_POSITION_INTENT_BINDING',d,['scenarioInput.deals[*].positionTicket','scenarioInput.deals[*].intentId'])
 return ok('DEAL_POSITION_INTENT_BINDING',d,['scenarioInput.deals[*].positionTicket','scenarioInput.deals[*].intentId'])
def ledger(r,d):
 p=r['persistedState'];ids=p['consumedDealIds'];deals={x['dealId'] for x in r.get('deals',[])}
 if len(ids)!=len(set(ids)) or not all(isinstance(x,str) and x for x in ids) or not isinstance(p['authoritativeLedgerRoot'],str) or len(p['authoritativeLedgerRoot'])!=64:return fail('PERSISTED_LEDGER_REVALIDATION',d,['scenarioInput.persistedState.consumedDealIds','scenarioInput.persistedState.authoritativeLedgerRoot'])
 if r['phase']=='REPLAY' and not deals<=set(ids):return fail('PERSISTED_LEDGER_REVALIDATION',d,['scenarioInput.persistedState.consumedDealIds'])
 return ok('PERSISTED_LEDGER_REVALIDATION',d,['scenarioInput.persistedState.consumedDealIds','scenarioInput.persistedState.authoritativeLedgerRoot'])
def batch(r,d):
 if r['phase']!='PRE_COMMIT':
  want={x['intentId'] for x in r['intents']};got={x['intentId'] for x in r.get('deals',[])}
  if want!=got:return fail('BATCH_ATOMICITY',d,['scenarioInput.deals[*]'])
 return ok('BATCH_ATOMICITY',d,['scenarioInput.deals[*]'])
def fills(r,d):
 sums={x['intentId']:Decimal(0) for x in r['intents']}
 for x in r.get('deals',[]):sums[x['intentId']]+=Decimal(x['volume'])
 for x in r['intents']:
  if sums[x['intentId']]>Decimal(x['requestedVolume']):return fail('PER_TICKET_FILL',d,['scenarioInput.intents[*].requestedVolume','scenarioInput.deals[*].volume'])
 return ok('PER_TICKET_FILL',d,['scenarioInput.intents[*].requestedVolume','scenarioInput.deals[*].volume'])
E={'POSITION_VALIDATION':pos,'INTENT_VALIDATION':intent,'DEAL_EVENT_UNIQUENESS':unique,'DEAL_POSITION_INTENT_BINDING':binding,'PERSISTED_LEDGER_REVALIDATION':ledger,'BATCH_ATOMICITY':batch,'PER_TICKET_FILL':fills}
def trace(r):
 firsttrace={x['predicateId']:x for x in first.trace(r)['predicates']};out=[];prev={}
 for pid in ORDER:
  deps={x:prev[x]['status'] for x in BY[pid]['prerequisitePredicates']}
  if any(v!='PASS' for v in deps.values()):x=res(pid,'BLOCKED_BY_PREREQUISITE',deps,[],'PREREQUISITE_NOT_PASSED')
  elif pid in firsttrace:x=firsttrace[pid]
  else:x=E[pid](r,deps)
  out.append(x);prev[pid]=x
 return out
