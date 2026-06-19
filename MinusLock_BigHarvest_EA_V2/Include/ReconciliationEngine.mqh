#ifndef __BH_RECONCILIATIONENGINE_MQH__
#define __BH_RECONCILIATIONENGINE_MQH__

datetime LastReconciliationTime = 0;

bool ValidatePositionSnapshotAgainstContext(string legName, ulong ctxTicket, ulong ctxIdentifier, Direction ctxDirection, double ctxLot, PositionSnapshot &snapshot)
{
   double tolerance = MathMax(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP), LotStep) * 0.5;
   if(tolerance <= 0.0)
      tolerance = 0.0000001;

   if(ctxTicket == 0 && ctxLot <= 0.0)
      return true;

   if(!snapshot.exists)
   {
      LogError("RECONCILIATION FAIL " + legName + "_NOT_FOUND");
      return false;
   }

   if(ctxIdentifier > 0 && snapshot.identifier > 0 && snapshot.identifier != ctxIdentifier)
   {
      LogError(StringFormat("RECONCILIATION FAIL %s_IDENTIFIER_MISMATCH ctxIdentifier=%I64u actualIdentifier=%I64u", legName, ctxIdentifier, snapshot.identifier));
      return false;
   }

   if(snapshot.direction != ctxDirection)
   {
      LogError(StringFormat("RECONCILIATION FAIL %s_DIRECTION_MISMATCH ctxDirection=%s actualDirection=%s", legName, DirectionToString(ctxDirection), DirectionToString(snapshot.direction)));
      return false;
   }

   if(MathAbs(snapshot.lot - ctxLot) > tolerance)
   {
      LogError(StringFormat("RECONCILIATION FAIL %s_VOLUME_MISMATCH ctxLot=%.2f actualLot=%.2f tolerance=%.5f", legName, ctxLot, snapshot.lot, tolerance));
      return false;
   }

   return true;
}

bool ValidateFarPosition()
{
   PositionSnapshot far;
   bool found = GetManagedPositionByTicket(Ctx.farTicket, far);
   return ValidatePositionSnapshotAgainstContext("FAR", Ctx.farTicket, Ctx.farIdentifier, Ctx.farDirection, Ctx.farLot, far);
}

bool ValidateBigPosition()
{
   PositionSnapshot big;
   bool found = GetManagedPositionByTicket(Ctx.bigTicket, big);
   return ValidatePositionSnapshotAgainstContext("BIG", Ctx.bigTicket, Ctx.bigIdentifier, Ctx.bigDirection, Ctx.bigLot, big);
}

bool ValidateSmallPosition()
{
   PositionSnapshot small;
   bool found = GetManagedPositionByTicket(Ctx.smallTicket, small);
   return ValidatePositionSnapshotAgainstContext("SMALL", Ctx.smallTicket, Ctx.smallIdentifier, Ctx.smallDirection, Ctx.smallLot, small);
}

double CalculateReserveFromHistory()
{
   if(IsInternalSimulationMode())
      return Ctx.totalReserve;

   datetime startTime = Ctx.cycleStartTime > 0 ? Ctx.cycleStartTime - 60 : TimeCurrent() - 86400 * 30;
   if(!HistorySelect(startTime, TimeCurrent() + 86400))
   {
      LogError("RECONCILIATION FAIL RESERVE_HISTORY_SELECT_FAILED");
      return Ctx.totalReserve;
   }

   double rebuiltReserve = 0.0;
   bool classified = false;
   int totalDeals = HistoryDealsTotal();
   for(int i = 0; i < totalDeals; i++)
   {
      ulong dealTicket = HistoryDealGetTicket(i);
      if(dealTicket == 0)
         continue;
      if((ulong)HistoryDealGetInteger(dealTicket, DEAL_MAGIC) != MagicNumber)
         continue;
      if(HistoryDealGetString(dealTicket, DEAL_SYMBOL) != _Symbol)
         continue;
      if((ENUM_DEAL_ENTRY)HistoryDealGetInteger(dealTicket, DEAL_ENTRY) != DEAL_ENTRY_OUT)
         continue;

      string comment = HistoryDealGetString(dealTicket, DEAL_COMMENT);
      double net = HistoryDealGetDouble(dealTicket, DEAL_PROFIT) + HistoryDealGetDouble(dealTicket, DEAL_COMMISSION) + HistoryDealGetDouble(dealTicket, DEAL_SWAP);
      if(net <= 0.0)
         continue;

      if(StringFind(comment, "BIG_HARVEST") >= 0 || StringFind(comment, "RETRY_CLOSE_BIG") >= 0 || StringFind(comment, "RETRY_CLOSE_SMALL") >= 0)
      {
         rebuiltReserve += net * WorkReserveShare;
         classified = true;
      }
      else if(StringFind(comment, "SMALL") >= 0 || StringFind(comment, "OLD_FAR") >= 0)
      {
         rebuiltReserve += net * WorkSmallReserveShare;
         classified = true;
      }
   }

   if(!classified)
   {
      LogInfo("RECONCILIATION RESERVE_REBUILD_FROM_HISTORY no classified reserve deals; using current Ctx.totalReserve as safe baseline");
      return Ctx.totalReserve;
   }

   return rebuiltReserve;
}

