#!/usr/bin/env python3
"""Reproduce R0D package coverage gaps on independent baseline archive, never edit history."""
import copy,hashlib,io,json,subprocess,tarfile,tempfile
from pathlib import Path
from datetime import datetime,timezone
import check_hsbi_02b_r0d_package as old
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];PREFIX=ROOT.relative_to(REPO).as_posix()+'/'
BASE='2d34c3378edc5f2df064282fa067bb4af2a1e3b0'
def main():
 start=datetime.now(timezone.utc).isoformat();rows=[]
 with tempfile.TemporaryDirectory(prefix='R0E_R0D_probes_',dir=ROOT/'Tests') as td:
  with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',BASE,PREFIX],cwd=REPO))) as tar:tar.extractall(td,filter='data')
  root=Path(td)/PREFIX;positive=old.verify(root,REPO)
  for name,path,edit in [
   ('empty-cases','Tests/Contracts/NEXT_STAGE_02B_R0D_VERIFICATION_MATRIX.json',lambda d:d.__setitem__('cases',[])),
   ('context-999','Tests/Evidence/NEXT_STAGE_02B_R0D_TEST_RESULTS.json',lambda d:d['tests'][0].__setitem__('context',999)),
   ('false-original-source-hash','Tests/Evidence/NEXT_STAGE_02B_R0D_MUTATION_RESULTS.json',lambda d:d['mutations'][0].__setitem__('OriginalSourceHash','0'*64)),
   ('false-mutant-source-hash','Tests/Evidence/NEXT_STAGE_02B_R0D_MUTATION_RESULTS.json',lambda d:d['mutations'][0].__setitem__('MutantSourceHash','0'*64)),
   ('approval-after-blank','Reports/NEXT_STAGE_02B_R0D_ADMIN_DECISIONS_RU.md',None)]:
   original=(root/path).read_bytes();proof=json.loads((root/old.PRES).read_text());original_proof=copy.deepcopy(proof)
   if edit:
    data=json.loads(original);edit(data);(root/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
   else:(root/path).write_text(original.decode().replace('AdministratorDecision:\n\n','AdministratorDecision:\n\nAPPROVED\n',1))
   proof['newArtifactHashes'][path]=hashlib.sha256((root/path).read_bytes()).hexdigest();(root/old.PRES).write_text(json.dumps(proof,indent=2)+'\n')
   errors=old.verify(root,REPO);rows.append(dict(ProbeID=name,Expected='REJECT_TAMPERED_PACKAGE',Actual='ACCEPT' if not errors else 'REJECT',Findings=errors,Classification='CONFIRMED' if not positive and not errors else 'NOT_REPRODUCED',Boundary='Frozen R0D checker; exact baseline archive; synthetic approval has no real administrative meaning'))
   (root/path).write_bytes(original);(root/old.PRES).write_text(json.dumps(original_proof,indent=2)+'\n')
 out=dict(BaseSHA=BASE,Command=['python','Tests/Static/check_hsbi_02b_r0e_r0d_provenance.py'],StartedUtc=start,FinishedUtc=datetime.now(timezone.utc).isoformat(),PositiveErrors=positive,probes=rows,SourceHashes={str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'Tests/Static/check_hsbi_02b_r0d_package.py':hashlib.sha256((ROOT/'Tests/Static/check_hsbi_02b_r0d_package.py').read_bytes()).hexdigest()})
 (ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_R0D_PROVENANCE_PROBES.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False));return int(bool(positive) or any(r['Classification']!='CONFIRMED' for r in rows))
if __name__=='__main__':raise SystemExit(main())
