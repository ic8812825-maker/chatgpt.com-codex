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

#endif // __BH_LOGGER_MQH__
