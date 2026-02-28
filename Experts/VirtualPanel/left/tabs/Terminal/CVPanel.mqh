#ifndef __CVPANEL_MQH__
#define __CVPANEL_MQH__

#include "CVirtualPosition.mqh"
#include "CVirtualStream.mqh"
#include "..\\..\\..\\constants\\PanelConstants.mqh"
#include "..\\..\\..\\ui\\UIHelpers.mqh"

enum EVirtualEventType
{
   VP_EVENT_NONE=0,
   VP_OPENED=1,
   VP_UPDATED=2,
   VP_CLOSED=3
};

enum EFsmState
{
   FSM_IDLE=0,
   FSM_BUY_ACTIVE=1,
   FSM_SELL_ACTIVE=2,
   FSM_DUAL_ACTIVE=3,
   FSM_RISK_ALERT=4
};

class CVPanel
{
private:
   CVirtualPosition positions[MAX_POSITIONS];
   int row_flow[MAX_POSITIONS]; // 1=BUY table flow, 2=SELL table flow
   int count;
   int next_id;
   int active_index;
   int add_dir;
   int pending_add_flow;

   int buy_flow_dir;
   int sell_flow_dir;
   bool buy_flow_pick_mode;
   bool sell_flow_pick_mode;
   bool buy_flow_price_locked;
   bool sell_flow_price_locked;
   bool buy_flow_add_price_error;
   bool sell_flow_add_price_error;
   bool buy_flow_last_price_locked;
   bool sell_flow_last_price_locked;
   double buy_flow_last_base_price;
   double sell_flow_last_base_price;
   int pick_flow;

   bool pick_mode;
   bool price_locked;
   int price_digits;
   double last_base_price;

   bool ui_dirty;
   bool update_in_progress;
   bool deferred_ui_dirty;
   bool add_price_error;
   bool last_price_locked;
   int mouse_x;
   int mouse_y;
   int last_active_index;

   EFsmState fsm_state;
   EVirtualEventType last_event;

   string RowName(const string prefix,const int row) const
   {
      return prefix+IntegerToString(row);
   }

   int FlowCount(const int flow_code) const
   {
      int c=0;
      for(int i=0;i<count;i++)
         if(row_flow[i]==flow_code) c++;
      return c;
   }

   int FlowIndexForRow(const int row,const int flow_code) const
   {
      int idx=0;
      for(int i=0;i<=row && i<count;i++)
         if(row_flow[i]==flow_code)
            idx++;
      return idx-1;
   }

   string FlowPrefixForRow(const int row) const
   {
      if(row<0 || row>=count) return "vp_row_buy_flow_";
      return (row_flow[row]==1 ? "vp_row_buy_flow_" : "vp_row_sell_flow_");
   }

   string RowFieldName(const int row,const string field) const
   {
      const int flow_code=(row>=0 && row<count ? row_flow[row] : 1);
      const int idx=FlowIndexForRow(row,flow_code);
      const string prefix=(flow_code==1 ? "vp_row_buy_flow_" : "vp_row_sell_flow_");
      return prefix+field+"_"+IntegerToString(idx);
   }

   int GlobalRowFromFlowAndIndex(const int flow_code,const int flow_index) const
   {
      if(flow_index<0)
         return -1;

      int idx=0;
      for(int i=0;i<count;i++)
      {
         if(row_flow[i]!=flow_code)
            continue;

         if(idx==flow_index)
            return i;
         idx++;
      }
      return -1;
   }

   int ParseRowFromFlowFieldName(const string name) const
   {
      int flow_code=0;
      int start=0;

      if(StringFind(name,"vp_row_buy_flow_")==0)
      {
         flow_code=1;
         start=StringLen("vp_row_buy_flow_");
      }
      else if(StringFind(name,"vp_row_sell_flow_")==0)
      {
         flow_code=2;
         start=StringLen("vp_row_sell_flow_");
      }
      else
         return -1;

      const int sep=StringFind(name,"_",start);
      if(sep<0)
         return -1;

      const int flow_index=(int)StringToInteger(StringSubstr(name,sep+1));
      return GlobalRowFromFlowAndIndex(flow_code,flow_index);
   }

   void UpdateFsm()
   {
      double total_buy=0.0;
      double total_sell=0.0;
      for(int i=0;i<count;i++)
      {
         if(positions[i].dir==DIR_BUY) total_buy+=positions[i].lot;
         if(positions[i].dir==DIR_SELL) total_sell+=positions[i].lot;
      }

      if(total_buy+total_sell>VP_MAX_TOTAL_LOT)
         fsm_state=FSM_RISK_ALERT;
      else if(total_buy>0.0 && total_sell>0.0)
         fsm_state=FSM_DUAL_ACTIVE;
      else if(total_buy>0.0)
         fsm_state=FSM_BUY_ACTIVE;
      else if(total_sell>0.0)
         fsm_state=FSM_SELL_ACTIVE;
      else
         fsm_state=FSM_IDLE;
   }

   void EmitEvent(const EVirtualEventType ev,const int row)
   {
      last_event=ev;
      if(row>=0 && row<count)
         PrintFormat("[VirtualPanel] event=%d id=%d dir=%d lot=%.2f",ev,positions[row].id,positions[row].dir,positions[row].lot);
      else
         PrintFormat("[VirtualPanel] event=%d",ev);
   }

public:
   int Init();
   void Deinit();

