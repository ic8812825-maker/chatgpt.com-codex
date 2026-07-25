#ifndef __HYBRID_CATCHUP_TEMPORAL_FIXTURES_MQH__
#define __HYBRID_CATCHUP_TEMPORAL_FIXTURES_MQH__

struct HybridCatchUpTemporalFixture { string id; string purpose; };
int BuildHybridCatchUpTemporalFixtures(HybridCatchUpTemporalFixture &rows[])
{
   ArrayResize(rows,47);
   rows[0].id="FT-01"; rows[0].purpose="first P0 to P1";
   rows[1].id="FT-02"; rows[1].purpose="second P1 to P2";
   rows[2].id="FT-03"; rows[2].purpose="third excludes P0";
   rows[3].id="FT-04"; rows[3].purpose="no projected close twice";
   rows[4].id="FT-05"; rows[4].purpose="disjoint cumulative harvest";
   rows[5].id="FT-06"; rows[5].purpose="remove level exact delta";
   rows[6].id="FT-07"; rows[6].purpose="partial credit";
   rows[7].id="FT-08"; rows[7].purpose="partial loss realized";
   rows[8].id="FT-09"; rows[8].purpose="partial reduces Far";
   rows[9].id="FT-10"; rows[9].purpose="budget carry";
   rows[10].id="FT-11"; rows[10].purpose="no FinalReserve source";
   rows[11].id="FT-12"; rows[11].purpose="invalid residual forbidden";
   rows[12].id="FT-13"; rows[12].purpose="adjust close for residual";
   rows[13].id="FT-14"; rows[13].purpose="full Far routes Final";
   rows[14].id="FT-15"; rows[14].purpose="remaining Far recalculated";
   rows[15].id="FT-16"; rows[15].purpose="next Core from residual";
   rows[16].id="FT-17"; rows[16].purpose="next Trend from residual";
   rows[17].id="FT-18"; rows[17].purpose="next Small from residual";
   rows[18].id="FT-19"; rows[18].purpose="Core Trend DOWN";
   rows[19].id="FT-20"; rows[19].purpose="Small UP";
   rows[20].id="FT-21"; rows[20].purpose="reopen at current level";
   rows[21].id="FT-22"; rows[21].purpose="trigger from new anchor";
   rows[22].id="FT-23"; rows[22].purpose="allocation conservation";
   rows[23].id="FT-24"; rows[23].purpose="partial budget conservation";
   rows[24].id="FT-25"; rows[24].purpose="PartialFar once";
   rows[25].id="FT-26"; rows[25].purpose="open commission once";
   rows[26].id="FT-27"; rows[26].purpose="close commission each close";
   rows[27].id="FT-28"; rows[27].purpose="no Reserve double count";
   rows[28].id="FT-29"; rows[28].purpose="negative Harvest no credit";
   rows[29].id="FT-30"; rows[29].purpose="Base Worst fingerprints";
   rows[30].id="FT-31"; rows[30].purpose="Worst partial independent";
   rows[31].id="FT-32"; rows[31].purpose="Worst Far independent";
   rows[32].id="FT-33"; rows[32].purpose="Base pass Worst fail";
   rows[33].id="FT-34"; rows[33].purpose="Worst not improve";
   rows[34].id="FT-35"; rows[34].purpose="margin released";
   rows[35].id="FT-36"; rows[35].purpose="steady includes basket";
   rows[36].id="FT-37"; rows[36].purpose="peak order";
   rows[37].id="FT-38"; rows[37].purpose="overlap separate";
   rows[38].id="FT-39"; rows[38].purpose="Far BUY";
   rows[39].id="FT-40"; rows[39].purpose="Far SELL mirror";
   rows[40].id="FT-41"; rows[40].purpose="BUY closes Bid";
   rows[41].id="FT-42"; rows[41].purpose="SELL closes Ask";
   rows[42].id="FT-43"; rows[42].purpose="no fixed snapshot component open";
   rows[43].id="FT-44"; rows[43].purpose="no fixed snapshot Far";
   rows[44].id="FT-45"; rows[44].purpose="StateAfter feeds next";
   rows[45].id="FT-46"; rows[45].purpose="no projectedHarvest accumulation";
   rows[46].id="FT-47"; rows[46].purpose="no execution integration";
   return ArraySize(rows);
}

#endif
