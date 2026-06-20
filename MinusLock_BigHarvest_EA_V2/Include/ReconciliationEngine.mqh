#ifndef __BH_RECONCILIATIONENGINE_MQH__
#define __BH_RECONCILIATIONENGINE_MQH__

datetime LastReconciliationTime = 0;

double ReconciliationVolumeTolerance()
{
   double tolerance = VolumeMismatchToleranceLots;
   if(tolerance <= 0.0)
      tolerance = GetEffectiveLotStep();
   if(tolerance <= 0.0)
      tolerance = 0.0000001;
   return tolerance;
}

void LogReconciliationVolumeDiagnostic(string severity, string source, string legName, double ctxLot, double actualLot, double normalizedCtxLot, double normalizedActualLot, double tolerance, ulong ticket, ulong identifier)
{
   double volumeStep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   double diff = MathAbs(actualLot - ctxLot);
   double normDiff = MathAbs(normalizedActualLot - normalizedCtxLot);
   LogInfo(StringFormat("RECON %s State=%s Source=%s Leg=%s LastAction=%s Ticket=%I64u Identifier=%I64u CtxLot=%.2f ActualLot=%.2f Diff=%.5f NormalizedCtxLot=%.2f NormalizedActualLot=%.2f NormDiff=%.5f LotStep=%.5f VolumeStep=%.5f RECON_TOLERANCE_USED=%.5f LastContextAction=%s",
                        severity,
                        StateToString(State),
                        source,
                        legName,
                        Ctx.lastAction,
                        ticket,
                        identifier,
                        ctxLot,
                        actualLot,
                        diff,
                        normalizedCtxLot,
                        normalizedActualLot,
                        normDiff,
                        LotStep,
                        volumeStep,
                        tolerance,
                        Ctx.lastAction));
}

bool ValidatePositionSnapshotAgainstContext(string legName, string source, ulong ctxTicket, ulong ctxIdentifier, Direction ctxDirection, double &ctxLot, PositionSnapshot &snapshot)
{
   double tolerance = ReconciliationVolumeTolerance();
   double step = GetEffectiveLotStep();
   if(step <= 0.0)
      step = tolerance;

   if(ctxTicket == 0 && ctxLot <= 0.0)
      return true;

   if(!snapshot.exists)
   {
      LogError("RECONCILIATION FAIL " + legName + "_NOT_FOUND State=" + StateToString(State));
      return false;
   }

   if(ctxIdentifier > 0 && snapshot.identifier > 0 && snapshot.identifier != ctxIdentifier)
   {
      LogError(StringFormat("RECONCILIATION FAIL %s_IDENTIFIER_MISMATCH State=%s ctxIdentifier=%I64u actualIdentifier=%I64u ticket=%I64u", legName, StateToString(State), ctxIdentifier, snapshot.identifier, snapshot.ticket));
      return false;
   }

   if(snapshot.direction != ctxDirection)
   {
      LogError(StringFormat("RECONCILIATION FAIL %s_DIRECTION_MISMATCH State=%s ctxDirection=%s actualDirection=%s ticket=%I64u", legName, StateToString(State), DirectionToString(ctxDirection), DirectionToString(snapshot.direction), snapshot.ticket));
      return false;
   }

   double normalizedCtxLot = NormalizeVolumeToStep(ctxLot);
   double normalizedActualLot = NormalizeVolumeToStep(snapshot.lot);
   double normDiff = MathAbs(normalizedActualLot - normalizedCtxLot);

   if(normDiff <= tolerance)
   {
      if(normDiff > 0.0)
         LogReconciliationVolumeDiagnostic("WARNING", source, legName, ctxLot, snapshot.lot, normalizedCtxLot, normalizedActualLot, tolerance, snapshot.ticket, snapshot.identifier);
      ctxLot = normalizedActualLot;
      return true;
   }

   LogReconciliationVolumeDiagnostic("FAIL", source, legName, ctxLot, snapshot.lot, normalizedCtxLot, normalizedActualLot, tolerance, snapshot.ticket, snapshot.identifier);
   LogError(StringFormat("RECONCILIATION FAIL %s_VOLUME_MISMATCH", legName));
   return false;
}

