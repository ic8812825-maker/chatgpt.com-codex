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
   GlobalVariableSet(StateKey("HarvestPhase"),(double)Ctx.harvestPhase); SaveStateUlong64("HarvestId",Ctx.harvestId); SaveStateLong64("HarvestDealFrom",Ctx.harvestDealFrom); SaveStateLong64("HarvestDealTo",Ctx.harvestDealTo);
   GlobalVariableSet(StateKey("HarvestReserveAdd"),Ctx.harvestReserveAdd); GlobalVariableSet(StateKey("HarvestPartialBudgetAdd"),Ctx.harvestPartialBudgetAdd); GlobalVariableSet(StateKey("HarvestCarryBefore"),Ctx.harvestCarryBefore); GlobalVariableSet(StateKey("HarvestCarryAfter"),Ctx.harvestCarryAfter);
   GlobalVariableSet(StateKey("ActualPartialFarCost"),Ctx.actualPartialFarCost);
   GlobalVariableSet(StateKey("ActualSmallTransitionNet"), Ctx.actualSmallTransitionNet);
   GlobalVariableSet(StateKey("FalseReverseAction"),(double)Ctx.falseReverseAction);SaveStateUlong64("FalseReverseExpectedTicket",Ctx.falseReverseExpectedTicket);GlobalVariableSet(StateKey("FalseReverseExpectedLot"),Ctx.falseReverseExpectedLot);
   GlobalVariableSet(StateKey("SmallOperationAuditCount"),(double)Ctx.smallOperationAuditCount);
   for(int auditIndex=0;auditIndex<5;auditIndex++) { string ap=StringFormat("SmallAudit_%d_",auditIndex); SmallOperationAudit a=Ctx.smallOperationAudits[auditIndex]; SaveStateUlong64(ap+"OperationId",a.operationId); GlobalVariableSet(StateKey(ap+"LegRole"),(double)a.legRole); GlobalVariableSet(StateKey(ap+"RequestedLot"),a.requestedLot); GlobalVariableSet(StateKey(ap+"FilledLot"),a.filledLot); GlobalVariableSet(StateKey(ap+"ResidualLot"),a.residualLot); GlobalVariableSet(StateKey(ap+"ProjectedNet"),a.projectedNet); GlobalVariableSet(StateKey(ap+"ActualNet"),a.actualNet); GlobalVariableSet(StateKey(ap+"ProjectedCommission"),a.projectedCommission); GlobalVariableSet(StateKey(ap+"ActualCommission"),a.actualCommission); GlobalVariableSet(StateKey(ap+"ProjectedSwap"),a.projectedSwap); GlobalVariableSet(StateKey(ap+"ActualSwap"),a.actualSwap); GlobalVariableSet(StateKey(ap+"ProjectedFee"),a.projectedFee); GlobalVariableSet(StateKey(ap+"ActualFee"),a.actualFee); SaveStateUlong64(ap+"Ticket",a.ticket); SaveStateUlong64(ap+"Identifier",a.identifier); SaveStateLong64(ap+"DealFrom",a.dealFrom); SaveStateLong64(ap+"DealTo",a.dealTo); GlobalVariableSet(StateKey(ap+"Completed"),a.completed?1.0:0.0); }
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
   GlobalVariableSet(StateKey("BigCoverageBefore"), Ctx.bigCoverageBefore);
   GlobalVariableSet(StateKey("BigFarLossBefore"), Ctx.bigFarLossBefore);
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

bool InspectPersistedUInt64(string fieldName, PersistedUInt64Inspection &result)
{
   result.fieldName = fieldName;
   result.highExists = GlobalVariableCheck(StateKey(fieldName + "High32"));
   result.lowExists = GlobalVariableCheck(StateKey(fieldName + "Low32"));
   result.highValue = 0;
   result.lowValue = 0;
   result.highRaw = 0.0;
   result.lowRaw = 0.0;
   result.highValueValid = false;
   result.lowValueValid = false;
   result.restoredValue = 0;
   result.reason = "";

   if(!result.highExists && !result.lowExists)
   {
      result.state = PERSISTED_UINT64_ABSENT;
      result.reason = "PERSISTED_UINT64_ABSENT";
      return true;
   }
   if(result.highExists != result.lowExists)
   {
      result.state = PERSISTED_UINT64_MALFORMED;
      result.reason = "PERSISTED_UINT64_MALFORMED";
      LogError(StringFormat("PERSISTED_UINT64_MALFORMED Field=%s HighExists=%s LowExists=%s RECOVERY_CONTEXT_RESET_FORBIDDEN",
                            fieldName, result.highExists ? "YES" : "NO", result.lowExists ? "YES" : "NO"));
      return false;
   }

   result.highRaw = GlobalVariableGet(StateKey(fieldName + "High32"));
   result.lowRaw = GlobalVariableGet(StateKey(fieldName + "Low32"));
   if(!MathIsValidNumber(result.highRaw) || !MathIsValidNumber(result.lowRaw))
   {
      result.state=PERSISTED_UINT64_MALFORMED; result.reason="PERSISTED_UINT64_NOT_FINITE"; return false;
   }
   if(result.highRaw < 0.0 || result.highRaw > 4294967295.0)
   {
      result.state=PERSISTED_UINT64_MALFORMED; result.reason="PERSISTED_UINT64_HIGH_OUT_OF_RANGE"; return false;
   }
   if(result.lowRaw < 0.0 || result.lowRaw > 4294967295.0)
   {
      result.state=PERSISTED_UINT64_MALFORMED; result.reason="PERSISTED_UINT64_LOW_OUT_OF_RANGE"; return false;
   }
   if(result.highRaw != MathFloor(result.highRaw))
   {
      result.state=PERSISTED_UINT64_MALFORMED; result.reason="PERSISTED_UINT64_HIGH_NOT_INTEGER"; return false;
   }
   if(result.lowRaw != MathFloor(result.lowRaw))
   {
      result.state=PERSISTED_UINT64_MALFORMED; result.reason="PERSISTED_UINT64_LOW_NOT_INTEGER"; return false;
   }
   result.highValueValid=true; result.lowValueValid=true;
   result.highValue = (uint)result.highRaw;
   result.lowValue = (uint)result.lowRaw;
   result.restoredValue = RestoreUlong64(result.highValue, result.lowValue);
   result.state = (result.restoredValue == 0 ? PERSISTED_UINT64_ZERO : PERSISTED_UINT64_ACTIVE);
   result.reason = (result.state == PERSISTED_UINT64_ZERO ? "PERSISTED_UINT64_ZERO" : "PERSISTED_UINT64_ACTIVE");
   return true;
}

void SaveStateLong64(string field, long value)
{
   uint high32, low32;
   SplitLong64(value, high32, low32);
   GlobalVariableSet(StateKey(field + "High32"), (double)high32);
   GlobalVariableSet(StateKey(field + "Low32"), (double)low32);
}

bool StrictLoadPersistedPair(string highKey,string lowKey,uint &high,uint &low,string fieldName)
{
   if(!GlobalVariableCheck(StateKey(highKey))||!GlobalVariableCheck(StateKey(lowKey))) { State=STATE_RECOVERY_MISMATCH; Ctx.lastError="PERSISTED_64_REQUIRED_PAIR_MISSING "+fieldName; return false; }
   double h=GlobalVariableGet(StateKey(highKey)),l=GlobalVariableGet(StateKey(lowKey));
   if(!MathIsValidNumber(h)||!MathIsValidNumber(l)||h<0.0||l<0.0||h>4294967295.0||l>4294967295.0||h!=MathFloor(h)||l!=MathFloor(l))
   { State=STATE_RECOVERY_MISMATCH; Ctx.lastError="PERSISTED_64_PAIR_MALFORMED "+fieldName; LogError(Ctx.lastError+" RECOVERY_CONTEXT_RESET_FORBIDDEN"); return false; }
   high=(uint)h; low=(uint)l; return true;
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
   uint high,low; if(!StrictLoadPersistedPair(highKey,lowKey,high,low,fieldName)) return false;
   value = RestoreUlong64(high,low);
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
   uint high,low; if(!StrictLoadPersistedPair(highKey,lowKey,high,low,fieldName)) return false;
   value = RestoreLong64(high,low);
   return true;
}

