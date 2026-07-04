#ifndef __BH_STATEMACHINE_MQH__
#define __BH_STATEMACHINE_MQH__

bool StateIntegrityValidationInProgress = false;

ReserveLedgerEntry ReserveLedger[];
long NextReserveEventId = 1;

void AppendReserveLedgerEntry(ReserveEventType type, double amount, double reserveBefore, double reserveAfter)
{
   int index = ArraySize(ReserveLedger);
   ArrayResize(ReserveLedger, index + 1);
   ReserveLedger[index].eventId = NextReserveEventId++;
   ReserveLedger[index].timestamp = TimeCurrent();
   ReserveLedger[index].type = type;
   ReserveLedger[index].amount = amount;
   ReserveLedger[index].reserveBefore = reserveBefore;
   ReserveLedger[index].reserveAfter = reserveAfter;
   ReserveLedger[index].bigIdentifier = (long)Ctx.bigIdentifier;
   ReserveLedger[index].smallIdentifier = (long)Ctx.smallIdentifier;
   ReserveLedger[index].farIdentifier = (long)Ctx.farIdentifier;
   ReserveLedger[index].harvestLevel = Ctx.harvestLevel;
   ReserveLedger[index].reverseCycle = Ctx.reverseCycleCount;
   LogInfo(StringFormat("RESERVE_LEDGER eventId=%d type=%d amount=%.2f reserveBefore=%.2f reserveAfter=%.2f bigIdentifier=%I64d smallIdentifier=%I64d farIdentifier=%I64d harvestLevel=%d reverseCycle=%d",
                        ReserveLedger[index].eventId,
                        (int)type,
                        amount,
                        reserveBefore,
                        reserveAfter,
                        ReserveLedger[index].bigIdentifier,
                        ReserveLedger[index].smallIdentifier,
                        ReserveLedger[index].farIdentifier,
                        ReserveLedger[index].harvestLevel,
                        ReserveLedger[index].reverseCycle));
}

void ApplyReserveCredit(ReserveEventType type, double amount)
{
   if(amount <= 0.0)
      return;
   double before = Ctx.totalReserve;
   Ctx.totalReserve = before + amount;
   AppendReserveLedgerEntry(type, amount, before, Ctx.totalReserve);
   SaveState();
}

void ApplyReserveDebit(ReserveEventType type, double amount)
{
   if(amount <= 0.0)
      return;
   double before = Ctx.totalReserve;
   Ctx.totalReserve = MathMax(0.0, before - amount);
   AppendReserveLedgerEntry(type, -amount, before, Ctx.totalReserve);
   SaveState();
}

void ApplyReserveReset(double amount, string reason)
{
   double before = Ctx.totalReserve;
   Ctx.totalReserve = MathMax(0.0, amount);
   AppendReserveLedgerEntry(RESERVE_EVENT_RESET, Ctx.totalReserve - before, before, Ctx.totalReserve);
   LogInfo("RESERVE_LEDGER_RESET " + reason);
   SaveState();
}

double RebuildReserveFromLedger()
{
   double reserve = 0.0;
   for(int i = 0; i < ArraySize(ReserveLedger); i++)
   {
      if(ReserveLedger[i].type == RESERVE_EVENT_RESET)
         reserve = ReserveLedger[i].reserveAfter;
      else
         reserve += ReserveLedger[i].amount;
   }
   if(reserve < 0.0)
      reserve = 0.0;
   return reserve;
}


bool ValidateNoOrphanManagedPositions();
bool ValidateStatePositionConsistency();
bool ValidateCurrentStateIntegrity();
bool ValidatePendingContract(EAState targetState);
bool ValidatePendingStateContract(EAState targetState);
bool PreparePendingOpenBigContext();
bool PreparePendingOpenSmallContext();
bool PreparePendingCloseBigContext();
bool PreparePendingCloseSmallContext();
bool PreparePendingCloseFarContext();
bool PreparePendingFinalCloseContext();
bool ResolveOpenedPositionAfterOpen(string comment, Direction direction, double expectedLot, ulong knownIdentifier, datetime openStartTime, PositionResolutionResult &result);
bool ApplyResolvedPositionToBig(PositionResolutionResult &result);
bool ApplyResolvedPositionToSmall(PositionResolutionResult &result);
bool TryRecoverPromotedBigAsFar(string reason);

bool IsProfitSystemCloseComment(string comment)
{
   return comment == "FINAL_CLOSE_PROFIT" ||
          comment == "CLOSED_PROFIT" ||
          comment == "MAX_LEVELS_FINAL_CLOSE";
}

bool CanEnterClosedProfit()
{
   RecalculateRealCycleStatsFromHistory();
   return CountManagedOpenPositions() == 0 &&
          !HasOpenLegContext() &&
          Ctx.realRecoveryPL > 0.0 &&
          Ctx.lastCloseWasSystemClose &&
          IsProfitSystemCloseComment(Ctx.lastSystemCloseComment);
}

void SetState(EAState nextState, string reason)
{
   if(nextState == STATE_CLOSED_PROFIT)
   {
      bool fullCloseVerified = true;
      if(Ctx.farTicket != 0) fullCloseVerified = VerifyFullClose(Ctx.farTicket, "STATE_CLOSED_PROFIT_FAR_GUARD") && fullCloseVerified;
      if(Ctx.bigTicket != 0) fullCloseVerified = VerifyFullClose(Ctx.bigTicket, "STATE_CLOSED_PROFIT_BIG_GUARD") && fullCloseVerified;
      if(Ctx.smallTicket != 0) fullCloseVerified = VerifyFullClose(Ctx.smallTicket, "STATE_CLOSED_PROFIT_SMALL_GUARD") && fullCloseVerified;

      if(!fullCloseVerified || !CanEnterClosedProfit())
      {
         LogError(StringFormat("CLOSED_PROFIT_BLOCKED: ManagedPositions=%d HasContext=%s RealRecoveryPL=%.2f LastCloseWasSystemClose=%s LastSystemCloseComment=%s",
                              CountManagedOpenPositions(),
                              HasOpenLegContext() ? "YES" : "NO",
                              Ctx.realRecoveryPL,
                              Ctx.lastCloseWasSystemClose ? "YES" : "NO",
                              Ctx.lastSystemCloseComment));
         if(CountManagedOpenPositions() == 0 && Ctx.realRecoveryPL <= 0.0)
         {
            nextState = STATE_CLOSED_RECOVERY_LOSS;
            reason = "CLOSED_RECOVERY_LOSS: realRecoveryPL <= 0";
         }
         else
         {
            nextState = STATE_MANUAL_INTERVENTION_REQUIRED;
            reason = "CLOSED_PROFIT_BLOCKED: strict recovery-profit guard failed";
         }
      }
   }

   if(State != nextState)
      LogTransition(State, nextState, reason);

   State = nextState;
   Ctx.lastAction = reason;
   if(nextState == STATE_ERROR || nextState == STATE_MANUAL_INTERVENTION_REQUIRED || nextState == STATE_RECOVERY_PENDING || nextState == STATE_INTEGRITY_ERROR || nextState == STATE_POSITION_RESOLUTION_ERROR)
      Ctx.lastError = reason;
   SaveState();

   if(nextState != STATE_INTEGRITY_ERROR && nextState != STATE_POSITION_RESOLUTION_ERROR && nextState != STATE_RECOVERY_MISMATCH && !StateIntegrityValidationInProgress)
      ValidateCurrentStateIntegrity();
}

string StateKey(string field)
{
   return StringFormat("MinusLock_%s_%I64u_%s", _Symbol, MagicNumber, field);
}

void SaveState()
{
   GlobalVariableSet(StateKey("State"), (double)State);
   GlobalVariableSet(StateKey("FarTicket"), (double)Ctx.farTicket);
   GlobalVariableSet(StateKey("FarIdentifier"), (double)Ctx.farIdentifier);
   GlobalVariableSet(StateKey("FarLot"), Ctx.farLot);
   GlobalVariableSet(StateKey("FarOpenPrice"), Ctx.farOpenPrice);
   GlobalVariableSet(StateKey("FarDirection"), (double)Ctx.farDirection);
   GlobalVariableSet(StateKey("BigTicket"), (double)Ctx.bigTicket);
   GlobalVariableSet(StateKey("BigIdentifier"), (double)Ctx.bigIdentifier);
   GlobalVariableSet(StateKey("BigLot"), Ctx.bigLot);
   GlobalVariableSet(StateKey("BigOpenPrice"), Ctx.bigOpenPrice);
   GlobalVariableSet(StateKey("BigDirection"), (double)Ctx.bigDirection);
   GlobalVariableSet(StateKey("SmallTicket"), (double)Ctx.smallTicket);
   GlobalVariableSet(StateKey("SmallIdentifier"), (double)Ctx.smallIdentifier);
   GlobalVariableSet(StateKey("SmallLot"), Ctx.smallLot);
   GlobalVariableSet(StateKey("SmallOpenPrice"), Ctx.smallOpenPrice);
   GlobalVariableSet(StateKey("SmallDirection"), (double)Ctx.smallDirection);
   GlobalVariableSet(StateKey("InitialBuyTicket"), (double)Ctx.initialBuyTicket);
   GlobalVariableSet(StateKey("InitialSellTicket"), (double)Ctx.initialSellTicket);
   GlobalVariableSet(StateKey("InitialBuyIdentifier"), (double)Ctx.initialBuyIdentifier);
   GlobalVariableSet(StateKey("InitialSellIdentifier"), (double)Ctx.initialSellIdentifier);
   GlobalVariableSet(StateKey("InitialBuyLot"), Ctx.initialBuyLot);
   GlobalVariableSet(StateKey("InitialSellLot"), Ctx.initialSellLot);
   GlobalVariableSet(StateKey("InitialBuyOpenPrice"), Ctx.initialBuyOpenPrice);
   GlobalVariableSet(StateKey("InitialSellOpenPrice"), Ctx.initialSellOpenPrice);
   GlobalVariableSet(StateKey("InitialLockRecovered"), Ctx.initialLockRecovered ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("HarvestLevel"), (double)Ctx.harvestLevel);
   GlobalVariableSet(StateKey("ReverseCycles"), (double)Ctx.reverseCycleCount);
   GlobalVariableSet(StateKey("TotalReserve"), Ctx.totalReserve);
   GlobalVariableSet(StateKey("ReserveLedgerCount"), (double)ArraySize(ReserveLedger));
   GlobalVariableSet(StateKey("ReserveNextEventId"), (double)NextReserveEventId);
   for(int ledgerIndex = 0; ledgerIndex < ArraySize(ReserveLedger); ledgerIndex++)
   {
      string prefix = StringFormat("ReserveLedger_%d_", ledgerIndex);
      GlobalVariableSet(StateKey(prefix + "EventId"), (double)ReserveLedger[ledgerIndex].eventId);
      GlobalVariableSet(StateKey(prefix + "Timestamp"), (double)ReserveLedger[ledgerIndex].timestamp);
      GlobalVariableSet(StateKey(prefix + "Type"), (double)ReserveLedger[ledgerIndex].type);
      GlobalVariableSet(StateKey(prefix + "Amount"), ReserveLedger[ledgerIndex].amount);
      GlobalVariableSet(StateKey(prefix + "ReserveBefore"), ReserveLedger[ledgerIndex].reserveBefore);
      GlobalVariableSet(StateKey(prefix + "ReserveAfter"), ReserveLedger[ledgerIndex].reserveAfter);
      GlobalVariableSet(StateKey(prefix + "BigIdentifier"), (double)ReserveLedger[ledgerIndex].bigIdentifier);
      GlobalVariableSet(StateKey(prefix + "SmallIdentifier"), (double)ReserveLedger[ledgerIndex].smallIdentifier);
      GlobalVariableSet(StateKey(prefix + "FarIdentifier"), (double)ReserveLedger[ledgerIndex].farIdentifier);
      GlobalVariableSet(StateKey(prefix + "HarvestLevel"), (double)ReserveLedger[ledgerIndex].harvestLevel);
      GlobalVariableSet(StateKey(prefix + "ReverseCycle"), (double)ReserveLedger[ledgerIndex].reverseCycle);
   }
   GlobalVariableSet(StateKey("CycleId"), (double)Ctx.cycleId);
   GlobalVariableSet(StateKey("InitialProfitIgnored"), Ctx.initialProfitIgnored ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("EffectiveFarDistancePoints"), Ctx.effectiveFarDistancePoints);
   GlobalVariableSet(StateKey("CycleATRRaw"), Ctx.cycleATRRaw);
   GlobalVariableSet(StateKey("CycleATRPoints"), Ctx.cycleATRPoints);
   GlobalVariableSet(StateKey("GeometrySource"), (double)Ctx.geometrySource);
   GlobalVariableSet(StateKey("GeometryFallback"), (double)Ctx.geometryFallback);
   GlobalVariableSet(StateKey("GeometryFallbackReasonCode"), (double)Ctx.geometryFallbackReasonCode);
   GlobalVariableSet(StateKey("GeometryCleared"), (double)Ctx.geometryCleared);
   GlobalVariableSet(StateKey("GeometryClearReasonCode"), (double)Ctx.geometryClearReasonCode);
   GlobalVariableSet(StateKey("WorkInitialTriggerPoints"), (double)Ctx.workInitialTriggerPoints);
   GlobalVariableSet(StateKey("WorkBigMoveStartPoints"), (double)Ctx.workBigMoveStartPoints);
   GlobalVariableSet(StateKey("WorkBigMoveStepPoints"), (double)Ctx.workBigMoveStepPoints);
   GlobalVariableSet(StateKey("WorkFarDistancePoints"), (double)Ctx.workFarDistancePoints);
   GlobalVariableSet(StateKey("GeometryModeUsed"), (double)Ctx.geometryModeUsed);
   GlobalVariableSet(StateKey("GeometryCalculatedTime"), (double)Ctx.geometryCalculatedTime);
   GlobalVariableSet(StateKey("CycleStartBalance"), Ctx.cycleStartBalance);
   GlobalVariableSet(StateKey("RealCyclePL"), Ctx.realCyclePL);
   GlobalVariableSet(StateKey("FinalCloseAllowed"), Ctx.finalCloseAllowed ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("LastRetryState"), (double)Ctx.lastRetryState);
   GlobalVariableSet(StateKey("RetryTicket"), (double)Ctx.retryTicket);
   GlobalVariableSet(StateKey("RetryLot"), Ctx.retryLot);
   GlobalVariableSet(StateKey("RetryAttempts"), (double)Ctx.retryAttempts);
   GlobalVariableSet(StateKey("PendingActionType"), (double)Ctx.pendingActionType);
   GlobalVariableSet(StateKey("PendingNextState"), (double)Ctx.pendingNextState);
   GlobalVariableSet(StateKey("PendingTicket"), (double)Ctx.pendingTicket);
   GlobalVariableSet(StateKey("PendingLot"), Ctx.pendingLot);
   GlobalVariableSet(StateKey("PendingAttempts"), (double)Ctx.pendingAttempts);
   GlobalVariableSet(StateKey("PendingOperationStartTime"), (double)Ctx.pendingOperationStartTime);
   GlobalVariableSet(StateKey("PendingBigPositionId"), (double)Ctx.pendingBigPositionId);
   GlobalVariableSet(StateKey("PendingSmallPositionId"), (double)Ctx.pendingSmallPositionId);
   GlobalVariableSet(StateKey("PendingRealNet"), Ctx.pendingRealNet);
   GlobalVariableSet(StateKey("PendingCloseFarBudget"), Ctx.pendingCloseFarBudget);
   GlobalVariableSet(StateKey("PendingReserveAdd"), Ctx.pendingReserveAdd);
   GlobalVariableSet(StateKey("PendingSmallReserveAdd"), Ctx.pendingSmallReserveAdd);
   GlobalVariableSet(StateKey("PendingReserveApplied"), Ctx.pendingReserveApplied ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("PendingSmallReserveApplied"), Ctx.pendingSmallReserveApplied ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("PendingCloseFarLot"), Ctx.pendingCloseFarLot);
   GlobalVariableSet(StateKey("PendingDirection"), (double)Ctx.pendingDirection);
   // PendingComment is rebuilt from the pending phase after restart.
   GlobalVariableSet(StateKey("SavedSmallDirection"), (double)Ctx.savedSmallDirection);
   GlobalVariableSet(StateKey("SavedSmallClosePrice"), Ctx.savedSmallClosePrice);
   GlobalVariableSet(StateKey("SavedSmallTouchPrice"), Ctx.savedSmallTouchPrice);
   GlobalVariableSet(StateKey("SavedSmallOpenPrice"), Ctx.savedSmallOpenPrice);
   GlobalVariableSet(StateKey("SavedSmallLot"), Ctx.savedSmallLot);
   GlobalVariableSet(StateKey("OldFarTicket"), (double)Ctx.oldFarTicket);
   GlobalVariableSet(StateKey("OldFarLot"), Ctx.oldFarLot);
   GlobalVariableSet(StateKey("OldFarDirection"), (double)Ctx.oldFarDirection);
   GlobalVariableSet(StateKey("OldFarOpenPrice"), Ctx.oldFarOpenPrice);
   GlobalVariableSet(StateKey("SmallScenarioRealBefore"), Ctx.smallScenarioRealBefore);
   GlobalVariableSet(StateKey("SmallScenarioRealAfter"), Ctx.smallScenarioRealAfter);
   GlobalVariableSet(StateKey("CycleStartTime"), (double)Ctx.cycleStartTime);
   GlobalVariableSet(StateKey("CurrentBigMovePoints"), Ctx.currentBigMovePoints);
   GlobalVariableSet(StateKey("CumulativeBigMovePoints"), Ctx.cumulativeBigMovePoints);
   GlobalVariableSet(StateKey("InitialFarDistancePoints"), Ctx.initialFarDistancePoints);
   GlobalVariableSet(StateKey("CurrentClosePrice"), Ctx.currentClosePrice);
   GlobalVariableSet(StateKey("SmallReverseNet"), Ctx.smallReverseNet);
   GlobalVariableSet(StateKey("ProjectedReserveCoverage"), Ctx.projectedReserveCoverage);
   GlobalVariableSet(StateKey("ReverseStrength"), Ctx.reverseStrength);
   // Text fields lastAction, lastError and lastSystemCloseComment are reported in logs and preserved by live context.
}

