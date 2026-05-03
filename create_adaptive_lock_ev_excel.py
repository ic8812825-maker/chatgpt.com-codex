from openpyxl import Workbook

sheets = ["README","Broker_Params","Symbol_Params","System_Params","Current_Positions","Market_Data","Calculations","Recommendations","Scenario_Up","Scenario_Down","Risk_Control","Trade_Log","Change_Log"]
wb=Workbook(); ws=wb.active; ws.title=sheets[0]
for s in sheets[1:]: wb.create_sheet(s)
wb['README']['A1']='Калькулятор не торгует. Он только рассчитывает следующий допустимый шаг системы.'
wb['README']['A3']='Заполните вручную Broker_Params, Symbol_Params, Current_Positions, Market_Data.'
# calculations map
c=wb['Calculations']
c['A1']='Z'; c['B1']='=(Market_Data!B2-Market_Data!B3)/Market_Data!B4'
c['A2']='V'; c['B2']='=Market_Data!B4/Market_Data!B5'
c['A8']='Q_Final'; c['B8']='=0.02'
c['A9']='PipValue'; c['B9']='=10'
c['A10']='TotalCost'; c['B10']='=1.2'
c['A11']='Safety'; c['B11']='=1.2'
c['A12']='MinMovePoints'; c['B12']='=(B10*B11)/(B8*B9)'
wb['Scenario_Up']['A1']='TriggerUp'; wb['Scenario_Up']['B1']='=Market_Data!B2+Calculations!B12*Symbol_Params!B3'
wb['Scenario_Down']['A1']='TriggerDown'; wb['Scenario_Down']['B1']='=Market_Data!B2-Calculations!B12*Symbol_Params!B3'
wb.save('adaptive_lock_ev_calculator.xlsx')
