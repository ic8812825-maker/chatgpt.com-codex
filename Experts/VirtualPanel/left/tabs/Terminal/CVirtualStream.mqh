#ifndef __CVIRTUALSTREAM_MQH__
#define __CVIRTUALSTREAM_MQH__

#include "CVirtualPosition.mqh"
#include "..\\..\\..\\constants\\PanelConstants.mqh"
#include "..\\..\\..\\ui\\UIHelpers.mqh"

class CVirtualStream
{
private:
   CVirtualPosition m_positions[MAX_POSITIONS];
   int m_count;
   int m_direction;
   string m_prefix;
   int m_base_y;
   int m_next_id;

   string DirectionText() const
   {
      return (m_direction==DIR_BUY ? "BUY" : "SELL");
   }

   bool ParseRowIndex(const string obj_name,int &row_index) const
   {
      const string token=m_prefix+"_row_";
      const int pos=StringFind(obj_name,token);
      if(pos!=0)
         return false;

      string suffix=StringSubstr(obj_name,StringLen(token));
      const int field_sep=StringFind(suffix,"_");
      if(field_sep<0)
         return false;

      const string idx_part=StringSubstr(suffix,0,field_sep);
      row_index=(int)StringToInteger(idx_part);
      return (row_index>=0 && row_index<m_count);
   }

   void DrawHeaders() const
   {
      const int y=m_base_y+TITLE_H+2;
      EnsureLabel(m_prefix+"_h_id",X0+COL_ID_X,y,COL_ID_W,"ID",clrSilver);
      EnsureLabel(m_prefix+"_h_dir",X0+COL_DIR_X,y,COL_DIR_W,"Direction",clrSilver);
      EnsureLabel(m_prefix+"_h_price",X0+COL_PRICE_X,y,COL_PRICE_W,"Price",clrSilver);
      EnsureLabel(m_prefix+"_h_pick",X0+COL_PICK_X,y,COL_PICK_W,"Pick",clrSilver);
      EnsureLabel(m_prefix+"_h_lot",X0+COL_LOT_X,y,COL_LOT_W,"Lot",clrSilver);
      EnsureLabel(m_prefix+"_h_comment",X0+COL_COMMENT_X,y,COL_COMMENT_W,"Comment",clrSilver);
      EnsureLabel(m_prefix+"_h_del",X0+COL_DELETE_X,y,COL_DELETE_W,"Delete",clrSilver);
   }

   double StreamPrice() const
   {
      const ENUM_SYMBOL_INFO_DOUBLE type=(m_direction==DIR_BUY ? SYMBOL_ASK : SYMBOL_BID);
      return SymbolInfoDouble(_Symbol,type);
   }

public:
   void Init(const int dir,const string name_prefix,const int start_y)
   {
      m_direction=dir;
      m_prefix=name_prefix;
      m_base_y=start_y;
      m_count=0;
      m_next_id=1;
   }

   void Deinit() const
   {
      DeleteByPrefix(m_prefix+"_");
   }

   int Count() const
   {
      return m_count;
   }

   int Direction() const
   {
      return m_direction;
   }


   double TotalLot() const
   {
      double total=0.0;
      for(int i=0;i<m_count;i++)
         total+=m_positions[i].lot;
      return total;
   }

   void RecalcVirtualMetrics()
   {
      const double bid=SymbolInfoDouble(_Symbol,SYMBOL_BID);
      const double ask=SymbolInfoDouble(_Symbol,SYMBOL_ASK);
      double contract_size=100000.0;
      SymbolInfoDouble(_Symbol,SYMBOL_TRADE_CONTRACT_SIZE,contract_size);
      const double leverage=(double)AccountInfoInteger(ACCOUNT_LEVERAGE);

      for(int i=0;i<m_count;i++)
         m_positions[i].UpdateVirtualMetrics(bid,ask,contract_size,leverage);
   }

   bool GetPositionCopy(const int index,CVirtualPosition &out_pos) const
   {
      if(index<0 || index>=m_count)
         return false;
      out_pos=m_positions[index];
      return true;
   }



   bool UpdatePosition(const int index,const double price,const double lot,const string comment)
   {
      if(index<0 || index>=m_count)
         return false;
      if(price<=0.0 || lot<MIN_LOT)
         return false;

      m_positions[index].price=price;
      m_positions[index].lot=lot;
      m_positions[index].comment=comment;
      RenderRows();
      return true;
   }

   bool AddPosition(const double price,const double lot,const string comment="")
   {
      if(m_count>=MAX_POSITIONS)
         return false;
      if(price<=0.0 || lot<MIN_LOT)
         return false;

      m_positions[m_count].Init(m_next_id,m_direction,price,lot,comment);
      m_count++;
      m_next_id++;
      RenderRows();
      return true;
   }

   bool DeletePosition(const int index)
   {
      if(index<0 || index>=m_count)
         return false;

      for(int i=index;i<m_count-1;i++)
         m_positions[i]=m_positions[i+1];

      m_count--;
      RenderRows();
      return true;
   }

   void RenderRows() const
   {
      // Единая таблица рендерится в CVPanel.
   }

   bool HandleClick(const string obj_name)
   {
      if(obj_name=="")
         return false;
      return false;
   }

   bool HandleEditEnd(const string obj_name)
   {
      if(obj_name=="")
         return false;
      return false;
   }
};

#endif // __CVIRTUALSTREAM_MQH__
