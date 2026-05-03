from openpyxl import Workbook

wb=Workbook()
for s in ["README","Broker_Params","Symbol_Params","System_Params","Current_Positions","Market_Data","Calculations","Recommendations","Scenario_Up","Scenario_Down","Risk_Control","Trade_Log","Change_Log"]:
    if s=="README": ws=wb.active; ws.title=s
    else: wb.create_sheet(s)

r=wb['README']
r['A1']='Калькулятор Adaptive Lock EV (демо)'
r['A2']='Назначение: расчет следующего допустимого шага системы.'
r['A3']='Важно: калькулятор не торгует, только рассчитывает.'
r['A4']='Логика следующего шага рассчитывается на листах Calculations/Scenario_Up/Scenario_Down/Recommendations.'

b=wb['Broker_Params']
rows=[('Параметр','Значение','Комментарий'),('Баланс счёта',10000,'Демо'),('Эквити',10000,'Демо'),('Плечо',100,'1:100'),('Спред (пункты)',2,'Демо'),('Комиссия за 1 лот',0.5,'Демо'),('Проскальзывание (пункты)',1,'Демо'),('Своп BUY',0,'Демо'),('Своп SELL',0,'Демо'),('Маржа на 1 лот',1000,'Демо'),('Мин. лот',0.01,'Демо'),('Шаг лота',0.01,'Демо'),('Макс. лот',100,'Демо')]
for i,row in enumerate(rows,1):
    for j,v in enumerate(row,1): b.cell(i,j,v)

s=wb['Symbol_Params']
rows=[('Параметр','Значение','Комментарий'),('Символ','EURUSD','Демо'),('Digits',5,'Точность'),('Point',0.0001,'Шаг цены'),('Tick Size',0.0001,'Размер тика'),('Tick Value',1,'Стоимость тика'),('Pip Value 1 Lot',10,'Стоимость пункта'),('Contract Size',100000,'Контракт'),('ATR Period Short',14,'Демо'),('ATR Period Long',100,'Демо'),('EMA Period',50,'Демо')]
for i,row in enumerate(rows,1):
    for j,v in enumerate(row,1): s.cell(i,j,v)

sp=wb['System_Params']
params=[('Параметр','Значение'),('Base Lock Buy Lot',0.10),('Base Lock Sell Lot',0.10),('Q Min',0.01),('Q Max',0.02),('Max Total Lot',0.30),('Max Exposure',0.05),('Z Entry Level',1.5),('V Mean Revert Max',1.2),('V Volatile Stop',1.5),('DD Stress Level',0.07),('DD Escape Level',0.15),('DD Beta Protection',0.10),('Beta DD Protection',0.80),('Min EV Required',0),('Safety Cost Multiplier',1.2),('Expected Mu',6)]
for i,row in enumerate(params,1): sp.cell(i,1,row[0]); sp.cell(i,2,row[1])

cp=wb['Current_Positions']
cp['A1']='ID'; cp['B1']='Тип'; cp['C1']='Лот'; cp['D1']='Цена открытия'; cp['E1']='Плавающий PnL'; cp['F1']='Комментарий'; cp['G1']='Убыток (USD)'; cp['H1']='Убыток (пункты)'
cp.append([1,'BUY',0.01,1.17385,'=(Market_Data!B2-D2)/Symbol_Params!B4*C2*Symbol_Params!B7','минусовой замок',-144.06,''])
cp.append([2,'SELL',0.01,1.17175,'=(D3-Market_Data!B2)/Symbol_Params!B4*C3*Symbol_Params!B7','противоположная нога','',''])
cp['J1']='Сумма BUY'; cp['K1']='=SUMIFS(C2:C100,B2:B100,"BUY")'
cp['J2']='Сумма SELL'; cp['K2']='=SUMIFS(C2:C100,B2:B100,"SELL")'

m=wb['Market_Data']
rows=[('Параметр','Значение'),('Текущая цена',1.17193),('EMA',1.17553),('ATR Short',0.0018),('ATR Long',0.0024),('Текущий DD',0.02),('Последний PnL 10 циклов',5)]
for i,row in enumerate(rows,1): m.cell(i,1,row[0]); m.cell(i,2,row[1])

