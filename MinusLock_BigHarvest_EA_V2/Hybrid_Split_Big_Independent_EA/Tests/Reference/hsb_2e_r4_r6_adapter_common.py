"""Structural historical-input to canonical R4-R6 adapter."""
import copy
from hsb_2e_test_fixtures_r4_r6 import broker_fixture
from hsb_2e_provenance_model_r4_r6 import D,digest

def infer_scenario(version,vector):
    source=vector.get('INPUT',{});fn=str(vector.get('FUNCTION','')).upper();scenario=source.get('scenario')
    if scenario in ('INITIAL','BIG','SMALL','FINAL'):return scenario
    if 'BIG' in fn:return 'BIG'
    if 'SMALL' in fn:return 'SMALL'
    return 'INITIAL'

def adapt(version,vector):
    if not isinstance(vector,dict) or not isinstance(vector.get('INPUT'),dict):return {'adapterResult':'UNMAPPED','reason':'INPUT_MISSING'}
    old=vector['INPUT'];scenario=infer_scenario(version,vector);x=broker_fixture(scenario);sources={}
    old_context=old.get('context',{})
    for k in ('accountLogin','symbol','magic','cycleId','transactionId','actionId','stateRevision','volumeStep'):
        if k in old_context:x['context'][k]=old_context[k];sources[f'context.{k}']=f'INPUT.context.{k}'
    # Preserve historical negative numeric/revision intent where representable.
    positions=old.get('positions')
    if isinstance(positions,list) and positions:
        for target,source in zip(x['positions'],positions):
            for oldk,newk in (('positionTicket','ticket'),('ticket','ticket'),('role','role'),('direction','direction'),('positionVolume','authoritativeVolume'),('volume','authoritativeVolume')):
                if oldk in source:target[newk]=source[oldk];sources[f'position.{newk}']=f'INPUT.positions.{oldk}'
    intents=old.get('intents')
    if isinstance(intents,list) and intents:
        for target,source in zip(x['intents'],intents):
            for k in ('intentId','positionTicket','positionRole','direction','intentKind','requestedVolume'):
                if k in source:target[k]=source[k];sources[f'intent.{k}']=f'INPUT.intents.{k}'
    # R2 has singular position/intent.
    if isinstance(old.get('position'),dict):
        p=old['position'];t=x['positions'][0];t['ticket']=p.get('ticket',t['ticket']);t['direction']=p.get('direction',t['direction']);t['authoritativeVolume']=p.get('volume',t['authoritativeVolume'])
    if isinstance(old.get('intent'),dict):
        i=old['intent'];t=x['intents'][0];t['intentId']=i.get('intentId',t['intentId']);t['positionTicket']=i.get('positionTicket',t['positionTicket']);t['requestedVolume']=i.get('requestedVolume',t['requestedVolume'])
    deals=old.get('deals')
    if isinstance(deals,list):
        if not deals:x['dealRecords']=[]
        for target,source in zip(x['dealRecords'],deals):
            mapping={'dealId':'dealId','eventId':'eventId','orderId':'orderId','positionTicket':'positionTicket','direction':'direction','volume':'volume','price':'price','profit':'profit','commission':'commission','swap':'swap','fee':'fee','confirmed':'confirmed','timestamp':'dealTimestamp'}
            for oldk,newk in mapping.items():
                if oldk in source:object.__setattr__(target,newk,D(source[oldk]) if newk in {'volume','price','profit','commission','swap','fee'} else source[oldk])
            object.__setattr__(target,'netMoney',target.profit+target.commission+target.swap+target.fee);object.__setattr__(target,'recordDigest',digest(target.body()))
    # Link canonical records after ticket/intent migration. This is mapping, not test-target execution.
    for r,p,i in zip(x['dealRecords'],x['positions'],x['intents']):
        object.__setattr__(r,'positionTicket',p['ticket']);object.__setattr__(r,'positionRole',p['role']);object.__setattr__(r,'direction',p['direction']);object.__setattr__(r,'intentId',i['intentId']);object.__setattr__(r,'recordDigest',digest(r.body()))
    return {'adapterResult':'ADAPTED','sourceVersion':version,'sourceVectorId':vector.get('VECTOR_ID'),'canonicalInput':x,'fieldSources':sources,'expectedSemantic':{'oldStatus':vector.get('EXPECTED_RESULT',{}).get('status'),'oldReason':vector.get('EXPECTED_RESULT',{}).get('reason')}}
