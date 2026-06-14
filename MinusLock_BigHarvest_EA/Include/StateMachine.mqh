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
   Ctx.initialFarDistancePoints = 0.0;
   Ctx.currentBigMovePoints = 0.0;
   Ctx.cumulativeBigMovePoints = 0.0;
   Ctx.effectiveFarDistancePoints = 0.0;
   Ctx.currentClosePrice = 0.0;

   Ctx.cycleStartTime = 0;
   Ctx.initialIgnoredProfit = 0.0;
   Ctx.realRecoveryPL = 0.0;
   Ctx.realCyclePL = 0.0;
   Ctx.realClosedProfit = 0.0;
   Ctx.realClosedLoss = 0.0;
   Ctx.realCommission = 0.0;
   Ctx.realSwap = 0.0;
   Ctx.realCosts = 0.0;
   Ctx.theoreticalCyclePL = 0.0;
   Ctx.cycleStartBalance = 0.0;
   Ctx.cycleCurrentBalance = 0.0;
   Ctx.cycleBalancePL = 0.0;
   Ctx.realCycleProfitPositive = false;
   Ctx.lastCloseWasSystemClose = false;
   Ctx.lastSystemCloseComment = "";
}

double CalcRealRecoveryPL()
{
   Ctx.cycleCurrentBalance = AccountInfoDouble(ACCOUNT_BALANCE);
   Ctx.cycleBalancePL = Ctx.cycleCurrentBalance - Ctx.cycleStartBalance;

   if(Ctx.realCyclePL != 0.0 || Ctx.realClosedProfit != 0.0 || Ctx.realClosedLoss != 0.0 || Ctx.realCommission != 0.0 || Ctx.realSwap != 0.0)
      Ctx.realRecoveryPL = Ctx.realCyclePL;
   else
      Ctx.realRecoveryPL = Ctx.cycleBalancePL;

   Ctx.realCycleProfitPositive = Ctx.realRecoveryPL > 0.0;
   return Ctx.realRecoveryPL;
}

bool RecalculateRealCycleStatsFromHistory()
{
   Ctx.cycleCurrentBalance = AccountInfoDouble(ACCOUNT_BALANCE);
   Ctx.cycleBalancePL = Ctx.cycleCurrentBalance - Ctx.cycleStartBalance;

   Ctx.realClosedProfit = 0.0;
   Ctx.realClosedLoss = 0.0;
   Ctx.realCommission = 0.0;
   Ctx.realSwap = 0.0;
   Ctx.realCosts = 0.0;
   Ctx.realCyclePL = 0.0;

   bool foundDeals = false;

   if(AllowRealTrading && Ctx.cycleStartTime > 0)
   {
      datetime fromTime = Ctx.cycleStartTime;
      datetime toTime = TimeCurrent() + 86400;
      if(HistorySelect(fromTime, toTime))
      {
         int totalDeals = HistoryDealsTotal();
         for(int i = 0; i < totalDeals; i++)
         {
            ulong dealTicket = HistoryDealGetTicket(i);
            if(dealTicket == 0)
               continue;

            if((ulong)HistoryDealGetInteger(dealTicket, DEAL_MAGIC) != MagicNumber)
               continue;

            if((ENUM_DEAL_ENTRY)HistoryDealGetInteger(dealTicket, DEAL_ENTRY) != DEAL_ENTRY_OUT)
               continue;

            double dealProfit = HistoryDealGetDouble(dealTicket, DEAL_PROFIT);
            double dealCommission = HistoryDealGetDouble(dealTicket, DEAL_COMMISSION);
            double dealSwap = HistoryDealGetDouble(dealTicket, DEAL_SWAP);
            double dealNet = dealProfit + dealCommission + dealSwap;

            if(dealNet >= 0.0)
               Ctx.realClosedProfit += dealNet;
            else
               Ctx.realClosedLoss += dealNet;

            Ctx.realCommission += dealCommission;
            Ctx.realSwap += dealSwap;
            foundDeals = true;
         }
      }
   }

   Ctx.realCosts = Ctx.realCommission + Ctx.realSwap;
   Ctx.realCyclePL = Ctx.realClosedProfit + Ctx.realClosedLoss;

   if(!foundDeals)
      Ctx.realCyclePL = Ctx.cycleBalancePL;

   CalcRealRecoveryPL();
   return foundDeals;
}

