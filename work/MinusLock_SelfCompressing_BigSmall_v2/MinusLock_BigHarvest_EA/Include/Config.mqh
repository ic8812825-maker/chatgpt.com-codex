#ifndef __BH_CONFIG_MQH__
#define __BH_CONFIG_MQH__

input double StartLot              = 1.00;
input double BigRatio              = 1.30;
input double SmallRatio            = 0.37;
input double CloseBigOnSmall       = 0.30;
input double RemainBigOnSmall      = 0.70;
input double CloseFarShare         = 0.90;
input double ReserveShare          = 0.10;

input int    InitialTriggerPoints  = 100;
input int    BigMoveLevel1         = 100;
input int    BigMoveLevel2         = 150;
input int    BigMoveLevel3         = 200;

input int    FarDistancePoints     = 200;
input int    MaxHarvestLevels      = 3;

input double LotStep               = 0.01;
input double MaxSpreadPoints       = 30;
input double MaxMarginPercent      = 70.0;

input ulong  MagicNumber           = 20260609;
input bool   AllowRealTrading      = false;
input bool   UseMarketOrders       = true;

#endif // __BH_CONFIG_MQH__
