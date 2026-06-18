#ifndef __BH_STATEMACHINE_MQH__
#define __BH_STATEMACHINE_MQH__

EAState State = STATE_IDLE;
RecoveryContext Ctx;

void SetState(EAState nextState, string reason)
{
   if(State != nextState)
      LogTransition(State, nextState, reason);

   State = nextState;
   Ctx.lastAction = reason;
   if(nextState == STATE_ERROR || nextState == STATE_MANUAL_INTERVENTION_REQUIRED || nextState == STATE_RECOVERY_PENDING)
      Ctx.lastError = reason;
   SaveState();
}

string StateKey(string field)
{
   return StringFormat("BH_%s_%I64u_%s", _Symbol, MagicNumber, field);
}

void SaveState()
{
   GlobalVariableSet(StateKey("State"), (double)State);
   GlobalVariableSet(StateKey("FarTicket"), (double)Ctx.farTicket);
   GlobalVariableSet(StateKey("FarLot"), Ctx.farLot);
   GlobalVariableSet(StateKey("FarOpenPrice"), Ctx.farOpenPrice);
   GlobalVariableSet(StateKey("FarDirection"), (double)Ctx.farDirection);
   GlobalVariableSet(StateKey("BigTicket"), (double)Ctx.bigTicket);
   GlobalVariableSet(StateKey("BigLot"), Ctx.bigLot);
   GlobalVariableSet(StateKey("BigOpenPrice"), Ctx.bigOpenPrice);
   GlobalVariableSet(StateKey("BigDirection"), (double)Ctx.bigDirection);
   GlobalVariableSet(StateKey("SmallTicket"), (double)Ctx.smallTicket);
   GlobalVariableSet(StateKey("SmallLot"), Ctx.smallLot);
   GlobalVariableSet(StateKey("SmallOpenPrice"), Ctx.smallOpenPrice);
   GlobalVariableSet(StateKey("SmallDirection"), (double)Ctx.smallDirection);
   GlobalVariableSet(StateKey("HarvestLevel"), (double)Ctx.harvestLevel);
   GlobalVariableSet(StateKey("ReverseCycles"), (double)Ctx.reverseCycleCount);
   GlobalVariableSet(StateKey("TotalReserve"), Ctx.totalReserve);
   GlobalVariableSet(StateKey("CycleId"), (double)Ctx.cycleId);
   GlobalVariableSet(StateKey("InitialProfitIgnored"), Ctx.initialProfitIgnored ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("EffectiveFarDistancePoints"), Ctx.effectiveFarDistancePoints);
   GlobalVariableSet(StateKey("CycleStartBalance"), Ctx.cycleStartBalance);
   GlobalVariableSet(StateKey("RealCyclePL"), Ctx.realCyclePL);
   GlobalVariableSet(StateKey("FinalCloseAllowed"), Ctx.finalCloseAllowed ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("LastRetryState"), (double)Ctx.lastRetryState);
   GlobalVariableSet(StateKey("RetryTicket"), (double)Ctx.retryTicket);
   GlobalVariableSet(StateKey("RetryLot"), Ctx.retryLot);
   GlobalVariableSet(StateKey("RetryAttempts"), (double)Ctx.retryAttempts);
}

bool GetStateDouble(string field, double &value)
{
   string key = StateKey(field);
   if(!GlobalVariableCheck(key))
      return false;
   value = GlobalVariableGet(key);
   return true;
}

bool ReconcileRecoveredPosition(string legName, string comment, ulong &ticket, double &lot, double &openPrice, Direction &direction)
{
   if(ticket == 0 && lot <= 0.0)
      return true;

   PositionSnapshot snapshot;
   bool found = GetManagedPositionByTicket(ticket, snapshot);
   if(!found && comment != "")
      found = GetManagedPositionByComment(comment, snapshot);

   if(found)
   {
      // Reconcile by Symbol + MagicNumber + Ticket + Position identifier + Comment + Direction + Lot + OpenPrice.
      ticket = snapshot.ticket;
      lot = snapshot.lot;
      openPrice = snapshot.openPrice;
      direction = snapshot.direction;
      LogInfo(StringFormat("RECOVER_RECONCILE %s OK Ticket=%I64u Comment=%s Direction=%s Lot=%.2f OpenPrice=%.5f", legName, ticket, snapshot.comment, DirectionToString(direction), lot, openPrice));
      return true;
   }

   LogError(StringFormat("RECOVER_RECONCILE %s missing saved Ticket=%I64u Comment=%s Lot=%.2f OpenPrice=%.5f", legName, ticket, comment, lot, openPrice));
   return false;
}

