#ifndef __BH_STATEMACHINE_MQH__
#define __BH_STATEMACHINE_MQH__

EAState State = STATE_IDLE;
RecoveryContext Ctx;

void SetState(EAState nextState, string reason)
{
   if(State != nextState)
      LogTransition(State, nextState, reason);

   State = nextState;
}

void ResetRecoveryContext()
{
   Ctx.farTicket = 0;
   Ctx.bigTicket = 0;
   Ctx.smallTicket = 0;

   Ctx.farLot = 0.0;
   Ctx.bigLot = 0.0;
   Ctx.smallLot = 0.0;

   Ctx.farOpenPrice = 0.0;
   Ctx.bigOpenPrice = 0.0;
   Ctx.smallOpenPrice = 0.0;

   Ctx.farDirection = DIR_NONE;
   Ctx.bigDirection = DIR_NONE;
   Ctx.smallDirection = DIR_NONE;

   Ctx.harvestLevel = 0;
   Ctx.totalReserve = 0.0;
   Ctx.cycleFinalPL = 0.0;

   Ctx.initialProfitIgnored = false;
   Ctx.finalCloseAllowed = false;
   Ctx.dualTailDetected = false;

   Ctx.reverseCycleCount = 0;
   Ctx.oldFarLotBeforeReverse = 0.0;
   Ctx.newFarLotAfterReverse = 0.0;
   Ctx.newBigLotAfterReverse = 0.0;
   Ctx.newSmallLotAfterReverse = 0.0;
   Ctx.reverseStrength = 0.0;
   Ctx.reverseQualityScore = 0.0;
   Ctx.projectedReserveCoverage = 0.0;
   Ctx.smallReverseNet = 0.0;
   Ctx.geometryValid = true;
   Ctx.reverseLimitReached = false;
   Ctx.reserveProjectionOk = true;
   Ctx.smallGeometryValid = true;
}

void UpdateFarFromSnapshot(PositionSnapshot &far)
{
   Ctx.farTicket = far.ticket;
   Ctx.farLot = NormalizeLotDown(far.lot);
   Ctx.farOpenPrice = far.openPrice;
   Ctx.farDirection = far.direction;
}

bool RefreshFar()
{
   PositionSnapshot far;

   if(GetManagedPositionByTicket(Ctx.farTicket, far))
   {
      UpdateFarFromSnapshot(far);
      return true;
   }

   if(!AllowRealTrading && Ctx.farLot > 0.0 && Ctx.farDirection != DIR_NONE)
      return true;

   return false;
}

bool RefreshBigSmall(PositionSnapshot &big, PositionSnapshot &small)
{
   bool bigFound = GetManagedPositionByTicket(Ctx.bigTicket, big);
   bool smallFound = GetManagedPositionByTicket(Ctx.smallTicket, small);

   if(bigFound && smallFound)
      return true;

   string bigComment = LevelComment("BIG", Ctx.harvestLevel);
   string smallComment = LevelComment("SMALL", Ctx.harvestLevel);

   bigFound = GetManagedPositionByComment(bigComment, big);
   smallFound = GetManagedPositionByComment(smallComment, small);

   if(bigFound)
   {
      Ctx.bigTicket = big.ticket;
      Ctx.bigLot = big.lot;
      Ctx.bigOpenPrice = big.openPrice;
      Ctx.bigDirection = big.direction;
   }

   if(smallFound)
   {
      Ctx.smallTicket = small.ticket;
      Ctx.smallLot = small.lot;
      Ctx.smallOpenPrice = small.openPrice;
      Ctx.smallDirection = small.direction;
   }

   if(!AllowRealTrading && Ctx.bigLot > 0.0 && Ctx.smallLot > 0.0)
   {
      big.exists = true;
      big.ticket = Ctx.bigTicket;
      big.direction = Ctx.bigDirection;
      big.lot = Ctx.bigLot;
      big.openPrice = Ctx.bigOpenPrice;
      big.comment = bigComment;

      small.exists = true;
      small.ticket = Ctx.smallTicket;
      small.direction = Ctx.smallDirection;
      small.lot = Ctx.smallLot;
      small.openPrice = Ctx.smallOpenPrice;
      small.comment = smallComment;
      return true;
   }

   return bigFound && smallFound;
}