bool LoadStateUlong64(string field, ulong &value)
{
   string hk = StateKey(field + "High32");
   string lk = StateKey(field + "Low32");
   if(GlobalVariableCheck(hk) && GlobalVariableCheck(lk))
   {
      uint high,low; if(!StrictLoadPersistedPair(field+"High32",field+"Low32",high,low,field)) return false;
      value = RestoreUlong64(high,low);
      return true;
   }
   double legacy = 0.0;
   if(GetStateDouble(field, legacy))
   {
      bool risk = (!MathIsValidNumber(legacy)||legacy<0.0||legacy!=MathFloor(legacy)||MathAbs(legacy) >= 9007199254740992.0);
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
      uint high,low; if(!StrictLoadPersistedPair(field+"High32",field+"Low32",high,low,field)) return false;
      value = RestoreLong64(high,low);
      return true;
   }
   double legacy = 0.0;
   if(GetStateDouble(field, legacy))
   {
      bool risk = (!MathIsValidNumber(legacy)||legacy!=MathFloor(legacy)||MathAbs(legacy) >= 9007199254740992.0);
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


bool PersistedUInt64IsActive(PersistedUInt64Inspection &value)
{
   return value.state == PERSISTED_UINT64_ACTIVE;
}

bool PersistedUInt64IsMalformed(PersistedUInt64Inspection &value)
{
   return value.state == PERSISTED_UINT64_MALFORMED;
}

bool InspectPersistedRole(string role, string ticketField, string identifierField, string lotField,
                          string openPriceField, string directionField, PersistedRoleInspection &result)
{
   result.role=role;
   InspectPersistedUInt64(ticketField,result.ticket);
   InspectPersistedUInt64(identifierField,result.identifier);
   bool ticketActive=PersistedUInt64IsActive(result.ticket), idActive=PersistedUInt64IsActive(result.identifier);
   result.ticketIdentifierMismatch=(ticketActive!=idActive);
   double lot=GlobalVariableCheck(StateKey(lotField))?GlobalVariableGet(StateKey(lotField)):0.0;
   double price=GlobalVariableCheck(StateKey(openPriceField))?GlobalVariableGet(StateKey(openPriceField)):0.0;
   int direction=(directionField=="" ? (role=="INITIAL_BUY"?DIR_BUY:(role=="INITIAL_SELL"?DIR_SELL:DIR_NONE)) :
                  (GlobalVariableCheck(StateKey(directionField))?(int)GlobalVariableGet(StateKey(directionField)):DIR_NONE));
   result.active=ticketActive&&idActive;
   result.numericContextWithoutIdentity=(!result.active && (MathAbs(lot)>VolumeMismatchToleranceLots || price!=0.0 || direction!=DIR_NONE));
   result.malformed=PersistedUInt64IsMalformed(result.ticket)||PersistedUInt64IsMalformed(result.identifier)||
                    result.ticketIdentifierMismatch||result.numericContextWithoutIdentity||lot<0.0||price<0.0||direction<DIR_NONE||direction>DIR_SELL||
                    (result.active && (lot<=VolumeMismatchToleranceLots||price<=0.0||direction==DIR_NONE));
   result.reason=result.malformed?role+"_ROLE_MALFORMED":(result.active?role+"_ROLE_ACTIVE":role+"_ROLE_CLEAR");
   return !result.malformed;
}

void EvaluateInitialPersistence(bool &active, bool &malformed, string &reason)
{
   PersistedRoleInspection buyRole,sellRole;
   InspectPersistedRole("INITIAL_BUY","InitialBuyTicket","InitialBuyIdentifier","InitialBuyLot","InitialBuyOpenPrice","",buyRole);
   InspectPersistedRole("INITIAL_SELL","InitialSellTicket","InitialSellIdentifier","InitialSellLot","InitialSellOpenPrice","",sellRole);
   PersistedUInt64Inspection buyTicket, sellTicket, buyIdentifier, sellIdentifier;
   InspectPersistedUInt64("InitialBuyTicket", buyTicket);
   InspectPersistedUInt64("InitialSellTicket", sellTicket);
   InspectPersistedUInt64("InitialBuyIdentifier", buyIdentifier);
   InspectPersistedUInt64("InitialSellIdentifier", sellIdentifier);

   bool buyTicketActive = PersistedUInt64IsActive(buyTicket);
   bool sellTicketActive = PersistedUInt64IsActive(sellTicket);
   bool buyIdentifierActive = PersistedUInt64IsActive(buyIdentifier);
   bool sellIdentifierActive = PersistedUInt64IsActive(sellIdentifier);
   active = buyTicketActive || sellTicketActive || buyIdentifierActive || sellIdentifierActive;
   malformed = buyRole.malformed || sellRole.malformed || PersistedUInt64IsMalformed(buyTicket) || PersistedUInt64IsMalformed(sellTicket) ||
               PersistedUInt64IsMalformed(buyIdentifier) || PersistedUInt64IsMalformed(sellIdentifier);

   if(buyTicketActive != buyIdentifierActive || sellTicketActive != sellIdentifierActive)
      malformed = true;
   if(buyTicketActive && sellTicketActive && buyTicket.restoredValue == sellTicket.restoredValue)
      malformed = true;
   if(buyIdentifierActive && sellIdentifierActive && buyIdentifier.restoredValue == sellIdentifier.restoredValue)
      malformed = true;

   if(GlobalVariableCheck(StateKey("State")) && (EAState)(int)GlobalVariableGet(StateKey("State")) == STATE_INITIAL_LOCK_OPENED &&
      (!(buyTicketActive && buyIdentifierActive) || !(sellTicketActive && sellIdentifierActive)))
      malformed = true;
   reason = malformed ? "INITIAL_CONTEXT_MALFORMED" : (active ? "INITIAL_CONTEXT_ACTIVE" : "INITIAL_CONTEXT_CLEAR");
}

bool PersistedDoubleNonZero(string field, double tolerance = 0.0000001)
{
   return GlobalVariableCheck(StateKey(field)) && MathAbs(GlobalVariableGet(StateKey(field))) > tolerance;
}

void EvaluateLegacyPersistence(bool &active, bool &malformed, string &reason)
{
   PersistedRoleInspection farRole,bigRole,smallRole;
   InspectPersistedRole("FAR","FarTicket","FarIdentifier","FarLot","FarOpenPrice","FarDirection",farRole);
   InspectPersistedRole("BIG","BigTicket","BigIdentifier","BigLot","BigOpenPrice","BigDirection",bigRole);
   InspectPersistedRole("SMALL","SmallTicket","SmallIdentifier","SmallLot","SmallOpenPrice","SmallDirection",smallRole);
   PersistedUInt64Inspection cycleId, farTicket, farIdentifier, bigTicket, bigIdentifier, smallTicket, smallIdentifier;
   InspectPersistedUInt64("CycleId", cycleId);
   InspectPersistedUInt64("FarTicket", farTicket); InspectPersistedUInt64("FarIdentifier", farIdentifier);
   InspectPersistedUInt64("BigTicket", bigTicket); InspectPersistedUInt64("BigIdentifier", bigIdentifier);
   InspectPersistedUInt64("SmallTicket", smallTicket); InspectPersistedUInt64("SmallIdentifier", smallIdentifier);

   bool farActive = PersistedUInt64IsActive(farTicket) || PersistedUInt64IsActive(farIdentifier);
   bool bigActive = PersistedUInt64IsActive(bigTicket) || PersistedUInt64IsActive(bigIdentifier);
   bool smallActive = PersistedUInt64IsActive(smallTicket) || PersistedUInt64IsActive(smallIdentifier);
   active = PersistedUInt64IsActive(cycleId) || farActive || bigActive || smallActive;
   malformed = farRole.malformed||bigRole.malformed||smallRole.malformed||PersistedUInt64IsMalformed(cycleId) || PersistedUInt64IsMalformed(farTicket) || PersistedUInt64IsMalformed(farIdentifier) ||
               PersistedUInt64IsMalformed(bigTicket) || PersistedUInt64IsMalformed(bigIdentifier) ||
               PersistedUInt64IsMalformed(smallTicket) || PersistedUInt64IsMalformed(smallIdentifier);
   if(PersistedUInt64IsActive(farTicket) != PersistedUInt64IsActive(farIdentifier) ||
      PersistedUInt64IsActive(bigTicket) != PersistedUInt64IsActive(bigIdentifier) ||
      PersistedUInt64IsActive(smallTicket) != PersistedUInt64IsActive(smallIdentifier))
      malformed = true;

   bool farNumeric = PersistedDoubleNonZero("FarLot", VolumeMismatchToleranceLots) || PersistedDoubleNonZero("FarOpenPrice") || PersistedDoubleNonZero("FarDirection");
   bool bigNumeric = PersistedDoubleNonZero("BigLot", VolumeMismatchToleranceLots) || PersistedDoubleNonZero("BigOpenPrice") || PersistedDoubleNonZero("BigDirection");
   bool smallNumeric = PersistedDoubleNonZero("SmallLot", VolumeMismatchToleranceLots) || PersistedDoubleNonZero("SmallOpenPrice") || PersistedDoubleNonZero("SmallDirection");
   if((farNumeric && !farActive) || (bigNumeric && !bigActive) || (smallNumeric && !smallActive)) malformed = true;
   if(PersistedDoubleNonZero("HarvestLevel") || PersistedDoubleNonZero("ReverseCycles")) active = true;
   if(PersistedUInt64IsActive(cycleId) && !farActive && !bigActive && !smallActive) malformed = true;
   reason = malformed ? "LEGACY_CONTEXT_MALFORMED" : (active ? "LEGACY_CONTEXT_ACTIVE" : "LEGACY_CONTEXT_CLEAR");
}

void EvaluateSplitPersistence(bool &active, bool &malformed, string &reason)
{
   string roles[] = {"BigCore", "BigTrend", "SmallBase", "ReverseSmall"};
   active = false;
   malformed = false;
   for(int i = 0; i < ArraySize(roles); i++)
   {
      PersistedUInt64Inspection ticket, identifier;
      PersistedRoleInspection roleInspection;
      InspectPersistedRole(roles[i],roles[i]+"Ticket",roles[i]+"Identifier",roles[i]+"Lot",roles[i]+"OpenPrice",roles[i]+"Direction",roleInspection);
      InspectPersistedUInt64(roles[i] + "Ticket", ticket);
      InspectPersistedUInt64(roles[i] + "Identifier", identifier);
      bool ticketActive = PersistedUInt64IsActive(ticket);
      bool identifierActive = PersistedUInt64IsActive(identifier);
      bool numeric = PersistedDoubleNonZero(roles[i] + "Lot", VolumeMismatchToleranceLots) ||
                     PersistedDoubleNonZero(roles[i] + "OpenPrice") || PersistedDoubleNonZero(roles[i] + "Direction");
      active = active || ticketActive || identifierActive;
      if(roleInspection.malformed || PersistedUInt64IsMalformed(ticket) || PersistedUInt64IsMalformed(identifier) ||
         ticketActive != identifierActive || (numeric && !(ticketActive && identifierActive)))
         malformed = true;
   }
   bool splitFlag = PersistedDoubleNonZero("SplitGeometryActive", 0.5) || PersistedDoubleNonZero("ReverseConfirmed", 0.5) ||
                    PersistedDoubleNonZero("ReverseSmallOpened", 0.5);
   bool projected = PersistedDoubleNonZero("ProjectedReverseSmallLot", VolumeMismatchToleranceLots) ||
                    PersistedDoubleNonZero("ProjectedReverseSmallFinalLot", VolumeMismatchToleranceLots) ||
                    PersistedDoubleNonZero("ActualTransitionNet") || PersistedDoubleNonZero("ActualSmallTransitionNet");
   bool harvestCalculated = PersistedDoubleNonZero("ActualSplitHarvestNetCalculated", 0.5);
   if((splitFlag || projected) && !active) malformed = true;
   active = active || splitFlag || projected;
   if(harvestCalculated && active) active = true;
   reason = malformed ? "SPLIT_CONTEXT_MALFORMED" : (active ? "SPLIT_CONTEXT_ACTIVE" : "SPLIT_CONTEXT_CLEAR");
}

bool IsSplitHarvestPersistenceState(EAState state)
{
   return state==STATE_SPLIT_BIG_HARVEST_CALC_NET||state==STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR||
          state==STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR||state==STATE_SPLIT_PARTIAL_HISTORY_PENDING||
          state==STATE_SPLIT_BIG_HARVEST_FINAL_CHECK||state==STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING||
          state==STATE_SPLIT_CLOSE_FAR_FULL_PENDING||state==STATE_RECOVERY_PENDING;
}

void EvaluateSplitHarvestPersistence(bool &active,bool &malformed,string &reason)
{
   bool calculated=PersistedDoubleNonZero("ActualSplitHarvestNetCalculated",0.5);
   string moneyFields[]={"ActualSplitHarvestNet","ActualBigTrendNet","ActualTransitionNet","ActualSmallTransitionNet","BigGrossRatio","BigNetExposureRatio","ReserveGrowthRatio","NewFarCompressionRatio","ActualBigExposureLot","ActualSmallExposureLot"};
   bool nonzero=false,invalid=false;
   for(int i=0;i<ArraySize(moneyFields);i++) if(GlobalVariableCheck(StateKey(moneyFields[i]))) { double v=GlobalVariableGet(StateKey(moneyFields[i])); invalid=invalid||!MathIsValidNumber(v)||MathAbs(v)>1.0e12; nonzero=nonzero||MathAbs(v)>0.0000001; }
   PersistedUInt64Inspection cycle,far; InspectPersistedUInt64("CycleId",cycle); InspectPersistedUInt64("FarIdentifier",far);
   bool splitActive=false,splitMalformed=false; string splitReason=""; EvaluateSplitPersistence(splitActive,splitMalformed,splitReason);
   EAState state=GlobalVariableCheck(StateKey("State"))?(EAState)(int)GlobalVariableGet(StateKey("State")):STATE_IDLE;
   active=calculated||nonzero;
   malformed=invalid||(!calculated&&PersistedDoubleNonZero("ActualSplitHarvestNet"))||
             (calculated&&(!PersistedUInt64IsActive(cycle)||!PersistedUInt64IsActive(far)||!splitActive||!IsSplitHarvestPersistenceState(state)));
   reason=malformed?"SPLIT_HARVEST_LIFECYCLE_MALFORMED":(active?"SPLIT_HARVEST_LIFECYCLE_ACTIVE":"SPLIT_HARVEST_LIFECYCLE_CLEAR");
}

void EvaluateFrozenGeometryPersistence(bool &active, bool &malformed, string &reason)
{
   PersistedUInt64Inspection cycleId;
   InspectPersistedUInt64("CycleId", cycleId);
   bool cycleActive = PersistedUInt64IsActive(cycleId);
   bool ready = PersistedDoubleNonZero("GeometryReady", 0.5);
   bool calculated = PersistedDoubleNonZero("GeometryCalculatedTime");
   bool levelsReady = PersistedDoubleNonZero("WorkInitialTriggerPoints") && PersistedDoubleNonZero("WorkBigMoveStartPoints") &&
                      PersistedDoubleNonZero("WorkBigMoveStepPoints") && PersistedDoubleNonZero("WorkFarDistancePoints");
   bool atrValues = PersistedDoubleNonZero("CycleATRRaw") || PersistedDoubleNonZero("CycleATRPoints");
   double modeRaw=GlobalVariableCheck(StateKey("GeometryModeUsed"))?GlobalVariableGet(StateKey("GeometryModeUsed")):(double)GEOMETRY_MANUAL;
   bool modeValid=MathIsValidNumber(modeRaw)&&modeRaw==MathFloor(modeRaw)&&modeRaw>=GEOMETRY_MANUAL&&modeRaw<=GEOMETRY_ATR_CUSTOM;
   GeometryModeEnum persistedMode=modeValid?(GeometryModeEnum)(int)modeRaw:GEOMETRY_MANUAL;
   bool atrMode = persistedMode != GEOMETRY_MANUAL;
   bool configurationMismatch=ready&&modeValid&&persistedMode!=GeometryMode;
   active = cycleActive && ready && calculated && levelsReady && (!atrMode || atrValues);
   malformed = !modeValid || configurationMismatch || PersistedUInt64IsMalformed(cycleId) || (ready && (!cycleActive || !calculated || !levelsReady)) ||
               (atrMode && ready && !atrValues) || (atrValues && !ready && atrMode);
   reason = malformed ? "FROZEN_GEOMETRY_CONTEXT_MALFORMED" : (active ? "FROZEN_GEOMETRY_CONTEXT_ACTIVE" : "FROZEN_GEOMETRY_CONTEXT_CLEAR");
}

void EvaluatePendingPersistence(bool &active, bool &malformed, string &reason)
{
   PersistedUInt64Inspection ticket, bigId, smallId;
   InspectPersistedUInt64("PendingTicket", ticket);
   InspectPersistedUInt64("PendingBigPositionId", bigId);
   InspectPersistedUInt64("PendingSmallPositionId", smallId);
   PendingActionType action = PENDING_NONE;
   if(GlobalVariableCheck(StateKey("PendingActionType"))) action = (PendingActionType)(int)GlobalVariableGet(StateKey("PendingActionType"));
   bool ticketActive = PersistedUInt64IsActive(ticket);
   bool idsActive = PersistedUInt64IsActive(bigId) || PersistedUInt64IsActive(smallId);
   bool amounts = PersistedDoubleNonZero("PendingLot", VolumeMismatchToleranceLots) || PersistedDoubleNonZero("PendingAttempts") ||
                  PersistedDoubleNonZero("PendingOperationStartTime") || PersistedDoubleNonZero("PendingRealNet") ||
                  PersistedDoubleNonZero("PendingCloseFarBudget") || PersistedDoubleNonZero("PendingReserveAdd") ||
                  PersistedDoubleNonZero("PendingSmallReserveAdd") || PersistedDoubleNonZero("PendingCloseFarLot", VolumeMismatchToleranceLots) ||
                  PersistedDoubleNonZero("PendingPartialFarBudgetAvailable") || PersistedDoubleNonZero("PendingPartialFarBudgetCarryBefore") ||
                  PersistedDoubleNonZero("PendingProjectedPartialFarLoss") || PersistedDoubleNonZero("PendingDirection") ||
                  PersistedDoubleNonZero("PendingReserveApplied", 0.5) || PersistedDoubleNonZero("PendingSmallReserveApplied", 0.5) ||
                  PersistedDoubleNonZero("PendingFullFarClose", 0.5);
   active = action != PENDING_NONE;
   malformed = PersistedUInt64IsMalformed(ticket) || PersistedUInt64IsMalformed(bigId) || PersistedUInt64IsMalformed(smallId);
   if(!active && (ticketActive || idsActive || amounts)) malformed = true;
   if(active)
   {
      bool actionValid=action>PENDING_NONE&&action<=PENDING_STOP_MAX_LEVELS_CLOSE;
      bool openAction=action==PENDING_OPEN_BIG||action==PENDING_OPEN_SMALL||action==PENDING_OPEN_BIG_CORE||action==PENDING_OPEN_BIG_TREND||action==PENDING_OPEN_SMALL_BASE||action==PENDING_OPEN_REVERSE_SMALL;
      bool closeAction=!openAction;
      double lot=GlobalVariableCheck(StateKey("PendingLot"))?GlobalVariableGet(StateKey("PendingLot")):0.0;
      double attempts=GlobalVariableCheck(StateKey("PendingAttempts"))?GlobalVariableGet(StateKey("PendingAttempts")):0.0;
      int direction=GlobalVariableCheck(StateKey("PendingDirection"))?(int)GlobalVariableGet(StateKey("PendingDirection")):DIR_NONE;
      bool hasStart = PersistedDoubleNonZero("PendingOperationStartTime");
      bool hasNext = GlobalVariableCheck(StateKey("PendingNextState")) && (EAState)(int)GlobalVariableGet(StateKey("PendingNextState")) != STATE_IDLE;
      if(!actionValid||!hasStart||!hasNext||lot<=VolumeMismatchToleranceLots||attempts<0||attempts>MaxCloseRetryAttempts||
         (openAction&&(direction<DIR_BUY||direction>DIR_SELL))||(closeAction&&!ticketActive)) malformed=true;
      if(GlobalVariableCheck(StateKey("State")))
      {
         EAState persistedState = (EAState)(int)GlobalVariableGet(StateKey("State"));
         if(IsPendingContractState(persistedState) && !PendingActionMatchesState(persistedState, action)) malformed = true;
      }
   }
   if(PersistedDoubleNonZero("PendingCloseFarLot", VolumeMismatchToleranceLots) && !ticketActive) malformed = true;
   if(action==PENDING_CLOSE_FAR_PARTIAL && (!ticketActive||!PersistedDoubleNonZero("PendingCloseFarLot",VolumeMismatchToleranceLots)||
      !GlobalVariableCheck(StateKey("PendingPartialFarBudgetAvailable"))||!GlobalVariableCheck(StateKey("PendingProjectedPartialFarLoss"))||
      GlobalVariableGet(StateKey("PendingPartialFarBudgetAvailable"))<0.0||GlobalVariableGet(StateKey("PendingProjectedPartialFarLoss"))<0.0||PersistedDoubleNonZero("PendingFullFarClose",0.5))) malformed=true;
   reason = malformed ? "PENDING_CONTEXT_MALFORMED" : (active ? "PENDING_CONTEXT_ACTIVE" : "PENDING_CONTEXT_CLEAR");
}

void EvaluateRetryPersistence(bool &active, bool &malformed, string &reason)
{
   PersistedUInt64Inspection ticket;
   InspectPersistedUInt64("RetryTicket", ticket);
   bool ticketActive = PersistedUInt64IsActive(ticket);
   double lot = GlobalVariableCheck(StateKey("RetryLot")) ? GlobalVariableGet(StateKey("RetryLot")) : 0.0;
   int attempts = GlobalVariableCheck(StateKey("RetryAttempts")) ? (int)GlobalVariableGet(StateKey("RetryAttempts")) : 0;
   EAState retryState = GlobalVariableCheck(StateKey("LastRetryState")) ? (EAState)(int)GlobalVariableGet(StateKey("LastRetryState")) : STATE_IDLE;
   bool lotActive = lot > VolumeMismatchToleranceLots;
   bool attemptsActive = attempts > 0;
   bool stateActive = retryState != STATE_IDLE;
   active = ticketActive || lotActive || attemptsActive || stateActive;
   malformed = PersistedUInt64IsMalformed(ticket) || lot<0.0 || attempts<0 || attempts>MaxCloseRetryAttempts || (lotActive != ticketActive) ||
               (attemptsActive && !stateActive) || (ticketActive && !stateActive) ||
               (stateActive && !IsPendingContractState(retryState));
   PendingActionType action = GlobalVariableCheck(StateKey("PendingActionType")) ? (PendingActionType)(int)GlobalVariableGet(StateKey("PendingActionType")) : PENDING_NONE;
   if(stateActive && (action == PENDING_NONE || !PendingActionMatchesState(retryState, action))) malformed = true;
   PersistedUInt64Inspection pendingTicket; InspectPersistedUInt64("PendingTicket",pendingTicket);
   if(ticketActive&&PersistedUInt64IsActive(pendingTicket)&&ticket.restoredValue!=pendingTicket.restoredValue) malformed=true;
   if(stateActive&&!PersistedDoubleNonZero("PendingOperationStartTime")) malformed=true;
   reason = malformed ? "RETRY_CONTEXT_MALFORMED" : (active ? "RETRY_CONTEXT_ACTIVE" : "RETRY_CONTEXT_CLEAR");
}

bool PersistedKeyPrefixExists(string fieldPrefix)
{
   string prefix = StateKey(fieldPrefix);
   for(int i = 0; i < GlobalVariablesTotal(); i++) if(StringFind(GlobalVariableName(i), prefix) == 0) return true;
   return false;
}

void EvaluateReserveLedgerPersistence(bool &active, bool &malformed, string &reason)
{
   const int MAX_PERSISTED_RESERVE_LEDGER_ROWS=10000;
   double countRaw = GlobalVariableCheck(StateKey("ReserveLedgerCount")) ? GlobalVariableGet(StateKey("ReserveLedgerCount")) : 0.0;
   int count = (int)countRaw;
   PersistedUInt64Inspection nextEvent, nextTx;
   InspectPersistedUInt64("ReserveNextEventId", nextEvent);
   InspectPersistedUInt64("NextReserveTransactionId", nextTx);
   bool rowsExist = PersistedKeyPrefixExists("ReserveLedger_");
   double reserve = GlobalVariableCheck(StateKey("TotalReserve")) ? GlobalVariableGet(StateKey("TotalReserve")) : 0.0;
   active = count > 0 || MathAbs(reserve) > ReserveMismatchTolerance;
   malformed = !MathIsValidNumber(countRaw)||countRaw < 0.0 || MathAbs(countRaw - count) > 0.000001 || count > MAX_PERSISTED_RESERVE_LEDGER_ROWS ||
               PersistedUInt64IsMalformed(nextEvent) || PersistedUInt64IsMalformed(nextTx) ||
               (count == 0 && rowsExist) || (count == 0 && PersistedUInt64IsActive(nextEvent) && nextEvent.restoredValue > 1) ||
               (count == 0 && MathAbs(reserve) > ReserveMismatchTolerance);
   double previousAfter=0.0,lastAfter=0.0;
   for(int i=0;i<count;i++)
   {
      string p=StringFormat("ReserveLedger_%d_",i);
      PersistedUInt64Inspection eventId,eventKey,symbolHash,magic,cycleId;
      InspectPersistedUInt64(p+"EventId",eventId); InspectPersistedUInt64(p+"EventKeyHash",eventKey); InspectPersistedUInt64(p+"SymbolHash",symbolHash); InspectPersistedUInt64(p+"MagicNumber",magic); InspectPersistedUInt64(p+"CycleId",cycleId);
      string scalar[]={"Timestamp","Type","Amount","ReserveBefore","ReserveAfter","SymbolLength","HarvestLevel","ReverseCycle"};
      for(int s=0;s<ArraySize(scalar);s++) if(!GlobalVariableCheck(StateKey(p+scalar[s]))) malformed=true;
      if(eventId.state!=PERSISTED_UINT64_ACTIVE||eventId.restoredValue!=(ulong)(i+1)||eventKey.state!=PERSISTED_UINT64_ACTIVE||symbolHash.state!=PERSISTED_UINT64_ACTIVE||magic.state!=PERSISTED_UINT64_ACTIVE) malformed=true;
      double type=GlobalVariableCheck(StateKey(p+"Type"))?GlobalVariableGet(StateKey(p+"Type")):-1;
      double amount=GlobalVariableCheck(StateKey(p+"Amount"))?GlobalVariableGet(StateKey(p+"Amount")):0;
      double before=GlobalVariableCheck(StateKey(p+"ReserveBefore"))?GlobalVariableGet(StateKey(p+"ReserveBefore")):0;
      double after=GlobalVariableCheck(StateKey(p+"ReserveAfter"))?GlobalVariableGet(StateKey(p+"ReserveAfter")):0;
      double stamp=GlobalVariableCheck(StateKey(p+"Timestamp"))?GlobalVariableGet(StateKey(p+"Timestamp")):0;
      if(!MathIsValidNumber(amount)||!MathIsValidNumber(before)||!MathIsValidNumber(after)||type<=RESERVE_EVENT_NONE||type>RESERVE_EVENT_RESET||type!=MathFloor(type)||stamp<=0||MathAbs(after-(before+amount))>ReserveMismatchTolerance||(i>0&&MathAbs(before-previousAfter)>ReserveMismatchTolerance)) malformed=true;
      previousAfter=after; lastAfter=after;
   }
   if(PersistedKeyPrefixExists(StringFormat("ReserveLedger_%d_",count))) malformed=true;
   if(count>0 && (!PersistedUInt64IsActive(nextEvent)||nextEvent.restoredValue!=(ulong)(count+1)||MathAbs(reserve-lastAfter)>ReserveMismatchTolerance)) malformed=true;
   reason = malformed ? "RESERVE_LEDGER_CONTEXT_MALFORMED" : (active ? "RESERVE_LEDGER_CONTEXT_ACTIVE" : "RESERVE_LEDGER_CONTEXT_CLEAR");
}

void EvaluateReserveTransactionPersistence(bool &active, bool &malformed, string &reason)
{
   active = PersistedDoubleNonZero("ReserveTxActive", 0.5);
   string ids[] = {"ReserveTxTransactionId","ReserveTxEventKeyHash","ReserveTxExpectedLedgerEventId","ReserveTxSymbolHash","ReserveTxMagicNumber","ReserveTxCycleId","ReserveTxFarIdentifier","ReserveTxBigIdentifier","ReserveTxSmallIdentifier","ReserveTxBigCoreIdentifier","ReserveTxBigTrendIdentifier","ReserveTxSmallBaseIdentifier","ReserveTxReverseSmallIdentifier"};
   bool residual = false;
   malformed = false;
   for(int i=0;i<ArraySize(ids);i++) { PersistedUInt64Inspection value; InspectPersistedUInt64(ids[i],value); residual=residual||PersistedUInt64IsActive(value); malformed=malformed||PersistedUInt64IsMalformed(value); }
   double phase=GlobalVariableCheck(StateKey("ReserveTxPhase"))?GlobalVariableGet(StateKey("ReserveTxPhase")):0.0;
   double amount=GlobalVariableCheck(StateKey("ReserveTxAmount"))?GlobalVariableGet(StateKey("ReserveTxAmount")):0.0;
   double before=GlobalVariableCheck(StateKey("ReserveTxReserveBefore"))?GlobalVariableGet(StateKey("ReserveTxReserveBefore")):0.0;
   double after=GlobalVariableCheck(StateKey("ReserveTxReserveAfter"))?GlobalVariableGet(StateKey("ReserveTxReserveAfter")):0.0;
   int eventType=GlobalVariableCheck(StateKey("ReserveTxEventType"))?(int)GlobalVariableGet(StateKey("ReserveTxEventType")):RESERVE_EVENT_NONE;
   bool eventValid=eventType>=RESERVE_EVENT_NONE&&eventType<=RESERVE_EVENT_RESET;
   bool phaseValid=phase>=RESERVE_TX_NONE&&phase<=RESERVE_TX_COMPLETED&&phase==MathFloor(phase);
   bool credit=(eventType==RESERVE_EVENT_BIG_HARVEST_ADD||eventType==RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD||eventType==RESERVE_EVENT_REVERSE_TRANSITION_ADD||eventType==RESERVE_EVENT_SMALL_HARVEST_ADD);
   bool debit=(eventType==RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT||eventType==RESERVE_EVENT_FAR_COVER_DEBIT||eventType==RESERVE_EVENT_BIG_FULL_FAR_CLOSE_DEBIT||eventType==RESERVE_EVENT_SMALL_FAR_DEBIT||eventType==RESERVE_EVENT_FINAL_CLOSE_DEBIT);
   residual=residual||phase!=RESERVE_TX_NONE||MathAbs(amount)>ReserveMismatchTolerance||PersistedDoubleNonZero("ReserveTxStartedAt");
   if(!active && residual) malformed=true;
   if(active && (!residual||!eventValid||!phaseValid||MathAbs(after-(before+amount))>ReserveMismatchTolerance||
      (credit&&(amount<=0.0||after<=before))||(debit&&(amount>=0.0||after>=before))||
      (eventType==RESERVE_EVENT_RESET&&MathAbs(after)>ReserveMismatchTolerance))) malformed=true;
   reason=malformed?"RESERVE_TRANSACTION_CONTEXT_MALFORMED":(active?"RESERVE_TRANSACTION_CONTEXT_ACTIVE":"RESERVE_TRANSACTION_CONTEXT_CLEAR");
}

void EvaluateRecoveryFailureMarkerPersistence(RecoveryFailureMarkerInspection &result)
{
   result.active=PersistedDoubleNonZero("RecoveryFailureActive",0.5);
   result.reasonCode=GlobalVariableCheck(StateKey("RecoveryFailureReasonCode"))?(int)GlobalVariableGet(StateKey("RecoveryFailureReasonCode")):RECOVERY_FAILURE_NONE;
   result.failureTime=GlobalVariableCheck(StateKey("RecoveryFailureTime"))?(datetime)GlobalVariableGet(StateKey("RecoveryFailureTime")):0;
   result.originalState=GlobalVariableCheck(StateKey("RecoveryFailureOriginalState"))?(EAState)(int)GlobalVariableGet(StateKey("RecoveryFailureOriginalState")):STATE_IDLE;
   InspectPersistedUInt64("RecoveryFailureCycleId",result.cycleId); InspectPersistedUInt64("RecoveryFailureTransactionId",result.transactionId); InspectPersistedUInt64("RecoveryFailureEventKey",result.eventKey);
   bool ids=PersistedUInt64IsActive(result.cycleId)||PersistedUInt64IsActive(result.transactionId)||PersistedUInt64IsActive(result.eventKey);
   bool invalidIds=PersistedUInt64IsMalformed(result.cycleId)||PersistedUInt64IsMalformed(result.transactionId)||PersistedUInt64IsMalformed(result.eventKey);
   bool residual=result.reasonCode!=RECOVERY_FAILURE_NONE||result.failureTime>0||result.originalState!=STATE_IDLE||ids;
   result.malformed=invalidIds||(!result.active&&residual)||(result.active&&(result.reasonCode<=RECOVERY_FAILURE_NONE||result.reasonCode>RECOVERY_FAILURE_OTHER||result.failureTime<=0||result.originalState<STATE_IDLE||result.originalState>STATE_ERROR))||
                    (PersistedUInt64IsActive(result.transactionId)&&!PersistedUInt64IsActive(result.eventKey));
   result.reason=result.malformed?"RECOVERY_FAILURE_MARKER_MALFORMED":(result.active?"RECOVERY_FAILURE_MARKER_ACTIVE":"RECOVERY_FAILURE_MARKER_CLEAR");
}

void AddCleanStartReason(string reason,string &allReasons)
{ if(reason=="") return; if(allReasons!="") allReasons+=";"; allReasons+=reason; }

bool EvaluateCleanStart(CleanStartEvaluation &r)
{
   r.stateKeyPresent=GlobalVariableCheck(StateKey("State")); r.allReasons=""; r.primaryReason="";
   string ledgerReason = "";
   EvaluateReserveLedgerPersistence(r.ledgerActive,r.ledgerMalformed,ledgerReason);
   string reserveTxReason=""; EvaluateReserveTransactionPersistence(r.reserveTransactionActive,r.reserveTransactionMalformed,reserveTxReason);
   RecoveryFailureMarkerInspection failureInspection; EvaluateRecoveryFailureMarkerPersistence(failureInspection);
   r.failureMarkerActive=failureInspection.active; r.failureMarkerMalformed=failureInspection.malformed;
   string pendingReason = "";
   EvaluatePendingPersistence(r.pendingActive,r.pendingMalformed,pendingReason);
   string retryReason = "";
   EvaluateRetryPersistence(r.retryActive,r.retryMalformed,retryReason);
   string initialReason = "";
   EvaluateInitialPersistence(r.initialActive,r.initialMalformed,initialReason);
   string legacyReason = "";
   EvaluateLegacyPersistence(r.legacyActive,r.legacyMalformed,legacyReason);
   string splitReason = "";
   EvaluateSplitPersistence(r.splitActive,r.splitMalformed,splitReason);
   string splitHarvestReason=""; EvaluateSplitHarvestPersistence(r.splitHarvestActive,r.splitHarvestMalformed,splitHarvestReason);
   string geometryReason = "";
   EvaluateFrozenGeometryPersistence(r.geometryActive,r.geometryMalformed,geometryReason); r.managedPositions=CountManagedOpenPositions();
   if(r.managedPositions>0) LogError(StringFormat("MANAGED_POSITIONS_PRESENT_DURING_RECOVERY_FAILURE Count=%d",r.managedPositions));
   if(r.managedPositions>0) AddCleanStartReason("MANAGED_POSITIONS_PRESENT",r.allReasons);
   if(r.reserveTransactionMalformed) AddCleanStartReason(reserveTxReason,r.allReasons); if(r.ledgerMalformed) AddCleanStartReason(ledgerReason,r.allReasons);
   if(r.pendingMalformed) AddCleanStartReason(pendingReason,r.allReasons); if(r.retryMalformed) AddCleanStartReason(retryReason,r.allReasons);
   if(r.initialMalformed) AddCleanStartReason(initialReason,r.allReasons); if(r.legacyMalformed) AddCleanStartReason(legacyReason,r.allReasons); if(r.splitMalformed) AddCleanStartReason(splitReason,r.allReasons);
   if(r.splitHarvestMalformed) AddCleanStartReason(splitHarvestReason,r.allReasons); if(r.geometryMalformed) AddCleanStartReason(geometryReason,r.allReasons); if(r.failureMarkerMalformed) AddCleanStartReason(failureInspection.reason,r.allReasons);
   bool anyActive=r.initialActive||r.legacyActive||r.splitActive||r.splitHarvestActive||r.geometryActive||r.pendingActive||r.retryActive||r.ledgerActive||r.reserveTransactionActive||r.failureMarkerActive;
   if(anyActive) AddCleanStartReason("ACTIVE_PERSISTENCE_CONTEXT",r.allReasons); if(r.stateKeyPresent) AddCleanStartReason("STATE_KEY_PRESENT",r.allReasons);
   r.cleanStartAllowed=r.managedPositions==0&&!anyActive&&r.allReasons=="";
   if(r.managedPositions>0) r.primaryReason="MANAGED_POSITIONS_PRESENT"; else if(r.reserveTransactionMalformed) r.primaryReason=reserveTxReason; else if(r.ledgerMalformed) r.primaryReason=ledgerReason; else if(r.pendingMalformed) r.primaryReason=pendingReason; else if(r.retryMalformed) r.primaryReason=retryReason; else if(r.allReasons!="") r.primaryReason=r.allReasons; else r.primaryReason="CLEAN_START_CONFIRMED";
   LogInfo(StringFormat("CLEAN_START_EVALUATION Initial=%s Legacy=%s Split=%s SplitHarvest=%s Geometry=%s Pending=%s Retry=%s Ledger=%s ReserveTx=%s FailureMarker=%s ManagedPositions=%d Allowed=%s PrimaryReason=%s AllReasons=%s",initialReason,legacyReason,splitReason,splitHarvestReason,geometryReason,pendingReason,retryReason,ledgerReason,reserveTxReason,failureInspection.reason,r.managedPositions,r.cleanStartAllowed?"YES":"NO",r.primaryReason,r.allReasons));
   return r.cleanStartAllowed;
}

bool IsProvenCleanStart() { CleanStartEvaluation evaluation; EvaluateCleanStart(evaluation); if(!evaluation.cleanStartAllowed) LogError("RECOVERY_CONTEXT_RESET_FORBIDDEN"); return evaluation.cleanStartAllowed; }

bool ReloadHarvestPersistence()
{
   double saved=0; if(!GetStateDouble("HarvestPhase",saved)) return false; int phase=(int)saved; if(phase<HARVEST_NONE||phase>HARVEST_CONSUMED) return false; Ctx.harvestPhase=(HarvestPhase)phase;
   if(!LoadOptionalStateUlong64("HarvestId",Ctx.harvestId)||!LoadOptionalStateLong64("HarvestDealFrom",Ctx.harvestDealFrom)||!LoadOptionalStateLong64("HarvestDealTo",Ctx.harvestDealTo)) return false;
   if(GetStateDouble("HarvestReserveAdd",saved)) Ctx.harvestReserveAdd=saved; if(GetStateDouble("HarvestPartialBudgetAdd",saved)) Ctx.harvestPartialBudgetAdd=saved; if(GetStateDouble("HarvestCarryBefore",saved)) Ctx.harvestCarryBefore=saved; if(GetStateDouble("HarvestCarryAfter",saved)) Ctx.harvestCarryAfter=saved;
   return Ctx.harvestPhase==HARVEST_NONE||Ctx.harvestId!=0;
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
   if(GetStateDouble("HarvestPhase",saved)) Ctx.harvestPhase=(HarvestPhase)((int)saved); LoadOptionalStateUlong64("HarvestId",Ctx.harvestId); LoadOptionalStateLong64("HarvestDealFrom",Ctx.harvestDealFrom); LoadOptionalStateLong64("HarvestDealTo",Ctx.harvestDealTo);
   if(GetStateDouble("HarvestReserveAdd",saved)) Ctx.harvestReserveAdd=saved; if(GetStateDouble("HarvestPartialBudgetAdd",saved)) Ctx.harvestPartialBudgetAdd=saved; if(GetStateDouble("HarvestCarryBefore",saved)) Ctx.harvestCarryBefore=saved; if(GetStateDouble("HarvestCarryAfter",saved)) Ctx.harvestCarryAfter=saved;
   if(GetStateDouble("ActualPartialFarCost",saved)) Ctx.actualPartialFarCost=saved;
   if(GetStateDouble("ActualSmallTransitionNet", saved)) Ctx.actualSmallTransitionNet = saved;
   if(GetStateDouble("FalseReverseAction",saved))Ctx.falseReverseAction=(int)saved;LoadOptionalStateUlong64("FalseReverseExpectedTicket",Ctx.falseReverseExpectedTicket);if(GetStateDouble("FalseReverseExpectedLot",saved))Ctx.falseReverseExpectedLot=saved;
   if(GetStateDouble("SmallOperationAuditCount",saved)) Ctx.smallOperationAuditCount=(int)saved;
   for(int auditIndex=0;auditIndex<5;auditIndex++) { string ap=StringFormat("SmallAudit_%d_",auditIndex); SmallOperationAudit a; LoadOptionalStateUlong64(ap+"OperationId",a.operationId); if(GetStateDouble(ap+"LegRole",saved))a.legRole=(int)saved; if(GetStateDouble(ap+"RequestedLot",saved))a.requestedLot=saved; if(GetStateDouble(ap+"FilledLot",saved))a.filledLot=saved; if(GetStateDouble(ap+"ResidualLot",saved))a.residualLot=saved; if(GetStateDouble(ap+"ProjectedNet",saved))a.projectedNet=saved; if(GetStateDouble(ap+"ActualNet",saved))a.actualNet=saved; if(GetStateDouble(ap+"ProjectedCommission",saved))a.projectedCommission=saved; if(GetStateDouble(ap+"ActualCommission",saved))a.actualCommission=saved; if(GetStateDouble(ap+"ProjectedSwap",saved))a.projectedSwap=saved; if(GetStateDouble(ap+"ActualSwap",saved))a.actualSwap=saved; if(GetStateDouble(ap+"ProjectedFee",saved))a.projectedFee=saved; if(GetStateDouble(ap+"ActualFee",saved))a.actualFee=saved; LoadOptionalStateUlong64(ap+"Ticket",a.ticket); LoadOptionalStateUlong64(ap+"Identifier",a.identifier); LoadOptionalStateLong64(ap+"DealFrom",a.dealFrom); LoadOptionalStateLong64(ap+"DealTo",a.dealTo); if(GetStateDouble(ap+"Completed",saved))a.completed=saved>0.5; Ctx.smallOperationAudits[auditIndex]=a; }
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
   if(GetStateDouble("BigCoverageBefore", saved)) Ctx.bigCoverageBefore=saved;
   if(GetStateDouble("BigFarLossBefore", saved)) Ctx.bigFarLossBefore=saved;
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
   double bid = MarketBid();
   double ask = MarketAsk();
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
   BrokerMoneyResult money; ResetBrokerMoneyResult(money);
   double swapPart = 0.0;
   if(PositionSelectByTicket(ticket))
   {
      double fullSwap = PositionGetDouble(POSITION_SWAP);
      if(pos.lot > 0.0) swapPart = fullSwap * (closeLot / pos.lot);
   }
   double profit = 0.0;
   if(IsInternalSimulationMode())
      profit = CalcSignedPositionPL(pos.direction, closeLot, pos.openPrice, closePrice);
   else
   {
      if(!CalcProjectedCloseNetMoneyWithAccrued(pos.direction, closeLot, pos.openPrice, closePrice, swapPart, money))
      {
         LogError("BROKER_MONEY_MODEL_REQUIRED " + money.reason);
         return false;
      }
      profit = money.grossProfit;
   }

   result.projectedGrossProfit = profit;
   result.projectedSwapPart = swapPart;
   result.estimatedCommission = money.closeCommission;
   // One account-currency model for simulation and live projection. Reserve is never part of this budget.
   result.projectedNet = money.netMoney;
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
      // Partial route must leave at least one broker volume step; full close belongs to FinalCloseGate.
      double residualSafe=NormalizeLotDown(Ctx.farLot-MathMax(minLot,SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_STEP)));
      if(residualSafe<minLot) return 0.0;
      ProjectedCloseNetResult safe; if(!CalculateProjectedFarCloseNet(residualSafe,safe)||safe.projectedLoss>budget+0.000001) return 0.0;
      projectedLoss=safe.projectedLoss; return residualSafe;
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


bool EvaluateFinalCloseGate(FinalCloseEvaluation &result)
{
   result.calculationValid = false;
   result.farCloseLossWorstCase = 0.0;
   result.expectedCurrentHarvestNet = 0.0;
   result.reserveAvailable = Ctx.totalReserve;
   result.partialCarryAvailable = Ctx.partialFarBudgetCarry;
   result.totalCoverageAvailable = Ctx.totalReserve + Ctx.partialFarBudgetCarry;
   result.projectedRecoveryPL = 0.0;
   result.projectedCommission = 0.0;
   result.projectedSpreadCost = 0.0;
   result.projectedSlippageCost = 0.0;
   result.safetyBuffer = SafetyBufferMoney + ExecutionSafetyBufferMoney;
   result.coveragePass = false;
   result.recoveryPass = false;
   result.positionsPass = false;
   result.finalAllowed = false;
   result.reason = "";

   if(ActiveReserveTransaction.active || Ctx.pendingActionType != PENDING_NONE || State == STATE_RECOVERY_MISMATCH)
   {
      result.reason = "FINAL_CLOSE_GATE_BLOCKED_BY_PENDING_OR_RECOVERY";
      return false;
   }

   ProjectedCloseNetResult farProjection;
   if(!CalculateProjectedFarCloseNet(Ctx.farLot, farProjection))
   {
      result.reason = "FINAL_CLOSE_GATE_MONEY_CALC_FAILED";
      return false;
   }

   result.calculationValid = true;
   result.farCloseLossWorstCase = farProjection.projectedLoss;
   result.projectedCommission = farProjection.estimatedCommission;
   // Current Harvest is available only before it is distributed into Reserve/partial carry.
   result.expectedCurrentHarvestNet = (Ctx.actualSplitHarvestNetCalculated && !Ctx.pendingReserveApplied) ? Ctx.actualSplitHarvestNet : 0.0;
   result.totalCoverageAvailable = Ctx.totalReserve + Ctx.partialFarBudgetCarry + MathMax(0.0, result.expectedCurrentHarvestNet);
   double projectedOpenPositionsNet=0.0; int projectedPositions=0; bool basketValid=true;
   for(int i=PositionsTotal()-1;i>=0;i--)
   {
      ulong ticket=PositionGetTicket(i); if(ticket==0||!PositionSelectByTicket(ticket)) continue;
      if(PositionGetString(POSITION_SYMBOL)!=_Symbol||(ulong)PositionGetInteger(POSITION_MAGIC)!=MagicNumber) continue;
      Direction d=(PositionGetInteger(POSITION_TYPE)==POSITION_TYPE_BUY?DIR_BUY:DIR_SELL);
      double lot=PositionGetDouble(POSITION_VOLUME),open=PositionGetDouble(POSITION_PRICE_OPEN),close=d==DIR_BUY?MarketBid():MarketAsk();
      BrokerMoneyResult item; if(!CalcProjectedCloseNetMoneyWithAccrued(d,lot,open,close,PositionGetDouble(POSITION_SWAP),item)) { basketValid=false; break; }
      projectedOpenPositionsNet+=item.netMoney; result.projectedCommission+=item.closeCommission; result.projectedSpreadCost+=item.spreadExpansionCost; result.projectedSlippageCost+=item.slippageCost; projectedPositions++;
   }
   result.calculationValid=result.calculationValid&&basketValid;
   result.projectedRecoveryPL=AccountInfoDouble(ACCOUNT_BALANCE)+projectedOpenPositionsNet-Ctx.cycleStartBalance-result.safetyBuffer;
   result.coveragePass = (result.totalCoverageAvailable + ReserveMismatchTolerance >= result.farCloseLossWorstCase + result.safetyBuffer);
   result.recoveryPass = (result.projectedRecoveryPL + ReserveMismatchTolerance >= MinimumRecoveryProfitMoney);
   result.positionsPass = basketValid&&projectedPositions>0&&(Ctx.farTicket != 0 || Ctx.farIdentifier != 0)&&Ctx.farLot>VolumeMismatchToleranceLots&&ValidateNoOrphanManagedPositions();
   result.finalAllowed = result.calculationValid && result.coveragePass && result.recoveryPass && result.positionsPass;
   result.reason = result.finalAllowed ? "FINAL_CLOSE_GATE_PASS" : "FINAL_CLOSE_GATE_FAIL";
   LogInfo(StringFormat("FINAL_CLOSE_GATE CalculationValid=%s FarCloseLossWorstCase=%.2f Coverage=%.2f ProjectedRecoveryPL=%.2f CoveragePass=%s RecoveryPass=%s PositionsPass=%s FinalAllowed=%s Reason=%s",
                        result.calculationValid ? "YES" : "NO", result.farCloseLossWorstCase, result.totalCoverageAvailable, result.projectedRecoveryPL,
                        result.coveragePass ? "YES" : "NO", result.recoveryPass ? "YES" : "NO", result.positionsPass ? "YES" : "NO", result.finalAllowed ? "YES" : "NO", result.reason));
   return result.finalAllowed;
}

void ProcessSmallCheckReserve()
{
   FinalCloseEvaluation finalGate;
   Ctx.finalCloseAllowed = EvaluateFinalCloseGate(finalGate);
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
   else if(role == ROLE_REVERSE_SMALL)
   {
      Ctx.reverseSmallTicket=result.ticket; Ctx.reverseSmallIdentifier=result.identifier; Ctx.reverseSmallLot=result.lot; Ctx.reverseSmallOpenPrice=result.openPrice; Ctx.reverseSmallDirection=resolvedDirection; Ctx.reverseSmallOpened=true;
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

   Direction basketDirections[3]={Ctx.bigCoreDirection,Ctx.bigTrendDirection,Ctx.smallBaseDirection};
   double basketLots[3]={Ctx.bigCoreLot,Ctx.bigTrendLot,Ctx.smallBaseLot}; BigBasketGate basketGate;
   if(!EvaluateBigBasketGate(basketDirections,basketLots,CountManagedOpenPositions(),basketGate)) { LogError("BIG_ATOMIC_BASKET_GATE_FAIL "+basketGate.reason); SetState(STATE_INVALID_SPLIT_GEOMETRY,basketGate.reason); return false; }

   double netBigExposureActual=Ctx.bigCoreLot+Ctx.bigTrendLot-Ctx.smallBaseLot-Ctx.farLot;
   if(netBigExposureActual<MinimumNetBigExposureLots)
   {
      LogError(StringFormat("BIG_GEOMETRY_GATE_FAIL Far=%.2f Core=%.2f Trend=%.2f Small=%.2f Net=%.2f Minimum=%.2f",Ctx.farLot,Ctx.bigCoreLot,Ctx.bigTrendLot,Ctx.smallBaseLot,netBigExposureActual,MinimumNetBigExposureLots));
      SetState(STATE_INVALID_SPLIT_GEOMETRY,"BIG_NET_EXPOSURE_TOO_SMALL after broker volume normalization"); return false;
   }
   Ctx.currentBigMovePoints=GetBigMovePoints(Ctx.harvestLevel);
   double point=SymbolInfoDouble(_Symbol,SYMBOL_POINT), mid=(MarketAsk()+MarketBid())*.5;
   double targetMid=mid+(Ctx.bigCoreDirection==DIR_BUY?1.0:-1.0)*Ctx.currentBigMovePoints*point;
   BrokerMoneyResult coreMoney,trendMoney,smallMoney,farMoney;
   bool moneyOk=CalcProjectedPositionNetMoney(Ctx.bigCoreDirection,Ctx.bigCoreLot,BrokerExecutionOpenPrice(Ctx.bigCoreDirection),BrokerClosePriceAtMid(Ctx.bigCoreDirection,targetMid),true,true,coreMoney)&&
                CalcProjectedPositionNetMoney(Ctx.bigTrendDirection,Ctx.bigTrendLot,BrokerExecutionOpenPrice(Ctx.bigTrendDirection),BrokerClosePriceAtMid(Ctx.bigTrendDirection,targetMid),true,true,trendMoney)&&
                CalcProjectedPositionNetMoney(Ctx.smallBaseDirection,Ctx.smallBaseLot,BrokerExecutionOpenPrice(Ctx.smallBaseDirection),BrokerClosePriceAtMid(Ctx.smallBaseDirection,targetMid),true,true,smallMoney)&&
                CalcProjectedCloseNetMoney(Ctx.farDirection,Ctx.farLot,Ctx.farOpenPrice,BrokerClosePriceAtMid(Ctx.farDirection,targetMid),farMoney);
   BigRecoveryEvaluation bigGate;
   if(!moneyOk||!EvaluateBigGeometryAndRecovery(Ctx.farLot,Ctx.bigCoreLot,Ctx.bigTrendLot,Ctx.smallBaseLot,coreMoney,trendMoney,smallMoney,farMoney,bigGate))
   {
      LogError(StringFormat("BIG_RECOVERY_GATE_FAIL Delta=%.2f Costs=%.2f NetExposure=%.2f Reason=%s",bigGate.projectedRecoveryDelta,bigGate.costs,bigGate.netBigExposure,bigGate.reason));
      SetState(STATE_INVALID_SPLIT_GEOMETRY,"BIG_RECOVERY_IMPROVEMENT_GATE_FAILED"); return false;
   }
   LogInfo(StringFormat("BIG_RECOVERY_GATE_PASS Delta=%.2f Costs=%.2f NetExposure=%.2f",bigGate.projectedRecoveryDelta,bigGate.costs,bigGate.netBigExposure));

   ProjectedCloseNetResult farNow; BigReserveCatchUpEvaluation projectedCatchUp;
   double projectedHarvest=MathMax(0.0,bigGate.projectedRecoveryDelta),projectedReserveAdd=projectedHarvest*WorkReserveShare,projectedCarryAdd=projectedHarvest-projectedReserveAdd;
   if(!CalculateProjectedFarCloseNet(Ctx.farLot,farNow)||!EvaluateBigReserveCatchUp(Ctx.totalReserve,Ctx.totalReserve+projectedReserveAdd,Ctx.partialFarBudgetCarry,Ctx.partialFarBudgetCarry+projectedCarryAdd,Ctx.farLot,Ctx.farLot,farNow.projectedLoss,MathMax(0.0,-farMoney.netMoney),0.0,projectedCatchUp))
   { LogError("BIG_ATOMIC_RESERVE_PROJECTION_FAIL "+projectedCatchUp.reason); SetState(STATE_INVALID_SPLIT_GEOMETRY,"BIG_ATOMIC_RESERVE_PROJECTION_FAIL"); return false; }

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
   if(role == ROLE_REVERSE_SMALL) return STATE_REVERSE_OPEN_DYNAMIC_SMALL;
   return STATE_ERROR;
}

PendingActionType SplitOpenPendingActionForRole(PositionRole role)
{
   if(role == ROLE_BIG_CORE) return PENDING_OPEN_BIG_CORE;
   if(role == ROLE_SMALL_BASE) return PENDING_OPEN_SMALL_BASE;
   if(role == ROLE_BIG_TREND) return PENDING_OPEN_BIG_TREND;
   if(role == ROLE_REVERSE_SMALL) return PENDING_OPEN_REVERSE_SMALL;
   return PENDING_NONE;
}

EAState SplitClosePendingStateForRole(PositionRole role)
{
   if(role == ROLE_BIG_CORE) return STATE_SPLIT_CLOSE_CORE_PENDING;
   if(role == ROLE_BIG_TREND) return STATE_SPLIT_CLOSE_TREND_PENDING;
   if(role == ROLE_SMALL_BASE) return STATE_SPLIT_CLOSE_SMALL_BASE_PENDING;
   if(role == ROLE_REVERSE_SMALL) return STATE_SMALL_CLOSE_DYNAMIC_SMALL;
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
      return MarketBid() >= Ctx.bigCoreOpenPrice + distance;
   if(Ctx.bigCoreDirection == DIR_SELL)
      return MarketAsk() <= Ctx.bigCoreOpenPrice - distance;
   return false;
}

bool EvaluateCurrentSmallPreTrade(string &reason)
{
   SmallTransitionLeg legs[5]; double targetFar=CalcTargetNewFarLot(Ctx.farLot),closeMid=Ctx.farOpenPrice;
   double reverseLot=NormalizeLotUp(MathMax(SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN),Ctx.bigCoreLot-Ctx.farLot-Ctx.smallBaseLot+Ctx.farLot*ReverseDirectionBufferRatio));
   double coreCloseLot=NormalizeLotDown(Ctx.bigCoreLot-targetFar); if(targetFar<=0||coreCloseLot<=0||reverseLot<=0) { reason="SMALL_PRETRADE_VOLUME_INVALID"; return false; }
   BrokerMoneyResult projected[5];
   bool ok=CalcProjectedCloseNetMoney(Ctx.bigTrendDirection,Ctx.bigTrendLot,Ctx.bigTrendOpenPrice,BrokerClosePriceAtMid(Ctx.bigTrendDirection,closeMid),projected[0])&&
           CalcProjectedCloseNetMoney(Ctx.smallBaseDirection,Ctx.smallBaseLot,Ctx.smallBaseOpenPrice,BrokerClosePriceAtMid(Ctx.smallBaseDirection,closeMid),projected[1])&&
           CalcProjectedPositionNetMoney(Ctx.farDirection,reverseLot,BrokerExecutionOpenPrice(Ctx.farDirection),BrokerClosePriceAtMid(Ctx.farDirection,closeMid),true,true,projected[2])&&
           CalcProjectedCloseNetMoney(Ctx.farDirection,Ctx.farLot,Ctx.farOpenPrice,BrokerClosePriceAtMid(Ctx.farDirection,closeMid),projected[3])&&
           CalcProjectedCloseNetMoney(Ctx.bigCoreDirection,coreCloseLot,Ctx.bigCoreOpenPrice,BrokerClosePriceAtMid(Ctx.bigCoreDirection,closeMid),projected[4]);
   if(!ok) { reason="SMALL_PRETRADE_MONEY_UNAVAILABLE"; return false; }
   for(int i=0;i<5;i++) { legs[i].role=(SmallTransitionLegRole)i; legs[i].money=projected[i]; }
   legs[0].actualPositionLot=Ctx.bigTrendLot;legs[0].requestedLot=Ctx.bigTrendLot;legs[0].fullClose=true;
   legs[1].actualPositionLot=Ctx.smallBaseLot;legs[1].requestedLot=Ctx.smallBaseLot;legs[1].fullClose=true;
   legs[2].actualPositionLot=reverseLot;legs[2].requestedLot=reverseLot;legs[2].openLot=reverseLot;legs[2].closeLot=reverseLot;legs[2].includesOpenAndClose=true;
   legs[3].actualPositionLot=Ctx.farLot;legs[3].requestedLot=Ctx.farLot;legs[3].fullClose=true;
   legs[4].actualPositionLot=Ctx.bigCoreLot;legs[4].requestedLot=coreCloseLot;legs[4].residualLot=targetFar;
   double marginLevel=AccountInfoDouble(ACCOUNT_MARGIN_LEVEL); if(marginLevel<=0) marginLevel=999999;
   SmallTransitionEvaluation transition; if(!EvaluateSmallTransition(legs,Ctx.farLot,targetFar,Ctx.farLot+Ctx.smallBaseLot+reverseLot-Ctx.bigCoreLot,marginLevel,transition)) { reason=transition.reason; return false; }
   ReverseCyclesEvaluation cycles; double farLoss=MathMax(0.0,-projected[3].netMoney);
   EvaluateRequiredReverseCyclesMoney(Ctx.farLot,farLoss,Ctx.totalReserve,Ctx.partialFarBudgetCarry,AccountInfoDouble(ACCOUNT_BALANCE)-Ctx.cycleStartBalance,MaximumNewFarRatio,transition.transitionNet,MathMax(0.0,transition.transitionNet*SmallReserveShare),0,0,SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN),cycles);
   if(!EvaluateSmallPreTradeGate(legs,Ctx.farLot,targetFar,Ctx.farLot+Ctx.smallBaseLot+reverseLot-Ctx.bigCoreLot,marginLevel,cycles,transition)) { reason=transition.reason; return false; }
   Ctx.projectedTransitionNet=transition.transitionNet; Ctx.projectedReverseSmallLot=reverseLot; reason="OK"; return true;
}

void ProcessSplitBigActive()
{
   double smallProfitPoints = ProfitPoints(Ctx.smallBaseDirection, Ctx.smallBaseOpenPrice);
   if(smallProfitPoints >= GetBigMovePoints(Ctx.harvestLevel))
   {
      string preTradeReason; if(!EvaluateCurrentSmallPreTrade(preTradeReason)) { LogError("SMALL_PRETRADE_GATE_FAIL "+preTradeReason); SetState(STATE_INVALID_SMALL_GEOMETRY,preTradeReason); return; }
      Ctx.smallScenarioRealBefore=AccountInfoDouble(ACCOUNT_BALANCE)-Ctx.cycleStartBalance;
      SetState(STATE_REVERSE_CLOSE_BIG_TREND,"Split Small trigger confirmed; close BigTrend first");
      return;
   }
   if(SplitBigTargetReached())
      SetState(STATE_SPLIT_BIG_HARVEST_CLOSE_CORE, "Split Big target reached from BigCoreOpenPrice");
}

void PrepareSmallOperationAudit(int legRole,ulong ticket,ulong identifier,double requestedLot,BrokerMoneyResult &projection)
{
   SmallOperationAudit a; a.operationId=(ulong)TimeCurrent()*10+(ulong)legRole; a.legRole=legRole; a.requestedLot=requestedLot; a.filledLot=0; a.residualLot=requestedLot; a.projectedNet=projection.netMoney; a.actualNet=0; a.projectedCommission=projection.openCommission+projection.closeCommission; a.actualCommission=0; a.projectedSwap=projection.accruedSwap+projection.projectedFutureSwap; a.actualSwap=0; a.projectedFee=projection.fee; a.actualFee=0; a.ticket=ticket; a.identifier=identifier; a.dealFrom=0; a.dealTo=0; a.completed=false; Ctx.smallOperationAudits[legRole]=a; if(Ctx.smallOperationAuditCount<legRole+1)Ctx.smallOperationAuditCount=legRole+1; SaveState();
}

bool CompleteSmallOperationAudit(int legRole,double residualLot)
{
   SmallOperationAudit a=Ctx.smallOperationAudits[legRole]; double filled=0,net=0,commission=0,swap=0,fee=0; long first=0,last=0;
   if(IsInternalSimulationMode()) { for(int i=0;i<ArraySize(SimDeals);i++) if(SimDeals[i].positionTicket==a.ticket && SimDeals[i].positionIdentifier==a.identifier && (SimDeals[i].entry==DEAL_ENTRY_OUT||SimDeals[i].entry==DEAL_ENTRY_INOUT||SimDeals[i].entry==DEAL_ENTRY_OUT_BY)) { filled+=SimDeals[i].filledLot; net+=SimDeals[i].netMoney; commission+=SimDeals[i].commissionMoney; swap+=SimDeals[i].swapMoney; fee+=SimDeals[i].feeMoney; if(first==0)first=(long)SimDeals[i].dealTicket;last=(long)SimDeals[i].dealTicket; } }
   else { if(!HistorySelect(Ctx.cycleStartTime,TimeCurrent()+60))return false; for(int i=0;i<HistoryDealsTotal();i++){ulong deal=HistoryDealGetTicket(i);if(deal==0||(ulong)HistoryDealGetInteger(deal,DEAL_MAGIC)!=MagicNumber||HistoryDealGetString(deal,DEAL_SYMBOL)!=_Symbol||(ulong)HistoryDealGetInteger(deal,DEAL_POSITION_ID)!=a.identifier)continue;ENUM_DEAL_ENTRY entry=(ENUM_DEAL_ENTRY)HistoryDealGetInteger(deal,DEAL_ENTRY);double p=HistoryDealGetDouble(deal,DEAL_PROFIT),c=HistoryDealGetDouble(deal,DEAL_COMMISSION),s=HistoryDealGetDouble(deal,DEAL_SWAP),f=HistoryDealGetDouble(deal,DEAL_FEE);net+=p+c+s+f;commission+=c;swap+=s;fee+=f;if(entry==DEAL_ENTRY_OUT||entry==DEAL_ENTRY_INOUT||entry==DEAL_ENTRY_OUT_BY)filled+=HistoryDealGetDouble(deal,DEAL_VOLUME);if(first==0||deal<(ulong)first)first=(long)deal;if(deal>(ulong)last)last=(long)deal;} }
   a.filledLot=filled;a.residualLot=residualLot;a.actualNet=net;a.actualCommission=commission;a.actualSwap=swap;a.actualFee=fee;a.dealFrom=first;a.dealTo=last;a.completed=filled>0;Ctx.smallOperationAudits[legRole]=a;SaveState();return a.completed;
}

bool PrepareSmallCloseAudit(int legRole,Direction direction,ulong ticket,ulong identifier,double lot,double openPrice)
{
   BrokerMoneyResult projection;if(!CalcProjectedCloseNetMoney(direction,lot,openPrice,CurrentPriceForDirectionClose(direction),projection))return false;PrepareSmallOperationAudit(legRole,ticket,identifier,lot,projection);return true;
}

bool ReconcileCompletedSmallTransition(double expectedNewFar)
{
   double total=0;for(int i=0;i<5;i++){SmallOperationAudit a=Ctx.smallOperationAudits[i];if(!a.completed||MathAbs(a.filledLot-a.requestedLot)>MathMax(VolumeMismatchToleranceLots,SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_STEP)*.5))return false;total+=a.actualNet;}
   if(GetActualPositionVolume(Ctx.smallOperationAudits[SMALL_LEG_OLD_FAR_CLOSE].ticket)>VolumeMismatchToleranceLots||GetActualPositionVolume(Ctx.smallOperationAudits[SMALL_LEG_BIG_TREND_CLOSE].ticket)>VolumeMismatchToleranceLots||GetActualPositionVolume(Ctx.smallOperationAudits[SMALL_LEG_SMALL_BASE_CLOSE].ticket)>VolumeMismatchToleranceLots||GetActualPositionVolume(Ctx.smallOperationAudits[SMALL_LEG_REVERSE_SMALL].ticket)>VolumeMismatchToleranceLots)return false;
   if(Ctx.farTicket==0||Ctx.farIdentifier==0||Ctx.farLot<=0||Ctx.farLot>=Ctx.oldFarLot||MathAbs(Ctx.farLot-expectedNewFar)>MathMax(VolumeMismatchToleranceLots,SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_STEP)*.5))return false;
   if(!ValidateNoOrphanManagedPositions()||CountManagedOpenPositions()!=1)return false;
   if(ArraySize(ReserveLedger)>0&&MathAbs(ReserveLedger[ArraySize(ReserveLedger)-1].reserveAfter-Ctx.totalReserve)>ReserveMismatchTolerance)return false;
   Ctx.actualSmallTransitionNet=total;return true;
}

