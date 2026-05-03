from openpyxl import Workbook

wb=Workbook()
for s in ["README","Broker_Params","Symbol_Params","System_Params","Current_Positions","Market_Data","Calculations","Recommendations","Scenario_Up","Scenario_Down","Risk_Control","Trade_Log","Change_Log"]:
    if s=="README": ws=wb.active; ws.title=s
    else: wb.create_sheet(s)

r=wb['README']
r['A1']='Калькулятор Adaptive Lock EV (демо)'
r['A2']='Назначение: расчет следующего допустимого шага системы.'
r['A3']='Важно: калькулятор не торгует, только рассчитывает.'
r['A5']='Все параметры ниже заполнены демо-данными на русском языке.'

b=wb['Broker_Params']
rows=[('Параметр','Значение','Комментарий'),('Баланс счёта',10000,'Демо'),('Эквити',10000,'Демо'),('Плечо',100,'1:100'),('Спред (пункты)',2,'Демо'),('Комиссия за 1 лот',0.5,'Демо'),('Проскальзывание (пункты)',1,'Демо'),('Своп BUY',0,'Демо'),('Своп SELL',0,'Демо'),('Маржа на 1 лот',1000,'Демо'),('Мин. лот',0.01,'Демо'),('Шаг лота',0.01,'Демо'),('Макс. лот',100,'Демо')]
for i,row in enumerate(rows,1):
    for j,v in enumerate(row,1): b.cell(i,j,v)

s=wb['Symbol_Params']
rows=[('Параметр','Значение','Комментарий'),('Символ','EURUSD','Демо'),('Digits',5,'Точность'),('Point',0.0001,'Шаг цены'),('Tick Size',0.0001,'Размер тика'),('Tick Value',1,'Стоимость тика'),('Pip Value 1 Lot',10,'Стоимость пункта'),('Contract Size',100000,'Контракт'),('ATR Period Short',14,'Демо'),('ATR Period Long',100,'Демо'),('EMA Period',50,'Демо')]
for i,row in enumerate(rows,1):
    for j,v in enumerate(row,1): s.cell(i,j,v)

sp=wb['System_Params']
params=[('Параметр','Значение'),('Base Lock Buy Lot',0.10),('Base Lock Sell Lot',0.10),('Q Min',0.01),('Q Max',0.02),('Max Total Lot',0.30),('Max Exposure',0.05),('Z Entry Level',1.5),('V Mean Revert Max',1.2),('V Volatile Stop',1.5),('DD Stress Level',0.07),('DD Escape Level',0.15),('DD Beta Protection',0.10),('Beta Min',0.30),('Beta Max',0.70),('Beta DD Protection',0.80),('Min EV Required',0),('Safety Cost Multiplier',1.2)]
for i,row in enumerate(params,1):
    sp.cell(i,1,row[0]); sp.cell(i,2,row[1])

m=wb['Market_Data']
rows=[('Параметр','Значение'),('Текущая цена',1.17193),('EMA',1.0985),('ATR Short',0.0018),('ATR Long',0.0020),('Текущий DD',0.02),('Последний PnL 10 циклов',5)]
for i,row in enumerate(rows,1):
    m.cell(i,1,row[0]); m.cell(i,2,row[1])

c=wb['Calculations']
c['A1']='Z'; c['B1']='=(Market_Data!B2-Market_Data!B3)/Market_Data!B4'
c['A2']='V'; c['B2']='=Market_Data!B4/Market_Data!B5'
c['A3']='Confidence'; c['B3']='=MIN(ABS(B1)/2,1)'
c['A4']='Q'; c['B4']='=MIN(MAX(System_Params!B4+System_Params!B4*B3,System_Params!B4),System_Params!B5)'
c['A5']='Beta'; c['B5']='=IF(Market_Data!B6>System_Params!B13,System_Params!B17,0.7-0.4*B3)'
c['A6']='Cost'; c['B6']='=(Broker_Params!B5*B4*Symbol_Params!B7)+(Broker_Params!B6*B4)+(Broker_Params!B7*B4*Symbol_Params!B7)'
c['A7']='EV'; c['B7']='=(6*B4*Symbol_Params!B7)-B6'
c['A8']='MinMovePoints'; c['B8']='=(B6*System_Params!B19)/(B4*Symbol_Params!B7)'

for sh in ['Recommendations','Scenario_Up','Scenario_Down','Risk_Control','Trade_Log','Change_Log']:
    ws=wb[sh]
    ws['A1']='Демо-данные заполнены'


cp=wb['Current_Positions']
cp['A1']='ID'; cp['B1']='Тип'; cp['C1']='Лот'; cp['D1']='Цена открытия'; cp['E1']='Плавающий PnL'; cp['F1']='Комментарий'; cp['G1']='Убыток (USD)'; cp['H1']='Убыток (пункты)'
cp.append([1,'BUY',0.01,1.17385,-10.50,'минусовой замок',-144.06,''])
cp.append([2,'SELL',0.01,1.17175,'','противоположная нога','',''])

wb.save('adaptive_lock_ev_calculator.xlsx')
print('adaptive_lock_ev_calculator.xlsx updated')
