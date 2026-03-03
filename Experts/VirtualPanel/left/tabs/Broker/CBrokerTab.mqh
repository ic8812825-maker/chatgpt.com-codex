#ifndef __CBROKERTAB_MQH__
#define __CBROKERTAB_MQH__

#include "..\\..\\..\\constants\\PanelConstants.mqh"
#include "..\\..\\..\\ui\\UIHelpers.mqh"

class CBrokerTab
{
private:
    int m_x, m_y, m_w, m_h;
    bool m_initialized;
    bool m_visible;

    // кеш для high-performance
    double m_balance, m_equity, m_margin, m_free_margin, m_margin_level, m_stopout;
    string m_currency;
    int m_leverage, m_trade_allowed;

    string Prefix() const { return "vp_broker_tab_"; }

    // вычисление Y позиции строки
    int RowY(const int row) const
    {
        return m_y + BROKER_TAB_HEADER_OFFSET + row * (ROW_H - BROKER_TAB_ROW_PADDING);
    }

    // создаём строку (ключ + значение)
    void DrawRow(const int row, const string key, const string value) const
    {
        int y = RowY(row);
        EnsureLabel(Prefix() + "k_" + IntegerToString(row), m_x, y, m_w / 2, key, clrSilver);
        EnsureLabel(Prefix() + "v_" + IntegerToString(row), m_x + m_w / 2, y, m_w / 2, value, clrWhite);
    }

    // скрываем/показываем объекты
    void ApplyVisibility()
    {
        int total = ObjectsTotal(0, 0, -1);
        for(int i = total-1; i >= 0; i--)
        {
            string name = ObjectName(0, i, 0, -1);
            if(StringFind(name, Prefix()) == 0)
                ObjectSetInteger(0, name, OBJPROP_HIDDEN, !m_visible);
        }
        ChartRedraw(0);
    }

public:
    // constructor
    CBrokerTab()
    {
        m_initialized = false;
        m_visible = true;
        ResetCache();
    }

    // сброс кеша
    void ResetCache()
    {
        m_balance = m_equity = m_margin = m_free_margin = m_margin_level = m_stopout = -1;
        m_currency = "";
        m_leverage = -1;
        m_trade_allowed = -1;
    }

    // init панели
    void Init(const int x, const int y, const int width, const int height)
    {
        if(m_initialized) Deinit();

        m_x = x; m_y = y; m_w = width; m_h = height;
        m_initialized = true;
        m_visible = true;

        DrawLayout();
        Update();
    }

    // изменение размеров
    void Resize(const int x, const int y, const int width, const int height)
    {
        m_x = x; m_y = y; m_w = width; m_h = height;
        if(m_visible) DrawLayout();
    }

    // видимость
    void SetVisible(const bool visible)
    {
        if(m_visible == visible) return;
        m_visible = visible;
        ApplyVisibility();
    }

    bool IsVisible() const { return m_visible; }

    // создаём строки панели
    void DrawLayout()
    {
        if(!m_initialized || !m_visible) return;

        EnsureLabel(Prefix()+"title", m_x, m_y, m_w, "Broker", clrAqua);

        DrawRow(0, "Balance", DoubleToString(m_balance, 2));
        DrawRow(1, "Equity", DoubleToString(m_equity, 2));
        DrawRow(2, "Margin", DoubleToString(m_margin, 2));
        DrawRow(3, "FreeMargin", DoubleToString(m_free_margin, 2));
        DrawRow(4, "MarginLevel", DoubleToString(m_margin_level, 1) + "%");
        DrawRow(5, "Leverage", "1:" + IntegerToString(m_leverage));
        DrawRow(6, "Currency", m_currency);
        DrawRow(7, "Trading", m_trade_allowed ? "Allowed" : "Disabled");
        DrawRow(8, "StopOut", DoubleToString(m_stopout, 1) + "%");

        ChartRedraw(0);
    }

    // обновление значений (только изменённые)
    void Update()
    {
        if(!m_initialized || !m_visible) return;

        int digits = (int)AccountInfoInteger(ACCOUNT_CURRENCY_DIGITS);

        double balance = AccountInfoDouble(ACCOUNT_BALANCE);
        if(balance != m_balance) m_balance = balance;

        double equity = AccountInfoDouble(ACCOUNT_EQUITY);
        if(equity != m_equity) m_equity = equity;

        double margin = AccountInfoDouble(ACCOUNT_MARGIN);
        if(margin != m_margin) m_margin = margin;

        double free = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
        if(free != m_free_margin) m_free_margin = free;

        double ml = AccountInfoDouble(ACCOUNT_MARGIN_LEVEL);
        if(ml != m_margin_level) m_margin_level = ml;

        int lev = (int)AccountInfoInteger(ACCOUNT_LEVERAGE);
        if(lev != m_leverage) m_leverage = lev;

        string cur = AccountInfoString(ACCOUNT_CURRENCY);
        if(cur != m_currency) m_currency = cur;

        int trade = (int)AccountInfoInteger(ACCOUNT_TRADE_ALLOWED);
        if(trade != m_trade_allowed) m_trade_allowed = trade;

        double so = AccountInfoDouble(ACCOUNT_MARGIN_SO_SO);
        if(so != m_stopout) m_stopout = so;

        DrawLayout();
    }

    // деинициализация
    void Deinit()
    {
        DeleteByPrefix(Prefix());
        m_initialized = false;
        m_visible = false;
        ChartRedraw(0);
    }
};

#endif // __CBROKERTAB_MQH__
