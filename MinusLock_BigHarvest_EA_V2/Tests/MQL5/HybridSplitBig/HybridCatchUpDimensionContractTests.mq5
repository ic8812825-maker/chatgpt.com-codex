#property strict
#property script_show_inputs
#include "../../../Include/Config.mqh"
#include "../../../Include/Types.mqh"
#include "../../../Include/LotUtils.mqh"
#include "../../../Include/BrokerMoneyModel.mqh"
#include "../../../Include/HybridRoundingModel.mqh"
#include "../../../Include/HybridCatchUpModel.mqh"
int dimensionPassed=0,dimensionFailed=0;
void DimCheck(string id,bool ok){if(ok){dimensionPassed++;Print("CATCHUP_DIMENSION_TEST|ID=",id,"|PASS");}else{dimensionFailed++;Print("CATCHUP_DIMENSION_TEST|ID=",id,"|FAIL|Expected=PASS|Actual=FAIL");}}
void OnStart()
{
 string symbol=_Symbol;double step=SymbolInfoDouble(symbol,SYMBOL_VOLUME_STEP),point=SymbolInfoDouble(symbol,SYMBOL_POINT),tol=HybridLotTolerance(symbol);
 DimCheck("MQL-DIM-01",HybridLotLess(symbol,0.009,0.01));DimCheck("MQL-DIM-02",!HybridLotEqual(symbol,0.10,0.10-step));DimCheck("MQL-DIM-03",HybridLotEqual(symbol,0.10,0.10+1e-10));DimCheck("MQL-DIM-04",!HybridPriceEqual(symbol,1.10,1.10+point));
 DimCheck("MQL-DIM-05",HybridRatioLess(0.99,1.0));DimCheck("MQL-DIM-06",HybridPercentGreaterOrEqual(200.0-HybridPercentTolerance()/2,200));DimCheck("MQL-DIM-07",HybridPercentLessOrEqual(50.0+HybridPercentTolerance()/2,50));DimCheck("MQL-DIM-08",!HybridLotGreater(symbol,tol/2,0));DimCheck("MQL-DIM-09",HybridLotGreaterOrEqual(symbol,0.05,0.05));
 HybridHarvestLevelResult b,w;ZeroMemory(b);ZeroMemory(w);b.triggerBid=1.10;b.triggerAsk=1.11;w.triggerBid=1.10-point;w.triggerAsk=1.11+point;DimCheck("MQL-DIM-10",HybridWorstCurrentLegsAreAdverse(symbol,b,w));DimCheck("MQL-DIM-11",!HybridLotLessOrEqual(symbol,0.11,0.10));DimCheck("MQL-DIM-12",HybridLotLess(symbol,0.09,0.10));
 HybridCatchUpState state,after;HybridCatchUpProfile profile;HybridHarvestLevelResult row;ZeroMemory(state);ZeroMemory(profile);profile.kind=HYBRID_CATCHUP_BASE;state.symbol=symbol;state.cycleId=1;state.farDirection=DIR_BUY;state.bigDirection=DIR_SELL;state.smallDirection=DIR_BUY;state.farLot=0.10;state.farOpenPrice=1.11;state.coreLot=0.16;state.trendLot=0.03;state.smallLot=0.06;state.coreOpenPrice=1.10;state.trendOpenPrice=1.10;state.smallOpenPrice=1.11;state.anchorBid=1.10;state.anchorAsk=1.11;state.baselineSpread=.01;state.equity=100000;state.currentMargin=100;HybridCatchUpOutcome outcome=EvaluateHybridCatchUpLevel(state,profile,row,after);DimCheck("MQL-DIM-EVALUATOR",outcome!=HYBRID_CATCHUP_OUTCOME_NOT_EVALUATED);
 Print("CATCHUP_DIMENSION_TEST|SUMMARY|Passed=",dimensionPassed,"|Failed=",dimensionFailed);
}
