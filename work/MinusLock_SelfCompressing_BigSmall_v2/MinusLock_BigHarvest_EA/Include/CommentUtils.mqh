#ifndef __BH_COMMENTUTILS_MQH__
#define __BH_COMMENTUTILS_MQH__

string FormatMLComment(string role, int level, string direction, double lot, string action, double pl = 0.0)
{
   string comment = StringFormat("ML|%s|L=%d", role, level);
   if(direction != "")
      comment += StringFormat("|DIR=%s", direction);
   if(lot >= 0.0)
      comment += StringFormat("|LOT=%.2f", lot);
   if(pl != 0.0)
      comment += StringFormat("|PL=%.2f", pl);
   comment += StringFormat("|M=%I64u", MagicNumber);
   if(action != "")
      comment += StringFormat("|ACT=%s", action);
   if(StringLen(comment) > 31)
      comment = StringSubstr(comment, 0, 31);
   return comment;
}

bool ValidateComment(string comment)
{
   if(StringLen(comment) <= 0 || StringLen(comment) > 31)
      return false;
   if(StringFind(comment, "ML|") != 0)
      return false;
   if(StringFind(comment, "|L=") < 0)
      return false;
   if(StringFind(comment, "|M=") < 0)
      return false;
   return true;
}

string CommentInitialBuy() { return FormatMLComment("INIT_BUY", 0, "BUY", StartLot, "OPEN"); }
string CommentInitialSell() { return FormatMLComment("INIT_SELL", 0, "SELL", StartLot, "OPEN"); }
string CommentFar(int level, string direction, double lot) { return FormatMLComment("FAR", level, direction, lot, "OPEN"); }
string CommentBig(int level, string direction, double lot) { return FormatMLComment("BIG", level, direction, lot, "OPEN"); }
string CommentSmall(int level, string direction, double lot) { return FormatMLComment("SMALL", level, direction, lot, "OPEN"); }
string CommentCloseInitialPlus(int level, double lot, double profit) { return FormatMLComment("CLOSE_INIT", level, "", lot, "CLOSE", profit); }
string CommentCloseBig(int level, double lot) { return FormatMLComment("CLOSE_BIG", level, "", lot, "CLOSE"); }
string CommentCloseSmall(int level, double lot) { return FormatMLComment("CLOSE_SMALL", level, "", lot, "CLOSE"); }
string CommentCloseFarPartial(int level, double lot) { return FormatMLComment("CLOSE_FAR", level, "", lot, "CLOSE"); }
string CommentFinalClose(int level, double lot, double realRecoveryPL) { return FormatMLComment("FINAL", level, "", lot, "CLOSE", realRecoveryPL); }
string CommentClosedProfit(int level, double lot, double realRecoveryPL) { return FormatMLComment("CLOSED_PROFIT", level, "", lot, "CLOSE", realRecoveryPL); }
string CommentStopMaxLevels(int level, double lot) { return FormatMLComment("STOP_MAX", level, "", lot, "STOP"); }
string CommentInvalidReverseGeometry(int level) { return FormatMLComment("INV_REV", level, "", -1.0, "STOP"); }
string CommentInvalidSmallGeometry(int level) { return FormatMLComment("INV_SMALL", level, "", -1.0, "STOP"); }
string CommentReverseLimit(int level) { return FormatMLComment("REV_LIMIT", level, "", -1.0, "STOP"); }

#endif // __BH_COMMENTUTILS_MQH__