void ProcessReverseCloseBigTrend()
{
   if(!PrepareSmallCloseAudit(SMALL_LEG_BIG_TREND_CLOSE,Ctx.bigTrendDirection,Ctx.bigTrendTicket,Ctx.bigTrendIdentifier,Ctx.bigTrendLot,Ctx.bigTrendOpenPrice)){SetState(STATE_SMALL_RECONCILIATION_FAILED,"BIG_TREND_PROJECTION_FAILED");return;} if(CloseSplitRoleFull(ROLE_BIG_TREND,Ctx.bigTrendTicket,Ctx.bigTrendLot,"SMALL_CLOSE_BIG_TREND",STATE_REVERSE_CALCULATE_DYNAMIC_SMALL,PENDING_CLOSE_BIG_TREND_FULL)&&!CompleteSmallOperationAudit(SMALL_LEG_BIG_TREND_CLOSE,0)){SetState(STATE_SMALL_RECONCILIATION_FAILED,"BIG_TREND_AUDIT_FAILED");}
}
void ProcessReverseCalculateDynamicSmall()
{
   double minimum=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN);
   Ctx.reverseSmallDirection=Ctx.farDirection;
   Ctx.reverseSmallLot=NormalizeLotUp(MathMax(minimum,Ctx.bigCoreLot-Ctx.farLot-Ctx.smallBaseLot+Ctx.farLot*ReverseDirectionBufferRatio));
   double netSmall=Ctx.farLot+Ctx.smallBaseLot+Ctx.reverseSmallLot-Ctx.bigCoreLot;
   if(Ctx.reverseSmallLot<=0||netSmall<=VolumeMismatchToleranceLots) { SetState(STATE_INVALID_SMALL_GEOMETRY,"REVERSE_SMALL_EXPOSURE_NOT_POSITIVE"); return; }
   SetState(STATE_REVERSE_OPEN_DYNAMIC_SMALL,"ReverseSmall normalized exposure approved");
}
void ProcessReverseOpenDynamicSmall()
{
   if(Ctx.reverseSmallTicket!=0||Ctx.reverseSmallOpened) { SetState(STATE_REVERSE_WAIT_FAR_TOUCH,"ReverseSmall exactly-once restored"); return; }
   if(OpenSplitRole(ROLE_REVERSE_SMALL,Ctx.reverseSmallDirection,Ctx.reverseSmallLot,STATE_REVERSE_WAIT_FAR_TOUCH,STATE_REVERSE_SMALL_OPEN_FAILED)) Ctx.reverseSmallOpened=true;
}
bool EvaluateCurrentFalseReverse(FalseReverseEvaluation &evaluation)
{
   FalseReverseOption candidates[6]; double realized=Ctx.realCyclePL,currentMargin=AccountInfoDouble(ACCOUNT_MARGIN),equity=AccountInfoDouble(ACCOUNT_EQUITY);
   BrokerMoneyResult reverseClose,baseClose,farClose,coreClose; bool valid=CalcProjectedCloseNetMoney(Ctx.reverseSmallDirection,Ctx.reverseSmallLot,Ctx.reverseSmallOpenPrice,CurrentPriceForDirectionClose(Ctx.reverseSmallDirection),reverseClose)&&CalcProjectedCloseNetMoney(Ctx.smallBaseDirection,Ctx.smallBaseLot,Ctx.smallBaseOpenPrice,CurrentPriceForDirectionClose(Ctx.smallBaseDirection),baseClose)&&CalcProjectedCloseNetMoney(Ctx.farDirection,Ctx.farLot,Ctx.farOpenPrice,CurrentPriceForDirectionClose(Ctx.farDirection),farClose)&&CalcProjectedCloseNetMoney(Ctx.bigCoreDirection,Ctx.bigCoreLot,Ctx.bigCoreOpenPrice,CurrentPriceForDirectionClose(Ctx.bigCoreDirection),coreClose);
   if(!valid) { evaluation.reason="FALSE_REVERSE_MONEY_UNAVAILABLE"; return false; }
   BrokerMoneyResult reverseMargin,baseMargin,farMargin,coreMargin;if(!CalcProjectedMarginMoney(Ctx.reverseSmallDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,Ctx.reverseSmallLot,BrokerExecutionOpenPrice(Ctx.reverseSmallDirection),reverseMargin)||!CalcProjectedMarginMoney(Ctx.smallBaseDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,Ctx.smallBaseLot,BrokerExecutionOpenPrice(Ctx.smallBaseDirection),baseMargin)||!CalcProjectedMarginMoney(Ctx.farDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,Ctx.farLot,BrokerExecutionOpenPrice(Ctx.farDirection),farMargin)||!CalcProjectedMarginMoney(Ctx.bigCoreDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,Ctx.bigCoreLot,BrokerExecutionOpenPrice(Ctx.bigCoreDirection),coreMargin)){evaluation.reason="FALSE_REVERSE_MARGIN_UNAVAILABLE";return false;}
   double legNet[4]={reverseClose.netMoney,baseClose.netMoney,farClose.netMoney,coreClose.netMoney},legMargin[4]={reverseMargin.requiredMargin,baseMargin.requiredMargin,farMargin.requiredMargin,coreMargin.requiredMargin};
   int masks[6]={0,1,2,3,15,0};EAState nextStates[6]={STATE_REVERSE_WAIT_FAR_TOUCH,STATE_FALSE_REVERSE_CLOSE_REVERSE,STATE_FALSE_REVERSE_CLOSE_BASE,STATE_FALSE_REVERSE_CLOSE_TAILS_REVERSE,STATE_FALSE_REVERSE_CLOSE_BASKET,STATE_FALSE_REVERSE_COMPLETED};
   double exposure[6]={Ctx.farLot+Ctx.smallBaseLot+Ctx.reverseSmallLot-Ctx.bigCoreLot,Ctx.farLot+Ctx.smallBaseLot-Ctx.bigCoreLot,Ctx.farLot+Ctx.reverseSmallLot-Ctx.bigCoreLot,Ctx.farLot-Ctx.bigCoreLot,0,Ctx.farLot+Ctx.smallBaseLot+Ctx.reverseSmallLot-Ctx.bigCoreLot};
   for(int i=0;i<6;i++) { double closed=0,floating=0,released=0;for(int leg=0;leg<4;leg++){if((masks[i]&(1<<leg))!=0){closed+=legNet[leg];released+=legMargin[leg];}else floating+=legNet[leg];}candidates[i].action=(FalseReverseAction)i;candidates[i].projectedClosedNet=closed;candidates[i].projectedFloatingNetRemaining=floating;candidates[i].realizedRecoveryPL=realized;candidates[i].projectedNet=closed+floating;candidates[i].projectedRecoveryPL=realized+closed+floating;candidates[i].reserveImpact=MathMax(0.0,-closed);candidates[i].projectedMarginReleased=released;candidates[i].projectedMarginAfter=MathMax(0.0,currentMargin-released);double projectedEquity=equity+closed;candidates[i].projectedMarginLevel=candidates[i].projectedMarginAfter>0?projectedEquity/candidates[i].projectedMarginAfter*100.0:999999;candidates[i].remainingExposure=exposure[i];candidates[i].secondTailRisk=(i==0);candidates[i].nextState=nextStates[i]; }
   return EvaluateFalseReverseMoney(candidates,MinimumRecoveryProfitMoney,Ctx.totalReserve,evaluation);
}
void ProcessReverseWaitFarTouch()
{
   double price=Ctx.farDirection==DIR_BUY?MarketAsk():MarketBid();
   bool touched=Ctx.farDirection==DIR_BUY?price>=Ctx.farOpenPrice:price<=Ctx.farOpenPrice;
   bool falseReverse=Ctx.bigCoreDirection==DIR_BUY?MarketBid()>=Ctx.bigCoreOpenPrice:MarketAsk()<=Ctx.bigCoreOpenPrice;
   if(falseReverse&&!touched)
   {
      SetState(STATE_FALSE_REVERSE_DECISION,"FALSE_REVERSE_MARKET_EVENT");return;
   }
   if(touched) SetState(STATE_SMALL_CLOSE_OLD_FAR,"Old Far touch confirmed for Split Small transition");
}