   void OnTimer();
   void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam);

   bool AddPosition(double price,int dir,double lot,string comment);
   CVirtualPosition* GetPosition(int index);
   int GetCount();
   void DeletePosition(int index);

   void SetActiveIndex(int index);
   int GetActiveIndex();

   void SetAddDir(int dir);
   int GetAddDir();

   void HandleAdd();
   void ClearAddInputs();

   void CreateAddPanel();
   void CreateTableHeader();
   void CreateRow(int row);
   void RenderTable();
   void DeleteByPrefix(string prefix);

   void ActivateRow(int row);
   void SaveRow(int row);
   void DeleteRow(int row);
   void ToggleRowDir(int row);

   bool UpdateTableSmart();
   bool UpdateEditIfChanged(string name,string new_text);
   bool UpdateEditStateSmart();
   void SetRowEditable(int row,bool active);

   double GetAutoPrice();
   bool UpdateAutoPriceSmart();
   bool AutoPriceNeedsRefresh();
   void SetAddPriceColor();

   bool ParsePositiveNumber(string text,double &value);
   void MarkEditError(string name);
   void ClearEditError(string name);

   void SetAddDirButtons();
   void SetAddDirButtonStyle(string name,bool active,color bg,color border);
   bool UpdateDirSmart();
   bool UpdatePriceColorSmart();

   bool IsMarketClosed();
   int TimeDayOfWeek();

   bool OnPseudoTick();
   void ResetButtonState(string name);
};

int CVPanel::Init()
{
   count=0;
   next_id=1;
   active_index=-1;
   add_dir=0;
   pending_add_flow=0;

   buy_flow_dir=DIR_BUY;
   sell_flow_dir=DIR_SELL;
   buy_flow_pick_mode=false;
   sell_flow_pick_mode=false;
   buy_flow_price_locked=true;
   sell_flow_price_locked=true;
   buy_flow_add_price_error=false;
   sell_flow_add_price_error=false;
   buy_flow_last_price_locked=true;
   sell_flow_last_price_locked=true;
   buy_flow_last_base_price=0.0;
   sell_flow_last_base_price=0.0;
   pick_flow=0;

   pick_mode=false;
   price_locked=true;
   last_base_price=0.0;

   ui_dirty=true;
   update_in_progress=false;
   deferred_ui_dirty=false;
   add_price_error=false;
   last_price_locked=true;
   mouse_x=0;
   mouse_y=0;
   last_active_index=-1;

   fsm_state=FSM_IDLE;
   last_event=VP_EVENT_NONE;

   price_digits=(int)SymbolInfoInteger(_Symbol,SYMBOL_DIGITS);
   if(price_digits<=0) price_digits=5;

   DeleteByPrefix("vp_");
   CreateAddPanel();
   CreateTableHeader();
   RenderTable();
   SetAddDirButtons();
   SetAddPriceColor();

   EventSetTimer(VP_DEFAULT_TIMER_SEC);
   ChartRedraw(0);
   return INIT_SUCCEEDED;
}

void CVPanel::Deinit()
{
   EventKillTimer();
   update_in_progress=false;
   ui_dirty=false;
   DeleteByPrefix("vp_");
   ChartRedraw(0);
}

void CVPanel::OnTimer()
{
   if(update_in_progress) return;
   if(!ui_dirty && !AutoPriceNeedsRefresh()) return;

   update_in_progress=true;
   if(OnPseudoTick()) ChartRedraw(0);
   ui_dirty=deferred_ui_dirty;
   deferred_ui_dirty=false;
   update_in_progress=false;
}

