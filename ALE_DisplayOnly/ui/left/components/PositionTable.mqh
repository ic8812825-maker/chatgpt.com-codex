#ifndef ALE_DO_UI_LEFT_COMPONENTS_POSITIONTABLE_MQH_INCLUDED
#define ALE_DO_UI_LEFT_COMPONENTS_POSITIONTABLE_MQH_INCLUDED

#include "../../../state/SystemState.mqh"
#include "../common/UI_Table.mqh"

class CPositionTableView
  {
private:
   CListView m_table;
   bool      m_initialized;

public:
            CPositionTableView() : m_initialized(false) {}

   bool      Render(const SystemState &system_state,const int x1,const int y1,const int x2,const int y2)
     {
      if(!m_initialized)
        {
         if(!UI_Table_Create(m_table,0,"ALE_PositionTable",0,x1,y1,x2,y2))
            return(false);
         m_initialized=true;
        }
      else
         m_table.Move(x1,y1);

      return(true);
     }
  };

#endif // ALE_DO_UI_LEFT_COMPONENTS_POSITIONTABLE_MQH_INCLUDED
