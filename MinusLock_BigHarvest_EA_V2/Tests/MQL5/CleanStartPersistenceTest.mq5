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
#include "../../Include/RecoveryMath.mqh"
#include "../../Include/BrokerMoneyModel.mqh"
#include "../../Include/RiskManager.mqh"
#include "../../Include/PendingContractEngine.mqh"
#include "../../Include/StateMachine.mqh"

#define CLEAN_START_TEST_MAGIC 9900260716
string CreatedKeys[];
void Put(string suffix,double value){string key=StateKey(suffix); GlobalVariableSet(key,value); int n=ArraySize(CreatedKeys); ArrayResize(CreatedKeys,n+1); CreatedKeys[n]=key;}
void Cleanup(){for(int i=0;i<ArraySize(CreatedKeys);i++) GlobalVariableDel(CreatedKeys[i]); ArrayResize(CreatedKeys,0);}
bool Expect(string name,bool value){Print("CLEAN_START_TEST ",name,"=",value?"PASS":"FAIL"); return value;}
void OnStart()
{
 if(MagicNumber!=CLEAN_START_TEST_MAGIC||AllowRealTrading){Print("COMPILE_NOT_RUN TEST_CONFIGURATION_REFUSED"); return;}
 int passed=0,total=0; PersistedUInt64Inspection x;
 Cleanup(); Put("HarnessZeroHigh32",0); Put("HarnessZeroLow32",0); InspectPersistedUInt64("HarnessZero",x); total++; if(Expect("UINT64_ZERO",x.state==PERSISTED_UINT64_ZERO))passed++;
 Cleanup(); Put("HarnessMalformedHigh32",1); InspectPersistedUInt64("HarnessMalformed",x); total++; if(Expect("UINT64_MALFORMED",x.state==PERSISTED_UINT64_MALFORMED))passed++;
 Cleanup(); CleanStartEvaluation clean; EvaluateCleanStart(clean); total++; if(Expect("FULLY_CLEAN",clean.cleanStartAllowed))passed++;
 Cleanup(); PrintFormat("CLEAN_START_PERSISTENCE_TEST %s Passed=%d Total=%d COMPILE_NOT_RUN",passed==total?"PASS":"FAIL",passed,total);
}