void CVPanel::OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
{
   if(id==CHARTEVENT_MOUSE_MOVE)
   {
      mouse_x=(int)lparam;
      mouse_y=(int)dparam;
   }

   if(id==CHARTEVENT_CLICK && pick_flow!=0 && sparam=="")
   {
      datetime click_time;
      double click_price=0.0;
      int x=mouse_x;
      int y=mouse_y;
      if(x==0 && y==0) { x=(int)lparam; y=(int)dparam; }

      bool found=false;
      int windows=(int)ChartGetInteger(0,CHART_WINDOWS_TOTAL);
      if(windows<=0) windows=1;
      for(int w=0;w<windows;w++)
      {
         if(ChartXYToTimePrice(0,w,x,y,click_time,click_price))
         {
            found=true;
            break;
         }
      }

      if(found)
      {
         if(pick_flow==1)
         {
            ObjectSetString(0,"vp_buy_flow_price",OBJPROP_TEXT,DoubleToString(click_price,price_digits));
            buy_flow_price_locked=false;
         }
         if(pick_flow==2)
         {
            ObjectSetString(0,"vp_sell_flow_price",OBJPROP_TEXT,DoubleToString(click_price,price_digits));
            sell_flow_price_locked=false;
         }
         SetAddPriceColor();
         ui_dirty=true;
      }
      buy_flow_pick_mode=false;
      sell_flow_pick_mode=false;
      pick_flow=0;
      return;
   }

   if(id==CHARTEVENT_OBJECT_CLICK)
   {
      bool handled=false;

      // BUY flow
      if(sparam=="vp_buy_flow_price") { buy_flow_price_locked=!buy_flow_price_locked; SetAddPriceColor(); handled=true; }
      if(sparam=="vp_buy_flow_buy")   { buy_flow_dir=DIR_BUY; SetAddDirButtons(); handled=true; }
      if(sparam=="vp_buy_flow_sell")  { buy_flow_dir=DIR_SELL; SetAddDirButtons(); handled=true; }
      if(sparam=="vp_buy_flow_pick")  { pick_flow=1; buy_flow_pick_mode=true; buy_flow_price_locked=false; SetAddPriceColor(); handled=true; }
      if(sparam=="vp_buy_flow_btn")
      {
         handled=true;
         double price=0.0;
         double lot=0.0;
         const string comment=ObjectGetString(0,"vp_buy_flow_comment",OBJPROP_TEXT);
         if(!ParsePositiveNumber(ObjectGetString(0,"vp_buy_flow_price",OBJPROP_TEXT),price)) { MarkEditError("vp_buy_flow_price"); handled=true; }
         else if(!ParsePositiveNumber(ObjectGetString(0,"vp_buy_flow_lot",OBJPROP_TEXT),lot)) { MarkEditError("vp_buy_flow_lot"); handled=true; }
         else if(lot<MIN_LOT) { MarkEditError("vp_buy_flow_lot"); handled=true; }
         else { pending_add_flow=1; bool added=AddPosition(NormalizeDouble(price,price_digits),buy_flow_dir,NormalizeDouble(lot,2),comment); pending_add_flow=0; if(added)
         {
            ClearEditError("vp_buy_flow_price");
            ClearEditError("vp_buy_flow_lot");
            ObjectSetString(0,"vp_buy_flow_price",OBJPROP_TEXT,"");
            ObjectSetString(0,"vp_buy_flow_lot",OBJPROP_TEXT,DoubleToString(DEFAULT_LOT,2));
            ObjectSetString(0,"vp_buy_flow_comment",OBJPROP_TEXT,"");
            RenderTable();
            handled=true;
         } }
         ResetButtonState(sparam);
      }
      if(sparam=="vp_buy_flow_clear") { ObjectSetString(0,"vp_buy_flow_price",OBJPROP_TEXT,""); ObjectSetString(0,"vp_buy_flow_lot",OBJPROP_TEXT,DoubleToString(DEFAULT_LOT,2)); ObjectSetString(0,"vp_buy_flow_comment",OBJPROP_TEXT,""); buy_flow_dir=DIR_BUY; buy_flow_pick_mode=false; buy_flow_price_locked=true; SetAddDirButtons(); SetAddPriceColor(); ResetButtonState(sparam); handled=true; }

      // SELL flow
      if(sparam=="vp_sell_flow_price") { sell_flow_price_locked=!sell_flow_price_locked; SetAddPriceColor(); handled=true; }
      if(sparam=="vp_sell_flow_sell")  { sell_flow_dir=DIR_SELL; SetAddDirButtons(); handled=true; }
      if(sparam=="vp_sell_flow_buy")   { sell_flow_dir=DIR_BUY; SetAddDirButtons(); handled=true; }
      if(sparam=="vp_sell_flow_pick")  { pick_flow=2; sell_flow_pick_mode=true; sell_flow_price_locked=false; SetAddPriceColor(); handled=true; }
      if(sparam=="vp_sell_flow_btn")
      {
         handled=true;
         double price=0.0;
         double lot=0.0;
         const string comment=ObjectGetString(0,"vp_sell_flow_comment",OBJPROP_TEXT);
         if(!ParsePositiveNumber(ObjectGetString(0,"vp_sell_flow_price",OBJPROP_TEXT),price)) { MarkEditError("vp_sell_flow_price"); handled=true; }
         else if(!ParsePositiveNumber(ObjectGetString(0,"vp_sell_flow_lot",OBJPROP_TEXT),lot)) { MarkEditError("vp_sell_flow_lot"); handled=true; }
         else if(lot<MIN_LOT) { MarkEditError("vp_sell_flow_lot"); handled=true; }
         else { pending_add_flow=2; bool added=AddPosition(NormalizeDouble(price,price_digits),sell_flow_dir,NormalizeDouble(lot,2),comment); pending_add_flow=0; if(added)
         {
            ClearEditError("vp_sell_flow_price");
            ClearEditError("vp_sell_flow_lot");
            ObjectSetString(0,"vp_sell_flow_price",OBJPROP_TEXT,"");
            ObjectSetString(0,"vp_sell_flow_lot",OBJPROP_TEXT,DoubleToString(DEFAULT_LOT,2));
            ObjectSetString(0,"vp_sell_flow_comment",OBJPROP_TEXT,"");
            RenderTable();
            handled=true;
         } }
         ResetButtonState(sparam);
      }
      if(sparam=="vp_sell_flow_clear") { ObjectSetString(0,"vp_sell_flow_price",OBJPROP_TEXT,""); ObjectSetString(0,"vp_sell_flow_lot",OBJPROP_TEXT,DoubleToString(DEFAULT_LOT,2)); ObjectSetString(0,"vp_sell_flow_comment",OBJPROP_TEXT,""); sell_flow_dir=DIR_SELL; sell_flow_pick_mode=false; sell_flow_price_locked=true; SetAddDirButtons(); SetAddPriceColor(); ResetButtonState(sparam); handled=true; }

      if(StringFind(sparam,"vp_edit_")==0)  { int row=(int)StringToInteger(StringSubstr(sparam,8)); ActivateRow(row); ResetButtonState(sparam); handled=true; }
      if(StringFind(sparam,"vp_save_")==0)  { int row=(int)StringToInteger(StringSubstr(sparam,8)); SaveRow(row); ResetButtonState(sparam); handled=true; }
      if(StringFind(sparam,"vp_del_")==0)   { int row=(int)StringToInteger(StringSubstr(sparam,7)); DeleteRow(row); ResetButtonState(sparam); handled=true; }
      for(int di=0;di<count;di++) { if(sparam==RowFieldName(di,"dir")) { ToggleRowDir(di); handled=true; break; } }

      if(handled)
      {
         ui_dirty=true;
         if(update_in_progress) deferred_ui_dirty=true;
         else
         {
            update_in_progress=true;
            OnPseudoTick();
            ChartRedraw(0);
            ui_dirty=false;
            update_in_progress=false;
         }
      }
      return;
   }

   if(id==CHARTEVENT_OBJECT_ENDEDIT)
   {
      const int edited_row=ParseRowFromFlowFieldName(sparam);
      if(edited_row>=0 && edited_row==active_index)
      {
         SaveRow(edited_row);
         RenderTable();
         ChartRedraw(0);
      }
   }
}