void OpenInitialLock()
{
   PositionSnapshot initialBuy;
   PositionSnapshot initialSell;

   bool hasBuy = GetInitialBuy(initialBuy);
   bool hasSell = GetInitialSell(initialSell);

   if(hasBuy && hasSell)
   {
      SetState(STATE_INITIAL_LOCK_OPENED, "existing initial BUY/SELL lock found");
      return;
   }

   if(CountManagedOpenPositions() > 0)
   {
      LogError("Managed positions already exist but the initial lock is incomplete");
      SetState(STATE_ERROR, "incomplete managed position set before initial lock");
      return;
   }

   double lot = NormalizeLotNearest(StartLot);
   if(lot <= 0.0)
   {
      LogError("StartLot normalized to zero");
      SetState(STATE_ERROR, "invalid StartLot");
      return;
   }

   bool buyOpened = OpenPosition(DIR_BUY, lot, "MinusLock_INITIAL_BUY");
   bool sellOpened = OpenPosition(DIR_SELL, lot, "MinusLock_INITIAL_SELL");

   if(!buyOpened || !sellOpened)
   {
      LogError("Failed to open initial BUY/SELL lock");
      SetState(STATE_ERROR, "initial lock open failed");
      return;
   }

   LogInfo(StringFormat("Initial lock requested: BUY %.2f and SELL %.2f. First plus will be ignored.", lot, lot));
   SetState(STATE_INITIAL_LOCK_OPENED, "initial lock opened");
}

void CheckInitialPlusClose()
{
   PositionSnapshot initialBuy;
   PositionSnapshot initialSell;

   bool hasBuy = GetInitialBuy(initialBuy);
   bool hasSell = GetInitialSell(initialSell);

   if(!hasBuy || !hasSell)
   {
      LogError("Initial lock positions not found while waiting for first plus");
      SetState(STATE_ERROR, "initial lock disappeared");
      return;
   }

   double buyProfitPoints = ProfitPoints(initialBuy.direction, initialBuy.openPrice);
   double sellProfitPoints = ProfitPoints(initialSell.direction, initialSell.openPrice);

   if(buyProfitPoints >= InitialTriggerPoints)
   {
      if(!ClosePositionByTicket(initialBuy.ticket, initialBuy.lot))
      {
         SetState(STATE_ERROR, "failed to close initial profitable BUY");
         return;
      }

      UpdateFarFromSnapshot(initialSell);
      Ctx.initialProfitIgnored = true;
      Ctx.totalReserve = 0.0;
      Ctx.cycleFinalPL = 0.0;

      LogInfo(StringFormat("CLOSE INITIAL PROFIT POSITION direction=BUY InitialProfit=%.2f InitialProfitIgnored=%s ReserveBeforeRecovery=%.2f RecoveryReserveAfterInitialClose=%.2f", initialBuy.profitMoney, Ctx.initialProfitIgnored ? "true" : "false", 0.0, Ctx.totalReserve));
      LogInfo(StringFormat("Initial BUY plus closed at %.1f points and ignored. Far is SELL %.2f", buyProfitPoints, Ctx.farLot));
      LogFarPosition(Ctx);
      SetState(STATE_FAR_ACTIVE, "initial plus ignored, remaining SELL is Far");
      return;
   }

   if(sellProfitPoints >= InitialTriggerPoints)
   {
      if(!ClosePositionByTicket(initialSell.ticket, initialSell.lot))
      {
         SetState(STATE_ERROR, "failed to close initial profitable SELL");
         return;
      }

      UpdateFarFromSnapshot(initialBuy);
      Ctx.initialProfitIgnored = true;
      Ctx.totalReserve = 0.0;
      Ctx.cycleFinalPL = 0.0;

      LogInfo(StringFormat("CLOSE INITIAL PROFIT POSITION direction=SELL InitialProfit=%.2f InitialProfitIgnored=%s ReserveBeforeRecovery=%.2f RecoveryReserveAfterInitialClose=%.2f", initialSell.profitMoney, Ctx.initialProfitIgnored ? "true" : "false", 0.0, Ctx.totalReserve));
      LogInfo(StringFormat("Initial SELL plus closed at %.1f points and ignored. Far is BUY %.2f", sellProfitPoints, Ctx.farLot));
      LogFarPosition(Ctx);
      SetState(STATE_FAR_ACTIVE, "initial plus ignored, remaining BUY is Far");
      return;
   }
}

