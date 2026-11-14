"""Re-run DG01 goldens with save redirected; do not rewrite historical evidence."""
import sys,json,importlib,traceback
from pathlib import Path
sys.dont_write_bytecode=True
p=Path(__file__).resolve().parent;sys.path.insert(0,str(p.parent/'Static'));sys.path.insert(0,str(p.parent/'Reference'))
a=importlib.import_module('HSBI_DG01_common')
def save(name,data):
 (p/('historical_'+name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
a.save=save
try:
 runner=importlib.import_module('HSBI_DG01_reference_tests');code=runner.main()
except Exception:
 code=2;(p/'historical_error.txt').write_text(traceback.format_exc())
(p/'historical_run.json').write_text(json.dumps(dict(ExitCode=code,Runner='Tests/Static/HSBI_DG01_reference_tests.py',SaveRedirection='Tests/Close/historical_*.json',HistoricalWritesAllowed=False),indent=2)+'\n')
raise SystemExit(code)
