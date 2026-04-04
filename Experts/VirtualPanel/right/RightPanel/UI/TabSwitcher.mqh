#ifndef __RIGHTPANEL_UI_TABSWITCHER_MQH__
#define __RIGHTPANEL_UI_TABSWITCHER_MQH__

#include "Button.mqh"

class CTabSwitcher
{
private:
   CUIButton m_btns[6];
   ulong     m_last_switch_msc;

public:
   CTabSwitcher(void): m_last_switch_msc(0) {}

   void Create(const int x,const int y,const int width)
   {
      string names[6]={"Overview","MPC","Risk","Dual","Exec","Logs"};
      int bw=width/6;
      for(int i=0;i<6;i++)
         m_btns[i].Create("RP_TAB_"+(string)i,x+i*bw,y,bw-2,22,names[i]);
   }

   int HandleClick(const string sparam)
   {
      ulong now=GetTickCount64();
      if(now-m_last_switch_msc<200) return -1; // debounce
      for(int i=0;i<6;i++)
      {
         if(m_btns[i].IsClicked(sparam))
         {
            m_last_switch_msc=now;
            return i;
         }
      }
      return -1;
   }

   void SetActive(const int tab)
   {
      for(int i=0;i<6;i++) m_btns[i].SetActive(i==tab);
   }

   void SetVisible(const bool visible)
   {
      for(int i=0;i<6;i++) m_btns[i].SetVisible(visible);
   }
};

#endif
