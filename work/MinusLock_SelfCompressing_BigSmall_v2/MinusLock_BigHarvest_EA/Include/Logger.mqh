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
   string actionAfterSmallScenario
)
{
   PrintFormat(
      "[BigHarvest][SMALL_AT_FAR_TRIGGERED] Level=%d OldFarLot=%.2f BigLot=%.2f SmallLot=%.2f SmallPL=%.2f OldFarPL=%.2f ClosedBigPL=%.2f SmallScenarioTotalPL=%.2f CloseBigLotRaw=%.5f CloseBigLotRounded=%.2f RemainBigLot=%.2f NewFarLot=%.2f NewFarDirection=%s NewBigLot=%.2f NewSmallLot=%.2f FarRemainLoss=%.2f TotalReserve=%.2f FinalCloseAllowed=%s CycleFinalPL=%.2f ActionAfterSmallScenario=%s",
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
      actionAfterSmallScenario
   );
}

#endif // __BH_LOGGER_MQH__
