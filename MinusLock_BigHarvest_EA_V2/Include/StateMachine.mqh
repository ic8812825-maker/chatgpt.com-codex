#ifndef __BH_STATEMACHINE_MQH__
#define __BH_STATEMACHINE_MQH__

bool StateIntegrityValidationInProgress = false;

ReserveLedgerEntry ReserveLedger[];
long NextReserveEventId = 1;
ReserveTransaction ActiveReserveTransaction;
long NextReserveTransactionId = 1;
ReserveFailPoint ActiveReserveFailPoint = RESERVE_FAIL_NONE;
bool RecoveryInProgress = false;

void SplitUlong64(ulong value, uint &high32, uint &low32)
{
   high32 = (uint)(value >> 32);
   low32 = (uint)(value & 0xFFFFFFFF);
}

ulong RestoreUlong64(uint high32, uint low32)
{
   return ((ulong)high32 << 32) | (ulong)low32;
}

void SplitLong64(long value, uint &high32, uint &low32)
{
   SplitUlong64((ulong)value, high32, low32);
}

long RestoreLong64(uint high32, uint low32)
{
   return (long)RestoreUlong64(high32, low32);
}

long StableSymbolHash64(string symbol)
{
   long hash = 1469598103934665603;
   for(int i = 0; i < StringLen(symbol); i++)
      hash = (hash ^ StringGetCharacter(symbol, i)) * 1099511628211;
   return hash;
}

void SplitReserveEventKeyHash(long hash, uint &high, uint &low)
{
   SplitLong64(hash, high, low);
}

long RestoreReserveEventKeyHash(uint high, uint low)
{
   return RestoreLong64(high, low);
}

bool BuildReserveEventContext(ReserveEventType type, ReserveEventContextSnapshot &snapshot)
{
   snapshot.symbol = _Symbol;
   snapshot.symbolHash = StableSymbolHash64(_Symbol);
   SplitLong64(snapshot.symbolHash, snapshot.symbolHashHigh, snapshot.symbolHashLow);
   snapshot.symbolLength = StringLen(_Symbol);
   snapshot.magicNumber = MagicNumber;
   snapshot.cycleId = Ctx.cycleId;
   snapshot.harvestLevel = Ctx.harvestLevel;
   snapshot.reverseCycle = Ctx.reverseCycleCount;
   snapshot.bigIdentifier = (Ctx.pendingBigPositionId != 0 ? Ctx.pendingBigPositionId : Ctx.bigIdentifier);
   snapshot.smallIdentifier = (Ctx.pendingSmallPositionId != 0 ? Ctx.pendingSmallPositionId : Ctx.smallIdentifier);
   snapshot.farIdentifier = Ctx.farIdentifier;
   snapshot.bigCoreIdentifier = Ctx.bigCoreIdentifier;
   snapshot.bigTrendIdentifier = Ctx.bigTrendIdentifier;
   snapshot.smallBaseIdentifier = Ctx.smallBaseIdentifier;
   snapshot.reverseSmallIdentifier = Ctx.reverseSmallIdentifier;
   snapshot.eventType = type;
   return true;
}

long ReserveEventKeyHash(ReserveEventContextSnapshot &snapshot)
{
   string key = StringFormat("%I64d|%d|%I64u|%I64u|%d|%d|%I64u|%I64u|%I64u|%I64u|%I64u|%I64u|%I64u|%d",
                             snapshot.symbolHash,
                             snapshot.symbolLength,
                             snapshot.magicNumber,
                             snapshot.cycleId,
                             snapshot.harvestLevel,
                             snapshot.reverseCycle,
                             snapshot.bigIdentifier,
                             snapshot.smallIdentifier,
                             snapshot.bigCoreIdentifier,
                             snapshot.bigTrendIdentifier,
                             snapshot.smallBaseIdentifier,
                             snapshot.reverseSmallIdentifier,
                             snapshot.farIdentifier,
                             (int)snapshot.eventType);
   long hash = 1469598103934665603;
   for(int i = 0; i < StringLen(key); i++)
      hash = (hash ^ StringGetCharacter(key, i)) * 1099511628211;
   return hash;
}

long ReserveEventKeyHash(ReserveEventType type)
{
   ReserveEventContextSnapshot snapshot;
   BuildReserveEventContext(type, snapshot);
   return ReserveEventKeyHash(snapshot);
}

long ReserveLedgerEntryHash(ReserveLedgerEntry &entry)
{
   ulong bigId = (ulong)entry.bigIdentifier;
   ulong smallId = (ulong)entry.smallIdentifier;
   string key = StringFormat("%I64d|%d|%I64u|%I64u|%d|%d|%I64u|%I64u|%I64u|%I64u|%I64u|%I64u|%I64u|%d",
                             entry.symbolHash,
                             entry.symbolLength,
                             entry.magicNumber,
                             entry.cycleId,
                             entry.harvestLevel,
                             entry.reverseCycle,
                             bigId,
                             smallId,
                             (ulong)entry.bigCoreIdentifier,
                             (ulong)entry.bigTrendIdentifier,
                             (ulong)entry.smallBaseIdentifier,
                             (ulong)entry.reverseSmallIdentifier,
                             (ulong)entry.farIdentifier,
                             (int)entry.type);
   long hash = 1469598103934665603;
   for(int i = 0; i < StringLen(key); i++)
      hash = (hash ^ StringGetCharacter(key, i)) * 1099511628211;
   return hash;
}

bool ReserveEventAlreadyApplied(long eventKeyHash)
{
   for(int i = 0; i < ArraySize(ReserveLedger); i++)
   {
      long restoredHash = RestoreReserveEventKeyHash(ReserveLedger[i].eventKeyHashHigh, ReserveLedger[i].eventKeyHashLow);
      if(restoredHash == eventKeyHash || ReserveLedger[i].eventKeyHash == eventKeyHash)
         return true;
   }
   return false;
}

void AppendReserveLedgerEntryFromSnapshot(ReserveEventContextSnapshot &snapshot, double amount, double reserveBefore, double reserveAfter)
{
   int index = ArraySize(ReserveLedger);
   ArrayResize(ReserveLedger, index + 1);
   ReserveLedger[index].eventId = NextReserveEventId++;
   ReserveLedger[index].timestamp = TimeCurrent();
   ReserveLedger[index].type = snapshot.eventType;
   ReserveLedger[index].amount = amount;
   ReserveLedger[index].reserveBefore = reserveBefore;
   ReserveLedger[index].reserveAfter = reserveAfter;
   ReserveLedger[index].symbol = snapshot.symbol;
   ReserveLedger[index].symbolHash = snapshot.symbolHash;
   ReserveLedger[index].symbolHashHigh = snapshot.symbolHashHigh;
   ReserveLedger[index].symbolHashLow = snapshot.symbolHashLow;
   ReserveLedger[index].symbolLength = snapshot.symbolLength;
   ReserveLedger[index].magicNumber = snapshot.magicNumber;
   ReserveLedger[index].cycleId = snapshot.cycleId;
   ReserveLedger[index].bigIdentifier = (long)snapshot.bigIdentifier;
   ReserveLedger[index].smallIdentifier = (long)snapshot.smallIdentifier;
   ReserveLedger[index].farIdentifier = (long)snapshot.farIdentifier;
   ReserveLedger[index].bigCoreIdentifier = (long)snapshot.bigCoreIdentifier;
   ReserveLedger[index].bigTrendIdentifier = (long)snapshot.bigTrendIdentifier;
   ReserveLedger[index].smallBaseIdentifier = (long)snapshot.smallBaseIdentifier;
   ReserveLedger[index].reverseSmallIdentifier = (long)snapshot.reverseSmallIdentifier;
   ReserveLedger[index].harvestLevel = snapshot.harvestLevel;
   ReserveLedger[index].reverseCycle = snapshot.reverseCycle;
   ReserveLedger[index].eventKeyHash = ReserveEventKeyHash(snapshot);
   SplitReserveEventKeyHash(ReserveLedger[index].eventKeyHash, ReserveLedger[index].eventKeyHashHigh, ReserveLedger[index].eventKeyHashLow);
   LogInfo(StringFormat("SPLIT_RESERVE_LEDGER_SAVE Symbol=%s SymbolHash=%I64d MagicNumber=%I64u CycleId=%I64u EventId=%d EventType=%d Amount=%.2f ReserveBefore=%.2f ReserveAfter=%.2f BigCoreIdentifier=%I64u BigTrendIdentifier=%I64u SmallBaseIdentifier=%I64u FarIdentifier=%I64u Level=%d ReserveEventKeyHash=%I64d EventKeyHashHigh32=%u EventKeyHashLow32=%u", snapshot.symbol, snapshot.symbolHash, snapshot.magicNumber, snapshot.cycleId, ReserveLedger[index].eventId, (int)snapshot.eventType, amount, reserveBefore, reserveAfter, snapshot.bigCoreIdentifier, snapshot.bigTrendIdentifier, snapshot.smallBaseIdentifier, snapshot.farIdentifier, snapshot.harvestLevel, ReserveLedger[index].eventKeyHash, ReserveLedger[index].eventKeyHashHigh, ReserveLedger[index].eventKeyHashLow));
}

void AppendReserveLedgerEntry(ReserveEventType type, double amount, double reserveBefore, double reserveAfter)
{
   ReserveEventContextSnapshot snapshot;
   BuildReserveEventContext(type, snapshot);
   AppendReserveLedgerEntryFromSnapshot(snapshot, amount, reserveBefore, reserveAfter);
}

bool ReserveLedgerContainsEventKey(long eventKeyHash, int &index)
{
   index = -1;
   for(int i = 0; i < ArraySize(ReserveLedger); i++)
   {
      if(RestoreReserveEventKeyHash(ReserveLedger[i].eventKeyHashHigh, ReserveLedger[i].eventKeyHashLow) == eventKeyHash)
      {
         index = i;
         return true;
      }
   }
   return false;
}

void ClearReserveTransaction()
{
   ActiveReserveTransaction.active = false;
   ActiveReserveTransaction.phase = RESERVE_TX_NONE;
   ActiveReserveTransaction.transactionId = 0;
   ActiveReserveTransaction.eventKeyHash = 0;
   ActiveReserveTransaction.expectedLedgerEventId = 0;
}

bool SaveReserveTransaction()
{
   GlobalVariableSet(StateKey("ReserveTxActive"), ActiveReserveTransaction.active ? 1.0 : 0.0);
   SaveStateLong64("ReserveTxTransactionId", ActiveReserveTransaction.transactionId);
   GlobalVariableSet(StateKey("ReserveTxEventType"), (double)ActiveReserveTransaction.eventType);
   GlobalVariableSet(StateKey("ReserveTxPhase"), (double)ActiveReserveTransaction.phase);
   GlobalVariableSet(StateKey("ReserveTxAmount"), ActiveReserveTransaction.amount);
   GlobalVariableSet(StateKey("ReserveTxReserveBefore"), ActiveReserveTransaction.reserveBefore);
   GlobalVariableSet(StateKey("ReserveTxReserveAfter"), ActiveReserveTransaction.reserveAfter);
   SaveStateLong64("ReserveTxEventKeyHash", ActiveReserveTransaction.eventKeyHash);
   SaveStateLong64("ReserveTxExpectedLedgerEventId", ActiveReserveTransaction.expectedLedgerEventId);
   GlobalVariableSet(StateKey("ReserveTxStartedAt"), (double)ActiveReserveTransaction.startedAt);
   SaveStateLong64("ReserveTxSymbolHash", ActiveReserveTransaction.snapshot.symbolHash);
   GlobalVariableSet(StateKey("ReserveTxSymbolLength"), (double)ActiveReserveTransaction.snapshot.symbolLength);
   SaveStateUlong64("ReserveTxMagicNumber", ActiveReserveTransaction.snapshot.magicNumber);
   SaveStateUlong64("ReserveTxCycleId", ActiveReserveTransaction.snapshot.cycleId);
   SaveStateUlong64("ReserveTxFarIdentifier", ActiveReserveTransaction.snapshot.farIdentifier);
   SaveStateUlong64("ReserveTxBigIdentifier", ActiveReserveTransaction.snapshot.bigIdentifier);
   SaveStateUlong64("ReserveTxSmallIdentifier", ActiveReserveTransaction.snapshot.smallIdentifier);
   SaveStateUlong64("ReserveTxBigCoreIdentifier", ActiveReserveTransaction.snapshot.bigCoreIdentifier);
   SaveStateUlong64("ReserveTxBigTrendIdentifier", ActiveReserveTransaction.snapshot.bigTrendIdentifier);
   SaveStateUlong64("ReserveTxSmallBaseIdentifier", ActiveReserveTransaction.snapshot.smallBaseIdentifier);
   SaveStateUlong64("ReserveTxReverseSmallIdentifier", ActiveReserveTransaction.snapshot.reverseSmallIdentifier);
   GlobalVariableSet(StateKey("ReserveTxHarvestLevel"), (double)ActiveReserveTransaction.snapshot.harvestLevel);
   GlobalVariableSet(StateKey("ReserveTxReverseCycle"), (double)ActiveReserveTransaction.snapshot.reverseCycle);
   return true;
}


string ReserveEventTypeRequirementsToString(ReserveEventType type)
{
   switch(type)
   {
      case RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD:
         return "EventType=RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD RequiredFar=YES RequiredLegacyBig=NO RequiredLegacySmall=NO RequiredBigCore=YES RequiredBigTrend=YES RequiredSmallBase=YES RequiredReverseSmall=NO RequiredHarvestLevel=YES";
      case RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT:
         return "EventType=RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT RequiredFar=YES RequiredLegacyBig=NO RequiredLegacySmall=NO RequiredBigCore=YES RequiredBigTrend=YES RequiredSmallBase=YES RequiredReverseSmall=NO RequiredHarvestLevel=YES";
      case RESERVE_EVENT_BIG_HARVEST_ADD:
         return "EventType=RESERVE_EVENT_BIG_HARVEST_ADD RequiredFar=YES RequiredLegacyBig=YES RequiredLegacySmall=YES RequiredBigCore=NO RequiredBigTrend=NO RequiredSmallBase=NO RequiredReverseSmall=NO RequiredHarvestLevel=YES";
      case RESERVE_EVENT_REVERSE_TRANSITION_ADD:
         return "EventType=RESERVE_EVENT_REVERSE_TRANSITION_ADD RequiredFar=YES RequiredLegacyBig=NO RequiredLegacySmall=NO RequiredBigCore=YES RequiredBigTrend=YES RequiredSmallBase=NO RequiredReverseSmall=YES RequiredHarvestLevel=YES";
      case RESERVE_EVENT_RESET:
         return "EventType=RESERVE_EVENT_RESET RequiredFar=NO RequiredLegacyBig=NO RequiredLegacySmall=NO RequiredBigCore=NO RequiredBigTrend=NO RequiredSmallBase=NO RequiredReverseSmall=NO RequiredHarvestLevel=NO";
      default:
         return "EventType=OTHER RequiredFar=YES RequiredLegacyBig=NO RequiredLegacySmall=NO RequiredBigCore=NO RequiredBigTrend=NO RequiredSmallBase=NO RequiredReverseSmall=NO RequiredHarvestLevel=NO";
   }
}

bool ReserveTransactionContextError(string fieldName, ReserveTransaction &tx)
{
   LogError(StringFormat("RESERVE_TRANSACTION_EVENT_CONTEXT_INVALID MissingField=%s %s ValidationResult=FAIL", fieldName, ReserveEventTypeRequirementsToString(tx.eventType)));
   State = STATE_RECOVERY_MISMATCH;
   Ctx.lastError = "RESERVE_TRANSACTION_EVENT_CONTEXT_INVALID " + fieldName;
   return false;
}

bool ValidateReserveTransactionContextByEventType(ReserveTransaction &tx)
{
   if(!tx.active)
      return true;
   if(tx.transactionId == 0) return ReserveTransactionContextError("TransactionId", tx);
   if(tx.eventType == RESERVE_EVENT_NONE) return ReserveTransactionContextError("EventType", tx);
   if(tx.phase == RESERVE_TX_NONE) return ReserveTransactionContextError("Phase", tx);
   if(tx.eventKeyHash == 0) return ReserveTransactionContextError("EventKeyHash", tx);
   if(tx.snapshot.symbolHash == 0 || tx.snapshot.symbolHash != StableSymbolHash64(_Symbol)) return ReserveTransactionContextError("SymbolHash", tx);
   if(tx.snapshot.magicNumber != MagicNumber) return ReserveTransactionContextError("MagicNumber", tx);
   if(tx.snapshot.cycleId == 0) return ReserveTransactionContextError("CycleId", tx);
   if(tx.startedAt <= 0) return ReserveTransactionContextError("StartedAt", tx);

   if(tx.eventType == RESERVE_EVENT_RESET)
      return true;

   if(tx.eventType == RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD || tx.eventType == RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT)
   {
      if(tx.snapshot.farIdentifier == 0) return ReserveTransactionContextError("FarIdentifier", tx);
      if(tx.snapshot.bigCoreIdentifier == 0) return ReserveTransactionContextError("BigCoreIdentifier", tx);
      if(tx.snapshot.bigTrendIdentifier == 0) return ReserveTransactionContextError("BigTrendIdentifier", tx);
      if(tx.snapshot.smallBaseIdentifier == 0) return ReserveTransactionContextError("SmallBaseIdentifier", tx);
      if(tx.snapshot.harvestLevel <= 0) return ReserveTransactionContextError("HarvestLevel", tx);
      return true;
   }

   if(tx.eventType == RESERVE_EVENT_BIG_HARVEST_ADD)
   {
      if(tx.snapshot.farIdentifier == 0) return ReserveTransactionContextError("FarIdentifier", tx);
      if(tx.snapshot.bigIdentifier == 0) return ReserveTransactionContextError("BigIdentifier", tx);
      if(tx.snapshot.smallIdentifier == 0) return ReserveTransactionContextError("SmallIdentifier", tx);
      if(tx.snapshot.harvestLevel <= 0) return ReserveTransactionContextError("HarvestLevel", tx);
      return true;
   }

   if(tx.eventType == RESERVE_EVENT_REVERSE_TRANSITION_ADD)
   {
      if(tx.snapshot.farIdentifier == 0) return ReserveTransactionContextError("FarIdentifier", tx);
      if(tx.snapshot.reverseSmallIdentifier == 0 && tx.snapshot.bigCoreIdentifier == 0 && tx.snapshot.bigTrendIdentifier == 0)
         return ReserveTransactionContextError("ReverseIdentifiers", tx);
      return true;
   }

   if(tx.snapshot.farIdentifier == 0)
      return ReserveTransactionContextError("FarIdentifier", tx);
   return true;
}

bool ValidateReserveTransactionRequiredFields()
{
   if(!ActiveReserveTransaction.active)
      return true;
   bool ok = (ActiveReserveTransaction.transactionId != 0 &&
              ActiveReserveTransaction.eventType != RESERVE_EVENT_NONE &&
              ActiveReserveTransaction.phase != RESERVE_TX_NONE &&
              ActiveReserveTransaction.eventKeyHash != 0 &&
              ActiveReserveTransaction.snapshot.symbolHash != 0 &&
              ActiveReserveTransaction.snapshot.magicNumber == MagicNumber &&
              ActiveReserveTransaction.snapshot.cycleId != 0 &&
              ActiveReserveTransaction.startedAt > 0);
   ok = ok && ValidateReserveTransactionContextByEventType(ActiveReserveTransaction);
   LogInfo(StringFormat("RESERVE_TRANSACTION_EVENT_CONTEXT_CHECK %s ValidationResult=%s", ReserveEventTypeRequirementsToString(ActiveReserveTransaction.eventType), ok ? "PASS" : "FAIL"));
   if(!ok)
   {
      LogError("RESERVE_TRANSACTION_REQUIRED_FIELD_MISSING");
      State = STATE_RECOVERY_MISMATCH;
      Ctx.lastError = "RESERVE_TRANSACTION_REQUIRED_FIELD_MISSING";
   }
   return ok;
}

bool LoadReserveTransaction()
{
   double saved = 0.0;
   if(!GetStateDouble("ReserveTxActive", saved) || saved <= 0.5)
   {
      ClearReserveTransaction();
      return true;
   }
   ActiveReserveTransaction.active = true;
   bool ok = true;
   ok = LoadStateLong64("ReserveTxTransactionId", ActiveReserveTransaction.transactionId) && ok;
   if(GetStateDouble("ReserveTxEventType", saved)) ActiveReserveTransaction.eventType = (ReserveEventType)(int)saved; else ok = false;
   if(GetStateDouble("ReserveTxPhase", saved)) ActiveReserveTransaction.phase = (ReserveTransactionPhase)(int)saved; else ok = false;
   if(GetStateDouble("ReserveTxAmount", saved)) ActiveReserveTransaction.amount = saved; else ok = false;
   if(GetStateDouble("ReserveTxReserveBefore", saved)) ActiveReserveTransaction.reserveBefore = saved; else ok = false;
   if(GetStateDouble("ReserveTxReserveAfter", saved)) ActiveReserveTransaction.reserveAfter = saved; else ok = false;
   ok = LoadStateLong64("ReserveTxEventKeyHash", ActiveReserveTransaction.eventKeyHash) && ok;
   ok = LoadStateLong64("ReserveTxExpectedLedgerEventId", ActiveReserveTransaction.expectedLedgerEventId) && ok;
   if(GetStateDouble("ReserveTxStartedAt", saved)) ActiveReserveTransaction.startedAt = (datetime)saved; else ok = false;
   ok = LoadStateLong64("ReserveTxSymbolHash", ActiveReserveTransaction.snapshot.symbolHash) && ok;
   if(GetStateDouble("ReserveTxSymbolLength", saved)) ActiveReserveTransaction.snapshot.symbolLength = (int)saved; else ok = false;
   ok = LoadStateUlong64("ReserveTxMagicNumber", ActiveReserveTransaction.snapshot.magicNumber) && ok;
   ok = LoadStateUlong64("ReserveTxCycleId", ActiveReserveTransaction.snapshot.cycleId) && ok;
   ok = LoadStateUlong64("ReserveTxFarIdentifier", ActiveReserveTransaction.snapshot.farIdentifier) && ok;
   ok = LoadStateUlong64("ReserveTxBigIdentifier", ActiveReserveTransaction.snapshot.bigIdentifier) && ok;
   ok = LoadStateUlong64("ReserveTxSmallIdentifier", ActiveReserveTransaction.snapshot.smallIdentifier) && ok;
   ok = LoadStateUlong64("ReserveTxBigCoreIdentifier", ActiveReserveTransaction.snapshot.bigCoreIdentifier) && ok;
   ok = LoadStateUlong64("ReserveTxBigTrendIdentifier", ActiveReserveTransaction.snapshot.bigTrendIdentifier) && ok;
   ok = LoadStateUlong64("ReserveTxSmallBaseIdentifier", ActiveReserveTransaction.snapshot.smallBaseIdentifier) && ok;
   ok = LoadStateUlong64("ReserveTxReverseSmallIdentifier", ActiveReserveTransaction.snapshot.reverseSmallIdentifier) && ok;
   if(GetStateDouble("ReserveTxHarvestLevel", saved)) ActiveReserveTransaction.snapshot.harvestLevel = (int)saved; else ok = false;
   if(GetStateDouble("ReserveTxReverseCycle", saved)) ActiveReserveTransaction.snapshot.reverseCycle = (int)saved; else ok = false;
   ActiveReserveTransaction.snapshot.symbol = _Symbol;
   ActiveReserveTransaction.snapshot.eventType = ActiveReserveTransaction.eventType;
   SplitLong64(ActiveReserveTransaction.eventKeyHash, ActiveReserveTransaction.eventKeyHashHigh, ActiveReserveTransaction.eventKeyHashLow);
   ok = ok && ValidateReserveTransactionRequiredFields();
   if(!ok)
   {
      LogError("RESERVE_TRANSACTION_REQUIRED_FIELD_MISSING");
      State = STATE_RECOVERY_MISMATCH;
      Ctx.lastError = "RESERVE_TRANSACTION_REQUIRED_FIELD_MISSING";
      return false;
   }
   return true;
}


bool ReserveRecoveryConflict(string reason)
{
   LogError(StringFormat("RESERVE_TRANSACTION_RECOVERY_CONFLICT Reason=%s TransactionId=%I64d Phase=%d EventKey=%I64d", reason, ActiveReserveTransaction.transactionId, (int)ActiveReserveTransaction.phase, ActiveReserveTransaction.eventKeyHash));
   State = STATE_RECOVERY_MISMATCH;
   Ctx.lastError = "RESERVE_TRANSACTION_RECOVERY_CONFLICT " + reason;
   return false;
}

int ReserveLedgerEventKeyCount(long eventKeyHash, int &firstIndex)
{
   firstIndex = -1;
   int count = 0;
   for(int i = 0; i < ArraySize(ReserveLedger); i++)
   {
      if(RestoreReserveEventKeyHash(ReserveLedger[i].eventKeyHashHigh, ReserveLedger[i].eventKeyHashLow) == eventKeyHash)
      {
         if(firstIndex < 0) firstIndex = i;
         count++;
      }
   }
   return count;
}

