#ifndef __PANELCONSTANTS_MQH__
#define __PANELCONSTANTS_MQH__

#define MAX_POSITIONS 100
#define DEFAULT_LOT 0.10
#define MIN_LOT 0.01

#define DIR_BUY   1
#define DIR_SELL -1


#define VP_DEFAULT_TIMER_SEC 1

// manual-compatible UI scale
#define VP_FONT_SIZE 10
#define VP_FONT_SIZE_TITLE 8

#define VP_BLOCK_GAP     12
#define VP_SECTION_GAP   0
#define VP_TABLE_GAP     14

#define BROKER_TAB_HEADER_OFFSET 18
#define BROKER_TAB_ROW_PADDING   2
#define BROKER_TAB_ROW_COUNT     10 

#define SYMBOL_TAB_HEADER_OFFSET 18

const int CORNER = CORNER_LEFT_UPPER;
const int X0 = 10;

const int ADD_LABEL_Y = 10;
const int ADD_ROW_Y   = 30;
const int TABLE_LABEL_Y = 110;
const int TABLE_ROW_Y   = 130;

const int ROW_H = 20;

// column widths (manual)
const int COL_W_ID = 50;
const int COL_W_PRICE = 80;
const int COL_W_PICK = 30;
const int COL_W_DIR = 50;
const int COL_W_LOT = 60;
const int COL_W_COMMENT = 160;
const int COL_W_BTN = 30;

// compatibility aliases used by existing helper logic
const int STREAM_GAP = 145;
const int TITLE_H = 16;
const int HEADER_H = 16;
const int BTN_H = ROW_H;

// dynamic column layout (enterprise safe)
const int COL_ID_X = 0;
const int COL_ID_W = COL_W_ID;

const int COL_DIR_X = COL_ID_X + COL_ID_W;
const int COL_DIR_W = COL_W_DIR;

const int COL_PRICE_X = COL_DIR_X + COL_DIR_W;
const int COL_PRICE_W = COL_W_PRICE;

const int COL_PICK_X = COL_PRICE_X + COL_PRICE_W;
const int COL_PICK_W = COL_W_PICK;

const int COL_LOT_X = COL_PICK_X + COL_PICK_W;
const int COL_LOT_W = COL_W_LOT;

const int COL_COMMENT_X = COL_LOT_X + COL_LOT_W;
const int COL_COMMENT_W = COL_W_COMMENT;

const int COL_DELETE_X = COL_COMMENT_X + COL_COMMENT_W;
const int COL_DELETE_W = COL_W_BTN * 3;

static const double VP_MAX_TOTAL_LOT = 10.0;

#define TABLE_ROW_STEP (ROW_H - 2)

#endif // __PANELCONSTANTS_MQH__