bool CVPanel::AddPosition(double price,int dir,double lot,string comment)
{
   if(count>=MAX_POSITIONS) return false;
   if(dir!=DIR_BUY && dir!=DIR_SELL) return false;
   if(price<=0.0 || lot<MIN_LOT) return false;

   positions[count].id=next_id++;
   positions[count].dir=dir;
   positions[count].direction=dir;
   positions[count].price=price;
   positions[count].lot=lot;
   positions[count].comment=comment;
   positions[count].UpdateVirtualMetrics(SymbolInfoDouble(_Symbol,SYMBOL_BID),SymbolInfoDouble(_Symbol,SYMBOL_ASK),100000.0,(double)AccountInfoInteger(ACCOUNT_LEVERAGE));
   row_flow[count]=(pending_add_flow==2?2:1);

   count++;
   UpdateFsm();
   EmitEvent(VP_OPENED,count-1);
   return true;
}

CVirtualPosition* CVPanel::GetPosition(int index)
{
   if(index<0 || index>=count) return NULL;
   return &positions[index];
}

int CVPanel::GetCount() { return count; }

void CVPanel::DeletePosition(int index)
{
   if(index<0 || index>=count) return;
   for(int i=index;i<count-1;i++) { positions[i]=positions[i+1]; row_flow[i]=row_flow[i+1]; }
   count--;
   if(active_index==index) active_index=-1;
   else if(active_index>index) active_index--;
   last_active_index=-1;
   UpdateFsm();
   EmitEvent(VP_CLOSED,-1);
}

void CVPanel::SetActiveIndex(int index) { active_index=index; }
int CVPanel::GetActiveIndex() { return active_index; }

void CVPanel::SetAddDir(int dir)
{
   add_dir=dir;
   SetAddDirButtons();
}

int CVPanel::GetAddDir() { return add_dir; }

void CVPanel::HandleAdd()
{
   if(count>=MAX_POSITIONS) return;
   if(add_dir==0) return;

   double price=0.0;
   double lot=0.0;
   string comment=ObjectGetString(0,"vp_add_comment",OBJPROP_TEXT);

   if(!ParsePositiveNumber(ObjectGetString(0,"vp_add_price",OBJPROP_TEXT),price))
   {
      MarkEditError("vp_add_price");
      return;
   }
   if(!ParsePositiveNumber(ObjectGetString(0,"vp_add_lot",OBJPROP_TEXT),lot))
   {
      MarkEditError("vp_add_lot");
      return;
   }

   price=NormalizeDouble(price,price_digits);
   lot=NormalizeDouble(lot,2);
   if(lot<MIN_LOT)
   {
      MarkEditError("vp_add_lot");
      return;
   }

   ClearEditError("vp_add_price");
   ClearEditError("vp_add_lot");

   if(!AddPosition(price,add_dir,lot,comment))
      return;

   ClearAddInputs();
   CreateRow(count-1);
}

void CVPanel::ClearAddInputs()
{
   ObjectSetString(0,"vp_buy_flow_price",OBJPROP_TEXT,"");
   ObjectSetString(0,"vp_buy_flow_lot",OBJPROP_TEXT,DoubleToString(DEFAULT_LOT,2));
   ObjectSetString(0,"vp_buy_flow_comment",OBJPROP_TEXT,"");

   ObjectSetString(0,"vp_sell_flow_price",OBJPROP_TEXT,"");
   ObjectSetString(0,"vp_sell_flow_lot",OBJPROP_TEXT,DoubleToString(DEFAULT_LOT,2));
   ObjectSetString(0,"vp_sell_flow_comment",OBJPROP_TEXT,"");

   buy_flow_dir=DIR_BUY;
   sell_flow_dir=DIR_SELL;
   buy_flow_pick_mode=false;
   sell_flow_pick_mode=false;
   buy_flow_price_locked=true;
   sell_flow_price_locked=true;
   buy_flow_add_price_error=false;
   sell_flow_add_price_error=false;

   add_dir=0;
   pending_add_flow=0;
   pick_mode=false;
   price_locked=true;
   add_price_error=false;
   SetAddDirButtons();
   SetAddPriceColor();
}