bool GetStateDouble(string field, double &value)
{
   string key = StateKey(field);
   if(!GlobalVariableCheck(key))
      return false;
   value = GlobalVariableGet(key);
   return true;
}

bool IsPositionFullyClosed(double actualVolume)
{
   return actualVolume <= VolumeMismatchToleranceLots;
}

bool VerifyFullClose(ulong ticket, string operationName)
{
   double actualVolume = GetActualPositionVolume(ticket);
   double normalizedActual = NormalizeVolumeToStep(actualVolume);
   double difference = MathAbs(normalizedActual - 0.0);
   LogInfo(StringFormat("VERIFY_FULL_CLOSE Operation=%s Ticket=%I64u ExpectedVolume=0.00 ActualVolume=%.2f Difference=%.5f VolumeMismatchToleranceLots=%.5f", operationName, ticket, normalizedActual, difference, VolumeMismatchToleranceLots));
   if(!IsPositionFullyClosed(normalizedActual))
   {
      LogError(StringFormat("FULL_CLOSE_INCOMPLETE Operation=%s Ticket=%I64u ExpectedVolume=0.00 ActualVolume=%.2f Difference=%.5f", operationName, ticket, normalizedActual, difference));
      return false;
   }
   return true;
}


bool HasInitialBuyContext()
{
   return (Ctx.initialBuyTicket != 0 || Ctx.initialBuyIdentifier != 0 || Ctx.initialBuyLot > VolumeMismatchToleranceLots);
}

bool HasInitialSellContext()
{
   return (Ctx.initialSellTicket != 0 || Ctx.initialSellIdentifier != 0 || Ctx.initialSellLot > VolumeMismatchToleranceLots);
}

bool HasFarContext()
{
   return (Ctx.farTicket != 0 || Ctx.farIdentifier != 0 || Ctx.farLot > VolumeMismatchToleranceLots || Ctx.farDirection != DIR_NONE);
}

bool HasBigContext()
{
   return (Ctx.bigTicket != 0 || Ctx.bigIdentifier != 0 || Ctx.bigLot > VolumeMismatchToleranceLots || Ctx.bigDirection != DIR_NONE);
}

bool HasSmallContext()
{
   return (Ctx.smallTicket != 0 || Ctx.smallIdentifier != 0 || Ctx.smallLot > VolumeMismatchToleranceLots || Ctx.smallDirection != DIR_NONE);
}

bool HasPendingOperationContext()
{
   return (Ctx.pendingActionType != PENDING_NONE || Ctx.pendingTicket != 0 || Ctx.pendingLot > VolumeMismatchToleranceLots || Ctx.pendingNextState != STATE_IDLE || Ctx.pendingAttempts > 0);
}

bool HasRetryOperationContext()
{
   return (Ctx.retryTicket != 0 || Ctx.retryLot > VolumeMismatchToleranceLots || Ctx.lastRetryState != STATE_IDLE || Ctx.retryAttempts > 0);
}

bool HasKnownContext()
{
   bool initialBuy = HasInitialBuyContext();
   bool initialSell = HasInitialSellContext();
   bool far = HasFarContext();
   bool big = HasBigContext();
   bool small = HasSmallContext();
   bool pending = HasPendingOperationContext();
   bool retry = HasRetryOperationContext();
   bool known = (initialBuy || initialSell || far || big || small || pending || retry);
   LogInfo(StringFormat("KNOWN_CONTEXT_PRESENT InitialBuy=%s InitialSell=%s Far=%s Big=%s Small=%s Pending=%s Retry=%s KnownContext=%s",
                        initialBuy ? "YES" : "NO",
                        initialSell ? "YES" : "NO",
                        far ? "YES" : "NO",
                        big ? "YES" : "NO",
                        small ? "YES" : "NO",
                        pending ? "YES" : "NO",
                        retry ? "YES" : "NO",
                        known ? "YES" : "NO"));
   return known;
}

void LogReconciliationContextSummary(string source)
{
   bool initialLock = (HasInitialBuyContext() || HasInitialSellContext());
   bool far = HasFarContext();
   bool big = HasBigContext();
   bool small = HasSmallContext();
   bool pending = HasPendingOperationContext();
   bool retry = HasRetryOperationContext();
   bool known = (initialLock || far || big || small || pending || retry);
   LogInfo(StringFormat("RECONCILIATION_CONTEXT_SUMMARY Source=%s CurrentState=%s ManagedPositions=%d KnownContext=%s InitialLock=%s Far=%s Big=%s Small=%s Pending=%s Retry=%s ConfiguredGeometryMode=%s RuntimeGeometryMode=%s GeometrySource=%s GeometryActive=%s GeometryCleared=%s GeometryClearReason=%s ATRRaw=%.10f ATRPoints=%.1f WorkInitialTriggerPoints=%d WorkBigMoveStartPoints=%d WorkBigMoveStepPoints=%d WorkFarDistancePoints=%d WorkSource=%s FallbackReason=%s",
                        source,
                        StateToString(State),
                        CountManagedOpenPositions(),
                        known ? "YES" : "NO",
                        initialLock ? "YES" : "NO",
                        far ? "YES" : "NO",
                        big ? "YES" : "NO",
                        small ? "YES" : "NO",
                        pending ? "YES" : "NO",
                        retry ? "YES" : "NO",
                        ConfiguredGeometryModeToString(),
                        RuntimeGeometryModeToString(),
                        GeometrySourceForDiagnostics(),
                        GeometryActive() ? "YES" : "NO",
                        Ctx.geometryCleared > 0 ? "YES" : "NO",
                        GeometryClearReasonToString(Ctx.geometryClearReasonCode),
                        Ctx.cycleATRRaw,
                        Ctx.cycleATRPoints,
                        DisplayWorkInitialTriggerPoints(),
                        DisplayWorkBigMoveStartPoints(),
                        DisplayWorkBigMoveStepPoints(),
                        DisplayWorkFarDistancePoints(),
                        GeometryActive() ? GeometrySourceForDiagnostics() : "MANUAL_FALLBACK_FOR_DISPLAY_ONLY",
                        GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode)));
}

bool HasOpenLegContext()
{
   return HasKnownContext();
}

void ClearFarContext(string reason)
{
   LogInfo("CLEAR_FAR_CONTEXT " + reason);
   Ctx.farTicket = 0;
   Ctx.farIdentifier = 0;
   Ctx.farLot = 0.0;
   Ctx.farDirection = DIR_NONE;
   Ctx.farOpenPrice = 0.0;
   SaveState();
}

void ClearBigContext(string reason)
{
   LogInfo("CLEAR_BIG_CONTEXT " + reason);
   Ctx.bigTicket = 0;
   Ctx.bigIdentifier = 0;
   Ctx.bigLot = 0.0;
   Ctx.bigDirection = DIR_NONE;
   Ctx.bigOpenPrice = 0.0;
   SaveState();
}

void ClearSmallContext(string reason)
{
   LogInfo("CLEAR_SMALL_CONTEXT " + reason);
   Ctx.smallTicket = 0;
   Ctx.smallIdentifier = 0;
   Ctx.smallLot = 0.0;
   Ctx.smallDirection = DIR_NONE;
   Ctx.smallOpenPrice = 0.0;
   SaveState();
}

void RegisterInitialLockFromSnapshots(PositionSnapshot &initialBuy, PositionSnapshot &initialSell, string reason)
{
   Ctx.initialBuyTicket = initialBuy.ticket;
   Ctx.initialSellTicket = initialSell.ticket;
   Ctx.initialBuyIdentifier = initialBuy.identifier;
   Ctx.initialSellIdentifier = initialSell.identifier;
   Ctx.initialBuyLot = NormalizeVolumeToStep(initialBuy.lot);
   Ctx.initialSellLot = NormalizeVolumeToStep(initialSell.lot);
   Ctx.initialBuyOpenPrice = initialBuy.openPrice;
   Ctx.initialSellOpenPrice = initialSell.openPrice;
   Ctx.initialLockRecovered = true;
   LogInfo(StringFormat("INITIAL_LOCK_REGISTERED Reason=%s BuyTicket=%I64u BuyIdentifier=%I64u BuyLot=%.2f BuyOpenPrice=%.5f SellTicket=%I64u SellIdentifier=%I64u SellLot=%.2f SellOpenPrice=%.5f",
                        reason,
                        Ctx.initialBuyTicket,
                        Ctx.initialBuyIdentifier,
                        Ctx.initialBuyLot,
                        Ctx.initialBuyOpenPrice,
                        Ctx.initialSellTicket,
                        Ctx.initialSellIdentifier,
                        Ctx.initialSellLot,
                        Ctx.initialSellOpenPrice));
   SaveState();
}

void ClearInitialLockContext(string reason)
{
   LogInfo("CLEAR_INITIAL_LOCK_CONTEXT " + reason);
   Ctx.initialBuyTicket = 0;
   Ctx.initialSellTicket = 0;
   Ctx.initialBuyIdentifier = 0;
   Ctx.initialSellIdentifier = 0;
   Ctx.initialBuyLot = 0.0;
   Ctx.initialSellLot = 0.0;
   Ctx.initialBuyOpenPrice = 0.0;
   Ctx.initialSellOpenPrice = 0.0;
   Ctx.initialLockRecovered = false;
   SaveState();
}

void ConvertInitialLockToFar(PositionSnapshot &remainingFar, PositionSnapshot &closedInitial, string reason)
{
   UpdateFarFromSnapshot(remainingFar);
   ClearInitialLockContext(reason);
   Ctx.initialLockRecovered = false;
   LogInfo(StringFormat("INITIAL_LOCK_CONVERTED_TO_FAR Reason=%s ClosedTicket=%I64u ClosedIdentifier=%I64u FarTicket=%I64u FarIdentifier=%I64u FarDirection=%s FarLot=%.2f",
                        reason,
                        closedInitial.ticket,
                        closedInitial.identifier,
                        Ctx.farTicket,
                        Ctx.farIdentifier,
                        DirectionToString(Ctx.farDirection),
                        Ctx.farLot));
   SaveState();
}

bool RefreshFarVolumeFromTerminal(string reason)
{
   bool ok = RefreshLegVolumeFromTerminal(Ctx.farTicket, Ctx.farLot, "FAR");
   LogInfo(StringFormat("REFRESH_FAR_VOLUME_FROM_TERMINAL Reason=%s Result=%s FarLot=%.2f", reason, ok ? "FOUND" : "NOT_FOUND", Ctx.farLot));
   SaveState();
   return ok;
}

bool RefreshBigVolumeFromTerminal(string reason)
{
   bool ok = RefreshLegVolumeFromTerminal(Ctx.bigTicket, Ctx.bigLot, "BIG");
   LogInfo(StringFormat("REFRESH_BIG_VOLUME_FROM_TERMINAL Reason=%s Result=%s BigLot=%.2f", reason, ok ? "FOUND" : "NOT_FOUND", Ctx.bigLot));
   SaveState();
   return ok;
}

bool RefreshSmallVolumeFromTerminal(string reason)
{
   bool ok = RefreshLegVolumeFromTerminal(Ctx.smallTicket, Ctx.smallLot, "SMALL");
   LogInfo(StringFormat("REFRESH_SMALL_VOLUME_FROM_TERMINAL Reason=%s Result=%s SmallLot=%.2f", reason, ok ? "FOUND" : "NOT_FOUND", Ctx.smallLot));
   SaveState();
   return ok;
}