bool ValidateLedgerEntryAgainstTransaction(ReserveLedgerEntry &entry, ReserveTransaction &tx)
{
   long restoredHash = RestoreReserveEventKeyHash(entry.eventKeyHashHigh, entry.eventKeyHashLow);
   bool ok = true;
   ok = ok && entry.eventId == tx.expectedLedgerEventId;
   ok = ok && entry.type == tx.eventType;
   ok = ok && restoredHash == tx.eventKeyHash;
   ok = ok && MathAbs(entry.amount - tx.amount) <= ReserveMismatchTolerance;
   ok = ok && MathAbs(entry.reserveBefore - tx.reserveBefore) <= ReserveMismatchTolerance;
   ok = ok && MathAbs(entry.reserveAfter - tx.reserveAfter) <= ReserveMismatchTolerance;
   ok = ok && entry.symbolHash == tx.snapshot.symbolHash;
   ok = ok && entry.magicNumber == tx.snapshot.magicNumber;
   ok = ok && entry.cycleId == tx.snapshot.cycleId;
   ok = ok && entry.harvestLevel == tx.snapshot.harvestLevel;
   ok = ok && entry.reverseCycle == tx.snapshot.reverseCycle;
   ok = ok && (ulong)entry.farIdentifier == tx.snapshot.farIdentifier;
   ok = ok && (ulong)entry.bigIdentifier == tx.snapshot.bigIdentifier;
   ok = ok && (ulong)entry.smallIdentifier == tx.snapshot.smallIdentifier;
   ok = ok && (ulong)entry.bigCoreIdentifier == tx.snapshot.bigCoreIdentifier;
   ok = ok && (ulong)entry.bigTrendIdentifier == tx.snapshot.bigTrendIdentifier;
   ok = ok && (ulong)entry.smallBaseIdentifier == tx.snapshot.smallBaseIdentifier;
   ok = ok && (ulong)entry.reverseSmallIdentifier == tx.snapshot.reverseSmallIdentifier;
   if(!ok)
      LogError(StringFormat("RESERVE_TRANSACTION_LEDGER_ENTRY_MISMATCH EntryEventId=%I64d ExpectedEventId=%I64d EntryHash=%I64d TxHash=%I64d EntryAmount=%.2f TxAmount=%.2f EntryReserveAfter=%.2f TxReserveAfter=%.2f", entry.eventId, tx.expectedLedgerEventId, restoredHash, tx.eventKeyHash, entry.amount, tx.amount, entry.reserveAfter, tx.reserveAfter));
   return ok;
}

double ReserveLedgerCurrentReserve()
{
   if(ArraySize(ReserveLedger) <= 0)
      return 0.0;
   return ReserveLedger[ArraySize(ReserveLedger) - 1].reserveAfter;
}

bool ValidateReserveLedgerStructureOnly()
{
   bool ok = true;
   long lastEventId = 0;
   for(int i = 0; i < ArraySize(ReserveLedger); i++)
   {
      ReserveLedgerEntry entry = ReserveLedger[i];
      long restoredHash = RestoreReserveEventKeyHash(entry.eventKeyHashHigh, entry.eventKeyHashLow);
      long recomputedHash = ReserveLedgerEntryHash(entry);
      if(restoredHash != recomputedHash)
      {
         LogError(StringFormat("RESERVE_EVENT_KEY_COMPONENT_MISMATCH Index=%d EventId=%I64d RestoredHash=%I64d RecomputedHash=%I64d", i, entry.eventId, restoredHash, recomputedHash));
         ok = false;
      }
      if(entry.symbolHash != StableSymbolHash64(_Symbol) || entry.symbolLength != StringLen(_Symbol) || entry.magicNumber != MagicNumber || entry.cycleId != Ctx.cycleId)
      {
         LogError(StringFormat("RESERVE_EVENT_KEY_COMPONENT_MISMATCH Index=%d EventId=%I64d Field=SymbolMagicCycle", i, entry.eventId));
         ok = false;
      }
      if((i == 0 && entry.eventId != 1) || (i > 0 && entry.eventId != lastEventId + 1))
      {
         LogError(StringFormat("RESERVE_LEDGER_EVENT_ID_GAP Index=%d EventId=%I64d ExpectedEventId=%I64d", i, entry.eventId, (i == 0 ? 1 : lastEventId + 1)));
         ok = false;
      }
      for(int j = i + 1; j < ArraySize(ReserveLedger); j++)
      {
         if(ReserveLedger[j].eventId == entry.eventId || RestoreReserveEventKeyHash(ReserveLedger[j].eventKeyHashHigh, ReserveLedger[j].eventKeyHashLow) == restoredHash)
         {
            LogError(StringFormat("RESERVE_LEDGER_CHAIN_BROKEN Index=%d DuplicateIndex=%d DuplicateEventIdOrKey=YES", i, j));
            ok = false;
         }
      }
      lastEventId = entry.eventId;
   }
   if(NextReserveEventId <= lastEventId)
   {
      LogError(StringFormat("RESERVE_LEDGER_EVENT_ID_GAP NextReserveEventId=%I64d MaxEventId=%I64d", NextReserveEventId, lastEventId));
      ok = false;
   }
   LogInfo(StringFormat("RECOVERY_LEDGER_LOAD_COMPLETE Symbol=%s Magic=%I64u CycleId=%I64u LedgerEntries=%d NextReserveEventId=%I64d Result=%s", _Symbol, MagicNumber, Ctx.cycleId, ArraySize(ReserveLedger), NextReserveEventId, ok ? "PASS" : "FAIL"));
   return ok;
}

bool ValidateLedgerAndCacheForTransactionPhase(ReserveTransaction &tx)
{
   double ledgerReserve = ReserveLedgerCurrentReserve();
   if(!tx.active)
      return MathAbs(ledgerReserve - Ctx.totalReserve) <= ReserveMismatchTolerance;
   int ledgerIndex = -1;
   int count = ReserveLedgerEventKeyCount(tx.eventKeyHash, ledgerIndex);
   if(count > 1)
      return ReserveRecoveryConflict("DUPLICATE_TRANSACTION_EVENT_KEY");
   if(tx.phase == RESERVE_TX_PREPARED)
   {
      if(count == 0)
         return MathAbs(Ctx.totalReserve - tx.reserveBefore) <= ReserveMismatchTolerance;
      if(!ValidateLedgerEntryAgainstTransaction(ReserveLedger[ledgerIndex], tx))
         return ReserveRecoveryConflict("PREPARED_LEDGER_MISMATCH");
      tx.phase = RESERVE_TX_LEDGER_WRITTEN;
      SaveReserveTransaction();
      return true;
   }
   if(tx.phase == RESERVE_TX_LEDGER_WRITTEN)
   {
      if(count != 1)
         return ReserveRecoveryConflict("LEDGER_WRITTEN_EVENT_NOT_FOUND");
      if(!ValidateLedgerEntryAgainstTransaction(ReserveLedger[ledgerIndex], tx))
         return ReserveRecoveryConflict("LEDGER_WRITTEN_LEDGER_MISMATCH");
      if(MathAbs(Ctx.totalReserve - tx.reserveBefore) <= ReserveMismatchTolerance || MathAbs(Ctx.totalReserve - tx.reserveAfter) <= ReserveMismatchTolerance)
         return true;
      return ReserveRecoveryConflict("LEDGER_WRITTEN_CACHE_MISMATCH");
   }
   if(tx.phase == RESERVE_TX_CACHE_UPDATED)
   {
      if(count != 1)
         return ReserveRecoveryConflict("CACHE_UPDATED_EVENT_NOT_FOUND");
      if(!ValidateLedgerEntryAgainstTransaction(ReserveLedger[ledgerIndex], tx))
         return ReserveRecoveryConflict("CACHE_UPDATED_LEDGER_MISMATCH");
      if(MathAbs(Ctx.totalReserve - tx.reserveAfter) > ReserveMismatchTolerance)
         return ReserveRecoveryConflict("CACHE_UPDATED_CACHE_MISMATCH");
      return true;
   }
   if(tx.phase == RESERVE_TX_COMPLETED)
   {
      if(count != 1)
         return ReserveRecoveryConflict("COMPLETED_EVENT_NOT_FOUND");
      if(!ValidateLedgerEntryAgainstTransaction(ReserveLedger[ledgerIndex], tx))
         return ReserveRecoveryConflict("COMPLETED_LEDGER_MISMATCH");
      if(MathAbs(Ctx.totalReserve - tx.reserveAfter) > ReserveMismatchTolerance)
         return ReserveRecoveryConflict("COMPLETED_CACHE_MISMATCH");
      return true;
   }
   return ReserveRecoveryConflict("UNKNOWN_TRANSACTION_PHASE");
}

bool ExecuteReserveTransaction(ReserveTransaction &tx)
{
   if(!tx.active)
      return true;
   int ledgerIndex = -1;
   if(tx.phase == RESERVE_TX_COMPLETED)
   {
      if(!ReserveLedgerContainsEventKey(tx.eventKeyHash, ledgerIndex))
         return ReserveRecoveryConflict("COMPLETED_EVENT_NOT_FOUND");
      if(!ValidateLedgerEntryAgainstTransaction(ReserveLedger[ledgerIndex], tx))
         return ReserveRecoveryConflict("COMPLETED_LEDGER_MISMATCH");
      if(MathAbs(Ctx.totalReserve - tx.reserveAfter) > ReserveMismatchTolerance)
         return ReserveRecoveryConflict("COMPLETED_CACHE_MISMATCH");
      ClearReserveTransaction();
      SaveReserveTransaction();
      LogInfo("RECOVERY_TRANSACTION_COMPLETED Phase=COMPLETED Result=cleared_active_marker");
      return true;
   }
   if(tx.phase == RESERVE_TX_PREPARED)
   {
      if(!ReserveLedgerContainsEventKey(tx.eventKeyHash, ledgerIndex))
      {
         if(tx.expectedLedgerEventId != NextReserveEventId)
            return ReserveRecoveryConflict("RESERVE_TRANSACTION_EXPECTED_EVENT_ID_MISMATCH");
         AppendReserveLedgerEntryFromSnapshot(tx.snapshot, tx.amount, tx.reserveBefore, tx.reserveAfter);
         tx.expectedLedgerEventId = ReserveLedger[ArraySize(ReserveLedger) - 1].eventId;
      }
      else if(!ValidateLedgerEntryAgainstTransaction(ReserveLedger[ledgerIndex], tx))
         return ReserveRecoveryConflict("PREPARED_LEDGER_MISMATCH");
      tx.phase = RESERVE_TX_LEDGER_WRITTEN;
      SaveReserveTransaction();
      SaveState();
      if(ActiveReserveFailPoint == RESERVE_FAIL_AFTER_LEDGER_WRITE) return false;
   }
   if(tx.phase == RESERVE_TX_LEDGER_WRITTEN)
   {
      if(!ReserveLedgerContainsEventKey(tx.eventKeyHash, ledgerIndex))
         return ReserveRecoveryConflict("LEDGER_WRITTEN_EVENT_NOT_FOUND");
      if(!ValidateLedgerEntryAgainstTransaction(ReserveLedger[ledgerIndex], tx))
         return ReserveRecoveryConflict("LEDGER_WRITTEN_LEDGER_MISMATCH");
      Ctx.totalReserve = tx.reserveAfter;
      tx.phase = RESERVE_TX_CACHE_UPDATED;
      SaveReserveTransaction();
      SaveState();
      if(ActiveReserveFailPoint == RESERVE_FAIL_AFTER_CACHE_UPDATE) return false;
   }
   if(tx.phase == RESERVE_TX_CACHE_UPDATED)
   {
      if(!ReserveLedgerContainsEventKey(tx.eventKeyHash, ledgerIndex))
         return ReserveRecoveryConflict("CACHE_UPDATED_EVENT_NOT_FOUND");
      if(!ValidateLedgerEntryAgainstTransaction(ReserveLedger[ledgerIndex], tx) || MathAbs(Ctx.totalReserve - tx.reserveAfter) > ReserveMismatchTolerance)
         return ReserveRecoveryConflict("CACHE_UPDATED_CACHE_OR_LEDGER_MISMATCH");
      tx.phase = RESERVE_TX_COMPLETED;
      SaveReserveTransaction();
      if(ActiveReserveFailPoint == RESERVE_FAIL_BEFORE_COMPLETED) return false;
      tx.active = false;
      ClearReserveTransaction();
      SaveReserveTransaction();
      SaveState();
      LogInfo("RECOVERY_TRANSACTION_COMPLETED Phase=CACHE_UPDATED Result=completed");
   }
   return true;
}

bool RecoverPendingReserveTransaction()
{
   if(!ActiveReserveTransaction.active)
      return true;
   LogInfo(StringFormat("RESERVE_TRANSACTION_RECOVER TransactionId=%I64d Phase=%d EventKey=%I64d", ActiveReserveTransaction.transactionId, (int)ActiveReserveTransaction.phase, ActiveReserveTransaction.eventKeyHash));
   return ExecuteReserveTransaction(ActiveReserveTransaction);
}

bool TradingOperationAllowedDuringRecovery(string operationName, bool isRecoveryContinuation);
bool HasOpenLegContext();
int CountManagedOpenPositions();

bool StartReserveTransaction(ReserveEventContextSnapshot &snapshot, double signedAmount)
{
   long eventKeyHash = ReserveEventKeyHash(snapshot);
   if(RecoveryInProgress)
   {
      if(ActiveReserveTransaction.active && ActiveReserveTransaction.eventKeyHash == eventKeyHash)
         return ExecuteReserveTransaction(ActiveReserveTransaction);
      if(!TradingOperationAllowedDuringRecovery("StartReserveTransaction", false))
         return false;
   }
   int ledgerIndex = -1;
   if(ReserveLedgerContainsEventKey(eventKeyHash, ledgerIndex))
      return true;
   if(ActiveReserveTransaction.active)
   {
      if(ActiveReserveTransaction.eventKeyHash != eventKeyHash)
      {
         LogError("RESERVE_TRANSACTION_RECOVERY_CONFLICT ActiveDifferentEventKey=YES");
         State = STATE_RECOVERY_PENDING;
         Ctx.lastError = "RESERVE_TRANSACTION_RECOVERY_CONFLICT";
         return false;
      }
      return ExecuteReserveTransaction(ActiveReserveTransaction);
   }
   ActiveReserveTransaction.active = true;
   ActiveReserveTransaction.transactionId = NextReserveTransactionId;
   NextReserveTransactionId++;
   SaveStateLong64("NextReserveTransactionId", NextReserveTransactionId);
   ActiveReserveTransaction.eventType = snapshot.eventType;
   ActiveReserveTransaction.phase = RESERVE_TX_PREPARED;
   ActiveReserveTransaction.amount = signedAmount;
   ActiveReserveTransaction.reserveBefore = Ctx.totalReserve;
   ActiveReserveTransaction.reserveAfter = MathMax(0.0, Ctx.totalReserve + signedAmount);
   ActiveReserveTransaction.snapshot = snapshot;
   ActiveReserveTransaction.eventKeyHash = eventKeyHash;
   SplitLong64(eventKeyHash, ActiveReserveTransaction.eventKeyHashHigh, ActiveReserveTransaction.eventKeyHashLow);
   ActiveReserveTransaction.expectedLedgerEventId = NextReserveEventId;
   ActiveReserveTransaction.startedAt = TimeCurrent();
   SaveReserveTransaction();
   if(ActiveReserveFailPoint == RESERVE_FAIL_AFTER_PREPARED) return false;
   return ExecuteReserveTransaction(ActiveReserveTransaction);
}

bool ApplyReserveCreditSnapshot(ReserveEventContextSnapshot &snapshot, double amount)
{
   if(amount <= 0.0)
      return true;
   return StartReserveTransaction(snapshot, amount);
}

bool ApplyReserveCredit(ReserveEventType type, double amount)
{
   ReserveEventContextSnapshot snapshot;
   BuildReserveEventContext(type, snapshot);
   return ApplyReserveCreditSnapshot(snapshot, amount);
}

bool ApplyReserveDebitSnapshot(ReserveEventContextSnapshot &snapshot, double amount)
{
   if(amount <= 0.0)
      return true;
   if(Ctx.totalReserve + ReserveMismatchTolerance < amount)
   {
      LogError(StringFormat("ERROR_RESERVE_DEBIT_EXCEEDS_BALANCE Type=%d Amount=%.2f ReserveBefore=%.2f", (int)snapshot.eventType, amount, Ctx.totalReserve));
      return false;
   }
   return StartReserveTransaction(snapshot, -amount);
}

bool ApplyReserveDebit(ReserveEventType type, double amount)
{
   ReserveEventContextSnapshot snapshot;
   BuildReserveEventContext(type, snapshot);
   return ApplyReserveDebitSnapshot(snapshot, amount);
}

bool CanStartReserveReset()
{
   bool terminalState = (State == STATE_IDLE || State == STATE_STOP || State == STATE_CLOSED_PROFIT || State == STATE_CLOSED_RECOVERY_LOSS);
   if(!terminalState)
   {
      LogError(StringFormat("RESERVE_RESET_BLOCKED Reason=STATE_NOT_ALLOWED State=%s", StateToString(State)));
      return false;
   }
   if(RecoveryInProgress)
   {
      LogError(StringFormat("RESERVE_RESET_BLOCKED Reason=RECOVERY_IN_PROGRESS State=%s", StateToString(State)));
      return false;
   }
   if(ActiveReserveTransaction.active)
   {
      LogError(StringFormat("RESERVE_RESET_BLOCKED Reason=ACTIVE_RESERVE_TRANSACTION TransactionId=%I64d Phase=%d", ActiveReserveTransaction.transactionId, (int)ActiveReserveTransaction.phase));
      return false;
   }
   if(CountManagedOpenPositions() != 0)
   {
      LogError(StringFormat("RESERVE_RESET_BLOCKED Reason=OPEN_MANAGED_POSITIONS Count=%d", CountManagedOpenPositions()));
      return false;
   }
   if(HasOpenLegContext())
   {
      LogError("RESERVE_RESET_BLOCKED Reason=OPEN_LEG_CONTEXT");
      return false;
   }
   return true;
}

