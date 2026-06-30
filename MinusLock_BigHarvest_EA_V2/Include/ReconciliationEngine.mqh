#ifndef __BH_RECONCILIATIONENGINE_MQH__
#define __BH_RECONCILIATIONENGINE_MQH__

datetime LastReconciliationTime = 0;
datetime LastRepeatWarningLogTime = 0;
int ReconciliationSuppressedRepeatWarnings = 0;

void LogReconciliationRepeatWarning(string message)
{
   datetime now = TimeCurrent();
   int interval = RetryLogIntervalSeconds > 0 ? RetryLogIntervalSeconds : RiskGateLogIntervalSeconds;
   if(interval <= 0)
      interval = 30;

   if(LastRepeatWarningLogTime == 0 || now - LastRepeatWarningLogTime >= interval)
   {
      if(ReconciliationSuppressedRepeatWarnings > 0)
         LogInfo(StringFormat("[Reconciliation] %s; suppressed %d repeated messages", message, ReconciliationSuppressedRepeatWarnings));
      else
         LogInfo("[Reconciliation] " + message);
      ReconciliationSuppressedRepeatWarnings = 0;
      LastRepeatWarningLogTime = now;
   }
   else
      ReconciliationSuppressedRepeatWarnings++;
}


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
         if(dealTicket == 0)
            continue;
         if((ulong)HistoryDealGetInteger(dealTicket, DEAL_MAGIC) != MagicNumber)
            continue;
         if(HistoryDealGetString(dealTicket, DEAL_SYMBOL) != _Symbol)
            continue;
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


bool IsManagedPositionKnownToContext(ulong ticket, ulong identifier)
{
   if(ticket != 0)
   {
      if(ticket == Ctx.farTicket || ticket == Ctx.bigTicket || ticket == Ctx.smallTicket ||
         ticket == Ctx.initialBuyTicket || ticket == Ctx.initialSellTicket)
         return true;
      if(ticket == Ctx.pendingTicket || ticket == Ctx.retryTicket)
         return true;
   }

   if(identifier != 0)
   {
      if(identifier == Ctx.farIdentifier || identifier == Ctx.bigIdentifier || identifier == Ctx.smallIdentifier ||
         identifier == Ctx.initialBuyIdentifier || identifier == Ctx.initialSellIdentifier)
         return true;
   }

   return false;
}

string ClassifyOrphanManagedPosition(ulong ticket, ulong identifier, string comment)
{
   if(ticket == Ctx.pendingTicket)
      return "ORPHAN_PENDING";
   if(ticket == Ctx.retryTicket)
      return "ORPHAN_RETRY";
   if(StringFind(comment, "FAR") >= 0 || StringFind(comment, "Far") >= 0)
      return "ORPHAN_FAR";
   if(StringFind(comment, "BIG") >= 0 || StringFind(comment, "Big") >= 0)
      return "ORPHAN_BIG";
   if(StringFind(comment, "SMALL") >= 0 || StringFind(comment, "Small") >= 0)
      return "ORPHAN_SMALL";
   if(identifier == Ctx.farIdentifier)
      return "ORPHAN_FAR";
   if(identifier == Ctx.bigIdentifier)
      return "ORPHAN_BIG";
   if(identifier == Ctx.smallIdentifier)
      return "ORPHAN_SMALL";
   return "ORPHAN_MANAGED_POSITION";
}


bool ValidateInitialLockLeg(string legName, ulong &ticket, ulong &identifier, double &lot, double &openPrice, string comment, Direction expectedDirection)
{
   PositionSnapshot snapshot;
   bool found = GetManagedPositionByTicket(ticket, snapshot);
   if(!found)
      found = GetManagedPositionByComment(comment, snapshot);

   if(!found)
   {
      LogError(StringFormat("INITIAL_LOCK_TICKET_MISMATCH Leg=%s Ticket=%I64u Comment=%s", legName, ticket, comment));
      return false;
   }

   if(expectedDirection != DIR_NONE && snapshot.direction != expectedDirection)
   {
      LogError(StringFormat("INITIAL_LOCK_STATE_INVALID Leg=%s Direction=%s Expected=%s", legName, DirectionToString(snapshot.direction), DirectionToString(expectedDirection)));
      return false;
   }

   if(identifier != 0 && snapshot.identifier != identifier)
   {
      LogError(StringFormat("INITIAL_LOCK_IDENTIFIER_MISMATCH Leg=%s SavedIdentifier=%I64u ActualIdentifier=%I64u Ticket=%I64u", legName, identifier, snapshot.identifier, snapshot.ticket));
      return false;
   }

   double actualVolume = GetActualPositionVolume(snapshot.ticket);
   if(actualVolume <= 0.0)
      actualVolume = snapshot.lot;
   if(MathAbs(NormalizeVolumeToStep(lot) - NormalizeVolumeToStep(actualVolume)) > VolumeMismatchToleranceLots)
   {
      LogError(StringFormat("INITIAL_LOCK_STATE_INVALID Leg=%s SavedVolume=%.2f ActualVolume=%.2f", legName, lot, actualVolume));
      return false;
   }

   ticket = snapshot.ticket;
   identifier = snapshot.identifier;
   lot = NormalizeVolumeToStep(actualVolume);
   openPrice = snapshot.openPrice;
   LogInfo(StringFormat("INITIAL_LOCK_STATE_VALID Leg=%s Ticket=%I64u Identifier=%I64u Lot=%.2f OpenPrice=%.5f", legName, ticket, identifier, lot, openPrice));
   return true;
}

