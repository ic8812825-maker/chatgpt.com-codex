#ifndef __TESTSAFEDEPOSIT_MQH__
#define __TESTSAFEDEPOSIT_MQH__

bool TestSafeDeposit_Run()
{
   const double k=1.3;
   const double alpha=0.5;
   const int max_levels=30;
   const double leverage=100.0;
   const double contract_size=100000.0;
   const double l0=0.01;

   const double geom=(MathPow(k,max_levels)-1.0)/(k-1.0);
   const double volume=l0*geom*MathPow(alpha,2.0);
   const double margin=volume*contract_size/leverage;
   return(margin>0.0);
}

#endif
