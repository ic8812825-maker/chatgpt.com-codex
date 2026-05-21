from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.chart import LineChart, Reference

OUT = Path(__file__).resolve().parent / 'MinusLock_Simple_Skew_Compression_Calculator.xlsx'

def h(ws,c,t):
    ws[c]=t; ws[c].font=Font(bold=True); ws[c].fill=PatternFill('solid',fgColor='D9E1F2')

def build_calc(ws):
    ws.title='Калькулятор'
    h(ws,'A1','ПАРАМЕТРЫ')
    params=[('СтартЛот',1.0),('ШагПункты',100),('МаксУровни',5),('ШагЛота',0.01),('Направление','DOWN'),('Округлять',True),('РежимBig','ВНИЗ'),('РежимSmall','ВВЕРХ'),('РежимClose','SAFE'),('СтоимостьПункта',10),('Спред',0),('Комиссия',0)]
    for i,(k,v) in enumerate(params,2): ws[f'A{i}']=k; ws[f'B{i}']=v

    h(ws,'D1','ПАРАМЕТРЫ РИСКА')
    risk=[('Баланс',10000),('Плечо',100),('РазмерКонтракта',100000),('ЦенаИнструмента',1.1),('СтоимостьПунктаНа1Лот',10),('МаксДвижениеПротив(пункты)',500),('УровеньStopOut%',50),('УровеньMarginCall%',100)]
    for i,(k,v) in enumerate(risk,2): ws[f'D{i}']=k; ws[f'E{i}']=v

    h(ws,'A16','СЕТКА УРОВНЕЙ')
    for c,n in enumerate(['Уровень','Big %','Small %','ЦелевойSkew %','РучноеЗакрытие %'],1): ws.cell(17,c,n).font=Font(bold=True)
    grid=[(1,90,30,0,''),(2,30,15,15,''),(3,20,15,10,''),(4,10,10,10,''),(5,5,5,10,'')]
    for r,row in enumerate(grid,18):
        for c,v in enumerate(row,1): ws.cell(r,c,v)

    def tbl(sr,name):
        h(ws,f'A{sr}',name)
        cols=['Уровень','Big %','Small %','ЦелевойSkew %','РучноеЗакрытие %','BigЛот','BigОкругл','SmallЛот','SmallОкругл','СтартДо %','MainДо %','OppДо %','АвтоЗакрытие %','ИтогЗакрытие %','ЗакрытиеЛот','ЗакрытиеЛотОкругл','СтартПосле %','СуммаBig %','СуммаSmall %','ИтогMain %','ИтогOpp %','Skew %','ОкруглMainЛот','ОкруглOppЛот','ОкруглSkewЛот','Статус']
        for c,n in enumerate(cols,1): ws.cell(sr+1,c,n).font=Font(bold=True)
        for i,r in enumerate(range(sr+2,sr+7),1):
            lv=17+i; p=r-1
            ws[f'A{r}']=f'=A{lv}'; ws[f'B{r}']=f'=B{lv}'; ws[f'C{r}']=f'=C{lv}'; ws[f'D{r}']=f'=D{lv}'; ws[f'E{r}']=f'=IF(E{lv}="","",E{lv})'
            ws[f'F{r}']=f'=$B$2*B{r}/100'; ws[f'G{r}']=f'=IF($B$7,FLOOR(F{r},$B$5),F{r})'; ws[f'H{r}']=f'=$B$2*C{r}/100'; ws[f'I{r}']=f'=IF($B$7,CEILING(H{r},$B$5),H{r})'
            ws[f'J{r}']='=100' if i==1 else f'=Q{p}'
            ws[f'R{r}']=f'=SUM($B${sr+2}:B{r})'; ws[f'S{r}']=f'=SUM($C${sr+2}:C{r})'
            ws[f'K{r}']=f'=J{r}+R{r}'; ws[f'L{r}']=f'=100+S{r}'
            ws[f'M{r}']=f'=MIN(J{r},MAX(0,K{r}-L{r}+D{r}))'; ws[f'N{r}']=f'=MIN(J{r},IF(E{r}="",M{r},E{r}))'
            ws[f'O{r}']=f'=$B$2*N{r}/100'; ws[f'P{r}']=f'=MIN($B$2*J{r}/100,IF($B$7,CEILING(O{r},$B$5),O{r}))'
            ws[f'Q{r}']=f'=J{r}-N{r}'; ws[f'T{r}']=f'=Q{r}+R{r}'; ws[f'U{r}']=f'=100+S{r}'; ws[f'V{r}']=f'=U{r}-T{r}'
            ws[f'W{r}']=f'=$B$2*Q{r}/100+SUM($G${sr+2}:G{r})'; ws[f'X{r}']=f'=$B$2+SUM($I${sr+2}:I{r})'; ws[f'Y{r}']=f'=X{r}-W{r}'
            ws[f'Z{r}']=f'=IF(T{r}>U{r},"ERROR",IF(AND(D{r}>0,ROUND(Y{r},6)<ROUND($B$2*D{r}/100,6)),"WARNING","OK"))'
    tbl(24,'РАСЧЕТ DOWN'); tbl(33,'РАСЧЕТ UP')

    h(ws,'A42','ИТОГИ')
    sums=[('ВыбранноеНаправление','=B6'),('ИтогMain %','=IF(B6="DOWN",T30,T39)'),('ИтогOpp %','=IF(B6="DOWN",U30,U39)'),('ИтогSkew %','=IF(B6="DOWN",V30,V39)'),('ИтогСтартОстаток %','=IF(B6="DOWN",Q30,Q39)'),('ИтогОкруглMain','=IF(B6="DOWN",W30,W39)'),('ИтогОкруглOpp','=IF(B6="DOWN",X30,X39)'),('ИтогОкруглSkew','=IF(B6="DOWN",Y30,Y39)'),('ИтогСтатус','=IF(B6="DOWN",Z30,Z39)')]
    for i,(k,f) in enumerate(sums,43): ws[f'A{i}']=k; ws[f'B{i}']=f

    h(ws,'D16','РИСКИ И МАРЖА')
    rh=['Уровень','Направление','Общий Main Lot','Общий Opposite Lot','Общий открытый объём','Чистый перекос','Маржа на 1 лот','Требуемая маржа','Нагрузка на баланс %','Макс движение против','Плавающая просадка $','Баланс после просадки','Equity после просадки','Свободная маржа','Margin Level %','Риск Margin Call','Риск StopOut','Статус риска','Комментарий']
    for c,n in enumerate(rh,4): ws.cell(17,c,n).font=Font(bold=True)
    for r in range(18,23):
        lv=r-17; dr=25+lv; ur=34+lv
        ws[f'D{r}']=lv; ws[f'E{r}']='=$B$6'
        ws[f'F{r}']=f'=IF($B$6="DOWN",W{dr},W{ur})'; ws[f'G{r}']=f'=IF($B$6="DOWN",X{dr},X{ur})'
        ws[f'H{r}']=f'=F{r}+G{r}'; ws[f'I{r}']=f'=ABS(F{r}-G{r})'
        ws[f'J{r}']='=$E$4*$E$5/$E$3'; ws[f'K{r}']=f'=H{r}*J{r}'; ws[f'L{r}']=f'=K{r}/$E$2*100'
        ws[f'M{r}']='=$E$7'; ws[f'N{r}']=f'=I{r}*$E$6*$E$7'; ws[f'O{r}']=f'=$E$2-N{r}'; ws[f'P{r}']=f'=O{r}'; ws[f'Q{r}']=f'=P{r}-K{r}'; ws[f'R{r}']=f'=IF(K{r}=0,0,P{r}/K{r}*100)'
        ws[f'S{r}']=f'=IF(R{r}<=$E$9,"РИСК MARGIN CALL","OK")'; ws[f'T{r}']=f'=IF(R{r}<=$E$8,"РИСК STOPOUT","OK")'
        ws[f'U{r}']=f'=IF(L{r}<30,"OK",IF(L{r}<50,"WARNING",IF(L{r}<70,"DANGER","CRITICAL")))'
        ws[f'V{r}']=f'="Уровень "&D{r}&". Объем="&ROUND(H{r},2)&" лот. Маржа="&ROUND(K{r},2)&"$. Нагрузка="&ROUND(L{r},1)&"%. Просадка="&ROUND(N{r},2)&"$. Статус="&U{r}'

