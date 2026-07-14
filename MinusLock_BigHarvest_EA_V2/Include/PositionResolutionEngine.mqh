#ifndef __BH_POSITIONRESOLUTIONENGINE_MQH__
#define __BH_POSITIONRESOLUTIONENGINE_MQH__

// V2.4.20 Position Resolution Architecture.
// OpenPosition success is not enough: a new leg is registered only after ticket,
// identifier, lot, type, open price and open time are resolved from MT5.

void ResetPositionResolutionResult(PositionResolutionResult &result)
{
   ZeroMemory(result);
   result.resolved = false;
   result.ticket = 0;
   result.identifier = 0;
   result.lot = 0.0;
   result.type = POSITION_TYPE_BUY;
   result.openPrice = 0.0;
   result.openTime = 0;
}

bool ResolutionResultFromSnapshot(PositionSnapshot &snapshot, datetime openTime, PositionResolutionResult &result)
{
   ResetPositionResolutionResult(result);
   result.resolved = snapshot.exists && snapshot.ticket != 0 && snapshot.identifier != 0 && snapshot.lot > VolumeMismatchToleranceLots;
   result.ticket = snapshot.ticket;
   result.identifier = snapshot.identifier;
   result.lot = NormalizeVolumeToStep(snapshot.lot);
   result.type = (snapshot.direction == DIR_BUY ? POSITION_TYPE_BUY : POSITION_TYPE_SELL);
   result.openPrice = snapshot.openPrice;
   result.openTime = openTime;
   return result.resolved;
}

bool PositionResolutionLotMatches(double actualLot, double expectedLot)
{
   double actual = NormalizeVolumeToStep(actualLot);
   double expected = NormalizeVolumeToStep(expectedLot);
   return expected <= 0.0 || MathAbs(actual - expected) <= VolumeMismatchToleranceLots;
}

bool PositionResolutionDirectionMatches(Direction actualDirection, Direction expectedDirection)
{
   return expectedDirection == DIR_NONE || actualDirection == expectedDirection;
}

bool IsKnownContextTicketOrIdentifier(ulong ticket, ulong identifier)
{
   if(ticket != 0)
   {
      if(ticket == Ctx.farTicket || ticket == Ctx.bigTicket || ticket == Ctx.smallTicket ||
         ticket == Ctx.initialBuyTicket || ticket == Ctx.initialSellTicket ||
         ticket == Ctx.bigCoreTicket || ticket == Ctx.bigTrendTicket || ticket == Ctx.smallBaseTicket ||
         ticket == Ctx.pendingTicket || ticket == Ctx.retryTicket)
         return true;
   }

   if(identifier != 0)
   {
      if(identifier == Ctx.farIdentifier || identifier == Ctx.bigIdentifier || identifier == Ctx.smallIdentifier ||
         identifier == Ctx.initialBuyIdentifier || identifier == Ctx.initialSellIdentifier ||
         identifier == Ctx.bigCoreIdentifier || identifier == Ctx.bigTrendIdentifier || identifier == Ctx.smallBaseIdentifier ||
         identifier == Ctx.pendingBigPositionId || identifier == Ctx.pendingSmallPositionId)
         return true;
   }

   return false;
}

bool ReadSelectedPositionResolution(PositionResolutionResult &result)
{
   PositionSnapshot snapshot;
   if(!ReadSelectedPosition(snapshot))
      return false;

   return ResolutionResultFromSnapshot(snapshot, (datetime)PositionGetInteger(POSITION_TIME), result);
}

