#ifndef __BH_LOGGER_MQH__
#define __BH_LOGGER_MQH__

void LogInfo(string message)
{
   Print("[BigHarvest] ", message);
}

void LogError(string message)
{
   Print("[BigHarvest][ERROR] ", message);
}

void LogTransition(EAState fromState, EAState toState, string reason)
{
   Print("[BigHarvest][STATE] ", StateToString(fromState), " -> ", StateToString(toState), " | ", reason);
}

void LogFarPosition(RecoveryContext &ctx)
{
   PrintFormat(
      "[BigHarvest][FAR] FarTicket=%I64u FarDirection=%s FarLot=%.2f FarOpenPrice=%.5f FarDistancePoints=%d InitialProfitIgnored=%s ReserveBeforeRecovery=%.2f RecoveryReserveAfterInitialClose=%.2f",
      ctx.farTicket,
      DirectionToString(ctx.farDirection),
      ctx.farLot,
      ctx.farOpenPrice,
      FarDistancePoints,
      ctx.initialProfitIgnored ? "true" : "false",
      0.0,
      ctx.totalReserve
   );
}

void LogHarvestLevel(
   int level,
   ulong farTicket,
   Direction farDirection,
   double farLotBefore,
   double bigLot,
   double smallLot,
   int bigMovePoints,
   double profitBig,
   double lossSmall,
   double netProfit,
   double closeFarBudget,
   double reserveAdd,
   double totalReserve,
   double closeFarLotRaw,
   double closeFarLotRounded,
   double farLotAfter,
   double farRemainLoss,
   bool finalCloseAllowed,
   double finalClosePL,
   bool initialProfitIgnored,
   EAState state
)
{
   PrintFormat(
      "[BigHarvest][LEVEL] Level=%d State=%s FarTicket=%I64u FarDirection=%s FarLotBefore=%.2f " +
      "BigLot=%.2f SmallLot=%.2f BigMovePoints=%d ProfitBig=%.2f LossSmall=%.2f NetProfit=%.2f " +
      "CloseFarBudget=%.2f ReserveAdd=%.2f TotalReserve=%.2f CloseFarLotRaw=%.5f " +
      "CloseFarLotRounded=%.2f FarLotAfter=%.2f FarRemainLoss=%.2f FinalCloseAllowed=%s " +
      "FinalClosePL=%.2f InitialProfitIgnored=%s",
      level,
      StateToString(state),
      farTicket,
      DirectionToString(farDirection),
      farLotBefore,
      bigLot,
      smallLot,
      bigMovePoints,
      profitBig,
      lossSmall,
      netProfit,
      closeFarBudget,
      reserveAdd,
      totalReserve,
      closeFarLotRaw,
      closeFarLotRounded,
      farLotAfter,
      farRemainLoss,
      finalCloseAllowed ? "YES" : "NO",
      finalClosePL,
      initialProfitIgnored ? "true" : "false"
   );
}

void LogSmallScenario(
   int level,
   ulong farTicket,
   Direction farDirection,
   double farLot,
   double smallLot,
   double closeBigLot,
   double remainBigLot,
   int smallMovePoints,
   double profitSmall,
   double lossClosedBig,
   double netSmall,
   bool dualTailDetected,
   EAState state
)
{
   PrintFormat(
      "[BigHarvest][SMALL] Level=%d State=%s FarTicket=%I64u FarDirection=%s FarLot=%.2f " +
      "SmallLot=%.2f CloseSmallLot=%.2f CloseBigLot=%.2f RemainBigLot=%.2f NewFar=%.2f " +
      "SmallMovePoints=%d ProfitSmall=%.2f LossClosedBig=%.2f NetSmall=%.2f " +
      "DualTailDetected=%s",
      level,
      StateToString(state),
      farTicket,
      DirectionToString(farDirection),
      farLot,
      smallLot,
      smallLot,
      closeBigLot,
      remainBigLot,
      remainBigLot,
      smallMovePoints,
      profitSmall,
      lossClosedBig,
      netSmall,
      dualTailDetected ? "true" : "false"
   );
}

