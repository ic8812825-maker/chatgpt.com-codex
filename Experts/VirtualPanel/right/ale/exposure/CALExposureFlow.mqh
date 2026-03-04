#ifndef __CALEXPOSUREFLOW_MQH__
#define __CALEXPOSUREFLOW_MQH__

#include "CALDeltaSurface.mqh"
#include "CALGammaProfile.mqh"
#include "CALConvexityAnalyzer.mqh"
#include "..\\interfaces\\IALExposureModel.mqh"
#include "..\\positions\\CALPositionBook.mqh"

class CALExposureFlow : public IALExposureModel
{
private:
   int m_direction;
   double m_exposure;
   double m_pnl;
   double m_delta_surface;
   double m_gamma_profile;
   double m_convexity;

   CALDeltaSurface m_delta_model;
   CALGammaProfile m_gamma_model;
   CALConvexityAnalyzer m_convexity_model;

public:
   void Init(const int direction)
   {
      m_direction=direction;
      m_exposure=0.0;
      m_pnl=0.0;
      m_delta_surface=0.0;
      m_gamma_profile=0.0;
      m_convexity=0.0;
   }

   virtual void Recalculate(const CALPositionBook &book,const double price)
   {
      const double contract_size=1.0;
      m_exposure=book.TotalAbsLot()*price;
      m_pnl=book.PnLAtPrice(price,contract_size);

      m_delta_surface=m_delta_model.DeltaFromBook(book);
      const double dp=1.0;
      m_gamma_profile=m_gamma_model.FromDeltaSurface(m_delta_surface,m_delta_surface,dp);

      if(m_direction==ALE_FLOW_BUY)
         m_convexity=m_convexity_model.ConvexityBuy(m_gamma_profile,m_delta_surface);
      else
         m_convexity=m_convexity_model.ConvexitySell(m_gamma_profile,m_delta_surface);
   }

   virtual double Exposure() const { return m_exposure; }
   virtual double DeltaSurface() const { return m_delta_surface; }
   virtual double GammaProfile() const { return m_gamma_profile; }
   double Convexity() const { return m_convexity; }
   double PnL() const { return m_pnl; }
};

#endif