void LogManagedPositionsForRecovery()
{
   LogInfo(StringFormat("RECOVERY_DIAGNOSTICS Managed positions found=%d", CountManagedOpenPositions()));
   if(IsInternalSimulationMode())
      return;

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;

      string symbol = PositionGetString(POSITION_SYMBOL);
      ulong magic = (ulong)PositionGetInteger(POSITION_MAGIC);
      ulong identifier = (ulong)PositionGetInteger(POSITION_IDENTIFIER);
      string comment = PositionGetString(POSITION_COMMENT);
      double lot = PositionGetDouble(POSITION_VOLUME);
      double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
      Direction direction = PositionTypeToDirection(PositionGetInteger(POSITION_TYPE));
      LogInfo(StringFormat("RECOVERY_POSITION Symbol=%s MagicNumber=%I64u Ticket=%I64u Position identifier=%I64u Comment=%s Direction=%s Lot=%.2f OpenPrice=%.5f", symbol, magic, ticket, identifier, comment, DirectionToString(direction), lot, openPrice));
   }
}

bool RecoverState()
{
   if(!GlobalVariableCheck(StateKey("State")))
      return false;

   ResetRecoveryContext();
   State = (EAState)(int)GlobalVariableGet(StateKey("State"));
   Ctx.farTicket = (ulong)GlobalVariableGet(StateKey("FarTicket"));
   Ctx.farLot = GlobalVariableGet(StateKey("FarLot"));
   Ctx.farOpenPrice = GlobalVariableGet(StateKey("FarOpenPrice"));
   Ctx.farDirection = (Direction)(int)GlobalVariableGet(StateKey("FarDirection"));
   Ctx.bigTicket = (ulong)GlobalVariableGet(StateKey("BigTicket"));
   Ctx.bigLot = GlobalVariableGet(StateKey("BigLot"));
   Ctx.bigOpenPrice = GlobalVariableGet(StateKey("BigOpenPrice"));
   Ctx.bigDirection = (Direction)(int)GlobalVariableGet(StateKey("BigDirection"));
   Ctx.smallTicket = (ulong)GlobalVariableGet(StateKey("SmallTicket"));
   Ctx.smallLot = GlobalVariableGet(StateKey("SmallLot"));
   Ctx.smallOpenPrice = GlobalVariableGet(StateKey("SmallOpenPrice"));
   Ctx.smallDirection = (Direction)(int)GlobalVariableGet(StateKey("SmallDirection"));
   Ctx.harvestLevel = (int)GlobalVariableGet(StateKey("HarvestLevel"));
   Ctx.reverseCycleCount = (int)GlobalVariableGet(StateKey("ReverseCycles"));
   Ctx.totalReserve = GlobalVariableGet(StateKey("TotalReserve"));

   double saved = 0.0;
   if(GetStateDouble("CycleId", saved)) Ctx.cycleId = (ulong)saved;
   if(GetStateDouble("InitialProfitIgnored", saved)) Ctx.initialProfitIgnored = (saved > 0.5);
   if(GetStateDouble("EffectiveFarDistancePoints", saved)) Ctx.effectiveFarDistancePoints = saved;
   if(GetStateDouble("CycleStartBalance", saved)) Ctx.cycleStartBalance = saved;
   if(GetStateDouble("RealCyclePL", saved)) Ctx.realCyclePL = saved;
   if(GetStateDouble("FinalCloseAllowed", saved)) Ctx.finalCloseAllowed = (saved > 0.5);
   if(GetStateDouble("LastRetryState", saved)) Ctx.lastRetryState = (EAState)(int)saved;
   if(GetStateDouble("RetryTicket", saved)) Ctx.retryTicket = (ulong)saved;
   if(GetStateDouble("RetryLot", saved)) Ctx.retryLot = saved;
   if(GetStateDouble("RetryAttempts", saved)) Ctx.retryAttempts = (int)saved;

   int managed = CountManagedOpenPositions();
   bool reconcileOk = true;
   if(managed > 0)
   {
      LogManagedPositionsForRecovery();
      reconcileOk = ReconcileRecoveredPosition("Far", "", Ctx.farTicket, Ctx.farLot, Ctx.farOpenPrice, Ctx.farDirection);
      if(Ctx.harvestLevel > 0)
      {
         string bigComment = LevelComment("BIG", Ctx.harvestLevel);
         string smallComment = LevelComment("SMALL", Ctx.harvestLevel);
         reconcileOk = ReconcileRecoveredPosition("Big", bigComment, Ctx.bigTicket, Ctx.bigLot, Ctx.bigOpenPrice, Ctx.bigDirection) && reconcileOk;
         reconcileOk = ReconcileRecoveredPosition("Small", smallComment, Ctx.smallTicket, Ctx.smallLot, Ctx.smallOpenPrice, Ctx.smallDirection) && reconcileOk;
      }
   }

   if(managed > 0 && State == STATE_IDLE)
   {
      State = STATE_RECOVERY_PENDING;
      LogError("RecoverState found managed positions while saved state is idle; recovery pending");
   }

   if(!reconcileOk)
   {
      State = STATE_RECOVERY_PENDING;
      Ctx.lastError = "saved state contradicts real open positions";
      LogError("RecoverState reconciliation failed; STATE_RECOVERY_PENDING and possible STATE_MANUAL_INTERVENTION_REQUIRED");
   }

   LogInfo(StringFormat("RecoverState restored State=%s CycleId=%I64u FarTicket=%I64u BigTicket=%I64u SmallTicket=%I64u ManagedPositions=%d RetryState=%s RetryTicket=%I64u RetryAttempts=%d", StateToString(State), Ctx.cycleId, Ctx.farTicket, Ctx.bigTicket, Ctx.smallTicket, managed, StateToString(Ctx.lastRetryState), Ctx.retryTicket, Ctx.retryAttempts));
   return true;
}