bool VerifyPositionVolumeIntegrity(string source, double expectedVolume, double actualVolume)
{
   double normalizedExpected = NormalizeVolumeToStep(expectedVolume);
   double normalizedActual = NormalizeVolumeToStep(actualVolume);
   double difference = MathAbs(normalizedExpected - normalizedActual);
   LogInfo(StringFormat("POSITION_VOLUME_INTEGRITY Source=%s ExpectedVolume=%.2f ActualVolume=%.2f Difference=%.5f VolumeMismatchToleranceLots=%.5f", source, normalizedExpected, normalizedActual, difference, VolumeMismatchToleranceLots));
   if(difference > VolumeMismatchToleranceLots)
   {
      LogError(StringFormat("POSITION_VOLUME_INTEGRITY_FAIL Source=%s ExpectedVolume=%.2f ActualVolume=%.2f Difference=%.5f VolumeMismatchToleranceLots=%.5f", source, normalizedExpected, normalizedActual, difference, VolumeMismatchToleranceLots));
      return false;
   }
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
      // Reconcile by Symbol + MagicNumber + Ticket + Position identifier + Comment + Direction + SavedVolume + ActualVolume + OpenPrice.
      double savedVolume = lot;
      double actualVolume = GetActualPositionVolume(snapshot.ticket);
      if(actualVolume <= 0.0)
         actualVolume = snapshot.lot;
      LogInfo(StringFormat("RECOVER_RECONCILE_VOLUME %s SavedVolume=%.2f ActualVolume=%.2f Difference=%.5f", legName, savedVolume, actualVolume, MathAbs(NormalizeVolumeToStep(savedVolume) - NormalizeVolumeToStep(actualVolume))));
      ticket = snapshot.ticket;
      lot = actualVolume;
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
   LogInfo(StringFormat("RECOVERY_DIAGNOSTICS Managed positions found | Saved State=%s Recovered State=%s Open Positions=%d Unknown Positions=0 Missing Positions=0 Duplicate Positions=0", StateToString(State), StateToString(State), CountManagedOpenPositions()));
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
   double saved = 0.0;
   State = (EAState)(int)GlobalVariableGet(StateKey("State"));
   Ctx.farTicket = (ulong)GlobalVariableGet(StateKey("FarTicket"));
   if(GetStateDouble("FarIdentifier", saved)) Ctx.farIdentifier = (ulong)saved;
   Ctx.farLot = GlobalVariableGet(StateKey("FarLot"));
   Ctx.farOpenPrice = GlobalVariableGet(StateKey("FarOpenPrice"));
   Ctx.farDirection = (Direction)(int)GlobalVariableGet(StateKey("FarDirection"));
   Ctx.bigTicket = (ulong)GlobalVariableGet(StateKey("BigTicket"));
   if(GetStateDouble("BigIdentifier", saved)) Ctx.bigIdentifier = (ulong)saved;
   Ctx.bigLot = GlobalVariableGet(StateKey("BigLot"));
   Ctx.bigOpenPrice = GlobalVariableGet(StateKey("BigOpenPrice"));
   Ctx.bigDirection = (Direction)(int)GlobalVariableGet(StateKey("BigDirection"));
   Ctx.smallTicket = (ulong)GlobalVariableGet(StateKey("SmallTicket"));
   if(GetStateDouble("SmallIdentifier", saved)) Ctx.smallIdentifier = (ulong)saved;
   Ctx.smallLot = GlobalVariableGet(StateKey("SmallLot"));
   Ctx.smallOpenPrice = GlobalVariableGet(StateKey("SmallOpenPrice"));
   Ctx.smallDirection = (Direction)(int)GlobalVariableGet(StateKey("SmallDirection"));
   if(GetStateDouble("InitialBuyTicket", saved)) Ctx.initialBuyTicket = (ulong)saved;
   if(GetStateDouble("InitialSellTicket", saved)) Ctx.initialSellTicket = (ulong)saved;
   if(GetStateDouble("InitialBuyIdentifier", saved)) Ctx.initialBuyIdentifier = (ulong)saved;
   if(GetStateDouble("InitialSellIdentifier", saved)) Ctx.initialSellIdentifier = (ulong)saved;
   if(GetStateDouble("InitialBuyLot", saved)) Ctx.initialBuyLot = saved;
   if(GetStateDouble("InitialSellLot", saved)) Ctx.initialSellLot = saved;
   if(GetStateDouble("InitialBuyOpenPrice", saved)) Ctx.initialBuyOpenPrice = saved;
   if(GetStateDouble("InitialSellOpenPrice", saved)) Ctx.initialSellOpenPrice = saved;
   if(GetStateDouble("InitialLockRecovered", saved)) Ctx.initialLockRecovered = (saved > 0.5);
   Ctx.harvestLevel = (int)GlobalVariableGet(StateKey("HarvestLevel"));
   Ctx.reverseCycleCount = (int)GlobalVariableGet(StateKey("ReverseCycles"));
   Ctx.totalReserve = GlobalVariableGet(StateKey("TotalReserve"));
   ArrayResize(ReserveLedger, 0);
   NextReserveEventId = 1;
   if(GetStateDouble("ReserveLedgerCount", saved))
   {
      int ledgerCount = (int)saved;
      ArrayResize(ReserveLedger, ledgerCount);
      for(int ledgerIndex = 0; ledgerIndex < ledgerCount; ledgerIndex++)
      {
         string prefix = StringFormat("ReserveLedger_%d_", ledgerIndex);
         if(GetStateDouble(prefix + "EventId", saved)) ReserveLedger[ledgerIndex].eventId = (long)saved;
         if(GetStateDouble(prefix + "Timestamp", saved)) ReserveLedger[ledgerIndex].timestamp = (datetime)saved;
         if(GetStateDouble(prefix + "Type", saved)) ReserveLedger[ledgerIndex].type = (ReserveEventType)(int)saved;
         if(GetStateDouble(prefix + "Amount", saved)) ReserveLedger[ledgerIndex].amount = saved;
         if(GetStateDouble(prefix + "ReserveBefore", saved)) ReserveLedger[ledgerIndex].reserveBefore = saved;
         if(GetStateDouble(prefix + "ReserveAfter", saved)) ReserveLedger[ledgerIndex].reserveAfter = saved;
         if(GetStateDouble(prefix + "BigIdentifier", saved)) ReserveLedger[ledgerIndex].bigIdentifier = (long)saved;
         if(GetStateDouble(prefix + "SmallIdentifier", saved)) ReserveLedger[ledgerIndex].smallIdentifier = (long)saved;
         if(GetStateDouble(prefix + "FarIdentifier", saved)) ReserveLedger[ledgerIndex].farIdentifier = (long)saved;
         if(GetStateDouble(prefix + "HarvestLevel", saved)) ReserveLedger[ledgerIndex].harvestLevel = (int)saved;
         if(GetStateDouble(prefix + "ReverseCycle", saved)) ReserveLedger[ledgerIndex].reverseCycle = (int)saved;
      }
   }
   if(GetStateDouble("ReserveNextEventId", saved)) NextReserveEventId = (long)saved;

   if(GetStateDouble("CycleId", saved)) Ctx.cycleId = (ulong)saved;
   if(GetStateDouble("InitialProfitIgnored", saved)) Ctx.initialProfitIgnored = (saved > 0.5);
   if(GetStateDouble("EffectiveFarDistancePoints", saved)) Ctx.effectiveFarDistancePoints = saved;
   if(GetStateDouble("CycleATRRaw", saved)) Ctx.cycleATRRaw = saved;
   if(GetStateDouble("CycleATRPoints", saved)) Ctx.cycleATRPoints = saved;
   if(GetStateDouble("GeometrySource", saved)) Ctx.geometrySource = (int)saved;
   if(GetStateDouble("GeometryFallback", saved)) Ctx.geometryFallback = (int)saved;
   if(GetStateDouble("GeometryFallbackReasonCode", saved)) Ctx.geometryFallbackReasonCode = (int)saved;
   if(GetStateDouble("GeometryCleared", saved)) Ctx.geometryCleared = (int)saved;
   if(GetStateDouble("GeometryClearReasonCode", saved)) Ctx.geometryClearReasonCode = (int)saved;
   if(GetStateDouble("WorkInitialTriggerPoints", saved)) Ctx.workInitialTriggerPoints = (int)saved;
   if(GetStateDouble("WorkBigMoveStartPoints", saved)) Ctx.workBigMoveStartPoints = (int)saved;
   if(GetStateDouble("WorkBigMoveStepPoints", saved)) Ctx.workBigMoveStepPoints = (int)saved;
   if(GetStateDouble("WorkFarDistancePoints", saved)) Ctx.workFarDistancePoints = (int)saved;
   if(GetStateDouble("GeometryModeUsed", saved)) Ctx.geometryModeUsed = (int)saved;
   if(GetStateDouble("GeometryCalculatedTime", saved)) Ctx.geometryCalculatedTime = (datetime)saved;
   if(GetStateDouble("CycleStartBalance", saved)) Ctx.cycleStartBalance = saved;
   if(GetStateDouble("RealCyclePL", saved)) Ctx.realCyclePL = saved;
   if(GetStateDouble("FinalCloseAllowed", saved)) Ctx.finalCloseAllowed = (saved > 0.5);
   if(GetStateDouble("LastRetryState", saved)) Ctx.lastRetryState = (EAState)(int)saved;
   if(GetStateDouble("RetryTicket", saved)) Ctx.retryTicket = (ulong)saved;
   if(GetStateDouble("RetryLot", saved)) Ctx.retryLot = saved;
   if(GetStateDouble("RetryAttempts", saved)) Ctx.retryAttempts = (int)saved;
   if(GetStateDouble("PendingActionType", saved)) Ctx.pendingActionType = (PendingActionType)(int)saved;
   if(GetStateDouble("PendingNextState", saved)) Ctx.pendingNextState = (EAState)(int)saved;
   if(GetStateDouble("PendingTicket", saved)) Ctx.pendingTicket = (ulong)saved;
   if(GetStateDouble("PendingLot", saved)) Ctx.pendingLot = saved;
   if(GetStateDouble("PendingAttempts", saved)) Ctx.pendingAttempts = (int)saved;
   if(GetStateDouble("PendingOperationStartTime", saved)) Ctx.pendingOperationStartTime = (datetime)saved;
   if(GetStateDouble("PendingBigPositionId", saved)) Ctx.pendingBigPositionId = (ulong)saved;
   if(GetStateDouble("PendingSmallPositionId", saved)) Ctx.pendingSmallPositionId = (ulong)saved;
   if(GetStateDouble("PendingRealNet", saved)) Ctx.pendingRealNet = saved;
   if(GetStateDouble("PendingCloseFarBudget", saved)) Ctx.pendingCloseFarBudget = saved;
   if(GetStateDouble("PendingReserveAdd", saved)) Ctx.pendingReserveAdd = saved;
   if(GetStateDouble("PendingSmallReserveAdd", saved)) Ctx.pendingSmallReserveAdd = saved;
   if(GetStateDouble("PendingReserveApplied", saved)) Ctx.pendingReserveApplied = (saved > 0.5);
   if(GetStateDouble("PendingSmallReserveApplied", saved)) Ctx.pendingSmallReserveApplied = (saved > 0.5);
   if(GetStateDouble("PendingCloseFarLot", saved)) Ctx.pendingCloseFarLot = saved;
   if(GetStateDouble("PendingDirection", saved)) Ctx.pendingDirection = (Direction)(int)saved;
   if(GetStateDouble("SavedSmallDirection", saved)) Ctx.savedSmallDirection = (Direction)(int)saved;
   if(GetStateDouble("SavedSmallClosePrice", saved)) Ctx.savedSmallClosePrice = saved;
   if(GetStateDouble("SavedSmallTouchPrice", saved)) Ctx.savedSmallTouchPrice = saved;
   if(GetStateDouble("SavedSmallOpenPrice", saved)) Ctx.savedSmallOpenPrice = saved;
   if(GetStateDouble("SavedSmallLot", saved)) Ctx.savedSmallLot = saved;
   if(GetStateDouble("OldFarTicket", saved)) Ctx.oldFarTicket = (ulong)saved;
   if(GetStateDouble("OldFarLot", saved)) Ctx.oldFarLot = saved;
   if(GetStateDouble("OldFarDirection", saved)) Ctx.oldFarDirection = (Direction)(int)saved;
   if(GetStateDouble("OldFarOpenPrice", saved)) Ctx.oldFarOpenPrice = saved;
   if(GetStateDouble("SmallScenarioRealBefore", saved)) Ctx.smallScenarioRealBefore = saved;
   if(GetStateDouble("SmallScenarioRealAfter", saved)) Ctx.smallScenarioRealAfter = saved;
   if(GetStateDouble("CycleStartTime", saved)) Ctx.cycleStartTime = (datetime)saved;
   if(GetStateDouble("CurrentBigMovePoints", saved)) Ctx.currentBigMovePoints = saved;
   if(GetStateDouble("CumulativeBigMovePoints", saved)) Ctx.cumulativeBigMovePoints = saved;
   if(GetStateDouble("InitialFarDistancePoints", saved)) Ctx.initialFarDistancePoints = saved;
   if(GetStateDouble("CurrentClosePrice", saved)) Ctx.currentClosePrice = saved;
   if(GetStateDouble("SmallReverseNet", saved)) Ctx.smallReverseNet = saved;
   if(GetStateDouble("ProjectedReserveCoverage", saved)) Ctx.projectedReserveCoverage = saved;
   if(GetStateDouble("ReverseStrength", saved)) Ctx.reverseStrength = saved;

   if(!HasCycleGeometry() && (State != STATE_IDLE || HasKnownContext()))
   {
      EnsureCycleGeometry("RecoverState restored active or pending context without saved Work geometry");
      SaveState();
   }

   PositionSnapshot recoveredInitialBuy;
   PositionSnapshot recoveredInitialSell;
   bool recoveredHasInitialBuy = GetInitialBuy(recoveredInitialBuy);
   bool recoveredHasInitialSell = GetInitialSell(recoveredInitialSell);
   if(recoveredHasInitialBuy && recoveredHasInitialSell)
   {
      RegisterInitialLockFromSnapshots(recoveredInitialBuy, recoveredInitialSell, "RecoverState");
      State = STATE_INITIAL_LOCK_OPENED;
      Ctx.initialLockRecovered = true;
      if(!HasCycleGeometry())
      {
         InitializeCycleGeometry();
         PrintGeometryDiagnostics();
      }
      LogInfo(StringFormat("INITIAL_LOCK_RECOVERED BuyTicket=%I64u SellTicket=%I64u", Ctx.initialBuyTicket, Ctx.initialSellTicket));
   }
   else if(State == STATE_INITIAL_LOCK_OPENED && (recoveredHasInitialBuy || recoveredHasInitialSell))
   {
      PositionSnapshot remainingInitial = recoveredHasInitialBuy ? recoveredInitialBuy : recoveredInitialSell;
      PositionSnapshot missingInitial;
      missingInitial.ticket = recoveredHasInitialBuy ? Ctx.initialSellTicket : Ctx.initialBuyTicket;
      missingInitial.identifier = recoveredHasInitialBuy ? Ctx.initialSellIdentifier : Ctx.initialBuyIdentifier;
      UpdateFarFromSnapshot(remainingInitial);
      ClearInitialLockContext("RecoverState partial initial lock converted to Far");
      if(!HasCycleGeometry())
      {
         InitializeCycleGeometry();
         PrintGeometryDiagnostics();
      }
      Ctx.initialProfitIgnored = true;
      Ctx.initialFarDistancePoints = WorkInitialTriggerPoints();
      State = STATE_FAR_ACTIVE;
      LogInfo(StringFormat("INITIAL_LOCK_CONVERTED_TO_FAR Reason=RecoverStatePartial RemainingTicket=%I64u FarTicket=%I64u", remainingInitial.ticket, Ctx.farTicket));
   }

   int managed = CountManagedOpenPositions();
   if(TryRecoverPromotedBigAsFar("RecoverState"))
      managed = CountManagedOpenPositions();
   bool reconcileOk = true;
   if(managed > 0)
   {
      LogManagedPositionsForRecovery();
      if(State != STATE_INITIAL_LOCK_OPENED)
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
   LogInfo(StringFormat("RECOVERY_CONTEXT_RESTORED State=%s ManagedPositions=%d KnownContext=%s", StateToString(State), managed, HasKnownContext() ? "YES" : "NO"));
   LogReconciliationContextSummary("RecoverState");
   return true;
}

void ResetRecoveryContext()
{
   if(IsInternalSimulationMode())
      SimResetHistory();

   Ctx.farTicket = 0;
   Ctx.bigTicket = 0;
   Ctx.smallTicket = 0;
   Ctx.farIdentifier = 0;
   Ctx.bigIdentifier = 0;
   Ctx.smallIdentifier = 0;
   Ctx.initialBuyTicket = 0;
   Ctx.initialSellTicket = 0;
   Ctx.initialBuyIdentifier = 0;
   Ctx.initialSellIdentifier = 0;

   Ctx.farLot = 0.0;
   Ctx.bigLot = 0.0;
   Ctx.smallLot = 0.0;

   Ctx.farOpenPrice = 0.0;
   Ctx.bigOpenPrice = 0.0;
   Ctx.smallOpenPrice = 0.0;
   Ctx.initialBuyLot = 0.0;
   Ctx.initialSellLot = 0.0;
   Ctx.initialBuyOpenPrice = 0.0;
   Ctx.initialSellOpenPrice = 0.0;

   Ctx.farDirection = DIR_NONE;
   Ctx.bigDirection = DIR_NONE;
   Ctx.smallDirection = DIR_NONE;

   Ctx.harvestLevel = 0;
   Ctx.totalReserve = 0.0;
   ArrayResize(ReserveLedger, 0);
   NextReserveEventId = 1;
   Ctx.cycleFinalPL = 0.0;

   Ctx.initialProfitIgnored = false;
   Ctx.initialLockRecovered = false;
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
   Ctx.cycleATRRaw = 0.0;
   Ctx.cycleATRPoints = 0.0;
   Ctx.geometrySource = 0;
   Ctx.geometryFallback = 0;
   Ctx.geometryFallbackReasonCode = 0;
   Ctx.geometryCleared = 0;
   Ctx.geometryClearReasonCode = 0;
   Ctx.workInitialTriggerPoints = 0;
   Ctx.workBigMoveStartPoints = 0;
   Ctx.workBigMoveStepPoints = 0;
   Ctx.workFarDistancePoints = 0;
   Ctx.geometryModeUsed = (int)GEOMETRY_MANUAL;
   Ctx.geometryCalculatedTime = 0;
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
   Ctx.pendingActionType = PENDING_NONE;
   Ctx.pendingOperation = "";
   Ctx.pendingNextState = STATE_IDLE;
   Ctx.pendingTicket = 0;
   Ctx.pendingLot = 0.0;
   Ctx.pendingAttempts = 0;
   Ctx.pendingOperationStartTime = 0;
   Ctx.pendingBigPositionId = 0;
   Ctx.pendingSmallPositionId = 0;
   Ctx.pendingRealNet = 0.0;
   Ctx.pendingCloseFarBudget = 0.0;
   Ctx.pendingReserveAdd = 0.0;
   Ctx.pendingSmallReserveAdd = 0.0;
   Ctx.pendingReserveApplied = false;
   Ctx.pendingSmallReserveApplied = false;
   Ctx.pendingCloseFarLot = 0.0;
   Ctx.pendingDirection = DIR_NONE;
   Ctx.pendingComment = "";
   Ctx.savedSmallDirection = DIR_NONE;
   Ctx.savedSmallClosePrice = 0.0;
   Ctx.savedSmallTouchPrice = 0.0;
   Ctx.savedSmallOpenPrice = 0.0;
   Ctx.savedSmallLot = 0.0;
   Ctx.oldFarTicket = 0;
   Ctx.oldFarLot = 0.0;
   Ctx.oldFarDirection = DIR_NONE;
   Ctx.oldFarOpenPrice = 0.0;
   Ctx.smallScenarioRealBefore = 0.0;
   Ctx.smallScenarioRealAfter = 0.0;
   ClearCycleGeometry(false, GEOMETRY_CLEAR_RESET_CONTEXT);
   Ctx.cycleId = (ulong)TimeCurrent();
}

double CalcRealRecoveryPL()
{
   if(IsInternalSimulationMode())
      Ctx.cycleCurrentBalance = Ctx.cycleStartBalance + Ctx.realCyclePL;
   else
      Ctx.cycleCurrentBalance = AccountInfoDouble(ACCOUNT_BALANCE);

   Ctx.cycleBalancePL = Ctx.cycleCurrentBalance - Ctx.cycleStartBalance;
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
            if(StringFind(dealComment, "INITIAL_BUY") >= 0 || StringFind(dealComment, "INITIAL_SELL") >= 0)
            {
               LogInfo(StringFormat("REAL_RECOVERY_SKIP_INITIAL_LOCK Deal=%I64u Comment=%s", dealTicket, dealComment));
               continue;
            }
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
      if(ok) ok = ValidateNoOrphanManagedPositions() && ok;
      return ok;
   }

   for(int j = 0; j < count; j++)
      ok = ClosePositionByTicketWithComment(tickets[j], lots[j], closeComment) && ok;

   if(ok) ok = ValidateNoOrphanManagedPositions() && ok;
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
          IsProfitSystemCloseComment(Ctx.lastSystemCloseComment);
}