void CVPanel::CreateAddPanel()
{
   int x=X0;
   int y_label=ADD_LABEL_Y;
   int y_row=ADD_ROW_Y;

   // BUY Flow
   EnsureLabel("vp_buy_flow_lbl",x,y_label-8,120,"BUY Flow",clrLime);
   EnsureLabel("vp_buy_flow_lbl_price",x,y_label,COL_W_PRICE,"Price",clrSilver);
   EnsureLabel("vp_buy_flow_lbl_dir",x+COL_W_PRICE,y_label,COL_W_DIR,"Dir",clrSilver);
   EnsureLabel("vp_buy_flow_lbl_lot",x+COL_W_PRICE+COL_W_DIR,y_label,COL_W_LOT,"Lot",clrSilver);
   EnsureLabel("vp_buy_flow_lbl_comment",x+COL_W_PRICE+COL_W_DIR+COL_W_LOT,y_label,COL_W_COMMENT,"Comment",clrSilver);

   int cx=x;
   EnsureEdit("vp_buy_flow_price",cx,y_row,COL_W_PRICE-COL_W_PICK,ROW_H,""); cx+=COL_W_PRICE-COL_W_PICK;
   EnsureButton("vp_buy_flow_pick",cx,y_row,COL_W_PICK,ROW_H,"🎯"); cx+=COL_W_PICK;
   int dir_w=COL_W_DIR/2;
   EnsureButton("vp_buy_flow_buy",cx,y_row,dir_w,ROW_H,"BUY"); cx+=dir_w;
   EnsureButton("vp_buy_flow_sell",cx,y_row,dir_w,ROW_H,"SELL"); cx+=dir_w;
   EnsureEdit("vp_buy_flow_lot",cx,y_row,COL_W_LOT,ROW_H,DoubleToString(DEFAULT_LOT,2)); cx+=COL_W_LOT;
   EnsureEdit("vp_buy_flow_comment",cx,y_row,COL_W_COMMENT,ROW_H,""); cx+=COL_W_COMMENT;
   EnsureButton("vp_buy_flow_btn",cx,y_row,COL_W_BTN,ROW_H,"✔"); cx+=COL_W_BTN;
   EnsureButton("vp_buy_flow_clear",cx,y_row,COL_W_BTN,ROW_H,"🧹");

   // SELL Flow
   y_label=ADD_LABEL_Y+ROW_H+10;
   y_row=ADD_ROW_Y+ROW_H+10;
   EnsureLabel("vp_sell_flow_lbl",x,y_label-8,120,"SELL Flow",clrTomato);
   EnsureLabel("vp_sell_flow_lbl_price",x,y_label,COL_W_PRICE,"Price",clrSilver);
   EnsureLabel("vp_sell_flow_lbl_dir",x+COL_W_PRICE,y_label,COL_W_DIR,"Dir",clrSilver);
   EnsureLabel("vp_sell_flow_lbl_lot",x+COL_W_PRICE+COL_W_DIR,y_label,COL_W_LOT,"Lot",clrSilver);
   EnsureLabel("vp_sell_flow_lbl_comment",x+COL_W_PRICE+COL_W_DIR+COL_W_LOT,y_label,COL_W_COMMENT,"Comment",clrSilver);

   cx=x;
   EnsureEdit("vp_sell_flow_price",cx,y_row,COL_W_PRICE-COL_W_PICK,ROW_H,""); cx+=COL_W_PRICE-COL_W_PICK;
   EnsureButton("vp_sell_flow_pick",cx,y_row,COL_W_PICK,ROW_H,"🎯"); cx+=COL_W_PICK;
   dir_w=COL_W_DIR/2;
   EnsureButton("vp_sell_flow_sell",cx,y_row,dir_w,ROW_H,"SELL"); cx+=dir_w;
   EnsureButton("vp_sell_flow_buy",cx,y_row,dir_w,ROW_H,"BUY"); cx+=dir_w;
   EnsureEdit("vp_sell_flow_lot",cx,y_row,COL_W_LOT,ROW_H,DoubleToString(DEFAULT_LOT,2)); cx+=COL_W_LOT;
   EnsureEdit("vp_sell_flow_comment",cx,y_row,COL_W_COMMENT,ROW_H,""); cx+=COL_W_COMMENT;
   EnsureButton("vp_sell_flow_btn",cx,y_row,COL_W_BTN,ROW_H,"✔"); cx+=COL_W_BTN;
   EnsureButton("vp_sell_flow_clear",cx,y_row,COL_W_BTN,ROW_H,"🧹");

   // compatibility hidden fields (legacy helpers)
   EnsureEdit("vp_add_price",-1000,-1000,1,1,"");
   EnsureEdit("vp_add_lot",-1000,-1000,1,1,DoubleToString(DEFAULT_LOT,2));
   EnsureEdit("vp_add_comment",-1000,-1000,1,1,"");
}

void CVPanel::CreateTableHeader()
{
   int x=X0;
   EnsureLabel("vp_tbl_lbl_id",x,TABLE_LABEL_Y,COL_W_ID,"ID",clrSilver); x+=COL_W_ID;
   EnsureLabel("vp_tbl_lbl_dir",x,TABLE_LABEL_Y,COL_W_DIR,"Dir",clrSilver); x+=COL_W_DIR;
   EnsureLabel("vp_tbl_lbl_price",x,TABLE_LABEL_Y,COL_W_PRICE,"Price",clrSilver); x+=COL_W_PRICE;
   EnsureLabel("vp_tbl_lbl_lot",x,TABLE_LABEL_Y,COL_W_LOT,"Lot",clrSilver); x+=COL_W_LOT;
   EnsureLabel("vp_tbl_lbl_comment",x,TABLE_LABEL_Y,COL_W_COMMENT,"Comment",clrSilver); x+=COL_W_COMMENT;
   EnsureLabel("vp_tbl_lbl_edit",x,TABLE_LABEL_Y,COL_W_BTN,"✏️",clrSilver); x+=COL_W_BTN;
   EnsureLabel("vp_tbl_lbl_save",x,TABLE_LABEL_Y,COL_W_BTN,"✔️",clrSilver); x+=COL_W_BTN;
   EnsureLabel("vp_tbl_lbl_del",x,TABLE_LABEL_Y,COL_W_BTN,"❌",clrSilver);
}