void ResetRecoveryContext()
{
   if(IsInternalSimulationMode())
      SimResetHistory();

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
   Ctx.lastAction = "";
   Ctx.lastError = "";
   Ctx.riskGateOk = true;
   Ctx.lastRetryState = STATE_IDLE;
   Ctx.retryTicket = 0;
   Ctx.retryLot = 0.0;
   Ctx.retryAttempts = 0;
   Ctx.lastRetryLogTime = 0;
   Ctx.cycleId = (ulong)TimeCurrent();
}

double CalcRealRecoveryPL()
{
   if(IsInternalSimulationMode())
   {
      Ctx.cycleCurrentBalance = Ctx.cycleStartBalance + Ctx.realCyclePL;
      Ctx.cycleBalancePL = Ctx.realCyclePL;
      Ctx.realRecoveryPL = Ctx.realCyclePL;
      Ctx.realCycleProfitPositive = Ctx.realRecoveryPL > 0.0;
      return Ctx.realRecoveryPL;
   }

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

   if(IsInternalSimulationMode())
   {
      foundDeals = SimRecalculateClosedStats(Ctx.realCyclePL, Ctx.realClosedProfit, Ctx.realClosedLoss);
      Ctx.realCosts = 0.0;
      Ctx.realCommission = 0.0;
      Ctx.realSwap = 0.0;
      Ctx.cycleCurrentBalance = Ctx.cycleStartBalance + Ctx.realCyclePL;
      Ctx.cycleBalancePL = Ctx.realCyclePL;
      CalcRealRecoveryPL();
      return foundDeals;
   }

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

            ulong dealPositionId = (ulong)HistoryDealGetInteger(dealTicket, DEAL_POSITION_ID);
            string dealComment = HistoryDealGetString(dealTicket, DEAL_COMMENT);
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
            LogInfo(StringFormat("HISTORY_DEAL_REAL_PL Ticket=%I64u DEAL_POSITION_ID=%I64u Comment=%s Net=%.2f", dealTicket, dealPositionId, dealComment, dealNet));
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

bool CloseAllManagedPositionsWithComment(string closeComment)
{
   bool ok = true;
   PositionSnapshot snapshot;
   ulong tickets[64];
   double lots[64];
   int count = 0;

   for(int i = PositionsTotal() - 1; i >= 0 && count < 64; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(!ReadSelectedPosition(snapshot))
         continue;
      tickets[count] = snapshot.ticket;
      lots[count] = snapshot.lot;
      count++;
   }

   if(IsInternalSimulationMode())
   {
      if(Ctx.farTicket != 0 && Ctx.farLot > 0.0) ok = ClosePositionByTicketWithComment(Ctx.farTicket, Ctx.farLot, closeComment) && ok;
      if(Ctx.bigTicket != 0 && Ctx.bigLot > 0.0) ok = ClosePositionByTicketWithComment(Ctx.bigTicket, Ctx.bigLot, closeComment) && ok;
      if(Ctx.smallTicket != 0 && Ctx.smallLot > 0.0) ok = ClosePositionByTicketWithComment(Ctx.smallTicket, Ctx.smallLot, closeComment) && ok;
      return ok;
   }

   for(int j = 0; j < count; j++)
      ok = ClosePositionByTicketWithComment(tickets[j], lots[j], closeComment) && ok;

   return ok;
}

void HandleInvalidGeometry(string reason)
{
   LogError(StringFormat("Invalid geometry: %s", reason));
   if(CloseAllOnInvalidGeometry)
   {
      if(CloseAllManagedPositionsWithComment("INVALID_GEOMETRY_CLOSE_ALL"))
         SetState(STATE_INVALID_GEOMETRY_CLOSED, reason);
      else
         SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Invalid geometry close-all failed");
      return;
   }

   SetState(STATE_MANUAL_INTERVENTION_REQUIRED, reason);
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

   if(IsInternalSimulationMode() && Ctx.bigLot > 0.0 && Ctx.smallLot > 0.0)
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
   if(!Ctx.riskGateOk && AllowRealTrading && StopOnRiskGateBlocked)
   {
      LogRiskGateBlocked("OpenInitialLock blocked: RiskGate blocks only new openings, not closes");
      return;
   }
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
      if(GetInitialBuy(initialBuy))
      {
         MarkSystemClose("ROLLBACK_INITIAL_BUY_WITHOUT_SELL");
         ClosePositionByTicketWithComment(initialBuy.ticket, initialBuy.lot, "ROLLBACK_INITIAL_BUY_WITHOUT_SELL");
      }
      SetState(STATE_ERROR, "Initial SELL failed; BUY rolled back");
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
   if(!Ctx.riskGateOk && AllowRealTrading && StopOnRiskGateBlocked)
   {
      LogRiskGateBlocked("OpenBigSmall blocked: RiskGate blocks only new Big/Small openings");
      return;
   }

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

   PositionSnapshot big;
   PositionSnapshot small;

   if(!bigOpened)
   {
      SetState(STATE_ERROR, "failed to open Big leg of Big/Small pair");
      return;
   }

   bool bigFoundAfterOpen = GetManagedPositionByComment(bigComment, big);
   bool smallOpened = OpenPosition(Ctx.smallDirection, Ctx.smallLot, smallComment);

   if(!smallOpened)
   {
      if(bigFoundAfterOpen)
      {
         MarkSystemClose("ROLLBACK_BIG_WITHOUT_SMALL");
         ClosePositionByTicketWithComment(big.ticket, big.lot, "ROLLBACK_BIG_WITHOUT_SMALL");
      }
      SetState(STATE_ERROR, "failed to open Small leg; Big leg rolled back");
      return;
   }

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

void SetRetryContext(EAState pendingState, ulong ticket, double lot, string reason)
{
   Ctx.lastRetryState = pendingState;
   Ctx.retryTicket = ticket;
   Ctx.retryLot = lot;
   Ctx.retryAttempts = 0;
   Ctx.lastRetryLogTime = 0;
   SetState(pendingState, reason);
}

bool RetryCloseTicket(string operationName, string comment, EAState successState)
{
   if(Ctx.retryTicket == 0 || Ctx.retryLot <= 0.0)
   {
      LogError(StringFormat("%s missing retry context Ticket=%I64u Lot=%.2f", operationName, Ctx.retryTicket, Ctx.retryLot));
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, operationName + " missing retry context");
      return false;
   }

   Ctx.retryAttempts++;
   datetime now = TimeCurrent();
   if(Ctx.lastRetryLogTime == 0 || RetryLogIntervalSeconds <= 0 || now - Ctx.lastRetryLogTime >= RetryLogIntervalSeconds)
   {
      Ctx.lastRetryLogTime = now;
      LogInfo(StringFormat("RETRY_CLOSE %s attempt=%d/%d Ticket=%I64u Lot=%.2f Comment=%s RiskGateOk=%s", operationName, Ctx.retryAttempts, MaxCloseRetryAttempts, Ctx.retryTicket, Ctx.retryLot, comment, Ctx.riskGateOk ? "YES" : "NO"));
   }

   MarkSystemClose(comment);
   if(ClosePositionByTicketWithComment(Ctx.retryTicket, Ctx.retryLot, comment))
   {
      Ctx.retryTicket = 0;
      Ctx.retryLot = 0.0;
      Ctx.retryAttempts = 0;
      Ctx.lastRetryState = STATE_IDLE;
      SetState(successState, operationName + " retry close succeeded");
      return true;
   }

   if(MaxCloseRetryAttempts > 0 && Ctx.retryAttempts >= MaxCloseRetryAttempts)
   {
      LogError(StringFormat("%s exceeded MaxCloseRetryAttempts=%d", operationName, MaxCloseRetryAttempts));
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, operationName + " exceeded close retry attempts");
   }
   else
      SaveState();

   return false;
}