void LogRealCycleMath(EAState state, double onTesterValue)
{
   bool passByRealPL = IsRealRecoveryPass();
   double initialDeposit = Ctx.cycleStartBalance - Ctx.initialIgnoredProfit;
   double accountPL = Ctx.cycleCurrentBalance - initialDeposit;
   double recoveryPL = Ctx.cycleCurrentBalance - Ctx.cycleStartBalance;
   bool passByAccountPL = accountPL > 0.0;
   PrintFormat(
      "REAL_CYCLE_MATH | State=%s InitialDeposit=%.2f InitialIgnoredProfit=%.2f CycleStartBalance=%.2f CurrentBalance=%.2f AccountPL=%.2f RecoveryPL=%.2f RealRecoveryPL=%.2f RealClosedProfit=%.2f RealClosedLoss=%.2f RealCommission=%.2f RealSwap=%.2f RealCosts=%.2f TheoreticalCyclePL=%.2f LastSystemCloseComment=%s LastCloseWasSystemClose=%s FinalCloseType=%s OnTesterValue=%.2f PassByAccountPL=%s PassByRecoveryPL=%s PassByRealPL=%s",
      StateToString(state),
      initialDeposit,
      Ctx.initialIgnoredProfit,
      Ctx.cycleStartBalance,
      Ctx.cycleCurrentBalance,
      accountPL,
      recoveryPL,
      Ctx.realRecoveryPL,
      Ctx.realClosedProfit,
      Ctx.realClosedLoss,
      Ctx.realCommission,
      Ctx.realSwap,
      Ctx.realCosts,
      Ctx.theoreticalCyclePL,
      Ctx.lastSystemCloseComment,
      Ctx.lastCloseWasSystemClose ? "YES" : "NO",
      Ctx.lastSystemCloseComment,
      onTesterValue,
      passByAccountPL ? "YES" : "NO",
      passByRealPL ? "YES" : "NO",
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
      passByRealPL,
      Ctx.lastCloseWasSystemClose,
      Ctx.lastSystemCloseComment,
      GeometryModeToString((GeometryModeEnum)Ctx.geometryModeUsed),
      EnumToString(ATRTimeframe),
      ATRPeriod,
      Ctx.cycleATRPoints,
      InitialRoundStep,
      BigStartRoundStep,
      BigStepRoundStep,
      FarDistanceRoundStep,
      WorkInitialTriggerPoints(),
      WorkBigMoveStartPoints(),
      WorkBigMoveStepPoints(),
      WorkFarDistancePoints(),
      FreezeGeometryPerCycle
   );
}


void UpdateFarFromSnapshot(PositionSnapshot &far)
{
   Ctx.farTicket = far.ticket;
   Ctx.farIdentifier = far.identifier;
   Ctx.farLot = NormalizeLotDown(far.lot);
   Ctx.farOpenPrice = far.openPrice;
   Ctx.farDirection = far.direction;
}


bool PromoteRemainingBigToNewFar()
{
   PositionSnapshot remainingBig;
   bool found = false;
   if(Ctx.bigTicket != 0)
      found = GetManagedPositionByTicket(Ctx.bigTicket, remainingBig);
   if(!found && Ctx.bigIdentifier != 0)
   {
      if(IsInternalSimulationMode())
      {
         for(int i = 0; i < ArraySize(SimPositions); i++)
         {
            if(SimPositions[i].exists && SimPositions[i].identifier == Ctx.bigIdentifier)
            {
               remainingBig = SimPositions[i];
               found = true;
               break;
            }
         }
      }
      else
      {
         for(int i = PositionsTotal() - 1; i >= 0; i--)
         {
            ulong ticket = PositionGetTicket(i);
            if(ticket == 0 || !PositionSelectByTicket(ticket))
               continue;
            PositionSnapshot candidate;
            if(!ReadSelectedPosition(candidate))
               continue;
            if(candidate.identifier == Ctx.bigIdentifier)
            {
               remainingBig = candidate;
               found = true;
               break;
            }
         }
      }
   }

   if(!found || !remainingBig.exists || remainingBig.ticket == 0 || remainingBig.identifier == 0)
   {
      LogError(StringFormat("PROMOTE_REMAINING_BIG_TO_FAR_FAILED Reason=BigNotFound BigTicket=%I64u BigIdentifier=%I64u", Ctx.bigTicket, Ctx.bigIdentifier));
      return false;
   }

   double actualVolume = GetActualPositionVolume(remainingBig.ticket);
   if(actualVolume <= VolumeMismatchToleranceLots)
      actualVolume = remainingBig.lot;
   actualVolume = NormalizeVolumeToStep(actualVolume);

   if(actualVolume <= VolumeMismatchToleranceLots)
   {
      LogError(StringFormat("PROMOTE_REMAINING_BIG_TO_FAR_FAILED Reason=ZeroVolume Ticket=%I64u Identifier=%I64u", remainingBig.ticket, remainingBig.identifier));
      return false;
   }

   if(Ctx.bigDirection != DIR_NONE && remainingBig.direction != Ctx.bigDirection)
   {
      LogError(StringFormat("PROMOTE_REMAINING_BIG_TO_FAR_FAILED Reason=DirectionMismatch Ticket=%I64u Expected=%s Actual=%s", remainingBig.ticket, DirectionToString(Ctx.bigDirection), DirectionToString(remainingBig.direction)));
      return false;
   }

   double currentPrice = Ctx.savedSmallTouchPrice;
   if(currentPrice <= 0.0 && Ctx.savedSmallDirection != DIR_NONE)
      currentPrice = CurrentPriceForSmallTouch(Ctx.savedSmallDirection);
   if(currentPrice <= 0.0)
      currentPrice = ExitPriceForDirection(remainingBig.direction);

   ulong oldBigTicket = Ctx.bigTicket;
   ulong oldBigIdentifier = Ctx.bigIdentifier;
   double oldBigLot = Ctx.bigLot;

   Ctx.farTicket = remainingBig.ticket;
   Ctx.farIdentifier = remainingBig.identifier;
   Ctx.farLot = actualVolume;
   Ctx.farOpenPrice = remainingBig.openPrice;
   Ctx.farDirection = remainingBig.direction;
   Ctx.effectiveFarDistancePoints = CalcRealPriceFarDistancePoints(currentPrice, Ctx.farOpenPrice);

   Ctx.bigTicket = 0;
   Ctx.bigIdentifier = 0;
   Ctx.bigLot = 0.0;
   Ctx.bigDirection = DIR_NONE;
   Ctx.bigOpenPrice = 0.0;
   Ctx.smallTicket = 0;
   Ctx.smallIdentifier = 0;
   Ctx.smallLot = 0.0;
   Ctx.smallDirection = DIR_NONE;
   Ctx.smallOpenPrice = 0.0;

   SaveState();
   LogInfo(StringFormat("PROMOTED_BIG_AS_FAR_RECOVERED OldBigTicket=%I64u OldBigIdentifier=%I64u OldBigLot=%.2f FarTicket=%I64u FarIdentifier=%I64u FarLot=%.2f FarDirection=%s FarOpenPrice=%.5f EffectiveFarDistancePoints=%.2f",
                        oldBigTicket,
                        oldBigIdentifier,
                        oldBigLot,
                        Ctx.farTicket,
                        Ctx.farIdentifier,
                        Ctx.farLot,
                        DirectionToString(Ctx.farDirection),
                        Ctx.farOpenPrice,
                        Ctx.effectiveFarDistancePoints));
   return true;
}

