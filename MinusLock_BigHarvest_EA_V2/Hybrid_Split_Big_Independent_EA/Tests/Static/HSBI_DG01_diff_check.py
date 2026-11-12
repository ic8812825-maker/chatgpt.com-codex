"""Reproducible applicability-only check. Never applies the patch."""
import hashlib,sys
import HSBI_DG01_common as a

def main():
 patch=a.ROOT/'Tests/Reference/HSBI_DG01_MINIMAL_R1_1_CANDIDATE.patch';source=a.ROOT/'Include/Money/HSBI_EconomicLedgerTypes.mqh';before=a.sha(source)
 candidate=(a.ROOT/'Tests/Reference/HSBI_DG01_identity_candidate.mqh').read_text();body=candidate[candidate.index('enum HSBI_EconomicIdentityStatusV2'):candidate.rindex('#endif')]
 x=a.run(['git','apply','--check','-'],input=patch.read_text(),cwd=a.REPO)
 x.update(TestID='DIFF-CHECK-ONLY',Applied=False,Target=str(source.relative_to(a.REPO)),BaseSHA256=before,CandidateBodySHA256=hashlib.sha256(body.encode()).hexdigest(),SubjectSHA256=a.sha(patch),RunnerSHA256=a.sha(__file__),SourceBytesUnchanged=a.sha(source)==before,ProofBoundary='Parse/applicability only. No apply, no native compiler.');a.save('DIFF_CHECK',x);print('DIFF_CHECK',x['ExitCode'],'UNCHANGED',x['SourceBytesUnchanged']);return x['ExitCode'] or int(not x['SourceBytesUnchanged'])
if __name__=='__main__':raise SystemExit(main())
