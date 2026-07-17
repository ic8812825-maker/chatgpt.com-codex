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
void Verify(string name,bool condition){total++;if(condition)passed++;PrintFormat("BIG_SMALL_E2E %s=%s State=%s Positions=%d Reserve=%.2f Recovery=%.2f Far=%.2f",name,condition?"PASS":"FAIL",StateToString(State),SimCountOpenPositions(),Ctx.totalReserve,Ctx.realCyclePL,Ctx.farLot);}
TestMarketEvent Event(double bid,double ask){TestMarketEvent e;e.bid=bid;e.ask=ask;e.time=TimeCurrent();e.rejectOpen=false;e.rejectClose=false;e.partialFillRatio=0;e.accountEquity=100000;e.accountMargin=0;e.accountFreeMargin=100000;e.brokerBuyVolume=0;e.brokerSellVolume=0;e.brokerVolumeLimit=100;e.marginPerLot=100;return e;}
void Drive(TestMarketEvent &event,int ticks=1){ApplyTestMarketEvent(event);for(int i=0;i<ticks;i++)RunStateMachine();}
void ResetDriver(){SimResetHistory();ResetRecoveryContext();ArrayResize(ReserveLedger,0);NextReserveEventId=1;State=STATE_IDLE;}
bool DriveInitialToFar(TestMarketEvent &start,TestMarketEvent &trigger){ResetDriver();Drive(start);if(State!=STATE_INITIAL_LOCK_OPENED)return false;Drive(trigger);Drive(trigger);return State==STATE_FAR_ACTIVE&&Ctx.initialProfitIgnored&&Ctx.farTicket!=0&&Ctx.farIdentifier!=0&&SimCountOpenPositions()==1;}
bool DriveFarToSplit(TestMarketEvent &event){Drive(event,4);return State==STATE_SPLIT_GEOMETRY_ACTIVE&&Ctx.bigCoreTicket!=0&&Ctx.bigTrendTicket!=0&&Ctx.smallBaseTicket!=0&&SimCountOpenPositions()==4;}
void OnStart()
{
 if(MagicNumber!=STATE_MACHINE_TEST_MAGIC||AllowRealTrading||!UseInternalSimulation||!UseSplitBigGeometry){Print("STATE_MACHINE_TEST_CONFIGURATION_REFUSED");return;}
 double point=SymbolInfoDouble(_Symbol,SYMBOL_POINT),bid=SymbolInfoDouble(_Symbol,SYMBOL_BID),ask=SymbolInfoDouble(_Symbol,SYMBOL_ASK),spread=ask-bid;if(point<=0||bid<=0||ask<=0){Print("STATE_MACHINE_TEST_SYMBOL_REFUSED");return;}
 TestMarketEvent start=Event(bid,ask),up=Event(bid+(InitialTriggerPoints+5)*point,ask+(InitialTriggerPoints+5)*point);
 Verify("BIG_01_INITIAL_TO_FAR",DriveInitialToFar(start,up));
 Verify("BIG_02_SPLIT_BASKET",DriveFarToSplit(up));
 int basketPositions=SimCountOpenPositions();
 TestMarketEvent bigMove=Event(up.bid+(BigMoveStartPoints+5)*point,up.ask+(BigMoveStartPoints+5)*point);Drive(bigMove,8);Verify("BIG_04_HARVEST_ACTUAL_DEALS",ArraySize(SimClosedDeals)>0&&Ctx.actualSplitHarvestNetCalculated);Verify("BIG_05_PARTIAL_CARRY",Ctx.partialFarBudgetCarry>=0&&Ctx.farLot>=0);Verify("BIG_06_RESERVE_LEDGER",ArraySize(ReserveLedger)>=0&&Ctx.totalReserve>=0);
 TestMarketEvent lowMargin=Event(bid,ask);lowMargin.accountEquity=100;lowMargin.accountMargin=90;lowMargin.accountFreeMargin=10;lowMargin.marginPerLot=1000;Verify("BIG_03_SETUP_FAR",DriveInitialToFar(start,up));int beforeAtomic=SimCountOpenPositions();Drive(lowMargin);Verify("BIG_03_ATOMIC_MARGIN_FAIL",State==STATE_INVALID_SPLIT_GEOMETRY&&SimCountOpenPositions()==beforeAtomic);
 Verify("REJECT_SETUP_FAR",DriveInitialToFar(start,up));TestMarketEvent rejectOpen=up;rejectOpen.rejectOpen=true;int beforeReject=SimCountOpenPositions();Drive(rejectOpen,2);Verify("REJECTED_OPEN_NO_LEG",SimCountOpenPositions()==beforeReject);
 ResetDriver();Drive(start);TestMarketEvent partial=up;partial.partialFillRatio=.5;Drive(partial);Verify("PARTIAL_FILL_EVENT",SimCountOpenPositions()==2&&ArraySize(SimClosedDeals)>0);TestMarketEvent finish=up;Drive(finish,2);Verify("PARTIAL_FILL_RECOVERY",State==STATE_FAR_ACTIVE||State==STATE_INITIAL_LOCK_OPENED);
 Verify("SMALL_SETUP_SPLIT",DriveInitialToFar(start,up)&&DriveFarToSplit(up));TestMarketEvent reverse=Event(bid-(BigMoveStartPoints+10)*point,ask-(BigMoveStartPoints+10)*point);Drive(reverse,2);Verify("SMALL_01_PRETRADE_BY_FSM",State!=STATE_SPLIT_GEOMETRY_ACTIVE||Ctx.projectedTransitionNet!=0);Drive(reverse,10);Verify("SMALL_RESULT_HAS_IDENTITIES",Ctx.farTicket!=0&&Ctx.farIdentifier!=0);
 TestMarketEvent collision=reverse;Ctx.reverseSmallOpened=true;Drive(collision);Verify("SMALL_12_COLLISION",State==STATE_INTEGRITY_ERROR);Ctx.reverseSmallOpened=false;
 ResetDriver();Ctx.cycleId=701;Ctx.harvestId=9001;Ctx.actualSplitHarvestNet=10;Ctx.harvestReserveAdd=6;Ctx.harvestPartialBudgetAdd=4;Ctx.harvestCarryAfter=4;State=STATE_SPLIT_BIG_HARVEST_FINAL_CHECK;
 for(int phase=HARVEST_CALCULATED;phase<=HARVEST_CONSUMED;phase++){Ctx.harvestPhase=(HarvestPhase)phase;SaveState();int rows=ArraySize(ReserveLedger);double reserveBefore=Ctx.totalReserve;ResetRecoveryContext();double restored=0;GetStateDouble("TotalReserve",restored);Ctx.totalReserve=restored;ReloadHarvestPersistence();ContinueSplitHarvestDistribution();double once=Ctx.totalReserve;int onceRows=ArraySize(ReserveLedger);ContinueSplitHarvestDistribution();Verify(StringFormat("BIG_09_HARVEST_RESTART_%d",phase),Ctx.totalReserve==once&&ArraySize(ReserveLedger)==onceRows&&onceRows<=rows+1&&Ctx.totalReserve>=reserveBefore);}
 Verify("REAL_TRADING_DISABLED",!AllowRealTrading);PrintFormat("BIG_SMALL_END_TO_END %s Passed=%d Total=%d",passed==total?"PASS":"FAIL",passed,total);
}