bool ResolveOpenedPosition(string comment,
                           Direction direction,
                           double expectedLot,
                           ulong knownIdentifier,
                           datetime openStartTime,
                           PositionResolutionResult &result)
{
   ResetPositionResolutionResult(result);
   LogInfo(StringFormat("POSITION_RESOLUTION_START Comment=%s Direction=%s ExpectedLot=%.2f KnownIdentifier=%I64u OpenStartTime=%I64d WindowSeconds=%d",
                        comment,
                        DirectionToString(direction),
                        expectedLot,
                        knownIdentifier,
                        (long)openStartTime,
                        PositionResolutionLookbackSeconds));

   // Level 1: broker-preserved comment + MagicNumber + Symbol through GetManagedPositionByComment().
   PositionSnapshot byComment;
   if(comment != "" && GetManagedPositionByComment(comment, byComment))
   {
      PositionResolutionResult byCommentResult;
      if(ResolutionResultFromSnapshot(byComment, TimeCurrent(), byCommentResult) &&
         PositionResolutionDirectionMatches(byComment.direction, direction) &&
         PositionResolutionLotMatches(byComment.lot, expectedLot))
      {
         result = byCommentResult;
         LogInfo(StringFormat("POSITION_RESOLUTION_BY_COMMENT Ticket=%I64u Identifier=%I64u Lot=%.2f Comment=%s", result.ticket, result.identifier, result.lot, comment));
         LogInfo(StringFormat("POSITION_RESOLUTION_PASS Ticket=%I64u Identifier=%I64u Lot=%.2f", result.ticket, result.identifier, result.lot));
         return true;
      }
   }

   if(IsInternalSimulationMode())
   {
      LogError(StringFormat("POSITION_RESOLUTION_FAIL Comment=%s Reason=simulation_comment_lookup_failed", comment));
      return false;
   }

   // Level 2: strict operation time window + direction + lot + MagicNumber + Symbol.
   datetime maxOpenTime = (openStartTime > 0 ? openStartTime + PositionResolutionLookbackSeconds : TimeCurrent());
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;

      PositionSnapshot candidate;
      if(!ReadSelectedPosition(candidate))
         continue;

      datetime positionTime = (datetime)PositionGetInteger(POSITION_TIME);
      bool inWindow = (openStartTime <= 0 || (positionTime >= openStartTime && positionTime <= maxOpenTime));
      if(inWindow && PositionResolutionDirectionMatches(candidate.direction, direction) && PositionResolutionLotMatches(candidate.lot, expectedLot))
      {
         ResolutionResultFromSnapshot(candidate, positionTime, result);
         LogInfo(StringFormat("POSITION_RESOLUTION_BY_TIME Ticket=%I64u Identifier=%I64u Lot=%.2f OpenTime=%I64d", result.ticket, result.identifier, result.lot, (long)positionTime));
         LogInfo(StringFormat("POSITION_RESOLUTION_PASS Ticket=%I64u Identifier=%I64u Lot=%.2f", result.ticket, result.identifier, result.lot));
         return true;
      }
   }

   // Level 3: explicit POSITION_IDENTIFIER if the caller already knows it.
   if(knownIdentifier != 0)
   {
      for(int i = PositionsTotal() - 1; i >= 0; i--)
      {
         ulong ticket = PositionGetTicket(i);
         if(ticket == 0 || !PositionSelectByTicket(ticket))
            continue;

         PositionSnapshot candidate;
         if(!ReadSelectedPosition(candidate))
            continue;

         if(candidate.identifier == knownIdentifier)
         {
            ResolutionResultFromSnapshot(candidate, (datetime)PositionGetInteger(POSITION_TIME), result);
            LogInfo(StringFormat("POSITION_RESOLUTION_BY_IDENTIFIER Ticket=%I64u Identifier=%I64u Lot=%.2f", result.ticket, result.identifier, result.lot));
            LogInfo(StringFormat("POSITION_RESOLUTION_PASS Ticket=%I64u Identifier=%I64u Lot=%.2f", result.ticket, result.identifier, result.lot));
            return true;
         }
      }
   }

   // Level 4: non-ambiguous fallback by Magic/Symbol/direction/lot, excluding already known context.
   int matches = 0;
   PositionResolutionResult fallback;
   ResetPositionResolutionResult(fallback);
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;

      PositionSnapshot candidate;
      if(!ReadSelectedPosition(candidate))
         continue;
      if(IsKnownContextTicketOrIdentifier(candidate.ticket, candidate.identifier))
         continue;
      if(!PositionResolutionDirectionMatches(candidate.direction, direction) || !PositionResolutionLotMatches(candidate.lot, expectedLot))
         continue;

      matches++;
      ResolutionResultFromSnapshot(candidate, (datetime)PositionGetInteger(POSITION_TIME), fallback);
   }

   if(matches == 1 && fallback.resolved)
   {
      result = fallback;
      LogInfo(StringFormat("POSITION_RESOLUTION_BY_MAGIC Ticket=%I64u Identifier=%I64u Lot=%.2f Direction=%s", result.ticket, result.identifier, result.lot, DirectionToString(PositionTypeToDirection((long)result.type))));
      LogInfo(StringFormat("POSITION_RESOLUTION_PASS Ticket=%I64u Identifier=%I64u Lot=%.2f", result.ticket, result.identifier, result.lot));
      return true;
   }
   if(matches > 1)
      LogError(StringFormat("POSITION_RESOLUTION_FAIL ambiguous fallback matches=%d Comment=%s", matches, comment));

   LogError(StringFormat("POSITION_RESOLUTION_FAIL Comment=%s Direction=%s ExpectedLot=%.2f KnownIdentifier=%I64u", comment, DirectionToString(direction), expectedLot, knownIdentifier));
   return false;
}