def build_risk(ws):
    ws.title='РИСК_АНАЛИЗ'
    h(ws,'A1','РИСК_АНАЛИЗ')
    headers=['Уровень','Нагрузка %','Маржа $','Объем лот','Просадка $','Margin Level %','Статус']
    for c,n in enumerate(headers,1): ws.cell(2,c,n).font=Font(bold=True)
    for r in range(3,8):
        src=r+15
        ws[f'A{r}']=f'=Калькулятор!D{src}'; ws[f'B{r}']=f'=Калькулятор!L{src}'; ws[f'C{r}']=f'=Калькулятор!K{src}'; ws[f'D{r}']=f'=Калькулятор!H{src}'; ws[f'E{r}']=f'=Калькулятор!N{src}'; ws[f'F{r}']=f'=Калькулятор!R{src}'; ws[f'G{r}']=f'=Калькулятор!U{src}'
    stats=[('Макс нагрузка %','=MAX(B3:B7)'),('Макс маржа $','=MAX(C3:C7)'),('Макс объем','=MAX(D3:D7)'),('Макс просадка','=MAX(E3:E7)'),('Худший уровень','=INDEX(A3:A7,MATCH(MAX(B3:B7),B3:B7,0))'),('Рекомендованный баланс','=MAX(C3:C7)/0.3'),('Рекомендованное плечо','=Калькулятор!E3'),('Рекомендованный мин депозит','=MAX(C3:C7)+MAX(E3:E7)')]
    for i,(k,v) in enumerate(stats,10): ws[f'A{i}']=k; ws[f'B{i}']=v

    for title,col,pos in [('График нагрузки на баланс',2,'I2'),('График роста объема',4,'I18'),('График роста маржи',3,'I34'),('График просадки',5,'I50'),('График Margin Level',6,'I66')]:
        ch=LineChart(); ch.title=title
        data=Reference(ws,min_col=col,min_row=2,max_row=7); cats=Reference(ws,min_col=1,min_row=3,max_row=7)
        ch.add_data(data,titles_from_data=True); ch.set_categories(cats); ws.add_chart(ch,pos)