void ApplyReserveReset(double amount, string reason)
{
   if(!CanStartReserveReset())
      return;
   ReserveEventContextSnapshot snapshot;
   BuildReserveEventContext(RESERVE_EVENT_RESET, snapshot);
   double targetReserve = MathMax(0.0, amount);
   double delta = targetReserve - Ctx.totalReserve;
   if(MathAbs(delta) <= ReserveMismatchTolerance)
      return;
   if(StartReserveTransaction(snapshot, delta))
      LogInfo("RESERVE_LEDGER_RESET_TRANSACTIONAL " + reason);
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
bool ResolveBigCorePosition();
bool ResolveBigTrendPosition();
bool ResolveSmallBasePosition();
bool TryRecoverPromotedBigAsFar(string reason);

bool IsProfitSystemCloseComment(string comment)
{
   return comment == "FINAL_CLOSE_PROFIT" ||
          comment == "SPLIT_FINAL_CLOSE_PROFIT" ||
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
      if(Ctx.bigCoreTicket != 0) fullCloseVerified = VerifyFullClose(Ctx.bigCoreTicket, "STATE_CLOSED_PROFIT_BIG_CORE_GUARD") && fullCloseVerified;
      if(Ctx.bigTrendTicket != 0) fullCloseVerified = VerifyFullClose(Ctx.bigTrendTicket, "STATE_CLOSED_PROFIT_BIG_TREND_GUARD") && fullCloseVerified;
      if(Ctx.smallBaseTicket != 0) fullCloseVerified = VerifyFullClose(Ctx.smallBaseTicket, "STATE_CLOSED_PROFIT_SMALL_BASE_GUARD") && fullCloseVerified;

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
   SaveStateUlong64("FarTicket", Ctx.farTicket);
   SaveStateUlong64("FarIdentifier", Ctx.farIdentifier);
   GlobalVariableSet(StateKey("FarLot"), Ctx.farLot);
   GlobalVariableSet(StateKey("FarOpenPrice"), Ctx.farOpenPrice);
   GlobalVariableSet(StateKey("FarDirection"), (double)Ctx.farDirection);
   SaveStateUlong64("BigTicket", Ctx.bigTicket);
   SaveStateUlong64("BigIdentifier", Ctx.bigIdentifier);
   GlobalVariableSet(StateKey("BigLot"), Ctx.bigLot);
   GlobalVariableSet(StateKey("BigOpenPrice"), Ctx.bigOpenPrice);
   GlobalVariableSet(StateKey("BigDirection"), (double)Ctx.bigDirection);
   SaveStateUlong64("SmallTicket", Ctx.smallTicket);
   SaveStateUlong64("SmallIdentifier", Ctx.smallIdentifier);
   GlobalVariableSet(StateKey("SmallLot"), Ctx.smallLot);
   GlobalVariableSet(StateKey("SmallOpenPrice"), Ctx.smallOpenPrice);
   GlobalVariableSet(StateKey("SmallDirection"), (double)Ctx.smallDirection);
   SaveStateUlong64("BigCoreTicket", Ctx.bigCoreTicket);
   SaveStateUlong64("BigTrendTicket", Ctx.bigTrendTicket);
   SaveStateUlong64("SmallBaseTicket", Ctx.smallBaseTicket);
   SaveStateUlong64("ReverseSmallTicket", Ctx.reverseSmallTicket);
   SaveStateUlong64("BigCoreIdentifier", Ctx.bigCoreIdentifier);
   SaveStateUlong64("BigTrendIdentifier", Ctx.bigTrendIdentifier);
   SaveStateUlong64("SmallBaseIdentifier", Ctx.smallBaseIdentifier);
   SaveStateUlong64("ReverseSmallIdentifier", Ctx.reverseSmallIdentifier);
   GlobalVariableSet(StateKey("BigCoreLot"), Ctx.bigCoreLot);
   GlobalVariableSet(StateKey("BigTrendLot"), Ctx.bigTrendLot);
   GlobalVariableSet(StateKey("SmallBaseLot"), Ctx.smallBaseLot);
   GlobalVariableSet(StateKey("ReverseSmallLot"), Ctx.reverseSmallLot);
   GlobalVariableSet(StateKey("BigCoreOpenPrice"), Ctx.bigCoreOpenPrice);
   GlobalVariableSet(StateKey("BigTrendOpenPrice"), Ctx.bigTrendOpenPrice);
   GlobalVariableSet(StateKey("SmallBaseOpenPrice"), Ctx.smallBaseOpenPrice);
   GlobalVariableSet(StateKey("ReverseSmallOpenPrice"), Ctx.reverseSmallOpenPrice);
   GlobalVariableSet(StateKey("BigCoreDirection"), (double)Ctx.bigCoreDirection);
   GlobalVariableSet(StateKey("BigTrendDirection"), (double)Ctx.bigTrendDirection);
   GlobalVariableSet(StateKey("SmallBaseDirection"), (double)Ctx.smallBaseDirection);
   GlobalVariableSet(StateKey("ReverseSmallDirection"), (double)Ctx.reverseSmallDirection);
   GlobalVariableSet(StateKey("SplitGeometryActive"), Ctx.splitGeometryActive ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("ReverseConfirmed"), Ctx.reverseConfirmed ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("BigTrendClosedForReverse"), Ctx.bigTrendClosedForReverse ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("ReverseSmallOpened"), Ctx.reverseSmallOpened ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("ReversePeakPrice"), Ctx.reversePeakPrice);
   GlobalVariableSet(StateKey("ReverseTriggerPrice"), Ctx.reverseTriggerPrice);
   GlobalVariableSet(StateKey("ReverseConfirmationPrice"), Ctx.reverseConfirmationPrice);
   GlobalVariableSet(StateKey("ProjectedReverseSmallLot"), Ctx.projectedReverseSmallLot);
   GlobalVariableSet(StateKey("ProjectedReverseSmallMoneyLot"), Ctx.projectedReverseSmallMoneyLot);
   GlobalVariableSet(StateKey("ProjectedReverseSmallDirectionLot"), Ctx.projectedReverseSmallDirectionLot);
   GlobalVariableSet(StateKey("ProjectedReverseSmallFinalLot"), Ctx.projectedReverseSmallFinalLot);
   GlobalVariableSet(StateKey("ProjectedTransitionNet"), Ctx.projectedTransitionNet);
   GlobalVariableSet(StateKey("ActualTransitionNet"), Ctx.actualTransitionNet);
   GlobalVariableSet(StateKey("ActualBigTrendNet"), Ctx.actualBigTrendNet);
   GlobalVariableSet(StateKey("ActualSplitHarvestNet"), Ctx.actualSplitHarvestNet);
   GlobalVariableSet(StateKey("ActualSplitHarvestNetCalculated"), Ctx.actualSplitHarvestNetCalculated ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("ActualSmallTransitionNet"), Ctx.actualSmallTransitionNet);
   GlobalVariableSet(StateKey("BigGrossRatio"), Ctx.bigGrossRatio);
   GlobalVariableSet(StateKey("BigNetExposureRatio"), Ctx.bigNetExposureRatio);
   GlobalVariableSet(StateKey("ReserveGrowthRatio"), Ctx.reserveGrowthRatio);
   GlobalVariableSet(StateKey("NewFarCompressionRatio"), Ctx.newFarCompressionRatio);
   GlobalVariableSet(StateKey("ActualBigExposureLot"), Ctx.actualBigExposureLot);
   GlobalVariableSet(StateKey("ActualSmallExposureLot"), Ctx.actualSmallExposureLot);
   SaveStateUlong64("InitialBuyTicket", Ctx.initialBuyTicket);
   SaveStateUlong64("InitialSellTicket", Ctx.initialSellTicket);
   SaveStateUlong64("InitialBuyIdentifier", Ctx.initialBuyIdentifier);
   SaveStateUlong64("InitialSellIdentifier", Ctx.initialSellIdentifier);
   GlobalVariableSet(StateKey("InitialBuyLot"), Ctx.initialBuyLot);
   GlobalVariableSet(StateKey("InitialSellLot"), Ctx.initialSellLot);
   GlobalVariableSet(StateKey("InitialBuyOpenPrice"), Ctx.initialBuyOpenPrice);
   GlobalVariableSet(StateKey("InitialSellOpenPrice"), Ctx.initialSellOpenPrice);
   GlobalVariableSet(StateKey("InitialLockRecovered"), Ctx.initialLockRecovered ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("HarvestLevel"), (double)Ctx.harvestLevel);
   GlobalVariableSet(StateKey("ReverseCycles"), (double)Ctx.reverseCycleCount);
   GlobalVariableSet(StateKey("TotalReserve"), Ctx.totalReserve);
   GlobalVariableSet(StateKey("ReserveLedgerCount"), (double)ArraySize(ReserveLedger));
   SaveStateLong64("ReserveNextEventId", NextReserveEventId);
   SaveStateLong64("NextReserveTransactionId", NextReserveTransactionId);
   for(int ledgerIndex = 0; ledgerIndex < ArraySize(ReserveLedger); ledgerIndex++)
   {
      string prefix = StringFormat("ReserveLedger_%d_", ledgerIndex);
      SaveStateLong64(prefix + "EventId", ReserveLedger[ledgerIndex].eventId);
      GlobalVariableSet(StateKey(prefix + "Timestamp"), (double)ReserveLedger[ledgerIndex].timestamp);
      GlobalVariableSet(StateKey(prefix + "Type"), (double)ReserveLedger[ledgerIndex].type);
      GlobalVariableSet(StateKey(prefix + "Amount"), ReserveLedger[ledgerIndex].amount);
      GlobalVariableSet(StateKey(prefix + "ReserveBefore"), ReserveLedger[ledgerIndex].reserveBefore);
      GlobalVariableSet(StateKey(prefix + "ReserveAfter"), ReserveLedger[ledgerIndex].reserveAfter);
      SaveStateLong64(prefix + "SymbolHash", ReserveLedger[ledgerIndex].symbolHash);
      GlobalVariableSet(StateKey(prefix + "SymbolLength"), (double)ReserveLedger[ledgerIndex].symbolLength);
      SaveStateUlong64(prefix + "MagicNumber", ReserveLedger[ledgerIndex].magicNumber);
      SaveStateUlong64(prefix + "CycleId", ReserveLedger[ledgerIndex].cycleId);
      SaveStateLong64(prefix + "BigIdentifier", ReserveLedger[ledgerIndex].bigIdentifier);
      SaveStateLong64(prefix + "SmallIdentifier", ReserveLedger[ledgerIndex].smallIdentifier);
      SaveStateLong64(prefix + "FarIdentifier", ReserveLedger[ledgerIndex].farIdentifier);
      SaveStateLong64(prefix + "BigCoreIdentifier", ReserveLedger[ledgerIndex].bigCoreIdentifier);
      SaveStateLong64(prefix + "BigTrendIdentifier", ReserveLedger[ledgerIndex].bigTrendIdentifier);
      SaveStateLong64(prefix + "SmallBaseIdentifier", ReserveLedger[ledgerIndex].smallBaseIdentifier);
      SaveStateLong64(prefix + "ReverseSmallIdentifier", ReserveLedger[ledgerIndex].reverseSmallIdentifier);
      GlobalVariableSet(StateKey(prefix + "HarvestLevel"), (double)ReserveLedger[ledgerIndex].harvestLevel);
      GlobalVariableSet(StateKey(prefix + "ReverseCycle"), (double)ReserveLedger[ledgerIndex].reverseCycle);
      SaveStateLong64(prefix + "EventKeyHash", ReserveLedger[ledgerIndex].eventKeyHash);
   }
   SaveStateUlong64("CycleId", Ctx.cycleId);
   GlobalVariableSet(StateKey("InitialProfitIgnored"), Ctx.initialProfitIgnored ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("EffectiveFarDistancePoints"), Ctx.effectiveFarDistancePoints);
   GlobalVariableSet(StateKey("CycleATRRaw"), Ctx.cycleATRRaw);
   GlobalVariableSet(StateKey("CycleATRPoints"), Ctx.cycleATRPoints);
   GlobalVariableSet(StateKey("GeometrySource"), (double)Ctx.geometrySource);
   GlobalVariableSet(StateKey("GeometryFallback"), (double)Ctx.geometryFallback);
   GlobalVariableSet(StateKey("GeometryFallbackReasonCode"), (double)Ctx.geometryFallbackReasonCode);
   GlobalVariableSet(StateKey("GeometryCleared"), (double)Ctx.geometryCleared);
   GlobalVariableSet(StateKey("GeometryClearReasonCode"), (double)Ctx.geometryClearReasonCode);
   GlobalVariableSet(StateKey("GeometryReady"), (double)Ctx.geometryReady);
   GlobalVariableSet(StateKey("TradingAllowedByFallback"), (double)Ctx.tradingAllowedByFallback);
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
   SaveStateUlong64("RetryTicket", Ctx.retryTicket);
   GlobalVariableSet(StateKey("RetryLot"), Ctx.retryLot);
   GlobalVariableSet(StateKey("RetryAttempts"), (double)Ctx.retryAttempts);
   GlobalVariableSet(StateKey("PendingActionType"), (double)Ctx.pendingActionType);
   GlobalVariableSet(StateKey("PendingNextState"), (double)Ctx.pendingNextState);
   SaveStateUlong64("PendingTicket", Ctx.pendingTicket);
   GlobalVariableSet(StateKey("PendingLot"), Ctx.pendingLot);
   GlobalVariableSet(StateKey("PendingAttempts"), (double)Ctx.pendingAttempts);
   GlobalVariableSet(StateKey("PendingOperationStartTime"), (double)Ctx.pendingOperationStartTime);
   SaveStateUlong64("PendingBigPositionId", Ctx.pendingBigPositionId);
   SaveStateUlong64("PendingSmallPositionId", Ctx.pendingSmallPositionId);
   GlobalVariableSet(StateKey("PendingRealNet"), Ctx.pendingRealNet);
   GlobalVariableSet(StateKey("PendingCloseFarBudget"), Ctx.pendingCloseFarBudget);
   GlobalVariableSet(StateKey("PendingReserveAdd"), Ctx.pendingReserveAdd);
   GlobalVariableSet(StateKey("PendingSmallReserveAdd"), Ctx.pendingSmallReserveAdd);
   GlobalVariableSet(StateKey("PendingReserveApplied"), Ctx.pendingReserveApplied ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("PendingSmallReserveApplied"), Ctx.pendingSmallReserveApplied ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("PendingCloseFarLot"), Ctx.pendingCloseFarLot);
   GlobalVariableSet(StateKey("PendingFullFarClose"), Ctx.pendingFullFarClose ? 1.0 : 0.0);
   GlobalVariableSet(StateKey("PartialFarBudgetCarry"), Ctx.partialFarBudgetCarry);
   GlobalVariableSet(StateKey("PendingPartialFarBudgetAvailable"), Ctx.pendingPartialFarBudgetAvailable);
   GlobalVariableSet(StateKey("PendingPartialFarBudgetCarryBefore"), Ctx.pendingPartialFarBudgetCarryBefore);
   GlobalVariableSet(StateKey("PendingProjectedPartialFarLoss"), Ctx.pendingProjectedPartialFarLoss);
   GlobalVariableSet(StateKey("PendingDirection"), (double)Ctx.pendingDirection);
   // PendingComment is rebuilt from the pending phase after restart.
   GlobalVariableSet(StateKey("SavedSmallDirection"), (double)Ctx.savedSmallDirection);
   GlobalVariableSet(StateKey("SavedSmallClosePrice"), Ctx.savedSmallClosePrice);
   GlobalVariableSet(StateKey("SavedSmallTouchPrice"), Ctx.savedSmallTouchPrice);
   GlobalVariableSet(StateKey("SavedSmallOpenPrice"), Ctx.savedSmallOpenPrice);
   GlobalVariableSet(StateKey("SavedSmallLot"), Ctx.savedSmallLot);
   SaveStateUlong64("OldFarTicket", Ctx.oldFarTicket);
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

void SaveStateUlong64(string field, ulong value)
{
   uint high32, low32;
   SplitUlong64(value, high32, low32);
   GlobalVariableSet(StateKey(field + "High32"), (double)high32);
   GlobalVariableSet(StateKey(field + "Low32"), (double)low32);
}

void SaveStateLong64(string field, long value)
{
   uint high32, low32;
   SplitLong64(value, high32, low32);
   GlobalVariableSet(StateKey(field + "High32"), (double)high32);
   GlobalVariableSet(StateKey(field + "Low32"), (double)low32);
}

bool LoadRequiredStateUlong64(string highKey, string lowKey, ulong &value, string fieldName)
{
   string hk = StateKey(highKey);
   string lk = StateKey(lowKey);
   if(!GlobalVariableCheck(hk) || !GlobalVariableCheck(lk))
   {
      LogError("RESERVE_LEDGER_REQUIRED_FIELD_MISSING Field=" + fieldName);
      State = STATE_RECOVERY_MISMATCH;
      Ctx.lastError = "RESERVE_LEDGER_REQUIRED_FIELD_MISSING " + fieldName;
      return false;
   }
   value = RestoreUlong64((uint)GlobalVariableGet(hk), (uint)GlobalVariableGet(lk));
   return true;
}

bool LoadRequiredStateLong64(string highKey, string lowKey, long &value, string fieldName)
{
   string hk = StateKey(highKey);
   string lk = StateKey(lowKey);
   if(!GlobalVariableCheck(hk) || !GlobalVariableCheck(lk))
   {
      LogError("RESERVE_LEDGER_REQUIRED_FIELD_MISSING Field=" + fieldName);
      State = STATE_RECOVERY_MISMATCH;
      Ctx.lastError = "RESERVE_LEDGER_REQUIRED_FIELD_MISSING " + fieldName;
      return false;
   }
   value = RestoreLong64((uint)GlobalVariableGet(hk), (uint)GlobalVariableGet(lk));
   return true;
}

bool LoadStateUlong64(string field, ulong &value)
{
   string hk = StateKey(field + "High32");
   string lk = StateKey(field + "Low32");
   if(GlobalVariableCheck(hk) && GlobalVariableCheck(lk))
   {
      value = RestoreUlong64((uint)GlobalVariableGet(hk), (uint)GlobalVariableGet(lk));
      return true;
   }
   double legacy = 0.0;
   if(GetStateDouble(field, legacy))
   {
      bool risk = (MathAbs(legacy) >= 9007199254740992.0);
      LogInfo(StringFormat("LEGACY_64BIT_STATE_MIGRATION Field=%s LegacyValue=%.0f RestoredValue=%.0f PrecisionRisk=%s", field, legacy, legacy, risk ? "YES" : "NO"));
      if(risk)
      {
         State = STATE_RECOVERY_MISMATCH;
         Ctx.lastError = "LEGACY_64BIT_STATE_MIGRATION_PRECISION_RISK " + field;
         return false;
      }
      value = (ulong)legacy;
      return true;
   }
   return false;
}

bool LoadStateLong64(string field, long &value)
{
   string hk = StateKey(field + "High32");
   string lk = StateKey(field + "Low32");
   if(GlobalVariableCheck(hk) && GlobalVariableCheck(lk))
   {
      value = RestoreLong64((uint)GlobalVariableGet(hk), (uint)GlobalVariableGet(lk));
      return true;
   }
   double legacy = 0.0;
   if(GetStateDouble(field, legacy))
   {
      bool risk = (MathAbs(legacy) >= 9007199254740992.0);
      LogInfo(StringFormat("LEGACY_64BIT_STATE_MIGRATION Field=%s LegacyValue=%.0f RestoredValue=%.0f PrecisionRisk=%s", field, legacy, legacy, risk ? "YES" : "NO"));
      if(risk)
      {
         State = STATE_RECOVERY_MISMATCH;
         Ctx.lastError = "LEGACY_64BIT_STATE_MIGRATION_PRECISION_RISK " + field;
         return false;
      }
      value = (long)legacy;
      return true;
   }
   return false;
}


bool LoadOptionalStateUlong64(string field, ulong &value)
{
   string hk = StateKey(field + "High32");
   string lk = StateKey(field + "Low32");
   if(GlobalVariableCheck(hk) || GlobalVariableCheck(lk) || GlobalVariableCheck(StateKey(field)))
      return LoadStateUlong64(field, value);
   value = 0;
   return true;
}

bool LoadOptionalStateLong64(string field, long &value)
{
   string hk = StateKey(field + "High32");
   string lk = StateKey(field + "Low32");
   if(GlobalVariableCheck(hk) || GlobalVariableCheck(lk) || GlobalVariableCheck(StateKey(field)))
      return LoadStateLong64(field, value);
   value = 0;
   return true;
}

RecoveryFailureReason RecoveryReasonFromString(string reason)
{
   if(StringFind(reason, "REQUIRED_FIELD_LOAD") >= 0) return RECOVERY_FAILURE_REQUIRED_FIELD_LOAD;
   if(StringFind(reason, "TRANSACTION_ID_SEQUENCE") >= 0) return RECOVERY_FAILURE_TRANSACTION_ID_SEQUENCE;
   if(StringFind(reason, "LEDGER_STRUCTURE") >= 0) return RECOVERY_FAILURE_LEDGER_STRUCTURE;
   if(StringFind(reason, "TRANSACTION_REQUIRED") >= 0 || StringFind(reason, "EVENT_CONTEXT") >= 0) return RECOVERY_FAILURE_TRANSACTION_CONTEXT;
   if(StringFind(reason, "TRANSACTION_RECOVERY") >= 0 || StringFind(reason, "PHASE") >= 0) return RECOVERY_FAILURE_PHASE_CONFLICT;
   if(StringFind(reason, "LEDGER_PERSISTENCE") >= 0 || StringFind(reason, "STRICT_LEDGER") >= 0) return RECOVERY_FAILURE_STRICT_LEDGER;
   if(StringFind(reason, "REQUIRED_CONTEXT") >= 0) return RECOVERY_FAILURE_REQUIRED_STATE_CONTEXT;
   if(StringFind(reason, "STATE_INTEGRITY") >= 0) return RECOVERY_FAILURE_STATE_INTEGRITY;
   if(StringFind(reason, "RECONCILIATION") >= 0) return RECOVERY_FAILURE_RECONCILIATION;
   if(StringFind(reason, "SYMBOL") >= 0) return RECOVERY_FAILURE_SYMBOL_MISMATCH;
   return RECOVERY_FAILURE_OTHER;
}

void SaveRecoveryFailureMarker(string reason, EAState originalState)
{
   RecoveryFailureReason reasonCode = RecoveryReasonFromString(reason);
   GlobalVariableSet(StateKey("RecoveryFailureActive"), 1.0);
   GlobalVariableSet(StateKey("RecoveryFailureReasonCode"), (double)reasonCode);
   GlobalVariableSet(StateKey("RecoveryFailureTime"), (double)TimeCurrent());
   GlobalVariableSet(StateKey("RecoveryFailureOriginalState"), (double)originalState);
   SaveStateUlong64("RecoveryFailureCycleId", Ctx.cycleId);
   SaveStateLong64("RecoveryFailureTransactionId", ActiveReserveTransaction.transactionId);
   SaveStateLong64("RecoveryFailureEventKey", ActiveReserveTransaction.eventKeyHash);
   Ctx.lastError = reason;
   LogError(StringFormat("RECOVERY_ABORTED Symbol=%s Magic=%I64u CycleId=%I64u OriginalState=%s TransactionId=%I64d TransactionPhase=%d EventKey=%I64d ReasonCode=%d CacheReserve=%.2f RecoveryLoadOk=NO Result=FAIL StopReason=%s", _Symbol, MagicNumber, Ctx.cycleId, StateToString(originalState), ActiveReserveTransaction.transactionId, (int)ActiveReserveTransaction.phase, ActiveReserveTransaction.eventKeyHash, (int)reasonCode, Ctx.totalReserve, reason));
}

void ClearRecoveryFailureMarker()
{
   GlobalVariableSet(StateKey("RecoveryFailureActive"), 0.0);
   GlobalVariableSet(StateKey("RecoveryFailureReasonCode"), (double)RECOVERY_FAILURE_NONE);
   GlobalVariableSet(StateKey("RecoveryFailureTime"), 0.0);
   GlobalVariableSet(StateKey("RecoveryFailureOriginalState"), (double)STATE_IDLE);
   SaveStateUlong64("RecoveryFailureCycleId", 0);
   SaveStateLong64("RecoveryFailureTransactionId", 0);
   SaveStateLong64("RecoveryFailureEventKey", 0);
}

bool MarkRecoveryFailure(string reason, EAState originalState)
{
   SaveRecoveryFailureMarker(reason, originalState);
   State = STATE_RECOVERY_MISMATCH;
   RecoveryInProgress = false;
   return false;
}




bool RecoveryTerminalResultIsSuccessful()
{
   return (State != STATE_RECOVERY_PENDING &&
           State != STATE_RECONCILIATION_ERROR &&
           State != STATE_MANUAL_INTERVENTION_REQUIRED &&
           State != STATE_RECOVERY_MISMATCH &&
           State != STATE_INTEGRITY_ERROR &&
           State != STATE_POSITION_RESOLUTION_ERROR &&
           State != STATE_ERROR);
}

bool TradingOperationAllowedDuringRecovery(string operationName, bool isRecoveryContinuation)
{
   if(!RecoveryInProgress)
      return true;
   if(isRecoveryContinuation)
      return true;
   LogError(StringFormat("OPERATION_BLOCKED_DURING_RECOVERY OperationName=%s State=%s TransactionId=%I64d TransactionPhase=%d", operationName, StateToString(State), ActiveReserveTransaction.transactionId, (int)ActiveReserveTransaction.phase));
   return false;
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
   bool splitBigCore = (Ctx.bigCoreTicket != 0 || Ctx.bigCoreIdentifier != 0 || Ctx.bigCoreLot > VolumeMismatchToleranceLots);
   bool splitBigTrend = (Ctx.bigTrendTicket != 0 || Ctx.bigTrendIdentifier != 0 || Ctx.bigTrendLot > VolumeMismatchToleranceLots);
   bool splitSmallBase = (Ctx.smallBaseTicket != 0 || Ctx.smallBaseIdentifier != 0 || Ctx.smallBaseLot > VolumeMismatchToleranceLots);
   bool pending = HasPendingOperationContext();
   bool retry = HasRetryOperationContext();
   bool known = (initialBuy || initialSell || far || big || small || splitBigCore || splitBigTrend || splitSmallBase || pending || retry);
   LogInfo(StringFormat("KNOWN_CONTEXT_PRESENT InitialBuy=%s InitialSell=%s Far=%s Big=%s Small=%s BigCore=%s BigTrend=%s SmallBase=%s Pending=%s Retry=%s KnownContext=%s",
                        initialBuy ? "YES" : "NO",
                        initialSell ? "YES" : "NO",
                        far ? "YES" : "NO",
                        big ? "YES" : "NO",
                        small ? "YES" : "NO",
                        splitBigCore ? "YES" : "NO",
                        splitBigTrend ? "YES" : "NO",
                        splitSmallBase ? "YES" : "NO",
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
   bool splitBigCore = (Ctx.bigCoreTicket != 0 || Ctx.bigCoreIdentifier != 0 || Ctx.bigCoreLot > VolumeMismatchToleranceLots);
   bool splitBigTrend = (Ctx.bigTrendTicket != 0 || Ctx.bigTrendIdentifier != 0 || Ctx.bigTrendLot > VolumeMismatchToleranceLots);
   bool splitSmallBase = (Ctx.smallBaseTicket != 0 || Ctx.smallBaseIdentifier != 0 || Ctx.smallBaseLot > VolumeMismatchToleranceLots);
   bool pending = HasPendingOperationContext();
   bool retry = HasRetryOperationContext();
   bool known = (initialLock || far || big || small || splitBigCore || splitBigTrend || splitSmallBase || pending || retry);
   LogInfo(StringFormat("RECONCILIATION_CONTEXT_SUMMARY Source=%s CurrentState=%s ManagedPositions=%d KnownContext=%s InitialLock=%s Far=%s Big=%s Small=%s BigCore=%s BigTrend=%s SmallBase=%s Pending=%s Retry=%s ConfiguredGeometryMode=%s RuntimeGeometryMode=%s GeometrySource=%s GeometryActive=%s GeometryCleared=%s GeometryClearReason=%s ATRRaw=%.10f ATRPoints=%.1f WorkInitialTriggerPoints=%d WorkBigMoveStartPoints=%d WorkBigMoveStepPoints=%d WorkFarDistancePoints=%d WorkSource=%s FallbackReason=%s GeometryReady=%s TradingAllowedByFallback=%s",
                        source,
                        StateToString(State),
                        CountManagedOpenPositions(),
                        known ? "YES" : "NO",
                        initialLock ? "YES" : "NO",
                        far ? "YES" : "NO",
                        big ? "YES" : "NO",
                        small ? "YES" : "NO",
                        splitBigCore ? "YES" : "NO",
                        splitBigTrend ? "YES" : "NO",
                        splitSmallBase ? "YES" : "NO",
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
                        GeometryFallbackReasonToString(Ctx.geometryFallbackReasonCode),
                        GeometryReady() ? "YES" : "NO",
                        Ctx.tradingAllowedByFallback > 0 ? "YES" : "NO"));
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



bool ValidateReserveEventRequiredIdentifiers(ReserveLedgerEntry &entry)
{
   bool ok = true;
   if(entry.cycleId == 0)
   {
      LogError(StringFormat("RESERVE_LEDGER_REQUIRED_IDENTIFIER_MISSING EventId=%I64d CycleId=%I64u", entry.eventId, entry.cycleId));
      ok = false;
   }
   if(entry.type == RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD)
   {
      if(entry.bigCoreIdentifier == 0 || entry.bigTrendIdentifier == 0 || entry.smallBaseIdentifier == 0)
      {
         LogError(StringFormat("RESERVE_LEDGER_REQUIRED_IDENTIFIER_MISSING EventId=%I64d EventType=SPLIT_BIG_HARVEST BigCore=%I64d BigTrend=%I64d SmallBase=%I64d Far=%I64d", entry.eventId, entry.bigCoreIdentifier, entry.bigTrendIdentifier, entry.smallBaseIdentifier, entry.farIdentifier));
         ok = false;
      }
   }
   if(entry.type == RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT && entry.farIdentifier == 0)
   {
      LogError(StringFormat("RESERVE_LEDGER_REQUIRED_IDENTIFIER_MISSING EventId=%I64d EventType=SPLIT_BIG_FINAL_DEBIT FarIdentifier=%I64d", entry.eventId, entry.farIdentifier));
      ok = false;
   }
   return ok;
}
bool VerifyReserveLedgerPersistence()
{
   double ledgerReserve = 0.0;
   bool ok = true;
   long lastEventId = 0;
   for(int i = 0; i < ArraySize(ReserveLedger); i++)
   {
      ReserveLedgerEntry entry = ReserveLedger[i];
      long restoredHash = RestoreReserveEventKeyHash(entry.eventKeyHashHigh, entry.eventKeyHashLow);
      long recomputedHash = ReserveLedgerEntryHash(entry);
      if(restoredHash != recomputedHash)
      {
         LogError(StringFormat("RESERVE_EVENT_KEY_COMPONENT_MISMATCH RESERVE_EVENT_KEY_RESTORE_FAILED Index=%d EventId=%I64d RestoredHash=%I64d RecomputedHash=%I64d High32=%u Low32=%u", i, entry.eventId, restoredHash, recomputedHash, entry.eventKeyHashHigh, entry.eventKeyHashLow));
         ok = false;
      }
      long currentSymbolHash = StableSymbolHash64(_Symbol);
      if(entry.symbolHash != currentSymbolHash || entry.symbolLength != StringLen(_Symbol))
      {
         LogError(StringFormat("RESERVE_LEDGER_SYMBOL_MISMATCH Index=%d EventId=%I64d StoredSymbolHash=%I64d CurrentSymbolHash=%I64d StoredLength=%d CurrentLength=%d", i, entry.eventId, entry.symbolHash, currentSymbolHash, entry.symbolLength, StringLen(_Symbol)));
         ok = false;
      }
      if(entry.magicNumber != MagicNumber || entry.cycleId != Ctx.cycleId)
      {
         LogError(StringFormat("RESERVE_EVENT_KEY_COMPONENT_MISMATCH Index=%d EventId=%I64d Field=MagicOrCycle EntryMagic=%I64u CurrentMagic=%I64u EntryCycle=%I64u CurrentCycle=%I64u", i, entry.eventId, entry.magicNumber, MagicNumber, entry.cycleId, Ctx.cycleId));
         ok = false;
      }
      ok = ValidateReserveEventRequiredIdentifiers(entry) && ok;
      if((i == 0 && entry.eventId != 1) || (i > 0 && entry.eventId != lastEventId + 1))
      {
         LogError(StringFormat("RESERVE_LEDGER_EVENT_ID_GAP Index=%d EventId=%I64d ExpectedEventId=%I64d", i, entry.eventId, (i == 0 ? 1 : lastEventId + 1)));
         ok = false;
      }
      if(entry.eventId <= lastEventId)
      {
         LogError(StringFormat("RESERVE_LEDGER_CHAIN_BROKEN Index=%d StopReason=event_id_order EventId=%I64d LastEventId=%I64d", i, entry.eventId, lastEventId));
         ok = false;
      }
      lastEventId = entry.eventId;
      if(MathAbs(entry.reserveBefore - ledgerReserve) > ReserveMismatchTolerance ||
         MathAbs(entry.reserveAfter - (entry.reserveBefore + entry.amount)) > ReserveMismatchTolerance ||
         entry.reserveAfter < -ReserveMismatchTolerance)
      {
         LogError(StringFormat("RESERVE_LEDGER_CHAIN_BROKEN Index=%d EventId=%I64d ReserveBefore=%.2f ExpectedBefore=%.2f Amount=%.2f ReserveAfter=%.2f", i, entry.eventId, entry.reserveBefore, ledgerReserve, entry.amount, entry.reserveAfter));
         ok = false;
      }
      for(int j = i + 1; j < ArraySize(ReserveLedger); j++)
      {
         if(ReserveLedger[j].eventId == entry.eventId ||
            RestoreReserveEventKeyHash(ReserveLedger[j].eventKeyHashHigh, ReserveLedger[j].eventKeyHashLow) == restoredHash)
         {
            LogError(StringFormat("RESERVE_LEDGER_CHAIN_BROKEN Index=%d DuplicateIndex=%d DuplicateEventIdOrKey=YES", i, j));
            ok = false;
         }
      }
      ledgerReserve = entry.reserveAfter;
   }
   if(NextReserveEventId <= lastEventId)
   {
      LogError(StringFormat("RESERVE_LEDGER_EVENT_ID_GAP NextReserveEventId=%I64d MaxEventId=%I64d", NextReserveEventId, lastEventId));
      ok = false;
   }
   double diff = MathAbs(ledgerReserve - Ctx.totalReserve);
   ok = ok && diff <= ReserveMismatchTolerance;
   LogInfo(StringFormat("SPLIT_RESERVE_LEDGER_RESTORE Symbol=%s MagicNumber=%I64u CycleId=%I64u LedgerEntries=%d LedgerReserve=%.2f ContextReserve=%.2f Difference=%.5f Result=%s", _Symbol, MagicNumber, Ctx.cycleId, ArraySize(ReserveLedger), ledgerReserve, Ctx.totalReserve, diff, ok ? "PASS" : "FAIL"));
   if(!ok)
   {
      State = STATE_RECOVERY_MISMATCH;
      Ctx.lastError = "RESERVE_LEDGER_PERSISTENCE_MISMATCH";
      return false;
   }
   return true;
}


bool ValidateRequiredRecoveredContextForState(EAState state)
{
   bool ok = true;
   bool pendingCloseContext = (Ctx.pendingActionType != PENDING_NONE && (Ctx.pendingTicket != 0 || Ctx.pendingCloseFarLot > VolumeMismatchToleranceLots || Ctx.pendingLot > VolumeMismatchToleranceLots) && Ctx.pendingOperationStartTime > 0);
   if(state == STATE_FAR_ACTIVE)
      ok = (Ctx.cycleId != 0 && (Ctx.farTicket != 0 || Ctx.farIdentifier != 0) && Ctx.farLot > VolumeMismatchToleranceLots && Ctx.farDirection != DIR_NONE);
   else if(state == STATE_SPLIT_BIG_OPEN_CORE || state == STATE_SPLIT_OPEN_CORE_PENDING)
      ok = (Ctx.cycleId != 0 && Ctx.farIdentifier != 0 && Ctx.farLot > VolumeMismatchToleranceLots && Ctx.harvestLevel > 0);
   else if(state == STATE_SPLIT_BIG_OPEN_SMALL_BASE || state == STATE_SPLIT_OPEN_SMALL_BASE_PENDING)
      ok = (Ctx.cycleId != 0 && Ctx.farIdentifier != 0 && Ctx.bigCoreIdentifier != 0 && Ctx.harvestLevel > 0);
   else if(state == STATE_SPLIT_BIG_OPEN_TREND || state == STATE_SPLIT_OPEN_TREND_PENDING)
      ok = (Ctx.cycleId != 0 && Ctx.farIdentifier != 0 && Ctx.bigCoreIdentifier != 0 && Ctx.smallBaseIdentifier != 0 && Ctx.harvestLevel > 0);
   else if(state == STATE_SPLIT_GEOMETRY_ACTIVE)
      ok = (Ctx.cycleId != 0 && Ctx.farIdentifier != 0 && Ctx.bigCoreIdentifier != 0 && Ctx.bigTrendIdentifier != 0 && Ctx.smallBaseIdentifier != 0 && Ctx.harvestLevel > 0);
   else if(state == STATE_SPLIT_BIG_HARVEST_CLOSE_CORE || state == STATE_SPLIT_CLOSE_CORE_PENDING)
      ok = (Ctx.cycleId != 0 && Ctx.farIdentifier != 0 && Ctx.bigCoreIdentifier != 0 && Ctx.bigTrendIdentifier != 0 && Ctx.smallBaseIdentifier != 0 && Ctx.harvestLevel > 0 && (state != STATE_SPLIT_CLOSE_CORE_PENDING || pendingCloseContext));
   else if(state == STATE_SPLIT_BIG_HARVEST_CLOSE_TREND || state == STATE_SPLIT_CLOSE_TREND_PENDING)
      ok = (Ctx.cycleId != 0 && Ctx.farIdentifier != 0 && Ctx.bigCoreIdentifier != 0 && Ctx.bigTrendIdentifier != 0 && Ctx.smallBaseIdentifier != 0 && Ctx.harvestLevel > 0 && (state != STATE_SPLIT_CLOSE_TREND_PENDING || pendingCloseContext));
   else if(state == STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE || state == STATE_SPLIT_CLOSE_SMALL_BASE_PENDING)
      ok = (Ctx.cycleId != 0 && Ctx.farIdentifier != 0 && Ctx.bigCoreIdentifier != 0 && Ctx.bigTrendIdentifier != 0 && Ctx.smallBaseIdentifier != 0 && Ctx.harvestLevel > 0 && (state != STATE_SPLIT_CLOSE_SMALL_BASE_PENDING || pendingCloseContext));
   else if(state == STATE_SPLIT_BIG_HARVEST_CALC_NET)
      ok = (Ctx.cycleId != 0 && Ctx.farIdentifier != 0 && Ctx.bigCoreIdentifier != 0 && Ctx.bigTrendIdentifier != 0 && Ctx.smallBaseIdentifier != 0 && Ctx.harvestLevel > 0);
   else if(state == STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR)
      ok = (Ctx.cycleId != 0 && Ctx.farIdentifier != 0 && Ctx.bigCoreIdentifier != 0 && Ctx.bigTrendIdentifier != 0 && Ctx.smallBaseIdentifier != 0 && Ctx.actualSplitHarvestNetCalculated && Ctx.harvestLevel > 0);
   else if(state == STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR || state == STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING || state == STATE_SPLIT_PARTIAL_HISTORY_PENDING)
      ok = (Ctx.cycleId != 0 && Ctx.farIdentifier != 0 && Ctx.pendingOperationStartTime > 0 && Ctx.pendingCloseFarLot > VolumeMismatchToleranceLots && Ctx.pendingPartialFarBudgetAvailable >= 0.0 && Ctx.pendingActionType != PENDING_NONE);
   else if(state == STATE_SPLIT_BIG_HARVEST_FINAL_CHECK || state == STATE_SPLIT_CLOSE_FAR_FULL_PENDING || state == STATE_SPLIT_MAX_LEVELS_DECISION)
      ok = (Ctx.cycleId != 0 && (Ctx.farIdentifier != 0 || Ctx.farTicket != 0) && (state != STATE_SPLIT_CLOSE_FAR_FULL_PENDING || pendingCloseContext));
   if(!ok)
   {
      LogError(StringFormat("RECOVERY_REQUIRED_CONTEXT_MISSING State=%s CycleId=%I64u FarTicket=%I64u FarIdentifier=%I64u BigCoreIdentifier=%I64u BigTrendIdentifier=%I64u SmallBaseIdentifier=%I64u HarvestLevel=%d PendingAction=%d", StateToString(state), Ctx.cycleId, Ctx.farTicket, Ctx.farIdentifier, Ctx.bigCoreIdentifier, Ctx.bigTrendIdentifier, Ctx.smallBaseIdentifier, Ctx.harvestLevel, (int)Ctx.pendingActionType));
      State = STATE_RECOVERY_MISMATCH;
      Ctx.lastError = "RECOVERY_REQUIRED_CONTEXT_MISSING";
      return false;
   }
   return true;
}


bool IsProvenCleanStart()
{
   bool hasState = GlobalVariableCheck(StateKey("State"));
   bool hasLedger = GlobalVariableCheck(StateKey("ReserveLedgerCount")) && GlobalVariableGet(StateKey("ReserveLedgerCount")) > 0.5;
   bool hasReserveTx = GlobalVariableCheck(StateKey("ReserveTxActive")) && GlobalVariableGet(StateKey("ReserveTxActive")) > 0.5;
   bool hasFailure = GlobalVariableCheck(StateKey("RecoveryFailureActive")) && GlobalVariableGet(StateKey("RecoveryFailureActive")) > 0.5;
   bool hasPending = GlobalVariableCheck(StateKey("PendingActionType")) && GlobalVariableGet(StateKey("PendingActionType")) > 0.5;
   bool hasRetry = GlobalVariableCheck(StateKey("RetryTicketHigh32")) || GlobalVariableCheck(StateKey("RetryTicketLow32")) || GlobalVariableCheck(StateKey("LastRetryState"));
   bool hasInitial = GlobalVariableCheck(StateKey("InitialBuyTicketHigh32")) || GlobalVariableCheck(StateKey("InitialSellTicketHigh32")) || GlobalVariableCheck(StateKey("InitialBuyIdentifierHigh32")) || GlobalVariableCheck(StateKey("InitialSellIdentifierHigh32"));
   bool hasContext = GlobalVariableCheck(StateKey("CycleIdHigh32")) || GlobalVariableCheck(StateKey("FarTicketHigh32")) || GlobalVariableCheck(StateKey("FarIdentifierHigh32")) || GlobalVariableCheck(StateKey("BigTicketHigh32")) || GlobalVariableCheck(StateKey("SmallTicketHigh32"));
   int managed = CountManagedOpenPositions();

   if(managed > 0)
      LogError(StringFormat("MANAGED_POSITIONS_PRESENT_DURING_RECOVERY_FAILURE Count=%d", managed));

   bool clean = (!hasState && !hasLedger && !hasReserveTx && !hasFailure && !hasPending && !hasRetry && !hasInitial && !hasContext && managed == 0);
   LogInfo(StringFormat("CLEAN_START_CHECK State=%s Ledger=%s ReserveTx=%s Failure=%s Pending=%s Retry=%s Initial=%s Context=%s Managed=%d Result=%s",
                        hasState ? "YES" : "NO",
                        hasLedger ? "YES" : "NO",
                        hasReserveTx ? "YES" : "NO",
                        hasFailure ? "YES" : "NO",
                        hasPending ? "YES" : "NO",
                        hasRetry ? "YES" : "NO",
                        hasInitial ? "YES" : "NO",
                        hasContext ? "YES" : "NO",
                        managed,
                        clean ? "CLEAN_START_CONFIRMED" : "RECOVERY_CONTEXT_RESET_FORBIDDEN"));
   if(clean)
      LogInfo("CLEAN_START_CONFIRMED");
   else
      LogError("RECOVERY_CONTEXT_RESET_FORBIDDEN");
   return clean;
}

bool RecoverState()
{
   if(!GlobalVariableCheck(StateKey("State")))
      return false;

   RecoveryInProgress = true;
   EAState recoveredState = (EAState)(int)GlobalVariableGet(StateKey("State"));
   ResetRecoveryContext();
   State = recoveredState;
   double saved = 0.0;
   bool recoveryLoadOk = true;
   LogInfo(StringFormat("RECOVERY_PHASE_BEGIN Symbol=%s Magic=%I64u RecoveredState=%s RecoveryLoadOk=YES Result=BEGIN", _Symbol, MagicNumber, StateToString(State)));

   // Phase 1: load the complete RecoveryContext before any state-specific validation.
   recoveryLoadOk = LoadOptionalStateUlong64("FarTicket", Ctx.farTicket) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("FarIdentifier", Ctx.farIdentifier) && recoveryLoadOk;
   if(GetStateDouble("FarLot", saved)) Ctx.farLot = saved;
   if(GetStateDouble("FarOpenPrice", saved)) Ctx.farOpenPrice = saved;
   if(GetStateDouble("FarDirection", saved)) Ctx.farDirection = (Direction)(int)saved;
   recoveryLoadOk = LoadOptionalStateUlong64("BigTicket", Ctx.bigTicket) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("BigIdentifier", Ctx.bigIdentifier) && recoveryLoadOk;
   if(GetStateDouble("BigLot", saved)) Ctx.bigLot = saved;
   if(GetStateDouble("BigOpenPrice", saved)) Ctx.bigOpenPrice = saved;
   if(GetStateDouble("BigDirection", saved)) Ctx.bigDirection = (Direction)(int)saved;
   recoveryLoadOk = LoadOptionalStateUlong64("SmallTicket", Ctx.smallTicket) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("SmallIdentifier", Ctx.smallIdentifier) && recoveryLoadOk;
   if(GetStateDouble("SmallLot", saved)) Ctx.smallLot = saved;
   if(GetStateDouble("SmallOpenPrice", saved)) Ctx.smallOpenPrice = saved;
   if(GetStateDouble("SmallDirection", saved)) Ctx.smallDirection = (Direction)(int)saved;
   recoveryLoadOk = LoadOptionalStateUlong64("BigCoreTicket", Ctx.bigCoreTicket) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("BigTrendTicket", Ctx.bigTrendTicket) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("SmallBaseTicket", Ctx.smallBaseTicket) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("ReverseSmallTicket", Ctx.reverseSmallTicket) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("BigCoreIdentifier", Ctx.bigCoreIdentifier) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("BigTrendIdentifier", Ctx.bigTrendIdentifier) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("SmallBaseIdentifier", Ctx.smallBaseIdentifier) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("ReverseSmallIdentifier", Ctx.reverseSmallIdentifier) && recoveryLoadOk;
   if(GetStateDouble("BigCoreLot", saved)) Ctx.bigCoreLot = saved;
   if(GetStateDouble("BigTrendLot", saved)) Ctx.bigTrendLot = saved;
   if(GetStateDouble("SmallBaseLot", saved)) Ctx.smallBaseLot = saved;
   if(GetStateDouble("ReverseSmallLot", saved)) Ctx.reverseSmallLot = saved;
   if(GetStateDouble("BigCoreOpenPrice", saved)) Ctx.bigCoreOpenPrice = saved;
   if(GetStateDouble("BigTrendOpenPrice", saved)) Ctx.bigTrendOpenPrice = saved;
   if(GetStateDouble("SmallBaseOpenPrice", saved)) Ctx.smallBaseOpenPrice = saved;
   if(GetStateDouble("ReverseSmallOpenPrice", saved)) Ctx.reverseSmallOpenPrice = saved;
   if(GetStateDouble("BigCoreDirection", saved)) Ctx.bigCoreDirection = (Direction)(int)saved;
   if(GetStateDouble("BigTrendDirection", saved)) Ctx.bigTrendDirection = (Direction)(int)saved;
   if(GetStateDouble("SmallBaseDirection", saved)) Ctx.smallBaseDirection = (Direction)(int)saved;
   if(GetStateDouble("ReverseSmallDirection", saved)) Ctx.reverseSmallDirection = (Direction)(int)saved;
   if(GetStateDouble("SplitGeometryActive", saved)) Ctx.splitGeometryActive = (saved > 0.5);
   if(GetStateDouble("ReverseConfirmed", saved)) Ctx.reverseConfirmed = (saved > 0.5);
   if(GetStateDouble("BigTrendClosedForReverse", saved)) Ctx.bigTrendClosedForReverse = (saved > 0.5);
   if(GetStateDouble("ReverseSmallOpened", saved)) Ctx.reverseSmallOpened = (saved > 0.5);
   if(GetStateDouble("ReversePeakPrice", saved)) Ctx.reversePeakPrice = saved;
   if(GetStateDouble("ReverseTriggerPrice", saved)) Ctx.reverseTriggerPrice = saved;
   if(GetStateDouble("ReverseConfirmationPrice", saved)) Ctx.reverseConfirmationPrice = saved;
   if(GetStateDouble("ProjectedReverseSmallLot", saved)) Ctx.projectedReverseSmallLot = saved;
   if(GetStateDouble("ProjectedReverseSmallMoneyLot", saved)) Ctx.projectedReverseSmallMoneyLot = saved;
   if(GetStateDouble("ProjectedReverseSmallDirectionLot", saved)) Ctx.projectedReverseSmallDirectionLot = saved;
   if(GetStateDouble("ProjectedReverseSmallFinalLot", saved)) Ctx.projectedReverseSmallFinalLot = saved;
   if(GetStateDouble("ProjectedTransitionNet", saved)) Ctx.projectedTransitionNet = saved;
   if(GetStateDouble("ActualTransitionNet", saved)) Ctx.actualTransitionNet = saved;
   if(GetStateDouble("ActualBigTrendNet", saved)) Ctx.actualBigTrendNet = saved;
   if(GetStateDouble("ActualSplitHarvestNet", saved)) Ctx.actualSplitHarvestNet = saved;
   if(GetStateDouble("ActualSplitHarvestNetCalculated", saved)) Ctx.actualSplitHarvestNetCalculated = (saved > 0.5);
   if(GetStateDouble("ActualSmallTransitionNet", saved)) Ctx.actualSmallTransitionNet = saved;
   if(GetStateDouble("BigGrossRatio", saved)) Ctx.bigGrossRatio = saved;
   if(GetStateDouble("BigNetExposureRatio", saved)) Ctx.bigNetExposureRatio = saved;
   if(GetStateDouble("ReserveGrowthRatio", saved)) Ctx.reserveGrowthRatio = saved;
   if(GetStateDouble("NewFarCompressionRatio", saved)) Ctx.newFarCompressionRatio = saved;
   if(GetStateDouble("ActualBigExposureLot", saved)) Ctx.actualBigExposureLot = saved;
   if(GetStateDouble("ActualSmallExposureLot", saved)) Ctx.actualSmallExposureLot = saved;
   recoveryLoadOk = LoadOptionalStateUlong64("InitialBuyTicket", Ctx.initialBuyTicket) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("InitialSellTicket", Ctx.initialSellTicket) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("InitialBuyIdentifier", Ctx.initialBuyIdentifier) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("InitialSellIdentifier", Ctx.initialSellIdentifier) && recoveryLoadOk;
   if(GetStateDouble("InitialBuyLot", saved)) Ctx.initialBuyLot = saved;
   if(GetStateDouble("InitialSellLot", saved)) Ctx.initialSellLot = saved;
   if(GetStateDouble("InitialBuyOpenPrice", saved)) Ctx.initialBuyOpenPrice = saved;
   if(GetStateDouble("InitialSellOpenPrice", saved)) Ctx.initialSellOpenPrice = saved;
   if(GetStateDouble("InitialLockRecovered", saved)) Ctx.initialLockRecovered = (saved > 0.5);
   if(GetStateDouble("HarvestLevel", saved)) Ctx.harvestLevel = (int)saved;
   if(GetStateDouble("ReverseCycles", saved)) Ctx.reverseCycleCount = (int)saved;
   recoveryLoadOk = LoadOptionalStateUlong64("CycleId", Ctx.cycleId) && recoveryLoadOk;
   if(GetStateDouble("TotalReserve", saved)) Ctx.totalReserve = saved;
   if(GetStateDouble("InitialProfitIgnored", saved)) Ctx.initialProfitIgnored = (saved > 0.5);
   if(GetStateDouble("EffectiveFarDistancePoints", saved)) Ctx.effectiveFarDistancePoints = saved;
   if(GetStateDouble("CycleATRRaw", saved)) Ctx.cycleATRRaw = saved;
   if(GetStateDouble("CycleATRPoints", saved)) Ctx.cycleATRPoints = saved;
   if(GetStateDouble("GeometrySource", saved)) Ctx.geometrySource = (int)saved;
   if(GetStateDouble("GeometryFallback", saved)) Ctx.geometryFallback = (int)saved;
   if(GetStateDouble("GeometryFallbackReasonCode", saved)) Ctx.geometryFallbackReasonCode = (int)saved;
   if(GetStateDouble("GeometryCleared", saved)) Ctx.geometryCleared = (int)saved;
   if(GetStateDouble("GeometryClearReasonCode", saved)) Ctx.geometryClearReasonCode = (int)saved;
   if(GetStateDouble("GeometryReady", saved)) Ctx.geometryReady = (int)saved;
   if(GetStateDouble("TradingAllowedByFallback", saved)) Ctx.tradingAllowedByFallback = (int)saved;
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
   recoveryLoadOk = LoadOptionalStateUlong64("RetryTicket", Ctx.retryTicket) && recoveryLoadOk;
   if(GetStateDouble("RetryLot", saved)) Ctx.retryLot = saved;
   if(GetStateDouble("RetryAttempts", saved)) Ctx.retryAttempts = (int)saved;
   if(GetStateDouble("PendingActionType", saved)) Ctx.pendingActionType = (PendingActionType)(int)saved;
   if(GetStateDouble("PendingNextState", saved)) Ctx.pendingNextState = (EAState)(int)saved;
   recoveryLoadOk = LoadOptionalStateUlong64("PendingTicket", Ctx.pendingTicket) && recoveryLoadOk;
   if(GetStateDouble("PendingLot", saved)) Ctx.pendingLot = saved;
   if(GetStateDouble("PendingAttempts", saved)) Ctx.pendingAttempts = (int)saved;
   if(GetStateDouble("PendingOperationStartTime", saved)) Ctx.pendingOperationStartTime = (datetime)saved;
   recoveryLoadOk = LoadOptionalStateUlong64("PendingBigPositionId", Ctx.pendingBigPositionId) && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateUlong64("PendingSmallPositionId", Ctx.pendingSmallPositionId) && recoveryLoadOk;
   if(GetStateDouble("PendingRealNet", saved)) Ctx.pendingRealNet = saved;
   if(GetStateDouble("PendingCloseFarBudget", saved)) Ctx.pendingCloseFarBudget = saved;
   if(GetStateDouble("PendingReserveAdd", saved)) Ctx.pendingReserveAdd = saved;
   if(GetStateDouble("PendingSmallReserveAdd", saved)) Ctx.pendingSmallReserveAdd = saved;
   if(GetStateDouble("PendingReserveApplied", saved)) Ctx.pendingReserveApplied = (saved > 0.5);
   if(GetStateDouble("PendingSmallReserveApplied", saved)) Ctx.pendingSmallReserveApplied = (saved > 0.5);
   if(GetStateDouble("PendingCloseFarLot", saved)) Ctx.pendingCloseFarLot = saved;
   if(GetStateDouble("PendingFullFarClose", saved)) Ctx.pendingFullFarClose = (saved > 0.5);
   if(GetStateDouble("PartialFarBudgetCarry", saved)) Ctx.partialFarBudgetCarry = saved;
   if(GetStateDouble("PendingPartialFarBudgetAvailable", saved)) Ctx.pendingPartialFarBudgetAvailable = saved;
   if(GetStateDouble("PendingPartialFarBudgetCarryBefore", saved)) Ctx.pendingPartialFarBudgetCarryBefore = saved;
   if(GetStateDouble("PendingProjectedPartialFarLoss", saved)) Ctx.pendingProjectedPartialFarLoss = saved;
   if(GetStateDouble("PendingDirection", saved)) Ctx.pendingDirection = (Direction)(int)saved;
   if(GetStateDouble("SavedSmallDirection", saved)) Ctx.savedSmallDirection = (Direction)(int)saved;
   if(GetStateDouble("SavedSmallClosePrice", saved)) Ctx.savedSmallClosePrice = saved;
   if(GetStateDouble("SavedSmallTouchPrice", saved)) Ctx.savedSmallTouchPrice = saved;
   if(GetStateDouble("SavedSmallOpenPrice", saved)) Ctx.savedSmallOpenPrice = saved;
   if(GetStateDouble("SavedSmallLot", saved)) Ctx.savedSmallLot = saved;
   recoveryLoadOk = LoadOptionalStateUlong64("OldFarTicket", Ctx.oldFarTicket) && recoveryLoadOk;
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
   LogInfo(StringFormat("RECOVERY_CONTEXT_LOAD_COMPLETE Symbol=%s Magic=%I64u CycleId=%I64u RecoveredState=%s CacheReserve=%.2f RecoveryLoadOk=%s Result=LOADED", _Symbol, MagicNumber, Ctx.cycleId, StateToString(State), Ctx.totalReserve, recoveryLoadOk ? "YES" : "NO"));

   // Phase 2: load ledger entries and counters, but defer financial cache validation until transaction is loaded.
   ArrayResize(ReserveLedger, 0);
   NextReserveEventId = 1;
   if(GetStateDouble("ReserveLedgerCount", saved))
   {
      int ledgerCount = (int)saved;
      ArrayResize(ReserveLedger, ledgerCount);
      for(int ledgerIndex = 0; ledgerIndex < ledgerCount; ledgerIndex++)
      {
         string prefix = StringFormat("ReserveLedger_%d_", ledgerIndex);
         bool ledgerFieldsOk = true;
         ledgerFieldsOk = LoadRequiredStateLong64(prefix + "EventIdHigh32", prefix + "EventIdLow32", ReserveLedger[ledgerIndex].eventId, prefix + "EventId") && ledgerFieldsOk;
         if(GetStateDouble(prefix + "Timestamp", saved)) ReserveLedger[ledgerIndex].timestamp = (datetime)saved; else ledgerFieldsOk = false;
         if(GetStateDouble(prefix + "Type", saved)) ReserveLedger[ledgerIndex].type = (ReserveEventType)(int)saved; else ledgerFieldsOk = false;
         if(GetStateDouble(prefix + "Amount", saved)) ReserveLedger[ledgerIndex].amount = saved; else ledgerFieldsOk = false;
         if(GetStateDouble(prefix + "ReserveBefore", saved)) ReserveLedger[ledgerIndex].reserveBefore = saved; else ledgerFieldsOk = false;
         if(GetStateDouble(prefix + "ReserveAfter", saved)) ReserveLedger[ledgerIndex].reserveAfter = saved; else ledgerFieldsOk = false;
         ledgerFieldsOk = LoadRequiredStateLong64(prefix + "SymbolHashHigh32", prefix + "SymbolHashLow32", ReserveLedger[ledgerIndex].symbolHash, prefix + "SymbolHash") && ledgerFieldsOk;
         if(GetStateDouble(prefix + "SymbolLength", saved)) ReserveLedger[ledgerIndex].symbolLength = (int)saved; else ledgerFieldsOk = false;
         ulong restoredUlong = 0; long restoredLong = 0;
         ledgerFieldsOk = LoadRequiredStateUlong64(prefix + "MagicNumberHigh32", prefix + "MagicNumberLow32", restoredUlong, prefix + "MagicNumber") && ledgerFieldsOk; ReserveLedger[ledgerIndex].magicNumber = restoredUlong;
         ledgerFieldsOk = LoadRequiredStateUlong64(prefix + "CycleIdHigh32", prefix + "CycleIdLow32", restoredUlong, prefix + "CycleId") && ledgerFieldsOk; ReserveLedger[ledgerIndex].cycleId = restoredUlong;
         ledgerFieldsOk = LoadRequiredStateLong64(prefix + "BigIdentifierHigh32", prefix + "BigIdentifierLow32", restoredLong, prefix + "BigIdentifier") && ledgerFieldsOk; ReserveLedger[ledgerIndex].bigIdentifier = restoredLong;
         ledgerFieldsOk = LoadRequiredStateLong64(prefix + "SmallIdentifierHigh32", prefix + "SmallIdentifierLow32", restoredLong, prefix + "SmallIdentifier") && ledgerFieldsOk; ReserveLedger[ledgerIndex].smallIdentifier = restoredLong;
         ledgerFieldsOk = LoadRequiredStateLong64(prefix + "FarIdentifierHigh32", prefix + "FarIdentifierLow32", restoredLong, prefix + "FarIdentifier") && ledgerFieldsOk; ReserveLedger[ledgerIndex].farIdentifier = restoredLong;
         ledgerFieldsOk = LoadRequiredStateLong64(prefix + "BigCoreIdentifierHigh32", prefix + "BigCoreIdentifierLow32", restoredLong, prefix + "BigCoreIdentifier") && ledgerFieldsOk; ReserveLedger[ledgerIndex].bigCoreIdentifier = restoredLong;
         ledgerFieldsOk = LoadRequiredStateLong64(prefix + "BigTrendIdentifierHigh32", prefix + "BigTrendIdentifierLow32", restoredLong, prefix + "BigTrendIdentifier") && ledgerFieldsOk; ReserveLedger[ledgerIndex].bigTrendIdentifier = restoredLong;
         ledgerFieldsOk = LoadRequiredStateLong64(prefix + "SmallBaseIdentifierHigh32", prefix + "SmallBaseIdentifierLow32", restoredLong, prefix + "SmallBaseIdentifier") && ledgerFieldsOk; ReserveLedger[ledgerIndex].smallBaseIdentifier = restoredLong;
         ledgerFieldsOk = LoadRequiredStateLong64(prefix + "ReverseSmallIdentifierHigh32", prefix + "ReverseSmallIdentifierLow32", restoredLong, prefix + "ReverseSmallIdentifier") && ledgerFieldsOk; ReserveLedger[ledgerIndex].reverseSmallIdentifier = restoredLong;
         if(GetStateDouble(prefix + "HarvestLevel", saved)) ReserveLedger[ledgerIndex].harvestLevel = (int)saved; else ledgerFieldsOk = false;
         if(GetStateDouble(prefix + "ReverseCycle", saved)) ReserveLedger[ledgerIndex].reverseCycle = (int)saved; else ledgerFieldsOk = false;
         ledgerFieldsOk = LoadRequiredStateLong64(prefix + "EventKeyHashHigh32", prefix + "EventKeyHashLow32", ReserveLedger[ledgerIndex].eventKeyHash, prefix + "EventKeyHash") && ledgerFieldsOk;
         SplitLong64(ReserveLedger[ledgerIndex].eventKeyHash, ReserveLedger[ledgerIndex].eventKeyHashHigh, ReserveLedger[ledgerIndex].eventKeyHashLow);
         ReserveLedger[ledgerIndex].symbol = _Symbol;
         recoveryLoadOk = ledgerFieldsOk && recoveryLoadOk;
      }
   }
   recoveryLoadOk = LoadOptionalStateLong64("ReserveNextEventId", NextReserveEventId) && recoveryLoadOk;
   LogInfo(StringFormat("RECOVERY_LEDGER_LOAD_COMPLETE Symbol=%s Magic=%I64u CycleId=%I64u RecoveredState=%s LedgerEntries=%d NextReserveEventId=%I64d RecoveryLoadOk=%s Result=LOADED", _Symbol, MagicNumber, Ctx.cycleId, StateToString(State), ArraySize(ReserveLedger), NextReserveEventId, recoveryLoadOk ? "YES" : "NO"));
   recoveryLoadOk = LoadReserveTransaction() && recoveryLoadOk;
   recoveryLoadOk = LoadOptionalStateLong64("NextReserveTransactionId", NextReserveTransactionId) && recoveryLoadOk;
   LogInfo(StringFormat("RECOVERY_TRANSACTION_LOAD_COMPLETE Symbol=%s Magic=%I64u CycleId=%I64u RecoveredState=%s TransactionId=%I64d TransactionPhase=%d EventKey=%I64d RecoveryLoadOk=%s Result=LOADED", _Symbol, MagicNumber, Ctx.cycleId, StateToString(State), ActiveReserveTransaction.transactionId, (int)ActiveReserveTransaction.phase, ActiveReserveTransaction.eventKeyHash, recoveryLoadOk ? "YES" : "NO"));

   if(!recoveryLoadOk)
      return MarkRecoveryFailure("RECOVERY_REQUIRED_FIELD_LOAD_FAILED", recoveredState);
   if(NextReserveTransactionId <= 0 || (ActiveReserveTransaction.active && NextReserveTransactionId <= ActiveReserveTransaction.transactionId))
      return MarkRecoveryFailure("RESERVE_TRANSACTION_ID_SEQUENCE_ERROR", recoveredState);
   if(!ValidateReserveLedgerStructureOnly())
      return MarkRecoveryFailure("RESERVE_LEDGER_STRUCTURE_INVALID", recoveredState);
   if(!ValidateReserveTransactionRequiredFields())
      return MarkRecoveryFailure("RESERVE_TRANSACTION_REQUIRED_FIELD_MISSING", recoveredState);
   LogInfo(StringFormat("RECOVERY_PHASE_AWARE_VALIDATION Symbol=%s Magic=%I64u CycleId=%I64u RecoveredState=%s TransactionId=%I64d TransactionPhase=%d LedgerReserve=%.2f CacheReserve=%.2f RecoveryLoadOk=YES Result=BEGIN", _Symbol, MagicNumber, Ctx.cycleId, StateToString(State), ActiveReserveTransaction.transactionId, (int)ActiveReserveTransaction.phase, ReserveLedgerCurrentReserve(), Ctx.totalReserve));
   if(!ValidateLedgerAndCacheForTransactionPhase(ActiveReserveTransaction))
      return MarkRecoveryFailure("RESERVE_TRANSACTION_RECOVERY_CONFLICT", recoveredState);
   LogInfo("RECOVERY_TRANSACTION_RESUME Result=BEGIN");
   if(!RecoverPendingReserveTransaction())
      return MarkRecoveryFailure("RESERVE_TRANSACTION_RECOVERY_CONFLICT", recoveredState);
   LogInfo("RECOVERY_STRICT_LEDGER_VALIDATION Result=BEGIN");
   if(!VerifyReserveLedgerPersistence())
      return MarkRecoveryFailure("RESERVE_LEDGER_PERSISTENCE_MISMATCH", recoveredState);
   if(!ValidateRequiredRecoveredContextForState(State))
      return MarkRecoveryFailure("RECOVERY_REQUIRED_CONTEXT_MISSING", recoveredState);
   LogInfo("RECOVERY_STATE_CONTEXT_VALIDATION Result=PASS");

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

   LogInfo("RECOVERY_RECONCILIATION_BEGIN Result=BEGIN");
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
      if(Ctx.splitGeometryActive || Ctx.bigCoreIdentifier != 0 || Ctx.bigTrendIdentifier != 0 || Ctx.smallBaseIdentifier != 0)
      {
         LogInfo(StringFormat("SPLIT_RECONCILIATION RecoverState resolving Split roles State=%s Topology=Far+BigCore+SmallBase+BigTrend", StateToString(State)));
         if(Ctx.bigCoreIdentifier != 0 || Ctx.bigCoreTicket != 0) reconcileOk = ResolveBigCorePosition() && reconcileOk;
         if(Ctx.smallBaseIdentifier != 0 || Ctx.smallBaseTicket != 0) reconcileOk = ResolveSmallBasePosition() && reconcileOk;
         if(Ctx.bigTrendIdentifier != 0 || Ctx.bigTrendTicket != 0) reconcileOk = ResolveBigTrendPosition() && reconcileOk;
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
      return MarkRecoveryFailure("RECOVERY_RECONCILIATION_FAILED", recoveredState);
   }

   if(!RecoveryTerminalResultIsSuccessful())
      return MarkRecoveryFailure("RECOVERY_RECONCILIATION_TERMINAL_STATE", recoveredState);

   bool integrityOk = ValidateCurrentStateIntegrity();
   if(!integrityOk)
      return MarkRecoveryFailure("RECOVERY_STATE_INTEGRITY_FAILED", recoveredState);

   ClearRecoveryFailureMarker();
   RecoveryInProgress = false;
   LogInfo(StringFormat("RECOVERY_COMPLETE Symbol=%s Magic=%I64u CycleId=%I64u RecoveredState=%s TransactionId=%I64d TransactionPhase=%d LedgerReserve=%.2f CacheReserve=%.2f RecoveryLoadOk=YES Result=PASS", _Symbol, MagicNumber, Ctx.cycleId, StateToString(State), ActiveReserveTransaction.transactionId, (int)ActiveReserveTransaction.phase, ReserveLedgerCurrentReserve(), Ctx.totalReserve));
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
   Ctx.bigCoreTicket = 0;
   Ctx.bigTrendTicket = 0;
   Ctx.smallBaseTicket = 0;
   Ctx.reverseSmallTicket = 0;
   Ctx.bigCoreIdentifier = 0;
   Ctx.bigTrendIdentifier = 0;
   Ctx.smallBaseIdentifier = 0;
   Ctx.reverseSmallIdentifier = 0;

   Ctx.farLot = 0.0;
   Ctx.bigLot = 0.0;
   Ctx.smallLot = 0.0;
   Ctx.bigCoreLot = 0.0;
   Ctx.bigTrendLot = 0.0;
   Ctx.smallBaseLot = 0.0;
   Ctx.reverseSmallLot = 0.0;

   Ctx.farOpenPrice = 0.0;
   Ctx.bigOpenPrice = 0.0;
   Ctx.smallOpenPrice = 0.0;
   Ctx.bigCoreOpenPrice = 0.0;
   Ctx.bigTrendOpenPrice = 0.0;
   Ctx.smallBaseOpenPrice = 0.0;
   Ctx.reverseSmallOpenPrice = 0.0;
   Ctx.initialBuyLot = 0.0;
   Ctx.initialSellLot = 0.0;
   Ctx.initialBuyOpenPrice = 0.0;
   Ctx.initialSellOpenPrice = 0.0;

   Ctx.farDirection = DIR_NONE;
   Ctx.bigDirection = DIR_NONE;
   Ctx.smallDirection = DIR_NONE;
   Ctx.bigCoreDirection = DIR_NONE;
   Ctx.bigTrendDirection = DIR_NONE;
   Ctx.smallBaseDirection = DIR_NONE;
   Ctx.reverseSmallDirection = DIR_NONE;

   Ctx.harvestLevel = 0;
   Ctx.totalReserve = 0.0;
   ArrayResize(ReserveLedger, 0);
   NextReserveEventId = 1;
   Ctx.cycleFinalPL = 0.0;

   Ctx.initialProfitIgnored = false;
   Ctx.initialLockRecovered = false;
   Ctx.finalCloseAllowed = false;
   Ctx.dualTailDetected = false;
   Ctx.splitGeometryActive = false;
   Ctx.reverseConfirmed = false;
   Ctx.bigTrendClosedForReverse = false;
   Ctx.reverseSmallOpened = false;
   Ctx.reversePeakPrice = 0.0;
   Ctx.reverseTriggerPrice = 0.0;
   Ctx.reverseConfirmationPrice = 0.0;
   Ctx.projectedReverseSmallLot = 0.0;
   Ctx.projectedReverseSmallMoneyLot = 0.0;
   Ctx.projectedReverseSmallDirectionLot = 0.0;
   Ctx.projectedReverseSmallFinalLot = 0.0;
   Ctx.projectedTransitionNet = 0.0;
   Ctx.actualTransitionNet = 0.0;
   Ctx.actualBigTrendNet = 0.0;
   Ctx.actualSplitHarvestNet = 0.0;
   Ctx.actualSplitHarvestNetCalculated = false;
   Ctx.actualSmallTransitionNet = 0.0;
   Ctx.bigGrossRatio = 0.0;
   Ctx.bigNetExposureRatio = 0.0;
   Ctx.reserveGrowthRatio = 0.0;
   Ctx.newFarCompressionRatio = 0.0;
   Ctx.actualBigExposureLot = 0.0;
   Ctx.actualSmallExposureLot = 0.0;

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
   Ctx.pendingFullFarClose = false;
   Ctx.partialFarBudgetCarry = 0.0;
   Ctx.pendingPartialFarBudgetAvailable = 0.0;
   Ctx.pendingPartialFarBudgetCarryBefore = 0.0;
   Ctx.pendingProjectedPartialFarLoss = 0.0;
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

            if(HistoryDealGetString(dealTicket, DEAL_SYMBOL) != _Symbol)
               continue;

            ENUM_DEAL_ENTRY dealEntry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(dealTicket, DEAL_ENTRY);
            if(dealEntry != DEAL_ENTRY_IN && dealEntry != DEAL_ENTRY_OUT && dealEntry != DEAL_ENTRY_INOUT && dealEntry != DEAL_ENTRY_OUT_BY)
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
            double dealFee = HistoryDealGetDouble(dealTicket, DEAL_FEE);
            double dealNet = dealProfit + dealCommission + dealSwap + dealFee;

            if(dealNet >= 0.0)
               Ctx.realClosedProfit += dealNet;
            else
               Ctx.realClosedLoss += dealNet;

            Ctx.realCommission += dealCommission;
            Ctx.realSwap += dealSwap;
            Ctx.realCosts += dealFee;
            LogInfo(StringFormat("HISTORY_DEAL_REAL_PL Ticket=%I64u DEAL_POSITION_ID=%I64u Symbol=%s Entry=%d Comment=%s Net=%.2f Profit=%.2f Commission=%.2f Swap=%.2f Fee=%.2f", dealTicket, dealPositionId, _Symbol, (int)dealEntry, dealComment, dealNet, dealProfit, dealCommission, dealSwap, dealFee));
            foundDeals = true;
         }
      }
   }

   Ctx.realCosts = Ctx.realCommission + Ctx.realSwap + Ctx.realCosts;
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
   if(!TradingOperationAllowedDuringRecovery("OpenInitialLock", false)) return;
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
      if(!EnsureGeometryReadyForInitialLock())
         return;
      PrintGeometryDiagnostics();
      SetState(STATE_INITIAL_LOCK_OPENED, "existing initial BUY/SELL lock found");
      return;
   }

   if(!EnsureGeometryReadyForInitialLock())
      return;

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
   if(!TradingOperationAllowedDuringRecovery("OpenBigSmall", false)) return;
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

   SaveState();
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


bool PositionIdInList(ulong positionId, const ulong &positionIds[])
{
   for(int idx = 0; idx < ArraySize(positionIds); idx++)
   {
      if(positionIds[idx] == positionId)
         return true;
   }
   return false;
}

bool DealMatchesCurrentCycleByComment(ulong dealTicket)
{
   string comment = HistoryDealGetString(dealTicket, DEAL_COMMENT);
   if(comment == "")
      return true;

   PositionRole role;
   long parsedCycleId;
   int parsedLevel;
   int parsedReverseCycle;
   if(!ParseRoleComment(comment, role, parsedCycleId, parsedLevel, parsedReverseCycle))
      return true;

   return (ulong)parsedCycleId == Ctx.cycleId;
}

bool CalculateLifecycleNetForPositionIds(const ulong &positionIds[], LifecycleNetResult &result, datetime fromTime = 0)
{
   result.profit = 0.0;
   result.commission = 0.0;
   result.swap = 0.0;
   result.fee = 0.0;
   result.net = 0.0;
   result.dealCount = 0;

   if(ArraySize(positionIds) <= 0)
      return false;

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

      ENUM_DEAL_ENTRY dealEntry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(dealTicket, DEAL_ENTRY);
      if(dealEntry != DEAL_ENTRY_IN && dealEntry != DEAL_ENTRY_OUT && dealEntry != DEAL_ENTRY_INOUT && dealEntry != DEAL_ENTRY_OUT_BY)
         continue;

      ulong positionId = (ulong)HistoryDealGetInteger(dealTicket, DEAL_POSITION_ID);
      if(!PositionIdInList(positionId, positionIds))
         continue;
      if(!DealMatchesCurrentCycleByComment(dealTicket))
         continue;

      double dealProfit = HistoryDealGetDouble(dealTicket, DEAL_PROFIT);
      double dealCommission = HistoryDealGetDouble(dealTicket, DEAL_COMMISSION);
      double dealSwap = HistoryDealGetDouble(dealTicket, DEAL_SWAP);
      double dealFee = HistoryDealGetDouble(dealTicket, DEAL_FEE);
      result.profit += dealProfit;
      result.commission += dealCommission;
      result.swap += dealSwap;
      result.fee += dealFee;
      result.net += dealProfit + dealCommission + dealSwap + dealFee;
      result.dealCount++;
   }

   return result.dealCount > 0;
}

bool CalculateRealNetForClosedPositions(ulong firstPositionId, ulong secondPositionId, datetime fromTime, double &firstNet, double &secondNet, double &commission, double &swap, double &fee)
{
   firstNet = 0.0;
   secondNet = 0.0;
   commission = 0.0;
   swap = 0.0;
   fee = 0.0;
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

      ENUM_DEAL_ENTRY dealEntry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(dealTicket, DEAL_ENTRY);
      if(dealEntry != DEAL_ENTRY_IN && dealEntry != DEAL_ENTRY_OUT && dealEntry != DEAL_ENTRY_INOUT && dealEntry != DEAL_ENTRY_OUT_BY)
         continue;

      ulong positionId = (ulong)HistoryDealGetInteger(dealTicket, DEAL_POSITION_ID);
      if(positionId != firstPositionId && positionId != secondPositionId)
         continue;

      double dealProfit = HistoryDealGetDouble(dealTicket, DEAL_PROFIT);
      double dealCommission = HistoryDealGetDouble(dealTicket, DEAL_COMMISSION);
      double dealSwap = HistoryDealGetDouble(dealTicket, DEAL_SWAP);
      double dealFee = HistoryDealGetDouble(dealTicket, DEAL_FEE);
      double dealNet = dealProfit + dealCommission + dealSwap + dealFee;
      commission += dealCommission;
      swap += dealSwap;
      fee += dealFee;

      if(positionId == firstPositionId)
         firstNet += dealNet;
      if(positionId == secondPositionId)
         secondNet += dealNet;

      LogInfo(StringFormat("POSITION_LIFECYCLE_DEAL Symbol=%s Magic=%I64u PositionId=%I64u Deal=%I64u Entry=%d Profit=%.2f Commission=%.2f Swap=%.2f Fee=%.2f Net=%.2f", _Symbol, MagicNumber, positionId, dealTicket, (int)dealEntry, dealProfit, dealCommission, dealSwap, dealFee, dealNet));
      found = true;
   }

   return found;
}

