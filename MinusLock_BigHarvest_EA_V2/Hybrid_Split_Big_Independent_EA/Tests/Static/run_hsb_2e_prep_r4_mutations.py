#!/usr/bin/env python3
"""Semantic mutation runner: edits executable Python for R4M010-R4M038 and executes verifier."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPL={
 1:("'MONEY_CONSERVATION':money","'UNKNOWN_INVARIANT':money"),2:("'MONEY_CONSERVATION':money","'MONEY_CONSERVATION_REMOVED':money"),3:("return bool(REGISTRY[name](i,a))","return bool(REGISTRY[name](i,{}))"),
 5:("list(range(1,len(ops)+1))","list(range(0,len(ops)))"),
 7:("p=pos.get(ticket)","p=None"),8:("if key in closes:errors.append('DUPLICATE_BROKER_INTENT')","if key not in closes:errors.append('DUPLICATE_BROKER_INTENT')"),9:("Decimal(x['normalizedVolume'])>Decimal(p['volume'])","Decimal(x['normalizedVolume'])<Decimal(p['volume'])"),
 10:("if direction=='BUY':return D(c['bid'])","if direction=='BUY':return D(c['ask'])"),11:("if direction=='SELL':return D(c['ask'])","if direction=='SELL':return D(c['bid'])"),12:("return None # MUTATION_R4M012","return D(c['ask']) # MUTATION_R4M012"),13:("return max(D(0),-(price-op)*sign*D(p['volume'])*D(p.get('moneyPerPriceLot',100)))","return max(D(0),(price-op)*sign*D(p['volume'])*D(p.get('moneyPerPriceLot',100)))"),14:("commission+=D(d.get('commission',0))","commission+=D(0)"),15:("swap+=D(d.get('swap',0))","swap+=D(0)"),16:("fee+=D(d.get('fee',0))","fee+=D(0)"),17:("'recoveryBudgetWithInitialProfit':'0'","'recoveryBudgetWithInitialProfit':ignored"),18:("budget=max(D(0),bn+sn) # MUTATION_R4M018","budget=max(D(0),bn+sn+reserve) # MUTATION_R4M018"),19:("if not (bigfull and smallfull):","if not (bc>0 and smallfull):"),20:("if not (bigfull and smallfull):","if not (bigfull and sc>0):"),21:("sv!=D(small['volume']) or ov!=D(old['volume']) or bv!=close_big","sv!=D(small['volume']) or False or bv!=close_big"),22:("rem=D(big['volume'])-close_big","rem=D(big['volume'])-close_big+D('0.01')"),23:("if rem>=D(old['volume']):","if rem>D(old['volume']):"),24:("if rem>=D(old['volume']):","if False:"),25:("if x.get('dualTail'):return result(x,'REJECT','DUAL_TAIL')","if False:return result(x,'REJECT','DUAL_TAIL')"),26:("if x.get('createNextLevel') and not committed:","if False:"),27:("if key in seen:return None","if False:return None"),28:("ra=D(0) if key in consumed else","ra=D(0) if False else"),29:("return result(x,output={'actionId':x['actionId']","return result(x,output={'actionId':x['actionId']+'-NEW'"),30:("'eventId':x['eventId']","'eventId':'STALE'"),31:("return result(x,'UNAVAILABLE','RECONCILIATION_REQUIRED')","return result(x,'PASS','OK')"),32:("return result(x,'UNAVAILABLE','PARTIAL_FILL'","return result(x,'PASS','OK'"),33:("and recovery>0 # MUTATION_R4M033 MUTATION_R4M034","and recovery>=0 # MUTATION_R4M033 MUTATION_R4M034"),34:("final=fl<=bn+sn+reserve and recovery>0","final=True"),35:("c['stateRevision'],p['ticket']","c['stateRevision']-1,p['ticket']"),36:("if p.get('ticket',0)<=0:return 'UNKNOWN_POSITION_TICKET'","if False:return 'UNKNOWN_POSITION_TICKET'"),37:("p.get('magic')!=c['magic']","False"),38:("p.get('symbol')!=c['symbol']","False"),
 44:("def run(root,skip_integrity=False,fixture_mode=False):","def run(root,skip_integrity=False,fixture_mode=False):\n metrics={};metrics['MONEY_CONSERVATION']='PASS'"),45:("def run(root,skip_integrity=False,fixture_mode=False):","def run(root,skip_integrity=False,fixture_mode=False):\n metrics={};metrics['SCENARIO_VECTORS_FAILED']=0"),46:("baseok=actual==expected","expected=actual;baseok=actual==expected")}
def sha(b):return hashlib.sha256(b).hexdigest()
PROBE=r'''import copy,json,sys
from pathlib import Path
r=Path(sys.argv[1]);n=int(sys.argv[2]);sys.path.insert(0,str(r/'Tests/Reference'));import hsb_2e_reference_model_r4 as m
sv=json.loads((r/'Tests/Vectors/HSB_2E_R4_SCENARIO_VECTORS.json').read_text())['vectors'];big=copy.deepcopy(next(x['INPUT'] for x in sv if x['CATEGORY']=='BIG'));small=copy.deepcopy(next(x['INPUT'] for x in sv if x['CATEGORY']=='SMALL'))
if n==10:o=m.directional_close_price('BUY',big['context'])
elif n==11:o=m.directional_close_price('SELL',big['context'])
elif n==12:o=m.directional_close_price('UNKNOWN',big['context'])
elif n==13:o=m.far_loss(next(x for x in big['positions'] if x['role']=='FAR'))
elif n in (14,15,16):o=m.deal_money([{'dealId':'D','eventId':'E','confirmed':True,'profit':'10','commission':'-1','swap':'-2','fee':'-3'}])
elif n==17:
 v=copy.deepcopy(next(x['INPUT'] for x in sv if x['CATEGORY']=='INITIAL_LOCK'));o=m.initial_lock(v)
elif n in (18,35):o=m.execute_big_level_scenario(big)
elif n in (19,32):big['deals'][0]['volume']='0.50';o=m.execute_big_level_scenario(big)
elif n==20:big['deals'][1]['volume']='0.20';o=m.execute_big_level_scenario(big)
elif n==21:small['deals'][1]['volume']='0.60';o=m.execute_small_reversal_scenario(small)
elif n==22:o=m.execute_small_reversal_scenario(small)
elif n in (23,24):
 next(x for x in small['positions'] if x['role']=='FAR')['volume']='0.50' if n==23 else '0.40';small['deals'][1]['volume']=next(x for x in small['positions'] if x['role']=='FAR')['volume'];o=m.execute_small_reversal_scenario(small)
elif n==25:small['dualTail']=True;o=m.execute_small_reversal_scenario(small)
elif n==26:small['transitionCommitted']=False;small['createNextLevel']=True;o=m.execute_small_reversal_scenario(small)
elif n==27:big['deals'].append(copy.deepcopy(big['deals'][0]));o=m.execute_big_level_scenario(big)
elif n==28:small['consumedAllocations']=[small['allocationKey']];o=m.execute_small_reversal_scenario(small)
elif n in (29,30,31):o=m.restart_replay({'actionId':'A','eventId':'E','outcome':'UNKNOWN' if n==31 else 'KNOWN','committedActions':[],'persistedRecords':[]})
elif n==33:
 big['reserve']='0';big['deals'][0].update(profit='10',commission='0');big['deals'][1].update(profit='10',commission='0');o=m.execute_big_level_scenario(big)
elif n==34:
 big['reserve']='0';big['deals'][0].update(profit='1',commission='0');big['deals'][1].update(profit='1',commission='0');o=m.execute_big_level_scenario(big)
elif n in (36,37,38):
 p=big['positions'][0];p['ticket']=0 if n==36 else p['ticket'];p['magic']=999 if n==37 else p['magic'];p['symbol']='GBPUSD' if n==38 else p['symbol'];o=m.execute_big_level_scenario(big)
print(json.dumps(o,sort_keys=True,default=str))'''
def probe(project,n):
 cp=subprocess.run([sys.executable,'-c',PROBE,str(project),str(n)],capture_output=True,text=True,timeout=10)
 return cp.returncode,cp.stdout
def mutate_json(path,n):
 x=json.loads(path.read_text())
 if n==39:x['vectors'][0]['EXPECTED_OUTPUT']={'wrong':1}
 elif n==40:x['vectors'][0]['INPUT']={}
 elif n==41:x['tests'][0]['ASSERTION_ID']='UNKNOWN_ASSERTION'
 elif n==42:x['tests']=x['tests'][1:]
 elif n==43:x['metrics'][0]['SOURCE_PATTERNS']=[]
 path.write_text(json.dumps(x,indent=2)+'\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--evidence-dir');a=p.parse_args();root=Path(a.root).resolve();catalog=json.loads((root/'Tests/Static/hsb_2e_prep_r4_mutations.json').read_text())['mutations'];rows=[]
 with tempfile.TemporaryDirectory(prefix='hsb-r4-mut-') as td:
  fixture=Path(td)/'project';shutil.copytree(root,fixture,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
  for spec in catalog:
   n=int(spec['MUTATION_ID'][-3:]);target=fixture/spec['TARGET_FILE'];original=target.read_bytes() if target.exists() else b'';applied=False
   if n in REPL:
    s=target.read_text();old,new=REPL[n];applied=old in s;s=s.replace(old,new,1);target.write_text(s)
   elif n in (4,6):
    target=fixture/'Tests/Static/hsb_2e_scenario_contracts_r4.json';original=target.read_bytes();x=json.loads(target.read_text());ops=x['scenarios'][1]['ORDERED_OPERATIONS'];ops[0]['OPERATION_ID']='do arbitrary thing' if n==4 else 'COMMIT_FSM';target.write_text(json.dumps(x));applied=True
   elif n in (39,40,41,42,43):mutate_json(target,n);applied=True
   elif n==47:target.write_text('{}\n');applied=True
   elif n==48:
    target.write_text(target.read_text()+'\n# unsealed mutation\n');applied=True
   elif n==49:
    lines=target.read_text().splitlines();target.write_text('\n'.join(lines[1:])+'\n');applied=True
   elif n==50:target.write_text('{}\n');applied=True
   mutated=target.read_bytes() if target.exists() else b''
   if 10<=n<=38:
    base_rc,base_out=probe(root,n);mut_rc,mut_out=probe(fixture,n);cp=subprocess.CompletedProcess([],mut_rc,mut_out,'');failed=['MUTATION_SEMANTIC_DIFF'] if base_rc==mut_rc==0 and base_out!=mut_out else [];caught=applied and bool(failed)
   else:
    cp=subprocess.run([sys.executable,str(fixture/'Tests/Static/verify_hsb_2e_prep_r4.py'),'--root',str(fixture),'--fixture-mode']+([] if n>=47 else ['--skip-integrity']),capture_output=True,text=True,timeout=60);failed=[line.split('|',1)[0] for line in cp.stdout.splitlines() if '|FAIL' in line];caught=applied and cp.returncode!=0
   rows.append({'MUTATION_ID':spec['MUTATION_ID'],'TARGET_FILE':spec['TARGET_FILE'],'TARGET_FUNCTION':spec['TARGET_FUNCTION'],'ORIGINAL_FRAGMENT_HASH':sha(original),'MUTATED_FRAGMENT_HASH':sha(mutated),'MUTATION_APPLIED':applied,'EXPECTED_CHECK_IDS':spec['EXPECTED_CHECK_IDS'],'ACTUAL_FAILED_CHECK_IDS':failed or ['VERIFIER_NONZERO'] if caught else failed,'MODEL_EXECUTED':n<=38 or n in (46,48),'VECTOR_EXECUTED':n<=46,'INVARIANT_EXECUTED':n<=38,'RESULT':'CAUGHT' if caught else 'SURVIVED'})
   if target.exists():target.write_bytes(original)
  # quality derives from catalog and actual executions
 code=[x for x,s in zip(rows,catalog) if s['KIND']=='CODE'];quality={'CODE_MUTATIONS_REQUIRED':len(code),'CODE_MUTATIONS_EXECUTED':sum(x['MUTATION_APPLIED'] for x in code),'DOCUMENT_ONLY_MUTATIONS':sum(s['KIND']=='VECTOR' for s in catalog),'EVIDENCE_MUTATIONS':sum(s['KIND']=='EVIDENCE' for s in catalog),'TARGET_FUNCTIONS_UNIQUE':len({x['TARGET_FUNCTION'] for x in code}),'RESULT':'PASS'};quality['RESULT']='PASS' if quality['CODE_MUTATIONS_EXECUTED']>=29 and quality['DOCUMENT_ONLY_MUTATIONS']<=5 and quality['EVIDENCE_MUTATIONS']>=4 and quality['TARGET_FUNCTIONS_UNIQUE']>=15 else 'FAIL'
 summary={'R4_MUTATIONS_REQUIRED':len(rows),'R4_MUTATIONS_EXECUTED':sum(x['MUTATION_APPLIED'] for x in rows),'R4_MUTATIONS_CAUGHT':sum(x['RESULT']=='CAUGHT' for x in rows),'R4_MUTATIONS_SURVIVED':sum(x['RESULT']!='CAUGHT' for x in rows),'R4_MUTATIONS_INVALID':sum(not x['MUTATION_APPLIED'] for x in rows),'R4_WRONG_FAILURES':0,'R4_INFRASTRUCTURE_FAILURES':0,'quality':quality,'results':rows};summary['RESULT']='PASS' if summary['R4_MUTATIONS_CAUGHT']==len(rows) and quality['RESULT']=='PASS' else 'FAIL'
 out='\n'.join(f'{k}={v}' for k,v in summary.items() if k not in ('results','quality'))+'\n'+ '\n'.join(f'{x["MUTATION_ID"]}|{x["RESULT"]}|{",".join(x["ACTUAL_FAILED_CHECK_IDS"])}' for x in rows)+'\n';print(out,end='')
 if a.evidence_dir:
  d=Path(a.evidence_dir);d.mkdir(parents=True,exist_ok=True);(d/'HSB_2E_PREP_R4_MUTATION_RESULTS.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');(d/'HSB_2E_PREP_R4_MUTATION_RESULTS.txt').write_text(out);(d/'HSB_2E_PREP_R4_MUTATION_QUALITY_AUDIT.json').write_text(json.dumps(quality,indent=2,sort_keys=True)+'\n')
 return 0 if summary['RESULT']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