c=wb['Calculations']
c['A1']='Z'; c['B1']='=(Market_Data!B2-Market_Data!B3)/Market_Data!B4'
c['A2']='V'; c['B2']='=Market_Data!B4/Market_Data!B5'
c['A3']='Regime'; c['B3']='=IF(B2>System_Params!B10,"VOLATILE",IF(B2<System_Params!B9,"MEAN_REVERT","NEUTRAL"))'
c['A4']='Confidence'; c['B4']='=MIN(ABS(B1)/2,1)'
c['A5']='Q'; c['B5']='=MIN(MAX(System_Params!B4+System_Params!B4*B4,System_Params!B4),System_Params!B5)'
c['A6']='Q adj'; c['B6']='=IF(B3="NEUTRAL",B5*0.5,IF(B3="VOLATILE",0,B5))'
c['A7']='Beta'; c['B7']='=IF(Market_Data!B6>System_Params!B13,System_Params!B14,0.7-0.4*B4)'
c['A8']='Cost'; c['B8']='=(Broker_Params!B5*B6*Symbol_Params!B7)+(Broker_Params!B6*B6)+(Broker_Params!B7*B6*Symbol_Params!B7)'
c['A9']='EV'; c['B9']='=(System_Params!B17*B6*Symbol_Params!B7)-B8'
c['A10']='MinMovePoints'; c['B10']='=(B8*System_Params!B16)/(B6*Symbol_Params!B7)'
c['A11']='MinMovePrice'; c['B11']='=B10*Symbol_Params!B4'
c['A12']='TotalLot'; c['B12']='=Current_Positions!K1+Current_Positions!K2'
c['A13']='Exposure'; c['B13']='=ABS(Current_Positions!K1-Current_Positions!K2)'
c['A14']='RiskOK'; c['B14']='=IF(AND(B12<=System_Params!B6,B13<=System_Params!B7),"YES","NO")'
c['A15']='EV_OK'; c['B15']='=IF(B9>System_Params!B15,"ALLOW","BLOCK")'

up=wb['Scenario_Up']
up['A1']='TriggerUp'; up['B1']='=Market_Data!B2+Calculations!B11'
up['A2']='Action'; up['B2']='=IF(AND(Calculations!B1>System_Params!B8,Calculations!B3="MEAN_REVERT",Calculations!B14="YES",Calculations!B15="ALLOW"),"OPEN","NO_ACTION")'
up['A3']='Type'; up['B3']='=IF(B2="OPEN","SELL","")'
up['A4']='Lot'; up['B4']='=IF(B2="OPEN",Calculations!B6,0)'
up['A5']='Comment'; up['B5']='=IF(B2="OPEN","Mean reversion SELL","Блокировка условий")'

dn=wb['Scenario_Down']
dn['A1']='TriggerDown'; dn['B1']='=Market_Data!B2-Calculations!B11'
dn['A2']='Action'; dn['B2']='=IF(AND(Calculations!B1<-System_Params!B8,Calculations!B3="MEAN_REVERT",Calculations!B14="YES",Calculations!B15="ALLOW"),"OPEN","NO_ACTION")'
dn['A3']='Type'; dn['B3']='=IF(B2="OPEN","BUY","")'
dn['A4']='Lot'; dn['B4']='=IF(B2="OPEN",Calculations!B6,0)'
dn['A5']='Comment'; dn['B5']='=IF(B2="OPEN","Mean reversion BUY","Блокировка условий")'

rec=wb['Recommendations']
rec['A1']='Direction'; rec['B1']='Action'; rec['C1']='Type'; rec['D1']='Price'; rec['E1']='Lot'; rec['F1']='Comment'
rec['A2']='UP'; rec['B2']='=Scenario_Up!B2'; rec['C2']='=Scenario_Up!B3'; rec['D2']='=Scenario_Up!B1'; rec['E2']='=Scenario_Up!B4'; rec['F2']='=Scenario_Up!B5'
rec['A3']='DOWN'; rec['B3']='=Scenario_Down!B2'; rec['C3']='=Scenario_Down!B3'; rec['D3']='=Scenario_Down!B1'; rec['E3']='=Scenario_Down!B4'; rec['F3']='=Scenario_Down!B5'

for sh in ['Risk_Control','Trade_Log','Change_Log']:
    wb[sh]['A1']='Демо-данные заполнены'

wb.save('adaptive_lock_ev_calculator.xlsx')
print('adaptive_lock_ev_calculator.xlsx updated with next-step formulas')