bool ResolveOpenedPositionAfterOpen(string comment,
                                    Direction direction,
                                    double expectedLot,
                                    ulong knownIdentifier,
                                    datetime openStartTime,
                                    PositionResolutionResult &result)
{
   return ResolveOpenedPosition(comment, direction, expectedLot, knownIdentifier, openStartTime, result);
}

bool ApplyResolvedPositionToBig(PositionResolutionResult &result)
{
   if(!result.resolved || result.ticket == 0 || result.identifier == 0 || result.lot <= VolumeMismatchToleranceLots)
   {
      LogError("POSITION_RESOLUTION_FAILED Big leg could not be registered with ticket/identifier/lot");
      SetState(STATE_POSITION_RESOLUTION_ERROR, "POSITION_RESOLUTION_FAILED Big");
      return false;
   }

   Ctx.bigTicket = result.ticket;
   Ctx.bigIdentifier = result.identifier;
   Ctx.bigLot = result.lot;
   Ctx.bigOpenPrice = result.openPrice;
   Ctx.bigDirection = PositionTypeToDirection((long)result.type);
   SaveState();
   return true;
}

bool ApplyResolvedPositionToSmall(PositionResolutionResult &result)
{
   if(!result.resolved || result.ticket == 0 || result.identifier == 0 || result.lot <= VolumeMismatchToleranceLots)
   {
      LogError("POSITION_RESOLUTION_FAILED Small leg could not be registered with ticket/identifier/lot");
      SetState(STATE_POSITION_RESOLUTION_ERROR, "POSITION_RESOLUTION_FAILED Small");
      return false;
   }

   Ctx.smallTicket = result.ticket;
   Ctx.smallIdentifier = result.identifier;
   Ctx.smallLot = result.lot;
   Ctx.smallOpenPrice = result.openPrice;
   Ctx.smallDirection = PositionTypeToDirection((long)result.type);
   SaveState();
   return true;
}


