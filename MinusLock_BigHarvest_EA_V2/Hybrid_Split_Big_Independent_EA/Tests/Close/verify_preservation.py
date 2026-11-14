"""Compare every baseline byte/mode/blob, and reject changes outside allowlisted new paths."""
import json,hashlib,subprocess,datetime,sys
from pathlib import Path
p=Path(__file__).resolve().parents[2];here=p/'Tests/Close';repo=p.parents[1];b=json.loads((here/'baseline.json').read_text());issues=[]
for f in b['Files']:
 path=p/f['Path']
 if not path.exists():issues.append(dict(Path=f['Path'],Issue='MISSING'));continue
 content=path.read_bytes()
 if hashlib.sha256(content).hexdigest()!=f['SHA256']:issues.append(dict(Path=f['Path'],Issue='SHA256_CHANGED'))
 if subprocess.check_output(['git','hash-object','--',str(path)],cwd=repo,text=True).strip()!=f['GitBlobSHA']:issues.append(dict(Path=f['Path'],Issue='GIT_BLOB_CHANGED'))
 mode='100755' if path.stat().st_mode&0o111 else '100644'
 if mode!=f['Mode']:issues.append(dict(Path=f['Path'],Issue='MODE_CHANGED'))
tracked=subprocess.check_output(['git','diff','--name-only',b['BASE_SHA']],cwd=repo,text=True).splitlines()
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=repo,text=True).splitlines()
allowed=['MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_CLOSE_','MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_MONEY_CONTRACT_','MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_R11_P0_','MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Tests/Close/']
for path in tracked+untracked:
 if not any(path.startswith(x) for x in allowed):issues.append(dict(Path=path,Issue='OUTSIDE_NEW_ALLOWLIST'))
result=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),BASE_SHA=b['BASE_SHA'],BaselineFilesChecked=len(b['Files']),AllBaselineBytesModesBlobsUnchanged=not any(x['Issue']!='OUTSIDE_NEW_ALLOWLIST' for x in issues),AllChangesWithinNewAllowlist=not any(x['Issue']=='OUTSIDE_NEW_ALLOWLIST' for x in issues),ProductionSourcesChecked=sum(f['Path'].endswith(('.mqh','.mq5')) and not f['Path'].startswith('Tests/') for f in b['Files']),Issues=issues,ChangedOrUntracked=sorted(set(tracked+untracked)),Boundary='All baseline project files compared; repository diff/untracked path list checks no working-tree changes outside project. Git metadata operations are not project modifications.')
if '--check-only' not in sys.argv:(here/'preservation_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print({k:result[k] for k in ('BaselineFilesChecked','ProductionSourcesChecked','AllBaselineBytesModesBlobsUnchanged','AllChangesWithinNewAllowlist','Issues')})
raise SystemExit(int(bool(issues)))
