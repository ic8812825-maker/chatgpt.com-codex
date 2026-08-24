#!/usr/bin/env python3
"""Canonical R4-R6 transaction barrier; the sole cross-version test target."""
import argparse,copy
from dataclasses import dataclass,asdict
from hsb_2e_provenance_model_r4_r6 import *
from hsb_2e_economic_model_r4_r6 import build_economic_proposal

REQUIRED={'INITIAL':{'WINNER'},'BIG':{'BIG','SMALL'},'SMALL':{'SMALL','OLD_FAR','BIG'},'FINAL':{'FAR'}}
@dataclass(frozen=True)
class HSBI_SettlementCommitCertificate:
    certificateVersion:int;settlementId:str;inputStateDigest:str;outputStateDigest:str;inputStateRevision:int;outputStateRevision:int;scenario:str;requiredPositionTickets:tuple;requiredIntentIds:tuple;acceptedDealIds:tuple;eventIds:tuple;dealEventBindingsDigest:str;fullFillProofDigest:str;brokerProposalDigest:str;economicProposalDigest:str;allocationResultDigest:str;persistenceRecordDigest:str;totalMoney:Decimal;totalVolume:Decimal;fsmTransition:str;validFrom:int;validUntil:int;certificateDigest:str=''
    def body(self):return {k:v for k,v in asdict(self).items() if k!='certificateDigest'}
    def sealed(self):return self.__class__(**{**self.body(),'certificateDigest':digest(self.body())})

def out(status,reason,phase,state,**kw):return {'status':status,'reason':reason,'phase':phase,'state':state,'settlementApplied':False,'allocationApplied':False,**kw}
def required_full_fill(inp,state):
    pmap={p['ticket']:p for p in inp['positions']};imap={i['positionTicket']:i for i in inp['intents']}
    if set(pmap)!=set(imap) or len(imap)!=len(inp['intents']):return None,'ONE_POSITION_ONE_INTENT_VIOLATION'
    fills={}
    for ticket,p in pmap.items():
        i=imap[ticket];requested=D(i['requestedVolume']);authoritative=D(p['authoritativeVolume']);confirmed=D(state['cumulativeFills'].get(str(ticket),0))
        if i['intentKind']!='FULL_CLOSE' or requested!=authoritative:return None,'FULL_CLOSE_REQUIRED'
        fills[str(ticket)]={'requested':requested,'confirmed':confirmed,'full':confirmed==requested}
    return fills,None

def validate_committed(inp,state):
    cert=state.get('commitCertificate')
    if not isinstance(cert,HSBI_SettlementCommitCertificate):return 'COMMIT_CERTIFICATE_MISSING'
    if cert.certificateDigest!=digest(cert.body()):return 'COMMIT_CERTIFICATE_DIGEST_INVALID'
    evidence_context={**inp['context'],'stateRevision':cert.inputStateRevision}
    error=revalidate_persisted(state,evidence_context,inp['positions'],inp['intents'],inp['snapshot'],inp['pricePolicy'])
    if error:return error
    fills,error=required_full_fill(inp,state)
    if error or not all(v['full'] for v in fills.values()):return 'COMMIT_FULL_FILL_UNPROVEN'
    expected={'requiredPositionTickets':tuple(sorted(p['ticket'] for p in inp['positions'])),'requiredIntentIds':tuple(sorted(i['intentId'] for i in inp['intents'])),'acceptedDealIds':tuple(state['consumedDealIds']),'eventIds':tuple(state['seenEventIds']),'dealEventBindingsDigest':digest(state['dealEventBindings']),'fullFillProofDigest':digest(fills),'totalMoney':sum(state['moneyByDeal'].values(),D(0)),'totalVolume':sum((r.volume for r in state['acceptedDealRecords']),D(0)),'inputStateRevision':state['stateRevision']-1,'outputStateRevision':state['stateRevision'],'scenario':inp['scenario']}
    if any(getattr(cert,k)!=v for k,v in expected.items()):return 'COMMIT_CERTIFICATE_LEDGER_MISMATCH'
    if cert.outputStateRevision!=cert.inputStateRevision+1 or cert.outputStateDigest!=state.get('committedOutputDigest'):return 'COMMIT_CERTIFICATE_STATE_MISMATCH'
    if cert.economicProposalDigest!=state.get('economicProposalDigest') or cert.allocationResultDigest!=state.get('allocationResultDigest') or cert.persistenceRecordDigest!=state.get('persistenceRecordDigest'):return 'COMMIT_CERTIFICATE_PIPELINE_MISMATCH'
    return None