void OpenBigSmall()
{
   if(!Ctx.initialProfitIgnored)
   {
      LogError("Recovery attempted before InitialProfitIgnored=true");
      SetState(STATE_ERROR, "initial plus was not ignored");
      return;
   }

   if(!RefreshFar())
   {
      LogError("Far position not found");
      SetState(STATE_ERROR, "missing Far");
      return;
   }

   if(Ctx.harvestLevel >= MaxHarvestLevels)
   {
      SetState(STATE_STOP, "MaxHarvestLevels reached before FinalCloseAllowed");
      return;
   }

   Ctx.harvestLevel++;
   Ctx.bigDirection = OppositeDirection(Ctx.farDirection);
   Ctx.smallDirection = Ctx.farDirection;
   Ctx.bigLot = CalcBigLot(Ctx.farLot);
   Ctx.smallLot = CalcSmallLot(Ctx.bigLot);

   if(Ctx.bigLot <= 0.0 || Ctx.smallLot <= 0.0)
   {
      LogError("Big/Small lot normalized to zero");
      SetState(STATE_ERROR, "invalid Big/Small lot");
      return;
   }

   string bigComment = LevelComment("BIG", Ctx.harvestLevel);
   string smallComment = LevelComment("SMALL", Ctx.harvestLevel);

   bool bigOpened = OpenPosition(Ctx.bigDirection, Ctx.bigLot, bigComment);
   bool smallOpened = OpenPosition(Ctx.smallDirection, Ctx.smallLot, smallComment);

   if(!bigOpened || !smallOpened)
   {
      SetState(STATE_ERROR, "failed to open Big/Small pair");
      return;
   }

   PositionSnapshot big;
   PositionSnapshot small;

   if(GetManagedPositionByComment(bigComment, big))
   {
      Ctx.bigTicket = big.ticket;
      Ctx.bigOpenPrice = big.openPrice;
   }
   else
   {
      Ctx.bigTicket = 0;
      Ctx.bigOpenPrice = EntryPriceForDirection(Ctx.bigDirection);
   }

   if(GetManagedPositionByComment(smallComment, small))
   {
      Ctx.smallTicket = small.ticket;
      Ctx.smallOpenPrice = small.openPrice;
   }
   else
   {
      Ctx.smallTicket = 0;
      Ctx.smallOpenPrice = EntryPriceForDirection(Ctx.smallDirection);
   }

   LogInfo(StringFormat(
      "OPEN BIG/SMALL Level=%d FarTicket=%I64u FarDirection=%s FarLot=%.2f BigDirection=%s BigLot=%.2f SmallDirection=%s SmallLot=%.2f Target=%d",
      Ctx.harvestLevel,
      Ctx.farTicket,
      DirectionToString(Ctx.farDirection),
      Ctx.farLot,
      DirectionToString(Ctx.bigDirection),
      Ctx.bigLot,
      DirectionToString(Ctx.smallDirection),
      Ctx.smallLot,
      GetBigMovePoints(Ctx.harvestLevel)
   ));

   SetState(STATE_BIG_SMALL_OPENED, "Big/Small pair opened from Far");
}

