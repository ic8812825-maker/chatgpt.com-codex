#ifndef ALE_DO_UI_LEFT_COMPONENTS_POSITIONROW_MQH_INCLUDED
#define ALE_DO_UI_LEFT_COMPONENTS_POSITIONROW_MQH_INCLUDED

#include <Controls\Label.mqh>

#include "../../../state/SystemState.mqh"

class CPositionRowView
  {
private:
   CLabel m_label;
   bool   m_initialized;

public:
           CPositionRowView() : m_initialized(false) {}

   bool    Render(const SystemState &system_state,const int index,const int x1,const int y1,const int x2,const int y2)
     {
      if(!m_initialized)
        {
         if(!m_label.Create(0,StringFormat("ALE_PositionRow_%d",index),0,x1,y1,x2,y2))
            return(false);
         m_initialized=true;
        }
      else
         m_label.Move(x1,y1,x2,y2);

      m_label.Text(StringFormat("Position %d",index));
      return(true);
     }
  };

#endif // ALE_DO_UI_LEFT_COMPONENTS_POSITIONROW_MQH_INCLUDED