void CVPanel::CreateRow(int row)
{
   if(row<0 || row>=count) return;

   const int dir=positions[row].dir;
   const int flow_code=row_flow[row];
   const int flow_idx=FlowIndexForRow(row,flow_code);
   const int buy_count=FlowCount(1);
   const int visual_row=(flow_code==1 ? flow_idx : (buy_count+1+flow_idx));

   int y=TABLE_ROW_Y+ROW_H*visual_row;
   int x=X0;

   string name_id=RowFieldName(row,"id");
   EnsureEdit(name_id,x,y,COL_W_ID,ROW_H,IntegerToString(positions[row].id));
   ObjectSetInteger(0,name_id,OBJPROP_READONLY,true);
   x+=COL_W_ID;

   string name_dir=RowFieldName(row,"dir");
   EnsureEdit(name_dir,x,y,COL_W_DIR,ROW_H,(positions[row].dir==DIR_BUY?"BUY":"SELL"));
   ObjectSetInteger(0,name_dir,OBJPROP_READONLY,true);
   ObjectSetInteger(0,name_dir,OBJPROP_COLOR,(positions[row].dir==DIR_BUY?clrLime:clrTomato));
   x+=COL_W_DIR;

   string name_price=RowFieldName(row,"price");
   EnsureEdit(name_price,x,y,COL_W_PRICE,ROW_H,DoubleToString(positions[row].price,price_digits));
   x+=COL_W_PRICE;

   string name_lot=RowFieldName(row,"lot");
   EnsureEdit(name_lot,x,y,COL_W_LOT,ROW_H,DoubleToString(positions[row].lot,2));
   x+=COL_W_LOT;

   string name_comment=RowFieldName(row,"comment");
   EnsureEdit(name_comment,x,y,COL_W_COMMENT,ROW_H,positions[row].comment);
   x+=COL_W_COMMENT;

   EnsureButton(RowName("vp_edit_",row),x,y,COL_W_BTN,ROW_H,"✏️"); x+=COL_W_BTN;
   EnsureButton(RowName("vp_save_",row),x,y,COL_W_BTN,ROW_H,"✔️"); x+=COL_W_BTN;
   EnsureButton(RowName("vp_del_",row),x,y,COL_W_BTN,ROW_H,"❌");

   SetRowEditable(row,row==active_index);
}

void CVPanel::RenderTable()
{
   DeleteByPrefix("vp_row_buy_flow_");
   DeleteByPrefix("vp_row_sell_flow_");
   DeleteByPrefix("vp_edit_");
   DeleteByPrefix("vp_save_");
   DeleteByPrefix("vp_del_");
   DeleteByPrefix("vp_tbl_sep_");
   DeleteByPrefix("vp_tbl_sec_");

   for(int i=0;i<count;i++)
      if(row_flow[i]==1)
         CreateRow(i);

   const int sep_y=TABLE_ROW_Y+ROW_H*FlowCount(1)-2;
   EnsureLabel("vp_tbl_sec_buy",X0,TABLE_ROW_Y-16,160,"BUY Flow",clrLime);
   EnsureLabel("vp_tbl_sep_line",X0,sep_y,COL_W_ID+COL_W_DIR+COL_W_PRICE+COL_W_LOT+COL_W_COMMENT+COL_W_BTN*3,"---   ---   ---   ---   ---   ---   ---   ---",clrSilver);
   EnsureLabel("vp_tbl_sec_sell",X0,sep_y+4,160,"SELL Flow",clrTomato);

   for(int j=0;j<count;j++)
      if(row_flow[j]==2)
         CreateRow(j);
}

void CVPanel::DeleteByPrefix(string prefix)
{
   const int total=ObjectsTotal(0,0,-1);
   for(int i=total-1;i>=0;i--)
   {
      string name=ObjectName(0,i,0,-1);
      if(StringFind(name,prefix)==0)
         ObjectDelete(0,name);
   }
}

void CVPanel::ActivateRow(int row)
{
   if(row<0 || row>=count) return;
   if(row==active_index) return;
   active_index=row;
}

void CVPanel::SaveRow(int row)
{
   if(row<0 || row>=count) return;
   if(active_index!=row) return;

   string name_price=RowFieldName(row,"price");
   string name_lot=RowFieldName(row,"lot");
   string name_comment=RowFieldName(row,"comment");

   double price=0.0;
   double lot=0.0;
   string comment=ObjectGetString(0,name_comment,OBJPROP_TEXT);

   if(!ParsePositiveNumber(ObjectGetString(0,name_price,OBJPROP_TEXT),price))
   {
      MarkEditError(name_price);
      return;
   }
   if(!ParsePositiveNumber(ObjectGetString(0,name_lot,OBJPROP_TEXT),lot))
   {
      MarkEditError(name_lot);
      return;
   }

   price=NormalizeDouble(price,price_digits);
   lot=NormalizeDouble(lot,2);
   if(lot<MIN_LOT)
   {
      MarkEditError(name_lot);
      return;
   }

   ClearEditError(name_price);
   ClearEditError(name_lot);

   positions[row].price=price;
   positions[row].lot=lot;
   positions[row].comment=comment;
   positions[row].UpdateVirtualMetrics(SymbolInfoDouble(_Symbol,SYMBOL_BID),SymbolInfoDouble(_Symbol,SYMBOL_ASK),100000.0,(double)AccountInfoInteger(ACCOUNT_LEVERAGE));

   active_index=-1;
   UpdateFsm();
   EmitEvent(VP_UPDATED,row);
}

