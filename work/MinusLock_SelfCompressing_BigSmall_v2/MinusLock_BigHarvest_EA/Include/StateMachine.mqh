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
      SetState(STATE_SMALL_SCENARIO, "Small reached protective movement");
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

void ProcessSmallScenario()
{
   PositionSnapshot big;
   PositionSnapshot small;

   if(!RefreshFar() || !RefreshBigSmall(big, small))
   {
      SetState(STATE_ERROR, "cannot process Small-scenario without Far/Big/Small");
      return;
   }

   int smallMovePoints = GetBigMovePoints(Ctx.harvestLevel);
   double closeBigLot = CalcCloseBigLotOnSmall(Ctx.bigLot);
   double remainBigLot = CalcRemainBigLotOnSmall(Ctx.bigLot);
   double profitSmall = CalcProfit(Ctx.smallLot, smallMovePoints);
   double lossClosedBig = CalcProfit(closeBigLot, smallMovePoints);
   double costs = 0.0;
   double netSmall = profitSmall - lossClosedBig - costs;

   if(!ClosePositionByTicket(Ctx.smallTicket, Ctx.smallLot))
   {
      SetState(STATE_ERROR, "failed to close Small 100% in Small-scenario");
      return;
   }

   if(closeBigLot > 0.0)
   {
      if(!ClosePositionByTicket(Ctx.bigTicket, closeBigLot))
      {
         SetState(STATE_ERROR, "failed to close Big 30% in Small-scenario");
         return;
      }
   }

   PositionSnapshot oldFar;
   bool oldFarStillExists = GetManagedPositionByTicket(Ctx.farTicket, oldFar) || (!AllowRealTrading && Ctx.farLot > 0.0);
   Ctx.dualTailDetected = oldFarStillExists && remainBigLot > 0.0;

   LogSmallScenario(
      Ctx.harvestLevel,
      Ctx.farTicket,
      Ctx.farDirection,
      Ctx.farLot,
      Ctx.smallLot,
      closeBigLot,
      remainBigLot,
      smallMovePoints,
      profitSmall,
      lossClosedBig,
      netSmall,
      Ctx.dualTailDetected,
      STATE_SMALL_SCENARIO
   );

   if(netSmall <= 0.0)
   {
      SetState(STATE_STOP, "Small-scenario net profit is not positive");
      return;
   }

   if(Ctx.dualTailDetected)
   {
      SetState(STATE_DUAL_TAIL, "old Far plus remaining Big detected; new level stopped");
      return;
   }

   Ctx.farTicket = Ctx.bigTicket;
   Ctx.farLot = remainBigLot;
   Ctx.farOpenPrice = Ctx.bigOpenPrice;
   Ctx.farDirection = Ctx.bigDirection;
   Ctx.bigTicket = 0;
   Ctx.smallTicket = 0;
   Ctx.bigLot = 0.0;
   Ctx.smallLot = 0.0;

   SetState(STATE_FAR_ACTIVE, "remaining 70% Big became new Far");
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

      case STATE_SMALL_SCENARIO:
         ProcessSmallScenario();
         break;

      case STATE_FINAL_CLOSE:
         ProcessFinalClose();
         break;

      case STATE_CLOSED_PROFIT:
      case STATE_DUAL_TAIL:
      case STATE_STOP:
      case STATE_ERROR:
         break;

      default:
         SetState(STATE_ERROR, "unknown state");
         break;
   }
}

#endif // __BH_STATEMACHINE_MQH__
