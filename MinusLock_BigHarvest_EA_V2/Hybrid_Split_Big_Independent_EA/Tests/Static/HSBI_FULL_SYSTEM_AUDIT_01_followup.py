"""Fresh R0F actual cases (not catalog enumeration), native discovery, archive index."""
import sys,json,subprocess
from pathlib import Path
import HSBI_FULL_SYSTEM_AUDIT_01_common as a

def main():
 import check_hsbi_02b_r0f_contracts as f
 started=a.now();rows=[]
 for case in f.cases():
  try:actual=case['Run']();result='PASS' if actual==case['Expected'] else 'FAIL';error=None
  except Exception as e:actual=None;result='INFRASTRUCTURE_ERROR';error=type(e).__name__+': '+str(e)
  rows.append(dict(TestID=case['TestID'],Expected=case['Expected'],Actual=actual,Result=result,Error=error))
 a.save('R0F_FRESH',dict(a.meta(__file__),SubjectRunnerHash=a.sha(f.__file__),StartedUtc=started,FinishedUtc=a.now(),Rows=rows,Pass=sum(r['Result']=='PASS' for r in rows),Fail=sum(r['Result']=='FAIL' for r in rows),ExitCode=int(any(r['Result']!='PASS' for r in rows)),Note='Earlier REGRESSIONS R0F_API enumerated116 cases only. This separate run actually invokes every Run callable; frozen main()/save() not called.'))
 commands=[]
 for name in ['metaeditor64','metaeditor','MetaEditor64.exe','terminal64','wine']:
  p=subprocess.run(['which',name],capture_output=True,text=True);commands.append(dict(Command=['which',name],ExitCode=p.returncode,Stdout=p.stdout,Stderr=p.stderr))
 cmd=['rg','--files','/opt','/workspace','/usr/local/bin','-g','*[Mm]eta[Ee]ditor*','-g','*terminal64*'];p=subprocess.run(cmd,text=True,capture_output=True);commands.append(dict(Command=cmd,ExitCode=p.returncode,Stdout=p.stdout,Stderr=p.stderr))
 compiler_available=any(x['ExitCode']==0 and x['Stdout'].strip() for x in commands[:3]) or any('metaeditor' in x.lower() and Path(x).suffix.lower()=='.exe' for x in p.stdout.splitlines())
 a.save('NATIVE_ENVIRONMENT',dict(a.meta(__file__),Commands=commands,MQL5_COMPILE='NOT_RUN',MQL5_NATIVE_TESTS='NOT_RUN',StrategyTester='NOT_RUN',CompilerAvailable=compiler_available,Scope='No real MetaEditor/terminal/Wine in PATH/searched locations; Windows helper is not installed compiler. No broker/account IO performed.'))
 old=a.inventory();index=[]
 for file in old:
  if file.startswith('Reports/') and ('NEXT_STAGE_02' in file or 'HSB_2D_V1_R7' in file):
   p=a.ROOT/file;text=p.read_text();statuses=[dict(Line=i,Text=s) for i,s in enumerate(text.splitlines(),1) if any(x in s for x in ('FINAL_STATUS','VERDICT','COMPLETE=','UNPROVEN','NOT_RUN','ADMIN_APPROVAL','AWAITING','FAIL'))]
   index.append(dict(File=file,SHA256=a.sha(p),StatusLocators=statuses,ReviewBoundary='HISTORICAL_EVIDENCE_ONLY unless separately reproduced by current tests; indexing is not semantic reacceptance'))
 a.save('HISTORICAL_INDEX',dict(a.meta(__file__),Rows=index,Count=len(index)))
 print('FOLLOWUP R0F',len(rows),sum(r['Result']=='PASS' for r in rows),'native NOT_RUN')
 return int(any(r['Result']!='PASS' for r in rows))
if __name__=='__main__':raise SystemExit(main())