bool TryRecoverPromotedBigAsFar(string reason)
{
   bool smallAbsent = (Ctx.smallTicket == 0 || GetActualPositionVolume(Ctx.smallTicket) <= VolumeMismatchToleranceLots);
   bool farAbsent = (Ctx.farTicket == 0 || GetActualPositionVolume(Ctx.farTicket) <= VolumeMismatchToleranceLots);
   bool bigPresent = (Ctx.bigTicket != 0 && GetActualPositionVolume(Ctx.bigTicket) > VolumeMismatchToleranceLots);

   if(!farAbsent || !smallAbsent || !bigPresent)
      return false;

   if(!PromoteRemainingBigToNewFar())
      return false;

   ClearPendingOperationContext();
   State = STATE_FAR_ACTIVE;
   Ctx.lastError = "";
   SaveState();
   LogInfo("[Recovery] PROMOTED_BIG_AS_FAR_RECOVERED Reason=" + reason + " State=STATE_FAR_ACTIVE");
   return true;
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
      Ctx.bigIdentifier = big.identifier;
      Ctx.bigLot = big.lot;
      Ctx.bigOpenPrice = big.openPrice;
      Ctx.bigDirection = big.direction;
   }

   if(smallFound)
   {
      Ctx.smallTicket = small.ticket;
      Ctx.smallIdentifier = small.identifier;
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
      RegisterInitialLockFromSnapshots(initialBuy, initialSell, "existing initial BUY/SELL lock found");
      ResetCycleGeometryFields("OpenInitialLock new cycle");
      InitializeCycleGeometry();
      PrintGeometryDiagnostics();
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
      RegisterInitialLockFromSnapshots(initialBuy, initialSell, "initial lock opened");
      ResetCycleGeometryFields("OpenInitialLock new cycle");
      InitializeCycleGeometry();
      PrintGeometryDiagnostics();
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

   if(buyProfitPoints >= WorkInitialTriggerPoints())
   {
      if(!ClosePositionByTicket(initialBuy.ticket, initialBuy.lot))
      {
         SetState(STATE_ERROR, "failed to close initial profitable BUY");
         return;
      }

      ConvertInitialLockToFar(initialSell, initialBuy, "INITIAL_BUY_CLOSED_SELL_TO_FAR");
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
      Ctx.initialFarDistancePoints = WorkInitialTriggerPoints();
      Ctx.cumulativeBigMovePoints = 0.0;

      LogInfo(StringFormat("CLOSE INITIAL PROFIT POSITION direction=BUY InitialProfit=%.2f InitialProfitIgnored=%s ReserveBeforeRecovery=%.2f RecoveryReserveAfterInitialClose=%.2f", initialBuy.profitMoney, Ctx.initialProfitIgnored ? "true" : "false", 0.0, Ctx.totalReserve));
      LogInfo(StringFormat("Initial BUY plus closed at %.1f points and ignored. Far is SELL %.2f", buyProfitPoints, Ctx.farLot));
      LogFarPosition(Ctx);
      SetState(STATE_FAR_ACTIVE, "initial plus ignored, remaining SELL is Far");
      return;
   }

   if(sellProfitPoints >= WorkInitialTriggerPoints())
   {
      if(!ClosePositionByTicket(initialSell.ticket, initialSell.lot))
      {
         SetState(STATE_ERROR, "failed to close initial profitable SELL");
         return;
      }

      ConvertInitialLockToFar(initialBuy, initialSell, "INITIAL_SELL_CLOSED_BUY_TO_FAR");
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
      Ctx.initialFarDistancePoints = WorkInitialTriggerPoints();
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
      SetState(STATE_MAX_LEVELS_DECISION, "WorkMaxHarvestLevels reached; route to explicit max-levels decision before any new Big/Small");
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

   datetime bigOpenStartTime = TimeCurrent();
   bool bigOpened = OpenPosition(Ctx.bigDirection, Ctx.bigLot, bigComment);

   if(!bigOpened)
   {
      SetState(STATE_ERROR, "failed to open Big leg of Big/Small pair");
      return;
   }

   PositionResolutionResult bigResolution;
   if(!ResolveOpenedPositionAfterOpen(bigComment, Ctx.bigDirection, Ctx.bigLot, 0, bigOpenStartTime, bigResolution))
   {
      SetState(STATE_POSITION_RESOLUTION_ERROR, "POSITION_RESOLUTION_FAILED OpenBigSmall Big");
      return;
   }
   if(!ApplyResolvedPositionToBig(bigResolution))
      return;

   datetime smallOpenStartTime = TimeCurrent();
   bool smallOpened = OpenPosition(Ctx.smallDirection, Ctx.smallLot, smallComment);

   if(!smallOpened)
   {
      MarkSystemClose("ROLLBACK_BIG_WITHOUT_SMALL");
      ClosePositionByTicketWithComment(Ctx.bigTicket, Ctx.bigLot, "ROLLBACK_BIG_WITHOUT_SMALL");
      SetState(STATE_ERROR, "failed to open Small leg; Big leg rolled back");
      return;
   }

   PositionResolutionResult smallResolution;
   if(!ResolveOpenedPositionAfterOpen(smallComment, Ctx.smallDirection, Ctx.smallLot, 0, smallOpenStartTime, smallResolution))
   {
      SetState(STATE_POSITION_RESOLUTION_ERROR, "POSITION_RESOLUTION_FAILED OpenBigSmall Small");
      return;
   }
   if(!ApplyResolvedPositionToSmall(smallResolution))
      return;

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

bool CalculateRealNetForClosedPositions(ulong firstPositionId, ulong secondPositionId, datetime fromTime, double &firstNet, double &secondNet, double &commission, double &swap)
{
   firstNet = 0.0;
   secondNet = 0.0;
   commission = 0.0;
   swap = 0.0;
   bool found = false;

   if(IsInternalSimulationMode())
   {
      double totalNet = 0.0;
      double profit = 0.0;
      double loss = 0.0;
      found = SimRecalculateClosedStats(totalNet, profit, loss);
      firstNet = profit;
      secondNet = loss;
      return found;
   }

   datetime startTime = fromTime > 0 ? fromTime - 60 : Ctx.cycleStartTime;
   datetime endTime = TimeCurrent() + 86400;
   if(!HistorySelect(startTime, endTime))
      return false;

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

      ulong positionId = (ulong)HistoryDealGetInteger(dealTicket, DEAL_POSITION_ID);
      if(positionId != firstPositionId && positionId != secondPositionId)
         continue;

      double dealProfit = HistoryDealGetDouble(dealTicket, DEAL_PROFIT);
      double dealCommission = HistoryDealGetDouble(dealTicket, DEAL_COMMISSION);
      double dealSwap = HistoryDealGetDouble(dealTicket, DEAL_SWAP);
      double dealNet = dealProfit + dealCommission + dealSwap;
      commission += dealCommission;
      swap += dealSwap;

      if(positionId == firstPositionId)
         firstNet += dealNet;
      if(positionId == secondPositionId)
         secondNet += dealNet;

      found = true;
   }

   return found;
}

void SetPendingOperation(PendingActionType actionType, string operation, EAState pendingState, ulong ticket, double lot, string comment, EAState nextState, string reason)
{
   Ctx.pendingActionType = actionType;
   Ctx.pendingOperation = operation;
   Ctx.pendingNextState = nextState;
   Ctx.pendingTicket = ticket;
   Ctx.pendingLot = lot;
   Ctx.pendingComment = comment;
   Ctx.pendingAttempts = 0;
   Ctx.retryTicket = ticket;
   Ctx.retryLot = lot;
   Ctx.retryAttempts = 0;
   Ctx.lastRetryState = pendingState;
   Ctx.lastRetryLogTime = 0;
   Ctx.pendingOperationStartTime = TimeCurrent();

   if(actionType == PENDING_CLOSE_BIG_FULL || actionType == PENDING_CLOSE_BIG_PARTIAL)
      Ctx.pendingDirection = Ctx.bigDirection;
   else if(actionType == PENDING_CLOSE_SMALL_FULL)
      Ctx.pendingDirection = Ctx.smallDirection;
   else if(actionType == PENDING_CLOSE_OLD_FAR_FULL || actionType == PENDING_CLOSE_FAR_FULL || actionType == PENDING_CLOSE_FAR_PARTIAL || actionType == PENDING_MAX_LEVELS_FINAL_CLOSE || actionType == PENDING_STOP_MAX_LEVELS_CLOSE)
      Ctx.pendingDirection = Ctx.farDirection;
   else
      Ctx.pendingDirection = DIR_NONE;

   LogInfo(StringFormat("PENDING_CONTRACT_CREATED TargetState=%s Action=%d Operation=%s Ticket=%I64u Lot=%.2f Comment=%s NextState=%s", StateToString(pendingState), (int)actionType, operation, ticket, lot, comment, StateToString(nextState)));
   SaveState();
   if(!ValidatePendingContract(pendingState))
   {
      SetState(STATE_INTEGRITY_ERROR, "INVALID_PENDING_CONTRACT before " + StateToString(pendingState));
      return;
   }
   SetState(pendingState, reason + " | pendingOperation=" + operation + " pendingNextState=" + StateToString(nextState) + " comment=" + comment);
}

void SetRetryContext(EAState pendingState, ulong ticket, double lot, string reason)
{
   Ctx.lastRetryState = pendingState;
   Ctx.retryTicket = ticket;
   Ctx.retryLot = lot;
   Ctx.retryAttempts = 0;
   Ctx.pendingActionType = PENDING_NONE;
   Ctx.pendingOperation = StateToString(pendingState);
   Ctx.pendingNextState = STATE_RECOVERY_PENDING;
   Ctx.pendingTicket = ticket;
   Ctx.pendingLot = lot;
   Ctx.pendingAttempts = 0;
   Ctx.lastRetryLogTime = 0;
   SetState(pendingState, reason);
}

bool ApplyPendingCloseSuccessToContext()
{
   switch(Ctx.pendingActionType)
   {
      case PENDING_CLOSE_BIG_FULL:
         if(!VerifyFullClose(Ctx.bigTicket, "PENDING_CLOSE_BIG_FULL"))
         {
            Ctx.bigLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.bigTicket));
            Ctx.retryLot = Ctx.bigLot;
            Ctx.pendingLot = Ctx.bigLot;
            SaveState();
            return false;
         }
         ClearBigContext("full Big close confirmed by VerifyFullClose");
         if(!ValidateNoOrphanManagedPositions()) return false;
         break;

      case PENDING_CLOSE_SMALL_FULL:
         if(!VerifyFullClose(Ctx.smallTicket, "PENDING_CLOSE_SMALL_FULL"))
         {
            Ctx.smallLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.smallTicket));
            Ctx.retryLot = Ctx.smallLot;
            Ctx.pendingLot = Ctx.smallLot;
            SaveState();
            return false;
         }
         ClearSmallContext("full Small close confirmed by VerifyFullClose");
         if(!ValidateNoOrphanManagedPositions()) return false;
         break;

      case PENDING_CLOSE_BIG_PARTIAL:
      {
         if(!RefreshBigVolumeFromTerminal("PENDING_CLOSE_BIG_PARTIAL"))
            ClearBigContext("PENDING_CLOSE_BIG_PARTIAL fully closed or missing after retry");
         if(!ValidateNoOrphanManagedPositions()) return false;
         break;
      }

      case PENDING_CLOSE_FAR_PARTIAL:
      {
         if(!RefreshFarVolumeFromTerminal("PENDING_CLOSE_FAR_PARTIAL"))
            ClearFarContext("PENDING_CLOSE_FAR_PARTIAL fully closed or missing after retry");
         if(!ValidateNoOrphanManagedPositions()) return false;
         break;
      }

      case PENDING_CLOSE_OLD_FAR_FULL:
      case PENDING_CLOSE_FAR_FULL:
      case PENDING_MAX_LEVELS_FINAL_CLOSE:
      case PENDING_STOP_MAX_LEVELS_CLOSE:
      {
         if(!VerifyFullClose(Ctx.farTicket, "PENDING_FULL_FAR_CLOSE"))
         {
            Ctx.farLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.farTicket));
            Ctx.retryLot = Ctx.farLot;
            Ctx.pendingLot = Ctx.farLot;
            SaveState();
            return false;
         }
         ClearFarContext("full Far close confirmed by VerifyFullClose");
         if(!ValidateNoOrphanManagedPositions()) return false;
         break;
      }

      default:
         break;
   }
   return true;
}

void ClearPendingOperationContext()
{
   Ctx.pendingActionType = PENDING_NONE;
   Ctx.pendingOperation = "";
   Ctx.pendingComment = "";
   Ctx.pendingNextState = STATE_IDLE;
   Ctx.pendingTicket = 0;
   Ctx.pendingLot = 0.0;
   Ctx.retryTicket = 0;
   Ctx.retryLot = 0.0;
   Ctx.pendingAttempts = 0;
   Ctx.retryAttempts = 0;
   Ctx.pendingDirection = DIR_NONE;
   Ctx.pendingOperationStartTime = 0;
   Ctx.lastRetryState = STATE_IDLE;
   Ctx.lastRetryLogTime = 0;
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
   Ctx.pendingAttempts = Ctx.retryAttempts;
   datetime now = TimeCurrent();
   if(Ctx.lastRetryLogTime == 0 || RetryLogIntervalSeconds <= 0 || now - Ctx.lastRetryLogTime >= RetryLogIntervalSeconds)
   {
      Ctx.lastRetryLogTime = now;
      LogInfo(StringFormat("RETRY_CLOSE %s attempt=%d/%d Ticket=%I64u Lot=%.2f Comment=%s RiskGateOk=%s", operationName, Ctx.retryAttempts, MaxCloseRetryAttempts, Ctx.retryTicket, Ctx.retryLot, comment, Ctx.riskGateOk ? "YES" : "NO"));
   }

   MarkSystemClose(comment);
   if(ClosePositionByTicketWithComment(Ctx.retryTicket, Ctx.retryLot, comment))
   {
      EAState nextState = (Ctx.pendingNextState != STATE_IDLE ? Ctx.pendingNextState : successState);
      if(!ApplyPendingCloseSuccessToContext())
      {
         if(State != STATE_RECOVERY_MISMATCH)
            SetState(Ctx.lastRetryState, operationName + " FULL_CLOSE_INCOMPLETE; retry remains pending");
         return false;
      }
      ClearPendingOperationContext();
      SetState(nextState, operationName + " retry close succeeded; continuing with " + StateToString(nextState));
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
   RetryCloseTicket("RetryCloseBig", "RETRY_CLOSE_BIG", Ctx.pendingNextState);
}

void RetryCloseSmall()
{
   RetryCloseTicket("RetryCloseSmall", "RETRY_CLOSE_SMALL", Ctx.pendingNextState);
}

void RetryCloseOldFar()
{
   RetryCloseTicket("RetryCloseOldFar", "RETRY_CLOSE_OLD_FAR", Ctx.pendingNextState);
}

void RetryCloseBigPart()
{
   RetryCloseTicket("RetryCloseBigPart", "RETRY_CLOSE_BIG_PART", Ctx.pendingNextState);
}

void RetryCloseNewFar()
{
   RetryCloseTicket("RetryCloseNewFar", "RETRY_CLOSE_NEW_FAR", Ctx.pendingNextState);
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
      if(!ValidateNoOrphanManagedPositions())
         return;
      if(!ValidateStatePositionConsistency())
         return;
      if(!ValidateCurrentStateIntegrity())
         return;
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
   LogInfo(StringFormat("BIG_SCENARIO_START Level=%d FarTicket=%I64u BigTicket=%I64u SmallTicket=%I64u FarLot=%.2f BigLot=%.2f SmallLot=%.2f TotalReserve=%.2f",
                        Ctx.harvestLevel, Ctx.farTicket, Ctx.bigTicket, Ctx.smallTicket, Ctx.farLot, Ctx.bigLot, Ctx.smallLot, Ctx.totalReserve));
   SetState(STATE_BIG_HARVEST_CLOSE_BIG, "BigHarvest phase FSM start");
}

void ProcessBigHarvestCloseBig()
{
   PositionSnapshot big;
   PositionSnapshot small;
   if(!RefreshFar() || !RefreshBigSmall(big, small))
   {
      SetState(STATE_ERROR, "cannot start phased BigHarvest without Far/Big/Small");
      return;
   }

   double bigClosePrice = ExitPriceForDirection(Ctx.bigDirection);
   Ctx.pendingOperationStartTime = TimeCurrent();
   Ctx.pendingBigPositionId = big.identifier;
   Ctx.pendingSmallPositionId = small.identifier;
   Ctx.currentBigMovePoints = CalcMovePointsBetween(Ctx.bigOpenPrice, bigClosePrice);
   Ctx.cumulativeBigMovePoints += Ctx.currentBigMovePoints;
   Ctx.currentClosePrice = bigClosePrice;
   Ctx.effectiveFarDistancePoints = CalcEffectiveFarDistancePoints(
      Ctx.initialFarDistancePoints,
      Ctx.currentBigMovePoints,
      Ctx.cumulativeBigMovePoints,
      Ctx.currentClosePrice,
      Ctx.farOpenPrice
   );

   if(!ClosePositionByTicket(Ctx.bigTicket, Ctx.bigLot))
   {
      SetPendingOperation(PENDING_CLOSE_BIG_FULL, "BIG_HARVEST_CLOSE_BIG", STATE_CLOSE_BIG_PENDING, Ctx.bigTicket, Ctx.bigLot, "RETRY_CLOSE_BIG", STATE_BIG_HARVEST_CLOSE_SMALL, "BigHarvest phase close Big failed; retry pending");
      return;
   }

   if(!VerifyFullClose(Ctx.bigTicket, "BIG_HARVEST_CLOSE_BIG"))
   {
      Ctx.bigLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.bigTicket));
      SetPendingOperation(PENDING_CLOSE_BIG_FULL, "BIG_HARVEST_CLOSE_BIG", STATE_CLOSE_BIG_PENDING, Ctx.bigTicket, Ctx.bigLot, "RETRY_CLOSE_BIG", STATE_BIG_HARVEST_CLOSE_SMALL, "FULL_CLOSE_INCOMPLETE after BigHarvest Big close; retry pending");
      return;
   }
   ClearBigContext("BigHarvest close Big phase confirmed by VerifyFullClose");
   LogInfo(StringFormat("BIG_CLOSED Level=%d BigPositionId=%I64u CurrentBigMovePoints=%.1f EffectiveFarDistancePoints=%.1f",
                        Ctx.harvestLevel, Ctx.pendingBigPositionId, Ctx.currentBigMovePoints, Ctx.effectiveFarDistancePoints));
   if(!ValidateNoOrphanManagedPositions()) return;
   SetState(STATE_BIG_HARVEST_CLOSE_SMALL, "BigHarvest close Big phase done");
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
   SetState(STATE_SMALL_CLOSE_SMALL, "Small-at-Far phase FSM start");
}