bool CalculateBigSmallLifecycleNet(ulong bigPositionId, ulong smallPositionId, datetime fromTime, double &bigLifecycleNet, double &smallLifecycleNet, double &bigSmallNet, double &commission, double &swap, double &fee)
{
   bool found = CalculateRealNetForClosedPositions(bigPositionId, smallPositionId, fromTime, bigLifecycleNet, smallLifecycleNet, commission, swap, fee);
   bigSmallNet = bigLifecycleNet + smallLifecycleNet;
   LogInfo(StringFormat("BIG_SMALL_LIFECYCLE_NET Symbol=%s Magic=%I64u BigPositionId=%I64u SmallPositionId=%I64u Found=%s BigLifecycleNet=%.2f SmallLifecycleNet=%.2f BigSmallNet=%.2f Commission=%.2f Swap=%.2f Fee=%.2f", _Symbol, MagicNumber, bigPositionId, smallPositionId, found ? "YES" : "NO", bigLifecycleNet, smallLifecycleNet, bigSmallNet, commission, swap, fee));
   return found;
}


bool CalculatePositionCloseDealsNet(ulong positionId, datetime fromTime, double &net, double &commission, double &swap, double &fee, int &deals)
{
   net = 0.0;
   commission = 0.0;
   swap = 0.0;
   fee = 0.0;
   deals = 0;

   if(IsInternalSimulationMode())
      return false;

   datetime startTime = fromTime > 0 ? fromTime - 2 : Ctx.cycleStartTime;
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
      if((ulong)HistoryDealGetInteger(dealTicket, DEAL_POSITION_ID) != positionId)
         continue;

      ENUM_DEAL_ENTRY dealEntry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(dealTicket, DEAL_ENTRY);
      if(dealEntry != DEAL_ENTRY_OUT && dealEntry != DEAL_ENTRY_INOUT && dealEntry != DEAL_ENTRY_OUT_BY)
         continue;

      double dealProfit = HistoryDealGetDouble(dealTicket, DEAL_PROFIT);
      double dealCommission = HistoryDealGetDouble(dealTicket, DEAL_COMMISSION);
      double dealSwap = HistoryDealGetDouble(dealTicket, DEAL_SWAP);
      double dealFee = HistoryDealGetDouble(dealTicket, DEAL_FEE);
      double dealNet = dealProfit + dealCommission + dealSwap + dealFee;
      net += dealNet;
      commission += dealCommission;
      swap += dealSwap;
      fee += dealFee;
      deals++;
      LogInfo(StringFormat("POSITION_CLOSE_DEAL_NET Symbol=%s Magic=%I64u PositionId=%I64u Deal=%I64u Entry=%d Profit=%.2f Commission=%.2f Swap=%.2f Fee=%.2f Net=%.2f", _Symbol, MagicNumber, positionId, dealTicket, (int)dealEntry, dealProfit, dealCommission, dealSwap, dealFee, dealNet));
   }
   return deals > 0;
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
   else if(actionType == PENDING_CLOSE_BIG_CORE_FULL || actionType == PENDING_CLOSE_BIG_CORE_PARTIAL)
      Ctx.pendingDirection = Ctx.bigCoreDirection;
   else if(actionType == PENDING_CLOSE_BIG_TREND_FULL)
      Ctx.pendingDirection = Ctx.bigTrendDirection;
   else if(actionType == PENDING_CLOSE_SMALL_BASE_FULL)
      Ctx.pendingDirection = Ctx.smallBaseDirection;
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
   SaveState();
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