void CheckBigOrSmallScenario()
{
   PositionSnapshot big;
   PositionSnapshot small;

   if(!RefreshBigSmall(big, small))
   {
      LogError("Big/Small pair not found");
      SetState(STATE_ERROR, "missing Big/Small pair");
      return;
   }

   int targetPoints = GetBigMovePoints(Ctx.harvestLevel);
   double bigProfitPoints = ProfitPoints(Ctx.bigDirection, Ctx.bigOpenPrice);
   double smallProfitPoints = ProfitPoints(Ctx.smallDirection, Ctx.smallOpenPrice);

   if(bigProfitPoints >= targetPoints)
   {
      SetState(STATE_BIG_HARVEST, "Big reached target movement");
      return;
   }

   if(smallProfitPoints >= targetPoints)
   {
      SetState(STATE_WAIT_SMALL_TO_FAR, "Small direction detected. Waiting for price to reach old Far open price.");
      return;
   }
}

void ProcessBigHarvest()
{
   PositionSnapshot big;
   PositionSnapshot small;

   if(!RefreshFar() || !RefreshBigSmall(big, small))
   {
      SetState(STATE_ERROR, "cannot process Big-harvest without Far/Big/Small");
      return;
   }

   double farStartLot = Ctx.farLot;
   int bigMovePoints = GetBigMovePoints(Ctx.harvestLevel);
   double profitBig = CalcProfit(Ctx.bigLot, bigMovePoints);
   double lossSmall = CalcProfit(Ctx.smallLot, bigMovePoints);
   double costs = 0.0;
   double netProfit = profitBig - lossSmall - costs;
   double closeFarBudget = CalcCloseFarBudget(netProfit);
   double reserveAdd = CalcReserveAdd(netProfit);
   double closeFarLotRaw = CalcCloseFarLotRaw(closeFarBudget, FarDistancePoints);
   double closeFarLotRounded = CalcCloseFarLotRounded(closeFarLotRaw, Ctx.farLot);
   double closeFarLotFinal = closeFarLotRounded;

   if(!ClosePositionByTicket(Ctx.bigTicket, Ctx.bigLot))
   {
      SetState(STATE_ERROR, "failed to close Big 100% in Big-harvest");
      return;
   }

   if(!ClosePositionByTicket(Ctx.smallTicket, Ctx.smallLot))
   {
      SetState(STATE_ERROR, "failed to close Small 100% in Big-harvest");
      return;
   }

   if(closeFarLotFinal > 0.0)
   {
      if(!ClosePositionByTicket(Ctx.farTicket, closeFarLotFinal))
      {
         SetState(STATE_ERROR, "failed to close Far by money budget");
         return;
      }
   }

   Ctx.totalReserve += reserveAdd;
   Ctx.farLot = NormalizeLotDown(MathMax(0.0, Ctx.farLot - closeFarLotFinal));
   Ctx.finalCloseAllowed = CalcFinalCloseAllowed(Ctx.totalReserve, Ctx.farLot, FarDistancePoints);
   Ctx.cycleFinalPL = Ctx.totalReserve - CalcFarRemainLoss(Ctx.farLot, FarDistancePoints);

   double farRemainLoss = CalcFarRemainLoss(Ctx.farLot, FarDistancePoints);

   LogHarvestLevel(
      Ctx.harvestLevel,
      Ctx.farTicket,
      Ctx.farDirection,
      farStartLot,
      Ctx.bigLot,
      Ctx.smallLot,
      bigMovePoints,
      profitBig,
      lossSmall,
      netProfit,
      closeFarBudget,
      reserveAdd,
      Ctx.totalReserve,
      closeFarLotRaw,
      closeFarLotRounded,
      Ctx.farLot,
      farRemainLoss,
      Ctx.finalCloseAllowed,
      Ctx.cycleFinalPL,
      Ctx.initialProfitIgnored,
      STATE_BIG_HARVEST
   );

   Ctx.bigTicket = 0;
   Ctx.smallTicket = 0;
   Ctx.bigLot = 0.0;
   Ctx.smallLot = 0.0;

   if(Ctx.farLot <= 0.0)
   {
      SetState(STATE_CLOSED_PROFIT, "Far was fully closed by Big-harvest budget");
      return;
   }

   if(Ctx.finalCloseAllowed)
   {
      SetState(STATE_FINAL_CLOSE, "TotalReserve covers remaining Far loss");
      return;
   }

   if(Ctx.harvestLevel >= MaxHarvestLevels)
   {
      SetState(STATE_STOP, "MaxHarvestLevels reached without final close");
      return;
   }

   SetState(STATE_FAR_ACTIVE, "Repeat Harvest from reduced Far");
}