void LogWaitSmallToFar(
   Direction smallDirection,
   ulong smallTicket,
   double smallOpenPrice,
   ulong oldFarTicket,
   double oldFarOpenPrice,
   double currentPrice,
   int smallFarTouchOffsetPoints,
   bool farTouchReached
)
{
   PrintFormat(
      "[BigHarvest][SMALL_WAIT] State=STATE_WAIT_SMALL_TO_FAR SmallDirection=%s SmallTicket=%I64u SmallOpenPrice=%.5f OldFarTicket=%I64u OldFarOpenPrice=%.5f CurrentPrice=%.5f SmallFarTouchOffsetPoints=%d FarTouchReached=%s",
      DirectionToString(smallDirection),
      smallTicket,
      smallOpenPrice,
      oldFarTicket,
      oldFarOpenPrice,
      currentPrice,
      smallFarTouchOffsetPoints,
      farTouchReached ? "true" : "false"
   );
}

void LogSmallAtFarTriggered(
   int level,
   double oldFarLot,
   double bigLot,
   double smallLot,
   double smallPL,
   double oldFarPL,
   double closedBigPL,
   double smallScenarioTotalPL,
   double closeBigLotRaw,
   double closeBigLotRounded,
   double remainBigLot,
   double newFarLot,
   Direction newFarDirection,
   double newBigLot,
   double newSmallLot,
   double farRemainLoss,
   double totalReserve,
   bool finalCloseAllowed,
   double cycleFinalPL,
   string actionAfterSmallScenario,
   double reverseStrength,
   string reverseStrengthStatus,
   double smallReverseNet,
   double projectedReserveCoverage,
   bool geometryValid,
   bool smallGeometryValid,
   bool reserveProjectionOk,
   int reverseCycleCount,
   int maxReverseCycles,
   string geometryInvalidReason,
   string smallInvalidReason,
   string riskWarningReason
)
{
   PrintFormat(
      "[BigHarvest][SMALL_AT_FAR_TRIGGERED] Level=%d OldFarLot=%.2f BigLot=%.2f SmallLot=%.2f SmallPL=%.2f OldFarPL=%.2f ClosedBigPL=%.2f SmallScenarioTotalPL=%.2f CloseBigLotRaw=%.5f CloseBigLotRounded=%.2f RemainBigLot=%.2f NewFarLot=%.2f NewFarDirection=%s NewBigLot=%.2f NewSmallLot=%.2f FarRemainLoss=%.2f TotalReserve=%.2f FinalCloseAllowed=%s CycleFinalPL=%.2f ActionAfterSmallScenario=%s ReverseStrength=%.5f ReverseQualityScore=%.5f ReverseStrengthStatus=%s SmallReverseNet=%.2f ProjectedReserveCoverage=%.5f GeometryValid=%s SmallGeometryValid=%s ReserveProjectionOk=%s ReverseCycleCount=%d MaxReverseCycles=%d GeometryInvalidReason=%s SmallInvalidReason=%s RiskWarningReason=%s ActionAfterValidation=%s",
      level,
      oldFarLot,
      bigLot,
      smallLot,
      smallPL,
      oldFarPL,
      closedBigPL,
      smallScenarioTotalPL,
      closeBigLotRaw,
      closeBigLotRounded,
      remainBigLot,
      newFarLot,
      DirectionToString(newFarDirection),
      newBigLot,
      newSmallLot,
      farRemainLoss,
      totalReserve,
      finalCloseAllowed ? "YES" : "NO",
      cycleFinalPL,
      actionAfterSmallScenario,
      reverseStrength,
      reverseStrength,
      reverseStrengthStatus,
      smallReverseNet,
      projectedReserveCoverage,
      geometryValid ? "true" : "false",
      smallGeometryValid ? "true" : "false",
      reserveProjectionOk ? "true" : "false",
      reverseCycleCount,
      maxReverseCycles,
      geometryInvalidReason,
      smallInvalidReason,
      riskWarningReason,
      actionAfterSmallScenario
   );
}


