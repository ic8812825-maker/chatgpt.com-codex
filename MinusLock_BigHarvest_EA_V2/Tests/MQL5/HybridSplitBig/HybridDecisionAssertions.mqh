#ifndef __BH_HYBRID_DECISION_ASSERTIONS_MQH__
#define __BH_HYBRID_DECISION_ASSERTIONS_MQH__

int HybridDecisionTestFailures=0;

void HybridAssertTrue(bool condition,string name,string details="")
{
   if(condition) Print("PASS "+name);
   else { HybridDecisionTestFailures++; Print("FAIL "+name+" "+details); }
}

void HybridAssertReject(HybridEvaluationResult &result,HybridRejectCode expected,string name)
{
   HybridAssertTrue(result.rejectCode==expected,name,StringFormat("expected=%d actual=%d reason=%s",(int)expected,(int)result.rejectCode,result.reason));
}

#endif // __BH_HYBRID_DECISION_ASSERTIONS_MQH__