double CurrentPriceForSmallTouch(Direction smallDirection)
{
   return ExitPriceForDirection(smallDirection);
}

bool FarTouchReachedForSmall(Direction smallDirection, double oldFarOpenPrice, double currentPrice)
{
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double offset = SmallFarTouchOffsetPoints * point;

   if(point <= 0.0 || oldFarOpenPrice <= 0.0 || currentPrice <= 0.0)
      return false;

   if(smallDirection == DIR_BUY)
      return currentPrice >= oldFarOpenPrice + offset;

   if(smallDirection == DIR_SELL)
      return currentPrice <= oldFarOpenPrice - offset;

   return false;
}

void CheckSmallToFarTouch()
{
   PositionSnapshot big;
   PositionSnapshot small;

   if(!RefreshFar() || !RefreshBigSmall(big, small))
   {
      SetState(STATE_ERROR, "cannot wait Small-to-Far without Far/Big/Small");
      return;
   }

   double currentPrice = CurrentPriceForSmallTouch(Ctx.smallDirection);
   bool farTouchReached = FarTouchReachedForSmall(Ctx.smallDirection, Ctx.farOpenPrice, currentPrice);

   LogWaitSmallToFar(
      Ctx.smallDirection,
      Ctx.smallTicket,
      Ctx.smallOpenPrice,
      Ctx.farTicket,
      Ctx.farOpenPrice,
      currentPrice,
      SmallFarTouchOffsetPoints,
      farTouchReached
   );

   if(!farTouchReached)
      return;

   SetState(STATE_SMALL_SCENARIO, "SMALL_AT_FAR_TRIGGERED");
   ProcessSmallAtFarTouch();
}