void ProcessSmallScenario()
{
   SetState(STATE_SMALL_CLOSE_SMALL, "Small Scenario phase FSM start");
}


void ProcessFinalClose()
{
   if(!RefreshFar())
   {
      RecalculateRealCycleStatsFromHistory();
      if(Ctx.realRecoveryPL > 0.0)
         MarkSystemClose("CLOSED_PROFIT");
      else
         MarkSystemClose("CLOSED_RECOVERY_LOSS");
      SetState(Ctx.realRecoveryPL > 0.0 ? STATE_CLOSED_PROFIT : STATE_CLOSED_RECOVERY_LOSS, "Far already absent at final close");
      LogRealCycleMath(State, IsRealRecoveryPass() ? Ctx.realRecoveryPL : -1.0);
      return;
   }

   double farRemainLoss = CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
   Ctx.cycleFinalPL = Ctx.totalReserve - farRemainLoss;
   Ctx.theoreticalCyclePL = Ctx.cycleFinalPL;

   double projectedCurrentPrice = CurrentPriceForDirectionClose(Ctx.farDirection);
   double projectedFarPL = CalculateFarFloatingPL(projectedCurrentPrice);
   double projectedBalanceAfterFinalClose = AccountInfoDouble(ACCOUNT_BALANCE) + projectedFarPL;
   double projectedRecoveryPLAfterFinalClose = projectedBalanceAfterFinalClose - Ctx.cycleStartBalance;
   LogInfo(StringFormat("FINAL_CLOSE_PROFIT_FORECAST ProjectedBalanceAfterFinalClose=%.2f ProjectedRecoveryPLAfterFinalClose=%.2f CycleStartBalance=%.2f FarFloatingPL=%.2f",
                        projectedBalanceAfterFinalClose,
                        projectedRecoveryPLAfterFinalClose,
                        Ctx.cycleStartBalance,
                        projectedFarPL));
   if(projectedRecoveryPLAfterFinalClose <= 0.0)
   {
      Ctx.finalCloseAllowed = false;
      if(Ctx.harvestLevel >= WorkMaxHarvestLevels)
         SetState(STATE_MAX_LEVELS_DECISION, "FINAL_CLOSE_STOP: projected recovery PL is not positive");
      else
         SetState(STATE_FAR_ACTIVE, "FINAL_CLOSE_STOP: wait for positive recovery PL");
      return;
   }

   LogCycleMathDetailed(
      Ctx.harvestLevel,
      "FINAL_CLOSE_PROFIT",
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
      farRemainLoss,
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
      IsRealRecoveryPass(),
      Ctx.lastCloseWasSystemClose,
      Ctx.lastSystemCloseComment,
      GeometryModeToString((GeometryModeEnum)Ctx.geometryModeUsed),
      EnumToString(ATRTimeframe),
      ATRPeriod,
      Ctx.cycleATRPoints,
      InitialRoundStep,
      BigStartRoundStep,
      BigStepRoundStep,
      FarDistanceRoundStep,
      WorkInitialTriggerPoints(),
      WorkBigMoveStartPoints(),
      WorkBigMoveStepPoints(),
      WorkFarDistancePoints(),
      FreezeGeometryPerCycle
   );

   MarkSystemClose("FINAL_CLOSE_PROFIT");
   if(!ClosePositionByTicketWithComment(Ctx.farTicket, Ctx.farLot, "FINAL_CLOSE_PROFIT"))
   {
      SetPendingOperation(PENDING_CLOSE_FAR_FULL, "FINAL_CLOSE_NEW_FAR", STATE_CLOSE_NEW_FAR_PENDING, Ctx.farTicket, Ctx.farLot, "RETRY_FINAL_CLOSE", STATE_CLOSED_PROFIT, "failed to close Far during FinalClose; retry pending");
      return;
   }

   LogInfo(StringFormat(
      "FinalClose completed: FarRemainLoss=%.2f TotalReserve=%.2f CycleFinalPL=%.2f",
      farRemainLoss,
      Ctx.totalReserve,
      Ctx.cycleFinalPL
   ));

   if(!VerifyFullClose(Ctx.farTicket, "FINAL_CLOSE_PROFIT"))
   {
      Ctx.farLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.farTicket));
      SetPendingOperation(PENDING_CLOSE_FAR_FULL, "FINAL_CLOSE_NEW_FAR", STATE_CLOSE_NEW_FAR_PENDING, Ctx.farTicket, Ctx.farLot, "RETRY_FINAL_CLOSE", STATE_CLOSED_PROFIT, "FULL_CLOSE_INCOMPLETE after FinalClose; retry pending");
      return;
   }
   ClearFarContext("FINAL_CLOSE_PROFIT confirmed by VerifyFullClose");
   if(!ValidateNoOrphanManagedPositions()) return;
   SetState(STATE_CLOSED_PROFIT, "cycle closed in profit; no new levels");
   RecalculateRealCycleStatsFromHistory();
   LogRealCycleMath(State, IsRealRecoveryPass() ? Ctx.realRecoveryPL : -1.0);
}

void ProcessBigHarvestCloseSmall()
{
   if(Ctx.smallTicket == 0 || Ctx.smallLot <= 0.0)
   {
      SetState(STATE_BIG_HARVEST_CALC_NET, "BigHarvest Small already closed; continue to real net calculation");
      return;
   }

   if(!ClosePositionByTicket(Ctx.smallTicket, Ctx.smallLot))
   {
      SetPendingOperation(PENDING_CLOSE_SMALL_FULL, "BIG_HARVEST_CLOSE_SMALL", STATE_CLOSE_SMALL_PENDING, Ctx.smallTicket, Ctx.smallLot, "RETRY_CLOSE_SMALL", STATE_BIG_HARVEST_CALC_NET, "BigHarvest phase close Small failed; retry pending");
      return;
   }

   if(!VerifyFullClose(Ctx.smallTicket, "BIG_HARVEST_CLOSE_SMALL"))
   {
      Ctx.smallLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.smallTicket));
      SetPendingOperation(PENDING_CLOSE_SMALL_FULL, "BIG_HARVEST_CLOSE_SMALL", STATE_CLOSE_SMALL_PENDING, Ctx.smallTicket, Ctx.smallLot, "RETRY_CLOSE_SMALL", STATE_BIG_HARVEST_CALC_NET, "FULL_CLOSE_INCOMPLETE after BigHarvest Small close; retry pending");
      return;
   }
   ClearSmallContext("BigHarvest close Small phase confirmed by VerifyFullClose");
   if(!ValidateNoOrphanManagedPositions()) return;
   SetState(STATE_BIG_HARVEST_CALC_NET, "BigHarvest Small close phase done");
}

void ProcessBigHarvestCalcNet()
{
   RecalculateRealCycleStatsFromHistory();
   double realClosedBigProfit = 0.0;
   double realClosedSmallProfit = 0.0;
   double realCommission = 0.0;
   double realSwap = 0.0;
   bool foundDeals = CalculateRealNetForClosedPositions(Ctx.pendingBigPositionId, Ctx.pendingSmallPositionId, Ctx.pendingOperationStartTime, realClosedBigProfit, realClosedSmallProfit, realCommission, realSwap);
   double realBigHarvestNet = realClosedBigProfit + realClosedSmallProfit;
   Ctx.pendingRealNet = realBigHarvestNet;

   if(foundDeals && realBigHarvestNet > 0.0)
   {
      Ctx.pendingReserveAdd = realBigHarvestNet * WorkReserveShare;
      Ctx.pendingCloseFarBudget = realBigHarvestNet * WorkCloseFarShare;
   }
   else
   {
      Ctx.pendingReserveAdd = 0.0;
      Ctx.pendingCloseFarBudget = 0.0;
   }

   Ctx.pendingCloseFarLot = CalcCloseFarLotRounded(CalcCloseFarLotRaw(Ctx.pendingCloseFarBudget, Ctx.effectiveFarDistancePoints), Ctx.farLot);
   double closeFarLotRaw = CalcCloseFarLotRaw(Ctx.pendingCloseFarBudget, Ctx.effectiveFarDistancePoints);
   double closeFarActualCost = CalcFarRemainLoss(Ctx.pendingCloseFarLot, Ctx.effectiveFarDistancePoints);
   LogInfo(StringFormat("BIG_SCENARIO_NET ClosedBigNet=%.2f ClosedSmallNet=%.2f BigScenarioNet=%.2f Commission=%.2f Swap=%.2f", realClosedBigProfit, realClosedSmallProfit, realBigHarvestNet, realCommission, realSwap));
   LogInfo(StringFormat("BIG_PROFIT_SPLIT CloseFarBudget=%.2f ReserveAdd=%.2f CloseFarShare=%.5f ReserveShare=%.5f SplitSum=%.5f", Ctx.pendingCloseFarBudget, Ctx.pendingReserveAdd, WorkCloseFarShare, WorkReserveShare, WorkCloseFarShare + WorkReserveShare));
   LogInfo(StringFormat("CLOSE_FAR_BUDGET CloseFarBudget=%.2f CloseFarLotRaw=%.5f CloseFarLotRounded=%.2f CloseFarActualCost=%.2f FarLotBefore=%.2f", Ctx.pendingCloseFarBudget, closeFarLotRaw, Ctx.pendingCloseFarLot, closeFarActualCost, Ctx.farLot));
   LogInfo(StringFormat("RESERVE_ADD ReserveAdd=%.2f TotalReserveBefore=%.2f ReserveApplied=%s", Ctx.pendingReserveAdd, Ctx.totalReserve, Ctx.pendingReserveApplied ? "YES" : "NO"));
   WriteCycleMathCsv(
      Ctx.harvestLevel,
      "BIG_SCENARIO_AUDIT",
      Ctx.farLot,
      0.0,
      0.0,
      realBigHarvestNet,
      Ctx.pendingCloseFarBudget,
      Ctx.pendingReserveAdd,
      Ctx.totalReserve,
      CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints),
      false,
      STATE_BIG_HARVEST_CALC_NET,
      realClosedBigProfit,
      0.0,
      realClosedSmallProfit,
      0.0,
      realClosedBigProfit,
      0.0,
      closeFarLotRaw,
      Ctx.pendingCloseFarLot,
      NormalizeLotDown(MathMax(0.0, Ctx.farLot - Ctx.pendingCloseFarLot)),
      Ctx.reverseStrength,
      Ctx.projectedReserveCoverage,
      "BIG_PROFIT_SPLIT",
      closeFarActualCost <= Ctx.pendingCloseFarBudget + 0.000001 ? "" : "CloseFarActualCost exceeds CloseFarBudget",
      realBigHarvestNet,
      realBigHarvestNet,
      realCommission + realSwap,
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
      IsRealRecoveryPass(),
      Ctx.lastCloseWasSystemClose,
      Ctx.lastSystemCloseComment,
      GeometryModeToString((GeometryModeEnum)Ctx.geometryModeUsed),
      EnumToString(ATRTimeframe),
      ATRPeriod,
      Ctx.cycleATRPoints,
      InitialRoundStep,
      BigStartRoundStep,
      BigStepRoundStep,
      FarDistanceRoundStep,
      WorkInitialTriggerPoints(),
      WorkBigMoveStartPoints(),
      WorkBigMoveStepPoints(),
      WorkFarDistancePoints(),
      FreezeGeometryPerCycle
   );
   LogInfo(StringFormat("BIG_HARVEST_REAL_RESERVE BIG_HARVEST_REAL_DEALS_CALC BigPositionId=%I64u SmallPositionId=%I64u FoundDeals=%s RealClosedBigProfit=%.2f RealClosedSmallProfit=%.2f Commission=%.2f Swap=%.2f BigScenarioNet=%.2f ReserveAdd=%.2f CloseFarBudget=%.2f CloseFarLot=%.2f", Ctx.pendingBigPositionId, Ctx.pendingSmallPositionId, foundDeals ? "YES" : "NO", realClosedBigProfit, realClosedSmallProfit, realCommission, realSwap, realBigHarvestNet, Ctx.pendingReserveAdd, Ctx.pendingCloseFarBudget, Ctx.pendingCloseFarLot));
   SetState(STATE_BIG_HARVEST_CLOSE_FAR, "BigHarvest real deal reserve calculated");
}

void ProcessBigHarvestCloseFar()
{
   if(Ctx.pendingCloseFarLot <= 0.0)
   {
      SetState(STATE_BIG_HARVEST_CHECK_FINAL, "BigHarvest has no Far budget to close");
      return;
   }

   if(!ClosePositionByTicket(Ctx.farTicket, Ctx.pendingCloseFarLot))
   {
      SetPendingOperation(PENDING_CLOSE_FAR_PARTIAL, "BIG_HARVEST_CLOSE_FAR", STATE_CLOSE_NEW_FAR_PENDING, Ctx.farTicket, Ctx.pendingCloseFarLot, "RETRY_CLOSE_FAR_BUDGET", STATE_BIG_HARVEST_CHECK_FINAL, "BigHarvest close Far budget failed; retry pending");
      return;
   }

   if(!RefreshFarVolumeFromTerminal("BIG_HARVEST_CLOSE_FAR partial close"))
      ClearFarContext("BIG_HARVEST_CLOSE_FAR actual remaining Far volume is zero");
   LogInfo(StringFormat("PARTIAL_FAR_CLOSE CloseFarLot=%.2f CLOSE_FAR_BUDGET=%.2f", Ctx.pendingCloseFarLot, Ctx.pendingCloseFarBudget));
   LogInfo(StringFormat("FAR_REMAINING FarTicket=%I64u FarLot=%.2f EffectiveFarDistancePoints=%.1f", Ctx.farTicket, Ctx.farLot, Ctx.effectiveFarDistancePoints));
   if(!ValidateNoOrphanManagedPositions()) return;
   SetState(STATE_BIG_HARVEST_CHECK_FINAL, "BigHarvest Far budget close done");
}

