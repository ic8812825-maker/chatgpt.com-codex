#ifndef ALE_DO_UI_LEFT_COMPONENTS_ADDPOSITIONFORM_MQH_INCLUDED
#define ALE_DO_UI_LEFT_COMPONENTS_ADDPOSITIONFORM_MQH_INCLUDED

#include "../../../state/SystemState.mqh"
#include "../common/UI_Input.mqh"

class CAddPositionFormView
  {
private:
   CEdit m_input;
   bool  m_initialized;

public:
         CAddPositionFormView() : m_initialized(false) {}

   bool   Render(const SystemState &system_state,const int x1,const int y1,const int x2,const int y2)
     {
      if(!m_initialized)
        {
         if(!UI_Input_Create(m_input,0,"ALE_AddPositionForm",0,x1,y1,x2,y2,""))
            return(false);
         m_initialized=true;
        }
      else
         m_input.Move(x1,y1);

      return(true);
     }
  };

#endif // ALE_DO_UI_LEFT_COMPONENTS_ADDPOSITIONFORM_MQH_INCLUDED