void ProcessSmallAtFarTouch()
{
   PositionSnapshot big;
   PositionSnapshot small;

   if(!RefreshFar() || !RefreshBigSmall(big, small))
   {
      SetState(STATE_ERROR, "cannot process Small-at-Far without Far/Big/Small");
      return;
   }

   double oldFarLot = Ctx.farLot;
   double oldFarOpenPrice = Ctx.farOpenPrice;
   ulong oldFarTicket = Ctx.farTicket;
   Direction oldFarDirection = Ctx.farDirection;

   double bigLot = Ctx.bigLot;
   double bigOpenPrice = Ctx.bigOpenPrice;
   ulong bigTicket = Ctx.bigTicket;
   Direction bigDirection = Ctx.bigDirection;

   double smallLot = Ctx.smallLot;
   double smallOpenPrice = Ctx.smallOpenPrice;
   ulong smallTicket = Ctx.smallTicket;
   Direction smallDirection = Ctx.smallDirection;

   double currentPrice = CurrentPriceForSmallTouch(smallDirection);
   double smallMovePoints = CalcMovePointsBetween(smallOpenPrice, currentPrice);
   double smallPL = CalcSignedPositionPL(smallDirection, smallLot, smallOpenPrice, currentPrice);
   double oldFarPL = CalcSignedPositionPL(oldFarDirection, oldFarLot, oldFarOpenPrice, currentPrice);
   double closeBigLotRaw = bigLot * CloseBigOnSmall;
   double closeBigLotRounded = NormalizeLotDown(closeBigLotRaw);
   double remainBigLot = NormalizeLotDown(MathMax(0.0, bigLot - closeBigLotRounded));
   double closedBigPL = CalcSignedPositionPL(bigDirection, closeBigLotRounded, bigOpenPrice, currentPrice);
   double costs = 0.0;
   double smallScenarioTotalPL = smallPL + oldFarPL + closedBigPL - costs;

   double newFarLot = remainBigLot;
   Direction newFarDirection = bigDirection;
   double newBigLot = CalcBigLot(newFarLot);
   double newSmallLot = CalcSmallLot(newBigLot);
   double expectedNextReserve = CalcExpectedNextReserve(newBigLot, newSmallLot, Ctx.harvestLevel + 1);
   double expectedNextFarLoss = CalcFarRemainLoss(newFarLot, FarDistancePoints);
   double projectedReserveCoverage = 0.0;
   double reverseStrength = 0.0;
   double smallReverseNet = 0.0;
   string geometryInvalidReason = "OK";
   string smallInvalidReason = "OK";
   string riskWarningReason = "OK";
   string actionAfterValidation = "OPEN_NEW_BIG_SMALL";

   bool geometryValid = ValidateReverseGeometry(oldFarLot, newFarLot, newBigLot, newSmallLot, reverseStrength, geometryInvalidReason);
   bool smallGeometryValid = ValidateSmallGeometry(smallPL, oldFarPL, closedBigPL, smallReverseNet, smallInvalidReason);
   bool reserveProjectionOk = ValidateReverseRisk(Ctx.totalReserve, expectedNextReserve, expectedNextFarLoss, projectedReserveCoverage, riskWarningReason);

   Ctx.oldFarLotBeforeReverse = oldFarLot;
   Ctx.newFarLotAfterReverse = newFarLot;
   Ctx.newBigLotAfterReverse = newBigLot;
   Ctx.newSmallLotAfterReverse = newSmallLot;
   Ctx.reverseStrength = reverseStrength;
   Ctx.reverseQualityScore = reverseStrength;
   Ctx.projectedReserveCoverage = projectedReserveCoverage;
   Ctx.smallReverseNet = smallReverseNet;
   Ctx.geometryValid = geometryValid;
   Ctx.smallGeometryValid = smallGeometryValid;
   Ctx.reserveProjectionOk = reserveProjectionOk;

   if(!geometryValid && StopOnInvalidReverseGeometry)
      actionAfterValidation = "STOP_INVALID_REVERSE_GEOMETRY";
   else if(!smallGeometryValid && !AllowNegativeSmallReverseNet)
      actionAfterValidation = "STOP_INVALID_SMALL_GEOMETRY";
   else if(!reserveProjectionOk)
      actionAfterValidation = "REVERSE_WARNING_CONTINUE";

   if(!geometryValid && StopOnInvalidReverseGeometry)
   {
      LogInfo(StringFormat("SMALL_AT_FAR_TRIGGERED SmallMovePoints=%.1f CurrentPrice=%.5f", smallMovePoints, currentPrice));
      LogSmallAtFarTriggered(
         Ctx.harvestLevel, oldFarLot, bigLot, smallLot, smallPL, oldFarPL, closedBigPL,
         smallScenarioTotalPL, closeBigLotRaw, closeBigLotRounded, remainBigLot, newFarLot,
         newFarDirection, newBigLot, newSmallLot, expectedNextFarLoss, Ctx.totalReserve,
         false, Ctx.totalReserve - expectedNextFarLoss, actionAfterValidation, reverseStrength,
         ReverseStrengthStatus(reverseStrength), smallReverseNet, projectedReserveCoverage,
         geometryValid, smallGeometryValid, reserveProjectionOk, Ctx.reverseCycleCount,
         MaxReverseCycles, geometryInvalidReason, smallInvalidReason, riskWarningReason
      );
      SetState(STATE_INVALID_REVERSE_GEOMETRY, geometryInvalidReason);
      return;
   }

   if(!smallGeometryValid && !AllowNegativeSmallReverseNet)
   {
      LogInfo(StringFormat("SMALL_AT_FAR_TRIGGERED SmallMovePoints=%.1f CurrentPrice=%.5f", smallMovePoints, currentPrice));
      LogSmallAtFarTriggered(
         Ctx.harvestLevel, oldFarLot, bigLot, smallLot, smallPL, oldFarPL, closedBigPL,
         smallScenarioTotalPL, closeBigLotRaw, closeBigLotRounded, remainBigLot, newFarLot,
         newFarDirection, newBigLot, newSmallLot, expectedNextFarLoss, Ctx.totalReserve,
         false, Ctx.totalReserve - expectedNextFarLoss, actionAfterValidation, reverseStrength,
         ReverseStrengthStatus(reverseStrength), smallReverseNet, projectedReserveCoverage,
         geometryValid, smallGeometryValid, reserveProjectionOk, Ctx.reverseCycleCount,
         MaxReverseCycles, geometryInvalidReason, smallInvalidReason, riskWarningReason
      );
      SetState(STATE_INVALID_SMALL_GEOMETRY, smallInvalidReason);
      return;
   }

   if(!ClosePositionByTicket(smallTicket, smallLot))
   {
      SetState(STATE_ERROR, "failed to close Small 100% at old Far touch");
      return;
   }

   if(!ClosePositionByTicket(oldFarTicket, oldFarLot))
   {
      SetState(STATE_ERROR, "failed to close old Far 100% at Small-at-Far");
      return;
   }

   if(closeBigLotRounded > 0.0)
   {
      if(!ClosePositionByTicket(bigTicket, closeBigLotRounded))
      {
         SetState(STATE_ERROR, "failed to close Big by CloseBigOnSmall at Small-at-Far");
         return;
      }
   }

   Ctx.reverseCycleCount += 1;
   Ctx.reverseLimitReached = Ctx.reverseCycleCount > MaxReverseCycles;
   if(Ctx.reverseLimitReached && StopOnReverseLimit)
      actionAfterValidation = "STOP_REVERSE_LIMIT";

   Ctx.farTicket = bigTicket;
   Ctx.farLot = newFarLot;
   Ctx.farOpenPrice = bigOpenPrice;
   Ctx.farDirection = newFarDirection;
   Ctx.bigTicket = 0;
   Ctx.smallTicket = 0;
   Ctx.bigLot = 0.0;
   Ctx.smallLot = 0.0;
   Ctx.bigOpenPrice = 0.0;
   Ctx.smallOpenPrice = 0.0;
   Ctx.bigDirection = DIR_NONE;
   Ctx.smallDirection = DIR_NONE;
   Ctx.dualTailDetected = false;

   double farRemainLoss = CalcFarRemainLoss(Ctx.farLot, FarDistancePoints);
   Ctx.finalCloseAllowed = CalcFinalCloseAllowed(Ctx.totalReserve, Ctx.farLot, FarDistancePoints);
   Ctx.cycleFinalPL = Ctx.totalReserve - farRemainLoss;

   if(Ctx.finalCloseAllowed)
      actionAfterValidation = "FINAL_CLOSE_NEW_FAR";
   else if(Ctx.reverseLimitReached && StopOnReverseLimit)
      actionAfterValidation = "STOP_REVERSE_LIMIT";
   else if(!reserveProjectionOk)
      actionAfterValidation = "REVERSE_WARNING_OPEN_NEW_BIG_SMALL";
   else if(!smallGeometryValid && AllowNegativeSmallReverseNet)
      actionAfterValidation = "SMALL_GEOMETRY_WARNING_OPEN_NEW_BIG_SMALL";
   else
      actionAfterValidation = "OPEN_NEW_BIG_SMALL";

   LogInfo(StringFormat("SMALL_AT_FAR_TRIGGERED SmallMovePoints=%.1f CurrentPrice=%.5f", smallMovePoints, currentPrice));
   LogSmallAtFarTriggered(
      Ctx.harvestLevel, oldFarLot, bigLot, smallLot, smallPL, oldFarPL, closedBigPL,
      smallScenarioTotalPL, closeBigLotRaw, closeBigLotRounded, remainBigLot, Ctx.farLot,
      Ctx.farDirection, newBigLot, newSmallLot, farRemainLoss, Ctx.totalReserve,
      Ctx.finalCloseAllowed, Ctx.cycleFinalPL, actionAfterValidation, reverseStrength,
      ReverseStrengthStatus(reverseStrength), smallReverseNet, projectedReserveCoverage,
      geometryValid, smallGeometryValid, reserveProjectionOk, Ctx.reverseCycleCount,
      MaxReverseCycles, geometryInvalidReason, smallInvalidReason, riskWarningReason
   );

   if(Ctx.reverseLimitReached && StopOnReverseLimit)
   {
      SetState(STATE_REVERSE_LIMIT, "reverseCycleCount > MaxReverseCycles");
      return;
   }

   if(Ctx.farLot <= 0.0)
   {
      SetState(STATE_CLOSED_PROFIT, "Small-at-Far left no NewFar lot");
      return;
   }

   if(Ctx.finalCloseAllowed)
   {
      if(!ClosePositionByTicket(Ctx.farTicket, Ctx.farLot))
      {
         SetState(STATE_ERROR, "failed to close NewFar after Small-at-Far FinalCloseAllowed");
         return;
      }

      Ctx.farTicket = 0;
      Ctx.farLot = 0.0;
      SetState(STATE_CLOSED_PROFIT, "FinalCloseAllowed after Small-at-Far; NewFar closed and no new Big/Small opened");
      return;
   }

   if(!reserveProjectionOk || (!smallGeometryValid && AllowNegativeSmallReverseNet))
      SetState(STATE_REVERSE_WARNING, "reverse validation warning logged; continuing with protected rebuild");

   SetState(STATE_FAR_ACTIVE, "Small-at-Far validation passed: old Far closed, remaining Big became NewFar");
}

