#ifndef __CBROKERTAB_MQH__
#define __CBROKERTAB_MQH__

#include "..\\..\\..\\constants\\PanelConstants.mqh"
#include "..\\..\\..\\ui\\UIHelpers.mqh"

class CBrokerTab
{
private:
   int m_x;
   int m_y;
   int m_w;
   int m_h;
   bool m_initialized;
   bool m_visible;

   string Prefix() const { return "vp_broker_tab_"; }

   void DrawRow(const int row,const string key,const string value) const
   {
      const int row_y=m_y+18+row*(ROW_H-2);
      EnsureLabel(Prefix()+"k_"+IntegerToString(row),m_x,row_y,m_w/2,key,clrSilver);
      EnsureLabel(Prefix()+"v_"+IntegerToString(row),m_x+m_w/2,row_y,m_w/2,value,clrWhite);
   }

public:
   void Init(const int x,const int y,const int width,const int height)
   {
      m_x=x;
      m_y=y;
      m_w=width;
      m_h=height;
      m_initialized=true;
      m_visible=true;
      Draw();
   }

   void Resize(const int x,const int y,const int width,const int height)
   {
      m_x=x;
      m_y=y;
      m_w=width;
      m_h=height;
      if(m_visible)
         Draw();
   }

   void SetVisible(const bool visible)
   {
      m_visible=visible;
      if(!m_visible)
      {
         DeleteByPrefix(Prefix());
         return;
      }
      Draw();
   }

   bool IsVisible() const
   {
      return m_visible;
   }

   void Update()
   {
      if(!m_initialized || !m_visible)
         return;

      DrawRow(0,"Account",IntegerToString((int)AccountInfoInteger(ACCOUNT_LOGIN)));
      DrawRow(1,"Balance",DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE),2));
      DrawRow(2,"Equity",DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY),2));
      DrawRow(3,"Margin",DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN),2));
      DrawRow(4,"FreeMargin",DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_FREE),2));
      DrawRow(5,"Leverage","1:"+IntegerToString((int)AccountInfoInteger(ACCOUNT_LEVERAGE)));
   }

   void Draw()
   {
      if(!m_initialized || !m_visible)
         return;

      EnsureLabel(Prefix()+"title",m_x,m_y,m_w,"Broker",clrAqua);
      Update();
   }

   void Deinit()
   {
      DeleteByPrefix(Prefix());
      m_initialized=false;
      m_visible=false;
   }
};

#endif // __CBROKERTAB_MQH__