bool ResolveSplitRolePosition(PositionRole role,
                              ulong &ticket,
                              ulong &identifier,
                              double &lot,
                              Direction &direction,
                              double &openPrice,
                              datetime openStartTime)
{
   string roleCode = PositionRoleToCode(role);
   string expectedComment = BuildRoleComment(role, (long)Ctx.cycleId, Ctx.harvestLevel, Ctx.reverseCycleCount);
   PositionResolutionResult result;
   ResetPositionResolutionResult(result);
   LogInfo(StringFormat("SPLIT_POSITION_RESOLUTION Start Role=%s Symbol=%s MagicNumber=%I64u CycleId=%I64u Level=%d Ticket=%I64u Identifier=%I64u ExpectedLot=%.2f ExpectedDirection=%s Comment=%s",
                        roleCode, _Symbol, MagicNumber, Ctx.cycleId, Ctx.harvestLevel, ticket, identifier, lot, DirectionToString(direction), expectedComment));

   // 1. Saved ticket.
   if(ticket != 0 && PositionSelectByTicket(ticket))
   {
      PositionSnapshot snapshot;
      if(ReadSelectedPosition(snapshot) &&
         (identifier == 0 || snapshot.identifier == identifier) &&
         PositionResolutionDirectionMatches(snapshot.direction, direction) &&
         PositionResolutionLotMatches(snapshot.lot, lot))
      {
         ResolutionResultFromSnapshot(snapshot, (datetime)PositionGetInteger(POSITION_TIME), result);
      }
   }

   // 2. POSITION_IDENTIFIER.
   if(!result.resolved && identifier != 0)
   {
      for(int i = PositionsTotal() - 1; i >= 0; i--)
      {
         ulong candidateTicket = PositionGetTicket(i);
         if(candidateTicket == 0 || !PositionSelectByTicket(candidateTicket))
            continue;
         PositionSnapshot snapshot;
         if(!ReadSelectedPosition(snapshot))
            continue;
         if(snapshot.identifier == identifier && PositionResolutionDirectionMatches(snapshot.direction, direction) && PositionResolutionLotMatches(snapshot.lot, lot))
         {
            ResolutionResultFromSnapshot(snapshot, (datetime)PositionGetInteger(POSITION_TIME), result);
            break;
         }
      }
   }

   // 3. Role comment + CycleId + Level, then still validate direction/volume.
   if(!result.resolved && expectedComment != "")
   {
      PositionSnapshot byComment;
      if(GetManagedPositionByComment(expectedComment, byComment) &&
         PositionResolutionDirectionMatches(byComment.direction, direction) &&
         PositionResolutionLotMatches(byComment.lot, lot))
      {
         ResolutionResultFromSnapshot(byComment, TimeCurrent(), result);
      }
   }

   // 4. Direction + volume + open time fallback.
   if(!result.resolved)
   {
      datetime maxOpenTime = (openStartTime > 0 ? openStartTime + PositionResolutionLookbackSeconds : TimeCurrent());
      int matches = 0;
      PositionResolutionResult fallback;
      ResetPositionResolutionResult(fallback);
      for(int i = PositionsTotal() - 1; i >= 0; i--)
      {
         ulong candidateTicket = PositionGetTicket(i);
         if(candidateTicket == 0 || !PositionSelectByTicket(candidateTicket))
            continue;
         PositionSnapshot snapshot;
         if(!ReadSelectedPosition(snapshot))
            continue;
         datetime positionTime = (datetime)PositionGetInteger(POSITION_TIME);
         bool inWindow = (openStartTime <= 0 || (positionTime >= openStartTime && positionTime <= maxOpenTime));
         if(inWindow && PositionResolutionDirectionMatches(snapshot.direction, direction) && PositionResolutionLotMatches(snapshot.lot, lot) && !IsKnownContextTicketOrIdentifier(snapshot.ticket, snapshot.identifier))
         {
            matches++;
            ResolutionResultFromSnapshot(snapshot, positionTime, fallback);
         }
      }
      if(matches == 1)
         result = fallback;
      else if(matches > 1)
         LogError(StringFormat("SPLIT_POSITION_RESOLUTION Result=FAIL Role=%s StopReason=ambiguous_fallback Matches=%d", roleCode, matches));
   }

   if(!result.resolved)
   {
      LogError(StringFormat("SPLIT_POSITION_RESOLUTION Result=FAIL Role=%s StopReason=not_found", roleCode));
      return false;
   }

   ticket = result.ticket;
   identifier = result.identifier;
   lot = NormalizeVolumeToStep(result.lot);
   direction = PositionTypeToDirection((long)result.type);
   openPrice = result.openPrice;
   LogInfo(StringFormat("SPLIT_POSITION_RESOLUTION Result=PASS Role=%s Ticket=%I64u Identifier=%I64u Lot=%.2f Direction=%s OpenPrice=%.5f", roleCode, ticket, identifier, lot, DirectionToString(direction), openPrice));
   SaveState();
   return true;
}

bool ResolveBigCorePosition()
{
   return ResolveSplitRolePosition(ROLE_BIG_CORE, Ctx.bigCoreTicket, Ctx.bigCoreIdentifier, Ctx.bigCoreLot, Ctx.bigCoreDirection, Ctx.bigCoreOpenPrice, Ctx.pendingOperationStartTime);
}

