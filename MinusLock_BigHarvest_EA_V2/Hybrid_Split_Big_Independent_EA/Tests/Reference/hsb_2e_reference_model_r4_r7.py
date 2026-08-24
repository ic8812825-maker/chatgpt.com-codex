#!/usr/bin/env python3
"""R4-R7 fail-closed transaction barrier with recomputable commit sources."""
import argparse,copy
from dataclasses import dataclass,asdict
from hsb_2e_provenance_model_r4_r7 import *
from hsb_2e_economic_model_r4_r7 import build_economic_proposal

REQUIRED={'INITIAL':{'WINNER'},'BIG':{'BIG','SMALL'},'SMALL':{'SMALL','OLD_FAR','BIG'},'FINAL':{'FAR'}}
@dataclass(frozen=True)
class HSBI_CommitObject:
    kind:str;bodyValue:dict;objectDigest:str=''
    def body(self):return {'kind':self.kind,'bodyValue':self.bodyValue}
    def sealed(self):return self.__class__(self.kind,self.bodyValue,digest(self.body()))
@dataclass(frozen=True)
class HSBI_SettlementCommitCertificate:
    certificateVersion:int;inputRevision:int;outputRevision:int;brokerDigest:str;economicDigest:str;allocationDigest:str;persistenceDigest:str;fsmDigest:str;outputStateDigest:str;certificateDigest:str=''
    def body(self):return {k:v for k,v in asdict(self).items() if k!='certificateDigest'}
    def sealed(self):return self.__class__(**{**self.body(),'certificateDigest':digest(self.body())})

def result(status,reason,phase,state,**kw):return {'status':status,'reason':reason,'phase':phase,'state':state,'settlementApplied':False,'allocationApplied':False,'revisionDelta':0,**kw}
def fill_contract(inp,state):
    pmap={p['ticket']:p for p in inp['positions']};imap={i['positionTicket']:i for i in inp['intents']}
    if set(pmap)!=set(imap) or len(imap)!=len(inp['intents']):return None,'ONE_POSITION_ONE_INTENT_VIOLATION'
    fills={}
    for ticket,p in pmap.items():
        i=imap[ticket];requested=D(i['requestedVolume']);before=D(p['authoritativeVolume']);confirmed=D(state['cumulativeFills'].get(str(ticket),0));kind=i['intentKind']
        if inp['scenario']=='SMALL' and p['role']=='BIG':
            if kind!='PARTIAL_CLOSE' or requested<=0 or requested>=before:return None,'SMALL_BIG_PARTIAL_INTENT_INVALID'
        elif kind!='FULL_CLOSE' or requested!=before:return None,'FULL_CLOSE_REQUIRED'
        fills[str(ticket)]={'requested':requested,'confirmed':confirmed,'full':confirmed==requested,'before':before}
    return fills,None
def broker_object(inp,state,fills):
    body={'context':inp['context'],'snapshot':inp['snapshot'],'moneyByTicket':state['moneyByTicket'],'moneyByRole':state['moneyByRole'],'volumeByTicket':state['volumeByTicket'],'acceptedDealIds':state['consumedDealIds'],'fills':fills}
    return HSBI_CommitObject('HSBI_BrokerProposal',body).sealed()
def output_digest(state):
    body={k:v for k,v in state.items() if k not in {'commitCertificate','committedOutputDigest'}}
    return digest(body)
def pipeline(inp,state):
    fills,error=fill_contract(inp,state)
    if error or not all(v['full'] for v in fills.values()):return None,error or 'COMMIT_FULL_FILL_UNPROVEN'
    broker=broker_object(inp,state,fills);broker_view={**broker.bodyValue,'brokerProposalDigest':broker.objectDigest}
    economic,error=build_economic_proposal(inp['scenario'],broker_view,inp['economicPolicy'],inp['positions'],True)
    if error:return None,error
    allocation=HSBI_CommitObject('HSBI_AllocationResult',economic.allocationAttribution).sealed()
    persistence=HSBI_CommitObject('HSBI_PersistenceRecord',{'order':['BROKER','ECONOMIC','ALLOCATION','PERSISTENCE','FSM'],'ledgerDigest':digest(state['acceptedDealRecords']),'evidenceRevision':state['evidenceRevision']}).sealed()
    fsm=HSBI_CommitObject('HSBI_FSMTransitionRecord',{'scenario':inp['scenario'],'inputRevision':inp['context']['stateRevision'],'outputRevision':inp['context']['stateRevision']+1}).sealed()
    return {'broker':broker,'economic':HSBI_CommitObject('HSBI_EconomicProposal',economic.body()).sealed(),'economicValue':economic,'allocation':allocation,'persistence':persistence,'fsm':fsm},None