void RetryCloseBig()
{
   RetryCloseTicket("RetryCloseBig", "RETRY_CLOSE_BIG", STATE_BIG_HARVEST);
}

void RetryCloseSmall()
{
   RetryCloseTicket("RetryCloseSmall", "RETRY_CLOSE_SMALL", STATE_BIG_HARVEST);
}

void RetryCloseOldFar()
{
   RetryCloseTicket("RetryCloseOldFar", "RETRY_CLOSE_OLD_FAR", STATE_SMALL_SCENARIO);
}

void RetryCloseBigPart()
{
   RetryCloseTicket("RetryCloseBigPart", "RETRY_CLOSE_BIG_PART", STATE_SMALL_SCENARIO);
}

void RetryCloseNewFar()
{
   RetryCloseTicket("RetryCloseNewFar", "RETRY_CLOSE_NEW_FAR", STATE_CLOSED_PROFIT);
}

void RetryReverseLimitClose()
{
   RetryCloseTicket("RetryReverseLimitClose", "STOP_REVERSE_LIMIT_CLOSE_NEW_FAR", STATE_REVERSE_LIMIT_CLOSED);
}

void ProcessRecoveryPending()
{
   LogInfo("PROCESS_RECOVERY_PENDING: reconciling saved GlobalVariables with real open positions");
   if(RecoverState())
   {
      if(State == STATE_RECOVERY_PENDING)
      {
         LogManagedPositionsForRecovery();
         if(CountManagedOpenPositions() == 0)
            SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "recovery pending but no managed positions found");
      }
      return;
   }

   SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "RecoverState failed in recovery pending");
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
   double bigClosePrice = ExitPriceForDirection(Ctx.bigDirection);
   double smallClosePrice = ExitPriceForDirection(Ctx.smallDirection);
   double actualBigMovePoints = CalcMovePointsBetween(Ctx.bigOpenPrice, bigClosePrice);
   Ctx.currentBigMovePoints = actualBigMovePoints;
   Ctx.cumulativeBigMovePoints += actualBigMovePoints;
   Ctx.currentClosePrice = bigClosePrice;
   Ctx.effectiveFarDistancePoints = CalcEffectiveFarDistancePoints(
      Ctx.initialFarDistancePoints,
      Ctx.currentBigMovePoints,
      Ctx.cumulativeBigMovePoints,
      Ctx.currentClosePrice,
      Ctx.farOpenPrice
   );
   double profitBig = CalcSignedPositionPL(Ctx.bigDirection, Ctx.bigLot, Ctx.bigOpenPrice, bigClosePrice);
   double lossSmall = -CalcSignedPositionPL(Ctx.smallDirection, Ctx.smallLot, Ctx.smallOpenPrice, smallClosePrice);
   double costs = 0.0;
   double totalReserveBefore = Ctx.totalReserve;
   RecalculateRealCycleStatsFromHistory();
   double realCycleBeforeBigHarvest = Ctx.realCyclePL;
   double netProfit = profitBig - lossSmall - costs;
   double closeFarBudget = CalcCloseFarBudget(netProfit);
   double reserveAdd = CalcReserveAdd(netProfit);
   double closeFarLotRaw = CalcCloseFarLotRaw(closeFarBudget, Ctx.effectiveFarDistancePoints);
   double closeFarLotRounded = CalcCloseFarLotRounded(closeFarLotRaw, Ctx.farLot);
   double closeFarLotFinal = closeFarLotRounded;

   if(!ClosePositionByTicket(Ctx.bigTicket, Ctx.bigLot))
   {
      SetRetryContext(STATE_CLOSE_BIG_PENDING, Ctx.bigTicket, Ctx.bigLot, "failed to close Big 100% in Big-harvest; retry pending");
      return;
   }

   if(!ClosePositionByTicket(Ctx.smallTicket, Ctx.smallLot))
   {
      SetRetryContext(STATE_CLOSE_SMALL_PENDING, Ctx.smallTicket, Ctx.smallLot, "failed to close Small 100% in Big-harvest; retry pending");
      return;
   }

   RecalculateRealCycleStatsFromHistory();
   double realBigHarvestNet = Ctx.realCyclePL - realCycleBeforeBigHarvest;
   if(IsInternalSimulationMode())
      realBigHarvestNet = Ctx.realCyclePL - realCycleBeforeBigHarvest;

   if(realBigHarvestNet > 0.0)
   {
      closeFarBudget = realBigHarvestNet * WorkCloseFarShare;
      reserveAdd = realBigHarvestNet * WorkReserveShare;
   }
   else
   {
      closeFarBudget = 0.0;
      reserveAdd = 0.0;
   }
   closeFarLotRaw = CalcCloseFarLotRaw(closeFarBudget, Ctx.effectiveFarDistancePoints);
   closeFarLotRounded = CalcCloseFarLotRounded(closeFarLotRaw, Ctx.farLot);
   closeFarLotFinal = closeFarLotRounded;
   LogInfo(StringFormat("BIG_HARVEST_REAL_RESERVE HistorySelect HistoryDealGetDouble DEAL_POSITION_ID RealBigHarvestNet=%.2f ReserveAdd=%.2f CloseFarBudget=%.2f ProjectedBigProfit=%.2f ProjectedSmallLoss=%.2f ProjectedNet=%.2f", realBigHarvestNet, reserveAdd, closeFarBudget, profitBig, lossSmall, netProfit));

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
         SetRetryContext(STATE_CLOSE_NEW_FAR_PENDING, Ctx.farTicket, closeFarLotFinal, "failed to close Far by real money budget; retry pending");
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
      (int)MathRound(actualBigMovePoints),
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
   double closeBigLotRounded = CalcCloseBigLotOnSmall(bigLot);
   double plannedRemainBigLot = CalcRemainBigLotOnSmall(bigLot);
   double remainBigLot = plannedRemainBigLot;
   double closedBigPL = CalcSignedPositionPL(bigDirection, closeBigLotRounded, bigOpenPrice, currentPrice);
   double costs = 0.0;
   double totalReserveBefore = Ctx.totalReserve;
   double smallScenarioTotalPL = smallPL + oldFarPL + closedBigPL - costs;

   double newFarLot = remainBigLot;
   Direction newFarDirection = bigDirection;
   double newFarOpenPrice = bigOpenPrice;
   double newFarDistancePoints = CalcRealPriceFarDistancePoints(currentPrice, newFarOpenPrice);
   double newBigLot = CalcBigLot(newFarLot);
   double newSmallLot = CalcSmallLot(newBigLot);
   double expectedNextReserve = CalcExpectedNextReserve(newBigLot, newSmallLot, Ctx.harvestLevel + 1);
   double expectedNextFarLoss = CalcFarRemainLoss(newFarLot, newFarDistancePoints);
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
      HandleInvalidGeometry(geometryInvalidReason);
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
      SetRetryContext(STATE_CLOSE_SMALL_PENDING, smallTicket, smallLot, "failed to close Small 100% at old Far touch; retry pending");
      return;
   }

   if(!ClosePositionByTicket(oldFarTicket, oldFarLot))
   {
      SetRetryContext(STATE_CLOSE_OLD_FAR_PENDING, oldFarTicket, oldFarLot, "failed to close old Far 100% at Small-at-Far; retry pending");
      return;
   }

   if(closeBigLotRounded > 0.0)
   {
      if(!ClosePositionByTicket(bigTicket, closeBigLotRounded))
      {
         SetRetryContext(STATE_CLOSE_BIG_PART_PENDING, bigTicket, closeBigLotRounded, "failed to close Big by CloseBigOnSmall at Small-at-Far; retry pending");
         return;
      }
   }

   double smallScenarioRealNet = smallScenarioTotalPL;
   RecalculateRealCycleStatsFromHistory();
   if(Ctx.realCyclePL != 0.0)
      smallScenarioRealNet = Ctx.realCyclePL - totalReserveBefore;
   double smallReserveAdd = CalcSmallReserveAdd(smallScenarioRealNet);
   Ctx.totalReserve += smallReserveAdd;
   LogInfo(StringFormat("SMALL_RESERVE_ADD SmallScenarioRealNet=%.2f SmallReserveShare=%.4f SmallReserveAdd=%.2f TotalReserve=%.2f", smallScenarioRealNet, WorkSmallReserveShare, smallReserveAdd, Ctx.totalReserve));

   Ctx.reverseCycleCount += 1;
   Ctx.reverseLimitReached = Ctx.reverseCycleCount > WorkMaxReverseCycles;
   if(Ctx.reverseLimitReached && StopOnReverseLimit)
      actionAfterValidation = "STOP_REVERSE_LIMIT";

   Ctx.farTicket = bigTicket;
   Ctx.farLot = newFarLot;
   Ctx.farOpenPrice = newFarOpenPrice;
   Ctx.farDirection = newFarDirection;
   Ctx.initialFarDistancePoints = newFarDistancePoints;
   Ctx.currentBigMovePoints = 0.0;
   Ctx.cumulativeBigMovePoints = 0.0;
   Ctx.effectiveFarDistancePoints = newFarDistancePoints;
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
   LogInfo(StringFormat(
      "SMALL_AT_FAR_NEW_FAR_CHECK bigOpenPrice=%.5f currentPrice=%.5f farOpenPrice=%.5f effectiveFarDistancePoints=%.1f expectedNextFarLoss=%.2f farRemainLoss=%.2f totalReserve=%.2f finalCloseAllowed=%s farOpenEqualsBigOpen=%s",
      bigOpenPrice,
      currentPrice,
      Ctx.farOpenPrice,
      Ctx.effectiveFarDistancePoints,
      expectedNextFarLoss,
      farRemainLoss,
      Ctx.totalReserve,
      Ctx.finalCloseAllowed ? "YES" : "NO",
      MathAbs(Ctx.farOpenPrice - bigOpenPrice) <= SymbolInfoDouble(_Symbol, SYMBOL_POINT) * 0.1 ? "YES" : "NO"
   ));
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
      MarkSystemClose("STOP_REVERSE_LIMIT_CLOSE_NEW_FAR");
      if(Ctx.farLot > 0.0 && Ctx.farTicket != 0 && ClosePositionByTicketWithComment(Ctx.farTicket, Ctx.farLot, "STOP_REVERSE_LIMIT_CLOSE_NEW_FAR"))
      {
         Ctx.farTicket = 0;
         Ctx.farLot = 0.0;
         SetState(STATE_REVERSE_LIMIT_CLOSED, "reverse limit reached; NewFar closed");
      }
      else
         SetRetryContext(STATE_REVERSE_LIMIT_CLOSE_PENDING, Ctx.farTicket, Ctx.farLot, "reverse limit reached; NewFar close pending");
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
         SetRetryContext(STATE_CLOSE_NEW_FAR_PENDING, Ctx.farTicket, Ctx.farLot, "failed to close NewFar after Small-at-Far FinalCloseAllowed; retry pending");
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
      SetRetryContext(STATE_CLOSE_NEW_FAR_PENDING, Ctx.farTicket, Ctx.farLot, "failed to close Far during FinalClose; retry pending");
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
      case STATE_REVERSE_LIMIT_CLOSED:
      case STATE_INVALID_GEOMETRY_CLOSED:
      case STATE_MANUAL_INTERVENTION_REQUIRED:
      case STATE_OPEN_NEW_BIG_PENDING:
      case STATE_OPEN_NEW_SMALL_PENDING:
      case STATE_STOP:
      case STATE_ERROR:
         break;

      case STATE_REVERSE_LIMIT_CLOSE_PENDING:
         RetryReverseLimitClose();
         break;

      case STATE_RECOVERY_PENDING:
         ProcessRecoveryPending();
         break;

      case STATE_CLOSE_BIG_PENDING:
         RetryCloseBig();
         break;

      case STATE_CLOSE_SMALL_PENDING:
         RetryCloseSmall();
         break;

      case STATE_CLOSE_OLD_FAR_PENDING:
         RetryCloseOldFar();
         break;

      case STATE_CLOSE_BIG_PART_PENDING:
         RetryCloseBigPart();
         break;

      case STATE_CLOSE_NEW_FAR_PENDING:
         RetryCloseNewFar();
         break;

      default:
         SetState(STATE_ERROR, "unknown state");
         break;
   }
}

#endif // __BH_STATEMACHINE_MQH__