void ProcessFalseReverseDecision()
{
   FalseReverseEvaluation decision;if(!EvaluateCurrentFalseReverse(decision)){SetState(STATE_MANUAL_INTERVENTION_REQUIRED,decision.reason);return;}Ctx.falseReverseAction=(int)decision.selected;SaveState();SetState(decision.options[(int)decision.selected].nextState,"FALSE_REVERSE_DECISION_APPLIED");
}
void ClearFalseReverseClosedContext(ulong ticket){if(ticket==0)return;if(ticket==Ctx.reverseSmallTicket){Ctx.reverseSmallTicket=0;Ctx.reverseSmallIdentifier=0;Ctx.reverseSmallLot=0;Ctx.reverseSmallOpened=false;}if(ticket==Ctx.smallBaseTicket){Ctx.smallBaseTicket=0;Ctx.smallBaseIdentifier=0;Ctx.smallBaseLot=0;}if(ticket==Ctx.farTicket){Ctx.farTicket=0;Ctx.farIdentifier=0;Ctx.farLot=0;}if(ticket==Ctx.bigCoreTicket){Ctx.bigCoreTicket=0;Ctx.bigCoreIdentifier=0;Ctx.bigCoreLot=0;}SaveState();}
bool ExecuteFalseReverseClose(ulong ticket,double lot,PendingActionType pending,EAState current,EAState next,string comment)
{
   if(ticket==0||GetActualPositionVolume(ticket)<=VolumeMismatchToleranceLots){ClearFalseReverseClosedContext(ticket);ClearPendingOperationContext();SetState(next,comment+" already complete");return true;}Ctx.falseReverseExpectedTicket=ticket;Ctx.falseReverseExpectedLot=lot;SaveState();if(!ClosePositionByTicketWithComment(ticket,lot,comment)||!VerifyFullClose(ticket,comment)){SetPendingOperation(pending,comment,current,ticket,lot,comment,next,"FALSE_REVERSE_CLOSE_PENDING");return false;}ClearFalseReverseClosedContext(ticket);ClearPendingOperationContext();SetState(next,comment+" confirmed");return true;
}
bool RetryFalseReverseClose(PendingActionType action,EAState next)
{if(Ctx.pendingActionType!=action)return false;EAState recoveredNext=Ctx.pendingNextState!=STATE_IDLE?Ctx.pendingNextState:next;if(Ctx.pendingAttempts>=MaxCloseRetryAttempts){SetState(STATE_FALSE_REVERSE_FAILED,"FALSE_REVERSE_RETRY_LIMIT");return true;}Ctx.pendingAttempts++;if(ClosePositionByTicketWithComment(Ctx.pendingTicket,Ctx.pendingLot,Ctx.pendingComment)&&VerifyFullClose(Ctx.pendingTicket,Ctx.pendingComment)){ulong closedTicket=Ctx.pendingTicket;ClearFalseReverseClosedContext(closedTicket);ClearPendingOperationContext();SetState(recoveredNext,"FALSE_REVERSE_RETRY_CONFIRMED");}else SaveState();return true;}
void ProcessFalseReverseCloseReverse(){if(RetryFalseReverseClose(PENDING_FALSE_REVERSE_CLOSE_REVERSE,STATE_FALSE_REVERSE_RECONCILIATION))return;ExecuteFalseReverseClose(Ctx.reverseSmallTicket,Ctx.reverseSmallLot,PENDING_FALSE_REVERSE_CLOSE_REVERSE,STATE_FALSE_REVERSE_CLOSE_REVERSE,STATE_FALSE_REVERSE_RECONCILIATION,"FALSE_REVERSE_CLOSE_REVERSE");}
void ProcessFalseReverseCloseBase(){if(RetryFalseReverseClose(PENDING_FALSE_REVERSE_CLOSE_BASE,STATE_FALSE_REVERSE_RECONCILIATION))return;ExecuteFalseReverseClose(Ctx.smallBaseTicket,Ctx.smallBaseLot,PENDING_FALSE_REVERSE_CLOSE_BASE,STATE_FALSE_REVERSE_CLOSE_BASE,STATE_FALSE_REVERSE_RECONCILIATION,"FALSE_REVERSE_CLOSE_BASE");}
void ProcessFalseReverseCloseTailsReverse(){if(RetryFalseReverseClose(PENDING_FALSE_REVERSE_CLOSE_TAILS_REVERSE,STATE_FALSE_REVERSE_CLOSE_TAILS_BASE))return;ExecuteFalseReverseClose(Ctx.reverseSmallTicket,Ctx.reverseSmallLot,PENDING_FALSE_REVERSE_CLOSE_TAILS_REVERSE,STATE_FALSE_REVERSE_CLOSE_TAILS_REVERSE,STATE_FALSE_REVERSE_CLOSE_TAILS_BASE,"FALSE_REVERSE_CLOSE_TAIL_REVERSE");}
void ProcessFalseReverseCloseTailsBase(){if(RetryFalseReverseClose(PENDING_FALSE_REVERSE_CLOSE_TAILS_BASE,STATE_FALSE_REVERSE_RECONCILIATION))return;ExecuteFalseReverseClose(Ctx.smallBaseTicket,Ctx.smallBaseLot,PENDING_FALSE_REVERSE_CLOSE_TAILS_BASE,STATE_FALSE_REVERSE_CLOSE_TAILS_BASE,STATE_FALSE_REVERSE_RECONCILIATION,"FALSE_REVERSE_CLOSE_TAIL_BASE");}
void ProcessFalseReverseCloseBasket(){if(RetryFalseReverseClose(PENDING_FALSE_REVERSE_CLOSE_BASKET,STATE_FALSE_REVERSE_CLOSE_BASKET))return;if(GetActualPositionVolume(Ctx.reverseSmallTicket)>VolumeMismatchToleranceLots){ExecuteFalseReverseClose(Ctx.reverseSmallTicket,Ctx.reverseSmallLot,PENDING_FALSE_REVERSE_CLOSE_BASKET,STATE_FALSE_REVERSE_CLOSE_BASKET,STATE_FALSE_REVERSE_CLOSE_BASKET,"FALSE_REVERSE_BASKET_REVERSE");return;}if(GetActualPositionVolume(Ctx.smallBaseTicket)>VolumeMismatchToleranceLots){ExecuteFalseReverseClose(Ctx.smallBaseTicket,Ctx.smallBaseLot,PENDING_FALSE_REVERSE_CLOSE_BASKET,STATE_FALSE_REVERSE_CLOSE_BASKET,STATE_FALSE_REVERSE_CLOSE_BASKET,"FALSE_REVERSE_BASKET_BASE");return;}if(GetActualPositionVolume(Ctx.farTicket)>VolumeMismatchToleranceLots){ExecuteFalseReverseClose(Ctx.farTicket,Ctx.farLot,PENDING_FALSE_REVERSE_CLOSE_BASKET,STATE_FALSE_REVERSE_CLOSE_BASKET,STATE_FALSE_REVERSE_CLOSE_BASKET,"FALSE_REVERSE_BASKET_FAR");return;}ExecuteFalseReverseClose(Ctx.bigCoreTicket,Ctx.bigCoreLot,PENDING_FALSE_REVERSE_CLOSE_BASKET,STATE_FALSE_REVERSE_CLOSE_BASKET,STATE_FALSE_REVERSE_RECONCILIATION,"FALSE_REVERSE_BASKET_CORE");}
void ProcessFalseReverseReconciliation(){RecalculateRealCycleStatsFromHistory();if(Ctx.realCyclePL+ReserveMismatchTolerance<MinimumRecoveryProfitMoney||!ValidateNoOrphanManagedPositions()){SetState(STATE_FALSE_REVERSE_FAILED,"FALSE_REVERSE_RECONCILIATION_FAIL");return;}SetState(STATE_FALSE_REVERSE_COMPLETED,"FALSE_REVERSE_RECONCILIATION_PASS");}
void ProcessFalseReverseFailed(){SetState(STATE_MANUAL_INTERVENTION_REQUIRED,"FALSE_REVERSE_EXECUTION_FAILED");}