void ProcessSmallScenario()
{
   ProcessSmallAtFarTouch();
}

void ProcessFinalClose()
{
   if(!RefreshFar())
   {
      SetState(STATE_CLOSED_PROFIT, "Far already absent at final close");
      return;
   }

   double farRemainLoss = CalcFarRemainLoss(Ctx.farLot, FarDistancePoints);
   Ctx.cycleFinalPL = Ctx.totalReserve - farRemainLoss;

   if(!ClosePositionByTicket(Ctx.farTicket, Ctx.farLot))
   {
      SetState(STATE_ERROR, "failed to close Far during FinalClose");
      return;
   }

   LogInfo(StringFormat(
      "FinalClose completed: FarRemainLoss=%.2f TotalReserve=%.2f CycleFinalPL=%.2f",
      farRemainLoss,
      Ctx.totalReserve,
      Ctx.cycleFinalPL
   ));

   Ctx.farTicket = 0;
   Ctx.farLot = 0.0;
   SetState(STATE_CLOSED_PROFIT, "cycle closed in profit; no new levels");
}

void RunStateMachine()
{
   switch(State)
   {
      case STATE_IDLE:
         OpenInitialLock();
         break;

      case STATE_INITIAL_LOCK_OPENED:
         CheckInitialPlusClose();
         break;

      case STATE_INITIAL_PLUS_CLOSED:
         SetState(STATE_FAR_ACTIVE, "compatibility transition to Far active");
         break;

      case STATE_FAR_ACTIVE:
         OpenBigSmall();
         break;

      case STATE_BIG_SMALL_OPENED:
         CheckBigOrSmallScenario();
         break;

      case STATE_BIG_HARVEST:
         ProcessBigHarvest();
         break;

      case STATE_WAIT_SMALL_TO_FAR:
         CheckSmallToFarTouch();
         break;

      case STATE_SMALL_SCENARIO:
         ProcessSmallScenario();
         break;

      case STATE_FINAL_CLOSE:
         ProcessFinalClose();
         break;

      case STATE_CLOSED_PROFIT:
      case STATE_DUAL_TAIL:
      case STATE_INVALID_REVERSE_GEOMETRY:
      case STATE_INVALID_SMALL_GEOMETRY:
      case STATE_REVERSE_LIMIT:
      case STATE_STOP:
      case STATE_ERROR:
         break;

      default:
         SetState(STATE_ERROR, "unknown state");
         break;
   }
}

#endif // __BH_STATEMACHINE_MQH__
