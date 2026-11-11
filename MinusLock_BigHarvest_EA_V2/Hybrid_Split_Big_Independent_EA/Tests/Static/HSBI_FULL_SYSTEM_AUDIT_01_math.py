"""Independent Fraction/integer/Decimal specification vectors. Not MQL5 evaluator."""
from fractions import Fraction as F
from decimal import Decimal,localcontext,ROUND_HALF_EVEN
import HSBI_FULL_SYSTEM_AUDIT_01_common as a

def rows():
 out=[]
 def add(i,actual,expected,derivation):out.append(dict(TestID=i,Actual=actual,Expected=expected,Result='PASS' if actual==expected else 'FAIL',Derivation=derivation,ProofBoundary='EXACT_SPECIFICATION_ARITHMETIC_ONLY'))
 add('FINAL-50-16',[500-450,10+5+1,(500-450)>=(10+5+1)],[50,16,True],'No adding reserve subset again; 500realized-450openloss=50.')
 add('FAR-ABSOLUTE',[max(0,-(-50)),50-40,30>=50,30>=50-40],[50,10,False,True],'Absolute50 vs increment10 are different coverage obligations.')
 levels=[dict(Transition=10,Reserve=100,Loss=90,Buffer=1),dict(Transition=5,Reserve=10,Loss=20,Buffer=1)];margins=[x['Reserve']-x['Loss']-x['Buffer'] for x in levels];old=max(range(2),key=lambda i:levels[i]['Transition']);new=min(range(2),key=lambda i:margins[i])
 add('CR09-EXTREMA',[margins,old+1,new+1,margins[old]>0,all(v>0 for v in margins)],[[9,-11],1,2,True,False],'ArgmaxTransition not argminMargin. Existing policy scope vs proposedalllevel assessment.')
 partial=[];s=0
 for f in [-15,100]:s+=f;partial.append(max(0,-s))
 add('TRANSITION-ABC',[partial[-1],max(partial),any(x>12 for x in partial)],[0,15,True],'Signedfinal loss0,peak15,sticky breachtrue; no chosenproductionpolicy.')
 add('CAP-MIN',min(20,15,12,18),12,'Four caps same money units; allknownfinite nonnegative required.')
 add('COMPRESSION',[str(F(1)-F(3,5)),str((F(1)-F(3,5))/F(1)),F(3,5)<=F(4,5)],[str(F(2,5)),str(F(2,5)),True],'Lotdifference anddimensionlessratio distinct.')
 add('MARGIN-LEVEL',str(F(100)*1000/100),'1000','Percent convention; zero margin/actual broker semantics separate.')
 q=F(4,5);add('DEPTH-CONDITIONAL',[q**20>F(1,100),q**21<=F(1,100)],[True,True],'K21 iff uniformq for allsuccessfultransitions. Does not guarantee price moves or completion.')
 add('PREFIX-NOT-TAIL',[q*q==F(16,25),F(16,25)>q**3],[True,True],'Observedprefix .8,.64 and continuation.64: endpoint holds, global q-law fails. No wrong-helper oracle.')
 add('RANGE-MONOTONICITY',[F(1)>F(0),F(-1)>F(1)],[True,False],'Two control values showing one positive local step does not prove allfutureticks.')
 lot=(F(5)/20//F(1,10))*F(1,10);add('PARTIAL-FLOOR',[str(lot),str(lot*20),lot*20<=5],['1/5','4',True],'Budget5 loss20/lot step.1 =>.2lot,4money. Actualclose costs must be rechecked.')
 add('INT64-OVERFLOW',2**63-1+1>2**63-1,True,'Mathematical wider oracle showsunsupported int64 result; do not sum first in native long.')
 add('MONEY-RESOLUTION',[float(10**28)-.01==float(10**28),F(10**28)-F(1,100)!=F(10**28)],[True,True],'Finite64 cannot resolve cents at1e28; no complete productionconsume API tested.')
 add('PRICE-GRID',str(round(F(10012,100)/F(1,4))*F(1,4)),'100','Exactprice100.12/tick.25 ->nearest100.')
 add('LEVEL-DISTANCE',str(F(100)+(10+2*5)*F(1,100)),'501/5','Distancepoints converted to price; 100.2.')
 n=[(F(1,5),10),(F(3,10),5)];add('OBJECTIVE-NON_EQUIVALENCE',[str(min(n,key=lambda x:x[0])[0]),str(min(n,key=lambda x:x[1])[0])],['1/5','3/10'],'MinimumN and minimumRisk notgenerallyequivalent without additionalmonotonicproof.')
 add('GRID-ORIGIN',[[str(F(3,100)+i*F(1,50)) for i in range(2)],[str(F(4,100)+i*F(1,50)) for i in range(2)]],[['3/100','1/20'],['1/25','3/50']],'Differentlattices for nonalignedmin/step; no universal brokerorigin assumed.')
 with localcontext() as c:
  c.prec=32;c.rounding=ROUND_HALF_EVEN
  v=Decimal('.005');comp=v.quantize(Decimal('.01'))*2;aggregate=(v*2).quantize(Decimal('.01'))
  add('ROUNDING-POLICY',[str(comp),str(aggregate)],['0.00','0.01'],'All operands <=3digits, precision32 exact here. Illustration of component/aggregate policies, not brokerposting evidence.')
 add('COST-OVERLAP',[110-101,(110-101)-1],[9,8],'BUYactualopenAsk101/closeBid110 already executable; extra sameSpread1 undercounts by1. Unknown costbasis =>not safezero.')
 add('ACCOUNT-MODE-NETTING',1+(-1),0,'In one-position-per-symbol netting model BUY1+SELL1 closes exposure; two independentinitialtickets impossible withoutdifferentarchitecture.')
 return out
if __name__=='__main__':
 r=rows();a.save('MATH_TESTS',dict(a.meta(__file__),Rows=r,Pass=sum(x['Result']=='PASS' for x in r),Fail=sum(x['Result']=='FAIL' for x in r),ExitCode=int(any(x['Result']!='PASS' for x in r))));print('MATH',len(r),sum(x['Result']=='PASS' for x in r))