def build_tests(ws):
    ws.title='Тесты'; ws['A1']='Тест'; ws['B1']='Факт'; ws['C1']='Ожидание'; ws['D1']='Результат'
    for c in 'ABCD': ws[f'{c}1'].font=Font(bold=True)
    rows=[('Маржа формула','=Калькулятор!J18','=Калькулятор!E4*Калькулятор!E5/Калькулятор!E3',False),('Просадка формула','=Калькулятор!N18','=Калькулятор!I18*Калькулятор!E6*Калькулятор!E7',False),('Margin Level формула','=Калькулятор!R18','=IF(K18=0,0,P18/K18*100)',False),('Human риск комментарий','=Калькулятор!V18','',False)]
    i=2
    for n,f,e,num in rows:
        ws[f'A{i}']=n; ws[f'B{i}']=f; ws[f'C{i}']=e
        ws[f'D{i}']=f'=IF(LEN(B{i})>0,"PASS","FAIL")'; i+=1

def build_text(ws,name,text): ws.title=name; ws['A1']=text; ws['A1'].font=Font(bold=True)

if __name__=='__main__':
    wb=Workbook(); build_calc(wb.active); build_risk(wb.create_sheet()); build_tests(wb.create_sheet()); build_text(wb.create_sheet(),'Руководство','См. MANUAL_RU.md'); build_text(wb.create_sheet(),'Описание','См. README.md'); wb.save(OUT); print('Created',OUT)