def execute_scenario(inp):
    try:
        scenario=inp['scenario'];state=copy.deepcopy(inp['persistedState'])
        if scenario not in REQUIRED:return out('REJECT','UNKNOWN_SCENARIO','VALIDATION_BLOCKED',state)
        roles=[p['role'] for p in inp['positions']]
        if set(roles)!=REQUIRED[scenario] or len(roles)!=len(set(roles)):return out('REJECT','MANDATORY_LEGS_INVALID','VALIDATION_BLOCKED',state)
        if state.get('commitCertificate'):
            error=validate_committed(inp,state)
            return out('REJECT',error,'VALIDATION_BLOCKED',state) if error else out('PASS','ALREADY_COMMITTED','IDEMPOTENT_REPLAY',state)
        before=digest(state);new,error=validate_all_then_apply(state,inp.get('dealRecords',[]),inp['context'],inp['positions'],inp['intents'],inp['snapshot'],inp['pricePolicy'])
        if error:return out('REJECT' if error!='EMPTY_BATCH' else 'UNAVAILABLE',error,'VALIDATION_BLOCKED',state)
        fills,error=required_full_fill(inp,new)
        if error:return out('REJECT',error,'VALIDATION_BLOCKED',state)
        if not all(v['full'] for v in fills.values()):return out('UNAVAILABLE','PARTIAL_FILL','WAITING_FOR_FULL_FILL',new)
        broker={'context':inp['context'],'snapshot':inp['snapshot'],'moneyByTicket':new['moneyByTicket'],'moneyByRole':new['moneyByRole'],'volumeByTicket':new['volumeByTicket'],'acceptedDealIds':new['consumedDealIds'],'sealed':True};broker['brokerProposalDigest']=digest(broker)
        economic,error=build_economic_proposal(scenario,broker,inp['economicPolicy'],inp['positions'],True)
        if error:return out('REJECT',error,'ECONOMIC_BLOCKED',new)
        allocation_digest=digest(economic.allocationAttribution);persistence_digest=digest(('BROKER_EVIDENCE','ECONOMIC_PROPOSAL','ALLOCATION','FSM_COMMIT'))
        output_revision=inp['context']['stateRevision']+1;committed=copy.deepcopy(new);committed.update(stateRevision=output_revision,settlementRevision=state.get('settlementRevision',0)+1,economicProposalDigest=economic.proposalDigest,allocationResultDigest=allocation_digest,persistenceRecordDigest=persistence_digest)
        # Output digest deliberately excludes the certificate to avoid a recursive hash.
        committed['committedOutputDigest']=digest(committed)
        cert=HSBI_SettlementCommitCertificate(1,digest((scenario,inp['context']['transactionId'],inp['context']['actionId'])),before,committed['committedOutputDigest'],inp['context']['stateRevision'],output_revision,scenario,tuple(sorted(p['ticket'] for p in inp['positions'])),tuple(sorted(i['intentId'] for i in inp['intents'])),tuple(committed['consumedDealIds']),tuple(committed['seenEventIds']),digest(committed['dealEventBindings']),digest(fills),broker['brokerProposalDigest'],economic.proposalDigest,allocation_digest,persistence_digest,economic.availableMoney,sum((r.volume for r in committed['acceptedDealRecords']),D(0)),f'{scenario}_COMMIT',inp['snapshot'].timestamp,inp['pricePolicy'].validUntil).sealed();committed['commitCertificate']=cert
        return {'status':'PASS','reason':'OK','phase':'FSM_COMMITTED','state':committed,'settlementApplied':True,'allocationApplied':economic.allocatedMoney>0,'brokerProposal':broker,'economicProposal':economic,'commitCertificate':cert}
    except (KeyError,TypeError,ValueError,ArithmeticError) as e:return out('REJECT','MALFORMED_INPUT_'+type(e).__name__.upper(),'VALIDATION_BLOCKED',inp.get('persistedState',{}))

def self_test():
    from hsb_2e_test_fixtures_r4_r6 import broker_fixture
    checks=[]
    for s in REQUIRED:checks.append(execute_scenario(broker_fixture(s))['status']=='PASS')
    x=broker_fixture('INITIAL');r=execute_scenario(x);y=broker_fixture('INITIAL');y['persistedState']=r['state'];y['context']['stateRevision']=r['state']['stateRevision'];checks.append(execute_scenario(y)['reason']=='ALREADY_COMMITTED')
    print(f'R4_R6_REFERENCE_SELF_TESTS={sum(checks)}/{len(checks)}');return all(checks)
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