void MarkSystemClose(string closeComment)
{
   Ctx.lastCloseWasSystemClose = true;
   Ctx.lastSystemCloseComment = closeComment;
}

bool IsRealRecoveryPass()
{
   return State == STATE_CLOSED_PROFIT &&
          Ctx.realRecoveryPL > 0.0 &&
          CountManagedOpenPositions() == 0 &&
          Ctx.lastCloseWasSystemClose &&
          (Ctx.lastSystemCloseComment == "FINAL_CLOSE" || Ctx.lastSystemCloseComment == "CLOSED_PROFIT");
}

void LogRealCycleMath(EAState state, double onTesterValue)
{
   bool passByRealPL = (state == STATE_CLOSED_PROFIT && Ctx.realRecoveryPL > 0.0 && CountManagedOpenPositions() == 0 && Ctx.lastCloseWasSystemClose);
   PrintFormat(
      "REAL_CYCLE_MATH | State=%s InitialIgnoredProfit=%.2f CycleStartBalance=%.2f CurrentBalance=%.2f RealRecoveryPL=%.2f RealClosedProfit=%.2f RealClosedLoss=%.2f RealCommission=%.2f RealSwap=%.2f RealCosts=%.2f TheoreticalCyclePL=%.2f LastSystemCloseComment=%s OnTesterValue=%.2f PassByRealPL=%s",
      StateToString(state),
      Ctx.initialIgnoredProfit,
      Ctx.cycleStartBalance,
      Ctx.cycleCurrentBalance,
      Ctx.realRecoveryPL,
      Ctx.realClosedProfit,
      Ctx.realClosedLoss,
      Ctx.realCommission,
      Ctx.realSwap,
      Ctx.realCosts,
      Ctx.theoreticalCyclePL,
      Ctx.lastSystemCloseComment,
      onTesterValue,
      passByRealPL ? "YES" : "NO"
   );

   WriteCycleMathCsv(
      Ctx.harvestLevel,
      "REAL_CYCLE_MATH",
      Ctx.farLot,
      Ctx.bigLot,
      Ctx.smallLot,
      Ctx.realRecoveryPL,
      0.0,
      0.0,
      Ctx.totalReserve,
      CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints),
      Ctx.finalCloseAllowed,
      state,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      Ctx.smallReverseNet,
      0.0,
      0.0,
      Ctx.farLot,
      Ctx.reverseStrength,
      Ctx.projectedReserveCoverage,
      passByRealPL ? "REAL_PASS" : "REAL_FAIL",
      passByRealPL ? "" : "RealRecoveryPL <= 0 or system close missing",
      Ctx.theoreticalCyclePL,
      Ctx.realRecoveryPL,
      Ctx.realCosts,
      Ctx.totalReserve,
      0.0,
      Ctx.initialFarDistancePoints,
      Ctx.currentBigMovePoints,
      Ctx.cumulativeBigMovePoints,
      Ctx.effectiveFarDistancePoints,
      FarDistanceModeToString(WorkFarDistanceMode),
      Ctx.farOpenPrice,
      Ctx.currentClosePrice,
      Ctx.initialIgnoredProfit,
      Ctx.cycleStartBalance,
      Ctx.cycleCurrentBalance,
      Ctx.realRecoveryPL,
      Ctx.realClosedProfit,
      Ctx.realClosedLoss,
      Ctx.realCommission,
      Ctx.realSwap,
      Ctx.realCosts,
      Ctx.theoreticalCyclePL,
      Ctx.lastSystemCloseComment,
      passByRealPL
   );
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
   Print("OPEN_INITIAL_LOCK_START");
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double spreadPoints = 0.0;
   if(point > 0.0 && ask > 0.0 && bid > 0.0)
      spreadPoints = (ask - bid) / point;

   Print("Bid=", bid);
   Print("Ask=", ask);
   Print("Spread=", spreadPoints);
   Print("SYMBOL_VOLUME_MIN=", SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN));
   Print("SYMBOL_VOLUME_STEP=", SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP));
   Print("SYMBOL_TRADE_MODE=", (int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_MODE));
   Print("SYMBOL_TRADE_EXECUTION=", (int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_EXEMODE));

   PositionSnapshot initialBuy;
   PositionSnapshot initialSell;

   bool hasBuy = GetInitialBuy(initialBuy);
   bool hasSell = GetInitialSell(initialSell);

   if(hasBuy && hasSell)
   {
      Print("INITIAL LOCK CREATED");
      Print("BuyTicket=", initialBuy.ticket);
      Print("SellTicket=", initialSell.ticket);
      Print("State=STATE_INITIAL_LOCK");
      SetState(STATE_INITIAL_LOCK_OPENED, "existing initial BUY/SELL lock found");
      return;
   }

   int managedPositions = CountManagedOpenPositions();
   if(managedPositions > 0)
   {
      LogError(StringFormat("Managed positions already exist but the initial lock is incomplete: ManagedPositions=%d", managedPositions));
      SetState(STATE_ERROR, "incomplete managed position set before initial lock");
      return;
   }

   double lot = NormalizeLotNearest(StartLot);
   Print("NormalizedLot=", lot);
   if(lot <= 0.0)
   {
      LogError("StartLot normalized to zero");
      Print("TRADE ERROR=", GetLastError());
      SetState(STATE_ERROR, "invalid StartLot");
      return;
   }

   ResetLastError();
   bool buyOpened = OpenPosition(DIR_BUY, lot, "MinusLock_INITIAL_BUY");
   if(!buyOpened)
   {
      Print("TRADE ERROR=", GetLastError());
      LogError("Failed to open initial BUY");
      SetState(STATE_ERROR, "initial BUY open failed");
      return;
   }

   if(GetInitialBuy(initialBuy))
   {
      Print("INITIAL BUY OPENED");
      Print("Ticket=", initialBuy.ticket);
      Print("Lot=", lot);
   }
   else
   {
      Print("INITIAL BUY OPENED");
      Print("Ticket=0");
      Print("Lot=", lot);
   }

   ResetLastError();
   bool sellOpened = OpenPosition(DIR_SELL, lot, "MinusLock_INITIAL_SELL");
   if(!sellOpened)
   {
      Print("TRADE ERROR=", GetLastError());
      LogError("Failed to open initial SELL");
      SetState(STATE_ERROR, "initial SELL open failed");
      return;
   }

   if(GetInitialSell(initialSell))
   {
      Print("INITIAL SELL OPENED");
      Print("Ticket=", initialSell.ticket);
      Print("Lot=", lot);
   }
   else
   {
      Print("INITIAL SELL OPENED");
      Print("Ticket=0");
      Print("Lot=", lot);
   }

   if(GetInitialBuy(initialBuy) && GetInitialSell(initialSell))
   {
      Print("INITIAL LOCK CREATED");
      Print("BuyTicket=", initialBuy.ticket);
      Print("SellTicket=", initialSell.ticket);
      Print("State=STATE_INITIAL_LOCK");
   }
   else
   {
      LogError("Initial BUY/SELL lock was opened but tickets could not be read back");
      Print("TRADE ERROR=", GetLastError());
      SetState(STATE_ERROR, "initial lock ticket readback failed");
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
      Ctx.initialIgnoredProfit = initialBuy.profitMoney;
      Ctx.totalReserve = 0.0;
      Ctx.cycleFinalPL = 0.0;
      Ctx.theoreticalCyclePL = 0.0;
      Ctx.cycleStartBalance = AccountInfoDouble(ACCOUNT_BALANCE);
      Ctx.cycleCurrentBalance = Ctx.cycleStartBalance;
      Ctx.cycleStartTime = TimeCurrent();
      Ctx.realRecoveryPL = 0.0;
      Ctx.realCyclePL = 0.0;
      Ctx.lastCloseWasSystemClose = false;
      Ctx.lastSystemCloseComment = "";
      Ctx.initialFarDistancePoints = InitialTriggerPoints;
      Ctx.cumulativeBigMovePoints = 0.0;

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
      Ctx.initialIgnoredProfit = initialSell.profitMoney;
      Ctx.totalReserve = 0.0;
      Ctx.cycleFinalPL = 0.0;
      Ctx.theoreticalCyclePL = 0.0;
      Ctx.cycleStartBalance = AccountInfoDouble(ACCOUNT_BALANCE);
      Ctx.cycleCurrentBalance = Ctx.cycleStartBalance;
      Ctx.cycleStartTime = TimeCurrent();
      Ctx.realRecoveryPL = 0.0;
      Ctx.realCyclePL = 0.0;
      Ctx.lastCloseWasSystemClose = false;
      Ctx.lastSystemCloseComment = "";
      Ctx.initialFarDistancePoints = InitialTriggerPoints;
      Ctx.cumulativeBigMovePoints = 0.0;

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

   if(Ctx.harvestLevel >= WorkMaxHarvestLevels)
   {
      SetState(STATE_STOP, "WorkMaxHarvestLevels reached before FinalCloseAllowed");
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
   Ctx.currentBigMovePoints = bigMovePoints;
   Ctx.cumulativeBigMovePoints += bigMovePoints;
   Ctx.currentClosePrice = ExitPriceForDirection(Ctx.bigDirection);
   Ctx.effectiveFarDistancePoints = CalcEffectiveFarDistancePoints(
      Ctx.initialFarDistancePoints,
      Ctx.currentBigMovePoints,
      Ctx.cumulativeBigMovePoints,
      Ctx.currentClosePrice,
      Ctx.farOpenPrice
   );
   double profitBig = CalcProfit(Ctx.bigLot, bigMovePoints);
   double lossSmall = CalcProfit(Ctx.smallLot, bigMovePoints);
   double costs = 0.0;
   double totalReserveBefore = Ctx.totalReserve;
   double netProfit = profitBig - lossSmall - costs;
   double closeFarBudget = CalcCloseFarBudget(netProfit);
   double reserveAdd = CalcReserveAdd(netProfit);
   double closeFarLotRaw = CalcCloseFarLotRaw(closeFarBudget, Ctx.effectiveFarDistancePoints);
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
      bool farClosedByBudget = false;
      if(closeFarLotFinal >= Ctx.farLot)
      {
         MarkSystemClose("CLOSED_PROFIT");
         farClosedByBudget = ClosePositionByTicketWithComment(Ctx.farTicket, closeFarLotFinal, "CLOSED_PROFIT");
      }
      else
         farClosedByBudget = ClosePositionByTicket(Ctx.farTicket, closeFarLotFinal);

      if(!farClosedByBudget)
      {
         SetState(STATE_ERROR, "failed to close Far by money budget");
         return;
      }
   }

   Ctx.totalReserve += reserveAdd;
   Ctx.farLot = NormalizeLotDown(MathMax(0.0, Ctx.farLot - closeFarLotFinal));
   Ctx.finalCloseAllowed = CalcFinalCloseAllowed(Ctx.totalReserve, Ctx.farLot, Ctx.effectiveFarDistancePoints);
   Ctx.cycleFinalPL = Ctx.totalReserve - CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
   Ctx.theoreticalCyclePL = Ctx.cycleFinalPL;

   double farRemainLoss = CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);

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

   LogCycleMathDetailed(
      Ctx.harvestLevel,
      "BIG_HARVEST",
      farStartLot,
      Ctx.bigLot,
      Ctx.smallLot,
      netProfit,
      closeFarBudget,
      reserveAdd,
      Ctx.totalReserve,
      farRemainLoss,
      Ctx.finalCloseAllowed,
      STATE_BIG_HARVEST,
      profitBig,
      lossSmall,
      0.0,
      0.0,
      0.0,
      0.0,
      closeFarLotRaw,
      closeFarLotRounded,
      Ctx.farLot,
      Ctx.reverseStrength,
      Ctx.projectedReserveCoverage,
      Ctx.finalCloseAllowed ? "FINAL_CLOSE_ALLOWED" : "REPEAT_HARVEST_OR_STOP_CHECK",
      "",
      netProfit,
      netProfit,
      costs,
      totalReserveBefore,
      Ctx.finalCloseAllowed ? farRemainLoss : 0.0
   );

   Ctx.bigTicket = 0;
   Ctx.smallTicket = 0;
   Ctx.bigLot = 0.0;
   Ctx.smallLot = 0.0;

   if(Ctx.farLot <= 0.0)
   {
      SetState(STATE_CLOSED_PROFIT, "Far was fully closed by Big-harvest budget");
      RecalculateRealCycleStatsFromHistory();
      LogRealCycleMath(State, IsRealRecoveryPass() ? Ctx.realRecoveryPL : -1.0);
      return;
   }

   if(Ctx.finalCloseAllowed)
   {
      SetState(STATE_FINAL_CLOSE, "TotalReserve covers remaining Far loss");
      return;
   }

   if(Ctx.harvestLevel >= WorkMaxHarvestLevels)
   {
      LogCycleMathDetailed(
         Ctx.harvestLevel,
         "STOP_MAX_LEVELS",
         Ctx.farLot,
         0.0,
         0.0,
         0.0,
         0.0,
         0.0,
         Ctx.totalReserve,
         CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints),
         false,
         STATE_STOP_MAX_LEVELS,
         0.0,
         0.0,
         0.0,
         0.0,
         0.0,
         0.0,
         0.0,
         0.0,
         Ctx.farLot,
         Ctx.reverseStrength,
         Ctx.projectedReserveCoverage,
         "STOP_MAX_LEVELS_CLOSE_RESIDUAL_FAR",
         "WorkMaxHarvestLevels reached after Big-harvest",
         0.0,
         0.0,
         0.0,
         Ctx.totalReserve,
         0.0
      );
      LogError(StringFormat("STOP_MAX_LEVELS: WorkMaxHarvestLevels=%d reached after Big-harvest. OpenFarLot=%.2f FarTicket=%I64u FinalCloseAllowed=NO State=%s", WorkMaxHarvestLevels, Ctx.farLot, Ctx.farTicket, StateToString(State)));
      if(Ctx.farLot > 0.0 && Ctx.farTicket != 0)
      {
         if(!ClosePositionByTicketWithComment(Ctx.farTicket, Ctx.farLot, "STOP_MAX_LEVELS"))
         {
            SetState(STATE_UNCLOSED_CYCLE, "WorkMaxHarvestLevels reached; failed to close Far with STOP_MAX_LEVELS");
            return;
         }
      }
      Ctx.farTicket = 0;
      Ctx.farLot = 0.0;
      SetState(STATE_UNCLOSED_CYCLE, "STOP_MAX_LEVELS: cycle failed, residual Far closed by EA to prevent end-of-test distortion");
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
   double closeBigLotRaw = bigLot * WorkCloseBigOnSmall;
   double closeBigLotRounded = NormalizeLotNearest(closeBigLotRaw);
   double remainBigLot = NormalizeLotDown(MathMax(0.0, bigLot - closeBigLotRounded));
   double closedBigPL = CalcSignedPositionPL(bigDirection, closeBigLotRounded, bigOpenPrice, currentPrice);
   double costs = 0.0;
   double totalReserveBefore = Ctx.totalReserve;
   double smallScenarioTotalPL = smallPL + oldFarPL + closedBigPL - costs;

   double newFarLot = remainBigLot;
   Direction newFarDirection = bigDirection;
   double newBigLot = CalcBigLot(newFarLot);
   double newSmallLot = CalcSmallLot(newBigLot);
   double expectedNextReserve = CalcExpectedNextReserve(newBigLot, newSmallLot, Ctx.harvestLevel + 1);
   double expectedNextFarLoss = 0.0;
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
         WorkMaxReverseCycles, geometryInvalidReason, smallInvalidReason, riskWarningReason
      );
      LogCycleMathDetailed(
         Ctx.harvestLevel,
         "SMALL_AT_FAR",
         oldFarLot,
         bigLot,
         smallLot,
         smallReverseNet,
         0.0,
         0.0,
         Ctx.totalReserve,
         expectedNextFarLoss,
         false,
         STATE_INVALID_REVERSE_GEOMETRY,
         0.0,
         0.0,
         smallPL,
         oldFarPL,
         closedBigPL,
         smallReverseNet,
         0.0,
         closeBigLotRounded,
         newFarLot,
         reverseStrength,
         projectedReserveCoverage,
         actionAfterValidation,
         geometryInvalidReason,
         smallScenarioTotalPL,
         smallReverseNet,
         costs,
         totalReserveBefore,
         0.0
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
         WorkMaxReverseCycles, geometryInvalidReason, smallInvalidReason, riskWarningReason
      );
      LogCycleMathDetailed(
         Ctx.harvestLevel,
         "SMALL_AT_FAR",
         oldFarLot,
         bigLot,
         smallLot,
         smallReverseNet,
         0.0,
         0.0,
         Ctx.totalReserve,
         expectedNextFarLoss,
         false,
         STATE_INVALID_SMALL_GEOMETRY,
         0.0,
         0.0,
         smallPL,
         oldFarPL,
         closedBigPL,
         smallReverseNet,
         0.0,
         closeBigLotRounded,
         newFarLot,
         reverseStrength,
         projectedReserveCoverage,
         actionAfterValidation,
         smallInvalidReason,
         smallScenarioTotalPL,
         smallReverseNet,
         costs,
         totalReserveBefore,
         0.0
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
   Ctx.reverseLimitReached = Ctx.reverseCycleCount > WorkMaxReverseCycles;
   if(Ctx.reverseLimitReached && StopOnReverseLimit)
      actionAfterValidation = "STOP_REVERSE_LIMIT";

   Ctx.farTicket = bigTicket;
   Ctx.farLot = newFarLot;
   Ctx.farOpenPrice = currentPrice;
   Ctx.farDirection = newFarDirection;
   Ctx.initialFarDistancePoints = 0.0;
   Ctx.currentBigMovePoints = 0.0;
   Ctx.cumulativeBigMovePoints = 0.0;
   Ctx.effectiveFarDistancePoints = 0.0;
   Ctx.currentClosePrice = currentPrice;
   Ctx.bigTicket = 0;
   Ctx.smallTicket = 0;
   Ctx.bigLot = 0.0;
   Ctx.smallLot = 0.0;
   Ctx.bigOpenPrice = 0.0;
   Ctx.smallOpenPrice = 0.0;
   Ctx.bigDirection = DIR_NONE;
   Ctx.smallDirection = DIR_NONE;
   Ctx.dualTailDetected = false;

   double farRemainLoss = CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
   Ctx.finalCloseAllowed = CalcFinalCloseAllowed(Ctx.totalReserve, Ctx.farLot, Ctx.effectiveFarDistancePoints);
   Ctx.cycleFinalPL = Ctx.totalReserve - farRemainLoss;
   Ctx.theoreticalCyclePL = Ctx.cycleFinalPL;

   if(Ctx.finalCloseAllowed)
      actionAfterValidation = "FINAL_CLOSE_NEW_FAR";
   else if(Ctx.harvestLevel >= WorkMaxHarvestLevels)
      actionAfterValidation = "STOP_MAX_LEVELS";
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
      WorkMaxReverseCycles, geometryInvalidReason, smallInvalidReason, riskWarningReason
   );

   LogCycleMathDetailed(
      Ctx.harvestLevel,
      "SMALL_AT_FAR",
      oldFarLot,
      bigLot,
      smallLot,
      smallReverseNet,
      0.0,
      0.0,
      Ctx.totalReserve,
      farRemainLoss,
      Ctx.finalCloseAllowed,
      STATE_SMALL_SCENARIO,
      0.0,
      0.0,
      smallPL,
      oldFarPL,
      closedBigPL,
      smallReverseNet,
      0.0,
      closeBigLotRounded,
      Ctx.farLot,
      reverseStrength,
      projectedReserveCoverage,
      actionAfterValidation,
      "",
      smallScenarioTotalPL,
      smallReverseNet,
      costs,
      totalReserveBefore,
      Ctx.finalCloseAllowed ? farRemainLoss : 0.0
   );

   if(Ctx.reverseLimitReached && StopOnReverseLimit)
   {
      SetState(STATE_REVERSE_LIMIT, "reverseCycleCount > WorkMaxReverseCycles");
      return;
   }

   if(!Ctx.finalCloseAllowed && Ctx.harvestLevel >= WorkMaxHarvestLevels)
   {
      LogCycleMathDetailed(
         Ctx.harvestLevel,
         "STOP_MAX_LEVELS",
         Ctx.farLot,
         0.0,
         0.0,
         0.0,
         0.0,
         0.0,
         Ctx.totalReserve,
         CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints),
         false,
         STATE_STOP_MAX_LEVELS,
         0.0,
         0.0,
         0.0,
         0.0,
         0.0,
         Ctx.smallReverseNet,
         0.0,
         0.0,
         Ctx.farLot,
         Ctx.reverseStrength,
         Ctx.projectedReserveCoverage,
         "STOP_MAX_LEVELS_CLOSE_NEW_FAR",
         "WorkMaxHarvestLevels reached after Small-at-Far",
         0.0,
         0.0,
         0.0,
         Ctx.totalReserve,
         0.0
      );
      LogError(StringFormat("STOP_MAX_LEVELS: WorkMaxHarvestLevels=%d reached after Small-at-Far. NewFarLot=%.2f NewFarTicket=%I64u FinalCloseAllowed=NO CycleFinalPL=%.2f", WorkMaxHarvestLevels, Ctx.farLot, Ctx.farTicket, Ctx.cycleFinalPL));
      if(Ctx.farLot > 0.0 && Ctx.farTicket != 0)
      {
         if(!ClosePositionByTicketWithComment(Ctx.farTicket, Ctx.farLot, "STOP_MAX_LEVELS"))
         {
            SetState(STATE_UNCLOSED_CYCLE, "WorkMaxHarvestLevels reached after Small-at-Far; failed to close NewFar with STOP_MAX_LEVELS");
            return;
         }
      }
      Ctx.farTicket = 0;
      Ctx.farLot = 0.0;
      SetState(STATE_UNCLOSED_CYCLE, "STOP_MAX_LEVELS: NewFar closed by EA; cycle not successful");
      return;
   }

   if(Ctx.farLot <= 0.0)
   {
      MarkSystemClose("CLOSED_PROFIT");
      SetState(STATE_CLOSED_PROFIT, "Small-at-Far left no NewFar lot");
      RecalculateRealCycleStatsFromHistory();
      LogRealCycleMath(State, IsRealRecoveryPass() ? Ctx.realRecoveryPL : -1.0);
      return;
   }

   if(Ctx.finalCloseAllowed)
   {
      MarkSystemClose("FINAL_CLOSE");
      if(!ClosePositionByTicketWithComment(Ctx.farTicket, Ctx.farLot, "FINAL_CLOSE"))
      {
         SetState(STATE_ERROR, "failed to close NewFar after Small-at-Far FinalCloseAllowed");
         return;
      }

      Ctx.farTicket = 0;
      Ctx.farLot = 0.0;
      SetState(STATE_CLOSED_PROFIT, "FinalCloseAllowed after Small-at-Far; NewFar closed and no new Big/Small opened");
      RecalculateRealCycleStatsFromHistory();
      LogRealCycleMath(State, IsRealRecoveryPass() ? Ctx.realRecoveryPL : -1.0);
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
      RecalculateRealCycleStatsFromHistory();
      LogRealCycleMath(State, IsRealRecoveryPass() ? Ctx.realRecoveryPL : -1.0);
      return;
   }

   double farRemainLoss = CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
   Ctx.cycleFinalPL = Ctx.totalReserve - farRemainLoss;
   Ctx.theoreticalCyclePL = Ctx.cycleFinalPL;

   LogCycleMathDetailed(
      Ctx.harvestLevel,
      "FINAL_CLOSE",
      Ctx.farLot,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      Ctx.totalReserve,
      farRemainLoss,
      true,
      STATE_FINAL_CLOSE,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      Ctx.farLot,
      Ctx.reverseStrength,
      Ctx.projectedReserveCoverage,
      "FINAL_CLOSE_RESIDUAL_FAR",
      "",
      0.0,
      0.0,
      0.0,
      Ctx.totalReserve,
      farRemainLoss
   );

   MarkSystemClose("FINAL_CLOSE");
   if(!ClosePositionByTicketWithComment(Ctx.farTicket, Ctx.farLot, "FINAL_CLOSE"))
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
   RecalculateRealCycleStatsFromHistory();
   LogRealCycleMath(State, IsRealRecoveryPass() ? Ctx.realRecoveryPL : -1.0);
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
      case STATE_STOP_MAX_LEVELS:
      case STATE_UNCLOSED_CYCLE:
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