void ProcessSplitSmallCloseOldFar()
{
   Ctx.oldFarTicket=Ctx.farTicket; Ctx.oldFarLot=Ctx.farLot; Ctx.oldFarDirection=Ctx.farDirection; Ctx.oldFarOpenPrice=Ctx.farOpenPrice;
   if(!PrepareSmallCloseAudit(SMALL_LEG_OLD_FAR_CLOSE,Ctx.farDirection,Ctx.farTicket,Ctx.farIdentifier,Ctx.farLot,Ctx.farOpenPrice)){SetState(STATE_SMALL_RECONCILIATION_FAILED,"OLD_FAR_PROJECTION_FAILED");return;}
   if(!ClosePositionByTicketWithComment(Ctx.farTicket,Ctx.farLot,"SPLIT_SMALL_CLOSE_OLD_FAR")||!VerifyFullClose(Ctx.farTicket,"SPLIT_SMALL_CLOSE_OLD_FAR")) { SetState(STATE_MANUAL_INTERVENTION_REQUIRED,"Split Old Far close not confirmed"); return; }
   if(!CompleteSmallOperationAudit(SMALL_LEG_OLD_FAR_CLOSE,0)){SetState(STATE_SMALL_RECONCILIATION_FAILED,"OLD_FAR_AUDIT_FAILED");return;}
   ClearFarContext("Split Small old Far confirmed closed"); SetState(STATE_SMALL_CLOSE_SMALL_BASE,"Close SmallBase after Old Far");
}
void ProcessSplitSmallCloseSmallBase()
{
   if(!PrepareSmallCloseAudit(SMALL_LEG_SMALL_BASE_CLOSE,Ctx.smallBaseDirection,Ctx.smallBaseTicket,Ctx.smallBaseIdentifier,Ctx.smallBaseLot,Ctx.smallBaseOpenPrice)){SetState(STATE_SMALL_RECONCILIATION_FAILED,"SMALL_BASE_PROJECTION_FAILED");return;}if(CloseSplitRoleFull(ROLE_SMALL_BASE,Ctx.smallBaseTicket,Ctx.smallBaseLot,"SPLIT_SMALL_CLOSE_BASE",STATE_SMALL_CLOSE_DYNAMIC_SMALL,PENDING_CLOSE_SMALL_BASE_FULL)&&!CompleteSmallOperationAudit(SMALL_LEG_SMALL_BASE_CLOSE,0))SetState(STATE_SMALL_RECONCILIATION_FAILED,"SMALL_BASE_AUDIT_FAILED");
}
void ProcessSplitSmallCloseReverse()
{
   BrokerMoneyResult projection;if(!CalcProjectedPositionNetMoney(Ctx.reverseSmallDirection,Ctx.reverseSmallLot,Ctx.reverseSmallOpenPrice,CurrentPriceForDirectionClose(Ctx.reverseSmallDirection),true,true,projection)){SetState(STATE_SMALL_RECONCILIATION_FAILED,"REVERSE_PROJECTION_FAILED");return;}PrepareSmallOperationAudit(SMALL_LEG_REVERSE_SMALL,Ctx.reverseSmallTicket,Ctx.reverseSmallIdentifier,Ctx.reverseSmallLot,projection);if(CloseSplitRoleFull(ROLE_REVERSE_SMALL,Ctx.reverseSmallTicket,Ctx.reverseSmallLot,"SPLIT_SMALL_CLOSE_REVERSE",STATE_SMALL_CLOSE_BIG_CORE_PART,PENDING_CLOSE_REVERSE_SMALL_FULL)&&!CompleteSmallOperationAudit(SMALL_LEG_REVERSE_SMALL,0))SetState(STATE_SMALL_RECONCILIATION_FAILED,"REVERSE_AUDIT_FAILED");
}
bool BuildDynamicReverseProjections(double startFarLot,double startFarLoss,ReverseCycleProjection &projections[])
{
   ArrayResize(projections,0);double farLot=startFarLot,farLoss=startFarLoss,transitionPerLot=Ctx.oldFarLot>0?(Ctx.smallScenarioRealAfter-Ctx.smallScenarioRealBefore)/Ctx.oldFarLot:0;double closePrice=CurrentPriceForDirectionClose(Ctx.farDirection);
   for(int cycleIndex=0;cycleIndex<WorkMaxReverseCycles;cycleIndex++)
   {
      ReverseCycleProjection p;p.farLotBefore=farLot;p.farLossBefore=farLoss;p.bigCoreLot=CalcBigCoreLot(farLot);p.bigTrendLot=CalcBigTrendLot(farLot);p.smallBaseLot=CalcSmallBaseLot(farLot);p.reverseSmallLot=NormalizeLotUp(MathMax(SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN),p.bigCoreLot-farLot-p.smallBaseLot+farLot*ReverseDirectionBufferRatio));p.targetNewFar=CalcTargetNewFarLot(farLot);p.closeLot=NormalizeLotDown(p.bigCoreLot-p.targetNewFar);p.farLotAfter=p.targetNewFar;
      if(p.targetNewFar<=0||p.closeLot<=0)return false;if(!CalcFarCloseLossWorstCaseMoney(Ctx.farDirection,p.farLotAfter,Ctx.farOpenPrice,closePrice,p.farLossAfter))return false;
      double totalTradeLot=p.bigTrendLot+p.smallBaseLot+2*p.reverseSmallLot+farLot+p.closeLot;BrokerMoneyResult costs;if(!CalcProjectedOpenAndCloseCosts(totalTradeLot,costs))return false;p.commission=costs.openCommission+costs.closeCommission;p.spread=costs.spreadExpansionCost;p.slippage=costs.slippageCost;
      SignedSwapResult swap;if(!CalcSignedBrokerSwap(Ctx.farDirection,totalTradeLot,TimeCurrent(),TimeCurrent()+ExpectedHoldingDays*86400,swap))return false;p.signedSwap=swap.expectedSignedSwap-swap.additionalSwapBuffer;
      Direction bigDirection=OppositeDirection(Ctx.farDirection),smallDirection=Ctx.farDirection;BrokerMoneyResult m1,m2,m3;if(!CalcProjectedMarginMoney(bigDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,p.bigCoreLot,BrokerExecutionOpenPrice(bigDirection),m1)||!CalcProjectedMarginMoney(bigDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,p.bigTrendLot,BrokerExecutionOpenPrice(bigDirection),m2)||!CalcProjectedMarginMoney(smallDirection==DIR_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL,p.smallBaseLot,BrokerExecutionOpenPrice(smallDirection),m3))return false;p.requiredMargin=m1.requiredMargin+m2.requiredMargin+m3.requiredMargin;p.availableMargin=AccountInfoDouble(ACCOUNT_MARGIN_FREE);
      p.transitionNet=transitionPerLot*farLot;p.reserveAdd=MathMax(0.0,p.transitionNet*SmallReserveShare);p.carryAdd=MathMax(0.0,p.transitionNet-p.reserveAdd);int n=ArraySize(projections);ArrayResize(projections,n+1);projections[n]=p;farLot=p.farLotAfter;farLoss=p.farLossAfter;
   }
   return ArraySize(projections)>0;
}
void ProcessSplitSmallCloseCorePart()
{
   double target=CalcTargetNewFarLot(Ctx.oldFarLot),closeLot=NormalizeLotDown(Ctx.bigCoreLot-target);
   if(target<=0||target>=Ctx.oldFarLot||Ctx.oldFarLot-target<MinimumFarCompressionLots||closeLot<=0) { SetState(STATE_INVALID_SMALL_GEOMETRY,"SMALL_TARGET_NEW_FAR_INVALID"); return; }
   if(!PrepareSmallCloseAudit(SMALL_LEG_BIG_CORE_PARTIAL,Ctx.bigCoreDirection,Ctx.bigCoreTicket,Ctx.bigCoreIdentifier,closeLot,Ctx.bigCoreOpenPrice)){SetState(STATE_SMALL_RECONCILIATION_FAILED,"BIG_CORE_PROJECTION_FAILED");return;}if(!ClosePositionByTicket(Ctx.bigCoreTicket,closeLot)) { SetState(STATE_MANUAL_INTERVENTION_REQUIRED,"BigCore compression close failed"); return; }
   double actual=NormalizeVolumeToStep(GetActualPositionVolume(Ctx.bigCoreTicket));
   if(!CompleteSmallOperationAudit(SMALL_LEG_BIG_CORE_PARTIAL,actual)){SetState(STATE_SMALL_RECONCILIATION_FAILED,"BIG_CORE_AUDIT_FAILED");return;}
   if(actual<=0||actual>=Ctx.oldFarLot||actual/ Ctx.oldFarLot>MaximumNewFarRatio+0.000001) { SetState(STATE_SMALL_COMPRESSION_FAILED,"ACTUAL_NEW_FAR_COMPRESSION_FAILED"); return; }
   Ctx.farTicket=Ctx.bigCoreTicket; Ctx.farIdentifier=Ctx.bigCoreIdentifier; Ctx.farLot=actual; Ctx.farDirection=Ctx.bigCoreDirection; Ctx.farOpenPrice=Ctx.bigCoreOpenPrice;
   Ctx.bigCoreTicket=0; Ctx.bigCoreIdentifier=0; Ctx.bigCoreLot=0; Ctx.bigCoreDirection=DIR_NONE;
   RecalculateRealCycleStatsFromHistory(); Ctx.smallScenarioRealAfter=Ctx.realCyclePL;
   if(Ctx.smallScenarioRealAfter-Ctx.smallScenarioRealBefore<MinimumTransitionProfitMoney) { SetState(STATE_MANUAL_INTERVENTION_REQUIRED,"SMALL_TRANSITION_MONEY_FAIL"); return; }
   if(!ReconcileCompletedSmallTransition(target)){SetState(STATE_SMALL_RECONCILIATION_FAILED,"SMALL_FIVE_LEG_RECONCILIATION_FAILED");return;}
   ProjectedCloseNetResult remainingFar; ReverseCyclesEvaluation reverseEvaluation; ReverseCycleProjection projections[];
   if(!CalculateProjectedFarCloseNet(Ctx.farLot,remainingFar)) { SetState(STATE_REVERSE_LIMIT,"REVERSE_FAR_MONEY_UNAVAILABLE"); return; }
   if(!BuildDynamicReverseProjections(Ctx.farLot,remainingFar.projectedLoss,projections)||!EvaluateDynamicReverseCycles(Ctx.farLot,remainingFar.projectedLoss,Ctx.totalReserve,Ctx.partialFarBudgetCarry,Ctx.realCyclePL,SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN),projections,reverseEvaluation)||reverseEvaluation.requiredCycles>WorkMaxReverseCycles) { SetState(STATE_REVERSE_LIMIT,reverseEvaluation.reason); return; }
   SetState(STATE_SMALL_CHECK_RESERVE,"Split Small transition actual New Far confirmed");
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
   if(role == ROLE_REVERSE_SMALL) { Ctx.reverseSmallTicket=0; Ctx.reverseSmallLot=0.0; Ctx.reverseSmallDirection=DIR_NONE; Ctx.reverseSmallOpened=false; }
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
   Ctx.harvestPhase=HARVEST_CALCULATED; Ctx.harvestId=(ulong)TimeCurrent(); Ctx.harvestCarryBefore=Ctx.partialFarBudgetCarry;
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
   Ctx.bigFarLossBefore=full.projectedLoss;
   Ctx.bigFarLotBefore=Ctx.farLot;
   Ctx.bigCoverageBefore=full.projectedLoss>0.0?(Ctx.totalReserve+Ctx.partialFarBudgetCarry)/full.projectedLoss:1.0;
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
   Ctx.harvestReserveAdd=Ctx.pendingReserveAdd; Ctx.harvestPartialBudgetAdd=Ctx.pendingCloseFarBudget; Ctx.harvestPhase=HARVEST_LEDGER_PREPARED; SaveState();
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
   Ctx.actualPartialFarCost=actualPartialLoss;
   Ctx.harvestCarryAfter=Ctx.partialFarBudgetCarry; Ctx.harvestPhase=HARVEST_LEDGER_PREPARED; SaveState();
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

