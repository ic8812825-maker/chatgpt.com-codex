#!/usr/bin/env python3
"""Read-only C2 reproduction; new C3 evidence only; frozen package on exact Git archive."""
import copy,io,tarfile,tempfile,types,subprocess,sys,json
from pathlib import Path
import check_hsbi_02b_r0e_c3_common as a
import check_hsbi_02b_r0e_c2_package as p

def main():
 started=a.now();reference=a.c2.run();a.save('C2_REFERENCE',dict(a.metadata(__file__),**{k:v for k,v in reference.items() if k not in ('StartedUtc','FinishedUtc')},StartedUtc=started,FinishedUtc=a.now(),Command=[sys.executable,*sys.argv],ExecutionRole='reference',ExitCodeScope='computed role outcome within one CLI; parent returns final ExitCode',ExitCode=int(reference['Fail']+reference['InfrastructureErrors']>0)))
 ms=a.mutants.run();a.save('C2_MUTATIONS',dict(a.metadata(__file__),**ms,StartedUtc=started,FinishedUtc=a.now(),Command=[sys.executable,*sys.argv],ExecutionRole='mutation',ExitCodeScope='computed role outcome within one CLI; parent returns final ExitCode',ExitCode=int(ms['UnexplainedSurvivors']+ms['InfrastructureErrors']>0)))
 with tempfile.TemporaryDirectory(prefix='R0E_C3_archive_',dir=a.ROOT/'Tests') as td:
  raw=subprocess.check_output(['git','archive',a.BASE,a.PREFIX],cwd=a.REPO)
  with tarfile.open(fileobj=io.BytesIO(raw)) as archive:archive.extractall(td,filter='data')
  root=Path(td)/a.PREFIX
  mod=types.ModuleType('archived_c2_checker');mod.__file__=p.__file__
  # Only path bookkeeping changes; verify/probe semantics remain frozen.
  source=Path(p.__file__).read_text().replace('str(Path(mu.__file__).relative_to(ROOT))','str(Path(mu.__file__).relative_to(t.ROOT))')
  exec(compile(source,p.__file__,'exec'),mod.__dict__);mod.ROOT=root;mod.REPO=a.REPO;mod.verify.__defaults__=(root,a.REPO,True);mod.git_tree.__defaults__=(a.REPO,)
  package=mod.probes()
 a.save('C2_PACKAGE',dict(a.metadata(__file__),**package,OriginalCheckerHash=a.sha(Path(p.__file__)),Adapter='Archive root/default arguments + relative path bookkeeping only; runner hash identifies exact adapter',StartedUtc=started,FinishedUtc=a.now(),Command=[sys.executable,*sys.argv],ExecutionRole='package',ExitCodeScope='computed role outcome within one CLI; parent returns final ExitCode',ExitCode=int(package['Positive']!='PASS' or package['NegativeFailed']>0)))
 rows=reference['Rows'];pairs=[(r['TestID'],r['ContextID']) for r in rows]
 # Repetition audit: contexts are repeated executions, not independent scenarios.
 fixture_groups={}
 for row in rows:
  if row['ContextID']==0:fixture_groups.setdefault(json.dumps(row.get('Input',{}).get('Calls',[]),sort_keys=True),[]).append(row['TestID'])
 duplicate_groups=[v for v in fixture_groups.values() if len(v)>1]
 result=dict(a.metadata(__file__),StartedUtc=started,FinishedUtc=a.now(),Command=[sys.executable,*sys.argv],ReferenceCounts={k:reference[k] for k in ('Scenarios','Executions','Comparisons','SchemaProbes','Pass','Fail','InfrastructureErrors')},MutationCounts={k:ms[k] for k in ('CatalogSize','Killed','RedundantSurvivors','UnexplainedSurvivors','InfrastructureErrors')},PackageCounts={k:package[k] for k in ('Positive','NegativePassed','NegativeFailed')},UniqueTestContextPairs=len(set(pairs)),DuplicateContext0CallGroups=duplicate_groups,DistinctScenarioWarning='158 TestIDs are not158 unique mathematical inputs. Shared positive controls/direct shapes and contexts are not independent proofs. Exact groups above derive from actual operation-call arguments.',Traceability=[dict(TestID=r['TestID'],Operation=r['Operation'],Observed=r['Operation'] in r['SubjectCalls']) for r in rows if r['ContextID']==0],HistoricalArtifactsUntouched=True)
 result['ExitCode']=int(reference['Pass']!=1264 or reference['SchemaProbes']!=2462 or reference['Comparisons']!=9914 or reference['Fail'] or reference['InfrastructureErrors'] or ms['Killed']!=64 or ms['RedundantSurvivors']!=6 or package['NegativePassed']!=58 or package['NegativeFailed'] or not all(r['Observed'] for r in result['Traceability']));a.save('REPRODUCTION',result);print('C2_REPRODUCTION',result['ExitCode']);return result['ExitCode']
if __name__=='__main__':raise SystemExit(main())