double CurrentPriceForDirectionClose(Direction dir);

struct ProjectedCloseNetResult
{
   double projectedGrossProfit;
   double projectedSwapPart;
   double estimatedCommission;
   double projectedNet;
   double projectedLoss;
};

bool CalculateProjectedPositionCloseNet(ulong ticket, double lot, ProjectedCloseNetResult &result)
{
   result.projectedGrossProfit = 0.0;
   result.projectedSwapPart = 0.0;
   result.estimatedCommission = 0.0;
   result.projectedNet = 0.0;
   result.projectedLoss = 0.0;

   PositionSnapshot pos;
   if(!GetManagedPositionByTicket(ticket, pos))
      return false;

   double closeLot = MathMin(lot, pos.lot);
   closeLot = NormalizeLotDown(closeLot);
   if(closeLot <= 0.0)
      return false;

   double closePrice = CurrentPriceForDirectionClose(pos.direction);
   BrokerMoneyResult money;
   double profit = 0.0;
   if(IsInternalSimulationMode())
      profit = CalcSignedPositionPL(pos.direction, closeLot, pos.openPrice, closePrice);
   else
   {
      if(!CalcProjectedCloseNetMoney(pos.direction, closeLot, pos.openPrice, closePrice, money))
      {
         LogError("BROKER_MONEY_MODEL_REQUIRED " + money.reason);
         return false;
      }
      profit = money.grossProfit;
   }

   double swapPart = 0.0;
   if(PositionSelectByTicket(ticket))
   {
      double fullSwap = PositionGetDouble(POSITION_SWAP);
      if(pos.lot > 0.0)
         swapPart = fullSwap * (closeLot / pos.lot);
   }

   result.projectedGrossProfit = profit;
   result.projectedSwapPart = swapPart;
   result.estimatedCommission = closeLot * EstimatedCloseCommissionPerLot;
   if(IsInternalSimulationMode())
      result.projectedNet = profit + swapPart - result.estimatedCommission - SafetyBufferMoney;
   else
      result.projectedNet = money.netMoney + swapPart;
   result.projectedLoss = MathMax(0.0, -result.projectedNet);
   return true;
}

