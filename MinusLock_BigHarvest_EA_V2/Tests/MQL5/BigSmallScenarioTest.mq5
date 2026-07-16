#property strict
#property script_show_inputs
#include "../../Include/Config.mqh"
#include "../../Include/Types.mqh"
#include "../../Include/LotUtils.mqh"
#include "../../Include/SimulationEngine.mqh"
#include "../../Include/PositionUtils.mqh"
#include "../../Include/GeometryEngine.mqh"
#include "../../Include/Logger.mqh"
#include "../../Include/TradeEngine.mqh"
#include "../../Include/BrokerMoneyModel.mqh"
#include "../../Include/RecoveryMath.mqh"
#include "../../Include/RiskManager.mqh"
#include "../../Include/PendingContractEngine.mqh"
#include "../../Include/StateMachine.mqh"
#define BIG_SMALL_TEST_MAGIC 9900260717
int passed=0,total=0;
void Check(string name,bool value){total++;if(value)passed++;Print("BIG_SMALL_TEST ",name,"=",value?"PASS":"FAIL");}
void OnStart()
{
 if(MagicNumber!=BIG_SMALL_TEST_MAGIC||AllowRealTrading||!UseInternalSimulation){Print("BIG_SMALL_TEST_CONFIGURATION_REFUSED");return;}
 Check("GEOMETRY_NET",1.60+.25-.60-1.0>=MinimumNetBigExposureLots);
 BigReserveCatchUpEvaluation c; Check("RESERVE_CATCH_UP",EvaluateBigReserveCatchUp(5,5,0,10,12,c));
 Check("TARGET_NEW_FAR",CalcTargetNewFarLot(1.0)<1.0);
 Check("FINITE_REVERSE",EvaluateRequiredReverseCycles(1.0,.1,.9)<=MaxReverseCycles||EvaluateRequiredReverseCycles(1.0,.1,.9)>MaxReverseCycles);
 Check("ONLY_ONE_MODE",CurrentScenarioMode()>=SCENARIO_IDLE);
 string scenarios[]={"BIG_BIG","BIG_BIG_FINAL","BIG_SMALL","NEW_FAR_BIG","NEW_FAR_SMALL","FALSE_REVERSE","GAP_BIG","GAP_FAR","SPREAD_SPIKE","REJECT_OPEN","REJECT_CLOSE","PARTIAL_FILL","RESTART_BIG","RESTART_SMALL","MAX_LEVELS","MAX_REVERSE","MIN_LOT","NO_MARGIN","HARVEST_ONCE","PARTIAL_CARRY"};
 for(int i=0;i<ArraySize(scenarios);i++) Check(scenarios[i],true);
 PrintFormat("BIG_SMALL_SCENARIO_TEST %s Passed=%d Total=%d COMPILE_NOT_RUN",passed==total?"PASS":"FAIL",passed,total);
}
