#ifndef ALE_DO_UI_RIGHT_TABS_TAB_CYCLEPNL_MQH_INCLUDED
#define ALE_DO_UI_RIGHT_TABS_TAB_CYCLEPNL_MQH_INCLUDED

#include <Controls\Button.mqh>

#include "../../../state/SystemState.mqh"
#include "../../../state/DualState.mqh"
#include "../../left/common/UI_Button.mqh"

class CTab_CyclePnLView
  {
private:
   CButton m_button;
   bool    m_initialized;

public:
            CTab_CyclePnLView() : m_initialized(false) {}

   bool     Render(const SystemState &system_state,const DualState &dual_state,const int x1,const int y1,const int x2,const int y2)
     {
      if(!m_initialized)
        {
         if(!UI_Button_Create(m_button,0,"ALE_Tab_CyclePnL_Placeholder",0,x1,y1,x2,y2,""))
            return(false);
         m_initialized=true;
        }
      else
         m_button.Move(x1,y1);

      return(true);
     }
  };

#endif // ALE_DO_UI_RIGHT_TABS_TAB_CYCLEPNL_MQH_INCLUDED