def replay(inp,state):
    cert=state.get('commitCertificate');bundle=state.get('commitBundle')
    if not isinstance(cert,HSBI_SettlementCommitCertificate) or not isinstance(bundle,dict):return 'COMMIT_SOURCE_OBJECT_MISSING'
    evidence_context={**inp['context'],'stateRevision':cert.inputRevision};e=revalidate_persisted(state,evidence_context,inp['positions'],inp['intents'],inp['snapshot'],inp['pricePolicy'])
    if e:return e
    recomputed,e=pipeline({**inp,'context':evidence_context},state)
    if e:return e
    names={'broker':'brokerDigest','economic':'economicDigest','allocation':'allocationDigest','persistence':'persistenceDigest','fsm':'fsmDigest'}
    if any(not isinstance(bundle.get(k),HSBI_CommitObject) or bundle[k].objectDigest!=digest(bundle[k].body()) or bundle[k].objectDigest!=recomputed[k].objectDigest or getattr(cert,n)!=recomputed[k].objectDigest for k,n in names.items()):return 'COMMIT_PIPELINE_RECOMPUTATION_MISMATCH'
    if cert.certificateDigest!=digest(cert.body()) or cert.outputRevision!=cert.inputRevision+1:return 'COMMIT_PIPELINE_RECOMPUTATION_MISMATCH'
    if state.get('committedOutputDigest')!=output_digest(state) or cert.outputStateDigest!=output_digest(state):return 'COMMIT_PIPELINE_RECOMPUTATION_MISMATCH'
    return None
def execute_scenario(inp):
    try:
        scenario=inp['scenario'];state=copy.deepcopy(inp['persistedState'])
        if scenario not in REQUIRED:return result('REJECT','UNKNOWN_SCENARIO','VALIDATION_BLOCKED',state)
        roles=[p['role'] for p in inp['positions']]
        if set(roles)!=REQUIRED[scenario] or len(roles)!=len(set(roles)):return result('REJECT','MANDATORY_LEGS_INVALID','VALIDATION_BLOCKED',state)
        if state.get('commitCertificate'):
            e=replay(inp,state);return result('REJECT',e,'VALIDATION_BLOCKED',state) if e else result('PASS','ALREADY_COMMITTED','IDEMPOTENT_REPLAY',state)
        new,e=validate_all_then_apply(state,inp.get('dealRecords',[]),inp['context'],inp['positions'],inp['intents'],inp['snapshot'],inp['pricePolicy'])
        if e:return result('REJECT' if e!='EMPTY_BATCH' else 'UNAVAILABLE',e,'VALIDATION_BLOCKED',state)
        pipe,e=pipeline(inp,new)
        if e:return result('UNAVAILABLE' if e=='COMMIT_FULL_FILL_UNPROVEN' else 'REJECT',e,'ECONOMIC_BLOCKED',new)
        out=copy.deepcopy(new);out['stateRevision']=inp['context']['stateRevision']+1;out['settlementRevision']=state.get('settlementRevision',0)+1;out['commitBundle']={k:v for k,v in pipe.items() if k!='economicValue'}
        cert=HSBI_SettlementCommitCertificate(1,inp['context']['stateRevision'],out['stateRevision'],pipe['broker'].objectDigest,pipe['economic'].objectDigest,pipe['allocation'].objectDigest,pipe['persistence'].objectDigest,pipe['fsm'].objectDigest,'').sealed();out['commitCertificate']=cert
        # Digest excludes its own field and certificate; certificate is resealed with it.
        out['committedOutputDigest']=output_digest(out);cert=HSBI_SettlementCommitCertificate(**{**cert.body(),'outputStateDigest':out['committedOutputDigest']}).sealed();out['commitCertificate']=cert
        return {'status':'PASS','reason':'OK','phase':'FSM_COMMITTED','state':out,'settlementApplied':True,'allocationApplied':pipe['economicValue'].allocatedMoney>0,'revisionDelta':1,'economicProposal':pipe['economicValue'],'commitCertificate':cert}
    except (KeyError,TypeError,ValueError,ArithmeticError) as e:return result('REJECT','MALFORMED_INPUT_'+type(e).__name__.upper(),'VALIDATION_BLOCKED',inp.get('persistedState',{}))
def self_test():
    from hsb_2e_test_fixtures_r4_r7 import broker_fixture
    checks=[]
    for s in REQUIRED:
        x=broker_fixture(s)
        if s=='SMALL':
            p=x['positions'][2];i=x['intents'][2];p['authoritativeVolume']='.8';i.update(intentKind='PARTIAL_CLOSE',requestedVolume='.5')
        checks.append(execute_scenario(x)['status']=='PASS')
    print(f'R4_R7_REFERENCE_SELF_TESTS={sum(checks)}/{len(checks)}');return all(checks)
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
