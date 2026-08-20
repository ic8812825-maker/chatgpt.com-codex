#!/usr/bin/env python3
"""Offline, fail-closed verifier for administrator-provided MetaEditor/MT5 logs."""
import argparse,re,sys,tempfile
from collections import Counter
from pathlib import Path
TRADE=re.compile(r'(?i)\b(OrderSend(?:Async)?|CTrade|TRADE_ACTION_|trade request|position open|buy request|sell request)\b')
def compile_result(text):
 m=re.findall(r'(?im)^\s*(\d+)\s+errors?\s*,\s*(\d+)\s+warnings?\s*$',text)
 return (int(m[-1][0]),int(m[-1][1])) if len(m)==1 else None
def tests(text):
 pairs=re.findall(r'(?m)^T(\d{3})=(PASS|FAIL)$',text);c=Counter(int(i) for i,_ in pairs);return {int(i):v for i,v in pairs},c
def verify(main,test,experts,journal,sha):
 cr1=compile_result(main);cr2=compile_result(test);e,ec=tests(experts);j,jc=tests(journal);required=set(range(1,465));found=set(e);summ=re.findall(r'(?m)^SUMMARY_TOTAL=(\d+)\s+SUMMARY_PASS=(\d+)\s+SUMMARY_FAIL=(\d+)$',experts);sha_ok=(experts.count('TESTED_GIT_SHA='+sha)==1 and journal.count('TESTED_GIT_SHA='+sha)==1);same=e==j and set(j)==found
 metrics={'MAIN_COMPILE_ERRORS':cr1[0] if cr1 else -1,'MAIN_COMPILE_WARNINGS':cr1[1] if cr1 else -1,'TEST_COMPILE_ERRORS':cr2[0] if cr2 else -1,'TEST_COMPILE_WARNINGS':cr2[1] if cr2 else -1,'TEST_IDS_REQUIRED':464,'TEST_IDS_FOUND':len(found),'TEST_IDS_MISSING':len(required-found),'TEST_IDS_DUPLICATE':sum(n-1 for n in ec.values() if n>1)+sum(n-1 for n in jc.values() if n>1),'TEST_FAILURES':sum(v=='FAIL' for v in e.values()),'SUMMARY_TOTAL':int(summ[0][0]) if len(summ)==1 else -1,'SUMMARY_PASS':int(summ[0][1]) if len(summ)==1 else -1,'SUMMARY_FAIL':int(summ[0][2]) if len(summ)==1 else -1,'TRADE_REQUEST_MARKERS':len(TRADE.findall(experts))+len(TRADE.findall(journal)),'SHA_MATCH':int(sha_ok),'EXPERTS_JOURNAL_MATCH':int(same)}
 ok=cr1==(0,0) and cr2==(0,0) and found==required and metrics['TEST_IDS_DUPLICATE']==0 and metrics['TEST_FAILURES']==0 and summ==[('464','464','0')] and metrics['TRADE_REQUEST_MARKERS']==0 and sha_ok and same
 return metrics,'PASS' if ok else 'UNABLE_TO_PROVE'
def self_test():
 sha='a'*40;base='TESTED_GIT_SHA='+sha+'\n'+'\n'.join(f'T{i:03}=PASS' for i in range(1,465))+'\nSUMMARY_TOTAL=464 SUMMARY_PASS=464 SUMMARY_FAIL=0\n';compile='0 errors, 0 warnings\n'
 cases={'clean':(compile,compile,base,base,True),'missing':(compile,compile,base.replace('T001=PASS\n',''),base,False),'duplicate':(compile,compile,base.replace('T001=PASS','T001=PASS\nT001=PASS'),base,False),'fail':(compile,compile,base.replace('T001=PASS','T001=FAIL'),base.replace('T001=PASS','T001=FAIL'),False),'false_summary':(compile,compile,base.replace('SUMMARY_PASS=464','SUMMARY_PASS=463'),base,False),'compile_error':('1 errors, 0 warnings',compile,base,base,False),'warning':(compile,'0 errors, 1 warnings',base,base,False),'trade':(compile,compile,base+'OrderSend\n',base,False),'wrong_sha':(compile,compile,base.replace(sha,'b'*40),base,False),'truncated':(compile,compile,base[:-30],base,False),'mismatch':(compile,compile,base,base.replace('T001=PASS','T001=FAIL'),False)}
 results={k:(verify(*v[:4],sha)[1]=='PASS')==v[4] for k,v in cases.items()};print('\n'.join(f'UE_{k}={"PASS" if v else "FAIL"}' for k,v in results.items()));print(f'USER_EVIDENCE_SELF_TESTS={sum(results.values())}/{len(results)}');return all(results.values())
def main():
 p=argparse.ArgumentParser();p.add_argument('--main-compile-log');p.add_argument('--test-compile-log');p.add_argument('--experts-log');p.add_argument('--journal-log');p.add_argument('--expected-sha');p.add_argument('--self-test',action='store_true');a=p.parse_args()
 if a.self_test:return 0 if self_test() else 1
 if not all((a.main_compile_log,a.test_compile_log,a.experts_log,a.journal_log,a.expected_sha)):p.error('all log arguments and --expected-sha are required')
 vals=[Path(x).read_text(encoding='utf-8-sig',errors='replace') for x in (a.main_compile_log,a.test_compile_log,a.experts_log,a.journal_log)];m,res=verify(*vals,a.expected_sha);print('\n'.join(f'{k}={v}' for k,v in m.items()));print('USER_EVIDENCE_RESULT='+res);return 0 if res=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
