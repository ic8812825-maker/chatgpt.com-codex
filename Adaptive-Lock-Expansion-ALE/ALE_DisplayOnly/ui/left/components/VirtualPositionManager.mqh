#ifndef ALE_DO_UI_LEFT_COMPONENTS_VIRTUALPOSITIONMANAGER_MQH_INCLUDED
#define ALE_DO_UI_LEFT_COMPONENTS_VIRTUALPOSITIONMANAGER_MQH_INCLUDED

#include "../../../book/VirtualPosition.mqh"

class CVirtualPositionManager
  {
private:
   VirtualPosition m_positions[];
   int             m_next_id;
   string          m_last_error;

   bool            IsVolumeValid(const double volume) const
     {
      const string symbol=_Symbol;
      const double vmin=SymbolInfoDouble(symbol,SYMBOL_VOLUME_MIN);
      const double vmax=SymbolInfoDouble(symbol,SYMBOL_VOLUME_MAX);
      const double vstep=SymbolInfoDouble(symbol,SYMBOL_VOLUME_STEP);

      if(volume<vmin || volume>vmax)
         return(false);
      if(vstep<=0.0)
         return(false);

      const double q=volume/vstep;
      return(MathAbs(q-MathRound(q))<1e-8);
     }

   int             FindIndexById(const int id) const
     {
      const int n=ArraySize(m_positions);
      for(int i=0;i<n;i++)
         if(m_positions[i].id==id)
            return(i);
      return(-1);
     }

public:
                   CVirtualPositionManager() : m_next_id(1),m_last_error("") {}

   string          LastError() const
     {
      return(m_last_error);
     }

   int             Count() const
     {
      return(ArraySize(m_positions));
     }

   VirtualPosition At(const int index) const
     {
      return(m_positions[index]);
     }

   bool            Add(const int stream,
                       const ENUM_ORDER_TYPE type,
                       const double price,
                       const double volume,
                       const string comment)
     {
      m_last_error="";
      if(price<=0.0)
        {
         m_last_error="Цена должна быть > 0";
         return(false);
        }
      if(!IsVolumeValid(volume))
        {
         m_last_error="Некорректный лот";
         return(false);
        }
      if(Count()>=100)
        {
         m_last_error="Достигнут лимит 100 позиций";
         return(false);
        }

      const int idx=ArraySize(m_positions);
      ArrayResize(m_positions,idx+1);

      m_positions[idx].id=m_next_id++;
      m_positions[idx].symbol=_Symbol;
      m_positions[idx].type=type;
      m_positions[idx].price=price;
      m_positions[idx].volume=volume;
      m_positions[idx].comment=comment;
      m_positions[idx].open_time=TimeCurrent();
      m_positions[idx].stream=stream;
      m_positions[idx].unrealized_pnl=0.0;
      m_positions[idx].swap=0.0;
      m_positions[idx].commission=0.0;
      m_positions[idx].ale_layer=0;
      m_positions[idx].ale_group_id=0;
      m_positions[idx].ale_managed=false;
      return(true);
     }

   bool            Remove(const int id)
     {
      const int idx=FindIndexById(id);
      if(idx<0)
         return(false);

      const int n=ArraySize(m_positions);
      for(int i=idx;i<n-1;i++)
         m_positions[i]=m_positions[i+1];
      ArrayResize(m_positions,n-1);
      return(true);
     }

   bool            Edit(const int id,const double price,const double volume,const string comment)
     {
      m_last_error="";
      if(price<=0.0)
        {
         m_last_error="Цена должна быть > 0";
         return(false);
        }
      if(!IsVolumeValid(volume))
        {
         m_last_error="Некорректный лот";
         return(false);
        }

      const int idx=FindIndexById(id);
      if(idx<0)
        {
         m_last_error="Позиция не найдена";
         return(false);
        }

      m_positions[idx].price=price;
      m_positions[idx].volume=volume;
      m_positions[idx].comment=comment;
      return(true);
     }
  };

#endif // ALE_DO_UI_LEFT_COMPONENTS_VIRTUALPOSITIONMANAGER_MQH_INCLUDED