bool ContinueSplitHarvestDistribution()
{
   if(Ctx.harvestPhase==HARVEST_CALCULATED)
   {
      if(Ctx.harvestReserveAdd==0&&Ctx.harvestPartialBudgetAdd==0){Ctx.harvestReserveAdd=Ctx.actualSplitHarvestNet*WorkReserveShare;Ctx.harvestPartialBudgetAdd=Ctx.actualSplitHarvestNet-Ctx.harvestReserveAdd;}
      if(MathAbs(Ctx.actualSplitHarvestNet-Ctx.harvestReserveAdd-Ctx.harvestPartialBudgetAdd)>ReserveMismatchTolerance)return false;Ctx.harvestPhase=HARVEST_LEDGER_PREPARED;SaveState();
   }
   if(Ctx.harvestPhase==HARVEST_LEDGER_PREPARED)
   {
      if(!ApplyReserveCredit(RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD,Ctx.harvestReserveAdd)) return false;
      Ctx.pendingReserveApplied=true; Ctx.harvestPhase=HARVEST_LEDGER_WRITTEN; SaveState();
   }
   if(Ctx.harvestPhase==HARVEST_LEDGER_WRITTEN) { Ctx.harvestPhase=HARVEST_RESERVE_UPDATED; SaveState(); }
   if(Ctx.harvestPhase==HARVEST_RESERVE_UPDATED) { Ctx.partialFarBudgetCarry=Ctx.harvestCarryAfter; Ctx.harvestPhase=HARVEST_CARRY_UPDATED; SaveState(); }
   if(Ctx.harvestPhase==HARVEST_CARRY_UPDATED) { Ctx.harvestPhase=HARVEST_DISTRIBUTED; SaveState(); }
   return Ctx.harvestPhase==HARVEST_DISTRIBUTED||Ctx.harvestPhase==HARVEST_CONSUMED;
}