bool ValidateInitialLockIntegrity()
{
   bool hasInitialContext = (Ctx.initialBuyTicket != 0 || Ctx.initialSellTicket != 0 ||
                             Ctx.initialBuyIdentifier != 0 || Ctx.initialSellIdentifier != 0 ||
                             Ctx.initialBuyLot > VolumeMismatchToleranceLots || Ctx.initialSellLot > VolumeMismatchToleranceLots ||
                             State == STATE_INITIAL_LOCK_OPENED);
   if(!hasInitialContext)
      return true;

   bool ok = true;
   ok = ValidateInitialLockLeg("INITIAL_BUY", Ctx.initialBuyTicket, Ctx.initialBuyIdentifier, Ctx.initialBuyLot, Ctx.initialBuyOpenPrice, "MinusLock_INITIAL_BUY", DIR_BUY) && ok;
   ok = ValidateInitialLockLeg("INITIAL_SELL", Ctx.initialSellTicket, Ctx.initialSellIdentifier, Ctx.initialSellLot, Ctx.initialSellOpenPrice, "MinusLock_INITIAL_SELL", DIR_SELL) && ok;

   if(ok)
   {
      Ctx.initialLockRecovered = true;
      LogInfo(StringFormat("INITIAL_LOCK_RECOVERED BuyTicket=%I64u SellTicket=%I64u", Ctx.initialBuyTicket, Ctx.initialSellTicket));
      SaveState();
   }
   else
      SetState(STATE_RECOVERY_MISMATCH, "INITIAL_LOCK_STATE_INVALID");

   return ok;
}

bool ValidateStatePositionConsistency()
{
   if(State == STATE_INITIAL_LOCK_OPENED)
   {
      bool valid = (HasInitialBuyContext() && HasInitialSellContext() &&
                    !HasFarContext() && !HasBigContext() && !HasSmallContext());
      if(!valid)
      {
         LogError(StringFormat("INITIAL_LOCK_STATE_INVALID State=%s InitialBuyTicket=%I64u InitialSellTicket=%I64u FarTicket=%I64u BigTicket=%I64u SmallTicket=%I64u", StateToString(State), Ctx.initialBuyTicket, Ctx.initialSellTicket, Ctx.farTicket, Ctx.bigTicket, Ctx.smallTicket));
         SetState(STATE_RECOVERY_MISMATCH, "INITIAL_LOCK_STATE_INVALID");
         return false;
      }
      LogInfo("INITIAL_LOCK_STATE_VALID State=STATE_INITIAL_LOCK_OPENED");
      return ValidateInitialLockIntegrity();
   }

   if(State == STATE_FAR_ACTIVE)
   {
      if(HasInitialBuyContext() || HasInitialSellContext() || !HasFarContext() || HasBigContext() || HasSmallContext())
      {
         LogError(StringFormat("INITIAL_LOCK_STATE_INVALID State=%s InitialBuyTicket=%I64u InitialSellTicket=%I64u FarTicket=%I64u BigTicket=%I64u SmallTicket=%I64u", StateToString(State), Ctx.initialBuyTicket, Ctx.initialSellTicket, Ctx.farTicket, Ctx.bigTicket, Ctx.smallTicket));
         SetState(STATE_RECOVERY_MISMATCH, "STATE_FAR_ACTIVE position consistency invalid");
         return false;
      }
      return true;
   }

   if(State == STATE_BIG_SMALL_OPENED || State == STATE_BIG_HARVEST || State == STATE_SMALL_SCENARIO || State == STATE_WAIT_SMALL_TO_FAR)
   {
      if(HasInitialBuyContext() || HasInitialSellContext() || !HasFarContext() || !HasBigContext() || !HasSmallContext())
      {
         LogError(StringFormat("INITIAL_LOCK_STATE_INVALID State=%s InitialBuyTicket=%I64u InitialSellTicket=%I64u FarTicket=%I64u BigTicket=%I64u SmallTicket=%I64u", StateToString(State), Ctx.initialBuyTicket, Ctx.initialSellTicket, Ctx.farTicket, Ctx.bigTicket, Ctx.smallTicket));
         SetState(STATE_RECOVERY_MISMATCH, "Big/Small state position consistency invalid");
         return false;
      }
   }

   return true;
}

