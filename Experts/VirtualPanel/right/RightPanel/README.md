# ALE+ALC Right Panel UI

## Integration (MQL5)

```cpp
#include "RightPanel/PanelCore.mqh"

CRightPanel g_panel;
SPanelSnapshot g_snapshot;

int OnInit()
{
   g_panel.Init();
   EventSetMillisecondTimer(200); // required refresh cadence
   return(INIT_SUCCEEDED);
}

void OnTimer()
{
   // Fill g_snapshot from ALE+ALC state/cache
   g_panel.Update(g_snapshot);
}

void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
{
   g_panel.OnChartEvent(id,sparam);
}
```

## Guarantees

- Panel starts at `max(chart_width*0.6, chart_width-300)` and stays on right side only.
- Exactly one tab visible at any moment.
- Tab switch debounce: 200ms.
- Dark theme and risk colors in Risk tab.
