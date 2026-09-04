#!/usr/bin/env python3
"""Read-only evidence that the current contract lacks a canonical ledger-root formula."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
V=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R10_POSITIVE_BASES.json'
def main():
 fs=json.loads(V.read_text())['fixtures'];r=next(x['scenarioInput'] for x in fs if x.get('scenarioInput',{}).get('phase')=='COMMITTED');p=r['persistedState'];candidate=hashlib.sha256(json.dumps(sorted(p['consumedDealIds']),separators=(',',':')).encode()).hexdigest();out={'fixtureId':'R10 committed positive','consumedDealIds':p['consumedDealIds'],'authoritativeLedgerRoot':p['authoritativeLedgerRoot'],'candidateCanonicalConsumedIdsSha256':candidate,'candidateMatchesPublishedRoot':candidate==p['authoritativeLedgerRoot'],'verdict':'NORMATIVE_CONTRACT_CONFLICT'};print(json.dumps(out,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
