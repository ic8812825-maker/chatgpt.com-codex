"""Compile unchanged header subset through a named portability shim, preserve FAIL."""
import subprocess,json,hashlib,datetime,tempfile
from pathlib import Path
p=Path(__file__).resolve().parent
runtime=tempfile.TemporaryDirectory(prefix='cpp-',dir=p)
cmd=['g++','-std=c++17','-Wall','-Wextra','-pedantic',str(p/'production_subset.cpp'),'-o',str(Path(runtime.name)/'production_subset.bin')]
c=subprocess.run(cmd,text=True,capture_output=True)
r=subprocess.run([str(Path(runtime.name)/'production_subset.bin')],text=True,capture_output=True) if c.returncode==0 else None
rows=[]
if r:
 for line in r.stdout.splitlines():
  f=line.split('\t')
  if len(f)==4: rows.append(dict(ID=f[0],Actual=int(f[1]),Expected=int(f[2]),Status=f[3]))
result=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),Command=cmd,CompileExit=c.returncode,CompileOutput=c.stdout+c.stderr,RunExit=r.returncode if r else None,Rows=rows,Pass=sum(x['Status']=='PASS' for x in rows),Fail=sum(x['Status']=='FAIL' for x in rows),Boundary='C++17 unchanged header subset + shim. NOT MQL5. PROPOSED expectations explicitly named. Failure is preserved; runner exits nonzero on failure.',HarnessSHA256=hashlib.sha256((p/'production_subset.cpp').read_bytes()).hexdigest())
(p/'production_subset_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
runtime.cleanup()
raise SystemExit(c.returncode or (r.returncode if r else 2))