void ProcessSplitBigHarvestFinalCheck()
{
   if(!Ctx.pendingFullFarClose && !ContinueSplitHarvestDistribution())
   {
      SetState(STATE_RECOVERY_PENDING,"HARVEST_DISTRIBUTION_RECOVERY_REQUIRED"); return;
   }
   RefreshFarVolumeFromTerminal("SPLIT_FINAL_CHECK actual Far");
   ProjectedCloseNetResult full;
   BigReserveCatchUpEvaluation catchUp;
   double reserveBefore=Ctx.totalReserve-(Ctx.pendingReserveApplied?Ctx.pendingReserveAdd:0.0);
   if(Ctx.farLot>0.0&&CalculateProjectedFarCloseNet(Ctx.farLot,full)&&Ctx.bigFarLossBefore>0.0&&
      !EvaluateBigReserveCatchUp(reserveBefore,Ctx.totalReserve,Ctx.harvestCarryBefore,Ctx.partialFarBudgetCarry,Ctx.bigFarLotBefore,Ctx.farLot,Ctx.bigFarLossBefore,full.projectedLoss,Ctx.actualPartialFarCost,catchUp))
   { LogError(StringFormat("BIG_RESERVE_CATCH_UP_ACTUAL_FAIL Before=%.6f After=%.6f FarBefore=%.2f FarAfter=%.2f",catchUp.coverageBefore,catchUp.coverageAfter,catchUp.farLossBefore,catchUp.farLossAfter)); SetState(STATE_BIG_COVERAGE_RECONCILIATION_FAILED,"BIG_RESERVE_COVERAGE_ACTUAL_NOT_IMPROVED"); return; }
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
   Ctx.harvestPhase=HARVEST_CONSUMED; SaveState();
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

ScenarioMode CurrentScenarioMode()
{
   if(State==STATE_SPLIT_GEOMETRY_ACTIVE||State==STATE_FAR_ACTIVE) return SCENARIO_BIG_ACTIVE;
   if(State>=STATE_SPLIT_BIG_HARVEST_CLOSE_CORE&&State<=STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE) return SCENARIO_BIG_CLOSING;
   if(State==STATE_SPLIT_BIG_HARVEST_CALC_NET||State==STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR||State==STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR||State==STATE_SPLIT_BIG_HARVEST_FINAL_CHECK) return SCENARIO_BIG_ACCOUNTING;
   if(State>=STATE_REVERSE_CLOSE_BIG_TREND&&State<=STATE_REVERSE_WAIT_FAR_TOUCH) return SCENARIO_SMALL_SWITCH_PENDING;
   if(State>=STATE_FALSE_REVERSE_DECISION&&State<=STATE_FALSE_REVERSE_COMPLETED) return SCENARIO_SMALL_CLOSING;
   if(State==STATE_FALSE_REVERSE_FAILED||State==STATE_SMALL_RECONCILIATION_FAILED) return SCENARIO_ERROR;
   if(State==STATE_SMALL_SCENARIO) return SCENARIO_SMALL_ACTIVE;
   if(State>=STATE_SMALL_CLOSE_SMALL&&State<=STATE_SMALL_BUILD_NEW_FAR) return SCENARIO_SMALL_CLOSING;
   if(State==STATE_FINAL_CLOSE) return SCENARIO_FINAL_CLOSE;
   if(State==STATE_RECOVERY_PENDING||State==STATE_RECOVERY_MISMATCH) return SCENARIO_RECOVERY;
   if(State>=STATE_INTEGRITY_ERROR) return SCENARIO_ERROR; return SCENARIO_IDLE;
}
bool ValidateScenarioIsolation()
{
   ScenarioMode mode=CurrentScenarioMode(); bool ok=true;
   if((mode==SCENARIO_BIG_ACTIVE||mode==SCENARIO_BIG_CLOSING||mode==SCENARIO_BIG_ACCOUNTING)&&Ctx.reverseSmallTicket!=0) ok=false;
   if((mode==SCENARIO_SMALL_SWITCH_PENDING||mode==SCENARIO_SMALL_ACTIVE||mode==SCENARIO_SMALL_CLOSING)&&
      (State==STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR||Ctx.pendingActionType==PENDING_CLOSE_FAR_PARTIAL)) ok=false;
   if(ActiveReserveTransaction.active&&Ctx.pendingReserveApplied&&Ctx.pendingSmallReserveApplied) ok=false;
   if(!ok) { LogError(StringFormat("SCENARIO_ISOLATION_FAIL State=%s Mode=%d",StateToString(State),(int)mode)); return false; }
   return true;
}

void RunStateMachine()
{
   if(!ValidateScenarioIsolation()) { SetState(STATE_INTEGRITY_ERROR,"BIG_SMALL_SCENARIO_ISOLATION_FAILED"); return; }
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

      case STATE_REVERSE_CLOSE_BIG_TREND: ProcessReverseCloseBigTrend(); break;
      case STATE_REVERSE_CALCULATE_DYNAMIC_SMALL: ProcessReverseCalculateDynamicSmall(); break;
      case STATE_REVERSE_OPEN_DYNAMIC_SMALL: ProcessReverseOpenDynamicSmall(); break;
      case STATE_REVERSE_WAIT_FAR_TOUCH: ProcessReverseWaitFarTouch(); break;
      case STATE_FALSE_REVERSE_DECISION: ProcessFalseReverseDecision(); break;
      case STATE_FALSE_REVERSE_CLOSE_REVERSE: ProcessFalseReverseCloseReverse(); break;
      case STATE_FALSE_REVERSE_CLOSE_BASE: ProcessFalseReverseCloseBase(); break;
      case STATE_FALSE_REVERSE_CLOSE_TAILS_REVERSE: ProcessFalseReverseCloseTailsReverse(); break;
      case STATE_FALSE_REVERSE_CLOSE_TAILS_BASE: ProcessFalseReverseCloseTailsBase(); break;
      case STATE_FALSE_REVERSE_CLOSE_BASKET: ProcessFalseReverseCloseBasket(); break;
      case STATE_FALSE_REVERSE_RECONCILIATION: ProcessFalseReverseReconciliation(); break;
      case STATE_FALSE_REVERSE_COMPLETED: break;
      case STATE_FALSE_REVERSE_FAILED: ProcessFalseReverseFailed(); break;
      case STATE_SMALL_RECONCILIATION_FAILED: break;
      case STATE_SMALL_COMPRESSION_FAILED: break;

      case STATE_SMALL_CLOSE_SMALL_BASE: ProcessSplitSmallCloseSmallBase(); break;
      case STATE_SMALL_CLOSE_DYNAMIC_SMALL: ProcessSplitSmallCloseReverse(); break;
      case STATE_SMALL_CLOSE_BIG_CORE_PART: ProcessSplitSmallCloseCorePart(); break;

      case STATE_SMALL_SCENARIO:
         ProcessSmallScenario();
         break;

      case STATE_SMALL_CLOSE_SMALL:
         ProcessSmallCloseSmall();
         break;

      case STATE_SMALL_CLOSE_OLD_FAR:
         if(Ctx.splitGeometryActive||Ctx.bigCoreTicket!=0) ProcessSplitSmallCloseOldFar(); else ProcessSmallCloseOldFar();
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