void WriteCycleMathCsv(
   int level,
   string scenario,
   double farLotBefore,
   double bigLot,
   double smallLot,
   double netProfit,
   double closeFarBudget,
   double reserveAdd,
   double totalReserve,
   double farRemainLoss,
   bool finalCloseAllowed,
   EAState state,
   double profitBig,
   double lossSmall,
   double smallPL,
   double oldFarPL,
   double closedBigPL,
   double smallReverseNet,
   double closeFarLotRaw,
   double closeFarLotRounded,
   double farRemainLot,
   double reverseStrength,
   double projectedReserveCoverage,
   string actionAfterValidation,
   string stopReason,
   double netProfitTheoretical,
   double netProfitRealized,
   double costsRealized,
   double totalReserveBefore,
   double reserveUsedForFinalClose
)
{
   if(!EnableCycleMathCsv)
      return;

   int handle = FileOpen("MinusLock_CycleMath.csv", FILE_READ | FILE_WRITE | FILE_CSV | FILE_ANSI, ',');
   if(handle == INVALID_HANDLE)
   {
      Print("[BigHarvest][ERROR] Cannot open MinusLock_CycleMath.csv, error=", GetLastError());
      return;
   }

   if(FileSize(handle) == 0)
   {
      FileWrite(
         handle,
         "Time", "Symbol", "Level", "Scenario", "FarLotBefore", "BigLot", "SmallLot",
         "NetProfit", "CloseFarBudget", "ReserveAdd", "TotalReserve", "FarRemainLoss",
         "FinalCloseAllowed", "State", "Balance", "Equity", "Margin", "FreeMargin",
         "ProfitBig", "LossSmall", "SmallPL", "OldFarPL", "ClosedBigPL", "SmallReverseNet",
         "CloseFarLotRaw", "CloseFarLotRounded", "FarRemainLot", "ReverseStrength",
         "ProjectedReserveCoverage", "ActionAfterValidation", "StopReason",
         "NetProfitTheoretical", "NetProfitRealized", "CostsRealized", "TotalReserveBefore",
         "TotalReserveAfter", "ReserveUsedForFinalClose"
      );
   }

   FileSeek(handle, 0, SEEK_END);
   FileWrite(
      handle,
      TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS),
      _Symbol,
      level,
      scenario,
      DoubleToString(farLotBefore, 2),
      DoubleToString(bigLot, 2),
      DoubleToString(smallLot, 2),
      DoubleToString(netProfit, 2),
      DoubleToString(closeFarBudget, 2),
      DoubleToString(reserveAdd, 2),
      DoubleToString(totalReserve, 2),
      DoubleToString(farRemainLoss, 2),
      finalCloseAllowed ? "YES" : "NO",
      StateToString(state),
      DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2),
      DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY), 2),
      DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN), 2),
      DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_FREE), 2),
      DoubleToString(profitBig, 2),
      DoubleToString(lossSmall, 2),
      DoubleToString(smallPL, 2),
      DoubleToString(oldFarPL, 2),
      DoubleToString(closedBigPL, 2),
      DoubleToString(smallReverseNet, 2),
      DoubleToString(closeFarLotRaw, 5),
      DoubleToString(closeFarLotRounded, 2),
      DoubleToString(farRemainLot, 2),
      DoubleToString(reverseStrength, 5),
      DoubleToString(projectedReserveCoverage, 5),
      actionAfterValidation,
      stopReason,
      DoubleToString(netProfitTheoretical, 2),
      DoubleToString(netProfitRealized, 2),
      DoubleToString(costsRealized, 2),
      DoubleToString(totalReserveBefore, 2),
      DoubleToString(totalReserve, 2),
      DoubleToString(reserveUsedForFinalClose, 2)
   );

   FileClose(handle);
}