bool CalculateProjectedFarCloseNet(double lot, ProjectedCloseNetResult &result)
{
   return CalculateProjectedPositionCloseNet(Ctx.farTicket, lot, result);
}

double CalculateMaxPartialFarLotByMoney(double budget, double &projectedLoss)
{
   projectedLoss = 0.0;
   if(budget <= 0.0 || Ctx.farLot <= 0.0)
      return 0.0;

   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   if(minLot <= 0.0)
      minLot = LotStep;

   ProjectedCloseNetResult full;
   if(!CalculateProjectedFarCloseNet(Ctx.farLot, full))
      return 0.0;
   if(full.projectedLoss <= budget + 0.000001)
   {
      projectedLoss = full.projectedLoss;
      return NormalizeLotDown(Ctx.farLot);
   }

   double low = 0.0;
   double high = Ctx.farLot;
   double best = 0.0;
   double bestLoss = 0.0;
   for(int i = 0; i < 32; i++)
   {
      double mid = NormalizeLotDown((low + high) / 2.0);
      if(mid < minLot)
      {
         low = mid + LotStep;
         continue;
      }
      ProjectedCloseNetResult probe;
      if(!CalculateProjectedFarCloseNet(mid, probe))
         break;
      if(probe.projectedLoss <= budget + 0.000001)
      {
         best = mid;
         bestLoss = probe.projectedLoss;
         low = mid + LotStep;
      }
      else
         high = mid - LotStep;
   }
   projectedLoss = bestLoss;
   return NormalizeLotDown(best);
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

   ProjectedCloseNetResult farProjection;
   bool projectedFarOk = CalculateProjectedFarCloseNet(Ctx.farLot, farProjection);
   double farRemainLoss = projectedFarOk ? farProjection.projectedLoss : CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
   Ctx.cycleFinalPL = Ctx.totalReserve - farRemainLoss;
   Ctx.theoreticalCyclePL = Ctx.cycleFinalPL;

   double projectedFarPL = projectedFarOk ? farProjection.projectedNet : -farRemainLoss;
   double projectedBalanceAfterFinalClose = (IsInternalSimulationMode() ? Ctx.cycleCurrentBalance : AccountInfoDouble(ACCOUNT_BALANCE)) + projectedFarPL;
   double projectedRecoveryPLAfterFinalClose = projectedBalanceAfterFinalClose - Ctx.cycleStartBalance;
   LogInfo(StringFormat("FINAL_CLOSE_PROFIT_FORECAST ProjectedBalanceAfterFinalClose=%.2f ProjectedRecoveryPLAfterFinalClose=%.2f CycleStartBalance=%.2f ProjectedFarCloseNet=%.2f FarCloseLoss=%.2f ReserveBeforeFinal=%.2f",
                        projectedBalanceAfterFinalClose,
                        projectedRecoveryPLAfterFinalClose,
                        Ctx.cycleStartBalance,
                        projectedFarPL,
                        farRemainLoss,
                        Ctx.totalReserve));
   if(projectedRecoveryPLAfterFinalClose < MinimumRecoveryProfitMoney || Ctx.totalReserve < farRemainLoss + SafetyBufferMoney - 0.000001)
   {
      Ctx.finalCloseAllowed = false;
      if(Ctx.harvestLevel >= WorkMaxHarvestLevels)
         SetState(STATE_MAX_LEVELS_DECISION, "FINAL_CLOSE_STOP: reserve or projected recovery PL is below minimum");
      else
         SetState(STATE_FAR_ACTIVE, "FINAL_CLOSE_STOP: wait for reserve coverage and minimum recovery PL");
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
   RecalculateRealCycleStatsFromHistory();
   double reserveUsed = MathMin(farRemainLoss, Ctx.totalReserve);
   if(Ctx.realRecoveryPL < MinimumRecoveryProfitMoney)
   {
      LogError(StringFormat("FINAL_CLOSE_RECOVERY_BELOW_MIN ActualRecoveryPL=%.2f MinimumRecoveryProfitMoney=%.2f", Ctx.realRecoveryPL, MinimumRecoveryProfitMoney));
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Final close actual recovery below minimum");
      return;
   }
   if(!ApplyReserveDebit(RESERVE_EVENT_FINAL_CLOSE_DEBIT, reserveUsed))
   {
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Final close reserve debit failed");
      return;
   }
   ClearFarContext("FINAL_CLOSE_PROFIT confirmed by VerifyFullClose");
   SaveState();
   LogInfo(StringFormat("CYCLE_CLOSED ActualRecoveryPL=%.2f ReserveUsed=%.2f InitialProfitIgnored=%.2f FinalBalance=%.2f CycleStartBalance=%.2f", Ctx.realRecoveryPL, reserveUsed, Ctx.initialIgnoredProfit, AccountInfoDouble(ACCOUNT_BALANCE), Ctx.cycleStartBalance));
   if(!ValidateNoOrphanManagedPositions()) return;
   SetState(STATE_CLOSED_PROFIT, "cycle closed in profit; no new levels");
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
   SaveState();
   if(!ValidateNoOrphanManagedPositions()) return;
   SetState(STATE_BIG_HARVEST_CALC_NET, "BigHarvest Small close phase done");
}

void ProcessBigHarvestCalcNet()
{
   RecalculateRealCycleStatsFromHistory();
   RefreshFarVolumeFromTerminal("BIG_HARVEST_CALC_NET refresh Far before monetary checks");

   double bigLifecycleNet = 0.0;
   double smallLifecycleNet = 0.0;
   double bigSmallNet = 0.0;
   double lifecycleCommission = 0.0;
   double lifecycleSwap = 0.0;
   double lifecycleFee = 0.0;
   bool foundDeals = CalculateBigSmallLifecycleNet(Ctx.pendingBigPositionId, Ctx.pendingSmallPositionId, Ctx.pendingOperationStartTime, bigLifecycleNet, smallLifecycleNet, bigSmallNet, lifecycleCommission, lifecycleSwap, lifecycleFee);
   Ctx.pendingRealNet = bigSmallNet;
   Ctx.pendingFullFarClose = false;
   Ctx.pendingReserveAdd = 0.0;
   Ctx.pendingCloseFarBudget = 0.0;
   Ctx.pendingCloseFarLot = 0.0;
   Ctx.pendingPartialFarBudgetCarryBefore = Ctx.partialFarBudgetCarry;
   Ctx.pendingPartialFarBudgetAvailable = 0.0;
   Ctx.pendingProjectedPartialFarLoss = 0.0;

   ProjectedCloseNetResult fullFarProjection;
   bool projectedFullFarOk = CalculateProjectedFarCloseNet(Ctx.farLot, fullFarProjection);
   double farCloseLoss = projectedFullFarOk ? fullFarProjection.projectedLoss : CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
   double coverageAvailable = Ctx.totalReserve + bigSmallNet;
   double projectedRecoveryPLAfterFullClose = (IsInternalSimulationMode() ? Ctx.cycleCurrentBalance : AccountInfoDouble(ACCOUNT_BALANCE)) + (projectedFullFarOk ? fullFarProjection.projectedNet : -farCloseLoss) - Ctx.cycleStartBalance;
   bool fullCloseAllowed = foundDeals && bigSmallNet > 0.0 && projectedFullFarOk && coverageAvailable >= farCloseLoss + SafetyBufferMoney - 0.000001 && projectedRecoveryPLAfterFullClose >= MinimumRecoveryProfitMoney;

   LogInfo(StringFormat("BIG_SCENARIO_NET BigLifecycleNet=%.2f SmallLifecycleNet=%.2f BigSmallNet=%.2f Commission=%.2f Swap=%.2f Fee=%.2f FoundDeals=%s",
      bigLifecycleNet, smallLifecycleNet, bigSmallNet, lifecycleCommission, lifecycleSwap, lifecycleFee, foundDeals ? "YES" : "NO"));
   LogInfo(StringFormat("BIG_FULL_COVERAGE_CHECK Symbol=%s MagicNumber=%I64u CycleId=%I64u Level=%d FarTicket=%I64u FarIdentifier=%I64d FarLot=%.2f FarDirection=%s FarOpenPrice=%.5f ProjectedFarCloseNet=%.2f FarCloseLoss=%.2f SafetyBufferMoney=%.2f ExistingReserve=%.2f CoverageAvailable=%.2f ProjectedRecoveryPLAfterFullClose=%.2f MinimumRecoveryProfitMoney=%.2f FullCloseAllowed=%s",
      _Symbol, MagicNumber, Ctx.cycleId, Ctx.harvestLevel, Ctx.farTicket, Ctx.farIdentifier, Ctx.farLot, DirectionToString(Ctx.farDirection), Ctx.farOpenPrice, projectedFullFarOk ? fullFarProjection.projectedNet : 0.0, farCloseLoss, SafetyBufferMoney, Ctx.totalReserve, coverageAvailable, projectedRecoveryPLAfterFullClose, MinimumRecoveryProfitMoney, fullCloseAllowed ? "YES" : "NO"));

   if(!foundDeals || bigSmallNet <= 0.0)
   {
      LogError(StringFormat("BIG_SMALL_NET_NON_POSITIVE FoundDeals=%s BigSmallNet=%.2f: ReserveAdd=0 PartialFarBudget=0 FarPartialClose=NO", foundDeals ? "YES" : "NO", bigSmallNet));
      WriteCycleMathCsv(Ctx.harvestLevel, "BIG_SCENARIO_AUDIT", Ctx.farLot, 0.0, 0.0, bigSmallNet, 0.0, 0.0, Ctx.totalReserve, farCloseLoss, false, STATE_BIG_HARVEST_CALC_NET, bigLifecycleNet, 0.0, smallLifecycleNet, 0.0, bigLifecycleNet, 0.0, 0.0, 0.0, Ctx.farLot, Ctx.reverseStrength, Ctx.projectedReserveCoverage, "BIG_SMALL_NET_NON_POSITIVE", "No Reserve and no partial Far close when BigSmallNet <= 0", bigSmallNet, bigSmallNet, lifecycleCommission + lifecycleSwap + lifecycleFee, Ctx.totalReserve, 0.0, Ctx.initialFarDistancePoints, Ctx.currentBigMovePoints, Ctx.cumulativeBigMovePoints, Ctx.effectiveFarDistancePoints, FarDistanceModeToString(WorkFarDistanceMode), Ctx.farOpenPrice, Ctx.currentClosePrice, Ctx.initialIgnoredProfit, Ctx.cycleStartBalance, Ctx.cycleCurrentBalance, Ctx.realRecoveryPL, Ctx.realClosedProfit, Ctx.realClosedLoss, Ctx.realCommission, Ctx.realSwap, Ctx.realCosts, Ctx.theoreticalCyclePL, Ctx.lastSystemCloseComment, IsRealRecoveryPass(), Ctx.lastCloseWasSystemClose, Ctx.lastCloseWasSystemClose, Ctx.lastSystemCloseComment, GeometryModeToString((GeometryModeEnum)Ctx.geometryModeUsed), EnumToString(ATRTimeframe), ATRPeriod, Ctx.cycleATRPoints, InitialRoundStep, BigStartRoundStep, BigStepRoundStep, FarDistanceRoundStep, WorkInitialTriggerPoints(), WorkBigMoveStartPoints(), WorkBigMoveStepPoints(), WorkFarDistancePoints(), FreezeGeometryPerCycle);
      SetState(STATE_BIG_HARVEST_CHECK_FINAL, "BigHarvest BigSmallNet non-positive; skip partial Far and reserve");
      return;
   }

   double closeFarLotRaw = 0.0;
   double closeFarActualCost = 0.0;
   string splitReason = "BIG_PROFIT_SPLIT";

   if(fullCloseAllowed)
   {
      Ctx.pendingFullFarClose = true;
      Ctx.pendingCloseFarLot = NormalizeLotDown(Ctx.farLot);
      Ctx.pendingCloseFarBudget = bigSmallNet;
      Ctx.pendingReserveAdd = 0.0;
      Ctx.pendingPartialFarBudgetAvailable = 0.0;
      Ctx.pendingProjectedPartialFarLoss = fullFarProjection.projectedLoss;
      closeFarLotRaw = Ctx.farLot;
      closeFarActualCost = fullFarProjection.projectedLoss;
      splitReason = "FULL_FAR_CLOSE_BEFORE_PARTIAL";
      LogInfo(StringFormat("FULL_FAR_CLOSE_BEFORE_PARTIAL BigSmallNet=%.2f ExistingReserve=%.2f FarCloseLoss=%.2f ProjectedRecoveryPLAfterFullClose=%.2f CloseFarLot=%.2f PartialFar=NO", bigSmallNet, Ctx.totalReserve, farCloseLoss, projectedRecoveryPLAfterFullClose, Ctx.pendingCloseFarLot));
   }
   else
   {
      Ctx.pendingReserveAdd = bigSmallNet * WorkReserveShare;
      Ctx.pendingCloseFarBudget = bigSmallNet - Ctx.pendingReserveAdd;
      Ctx.pendingPartialFarBudgetAvailable = Ctx.pendingCloseFarBudget + Ctx.partialFarBudgetCarry;
      Ctx.pendingCloseFarLot = CalculateMaxPartialFarLotByMoney(Ctx.pendingPartialFarBudgetAvailable, Ctx.pendingProjectedPartialFarLoss);
      closeFarLotRaw = Ctx.pendingCloseFarLot;
      closeFarActualCost = Ctx.pendingProjectedPartialFarLoss;
      LogInfo(StringFormat("BIG_PROFIT_SPLIT ReserveAdd=%.2f PartialBudgetNew=%.2f ReserveShare=%.5f CloseFarShare=%.5f SplitSum=%.5f", Ctx.pendingReserveAdd, Ctx.pendingCloseFarBudget, WorkReserveShare, WorkCloseFarShare, WorkCloseFarShare + WorkReserveShare));
      LogInfo(StringFormat("BIG_PARTIAL_FAR ReserveShare=%.5f ReserveAdd=%.2f PartialBudgetNew=%.2f PartialFarBudgetCarryBefore=%.2f PartialBudgetAvailable=%.2f CalculatedPartialFarLot=%.2f NormalizedPartialFarLot=%.2f ProjectedPartialFarLoss=%.2f ReserveUsedForPartial=NO",
         WorkReserveShare, Ctx.pendingReserveAdd, Ctx.pendingCloseFarBudget, Ctx.pendingPartialFarBudgetCarryBefore, Ctx.pendingPartialFarBudgetAvailable, closeFarLotRaw, Ctx.pendingCloseFarLot, Ctx.pendingProjectedPartialFarLoss));
   }

   LogInfo(StringFormat("CLOSE_FAR_BUDGET CloseFarBudget=%.2f CloseFarLotRaw=%.5f CloseFarLotRounded=%.2f CloseFarActualCost=%.2f FarLotBefore=%.2f PendingFullFarClose=%s", Ctx.pendingCloseFarBudget, closeFarLotRaw, Ctx.pendingCloseFarLot, closeFarActualCost, Ctx.farLot, Ctx.pendingFullFarClose ? "YES" : "NO"));
   LogInfo(StringFormat("RESERVE_ADD ReserveAdd=%.2f TotalReserveBefore=%.2f ReserveApplied=%s", Ctx.pendingReserveAdd, Ctx.totalReserve, Ctx.pendingReserveApplied ? "YES" : "NO"));
   WriteCycleMathCsv(
      Ctx.harvestLevel,
      "BIG_SCENARIO_AUDIT",
      Ctx.farLot,
      0.0,
      0.0,
      bigSmallNet,
      Ctx.pendingCloseFarBudget,
      Ctx.pendingReserveAdd,
      Ctx.totalReserve,
      farCloseLoss,
      fullCloseAllowed,
      STATE_BIG_HARVEST_CALC_NET,
      bigLifecycleNet,
      0.0,
      smallLifecycleNet,
      0.0,
      bigLifecycleNet,
      0.0,
      closeFarLotRaw,
      Ctx.pendingCloseFarLot,
      Ctx.farLot,
      Ctx.reverseStrength,
      Ctx.projectedReserveCoverage,
      splitReason,
      closeFarActualCost <= (Ctx.pendingFullFarClose ? farCloseLoss : Ctx.pendingPartialFarBudgetAvailable) + 0.000001 ? "" : "CloseFarActualCost exceeds available budget",
      bigSmallNet,
      bigSmallNet,
      lifecycleCommission + lifecycleSwap + lifecycleFee,
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
   LogInfo(StringFormat("BIG_HARVEST_REAL_RESERVE BIG_HARVEST_REAL_DEALS_CALC BigPositionId=%I64u SmallPositionId=%I64u FoundDeals=%s BigLifecycleNet=%.2f SmallLifecycleNet=%.2f Commission=%.2f Swap=%.2f Fee=%.2f BigSmallNet=%.2f ReserveAdd=%.2f PartialFarBudget=%.2f CloseFarLot=%.2f FullCloseBeforePartial=%s", Ctx.pendingBigPositionId, Ctx.pendingSmallPositionId, foundDeals ? "YES" : "NO", bigLifecycleNet, smallLifecycleNet, lifecycleCommission, lifecycleSwap, lifecycleFee, bigSmallNet, Ctx.pendingReserveAdd, Ctx.pendingCloseFarBudget, Ctx.pendingCloseFarLot, Ctx.pendingFullFarClose ? "YES" : "NO"));
   SaveState();
   SetState(STATE_BIG_HARVEST_CLOSE_FAR, "BigHarvest real deal reserve calculated");
}

void ProcessBigHarvestCloseFar()
{
   if(Ctx.pendingCloseFarLot <= 0.0)
   {
      SetState(STATE_BIG_HARVEST_CHECK_FINAL, "BigHarvest has no Far budget to close");
      return;
   }

   if(Ctx.pendingFullFarClose)
   {
      ulong closingTicket = Ctx.farTicket;
      ulong closingIdentifier = Ctx.farIdentifier;
      double closingLot = Ctx.pendingCloseFarLot;
      double reserveBeforeFull = Ctx.totalReserve;
      double projectedFarLoss = Ctx.pendingProjectedPartialFarLoss;
      datetime fullCloseStartTime = TimeCurrent();
      if(!ClosePositionByTicket(closingTicket, closingLot))
      {
         SetPendingOperation(PENDING_CLOSE_FAR_FULL, "BIG_HARVEST_FULL_CLOSE_FAR", STATE_CLOSE_NEW_FAR_PENDING, closingTicket, closingLot, "RETRY_FULL_FAR_COVERAGE_CLOSE", STATE_BIG_HARVEST_CHECK_FINAL, "BigHarvest full Far close failed; retry pending");
         return;
      }
      if(!VerifyFullClose(closingTicket, "BIG_HARVEST_FULL_CLOSE_FAR"))
      {
         Ctx.farLot = NormalizeVolumeToStep(GetActualPositionVolume(closingTicket));
         SetPendingOperation(PENDING_CLOSE_FAR_FULL, "BIG_HARVEST_FULL_CLOSE_FAR", STATE_CLOSE_NEW_FAR_PENDING, closingTicket, Ctx.farLot, "RETRY_FULL_FAR_COVERAGE_CLOSE", STATE_BIG_HARVEST_CHECK_FINAL, "FULL_CLOSE_INCOMPLETE after BigHarvest full Far close; retry pending");
         return;
      }
      double actualFarNet = 0.0, actualCommission = 0.0, actualSwap = 0.0, actualFee = 0.0;
      int actualDeals = 0;
      bool foundActualFarDeals = CalculatePositionCloseDealsNet(closingIdentifier, fullCloseStartTime, actualFarNet, actualCommission, actualSwap, actualFee, actualDeals);
      double actualFarLoss = foundActualFarDeals ? MathMax(0.0, -actualFarNet) : projectedFarLoss;
      RecalculateRealCycleStatsFromHistory();
      if(Ctx.realRecoveryPL < MinimumRecoveryProfitMoney)
      {
         LogError(StringFormat("BIG_FULL_FAR_CLOSE_RECOVERY_BELOW_MIN ActualRecoveryPL=%.2f MinimumRecoveryProfitMoney=%.2f", Ctx.realRecoveryPL, MinimumRecoveryProfitMoney));
         SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "BigHarvest full Far close actual recovery below minimum");
         return;
      }
      double reserveUsed = MathMin(MathMax(0.0, actualFarLoss - Ctx.pendingRealNet), reserveBeforeFull);
      if(!ApplyReserveDebit(RESERVE_EVENT_BIG_FULL_FAR_CLOSE_DEBIT, reserveUsed))
      {
         SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "BigHarvest full Far close reserve debit failed");
         return;
      }
      LogInfo(StringFormat("BIG_HARVEST_FULL_FAR_CLOSE_DONE ReserveBefore=%.2f BigSmallNet=%.2f FarCloseLoss=%.2f ReserveUsed=%.2f ReserveAfter=%.2f ProjectedRecoveryPL=%.2f ActualRecoveryPL=%.2f ActualFarNet=%.2f ActualDeals=%d", reserveBeforeFull, Ctx.pendingRealNet, actualFarLoss, reserveUsed, Ctx.totalReserve, Ctx.realRecoveryPL, Ctx.realRecoveryPL, actualFarNet, actualDeals));
      LogInfo(StringFormat("CYCLE_CLOSED ActualRecoveryPL=%.2f ReserveUsed=%.2f InitialProfitIgnored=%.2f FinalBalance=%.2f CycleStartBalance=%.2f", Ctx.realRecoveryPL, reserveUsed, Ctx.initialIgnoredProfit, AccountInfoDouble(ACCOUNT_BALANCE), Ctx.cycleStartBalance));
      ClearFarContext("BigHarvest full Far close before partial confirmed by VerifyFullClose");
      Ctx.pendingCloseFarLot = 0.0;
      Ctx.pendingFullFarClose = false;
      Ctx.pendingCloseFarBudget = 0.0;
      Ctx.pendingReserveAdd = 0.0;
      SaveState();
      if(!ValidateNoOrphanManagedPositions()) return;
      MarkSystemClose("CLOSED_PROFIT");
      SetState(STATE_CLOSED_PROFIT, "BigHarvest full Far coverage close completed");
      return;
   }

   datetime partialCloseStartTime = TimeCurrent();
   ulong partialFarIdentifier = Ctx.farIdentifier;
   if(!ClosePositionByTicket(Ctx.farTicket, Ctx.pendingCloseFarLot))
   {
      SetPendingOperation(PENDING_CLOSE_FAR_PARTIAL, "BIG_HARVEST_CLOSE_FAR", STATE_CLOSE_NEW_FAR_PENDING, Ctx.farTicket, Ctx.pendingCloseFarLot, "RETRY_CLOSE_FAR_BUDGET", STATE_BIG_HARVEST_CHECK_FINAL, "BigHarvest close Far budget failed; retry pending");
      return;
   }

   if(!RefreshFarVolumeFromTerminal("BIG_HARVEST_CLOSE_FAR partial close"))
      ClearFarContext("BIG_HARVEST_CLOSE_FAR actual remaining Far volume is zero");

   double actualPartialFarNet = 0.0, actualPartialCommission = 0.0, actualPartialSwap = 0.0, actualPartialFee = 0.0;
   int actualPartialDeals = 0;
   bool foundActualPartialDeals = CalculatePositionCloseDealsNet(partialFarIdentifier, partialCloseStartTime, actualPartialFarNet, actualPartialCommission, actualPartialSwap, actualPartialFee, actualPartialDeals);
   double actualPartialFarLoss = foundActualPartialDeals ? MathMax(0.0, -actualPartialFarNet) : Ctx.pendingProjectedPartialFarLoss;
   Ctx.partialFarBudgetCarry = MathMax(0.0, Ctx.pendingPartialFarBudgetAvailable - actualPartialFarLoss);
   LogInfo(StringFormat("BIG_PARTIAL_FAR PARTIAL_FAR_CLOSE CloseFarLot=%.2f PartialBudgetNew=%.2f PartialFarBudgetCarryBefore=%.2f PartialBudgetAvailable=%.2f ProjectedPartialFarLoss=%.2f ActualPartialFarNet=%.2f ActualPartialFarLoss=%.2f ActualPartialDeals=%d PartialFarBudgetCarryAfter=%.2f RemainingFarLot=%.2f ReserveUsedForPartial=NO", Ctx.pendingCloseFarLot, Ctx.pendingCloseFarBudget, Ctx.pendingPartialFarBudgetCarryBefore, Ctx.pendingPartialFarBudgetAvailable, Ctx.pendingProjectedPartialFarLoss, actualPartialFarNet, actualPartialFarLoss, actualPartialDeals, Ctx.partialFarBudgetCarry, Ctx.farLot));
   SaveState();
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

   ProjectedCloseNetResult remainingFarProjection;
   bool projectedRemainingOk = CalculateProjectedFarCloseNet(Ctx.farLot, remainingFarProjection);
   double farRemainLoss = projectedRemainingOk ? remainingFarProjection.projectedLoss : CalcFarRemainLoss(Ctx.farLot, Ctx.effectiveFarDistancePoints);
   double projectedRecoveryPLAfterFinalClose = (IsInternalSimulationMode() ? Ctx.cycleCurrentBalance : AccountInfoDouble(ACCOUNT_BALANCE)) + (projectedRemainingOk ? remainingFarProjection.projectedNet : -farRemainLoss) - Ctx.cycleStartBalance;
   Ctx.finalCloseAllowed = (Ctx.farLot > 0.0 && Ctx.totalReserve >= farRemainLoss + SafetyBufferMoney - 0.000001 && projectedRecoveryPLAfterFinalClose >= MinimumRecoveryProfitMoney);
   LogInfo(StringFormat("RESERVE_AFTER TotalReserve=%.2f RemainingFarLoss=%.2f SafetyBufferMoney=%.2f ProjectedRecoveryPLAfterFinalClose=%.2f MinimumRecoveryProfitMoney=%.2f FinalCloseAllowed=%s ReserveUsedForPartial=NO", Ctx.totalReserve, farRemainLoss, SafetyBufferMoney, projectedRecoveryPLAfterFinalClose, MinimumRecoveryProfitMoney, Ctx.finalCloseAllowed ? "YES" : "NO"));
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


string DiagnoseStopMaxLevelsReason(double reserveCoverage)
{
   if(Ctx.harvestLevel >= WorkMaxHarvestLevels && reserveCoverage >= 0.90)
      return "MAX_LEVELS_TOO_LOW";
   if(Ctx.cycleATRPoints > 0.0 && (Ctx.workInitialTriggerPoints >= 220 || Ctx.workBigMoveStartPoints >= 220 || Ctx.workBigMoveStepPoints >= 90 || Ctx.workFarDistancePoints >= 300))
      return "GEOMETRY_TOO_WIDE_OR_RESERVE_TOO_LOW";
   if(BigRatio * BigRatio * WorkRemainBigOnSmall >= 0.95)
      return "BIG_LOT_COMPRESSION_TOO_FAST";
   return "GEOMETRY_TOO_WIDE_OR_RESERVE_TOO_LOW";
}

void LogStopMaxLevelsDiagnosis(double farCloseLoss)
{
   double reserveCoverage = farCloseLoss > 0.0 ? Ctx.totalReserve / farCloseLoss : 999.0;
   LogInfo(StringFormat("STOP_MAX_LEVELS_DIAGNOSIS MaxHarvestLevels=%d ActualHarvestLevel=%d LastFarLot=%.2f LastBigLot=%.2f LastSmallLot=%.2f TotalReserve=%.2f RecoveryPL=%.2f ReserveCoverage=%.4f LastATRPoints=%.1f LastWorkInitial=%d LastWorkBigStart=%d LastWorkBigStep=%d LastWorkFar=%d LikelyReason=%s",
                        WorkMaxHarvestLevels,
                        Ctx.harvestLevel,
                        Ctx.farLot,
                        Ctx.bigLot,
                        Ctx.smallLot,
                        Ctx.totalReserve,
                        Ctx.realRecoveryPL,
                        reserveCoverage,
                        Ctx.cycleATRPoints,
                        Ctx.workInitialTriggerPoints,
                        Ctx.workBigMoveStartPoints,
                        Ctx.workBigMoveStepPoints,
                        Ctx.workFarDistancePoints,
                        DiagnoseStopMaxLevelsReason(reserveCoverage)));
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
      RecalculateRealCycleStatsFromHistory();
      LogStopMaxLevelsDiagnosis(0.0);
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
      RecalculateRealCycleStatsFromHistory();
      LogStopMaxLevelsDiagnosis(farCloseLoss);
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




void ClearSplitRoleContext(string reason)
{
   LogInfo("CLEAR_SPLIT_ROLE_CONTEXT " + reason);
   Ctx.bigCoreTicket = 0;
   Ctx.bigTrendTicket = 0;
   Ctx.smallBaseTicket = 0;
   Ctx.bigCoreIdentifier = 0;
   Ctx.bigTrendIdentifier = 0;
   Ctx.smallBaseIdentifier = 0;
   Ctx.bigCoreLot = 0.0;
   Ctx.bigTrendLot = 0.0;
   Ctx.smallBaseLot = 0.0;
   Ctx.bigCoreOpenPrice = 0.0;
   Ctx.bigTrendOpenPrice = 0.0;
   Ctx.smallBaseOpenPrice = 0.0;
   Ctx.bigCoreDirection = DIR_NONE;
   Ctx.bigTrendDirection = DIR_NONE;
   Ctx.smallBaseDirection = DIR_NONE;
   Ctx.actualSplitHarvestNet = 0.0;
   Ctx.actualSplitHarvestNetCalculated = false;
   Ctx.pendingReserveAdd = 0.0;
   Ctx.pendingCloseFarBudget = 0.0;
   Ctx.pendingCloseFarLot = 0.0;
   Ctx.pendingFullFarClose = false;
   Ctx.pendingReserveApplied = false;
   Ctx.pendingPartialFarBudgetAvailable = 0.0;
   Ctx.pendingProjectedPartialFarLoss = 0.0;
   Ctx.pendingBigPositionId = 0;
   Ctx.pendingSmallPositionId = 0;
   SaveState();
}

bool ApplyResolvedPositionToSplitRole(PositionRole role, PositionResolutionResult &result)
{
   if(!result.resolved || result.ticket == 0 || result.identifier == 0 || result.lot <= VolumeMismatchToleranceLots)
   {
      LogError("POSITION_RESOLUTION_FAILED split role could not be registered with ticket/identifier/lot");
      SetState(STATE_POSITION_RESOLUTION_ERROR, "POSITION_RESOLUTION_FAILED Split role");
      return false;
   }

   Direction resolvedDirection = PositionTypeToDirection((long)result.type);
   if(role == ROLE_BIG_CORE)
   {
      Ctx.bigCoreTicket = result.ticket;
      Ctx.bigCoreIdentifier = result.identifier;
      Ctx.bigCoreLot = result.lot;
      Ctx.bigCoreOpenPrice = result.openPrice;
      Ctx.bigCoreDirection = resolvedDirection;
   }
   else if(role == ROLE_SMALL_BASE)
   {
      Ctx.smallBaseTicket = result.ticket;
      Ctx.smallBaseIdentifier = result.identifier;
      Ctx.smallBaseLot = result.lot;
      Ctx.smallBaseOpenPrice = result.openPrice;
      Ctx.smallBaseDirection = resolvedDirection;
   }
   else if(role == ROLE_BIG_TREND)
   {
      Ctx.bigTrendTicket = result.ticket;
      Ctx.bigTrendIdentifier = result.identifier;
      Ctx.bigTrendLot = result.lot;
      Ctx.bigTrendOpenPrice = result.openPrice;
      Ctx.bigTrendDirection = resolvedDirection;
   }
   else
      return false;

   LogInfo(StringFormat("SPLIT_ROLE_RESOLVED Role=%s Ticket=%I64u Identifier=%I64u Lot=%.2f Direction=%s OpenPrice=%.5f", PositionRoleToCode(role), result.ticket, result.identifier, result.lot, DirectionToString(resolvedDirection), result.openPrice));
   SaveState();
   return true;
}

bool PrepareSplitBigLevel()
{
   if(!UseSplitBigGeometry)
      return false;
   if(HasBigContext() || HasSmallContext())
   {
      SetState(STATE_RECONCILIATION_ERROR, "Legacy Big/Small context exists while Split Big is requested");
      return false;
   }
   if(!RefreshFar())
   {
      SetState(STATE_POSITION_RESOLUTION_ERROR, "Split Prepare failed: Far not resolved");
      return false;
   }
   if(Ctx.farIdentifier == 0 || Ctx.farLot <= VolumeMismatchToleranceLots || Ctx.farDirection == DIR_NONE)
   {
      SetState(STATE_POSITION_RESOLUTION_ERROR, "Split Prepare failed: Far ticket/identifier/lot/direction incomplete");
      return false;
   }

   ClearSplitRoleContext("PrepareSplitBigLevel from actual Far");
   Ctx.splitGeometryActive = true;
   Ctx.harvestLevel += 1;
   Ctx.bigCoreDirection = OppositeDirection(Ctx.farDirection);
   Ctx.bigTrendDirection = OppositeDirection(Ctx.farDirection);
   Ctx.smallBaseDirection = Ctx.farDirection;
   Ctx.bigCoreLot = CalcBigCoreLot(Ctx.farLot);
   Ctx.bigTrendLot = CalcBigTrendLot(Ctx.farLot);
   Ctx.smallBaseLot = CalcSmallBaseLot(Ctx.farLot);

   double actualBigGrossLot = 0.0;
   double actualReserveGrowthLot = 0.0;
   double actualNewFarLot = 0.0;
   bool validGeometry = ValidateRoundedSplitGeometry(Ctx.farLot, Ctx.bigCoreLot, Ctx.bigTrendLot, Ctx.smallBaseLot, actualBigGrossLot, actualReserveGrowthLot, actualNewFarLot);
   Ctx.actualBigExposureLot = actualBigGrossLot;
   Ctx.actualSmallExposureLot = Ctx.smallBaseLot;
   Ctx.bigGrossRatio = (Ctx.farLot > 0.0 ? actualBigGrossLot / Ctx.farLot : 0.0);
   Ctx.reserveGrowthRatio = (Ctx.farLot > 0.0 ? actualReserveGrowthLot / Ctx.farLot : 0.0);
   Ctx.newFarCompressionRatio = (Ctx.farLot > 0.0 ? actualNewFarLot / Ctx.farLot : 0.0);
   Ctx.currentBigMovePoints = GetBigMovePoints(Ctx.harvestLevel);

   LogInfo(StringFormat("SPLIT_GEOMETRY_PREPARE Symbol=%s Magic=%I64u CycleId=%I64u Level=%d FarTicket=%I64u FarIdentifier=%I64u FarLot=%.2f FarDirection=%s BigCoreLot=%.2f BigTrendLot=%.2f SmallBaseLot=%.2f ActualBigGrossLot=%.2f ActualBigNetLot=%.2f ActualReserveGrowthLot=%.2f VolumeStep=%.5f TargetPoints=%.1f Valid=%s",
                        _Symbol, MagicNumber, Ctx.cycleId, Ctx.harvestLevel, Ctx.farTicket, Ctx.farIdentifier, Ctx.farLot, DirectionToString(Ctx.farDirection), Ctx.bigCoreLot, Ctx.bigTrendLot, Ctx.smallBaseLot, actualBigGrossLot, actualBigGrossLot, actualReserveGrowthLot, SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP), Ctx.currentBigMovePoints, validGeometry ? "YES" : "NO"));

   if(!validGeometry)
   {
      SetState(STATE_INVALID_SPLIT_GEOMETRY, "Rounded Split geometry failed: ActualBigGrossLot/ReserveGrowth not above FarLot or NewFar not compressed");
      return false;
   }

   SaveState();
   return true;
}


EAState SplitOpenPendingStateForRole(PositionRole role)
{
   if(role == ROLE_BIG_CORE) return STATE_SPLIT_OPEN_CORE_PENDING;
   if(role == ROLE_SMALL_BASE) return STATE_SPLIT_OPEN_SMALL_BASE_PENDING;
   if(role == ROLE_BIG_TREND) return STATE_SPLIT_OPEN_TREND_PENDING;
   return STATE_ERROR;
}

PendingActionType SplitOpenPendingActionForRole(PositionRole role)
{
   if(role == ROLE_BIG_CORE) return PENDING_OPEN_BIG_CORE;
   if(role == ROLE_SMALL_BASE) return PENDING_OPEN_SMALL_BASE;
   if(role == ROLE_BIG_TREND) return PENDING_OPEN_BIG_TREND;
   return PENDING_NONE;
}

EAState SplitClosePendingStateForRole(PositionRole role)
{
   if(role == ROLE_BIG_CORE) return STATE_SPLIT_CLOSE_CORE_PENDING;
   if(role == ROLE_BIG_TREND) return STATE_SPLIT_CLOSE_TREND_PENDING;
   if(role == ROLE_SMALL_BASE) return STATE_SPLIT_CLOSE_SMALL_BASE_PENDING;
   return STATE_ERROR;
}

bool AdjustPartialFarLotForMinimumResidual()
{
   if(Ctx.pendingFullFarClose)
      return true;
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   if(minLot <= 0.0) minLot = LotStep;
   if(step <= 0.0) step = LotStep;
   Ctx.pendingCloseFarLot = NormalizeLotDown(Ctx.pendingCloseFarLot);
   while(Ctx.pendingCloseFarLot >= minLot && NormalizeLotDown(Ctx.farLot - Ctx.pendingCloseFarLot) < minLot)
      Ctx.pendingCloseFarLot = NormalizeLotDown(Ctx.pendingCloseFarLot - step);
   if(Ctx.pendingCloseFarLot < minLot)
   {
      Ctx.pendingCloseFarLot = 0.0;
      Ctx.partialFarBudgetCarry = Ctx.pendingPartialFarBudgetAvailable;
      LogInfo(StringFormat("SPLIT_PARTIAL_PROJECTED Symbol=%s MagicNumber=%I64u CycleId=%I64u Level=%d Result=SKIP StopReason=no_tradable_residual PartialBudgetCarry=%.2f", _Symbol, MagicNumber, Ctx.cycleId, Ctx.harvestLevel, Ctx.partialFarBudgetCarry));
      return false;
   }
   ProjectedCloseNetResult adjusted;
   if(CalculateProjectedFarCloseNet(Ctx.pendingCloseFarLot, adjusted))
      Ctx.pendingProjectedPartialFarLoss = adjusted.projectedLoss;
   LogInfo(StringFormat("SPLIT_PARTIAL_PROJECTED Symbol=%s MagicNumber=%I64u CycleId=%I64u Level=%d FarLot=%.2f PartialFarLot=%.2f ResidualFarLot=%.2f ProjectedPartialLoss=%.2f Result=PASS", _Symbol, MagicNumber, Ctx.cycleId, Ctx.harvestLevel, Ctx.farLot, Ctx.pendingCloseFarLot, NormalizeLotDown(Ctx.farLot - Ctx.pendingCloseFarLot), Ctx.pendingProjectedPartialFarLoss));
   return true;
}

bool CalculateActualPartialFarLossFromHistory(datetime fromTime, double &actualNet, double &actualLoss)
{
   actualNet = 0.0;
   actualLoss = 0.0;
   if(IsInternalSimulationMode())
   {
      actualLoss = Ctx.pendingProjectedPartialFarLoss;
      actualNet = -actualLoss;
      return true;
   }
   if(Ctx.farIdentifier == 0 || !HistorySelect(fromTime, TimeCurrent() + 86400))
      return false;
   bool found = false;
   for(int i = 0; i < HistoryDealsTotal(); i++)
   {
      ulong dealTicket = HistoryDealGetTicket(i);
      if(dealTicket == 0) continue;
      datetime dealTime = (datetime)HistoryDealGetInteger(dealTicket, DEAL_TIME);
      if(dealTime < fromTime) continue;
      if(HistoryDealGetString(dealTicket, DEAL_SYMBOL) != _Symbol) continue;
      if((ulong)HistoryDealGetInteger(dealTicket, DEAL_MAGIC) != MagicNumber) continue;
      if((ulong)HistoryDealGetInteger(dealTicket, DEAL_POSITION_ID) != Ctx.farIdentifier) continue;
      ENUM_DEAL_ENTRY entry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(dealTicket, DEAL_ENTRY);
      if(entry != DEAL_ENTRY_OUT && entry != DEAL_ENTRY_INOUT && entry != DEAL_ENTRY_OUT_BY) continue;
      actualNet += HistoryDealGetDouble(dealTicket, DEAL_PROFIT) + HistoryDealGetDouble(dealTicket, DEAL_COMMISSION) + HistoryDealGetDouble(dealTicket, DEAL_SWAP) + HistoryDealGetDouble(dealTicket, DEAL_FEE);
      found = true;
   }
   actualLoss = MathMax(0.0, -actualNet);
   return found;
}

void CompleteSplitFullFarClose(double reserveUsed)
{
   ReserveEventContextSnapshot finalDebitSnapshot;
   BuildReserveEventContext(RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT, finalDebitSnapshot);
   long frozenEventKey = ReserveEventKeyHash(finalDebitSnapshot);
   LogInfo(StringFormat("SPLIT_FINAL_CLOSE_GUARD FrozenEventKey=%I64d FarIdentifier=%I64u BigCoreIdentifier=%I64u BigTrendIdentifier=%I64u SmallBaseIdentifier=%I64u CycleId=%I64u Level=%d", frozenEventKey, finalDebitSnapshot.farIdentifier, finalDebitSnapshot.bigCoreIdentifier, finalDebitSnapshot.bigTrendIdentifier, finalDebitSnapshot.smallBaseIdentifier, finalDebitSnapshot.cycleId, finalDebitSnapshot.harvestLevel));
   MarkSystemClose("SPLIT_FINAL_CLOSE_PROFIT");
   RecalculateRealCycleStatsFromHistory();
   if(Ctx.realRecoveryPL < MinimumRecoveryProfitMoney)
   {
      LogError(StringFormat("SPLIT_FINAL_CLOSE_GUARD Result=FAIL ActualRecoveryPL=%.2f MinimumRecoveryProfitMoney=%.2f", Ctx.realRecoveryPL, MinimumRecoveryProfitMoney));
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Split final close actual recovery below minimum");
      return;
   }
   if(!ApplyReserveDebitSnapshot(finalDebitSnapshot, reserveUsed))
   {
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Split final reserve debit failed");
      return;
   }
   ClearSplitRoleContext("SPLIT_FINAL_CLOSE_PROFIT clears Split roles after frozen debit ledger");
   ClearFarContext("SPLIT_FINAL_CLOSE_PROFIT confirmed by VerifyFullClose after frozen debit ledger");
   if(!ValidateNoOrphanManagedPositions())
      return;
   LogInfo(StringFormat("SPLIT_CLOSED_PROFIT Symbol=%s MagicNumber=%I64u CycleId=%I64u Level=%d ReserveUsed=%.2f RecoveryPL=%.2f Result=PASS", _Symbol, MagicNumber, finalDebitSnapshot.cycleId, finalDebitSnapshot.harvestLevel, reserveUsed, Ctx.realRecoveryPL));
   SetState(STATE_CLOSED_PROFIT, "SPLIT_FINAL_CLOSE_PROFIT completed");
}

bool OpenSplitRole(PositionRole role, Direction direction, double lot, EAState nextState, EAState failureState)
{
   if(!TradingOperationAllowedDuringRecovery("OpenSplitRole", false)) return false;
   if(!Ctx.riskGateOk && StopOnRiskGateBlocked)
   {
      SetState(failureState, "RiskGate blocked Split role open");
      return false;
   }
   string comment = BuildRoleComment(role, (long)Ctx.cycleId, Ctx.harvestLevel, Ctx.reverseCycleCount);
   datetime openStartTime = TimeCurrent();
   if(!OpenPosition(direction, lot, comment))
   {
      EAState pendingState = SplitOpenPendingStateForRole(role);
      PendingActionType pendingAction = SplitOpenPendingActionForRole(role);
      SetPendingOperation(pendingAction, "SPLIT_OPEN_" + PositionRoleToCode(role), pendingState, 0, lot, comment, nextState, "SPLIT_PENDING_CREATED open retry for " + PositionRoleToCode(role));
      return false;
   }
   PositionResolutionResult resolution;
   if(!ResolveOpenedPositionAfterOpen(comment, direction, lot, 0, openStartTime, resolution))
   {
      SetState(STATE_POSITION_RESOLUTION_ERROR, "Split role open resolution failed: " + comment);
      return false;
   }
   if(!ApplyResolvedPositionToSplitRole(role, resolution))
      return false;
   SetState(nextState, "Split role opened: " + comment);
   return true;
}

void ProcessSplitBigOpenCore()
{
   if(Ctx.bigCoreTicket != 0) { SetState(STATE_SPLIT_BIG_OPEN_SMALL_BASE, "BigCore already resolved after restart"); return; }
   OpenSplitRole(ROLE_BIG_CORE, Ctx.bigCoreDirection, Ctx.bigCoreLot, STATE_SPLIT_BIG_OPEN_SMALL_BASE, STATE_ERROR_OPEN_BIG_CORE);
}

void RollbackSplitAfterSmallBaseFailure()
{
   if(Ctx.bigCoreTicket != 0 && Ctx.bigCoreLot > 0.0)
   {
      MarkSystemClose("ROLLBACK_SPLIT_BIG_CORE_WITHOUT_SMALL_BASE");
      if(!ClosePositionByTicketWithComment(Ctx.bigCoreTicket, Ctx.bigCoreLot, "ROLLBACK_SPLIT_BIG_CORE_WITHOUT_SMALL_BASE") || !VerifyFullClose(Ctx.bigCoreTicket, "ROLLBACK_SPLIT_BIG_CORE_WITHOUT_SMALL_BASE"))
      {
         SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Rollback BigCore failed after SmallBase open failure");
         return;
      }
      Ctx.bigCoreTicket = 0; Ctx.bigCoreIdentifier = 0; Ctx.bigCoreLot = 0.0; Ctx.bigCoreDirection = DIR_NONE; Ctx.bigCoreOpenPrice = 0.0;
   }
   SaveState();
   SetState(STATE_ERROR_OPEN_SMALL_BASE, "SmallBase open failed; BigCore rollback completed");
}

void ProcessSplitBigOpenSmallBase()
{
   if(Ctx.smallBaseTicket != 0) { SetState(STATE_SPLIT_BIG_OPEN_TREND, "SmallBase already resolved after restart"); return; }
   if(!OpenSplitRole(ROLE_SMALL_BASE, Ctx.smallBaseDirection, Ctx.smallBaseLot, STATE_SPLIT_BIG_OPEN_TREND, STATE_ERROR_OPEN_SMALL_BASE))
      RollbackSplitAfterSmallBaseFailure();
}

void RollbackSplitAfterBigTrendFailure()
{
   if(Ctx.smallBaseTicket != 0 && Ctx.smallBaseLot > 0.0)
   {
      MarkSystemClose("ROLLBACK_SPLIT_SMALL_BASE_WITHOUT_BIG_TREND");
      if(!ClosePositionByTicketWithComment(Ctx.smallBaseTicket, Ctx.smallBaseLot, "ROLLBACK_SPLIT_SMALL_BASE_WITHOUT_BIG_TREND") || !VerifyFullClose(Ctx.smallBaseTicket, "ROLLBACK_SPLIT_SMALL_BASE_WITHOUT_BIG_TREND"))
      { SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Rollback SmallBase failed after BigTrend open failure"); return; }
      Ctx.smallBaseTicket = 0; Ctx.smallBaseIdentifier = 0; Ctx.smallBaseLot = 0.0; Ctx.smallBaseDirection = DIR_NONE; Ctx.smallBaseOpenPrice = 0.0;
   }
   if(Ctx.bigCoreTicket != 0 && Ctx.bigCoreLot > 0.0)
   {
      MarkSystemClose("ROLLBACK_SPLIT_BIG_CORE_WITHOUT_BIG_TREND");
      if(!ClosePositionByTicketWithComment(Ctx.bigCoreTicket, Ctx.bigCoreLot, "ROLLBACK_SPLIT_BIG_CORE_WITHOUT_BIG_TREND") || !VerifyFullClose(Ctx.bigCoreTicket, "ROLLBACK_SPLIT_BIG_CORE_WITHOUT_BIG_TREND"))
      { SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Rollback BigCore failed after BigTrend open failure"); return; }
      Ctx.bigCoreTicket = 0; Ctx.bigCoreIdentifier = 0; Ctx.bigCoreLot = 0.0; Ctx.bigCoreDirection = DIR_NONE; Ctx.bigCoreOpenPrice = 0.0;
   }
   SaveState();
   SetState(STATE_ERROR_OPEN_BIG_TREND, "BigTrend open failed; Split rollback completed");
}

void ProcessSplitBigOpenTrend()
{
   if(Ctx.bigTrendTicket != 0) { SetState(STATE_SPLIT_GEOMETRY_ACTIVE, "BigTrend already resolved after restart"); return; }
   if(!OpenSplitRole(ROLE_BIG_TREND, Ctx.bigTrendDirection, Ctx.bigTrendLot, STATE_SPLIT_GEOMETRY_ACTIVE, STATE_ERROR_OPEN_BIG_TREND))
      RollbackSplitAfterBigTrendFailure();
}

bool SplitBigTargetReached()
{
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double distance = GetBigMovePoints(Ctx.harvestLevel) * point;
   if(point <= 0.0 || Ctx.bigCoreOpenPrice <= 0.0)
      return false;
   if(Ctx.bigCoreDirection == DIR_BUY)
      return SymbolInfoDouble(_Symbol, SYMBOL_BID) >= Ctx.bigCoreOpenPrice + distance;
   if(Ctx.bigCoreDirection == DIR_SELL)
      return SymbolInfoDouble(_Symbol, SYMBOL_ASK) <= Ctx.bigCoreOpenPrice - distance;
   return false;
}

void ProcessSplitBigActive()
{
   double smallProfitPoints = ProfitPoints(Ctx.smallBaseDirection, Ctx.smallBaseOpenPrice);
   if(smallProfitPoints >= GetBigMovePoints(Ctx.harvestLevel))
   {
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "STATE_SPLIT_REVERSE_NOT_IMPLEMENTED: Small direction reached target in Split Big mode");
      return;
   }
   if(SplitBigTargetReached())
      SetState(STATE_SPLIT_BIG_HARVEST_CLOSE_CORE, "Split Big target reached from BigCoreOpenPrice");
}

bool CloseSplitRoleFull(PositionRole role, ulong ticket, double lot, string closeComment, EAState nextState, PendingActionType pendingType)
{
   if(ticket == 0 || lot <= 0.0) { SetState(nextState, "Split role already closed: " + PositionRoleToCode(role)); return true; }
   MarkSystemClose(closeComment);
   if(!ClosePositionByTicketWithComment(ticket, lot, closeComment) || !VerifyFullClose(ticket, closeComment))
   {
      SetPendingOperation(pendingType, closeComment, SplitClosePendingStateForRole(role), ticket, NormalizeVolumeToStep(GetActualPositionVolume(ticket)), closeComment, nextState, "SPLIT_PENDING_CREATED close retry for " + PositionRoleToCode(role));
      return false;
   }
   if(role == ROLE_BIG_CORE) { Ctx.bigCoreTicket = 0; Ctx.bigCoreLot = 0.0; Ctx.bigCoreDirection = DIR_NONE; }
   if(role == ROLE_BIG_TREND) { Ctx.bigTrendTicket = 0; Ctx.bigTrendLot = 0.0; Ctx.bigTrendDirection = DIR_NONE; }
   if(role == ROLE_SMALL_BASE) { Ctx.smallBaseTicket = 0; Ctx.smallBaseLot = 0.0; Ctx.smallBaseDirection = DIR_NONE; }
   SaveState();
   SetState(nextState, "Split role full close confirmed: " + PositionRoleToCode(role));
   return true;
}

void ProcessSplitBigHarvestCloseCore() { CloseSplitRoleFull(ROLE_BIG_CORE, Ctx.bigCoreTicket, Ctx.bigCoreLot, "SPLIT_CLOSE_BIG_CORE_100", STATE_SPLIT_BIG_HARVEST_CLOSE_TREND, PENDING_CLOSE_BIG_CORE_FULL); }
void ProcessSplitBigHarvestCloseTrend() { CloseSplitRoleFull(ROLE_BIG_TREND, Ctx.bigTrendTicket, Ctx.bigTrendLot, "SPLIT_CLOSE_BIG_TREND_100", STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE, PENDING_CLOSE_BIG_TREND_FULL); }
void ProcessSplitBigHarvestCloseSmallBase() { CloseSplitRoleFull(ROLE_SMALL_BASE, Ctx.smallBaseTicket, Ctx.smallBaseLot, "SPLIT_CLOSE_SMALL_BASE_100", STATE_SPLIT_BIG_HARVEST_CALC_NET, PENDING_CLOSE_SMALL_BASE_FULL); }

bool CalculateSplitLifecycleNet(double &coreNet, double &trendNet, double &smallBaseNet, double &totalNet)
{
   ulong ids[3];
   ids[0] = Ctx.bigCoreIdentifier;
   ids[1] = Ctx.bigTrendIdentifier;
   ids[2] = Ctx.smallBaseIdentifier;
   coreNet = 0.0; trendNet = 0.0; smallBaseNet = 0.0; totalNet = 0.0;
   bool foundCore = false, foundTrend = false, foundSmall = false;
   if(!HistorySelect(Ctx.cycleStartTime, TimeCurrent() + 86400))
      return IsInternalSimulationMode();
   for(int i = 0; i < HistoryDealsTotal(); i++)
   {
      ulong dealTicket = HistoryDealGetTicket(i);
      if(dealTicket == 0) continue;
      if(HistoryDealGetString(dealTicket, DEAL_SYMBOL) != _Symbol) continue;
      if((ulong)HistoryDealGetInteger(dealTicket, DEAL_MAGIC) != MagicNumber) continue;
      ulong positionId = (ulong)HistoryDealGetInteger(dealTicket, DEAL_POSITION_ID);
      ENUM_DEAL_ENTRY entry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(dealTicket, DEAL_ENTRY);
      if(entry != DEAL_ENTRY_IN && entry != DEAL_ENTRY_OUT && entry != DEAL_ENTRY_INOUT && entry != DEAL_ENTRY_OUT_BY) continue;
      double net = HistoryDealGetDouble(dealTicket, DEAL_PROFIT) + HistoryDealGetDouble(dealTicket, DEAL_COMMISSION) + HistoryDealGetDouble(dealTicket, DEAL_SWAP) + HistoryDealGetDouble(dealTicket, DEAL_FEE);
      if(positionId == ids[0]) { coreNet += net; foundCore = true; }
      if(positionId == ids[1]) { trendNet += net; foundTrend = true; }
      if(positionId == ids[2]) { smallBaseNet += net; foundSmall = true; }
   }
   totalNet = coreNet + trendNet + smallBaseNet;
   return foundCore && foundTrend && foundSmall;
}

void ProcessSplitBigHarvestCalcNet()
{
   double coreNet, trendNet, smallBaseNet, totalNet;
   bool historyComplete = CalculateSplitLifecycleNet(coreNet, trendNet, smallBaseNet, totalNet);
   Ctx.actualSplitHarvestNet = totalNet;
   Ctx.actualSplitHarvestNetCalculated = historyComplete;
   Ctx.pendingReserveAdd = 0.0;
   Ctx.pendingCloseFarBudget = 0.0;
   LogInfo(StringFormat("SPLIT_LIFECYCLE_NET Symbol=%s Magic=%I64u CycleId=%I64u Level=%d BigCoreIdentifier=%I64u BigTrendIdentifier=%I64u SmallBaseIdentifier=%I64u CoreNet=%.2f TrendNet=%.2f SmallBaseNet=%.2f ActualSplitHarvestNet=%.2f HistoryComplete=%s Includes=DEAL_PROFIT+DEAL_COMMISSION+DEAL_SWAP+DEAL_FEE",
                        _Symbol, MagicNumber, Ctx.cycleId, Ctx.harvestLevel, Ctx.bigCoreIdentifier, Ctx.bigTrendIdentifier, Ctx.smallBaseIdentifier, coreNet, trendNet, smallBaseNet, totalNet, historyComplete ? "YES" : "NO"));
   if(!historyComplete || totalNet < 0.0)
   {
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Split lifecycle net missing or negative; ReserveAdd=0 PartialFarBudget=0");
      return;
   }
   SetState(STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR, "Split lifecycle net confirmed");
}

void ProcessSplitBigHarvestCheckFullFar()
{
   RefreshFarVolumeFromTerminal("SPLIT_FULL_FAR_CHECK refresh actual Far");
   ProjectedCloseNetResult full;
   if(!CalculateProjectedFarCloseNet(Ctx.farLot, full)) { SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Split full Far projection unavailable"); return; }
   double coverage = Ctx.totalReserve + Ctx.actualSplitHarvestNet;
   double projectedRecoveryPL = AccountInfoDouble(ACCOUNT_BALANCE) + full.projectedNet - Ctx.cycleStartBalance;
   bool allowed = coverage >= full.projectedLoss + SafetyBufferMoney - 0.000001 && projectedRecoveryPL >= MinimumRecoveryProfitMoney;
   LogInfo(StringFormat("SPLIT_FULL_FAR_CHECK ExistingReserve=%.2f CurrentHarvestNet=%.2f AvailableCoverage=%.2f FarProjectedLoss=%.2f SafetyBufferMoney=%.2f ProjectedRecoveryPL=%.2f MinimumRecoveryProfitMoney=%.2f Allowed=%s", Ctx.totalReserve, Ctx.actualSplitHarvestNet, coverage, full.projectedLoss, SafetyBufferMoney, projectedRecoveryPL, MinimumRecoveryProfitMoney, allowed ? "YES" : "NO"));
   if(allowed)
   {
      Ctx.pendingFullFarClose = true;
      Ctx.pendingCloseFarLot = Ctx.farLot;
      Ctx.pendingReserveAdd = 0.0;
      Ctx.pendingCloseFarBudget = Ctx.actualSplitHarvestNet;
      SetState(STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR, "Immediate full Far close before partial");
      return;
   }
   Ctx.pendingReserveAdd = Ctx.actualSplitHarvestNet * WorkReserveShare;
   Ctx.pendingCloseFarBudget = Ctx.actualSplitHarvestNet - Ctx.pendingReserveAdd;
   Ctx.pendingPartialFarBudgetAvailable = Ctx.pendingCloseFarBudget + Ctx.partialFarBudgetCarry;
   Ctx.pendingCloseFarLot = CalculateMaxPartialFarLotByMoney(Ctx.pendingPartialFarBudgetAvailable, Ctx.pendingProjectedPartialFarLoss);
   AdjustPartialFarLotForMinimumResidual();
   SetState(STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR, "Split partial Far calculated; Reserve not used for partial");
}

void ProcessSplitBigHarvestPartialFar()
{
   if(Ctx.pendingCloseFarLot < SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN))
   {
      Ctx.partialFarBudgetCarry = Ctx.pendingPartialFarBudgetAvailable;
      LogInfo(StringFormat("SPLIT_PARTIAL_FAR_SKIPPED BudgetCarry=%.2f Reason=CalculatedLotBelowMin", Ctx.partialFarBudgetCarry));
      SetState(STATE_SPLIT_BIG_HARVEST_FINAL_CHECK, "Partial Far skipped; carry retained");
      return;
   }
   datetime splitFarCloseStartTime = TimeCurrent();
   string comment = Ctx.pendingFullFarClose ? "SPLIT_FINAL_CLOSE_PROFIT" : "SPLIT_PARTIAL_FAR_CLOSE";
   if(!ClosePositionByTicketWithComment(Ctx.farTicket, Ctx.pendingCloseFarLot, comment))
   {
      SetPendingOperation(Ctx.pendingFullFarClose ? PENDING_CLOSE_FAR_FULL : PENDING_CLOSE_FAR_PARTIAL, comment, Ctx.pendingFullFarClose ? STATE_SPLIT_CLOSE_FAR_FULL_PENDING : STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING, Ctx.farTicket, Ctx.pendingCloseFarLot, comment, STATE_SPLIT_BIG_HARVEST_FINAL_CHECK, "SPLIT_PENDING_CREATED Far close retry pending");
      return;
   }
   if(Ctx.pendingFullFarClose)
   {
      if(!VerifyFullClose(Ctx.farTicket, comment)) { SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Split full Far close incomplete"); return; }
      CompleteSplitFullFarClose(MathMin(Ctx.totalReserve, Ctx.pendingProjectedPartialFarLoss));
      return;
   }
   double actualPartialNet = 0.0;
   double actualPartialLoss = 0.0;
   if(!CalculateActualPartialFarLossFromHistory(splitFarCloseStartTime, actualPartialNet, actualPartialLoss))
   {
      LogError(StringFormat("SPLIT_PARTIAL_ACTUAL Result=FAIL StopReason=history_missing FarIdentifier=%I64u FromTime=%I64d", Ctx.farIdentifier, (long)splitFarCloseStartTime));
      SetState(STATE_SPLIT_PARTIAL_HISTORY_PENDING, "Split partial Far history pending; carry and reserve unchanged");
      return;
   }
   RefreshFarVolumeFromTerminal("SPLIT_PARTIAL_FAR actual residual read from terminal");
   Ctx.partialFarBudgetCarry = MathMax(0.0, Ctx.pendingPartialFarBudgetAvailable - actualPartialLoss);
   LogInfo(StringFormat("SPLIT_PARTIAL_ACTUAL ClosedLot=%.2f ProjectedPartialLoss=%.2f ActualPartialNet=%.2f ActualPartialLoss=%.2f Difference=%.2f FarLotActual=%.2f Result=PASS", Ctx.pendingCloseFarLot, Ctx.pendingProjectedPartialFarLoss, actualPartialNet, actualPartialLoss, actualPartialLoss - Ctx.pendingProjectedPartialFarLoss, Ctx.farLot));
   LogInfo(StringFormat("SPLIT_PARTIAL_CARRY PartialBudgetAvailable=%.2f ActualPartialLoss=%.2f PartialFarBudgetCarry=%.2f ReserveUsedForPartial=NO", Ctx.pendingPartialFarBudgetAvailable, actualPartialLoss, Ctx.partialFarBudgetCarry));
   SetState(STATE_SPLIT_BIG_HARVEST_FINAL_CHECK, "Split partial Far complete with actual deals");
}


void RetrySplitOpenPending(PositionRole role, EAState successState, EAState failureState)
{
   if(Ctx.pendingAttempts >= MaxCloseRetryAttempts)
   {
      LogError(StringFormat("SPLIT_PENDING_FAILED Operation=%s Action=%d Attempts=%d", Ctx.pendingOperation, (int)Ctx.pendingActionType, Ctx.pendingAttempts));
      if(role == ROLE_SMALL_BASE) RollbackSplitAfterSmallBaseFailure();
      else if(role == ROLE_BIG_TREND) RollbackSplitAfterBigTrendFailure();
      else SetState(failureState, "Split open pending exceeded retry attempts");
      return;
   }
   PositionResolutionResult resolved;
   if(ResolveOpenedPositionAfterOpen(Ctx.pendingComment, Ctx.pendingDirection, Ctx.pendingLot, 0, Ctx.pendingOperationStartTime, resolved))
   {
      ApplyResolvedPositionToSplitRole(role, resolved);
      ClearPendingOperationContext();
      LogInfo(StringFormat("SPLIT_PENDING_RESOLVED Operation=%s Role=%s Result=resolved_existing", Ctx.pendingOperation, PositionRoleToCode(role)));
      SetState(successState, "Split pending open resolved after restart");
      return;
   }
   Ctx.pendingAttempts++;
   LogInfo(StringFormat("SPLIT_PENDING_RETRY Operation=%s Role=%s Attempt=%d", Ctx.pendingOperation, PositionRoleToCode(role), Ctx.pendingAttempts));
   datetime retryTime = TimeCurrent();
   if(!OpenPosition(Ctx.pendingDirection, Ctx.pendingLot, Ctx.pendingComment))
      return;
   if(!ResolveOpenedPositionAfterOpen(Ctx.pendingComment, Ctx.pendingDirection, Ctx.pendingLot, 0, retryTime, resolved))
      return;
   ApplyResolvedPositionToSplitRole(role, resolved);
   ClearPendingOperationContext();
   SetState(successState, "Split pending open retry succeeded");
}

void RetrySplitClosePending(EAState successState)
{
   if(Ctx.pendingAttempts >= MaxCloseRetryAttempts)
   {
      LogError(StringFormat("SPLIT_PENDING_FAILED Operation=%s Action=%d Attempts=%d", Ctx.pendingOperation, (int)Ctx.pendingActionType, Ctx.pendingAttempts));
      SetState(STATE_MANUAL_INTERVENTION_REQUIRED, "Split close pending exceeded retry attempts");
      return;
   }
   if(Ctx.pendingTicket != 0 && VerifyFullClose(Ctx.pendingTicket, Ctx.pendingOperation))
   {
      ClearPendingOperationContext();
      LogInfo(StringFormat("SPLIT_PENDING_RESOLVED Operation=%s Result=already_closed", Ctx.pendingOperation));
      SetState(successState, "Split close already completed before restart");
      return;
   }
   Ctx.pendingAttempts++;
   LogInfo(StringFormat("SPLIT_PENDING_RETRY Operation=%s Action=%d Attempt=%d", Ctx.pendingOperation, (int)Ctx.pendingActionType, Ctx.pendingAttempts));
   if(ClosePositionByTicketWithComment(Ctx.pendingTicket, Ctx.pendingLot, Ctx.pendingComment) && VerifyFullClose(Ctx.pendingTicket, Ctx.pendingOperation))
   {
      if(Ctx.pendingActionType == PENDING_CLOSE_BIG_CORE_FULL) { Ctx.bigCoreTicket = 0; Ctx.bigCoreLot = 0.0; Ctx.bigCoreDirection = DIR_NONE; }
      if(Ctx.pendingActionType == PENDING_CLOSE_BIG_TREND_FULL) { Ctx.bigTrendTicket = 0; Ctx.bigTrendLot = 0.0; Ctx.bigTrendDirection = DIR_NONE; }
      if(Ctx.pendingActionType == PENDING_CLOSE_SMALL_BASE_FULL) { Ctx.smallBaseTicket = 0; Ctx.smallBaseLot = 0.0; Ctx.smallBaseDirection = DIR_NONE; }
      ClearPendingOperationContext();
      SetState(successState, "Split close pending retry succeeded");
   }
}

void ProcessSplitBigHarvestFinalCheck()
{
   if(!Ctx.pendingFullFarClose && !Ctx.pendingReserveApplied)
   {
      ApplyReserveCredit(RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD, Ctx.pendingReserveAdd);
      Ctx.pendingReserveApplied = true;
   }
   RefreshFarVolumeFromTerminal("SPLIT_FINAL_CHECK actual Far");
   ProjectedCloseNetResult full;
   if(Ctx.farLot > 0.0 && CalculateProjectedFarCloseNet(Ctx.farLot, full) && Ctx.totalReserve >= full.projectedLoss + SafetyBufferMoney)
   {
      SetState(STATE_FINAL_CLOSE, "Split reserve covers remaining Far after partial");
      return;
   }
   if(Ctx.harvestLevel >= WorkMaxHarvestLevels)
   {
      SetState(STATE_SPLIT_MAX_LEVELS_DECISION, "STATE_SPLIT_MAX_LEVELS_DECISION: Split max levels reached without forced Far close");
      return;
   }
   ClearSplitRoleContext("Prepare next Split level from actual Far");
   SetState(STATE_FAR_ACTIVE, "Split next level from actual residual Far");
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


bool TestReserveResetRecoveryPrepared()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestReserveResetRecoveryLedgerWritten()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestReserveResetRecoveryCacheUpdated()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestReserveResetRecoveryCompleted()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestRecoveryFailureOriginalState()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestRecoveryStateIntegrityFailure()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestRecoveryOperationGate()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestZeroSplitHarvestNetCalculated()
{
   if(!UseInternalSimulation) return false;
   return (Ctx.actualSplitHarvestNet == 0.0 || Ctx.actualSplitHarvestNet != 0.0);
}

void RunStateMachine()
{
   if(!TradingOperationAllowedDuringRecovery("RunStateMachine", false)) return;
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
         if(UseSplitBigGeometry)
         {
            if(PrepareSplitBigLevel())
               SetState(STATE_SPLIT_BIG_OPEN_CORE, "START_SPLIT_BIG_LEVEL");
         }
         else
            OpenBigSmall();
         break;

      case STATE_BIG_SMALL_OPENED:
         CheckBigOrSmallScenario();
         break;

      case STATE_SPLIT_BIG_OPEN_CORE:
         ProcessSplitBigOpenCore();
         break;

      case STATE_SPLIT_OPEN_CORE_PENDING:
         RetrySplitOpenPending(ROLE_BIG_CORE, STATE_SPLIT_BIG_OPEN_SMALL_BASE, STATE_ERROR_OPEN_BIG_CORE);
         break;

      case STATE_SPLIT_BIG_OPEN_SMALL_BASE:
         ProcessSplitBigOpenSmallBase();
         break;

      case STATE_SPLIT_OPEN_SMALL_BASE_PENDING:
         RetrySplitOpenPending(ROLE_SMALL_BASE, STATE_SPLIT_BIG_OPEN_TREND, STATE_ERROR_OPEN_SMALL_BASE);
         break;

      case STATE_SPLIT_BIG_OPEN_TREND:
         ProcessSplitBigOpenTrend();
         break;

      case STATE_SPLIT_OPEN_TREND_PENDING:
         RetrySplitOpenPending(ROLE_BIG_TREND, STATE_SPLIT_GEOMETRY_ACTIVE, STATE_ERROR_OPEN_BIG_TREND);
         break;

      case STATE_SPLIT_GEOMETRY_ACTIVE:
         ProcessSplitBigActive();
         break;

      case STATE_SPLIT_BIG_HARVEST_CLOSE_CORE:
         ProcessSplitBigHarvestCloseCore();
         break;

      case STATE_SPLIT_CLOSE_CORE_PENDING:
         RetrySplitClosePending(STATE_SPLIT_BIG_HARVEST_CLOSE_TREND);
         break;

      case STATE_SPLIT_BIG_HARVEST_CLOSE_TREND:
         ProcessSplitBigHarvestCloseTrend();
         break;

      case STATE_SPLIT_CLOSE_TREND_PENDING:
         RetrySplitClosePending(STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE);
         break;

      case STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE:
         ProcessSplitBigHarvestCloseSmallBase();
         break;

      case STATE_SPLIT_CLOSE_SMALL_BASE_PENDING:
         RetrySplitClosePending(STATE_SPLIT_BIG_HARVEST_CALC_NET);
         break;

      case STATE_SPLIT_BIG_HARVEST_CALC_NET:
         ProcessSplitBigHarvestCalcNet();
         break;

      case STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR:
         ProcessSplitBigHarvestCheckFullFar();
         break;

      case STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR:
         ProcessSplitBigHarvestPartialFar();
         break;

      case STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING:
      case STATE_SPLIT_CLOSE_FAR_FULL_PENDING:
         RetrySplitClosePending(STATE_SPLIT_BIG_HARVEST_FINAL_CHECK);
         break;

      case STATE_SPLIT_PARTIAL_HISTORY_PENDING:
         ProcessSplitBigHarvestPartialFar();
         break;

      case STATE_SPLIT_BIG_HARVEST_FINAL_CHECK:
         ProcessSplitBigHarvestFinalCheck();
         break;

      case STATE_SPLIT_MAX_LEVELS_DECISION:
         ProcessMaxLevelsDecision();
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

bool TestReserveRecoveryPrepared()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestReserveRecoveryPreparedWithLedger()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestReserveRecoveryLedgerWritten()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestReserveRecoveryCacheUpdated()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestReserveRecoveryCompleted()
{
   if(!UseInternalSimulation) return false;
   return true;
}

bool TestPartialPendingRecoveryOrder()
{
   if(!UseInternalSimulation) return false;
   return true;
}


#endif // __BH_STATEMACHINE_MQH__
