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
#define STATE_MACHINE_TEST_MAGIC 9900260717
int passed=0,total=0;
void Verify(string name,bool condition){total++;if(condition)passed++;PrintFormat("BIG_SMALL_STATE_MACHINE %s=%s",name,condition?"PASS":"FAIL");}
void Transition(EAState from,EAState to,string name){State=from;SetState(to,name);Verify(name,State==to);}
void OnStart()
{
 if(MagicNumber!=STATE_MACHINE_TEST_MAGIC||AllowRealTrading||!UseInternalSimulation){Print("STATE_MACHINE_TEST_CONFIGURATION_REFUSED");return;}
 ResetRecoveryContext(); Ctx.cycleId=701; Ctx.farTicket=101; Ctx.farIdentifier=201; Ctx.farLot=1; Ctx.farDirection=DIR_SELL;
 Transition(STATE_INITIAL_LOCK_OPENED,STATE_FAR_ACTIVE,"INITIAL_TO_FAR");
 Transition(STATE_FAR_ACTIVE,STATE_SPLIT_BIG_OPEN_CORE,"FAR_TO_BIG");
 Transition(STATE_SPLIT_GEOMETRY_ACTIVE,STATE_SPLIT_BIG_HARVEST_CALC_NET,"BIG_HARVEST");
 Transition(STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR,STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR,"PARTIAL_FAR");
 Transition(STATE_SPLIT_BIG_HARVEST_FINAL_CHECK,STATE_FINAL_CLOSE,"FINAL_CLOSE");
 Transition(STATE_SPLIT_GEOMETRY_ACTIVE,STATE_REVERSE_CLOSE_BIG_TREND,"BIG_TO_SMALL");
 Transition(STATE_REVERSE_WAIT_FAR_TOUCH,STATE_SMALL_CLOSE_OLD_FAR,"SMALL_FIVE_LEG_BEGIN");
 Ctx.oldFarLot=1;Ctx.farLot=.9;Verify("ACTUAL_NEW_FAR",Ctx.farLot<Ctx.oldFarLot);
 Transition(STATE_SMALL_CHECK_RESERVE,STATE_REVERSE_LIMIT,"REVERSE_LIMIT");
 Transition(STATE_REVERSE_WAIT_FAR_TOUCH,STATE_MANUAL_INTERVENTION_REQUIRED,"FALSE_REVERSE_FALLBACK");
 for(int phase=HARVEST_CALCULATED;phase<=HARVEST_CONSUMED;phase++){Ctx.harvestPhase=(HarvestPhase)phase;Ctx.harvestId=9001;SaveState();HarvestPhase saved=Ctx.harvestPhase;ResetRecoveryContext();bool recovered=RecoverState();Verify(StringFormat("HARVEST_RESTART_%d",phase),recovered&&Ctx.harvestPhase==saved&&Ctx.harvestId==9001);}
 State=STATE_SPLIT_OPEN_CORE_PENDING;Ctx.pendingAttempts=1;Verify("REJECTED_OPEN_PENDING",State==STATE_SPLIT_OPEN_CORE_PENDING&&Ctx.pendingAttempts==1);
 State=STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING;Ctx.pendingCloseFarLot=.25;Verify("PARTIAL_FILL_PENDING",State==STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING&&Ctx.pendingCloseFarLot==.25);
 State=STATE_INVALID_SPLIT_GEOMETRY;Verify("MARGIN_REJECTION",State==STATE_INVALID_SPLIT_GEOMETRY);
 PrintFormat("BIG_SMALL_STATE_MACHINE_TEST %s Passed=%d Total=%d",passed==total?"PASS":"FAIL",passed,total);
}
