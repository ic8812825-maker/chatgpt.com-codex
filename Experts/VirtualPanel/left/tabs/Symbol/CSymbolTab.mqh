#ifndef __CSYMBOLTAB_MQH__
#define __CSYMBOLTAB_MQH__

#include "..\\..\\..\\constants\\PanelConstants.mqh"
#include "..\\..\\..\\ui\\UIHelpers.mqh"

class CSymbolTab
{
private:
   int m_x;
   int m_y;
   int m_w;
   int m_h;
   bool m_initialized;
   bool m_visible;

   string Prefix() const { return "vp_symbol_tab_"; }

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

      const double bid=SymbolInfoDouble(_Symbol,SYMBOL_BID);
      const double ask=SymbolInfoDouble(_Symbol,SYMBOL_ASK);
      const double point=SymbolInfoDouble(_Symbol,SYMBOL_POINT);
      const double contract_size=SymbolInfoDouble(_Symbol,SYMBOL_TRADE_CONTRACT_SIZE);
      const int spread_pts=(int)SymbolInfoInteger(_Symbol,SYMBOL_SPREAD);
      const int digits=(int)SymbolInfoInteger(_Symbol,SYMBOL_DIGITS);

      DrawRow(0,"Symbol",_Symbol);
      DrawRow(1,"Bid",DoubleToString(bid,digits));
      DrawRow(2,"Ask",DoubleToString(ask,digits));
      DrawRow(3,"Spread",IntegerToString(spread_pts));
      DrawRow(4,"Point",DoubleToString(point,digits));
      DrawRow(5,"LotSize",DoubleToString(contract_size,2));
   }

   void Draw()
   {
      if(!m_initialized || !m_visible)
         return;

      EnsureLabel(Prefix()+"title",m_x,m_y,m_w,"Symbol",clrAqua);
      Update();
   }

   void Deinit()
   {
      DeleteByPrefix(Prefix());
      m_initialized=false;
      m_visible=false;
   }
};

#endif // __CSYMBOLTAB_MQH__