void CVPanel::DeleteRow(int row)
{
   if(row<0 || row>=count) return;
   DeletePosition(row);
   RenderTable();
   ChartRedraw(0);
}

void CVPanel::ToggleRowDir(int row)
{
   if(row<0 || row>=count) return;
   positions[row].dir=(positions[row].dir==DIR_BUY?DIR_SELL:DIR_BUY);
   positions[row].direction=positions[row].dir;
   UpdateFsm();
   EmitEvent(VP_UPDATED,row);
}

bool CVPanel::UpdateTableSmart()
{
   bool changed=false;
   for(int i=0;i<count;i++)
   {
      if(i==active_index) continue;
      if(UpdateEditIfChanged(RowFieldName(i,"price"),DoubleToString(positions[i].price,price_digits))) changed=true;
      if(UpdateEditIfChanged(RowFieldName(i,"lot"),DoubleToString(positions[i].lot,2))) changed=true;
      if(UpdateEditIfChanged(RowFieldName(i,"comment"),positions[i].comment)) changed=true;
   }
   return changed;
}

bool CVPanel::UpdateEditIfChanged(string name,string new_text)
{
   if(ObjectFind(0,name)<0) return false;
   string old_text=ObjectGetString(0,name,OBJPROP_TEXT);
   if(old_text!=new_text)
   {
      ObjectSetString(0,name,OBJPROP_TEXT,new_text);
      return true;
   }
   return false;
}

bool CVPanel::UpdateEditStateSmart()
{
   if(last_active_index==active_index) return false;
   if(last_active_index>=0) SetRowEditable(last_active_index,false);
   if(active_index>=0) SetRowEditable(active_index,true);
   last_active_index=active_index;
   return true;
}

void CVPanel::SetRowEditable(int row,bool active)
{
   if(row<0 || row>=count) return;

   string name_price=RowFieldName(row,"price");
   string name_lot=RowFieldName(row,"lot");
   string name_comment=RowFieldName(row,"comment");

   if(ObjectFind(0,name_price)>=0) ObjectSetInteger(0,name_price,OBJPROP_READONLY,!active);
   if(ObjectFind(0,name_lot)>=0) ObjectSetInteger(0,name_lot,OBJPROP_READONLY,!active);
   if(ObjectFind(0,name_comment)>=0) ObjectSetInteger(0,name_comment,OBJPROP_READONLY,!active);

   color c=(active?clrYellow:clrWhite);
   if(ObjectFind(0,name_price)>=0) ObjectSetInteger(0,name_price,OBJPROP_COLOR,c);
   if(ObjectFind(0,name_lot)>=0) ObjectSetInteger(0,name_lot,OBJPROP_COLOR,c);
   if(ObjectFind(0,name_comment)>=0) ObjectSetInteger(0,name_comment,OBJPROP_COLOR,c);
}

double CVPanel::GetAutoPrice()
{
   if(IsMarketClosed()) return 0.0;
   if(add_dir==DIR_BUY)
      return SymbolInfoDouble(_Symbol,SYMBOL_ASK);
   if(add_dir==DIR_SELL)
      return SymbolInfoDouble(_Symbol,SYMBOL_BID);
   return 0.0;
}

bool CVPanel::UpdateAutoPriceSmart()
{
   bool changed=false;

   if(buy_flow_price_locked)
   {
      double p=(buy_flow_dir==DIR_BUY?SymbolInfoDouble(_Symbol,SYMBOL_ASK):SymbolInfoDouble(_Symbol,SYMBOL_BID));
      if(p>0.0)
      {
         buy_flow_last_base_price=p;
         changed |= UpdateEditIfChanged("vp_buy_flow_price",DoubleToString(p,price_digits));
      }
   }

   if(sell_flow_price_locked)
   {
      double p=(sell_flow_dir==DIR_BUY?SymbolInfoDouble(_Symbol,SYMBOL_ASK):SymbolInfoDouble(_Symbol,SYMBOL_BID));
      if(p>0.0)
      {
         sell_flow_last_base_price=p;
         changed |= UpdateEditIfChanged("vp_sell_flow_price",DoubleToString(p,price_digits));
      }
   }

   return changed;
}

bool CVPanel::AutoPriceNeedsRefresh()
{
   if(IsMarketClosed()) return false;

   if(buy_flow_price_locked)
   {
      double p=(buy_flow_dir==DIR_BUY?SymbolInfoDouble(_Symbol,SYMBOL_ASK):SymbolInfoDouble(_Symbol,SYMBOL_BID));
      if(p>0.0 && MathAbs(p-buy_flow_last_base_price)>_Point*0.5) return true;
   }

   if(sell_flow_price_locked)
   {
      double p=(sell_flow_dir==DIR_BUY?SymbolInfoDouble(_Symbol,SYMBOL_ASK):SymbolInfoDouble(_Symbol,SYMBOL_BID));
      if(p>0.0 && MathAbs(p-sell_flow_last_base_price)>_Point*0.5) return true;
   }

   return false;
}