bool ResolveBigTrendPosition()
{
   return ResolveSplitRolePosition(ROLE_BIG_TREND, Ctx.bigTrendTicket, Ctx.bigTrendIdentifier, Ctx.bigTrendLot, Ctx.bigTrendDirection, Ctx.bigTrendOpenPrice, Ctx.pendingOperationStartTime);
}

bool ResolveSmallBasePosition()
{
   return ResolveSplitRolePosition(ROLE_SMALL_BASE, Ctx.smallBaseTicket, Ctx.smallBaseIdentifier, Ctx.smallBaseLot, Ctx.smallBaseDirection, Ctx.smallBaseOpenPrice, Ctx.pendingOperationStartTime);
}

bool ValidateSplitPositionResolutionContext()
{
   bool ok = true;
   if((Ctx.bigCoreTicket != 0 || Ctx.bigCoreIdentifier != 0 || Ctx.bigCoreLot > VolumeMismatchToleranceLots || Ctx.bigCoreDirection != DIR_NONE) && (Ctx.bigCoreTicket == 0 || Ctx.bigCoreIdentifier == 0 || Ctx.bigCoreLot <= VolumeMismatchToleranceLots))
   {
      LogError(StringFormat("SPLIT_POSITION_RESOLUTION Result=FAIL Role=BC Ticket=%I64u Identifier=%I64u Lot=%.2f", Ctx.bigCoreTicket, Ctx.bigCoreIdentifier, Ctx.bigCoreLot));
      ok = false;
   }
   if((Ctx.bigTrendTicket != 0 || Ctx.bigTrendIdentifier != 0 || Ctx.bigTrendLot > VolumeMismatchToleranceLots || Ctx.bigTrendDirection != DIR_NONE) && (Ctx.bigTrendTicket == 0 || Ctx.bigTrendIdentifier == 0 || Ctx.bigTrendLot <= VolumeMismatchToleranceLots))
   {
      LogError(StringFormat("SPLIT_POSITION_RESOLUTION Result=FAIL Role=BT Ticket=%I64u Identifier=%I64u Lot=%.2f", Ctx.bigTrendTicket, Ctx.bigTrendIdentifier, Ctx.bigTrendLot));
      ok = false;
   }
   if((Ctx.smallBaseTicket != 0 || Ctx.smallBaseIdentifier != 0 || Ctx.smallBaseLot > VolumeMismatchToleranceLots || Ctx.smallBaseDirection != DIR_NONE) && (Ctx.smallBaseTicket == 0 || Ctx.smallBaseIdentifier == 0 || Ctx.smallBaseLot <= VolumeMismatchToleranceLots))
   {
      LogError(StringFormat("SPLIT_POSITION_RESOLUTION Result=FAIL Role=SB Ticket=%I64u Identifier=%I64u Lot=%.2f", Ctx.smallBaseTicket, Ctx.smallBaseIdentifier, Ctx.smallBaseLot));
      ok = false;
   }
   return ok;
}

bool ValidatePositionResolutionContext()
{
   bool ok = true;
   if(HasBigContext() && (Ctx.bigTicket == 0 || Ctx.bigIdentifier == 0 || Ctx.bigLot <= VolumeMismatchToleranceLots))
   {
      LogError(StringFormat("POSITION_RESOLUTION_FAILED Big context unresolved Ticket=%I64u Identifier=%I64u Lot=%.2f", Ctx.bigTicket, Ctx.bigIdentifier, Ctx.bigLot));
      ok = false;
   }
   if(HasSmallContext() && (Ctx.smallTicket == 0 || Ctx.smallIdentifier == 0 || Ctx.smallLot <= VolumeMismatchToleranceLots))
   {
      LogError(StringFormat("POSITION_RESOLUTION_FAILED Small context unresolved Ticket=%I64u Identifier=%I64u Lot=%.2f", Ctx.smallTicket, Ctx.smallIdentifier, Ctx.smallLot));
      ok = false;
   }
   ok = ValidateSplitPositionResolutionContext() && ok;
   return ok;
}

#endif // __BH_POSITIONRESOLUTIONENGINE_MQH__