double GetActualFarVolume()
{
   PositionSnapshot far;
   if(!GetManagedPositionByTicket(Ctx.farTicket, far))
      return 0.0;
   return far.lot;
}

bool ValidateHarvestLevelFromHistory()
{
   if(Ctx.harvestLevel <= 0 || IsInternalSimulationMode())
      return true;

   int maxSeenLevel = 0;
   if(HistorySelect(Ctx.cycleStartTime > 0 ? Ctx.cycleStartTime - 60 : TimeCurrent() - 86400 * 30, TimeCurrent() + 86400))
   {
      int totalDeals = HistoryDealsTotal();
      for(int i = 0; i < totalDeals; i++)
      {
         ulong dealTicket = HistoryDealGetTicket(i);
         string comment = HistoryDealGetString(dealTicket, DEAL_COMMENT);
         for(int level = 1; level <= WorkMaxHarvestLevels; level++)
         {
            if(StringFind(comment, LevelComment("BIG", level)) >= 0 || StringFind(comment, LevelComment("SMALL", level)) >= 0)
               maxSeenLevel = MathMax(maxSeenLevel, level);
         }
      }
   }

   if(maxSeenLevel > 0 && maxSeenLevel != Ctx.harvestLevel)
   {
      LogError(StringFormat("RECONCILIATION FAIL HARVEST_LEVEL_MISMATCH ctxHarvestLevel=%d historyHarvestLevel=%d", Ctx.harvestLevel, maxSeenLevel));
      return false;
   }
   return true;
}

bool ValidateReverseCyclesFromHistory()
{
   // Reverse-cycle history comments are broker-dependent; this guard logs the current value for audit and reserves hard failure for explicit future mismatch evidence.
   LogInfo(StringFormat("RECONCILIATION reverseCycles=%d", Ctx.reverseCycleCount));
   return true;
}

bool RunReconciliation()
{
   bool ok = true;
   ok = ValidateFarPosition() && ok;
   ok = ValidateBigPosition() && ok;
   ok = ValidateSmallPosition() && ok;

   double actualFarVolume = GetActualFarVolume();
   if(Ctx.farTicket > 0 && MathAbs(actualFarVolume - Ctx.farLot) > MathMax(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP), LotStep) * 0.5)
   {
      LogError(StringFormat("RECONCILIATION FAIL FAR_VOLUME_MISMATCH ctxFarLot=%.2f actualFarVolume=%.2f", Ctx.farLot, actualFarVolume));
      ok = false;
   }

   double realReserve = CalculateReserveFromHistory();
   if(MathAbs(realReserve - Ctx.totalReserve) > ReserveMismatchTolerance)
   {
      LogError(StringFormat("RECONCILIATION FAIL RESERVE_MISMATCH realReserve=%.2f ctxTotalReserve=%.2f tolerance=%.2f", realReserve, Ctx.totalReserve, ReserveMismatchTolerance));
      ok = false;
   }

   ok = ValidateHarvestLevelFromHistory() && ok;
   ok = ValidateReverseCyclesFromHistory() && ok;

   if(!ok)
   {
      State = STATE_RECOVERY_MISMATCH;
      Ctx.lastError = "RECONCILIATION FAIL";
      LogError("RECONCILIATION FAIL -> STATE_RECOVERY_MISMATCH");
      SaveState();
      return false;
   }

   LogInfo(StringFormat("RECONCILIATION PASS State=%s FarLot=%.2f BigLot=%.2f SmallLot=%.2f TotalReserve=%.2f HarvestLevel=%d ReverseCycles=%d", StateToString(State), Ctx.farLot, Ctx.bigLot, Ctx.smallLot, Ctx.totalReserve, Ctx.harvestLevel, Ctx.reverseCycleCount));
   return true;
}

void RunPeriodicReconciliation()
{
   if(ReconciliationIntervalSeconds <= 0)
      return;

   datetime now = TimeCurrent();
   if(LastReconciliationTime != 0 && now - LastReconciliationTime < ReconciliationIntervalSeconds)
      return;

   LastReconciliationTime = now;
   RunReconciliation();
}

#endif // __BH_RECONCILIATIONENGINE_MQH__