void CVPanel::SetAddPriceColor()
{
   color c_buy=(buy_flow_price_locked?clrLime:clrYellow);
   if(buy_flow_add_price_error) c_buy=clrRed;
   if(ObjectFind(0,"vp_buy_flow_price")>=0)
      ObjectSetInteger(0,"vp_buy_flow_price",OBJPROP_COLOR,c_buy);

   color c_sell=(sell_flow_price_locked?clrLime:clrYellow);
   if(sell_flow_add_price_error) c_sell=clrRed;
   if(ObjectFind(0,"vp_sell_flow_price")>=0)
      ObjectSetInteger(0,"vp_sell_flow_price",OBJPROP_COLOR,c_sell);
}

bool CVPanel::ParsePositiveNumber(string text,double &value)
{
   value=StringToDouble(text);
   return (value>0.0);
}

void CVPanel::MarkEditError(string name)
{
   if(ObjectFind(0,name)<0) return;
   ObjectSetInteger(0,name,OBJPROP_COLOR,clrRed);
   if(name=="vp_buy_flow_price") buy_flow_add_price_error=true;
   if(name=="vp_sell_flow_price") sell_flow_add_price_error=true;
   if(name=="vp_add_price") add_price_error=true;
}

void CVPanel::ClearEditError(string name)
{
   if(ObjectFind(0,name)<0) return;
   if(name=="vp_buy_flow_price") { buy_flow_add_price_error=false; SetAddPriceColor(); return; }
   if(name=="vp_sell_flow_price") { sell_flow_add_price_error=false; SetAddPriceColor(); return; }
   if(name=="vp_add_price")
   {
      add_price_error=false;
      SetAddPriceColor();
      last_price_locked=price_locked;
      return;
   }
   ObjectSetInteger(0,name,OBJPROP_COLOR,clrWhite);
}

void CVPanel::SetAddDirButtons()
{
   SetAddDirButtonStyle("vp_buy_flow_buy",true,clrGreen,clrLime);
   SetAddDirButtonStyle("vp_buy_flow_sell",true,clrRed,clrRed);

   SetAddDirButtonStyle("vp_sell_flow_sell",true,clrRed,clrRed);
   SetAddDirButtonStyle("vp_sell_flow_buy",true,clrGreen,clrLime);
}

void CVPanel::SetAddDirButtonStyle(string name,bool active,color bg,color border)
{
   if(ObjectFind(0,name)<0) return;
   if(active)
   {
      ObjectSetInteger(0,name,OBJPROP_STATE,true);
      ObjectSetInteger(0,name,OBJPROP_BGCOLOR,bg);
      ObjectSetInteger(0,name,OBJPROP_BORDER_COLOR,border);
      ObjectSetInteger(0,name,OBJPROP_COLOR,clrWhite);
   }
   else
   {
      ObjectSetInteger(0,name,OBJPROP_STATE,false);
      ObjectSetInteger(0,name,OBJPROP_BGCOLOR,clrDimGray);
      ObjectSetInteger(0,name,OBJPROP_BORDER_COLOR,clrGray);
      ObjectSetInteger(0,name,OBJPROP_COLOR,clrSilver);
   }
}

bool CVPanel::UpdateDirSmart()
{
   bool changed=false;
   for(int i=0;i<count;i++)
   {
      const string name=RowFieldName(i,"dir");
      const string txt=(positions[i].dir==DIR_BUY?"BUY":"SELL");
      if(UpdateEditIfChanged(name,txt)) changed=true;
      if(ObjectFind(0,name)>=0)
         ObjectSetInteger(0,name,OBJPROP_COLOR,(positions[i].dir==DIR_BUY?clrLime:clrTomato));
   }
   return changed;
}

bool CVPanel::UpdatePriceColorSmart()
{
   bool changed=false;
   if(buy_flow_last_price_locked!=buy_flow_price_locked) { buy_flow_last_price_locked=buy_flow_price_locked; changed=true; }
   if(sell_flow_last_price_locked!=sell_flow_price_locked) { sell_flow_last_price_locked=sell_flow_price_locked; changed=true; }
   if(changed || buy_flow_add_price_error || sell_flow_add_price_error)
   {
      SetAddPriceColor();
      return true;
   }
   return false;
}

bool CVPanel::IsMarketClosed()
{
   int wd=TimeDayOfWeek();
   return (wd==0 || wd==6);
}

int CVPanel::TimeDayOfWeek()
{
   MqlDateTime dt;
   TimeToStruct(TimeCurrent(),dt);
   return dt.day_of_week;
}

bool CVPanel::OnPseudoTick()
{
   bool changed=false;
   if(UpdateAutoPriceSmart()) changed=true;
   if(UpdateTableSmart()) changed=true;
   if(UpdateEditStateSmart()) changed=true;
   if(UpdatePriceColorSmart()) changed=true;
   if(UpdateDirSmart()) changed=true;
   return changed;
}

void CVPanel::ResetButtonState(string name)
{
   if(ObjectFind(0,name)<0) return;
   ObjectSetInteger(0,name,OBJPROP_STATE,false);
}

#endif // __CVPANEL_MQH__