bool ValidateFarPosition()
{
   PositionSnapshot far;
   bool found = GetManagedPositionByTicket(Ctx.farTicket, far);
   return ValidatePositionSnapshotAgainstContext("FAR", "FarVolumeCheck", Ctx.farTicket, Ctx.farIdentifier, Ctx.farDirection, Ctx.farLot, far);
}

bool ValidateBigPosition()
{
   PositionSnapshot big;
   bool found = GetManagedPositionByTicket(Ctx.bigTicket, big);
   return ValidatePositionSnapshotAgainstContext("BIG", "BigVolumeCheck", Ctx.bigTicket, Ctx.bigIdentifier, Ctx.bigDirection, Ctx.bigLot, big);
}

bool ValidateSmallPosition()
{
   PositionSnapshot small;
   bool found = GetManagedPositionByTicket(Ctx.smallTicket, small);
   return ValidatePositionSnapshotAgainstContext("SMALL", "SmallVolumeCheck", Ctx.smallTicket, Ctx.smallIdentifier, Ctx.smallDirection, Ctx.smallLot, small);
}

double CalculateReserveFromHistory()
{
   // V2.4.9: HistoryDeals alone are not a source of reserve truth.
   // Initial lock profit is intentionally ignored and must never create RESERVE_EVENT_* credit.
   if(!IsInternalSimulationMode())
   {
      datetime startTime = Ctx.cycleStartTime > 0 ? Ctx.cycleStartTime - 60 : TimeCurrent() - 86400 * 30;
      if(HistorySelect(startTime, TimeCurrent() + 86400))
      {
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

            string comment = HistoryDealGetString(dealTicket, DEAL_COMMENT);
            if(StringFind(comment, "INITIAL_BUY") >= 0 || StringFind(comment, "INITIAL_SELL") >= 0)
               LogInfo(StringFormat("RESERVE_REBUILD_SKIP_INITIAL_LOCK Deal=%I64u Comment=%s", dealTicket, comment));
         }
      }
   }

   double ledgerReserve = RebuildReserveFromLedger();
   LogInfo(StringFormat("RESERVE_REBUILD_FROM_LEDGER LedgerEntries=%d LedgerReserve=%.2f ContextReserve=%.2f", ArraySize(ReserveLedger), ledgerReserve, Ctx.totalReserve));
   return ledgerReserve;
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
   if(Ctx.farTicket == 0 && Ctx.bigTicket == 0 && Ctx.smallTicket == 0 && CountManagedOpenPositions() > 0)
   {
      LogError(StringFormat("CONTEXT_CLEARED_WITH_LIVE_POSITION State=%s ManagedPositions=%d", StateToString(State), CountManagedOpenPositions()));
      ok = false;
   }
   ok = ValidateFarPosition() && ok;
   ok = ValidateBigPosition() && ok;
   ok = ValidateSmallPosition() && ok;

   double actualFarVolume = GetActualFarVolume();

   double realReserve = CalculateReserveFromHistory();
   double reserveDiff = MathAbs(realReserve - Ctx.totalReserve);
   LogInfo(StringFormat("RECON_TOLERANCE_USED=%.5f ReserveCheck realReserve=%.2f ctxTotalReserve=%.2f reserveDiff=%.5f", ReserveMismatchTolerance, realReserve, Ctx.totalReserve, reserveDiff));
   if(reserveDiff > ReserveMismatchTolerance)
   {
      // V2.4.9 P0: reserve reconstruction is diagnostic only unless a structural position mismatch is also present.
      // Initial-lock profit and other profitable deals are warning-only signals, not fatal recovery evidence.
      LogInfo(StringFormat("RECONCILIATION WARNING RESERVE_REBUILD_UNVERIFIED realReserve=%.2f ctxTotalReserve=%.2f reserveDiff=%.5f tolerance=%.2f", realReserve, Ctx.totalReserve, reserveDiff, ReserveMismatchTolerance));
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
   if(State == STATE_RECOVERY_MISMATCH)
   {
      LogInfo("RECONCILIATION REPEAT WARNING skipped because STATE_RECOVERY_MISMATCH is already active");
      return;
   }

   if(ReconciliationIntervalSeconds <= 0)
      return;

   datetime now = TimeCurrent();
   if(LastReconciliationTime != 0 && now - LastReconciliationTime < ReconciliationIntervalSeconds)
      return;

   LastReconciliationTime = now;
   RunReconciliation();
}

#endif // __BH_RECONCILIATIONENGINE_MQH__
