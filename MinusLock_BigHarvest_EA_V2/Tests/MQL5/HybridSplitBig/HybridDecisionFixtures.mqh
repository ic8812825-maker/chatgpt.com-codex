#ifndef __BH_HYBRID_DECISION_FIXTURES_MQH__
#define __BH_HYBRID_DECISION_FIXTURES_MQH__

void BuildHybridDefaultSnapshot(HybridCycleSnapshot &s)
{
   ZeroMemory(s);
   s.symbol=_Symbol;
   s.magic=MagicNumber;
   s.cycleId=1;
   s.snapshotTime=TimeCurrent();
   s.stateRevision=1;
   s.positionFingerprint=1001;
   s.farDirection=DIR_BUY;
   s.farLot=1.0;
   s.farOpenPrice=1.10000;
   s.farIdentifier=101;
   s.coreDirection=DIR_SELL;
   s.coreLot=0;
   s.coreOpenPrice=1.10000;
   s.coreIdentifier=0;
   s.trendDirection=DIR_SELL;
   s.trendLot=0;
   s.trendOpenPrice=1.10000;
   s.trendIdentifier=0;
   s.smallDirection=DIR_BUY;
   s.smallLot=0;
   s.smallOpenPrice=1.10000;
   s.smallIdentifier=0;
   s.realizedCyclePL=0;
   s.finalReserveReal=0;
   s.partialFarAvailable=0;
   s.transitionAvailable=1000;
   s.cumulativeTransitionLoss=0;
   s.bid=MarketBid()>0?MarketBid():1.09990;
   s.ask=MarketAsk()>0?MarketAsk():1.10010;
   s.equity=ModelAccountEquity()>0?ModelAccountEquity():10000;
   s.margin=ModelAccountMargin();
   s.freeMargin=ModelAccountFreeMargin()>0?ModelAccountFreeMargin():9000;
}

#endif // __BH_HYBRID_DECISION_FIXTURES_MQH__