bool ValidateNoOrphanManagedPositions()
{
   bool ok = true;

   if(IsInternalSimulationMode())
   {
      for(int i = 0; i < ArraySize(SimPositions); i++)
      {
         if(!SimPositions[i].exists || SimPositions[i].lot <= VolumeMismatchToleranceLots)
            continue;

         ulong ticket = SimPositions[i].ticket;
         ulong identifier = SimPositions[i].identifier;
         if(IsManagedPositionKnownToContext(ticket, identifier))
            continue;

         string orphanType = ClassifyOrphanManagedPosition(ticket, identifier, SimPositions[i].comment);
         LogError(StringFormat("ORPHAN_MANAGED_POSITION DETECTED Type=%s Ticket=%I64u Identifier=%I64u Volume=%.2f Direction=%s Comment=%s", orphanType, ticket, identifier, SimPositions[i].lot, DirectionToString(SimPositions[i].direction), SimPositions[i].comment));
         ok = false;
      }
   }
   else
   {
      for(int i = PositionsTotal() - 1; i >= 0; i--)
      {
         ulong ticket = PositionGetTicket(i);
         if(ticket == 0 || !PositionSelectByTicket(ticket))
            continue;

         if(PositionGetString(POSITION_SYMBOL) != _Symbol)
            continue;
         if((ulong)PositionGetInteger(POSITION_MAGIC) != MagicNumber)
            continue;

         ulong identifier = (ulong)PositionGetInteger(POSITION_IDENTIFIER);
         double volume = NormalizeVolumeToStep(PositionGetDouble(POSITION_VOLUME));
         Direction direction = PositionTypeToDirection(PositionGetInteger(POSITION_TYPE));
         string comment = PositionGetString(POSITION_COMMENT);

         if(volume <= VolumeMismatchToleranceLots)
            continue;
         if(IsManagedPositionKnownToContext(ticket, identifier))
            continue;

         string orphanType = ClassifyOrphanManagedPosition(ticket, identifier, comment);
         LogError(StringFormat("ORPHAN_MANAGED_POSITION DETECTED Type=%s Ticket=%I64u Identifier=%I64u Volume=%.2f Direction=%s Comment=%s", orphanType, ticket, identifier, volume, DirectionToString(direction), comment));
         ok = false;
      }
   }

   if(!ok)
      SetState(STATE_RECOVERY_MISMATCH, "ORPHAN_MANAGED_POSITION detected by ValidateNoOrphanManagedPositions");

   return ok;
}

bool RunReconciliation()
{
   bool ok = true;
   LogReconciliationContextSummary("RunReconciliation");
   if(!HasKnownContext() && CountManagedOpenPositions() > 0)
   {
      LogError(StringFormat("CONTEXT_CLEARED_WITH_LIVE_POSITION State=%s ManagedPositions=%d", StateToString(State), CountManagedOpenPositions()));
      ok = false;
   }
   ok = ValidateInitialLockIntegrity() && ok;
   if(TryRecoverPromotedBigAsFar("RunReconciliation"))
      ok = true;
   ok = ValidateStatePositionConsistency() && ok;
   ok = ValidateCurrentStateIntegrity() && ok;
   ok = ValidatePositionResolutionContext() && ok;
   ok = ValidateNoOrphanManagedPositions() && ok;
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
      if(State != STATE_INTEGRITY_ERROR && State != STATE_POSITION_RESOLUTION_ERROR)
      {
         State = STATE_RECOVERY_MISMATCH;
         Ctx.lastError = "RECONCILIATION FAIL";
         LogError("RECONCILIATION FAIL -> STATE_RECOVERY_MISMATCH");
      }
      else
      {
         Ctx.lastError = "STATE_INTEGRITY_FAIL";
         LogError("RECONCILIATION FAIL -> STATE_INTEGRITY_ERROR");
      }
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
      LogReconciliationRepeatWarning("STATE_RECOVERY_MISMATCH still active");
      return;
   }

   if(State == STATE_INTEGRITY_ERROR)
   {
      if(TryRecoverPromotedBigAsFar("AutoRecover STATE_INTEGRITY_ERROR"))
      {
         LogInfo("STATE_INTEGRITY_ERROR recovered by promoted Big-as-Far reconstruction");
      }
      else
      {
         LogReconciliationRepeatWarning("STATE_INTEGRITY_ERROR still active");
         return;
      }
   }

   if(State == STATE_POSITION_RESOLUTION_ERROR)
   {
      if(TryRecoverPromotedBigAsFar("AutoRecover STATE_POSITION_RESOLUTION_ERROR"))
      {
         LogInfo("STATE_POSITION_RESOLUTION_ERROR recovered by promoted Big-as-Far reconstruction");
      }
      else
      {
         LogReconciliationRepeatWarning("STATE_POSITION_RESOLUTION_ERROR still active");
         return;
      }
   }

   if(ReconciliationIntervalSeconds <= 0)
      return;

   datetime now = TimeCurrent();
   if(LastReconciliationTime != 0 && now - LastReconciliationTime < ReconciliationIntervalSeconds)
      return;

   LastReconciliationTime = now;
   if(RunReconciliation())
   {
      ValidateNoOrphanManagedPositions();
      ValidateCurrentStateIntegrity();
   }
}

#endif // __BH_RECONCILIATIONENGINE_MQH__