void ProcessBigHarvestCheckFinal()
{
   if(!Ctx.pendingReserveApplied)
   {
      ApplyReserveCredit(RESERVE_EVENT_BIG_HARVEST_ADD, Ctx.pendingReserveAdd);
      Ctx.pendingReserveApplied = true;
   }
   Ctx.pendingReserveAdd = 0.0;
   Ctx.pendingReserveApplied = false;
   double farRemainLoss = CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
   Ctx.finalCloseAllowed = CalcFinalCloseAllowed(Ctx.totalReserve, Ctx.farLot, Ctx.effectiveFarDistancePoints);
   LogInfo(StringFormat("RESERVE_AFTER TotalReserve=%.2f FinalCloseAllowed=%s", Ctx.totalReserve, Ctx.finalCloseAllowed ? "YES" : "NO"));
   Ctx.cycleFinalPL = Ctx.totalReserve - farRemainLoss;
   if(Ctx.farLot <= 0.0)
   {
      RecalculateRealCycleStatsFromHistory();
      if(Ctx.realRecoveryPL > 0.0)
         MarkSystemClose("CLOSED_PROFIT");
      else
         MarkSystemClose("CLOSED_RECOVERY_LOSS");
      SetState(Ctx.realRecoveryPL > 0.0 ? STATE_CLOSED_PROFIT : STATE_CLOSED_RECOVERY_LOSS, "BigHarvest phase completed with Far fully closed");
   }
   else if(Ctx.finalCloseAllowed)
      SetState(STATE_FINAL_CLOSE, "BigHarvest phase reserve covers remaining Far");
   else if(Ctx.harvestLevel >= WorkMaxHarvestLevels)
      SetState(STATE_MAX_LEVELS_DECISION, "BigHarvest phase done at MaxHarvestLevels; decide residual Far");
   else
      SetState(STATE_FAR_ACTIVE, "BigHarvest phase done; continue next harvest level");
   LogInfo(StringFormat("BIG_SCENARIO_END Level=%d TotalReserve=%.2f FarLot=%.2f FinalCloseAllowed=%s NextState=%s", Ctx.harvestLevel, Ctx.totalReserve, Ctx.farLot, Ctx.finalCloseAllowed ? "YES" : "NO", StateToString(State)));
}

void ProcessSmallCloseSmall()
{
   PositionSnapshot big;
   PositionSnapshot small;
   if(!RefreshFar() || !RefreshBigSmall(big, small))
   {
      SetState(STATE_ERROR, "cannot start phased Small Scenario without Far/Big/Small");
      return;
   }

   Ctx.smallScenarioRealBefore = Ctx.realCyclePL;
   RecalculateRealCycleStatsFromHistory();
   Ctx.smallScenarioRealBefore = Ctx.realCyclePL;
   Ctx.pendingOperationStartTime = TimeCurrent();
   Ctx.pendingBigPositionId = big.identifier;
   Ctx.pendingSmallPositionId = small.identifier;

   Ctx.savedSmallDirection = Ctx.smallDirection;
   Ctx.savedSmallOpenPrice = Ctx.smallOpenPrice;
   Ctx.savedSmallLot = Ctx.smallLot;
   Ctx.savedSmallClosePrice = ExitPriceForDirection(Ctx.smallDirection);
   Ctx.savedSmallTouchPrice = CurrentPriceForSmallTouch(Ctx.smallDirection);

   if(!ClosePositionByTicket(Ctx.smallTicket, Ctx.smallLot))
   {
      SetPendingOperation(PENDING_CLOSE_SMALL_FULL, "SMALL_CLOSE_SMALL", STATE_CLOSE_SMALL_PENDING, Ctx.smallTicket, Ctx.smallLot, "RETRY_CLOSE_SMALL_AT_FAR", STATE_SMALL_CLOSE_OLD_FAR, "Small phase close Small failed; retry pending");
      return;
   }

   if(!VerifyFullClose(Ctx.smallTicket, "SMALL_CLOSE_SMALL"))
   {
      Ctx.smallLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.smallTicket));
      SetPendingOperation(PENDING_CLOSE_SMALL_FULL, "SMALL_CLOSE_SMALL", STATE_CLOSE_SMALL_PENDING, Ctx.smallTicket, Ctx.smallLot, "RETRY_CLOSE_SMALL_AT_FAR", STATE_SMALL_CLOSE_OLD_FAR, "FULL_CLOSE_INCOMPLETE after Small close Small; retry pending");
      return;
   }
   ClearSmallContext("Small close Small phase confirmed by VerifyFullClose");
   if(!ValidateNoOrphanManagedPositions()) return;
   SetState(STATE_SMALL_CLOSE_OLD_FAR, "Small close Small phase done");
}


void ProcessSmallCloseOldFar()
{
   if(Ctx.farTicket == 0 || Ctx.farLot <= 0.0)
   {
      SetState(STATE_SMALL_CLOSE_BIG_PART, "Small scenario old Far already closed; continue Big part");
      return;
   }

   Ctx.oldFarTicket = Ctx.farTicket;
   Ctx.oldFarLot = Ctx.farLot;
   Ctx.oldFarDirection = Ctx.farDirection;
   Ctx.oldFarOpenPrice = Ctx.farOpenPrice;

   if(!ClosePositionByTicket(Ctx.farTicket, Ctx.farLot))
   {
      SetPendingOperation(PENDING_CLOSE_OLD_FAR_FULL, "SMALL_CLOSE_OLD_FAR", STATE_CLOSE_OLD_FAR_PENDING, Ctx.farTicket, Ctx.farLot, "RETRY_CLOSE_OLD_FAR", STATE_SMALL_CLOSE_BIG_PART, "Small phase old Far close failed; retry pending");
      return;
   }

   if(!VerifyFullClose(Ctx.farTicket, "SMALL_CLOSE_OLD_FAR"))
   {
      Ctx.farLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.farTicket));
      SetPendingOperation(PENDING_CLOSE_OLD_FAR_FULL, "SMALL_CLOSE_OLD_FAR", STATE_CLOSE_OLD_FAR_PENDING, Ctx.farTicket, Ctx.farLot, "RETRY_CLOSE_OLD_FAR", STATE_SMALL_CLOSE_BIG_PART, "FULL_CLOSE_INCOMPLETE after Small old Far close; retry pending");
      return;
   }
   ClearFarContext("Small scenario old Far close confirmed by VerifyFullClose");
   if(!ValidateNoOrphanManagedPositions()) return;
   SetState(STATE_SMALL_CLOSE_BIG_PART, "Small scenario old Far close phase done; active OldFar context cleared");
}

void ProcessSmallCloseBigPart()
{
   double closeBigLotRounded = CalcCloseBigLotOnSmall(Ctx.bigLot);
   if(closeBigLotRounded <= 0.0)
   {
      SetState(STATE_SMALL_BUILD_NEW_FAR, "Small scenario has no Big part to close");
      return;
   }

   if(!ClosePositionByTicket(Ctx.bigTicket, closeBigLotRounded))
   {
      SetPendingOperation(PENDING_CLOSE_BIG_PARTIAL, "SMALL_CLOSE_BIG_PART", STATE_CLOSE_BIG_PART_PENDING, Ctx.bigTicket, closeBigLotRounded, "RETRY_CLOSE_BIG_PART", STATE_SMALL_BUILD_NEW_FAR, "Small phase Big part close failed; retry pending");
      return;
   }

   double beforeBigLot = Ctx.bigLot;
   double expectedRemaining = NormalizeVolumeToStep(MathMax(0.0, beforeBigLot - closeBigLotRounded));
   double actualRemaining = GetActualPositionVolume(Ctx.bigTicket);
   double difference = MathAbs(expectedRemaining - actualRemaining);
   LogInfo(StringFormat("BIG_PARTIAL_CLOSE_VERIFY ExpectedRemaining=%.2f ActualRemaining=%.2f Difference=%.5f", expectedRemaining, actualRemaining, difference));
   if(actualRemaining <= 0.0 || !VerifyPositionVolumeIntegrity("BIG_PARTIAL_CLOSE_VERIFY", expectedRemaining, actualRemaining))
   {
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "POSITION_VOLUME_INTEGRITY_FAIL after Small Big partial close");
      return;
   }

   Ctx.bigLot = actualRemaining;
   if(!ValidateNoOrphanManagedPositions()) return;
   SetState(STATE_SMALL_BUILD_NEW_FAR, "Small scenario Big part close phase done");
}

void ProcessSmallBuildNewFar()
{
   if(Ctx.savedSmallDirection == DIR_NONE)
   {
      LogError("SMALL_BUILD_NEW_FAR FAILED: savedSmallDirection is DIR_NONE");
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "SMALL_BUILD_NEW_FAR FAILED: savedSmallDirection is DIR_NONE");
      return;
   }

   if(!PromoteRemainingBigToNewFar())
   {
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "PROMOTE_REMAINING_BIG_TO_FAR_FAILED");
      return;
   }
   double expectedNextFarLoss = CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
   RecalculateRealCycleStatsFromHistory();
   Ctx.smallScenarioRealAfter = Ctx.realCyclePL;
   double smallScenarioRealNet = Ctx.smallScenarioRealAfter - Ctx.smallScenarioRealBefore;
   Ctx.pendingSmallReserveAdd = CalcSmallReserveAdd(smallScenarioRealNet);
   if(!Ctx.pendingSmallReserveApplied)
   {
      ApplyReserveCredit(RESERVE_EVENT_SMALL_HARVEST_ADD, Ctx.pendingSmallReserveAdd);
      Ctx.pendingSmallReserveApplied = true;
   }
   double smallReserveAdd = Ctx.pendingSmallReserveAdd;
   Ctx.pendingSmallReserveAdd = 0.0;
   Ctx.pendingSmallReserveApplied = false;
   LogInfo(StringFormat("SMALL_RESERVE_ADD SMALL_REAL_NET_CALC smallScenarioRealBefore=%.2f smallScenarioRealAfter=%.2f smallScenarioRealNet=%.2f SmallReserveAdd=%.2f expectedNextFarLoss=%.2f", Ctx.smallScenarioRealBefore, Ctx.smallScenarioRealAfter, smallScenarioRealNet, smallReserveAdd, expectedNextFarLoss));
   SetState(STATE_SMALL_CHECK_RESERVE, "Small scenario NewFar built from remaining Big");
}

void ProcessSmallCheckReserve()
{
   double farRemainLoss = CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
   Ctx.finalCloseAllowed = CalcFinalCloseAllowed(Ctx.totalReserve, Ctx.farLot, Ctx.effectiveFarDistancePoints);
   if(Ctx.finalCloseAllowed)
      SetState(STATE_FINAL_CLOSE, "Small scenario reserve covers NewFar");
   else if(Ctx.harvestLevel >= WorkMaxHarvestLevels)
      SetState(STATE_MAX_LEVELS_DECISION, "Small scenario reserve insufficient at MaxHarvestLevels; decide residual Far");
   else
      SetState(STATE_SMALL_OPEN_NEW_BIG, "Small scenario reserve insufficient; open next Big");
}


double CurrentPriceForDirectionClose(Direction dir)
{
   return ExitPriceForDirection(dir);
}

double CalculateFarFloatingPL(double closePrice)
{
   if(Ctx.farLot <= 0.0 || Ctx.farOpenPrice <= 0.0 || closePrice <= 0.0 || Ctx.farDirection == DIR_NONE)
      return 0.0;

   if(IsInternalSimulationMode())
      return CalcSignedPositionPL(Ctx.farDirection, Ctx.farLot, Ctx.farOpenPrice, closePrice);

   double profit = 0.0;
   ENUM_ORDER_TYPE orderType = (Ctx.farDirection == DIR_BUY ? ORDER_TYPE_BUY : ORDER_TYPE_SELL);
   if(OrderCalcProfit(orderType, _Symbol, Ctx.farLot, Ctx.farOpenPrice, closePrice, profit))
      return profit;

   return CalcSignedPositionPL(Ctx.farDirection, Ctx.farLot, Ctx.farOpenPrice, closePrice);
}

void LogMaxLevelsDecision(double currentPrice, double farFloatingPL, double farCloseLoss, string decision)
{
   double coverage = farCloseLoss > 0.0 ? Ctx.totalReserve / farCloseLoss : 999.0;
   LogInfo(StringFormat("[MAX_LEVELS_DECISION] harvestLevel=%d MaxHarvestLevels=%d farTicket=%I64u farLot=%.2f farDirection=%s farOpenPrice=%.5f currentPrice=%.5f farFloatingPL=%.2f totalReserve=%.2f farCloseLoss=%.2f reserveCoverage=%.4f decision=%s RiskGateOk=%s CloseFarOnMaxLevels=%s",
                        Ctx.harvestLevel,
                        WorkMaxHarvestLevels,
                        Ctx.farTicket,
                        Ctx.farLot,
                        DirectionToString(Ctx.farDirection),
                        Ctx.farOpenPrice,
                        currentPrice,
                        farFloatingPL,
                        Ctx.totalReserve,
                        farCloseLoss,
                        coverage,
                        decision,
                        Ctx.riskGateOk ? "YES" : "NO",
                        CloseFarOnMaxLevels ? "true" : "false"));
}