void LogCycleMathDetailed(
   int level,
   string scenario,
   double farLotBefore,
   double bigLot,
   double smallLot,
   double netProfit,
   double closeFarBudget,
   double reserveAdd,
   double totalReserve,
   double farRemainLoss,
   bool finalCloseAllowed,
   EAState state,
   double profitBig,
   double lossSmall,
   double smallPL,
   double oldFarPL,
   double closedBigPL,
   double smallReverseNet,
   double closeFarLotRaw,
   double closeFarLotRounded,
   double farRemainLot,
   double reverseStrength,
   double projectedReserveCoverage,
   string actionAfterValidation,
   string stopReason,
   double netProfitTheoretical,
   double netProfitRealized,
   double costsRealized,
   double totalReserveBefore,
   double reserveUsedForFinalClose
)
{
   PrintFormat(
      "CYCLE_MATH | Level=%d Scenario=%s FarLotBefore=%.2f BigLot=%.2f SmallLot=%.2f NetProfit=%.2f CloseFarBudget=%.2f ReserveAdd=%.2f TotalReserve=%.2f FarRemainLoss=%.2f FinalCloseAllowed=%s State=%s ProfitBig=%.2f LossSmall=%.2f SmallPL=%.2f OldFarPL=%.2f ClosedBigPL=%.2f SmallReverseNet=%.2f CloseFarLotRaw=%.5f CloseFarLotRounded=%.2f FarRemainLot=%.2f ReverseStrength=%.5f ProjectedReserveCoverage=%.5f ActionAfterValidation=%s StopReason=%s NetProfitTheoretical=%.2f NetProfitRealized=%.2f CostsRealized=%.2f TotalReserveBefore=%.2f TotalReserveAfter=%.2f ReserveUsedForFinalClose=%.2f",
      level,
      scenario,
      farLotBefore,
      bigLot,
      smallLot,
      netProfit,
      closeFarBudget,
      reserveAdd,
      totalReserve,
      farRemainLoss,
      finalCloseAllowed ? "YES" : "NO",
      StateToString(state),
      profitBig,
      lossSmall,
      smallPL,
      oldFarPL,
      closedBigPL,
      smallReverseNet,
      closeFarLotRaw,
      closeFarLotRounded,
      farRemainLot,
      reverseStrength,
      projectedReserveCoverage,
      actionAfterValidation,
      stopReason,
      netProfitTheoretical,
      netProfitRealized,
      costsRealized,
      totalReserveBefore,
      totalReserve,
      reserveUsedForFinalClose
   );

   WriteCycleMathCsv(
      level,
      scenario,
      farLotBefore,
      bigLot,
      smallLot,
      netProfit,
      closeFarBudget,
      reserveAdd,
      totalReserve,
      farRemainLoss,
      finalCloseAllowed,
      state,
      profitBig,
      lossSmall,
      smallPL,
      oldFarPL,
      closedBigPL,
      smallReverseNet,
      closeFarLotRaw,
      closeFarLotRounded,
      farRemainLot,
      reverseStrength,
      projectedReserveCoverage,
      actionAfterValidation,
      stopReason,
      netProfitTheoretical,
      netProfitRealized,
      costsRealized,
      totalReserveBefore,
      reserveUsedForFinalClose
   );
}

void LogCycleMath(
   int level,
   string scenario,
   double farLotBefore,
   double bigLot,
   double smallLot,
   double netProfit,
   double closeFarBudget,
   double reserveAdd,
   double totalReserve,
   double farRemainLoss,
   bool finalCloseAllowed,
   EAState state
)
{
   LogCycleMathDetailed(
      level,
      scenario,
      farLotBefore,
      bigLot,
      smallLot,
      netProfit,
      closeFarBudget,
      reserveAdd,
      totalReserve,
      farRemainLoss,
      finalCloseAllowed,
      state,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      farLotBefore,
      0.0,
      0.0,
      "BASIC",
      "",
      netProfit,
      netProfit,
      0.0,
      totalReserve - reserveAdd,
      0.0
   );
}

#endif // __BH_LOGGER_MQH__
