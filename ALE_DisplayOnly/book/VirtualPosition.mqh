#ifndef ALE_DO_BOOK_VIRTUALPOSITION_MQH_INCLUDED
#define ALE_DO_BOOK_VIRTUALPOSITION_MQH_INCLUDED

class VirtualPosition
  {
public:
   int             id;
   string          symbol;
   ENUM_ORDER_TYPE type;
   double          price;
   double          volume;
   string          comment;
   datetime        open_time;
   int             stream; // 0=BUY поток, 1=SELL поток

   // future pnl
   double          unrealized_pnl;
   double          swap;
   double          commission;

   // ALE binding
   int             ale_layer;
   int             ale_group_id;
   bool            ale_managed;

                  VirtualPosition()
                    : id(0),symbol(""),type(ORDER_TYPE_BUY),price(0.0),volume(0.0),comment(""),
                      open_time(0),stream(0),unrealized_pnl(0.0),swap(0.0),commission(0.0),
                      ale_layer(0),ale_group_id(0),ale_managed(false)
     {
     }
  };

#endif // ALE_DO_BOOK_VIRTUALPOSITION_MQH_INCLUDED
