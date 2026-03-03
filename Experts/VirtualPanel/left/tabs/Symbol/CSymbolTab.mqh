#ifndef __CSYMBOLTAB_MQH__
#define __CSYMBOLTAB_MQH__

#include "..\\..\\..\\constants\\PanelConstants.mqh"
#include "..\\..\\..\\ui\\UIHelpers.mqh"
#include <Trade\SymbolInfo.mqh> // <--- подключаем CSymbolInfo

class CSymbolTab
{
private:
    int m_x, m_y, m_w, m_h;
    bool m_initialized, m_visible;

    string Prefix() const { return "vp_symbol_tab_"; }

    // --- вычисление Y позиции строки
    int RowY(const int row) const
    {
        return m_y + SYMBOL_TAB_HEADER_OFFSET + row * TABLE_ROW_STEP;
    }

    // --- создаём строку (ключ + значение)
    void DrawRow(const int row, const string key, const string value) const
    {
        int y = RowY(row);
        EnsureLabel(Prefix() + "k_" + IntegerToString(row), m_x, y, m_w / 2, key, clrSilver);
        EnsureLabel(Prefix() + "v_" + IntegerToString(row), m_x + m_w / 2, y, m_w / 2, value, clrWhite);
    }

public:
    void Init(const int x, const int y, const int width, const int height)
    {
        m_x = x; m_y = y; m_w = width; m_h = height;
        m_initialized = true; m_visible = true;
        Draw();
    }

    void Resize(const int x, const int y, const int width, const int height)
    {
        m_x = x; m_y = y; m_w = width; m_h = height;
        if(m_visible) Draw();
    }

    void SetVisible(const bool visible)
    {
        m_visible = visible;
        int total = ObjectsTotal(0,0,-1);
        for(int i=0; i<total; i++)
        {
            string name = ObjectName(0,i,0,-1);
            if(StringFind(name, Prefix()) == 0)
                ObjectSetInteger(0, name, OBJPROP_HIDDEN, !m_visible);
        }
    }

    bool IsVisible() const { return m_visible; }

    void Update()
    {
        if(!m_initialized || !m_visible) return;

        CSymbolInfo sym;
        if(!sym.Name(_Symbol)) return;       // привязываем объект к символу
        if(!sym.Select(true)) return;        // подгружаем актуальные данные

        int digits = sym.Digits();

        // --- цены
        double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
        double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
        double open  = iOpen(_Symbol, PERIOD_CURRENT, 0);
        double high  = iHigh(_Symbol, PERIOD_CURRENT, 0);
        double low   = iLow(_Symbol, PERIOD_CURRENT, 0);
        double close = iClose(_Symbol, PERIOD_CURRENT, 0);
        double point = sym.Point();
        double tick_value = sym.TickValue();
        double tick_size  = sym.TickSize();
        double contract   = sym.ContractSize();

        // --- лоты
        double min_lot = sym.LotsMin();
        double max_lot = sym.LotsMax();
        double lot_step = sym.LotsStep();

        // --- сессия
        long session_deals = sym.SessionDeals();
        double session_volume = sym.SessionBuyOrdersVolume() + sym.SessionSellOrdersVolume();
        double session_profit = sym.SessionTurnover();

        // --- валюта и торговые права
        string currency_base   = sym.CurrencyBase();
        string currency_profit = sym.CurrencyProfit();
        bool trade_allowed = sym.TradeMode() != SYMBOL_TRADE_MODE_DISABLED;

        // --- рисуем строки
        int row = 0;
        DrawRow(row++, "Symbol", _Symbol);
        DrawRow(row++, "Bid", DoubleToString(bid, digits));
        DrawRow(row++, "Ask", DoubleToString(ask, digits));
        DrawRow(row++, "Open", DoubleToString(open, digits));
        DrawRow(row++, "High", DoubleToString(high, digits));
        DrawRow(row++, "Low", DoubleToString(low, digits));
        DrawRow(row++, "Close", DoubleToString(close, digits));
        DrawRow(row++, "Point", DoubleToString(point, digits));
        DrawRow(row++, "Tick Value", DoubleToString(tick_value, 2));
        DrawRow(row++, "Tick Size", DoubleToString(tick_size, digits));
        DrawRow(row++, "Contract Size", DoubleToString(contract, 2));
        DrawRow(row++, "Min Lot", DoubleToString(min_lot, 2));
        DrawRow(row++, "Max Lot", DoubleToString(max_lot, 2));
        DrawRow(row++, "Lot Step", DoubleToString(lot_step, 2));
        DrawRow(row++, "Session Deals", IntegerToString(session_deals));
        DrawRow(row++, "Session Volume", DoubleToString(session_volume, 2));
        DrawRow(row++, "Session Profit", DoubleToString(session_profit, 2));
        DrawRow(row++, "Currency Base", currency_base);
        DrawRow(row++, "Currency Profit", currency_profit);
        DrawRow(row++, "Trade Allowed", trade_allowed ? "Yes" : "No");
    }

    void Draw()
    {
        if(!m_initialized || !m_visible) return;
        EnsureLabel(Prefix() + "title", m_x, m_y, m_w, "Symbol", clrAqua);
        Update();
    }

    void Deinit()
    {
        DeleteByPrefix(Prefix());
        m_initialized = false; m_visible = false;
    }
};

#endif // __CSYMBOLTAB_MQH__
