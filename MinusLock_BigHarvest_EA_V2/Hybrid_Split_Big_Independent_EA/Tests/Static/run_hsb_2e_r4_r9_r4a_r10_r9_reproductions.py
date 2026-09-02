#!/usr/bin/env python3
"""Read-only reproductions of R9 replay binding and mutation-harness defects."""
import copy,hashlib,json,sys,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r9 as v9
import accept_hsb_2e_r4_r9_r4a_r9 as a9
from build_hsb_2e_r4_r9_r4a_r7_assets import cert
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def outcome(fn):
 try:fn();return {'class':'ACCEPTED','checkId':'','reason':''}
 except v9.NormativeError as e:return {'class':'NORMATIVE_REJECTION','checkId':e.checkId,'reason':e.reason}
 except Exception as e:return {'class':'INFRASTRUCTURE_ERROR','checkId':type(e).__name__,'reason':str(e)}
def main():
 fs=v9.fixtures();r=next(copy.deepcopy(f['scenarioInput']) for f in fs if f.get('scenarioInput',{}).get('phase')=='REPLAY');before=copy.deepcopy(r);src=r['replayContract']['historicalSourceObjects'];old=src['context']['magic'];src['context']['magic']=old+100;r['certificate']=cert(src)
 foreign={'caseId':'R9_FOREIGN_HISTORICAL_MAGIC_RESEALED','positiveSha256':sha(before),'mutatedSha256':sha(r),'diff':{'path':'replayContract.historicalSourceObjects.context.magic','before':old,'after':old+100,'certificateResealedInFixture':True},'expected':'NORMATIVE_REJECTION','actual':outcome(lambda:v9.runtime(r))}
 # Reproduce cross-file persistence of the historical single-workspace algorithm.
 a=ROOT/'Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py';b=ROOT/'Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py';tmp=Path(tempfile.mkdtemp(prefix='.r10_repro_',dir=ROOT))
 try:
  aa=tmp/a.name;bb=tmp/b.name;shutil.copy2(a,aa);shutil.copy2(b,bb);baseA=hashlib.sha256(aa.read_bytes()).hexdigest();baseB=hashlib.sha256(bb.read_bytes()).hexdigest();aa.write_text(aa.read_text()+'\n# MUTANT_A\n');afterA=hashlib.sha256(aa.read_bytes()).hexdigest();bb.write_text(bb.read_text()+'\n# MUTANT_B\n');inventory={'beforeB':{'r8':baseA,'r9':baseB},'afterB':{'r8':hashlib.sha256(aa.read_bytes()).hexdigest(),'r9':hashlib.sha256(bb.read_bytes()).hexdigest()},'priorMutationPersisted':hashlib.sha256(aa.read_bytes()).hexdigest()==afterA and afterA!=baseA}
 finally:shutil.rmtree(tmp)
 # A protected-only mismatch is distinct from semantic outcome evidence.
 fresh=a9.fresh_result();semantic=a9.assess(fresh,skip_scope=True);hash_only={'semanticFindings':[x['check'] for x in semantic['findings']],'protectedHashCanIndependentlyFailAcceptance':True,'note':'R9 harness counted exit 1 without requiring affected outcome IDs; protected mismatch can therefore masquerade as semantic catch.'}
 out={'targetSha':'8237e52bbbd3c7a4822c5189ee72969a43a4df5a','foreignHistoricalContext':foreign,'mutationContamination':inventory,'hashOnlyDetection':hash_only};print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