void ProcessMaxLevelsDecision()
{
   if(!RefreshFar())
   {
      LogMaxLevelsDecision(0.0, 0.0, 0.0, "NO_FAR_FOUND_SET_STOP_MAX_LEVELS");
      SetState(STATE_STOP_MAX_LEVELS, "Max levels reached and no residual Far found");
      return;
   }

   double currentPrice = CurrentPriceForDirectionClose(Ctx.farDirection);
   double farFloatingPL = CalculateFarFloatingPL(currentPrice);
   double farCloseLoss = MathMax(0.0, -farFloatingPL);
   Ctx.finalCloseAllowed = (Ctx.totalReserve >= farCloseLoss);

   if(Ctx.finalCloseAllowed)
   {
      LogMaxLevelsDecision(currentPrice, farFloatingPL, farCloseLoss, "FINAL_CLOSE_RESERVE_COVERS_FAR");
      MarkSystemClose("MAX_LEVELS_FINAL_CLOSE");
      if(!ClosePositionByTicketWithComment(Ctx.farTicket, Ctx.farLot, "MAX_LEVELS_FINAL_CLOSE"))
      {
         SetPendingOperation(PENDING_MAX_LEVELS_FINAL_CLOSE, "MAX_LEVELS_FINAL_CLOSE_FAR", STATE_MAX_LEVELS_FINAL_CLOSE_PENDING, Ctx.farTicket, Ctx.farLot, "MAX_LEVELS_FINAL_CLOSE", STATE_CLOSED_PROFIT, "Max levels reserve close failed; retry pending");
         return;
      }
      if(!VerifyFullClose(Ctx.farTicket, "MAX_LEVELS_FINAL_CLOSE"))
      {
         Ctx.farLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.farTicket));
         SetPendingOperation(PENDING_MAX_LEVELS_FINAL_CLOSE, "MAX_LEVELS_FINAL_CLOSE_FAR", STATE_MAX_LEVELS_FINAL_CLOSE_PENDING, Ctx.farTicket, Ctx.farLot, "MAX_LEVELS_FINAL_CLOSE", STATE_CLOSED_PROFIT, "FULL_CLOSE_INCOMPLETE after max-level final close; retry pending");
         return;
      }
      ClearFarContext("MAX_LEVELS_FINAL_CLOSE confirmed by VerifyFullClose");
      if(!ValidateNoOrphanManagedPositions()) return;
      RecalculateRealCycleStatsFromHistory();
      SetState(Ctx.realRecoveryPL > 0.0 ? STATE_CLOSED_PROFIT : STATE_CLOSED_RECOVERY_LOSS, "Max levels residual Far closed; classify by real recovery PL");
      return;
   }

   if(CloseFarOnMaxLevels)
   {
      LogMaxLevelsDecision(currentPrice, farFloatingPL, farCloseLoss, "STOP_MAX_LEVELS_CLOSE_FAR");
      MarkSystemClose("STOP_MAX_LEVELS_CLOSE_FAR");
      if(!ClosePositionByTicketWithComment(Ctx.farTicket, Ctx.farLot, "STOP_MAX_LEVELS_CLOSE_FAR"))
      {
         LogMaxLevelsDecision(currentPrice, farFloatingPL, farCloseLoss, "CLOSE_FAILED: retry pending");
         SetPendingOperation(PENDING_STOP_MAX_LEVELS_CLOSE, "STOP_MAX_LEVELS_CLOSE_FAR", STATE_STOP_MAX_LEVELS_CLOSE_PENDING, Ctx.farTicket, Ctx.farLot, "STOP_MAX_LEVELS_CLOSE_FAR", STATE_STOP_MAX_LEVELS, "Stop max levels Far close failed; retry pending");
         return;
      }
      if(!VerifyFullClose(Ctx.farTicket, "STOP_MAX_LEVELS_CLOSE_FAR"))
      {
         Ctx.farLot = NormalizeVolumeToStep(GetActualPositionVolume(Ctx.farTicket));
         SetPendingOperation(PENDING_STOP_MAX_LEVELS_CLOSE, "STOP_MAX_LEVELS_CLOSE_FAR", STATE_STOP_MAX_LEVELS_CLOSE_PENDING, Ctx.farTicket, Ctx.farLot, "STOP_MAX_LEVELS_CLOSE_FAR", STATE_STOP_MAX_LEVELS, "FULL_CLOSE_INCOMPLETE after stop max levels close; retry pending");
         return;
      }
      ClearFarContext("STOP_MAX_LEVELS_CLOSE_FAR confirmed by VerifyFullClose");
      if(!ValidateNoOrphanManagedPositions()) return;
      SetState(STATE_STOP_MAX_LEVELS, "MaxHarvestLevels reached; residual Far closed by STOP_MAX_LEVELS_CLOSE_FAR");
      return;
   }

   LogMaxLevelsDecision(currentPrice, farFloatingPL, farCloseLoss, "NOT_CLOSED: reserve insufficient and CloseFarOnMaxLevels=false");
   SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "MaxHarvestLevels reached; residual Far requires manual intervention");
}

void RetryMaxLevelsFinalClose()
{
   RetryCloseTicket("RetryMaxLevelsFinalClose", "MAX_LEVELS_FINAL_CLOSE", STATE_CLOSED_PROFIT);
}

void RetryStopMaxLevelsClose()
{
   RetryCloseTicket("RetryStopMaxLevelsClose", "STOP_MAX_LEVELS_CLOSE_FAR", STATE_STOP_MAX_LEVELS);
}

void RetryOpenNewBig()
{
   if(Ctx.harvestLevel >= WorkMaxHarvestLevels)
   {
      SetState(STATE_MAX_LEVELS_DECISION, "RetryOpenNewBig blocked: MaxHarvestLevels reached; no new Big/Small allowed");
      return;
   }

   if(Ctx.pendingActionType != PENDING_OPEN_BIG || State != STATE_OPEN_NEW_BIG_PENDING)
   {
      if(!PreparePendingOpenBigContext())
      {
         SetState(STATE_INTEGRITY_ERROR, "INVALID_PENDING_CONTRACT for STATE_OPEN_NEW_BIG_PENDING");
         return;
      }
   }

   if(!Ctx.riskGateOk && AllowRealTrading && StopOnRiskGateBlocked)
   {
      LogRiskGateBlocked("RetryOpenNewBig blocked by RiskGate; open retry remains pending");
      if(!ValidatePendingContract(STATE_OPEN_NEW_BIG_PENDING))
      {
         SetState(STATE_INTEGRITY_ERROR, "INVALID_PENDING_CONTRACT before STATE_OPEN_NEW_BIG_PENDING");
         return;
      }
      SetState(STATE_OPEN_NEW_BIG_PENDING, "Open NewBig blocked by RiskGate");
      return;
   }

   if(!ValidatePendingContract(STATE_OPEN_NEW_BIG_PENDING))
   {
      SetState(STATE_INTEGRITY_ERROR, "INVALID_PENDING_CONTRACT before RetryOpenNewBig");
      return;
   }

   Ctx.pendingAttempts++;

   datetime bigOpenStartTime = TimeCurrent();
   if(Ctx.pendingLot <= 0.0 || !OpenPosition(Ctx.pendingDirection, Ctx.pendingLot, Ctx.pendingComment))
   {
      if(MaxCloseRetryAttempts > 0 && Ctx.pendingAttempts >= MaxCloseRetryAttempts)
         SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "RetryOpenNewBig exceeded retry attempts");
      else
         SetState(STATE_OPEN_NEW_BIG_PENDING, "RetryOpenNewBig failed; retry pending");
      return;
   }

   PositionResolutionResult bigResolution;
   if(!ResolveOpenedPositionAfterOpen(Ctx.pendingComment, Ctx.pendingDirection, Ctx.pendingLot, 0, bigOpenStartTime, bigResolution))
   {
      SetState(STATE_POSITION_RESOLUTION_ERROR, "POSITION_RESOLUTION_FAILED RetryOpenNewBig");
      return;
   }
   if(!ApplyResolvedPositionToBig(bigResolution))
      return;

   Ctx.pendingAttempts = 0;
   if(!PreparePendingOpenSmallContext())
   {
      SetState(STATE_INTEGRITY_ERROR, "INVALID_PENDING_CONTRACT for STATE_OPEN_NEW_SMALL_PENDING");
      return;
   }
   SetState(STATE_OPEN_NEW_SMALL_PENDING, "RetryOpenNewBig succeeded; PENDING_OPEN_SMALL prepared; continue opening Small");
}


void RetryOpenNewSmall()
{
   if(Ctx.pendingActionType != PENDING_OPEN_SMALL || State != STATE_OPEN_NEW_SMALL_PENDING)
   {
      if(!PreparePendingOpenSmallContext())
      {
         SetState(STATE_INTEGRITY_ERROR, "INVALID_PENDING_CONTRACT for STATE_OPEN_NEW_SMALL_PENDING");
         return;
      }
   }

   if(!Ctx.riskGateOk && AllowRealTrading && StopOnRiskGateBlocked)
   {
      LogRiskGateBlocked("RetryOpenNewSmall blocked by RiskGate; open retry remains pending");
      if(!ValidatePendingContract(STATE_OPEN_NEW_SMALL_PENDING))
      {
         SetState(STATE_INTEGRITY_ERROR, "INVALID_PENDING_CONTRACT before STATE_OPEN_NEW_SMALL_PENDING");
         return;
      }
      SetState(STATE_OPEN_NEW_SMALL_PENDING, "Open NewSmall blocked by RiskGate");
      return;
   }

   if(!ValidatePendingContract(STATE_OPEN_NEW_SMALL_PENDING))
   {
      SetState(STATE_INTEGRITY_ERROR, "INVALID_PENDING_CONTRACT before RetryOpenNewSmall");
      return;
   }

   Ctx.pendingAttempts++;

   datetime smallOpenStartTime = TimeCurrent();
   if(Ctx.pendingLot <= 0.0 || !OpenPosition(Ctx.pendingDirection, Ctx.pendingLot, Ctx.pendingComment))
   {
      if(MaxCloseRetryAttempts > 0 && Ctx.pendingAttempts >= MaxCloseRetryAttempts)
         SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "RetryOpenNewSmall exceeded retry attempts");
      else
         SetState(STATE_OPEN_NEW_SMALL_PENDING, "RetryOpenNewSmall failed; retry pending");
      return;
   }

   PositionResolutionResult smallResolution;
   if(!ResolveOpenedPositionAfterOpen(Ctx.pendingComment, Ctx.pendingDirection, Ctx.pendingLot, 0, smallOpenStartTime, smallResolution))
   {
      SetState(STATE_POSITION_RESOLUTION_ERROR, "POSITION_RESOLUTION_FAILED RetryOpenNewSmall");
      return;
   }
   if(!ApplyResolvedPositionToSmall(smallResolution))
      return;

   Ctx.harvestLevel += 1;
   Ctx.pendingAttempts = 0;
   ClearPendingOperationContext();
   SetState(STATE_BIG_SMALL_OPENED, "RetryOpenNewSmall succeeded; Big/Small opened");
}



bool ValidateFSMIntegrity()
{
   // FSM Integrity Check: unreachable states, dead states, states without handlers, states without transitions, states without retry.
   bool ok = true;
   string report = "FSM_INTEGRITY_CHECK | BigHarvestPhaseFSM=YES SmallScenarioPhaseFSM=YES OpenPendingRetry=YES ClosePendingRetry=YES LegacyPathRemoved=YES TerminalStatesNeverOpen=YES SmallBuildUsesSavedSmallDirection=YES OldFarCleanup=YES MaxLevelsDecision=YES StopMaxLevelsCloseRetry=YES RiskGateDoesNotBlockMaxLevelsClose=YES";
   LogInfo(report);

   if(StateToString(STATE_BIG_HARVEST_CLOSE_BIG) == "STATE_UNKNOWN") ok = false;
   if(StateToString(STATE_SMALL_CLOSE_SMALL) == "STATE_UNKNOWN") ok = false;
   if(StateToString(STATE_OPEN_NEW_BIG_PENDING) == "STATE_UNKNOWN") ok = false;
   if(StateToString(STATE_OPEN_NEW_SMALL_PENDING) == "STATE_UNKNOWN") ok = false;
   if(StateToString(STATE_INTEGRITY_ERROR) == "STATE_UNKNOWN") ok = false;
   if(StateToString(STATE_POSITION_RESOLUTION_ERROR) == "STATE_UNKNOWN") ok = false;
   // Strict V2.4.5 guards: terminal states must not route to RetryOpenNewBig/RetryOpenNewSmall/OpenBigSmall/OpenInitialLock; pending open states are handled separately; SmallBuildNewFar uses savedSmallDirection; OldFar close clears Ctx.far*.

   if(!ok)
      LogError("FSM_INTEGRITY_CHECK failed: state string mapping missing");
   return ok;
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

      case STATE_BIG_HARVEST_CLOSE_BIG:
         ProcessBigHarvestCloseBig();
         break;

      case STATE_BIG_HARVEST_CLOSE_SMALL:
         ProcessBigHarvestCloseSmall();
         break;

      case STATE_BIG_HARVEST_CALC_NET:
         ProcessBigHarvestCalcNet();
         break;

      case STATE_BIG_HARVEST_CLOSE_FAR:
         ProcessBigHarvestCloseFar();
         break;

      case STATE_BIG_HARVEST_CHECK_FINAL:
         ProcessBigHarvestCheckFinal();
         break;

      case STATE_WAIT_SMALL_TO_FAR:
         CheckSmallToFarTouch();
         break;

      case STATE_SMALL_SCENARIO:
         ProcessSmallScenario();
         break;

      case STATE_SMALL_CLOSE_SMALL:
         ProcessSmallCloseSmall();
         break;

      case STATE_SMALL_CLOSE_OLD_FAR:
         ProcessSmallCloseOldFar();
         break;

      case STATE_SMALL_CLOSE_BIG_PART:
         ProcessSmallCloseBigPart();
         break;

      case STATE_SMALL_BUILD_NEW_FAR:
         ProcessSmallBuildNewFar();
         break;

      case STATE_SMALL_CHECK_RESERVE:
         ProcessSmallCheckReserve();
         break;

      case STATE_SMALL_OPEN_NEW_BIG:
         RetryOpenNewBig();
         break;

      case STATE_SMALL_OPEN_NEW_SMALL:
         RetryOpenNewSmall();
         break;

      case STATE_FINAL_CLOSE:
         ProcessFinalClose();
         break;

      case STATE_MAX_LEVELS_DECISION:
         ProcessMaxLevelsDecision();
         break;

      case STATE_CLOSED_PROFIT:
         ClearCycleGeometry(true, GEOMETRY_CLEAR_CLOSED_PROFIT);
         break;
      case STATE_CLOSED_RECOVERY_LOSS:
         ClearCycleGeometry(true, GEOMETRY_CLEAR_CLOSED_RECOVERY_LOSS);
         break;
      case STATE_STOP_MAX_LEVELS:
         ClearCycleGeometry(true, GEOMETRY_CLEAR_STOP_MAX_LEVELS);
         break;
      case STATE_UNCLOSED_CYCLE:
      case STATE_DUAL_TAIL:
      case STATE_INVALID_REVERSE_GEOMETRY:
      case STATE_INVALID_SMALL_GEOMETRY:
      case STATE_REVERSE_LIMIT:
      case STATE_REVERSE_LIMIT_CLOSED:
      case STATE_INVALID_GEOMETRY_CLOSED:
      case STATE_RECOVERY_MISMATCH:
      case STATE_INTEGRITY_ERROR:
      case STATE_POSITION_RESOLUTION_ERROR:
      case STATE_MANUAL_INTERVENTION_REQUIRED:
      case STATE_STOP:
      case STATE_ERROR:
         break;

      case STATE_OPEN_NEW_BIG_PENDING:
         RetryOpenNewBig();
         break;

      case STATE_OPEN_NEW_SMALL_PENDING:
         RetryOpenNewSmall();
         break;

      case STATE_REVERSE_LIMIT_CLOSE_PENDING:
         RetryReverseLimitClose();
         break;

      case STATE_MAX_LEVELS_FINAL_CLOSE_PENDING:
         RetryMaxLevelsFinalClose();
         break;

      case STATE_STOP_MAX_LEVELS_CLOSE_PENDING:
         RetryStopMaxLevelsClose();
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
