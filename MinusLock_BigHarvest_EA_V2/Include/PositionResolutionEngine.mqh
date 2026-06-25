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
         ticket == Ctx.pendingTicket || ticket == Ctx.retryTicket)
         return true;
   }

   if(identifier != 0)
   {
      if(identifier == Ctx.farIdentifier || identifier == Ctx.bigIdentifier || identifier == Ctx.smallIdentifier ||
         identifier == Ctx.initialBuyIdentifier || identifier == Ctx.initialSellIdentifier ||
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
   return ok;
}

#endif // __BH_POSITIONRESOLUTIONENGINE_MQH__
