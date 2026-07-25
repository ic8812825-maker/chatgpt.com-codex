#ifndef __HYBRID_CATCHUP_FIXTURES_MQH__
#define __HYBRID_CATCHUP_FIXTURES_MQH__

// Scenario catalogue consumed by the administrator-side MQL5 runner. Values that
// depend on broker tick value/commission are asserted against the returned rows.
struct HybridCatchUpFixture
{
   string id;
   string purpose;
   Direction farDirection;
   int expectedFiniteLevel; // -1 means no PASS under the fixture's broker profile
   bool expectPass;
};

int BuildHybridCatchUpFixtures(HybridCatchUpFixture &rows[])
{
   ArrayResize(rows,11);
   rows[0].id="FC-01"; rows[0].purpose="coverage level 1"; rows[0].farDirection=DIR_BUY; rows[0].expectedFiniteLevel=1; rows[0].expectPass=true;
   rows[1].id="FC-02"; rows[1].purpose="coverage level 2"; rows[1].farDirection=DIR_BUY; rows[1].expectedFiniteLevel=2; rows[1].expectPass=true;
   rows[2].id="FC-03"; rows[2].purpose="coverage level N"; rows[2].farDirection=DIR_BUY; rows[2].expectedFiniteLevel=3; rows[2].expectPass=true;
   rows[3].id="FC-04"; rows[3].purpose="no coverage"; rows[3].farDirection=DIR_BUY; rows[3].expectedFiniteLevel=-1; rows[3].expectPass=false;
   rows[4].id="FC-05"; rows[4].purpose="RecoveryPL fail"; rows[4].farDirection=DIR_BUY; rows[4].expectedFiniteLevel=-1; rows[4].expectPass=false;
   rows[5].id="FC-06"; rows[5].purpose="margin fail"; rows[5].farDirection=DIR_BUY; rows[5].expectedFiniteLevel=-1; rows[5].expectPass=false;
   rows[6].id="FC-07"; rows[6].purpose="Worst Case fail"; rows[6].farDirection=DIR_BUY; rows[6].expectedFiniteLevel=-1; rows[6].expectPass=false;
   rows[7].id="FC-08"; rows[7].purpose="BUY/SELL symmetry"; rows[7].farDirection=DIR_SELL; rows[7].expectedFiniteLevel=3; rows[7].expectPass=true;
   rows[8].id="FC-09"; rows[8].purpose="spread shock changes finite level"; rows[8].farDirection=DIR_BUY; rows[8].expectedFiniteLevel=4; rows[8].expectPass=true;
   rows[9].id="FC-10"; rows[9].purpose="commission shock changes finite level"; rows[9].farDirection=DIR_BUY; rows[9].expectedFiniteLevel=4; rows[9].expectPass=true;
   rows[10].id="FC-11"; rows[10].purpose="allocation and monotonic invariants"; rows[10].farDirection=DIR_BUY; rows[10].expectedFiniteLevel=3; rows[10].expectPass=true;
   return ArraySize(rows);
}

#endif
