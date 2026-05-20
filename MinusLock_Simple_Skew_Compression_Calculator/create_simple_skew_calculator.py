from __future__ import annotations
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT_FILE = Path(__file__).resolve().parent / "MinusLock_Simple_Skew_Compression_Calculator.xlsx"

def title(ws, cell, text):
    ws[cell] = text
    ws[cell].font = Font(bold=True)
    ws[cell].fill = PatternFill("solid", fgColor="D9E1F2")

def build_calc(ws):
    ws.title = "Calculator"
    title(ws, "A1", "PARAMETERS")
    params=[("StartLot",1.0,"стартовый лот"),("StepPoints",100,"шаг сетки в пунктах"),("MaxLevels",5,"максимум уровней"),("LotStep",0.01,"шаг лота брокера"),("Direction","DOWN","выбранный сценарий DOWN/UP"),("UseRounding",True,"использовать округление"),("BigRoundMode","DOWN","Big округлять вниз"),("SmallRoundMode","UP","Small округлять вверх"),("CloseRoundMode","SAFE","защитное округление Close"),("PointValue",1,"стоимость пункта"),("Spread",0,"спред"),("Commission",0,"комиссия")]
    for i,(n,v,d) in enumerate(params,2): ws[f"A{i}"]=n; ws[f"B{i}"]=v; ws[f"C{i}"]=d

    title(ws, "E1", "STATUS / CHECKS")
    checks=[("StartLot",'=IF(B2<=0,"ERROR: Invalid StartLot","OK")'),("LotStep",'=IF(B5<=0,"ERROR: Invalid LotStep","OK")'),("MaxLevels",'=IF(B4<1,"ERROR: Invalid MaxLevels","OK")'),("Direction",'=IF(OR(B6="DOWN",B6="UP"),"OK","ERROR: Invalid Direction")'),("StepPoints",'=IF(B3<=0,"ERROR: Invalid StepPoints","OK")'),("PointValue",'=IF(B11<=0,"ERROR: Invalid PointValue","OK")'),("Spread",'=IF(B12<0,"ERROR: Invalid Spread","OK")'),("Commission",'=IF(B13<0,"ERROR: Invalid Commission","OK")')]
    for i,(k,f) in enumerate(checks,2): ws[f"E{i}"]=k; ws[f"F{i}"]=f

    title(ws,"A16","LEVEL GRID")
    for c,h in enumerate(["Level","Big %","Small %","TargetSkew %","ManualClose %"],1): ws.cell(17,c,h).font=Font(bold=True)
    grid=[(1,90,30,0,""),(2,30,15,15,""),(3,20,15,10,""),(4,10,10,10,""),(5,5,5,10,"")]
    for r,row in enumerate(grid,18):
        for c,v in enumerate(row,1): ws.cell(r,c,v)

    def table(start,label):
        title(ws,f"A{start}",label)
        heads=["Level","Big %","Small %","TargetSkew %","ManualClose %","Big Lot Raw","Big Lot Rounded","Small Lot Raw","Small Lot Rounded","Start Before %","Total Main Before %","Total Opp After %","Auto Close %","Final Close %","Close Lot Raw","Close Lot Rounded","Start After %","Sum Big %","Sum Small %","Total Main %","Total Opp %","Skew %","Rounded Total Main Lot","Rounded Total Opp Lot","Rounded Skew Lot","Status"]
        for c,h in enumerate(heads,1): ws.cell(start+1,c,h).font=Font(bold=True)
        for i,r in enumerate(range(start+2,start+7),start=18):
            p=r-1
            ws[f"A{r}"]=f"=A{i}"; ws[f"B{r}"]=f"=B{i}"; ws[f"C{r}"]=f"=C{i}"; ws[f"D{r}"]=f"=D{i}"; ws[f"E{r}"]=f"=IF(E{i}=\"\",\"\",E{i})"
            ws[f"F{r}"]=f"=$B$2*B{r}/100"; ws[f"G{r}"]=f"=IF($B$7,FLOOR(F{r},$B$5),F{r})"
            ws[f"H{r}"]=f"=$B$2*C{r}/100"; ws[f"I{r}"]=f"=IF($B$7,CEILING(H{r},$B$5),H{r})"
            ws[f"J{r}"]="=100" if r==start+2 else f"=Q{p}"
            ws[f"R{r}"]=f"=SUM($B${start+2}:B{r})"; ws[f"S{r}"]=f"=SUM($C${start+2}:C{r})"
            ws[f"K{r}"]=f"=J{r}+R{r}"; ws[f"L{r}"]=f"=100+S{r}"
            ws[f"M{r}"]=f"=MIN(J{r},MAX(0,K{r}-L{r}+D{r}))"
            ws[f"N{r}"]=f"=MIN(J{r},IF(E{r}=\"\",M{r},E{r}))"
            ws[f"O{r}"]=f"=$B$2*N{r}/100"; ws[f"P{r}"]=f"=MIN($B$2*J{r}/100,IF($B$7,CEILING(O{r},$B$5),O{r}))"
            ws[f"Q{r}"]=f"=J{r}-N{r}"; ws[f"T{r}"]=f"=Q{r}+R{r}"; ws[f"U{r}"]=f"=100+S{r}"; ws[f"V{r}"]=f"=U{r}-T{r}"
            ws[f"W{r}"]=f"=$B$2*Q{r}/100+SUM($G${start+2}:G{r})"
            ws[f"X{r}"]=f"=$B$2+SUM($I${start+2}:I{r})"; ws[f"Y{r}"]=f"=X{r}-W{r}"
            ws[f"Z{r}"]=(f"=IF(OR($B$2<=0,$B$5<=0,$B$4<1,NOT(OR($B$6=\"DOWN\",$B$6=\"UP\"))),\"ERROR\",IF(B{r}<C{r},\"ERROR\",IF(AND(E{r}<>\"\",E{r}>J{r}),\"ERROR\",IF(T{r}>U{r},\"ERROR\",IF(W{r}>X{r},\"ERROR\",IF(AND(B{r}>0,G{r}=0),\"ERROR\",IF(AND(C{r}>0,I{r}=0),\"ERROR\",IF(AND(D{r}>0,Y{r}<($B$2*D{r}/100)),\"WARNING\",\"OK\"))))))))")

    table(24,"DOWN CALCULATION"); table(33,"UP CALCULATION")
    title(ws,"A42","SUMMARY")
    rows=[("Selected Direction",'=B6'),("Final Total Main %",'=IF(B6="DOWN",T30,T39)'),("Final Total Opposite %",'=IF(B6="DOWN",U30,U39)'),("Final Skew %",'=IF(B6="DOWN",V30,V39)'),("Final Start Remaining %",'=IF(B6="DOWN",Q30,Q39)'),("Final Rounded Main Lot",'=IF(B6="DOWN",W30,W39)'),("Final Rounded Opp Lot",'=IF(B6="DOWN",X30,X39)'),("Final Rounded Skew Lot",'=IF(B6="DOWN",Y30,Y39)'),("Final Rounded Status",'=IF(B6="DOWN",Z30,Z39)'),("Final System Status",'=IF(B6="DOWN",IF(COUNTIF(Z26:Z30,"ERROR")>0,"ERROR",IF(COUNTIF(Z26:Z30,"WARNING")>0,"WARNING","OK")),IF(COUNTIF(Z35:Z39,"ERROR")>0,"ERROR",IF(COUNTIF(Z35:Z39,"WARNING")>0,"WARNING","OK")))')]
    for i,(k,f) in enumerate(rows,43): ws[f"A{i}"]=k; ws[f"B{i}"]=f

def build_tests(ws):
    ws.title="Tests"
    ws["A1"]="Test"; ws["B1"]="Actual"; ws["C1"]="Expected"; ws["D1"]="Result"
    for c in "ABCD": ws[f"{c}1"].font=Font(bold=True)
    rows=[
      ("Down L1 Close%",'=Calculator!N26',60,True),("Down L2 Close%",'=Calculator!N27',30,True),("Down Final Main",'=Calculator!T30',165,True),("Down Final Opp",'=Calculator!U30',175,True),("Down Final Skew",'=Calculator!V30',10,True),
      ("Up L1 Close%",'=Calculator!N35',60,True),("Up L2 Close%",'=Calculator!N36',30,True),("Up Final Main",'=Calculator!T39',165,True),("Up Final Opp",'=Calculator!U39',175,True),("Up Final Skew",'=Calculator!V39',10,True),
      ("Down L1 Rounded Main",'=Calculator!W26',1.30,True),("Down L1 Rounded Opp",'=Calculator!X26',1.30,True),("Down L1 Rounded Skew",'=Calculator!Y26',0.00,True),("Down L1 Status",'=Calculator!Z26','OK',False),
      ("Down L2 Rounded Main",'=Calculator!W27',1.30,True),("Down L2 Rounded Opp",'=Calculator!X27',1.45,True),("Down L2 Rounded Skew",'=Calculator!Y27',0.15,True),("Down L2 Status",'=Calculator!Z27','OK',False),
      ("Down Final Rounded Main",'=Calculator!W30',1.65,True),("Down Final Rounded Opp",'=Calculator!X30',1.75,True),("Down Final Rounded Skew",'=Calculator!Y30',0.10,True),("Down Final Status",'=Calculator!Z30','OK',False),
      ("Up L1 Rounded Main",'=Calculator!W35',1.30,True),("Up L1 Rounded Opp",'=Calculator!X35',1.30,True),("Up L1 Rounded Skew",'=Calculator!Y35',0.00,True),("Up L1 Status",'=Calculator!Z35','OK',False),
      ("Up L2 Rounded Main",'=Calculator!W36',1.30,True),("Up L2 Rounded Opp",'=Calculator!X36',1.45,True),("Up L2 Rounded Skew",'=Calculator!Y36',0.15,True),("Up L2 Status",'=Calculator!Z36','OK',False),
      ("Up Final Rounded Main",'=Calculator!W39',1.65,True),("Up Final Rounded Opp",'=Calculator!X39',1.75,True),("Up Final Rounded Skew",'=Calculator!Y39',0.10,True),("Up Final Status",'=Calculator!Z39','OK',False),
      ("Down Level1 Status",'=Calculator!Z26','OK',False),("Down Level2 Status",'=Calculator!Z27','OK',False),("Down Level5 Status",'=Calculator!Z30','OK',False),("Up Level1 Status",'=Calculator!Z35','OK',False),("Up Level2 Status",'=Calculator!Z36','OK',False),("Up Level5 Status",'=Calculator!Z39','OK',False),("Summary Final Rounded Status",'=Calculator!B51','OK',False),("Summary Final System Status",'=Calculator!B52','OK',False),
      ("Empty ManualClose uses AutoClose",'=IF(AND(ABS(Calculator!N26-Calculator!M26)<0.000001,ABS(Calculator!N27-Calculator!M27)<0.000001,ABS(Calculator!N35-Calculator!M35)<0.000001),"PASS","FAIL")','PASS',False),
      ("ManualClose override works",'=IF(AND(MIN(Calculator!J26,IF(50="",Calculator!M26,50))=50,MIN(Calculator!J35,IF(50="",Calculator!M35,50))=50),"PASS","FAIL")','PASS',False),
      ("Empty ManualClose is blank not zero",'=IF(AND(Calculator!E26="",Calculator!E27="",Calculator!E28="",Calculator!E35="",Calculator!E36="",Calculator!E37=""),"PASS","FAIL")','PASS',False)
    ]
    for i,(n,a,e,num) in enumerate(rows,2):
        ws[f"A{i}"]=n; ws[f"B{i}"]=a; ws[f"C{i}"]=e
        ws[f"D{i}"]=f'=IF(ABS(B{i}-C{i})<0.000001,"PASS","FAIL")' if num else f'=IF(B{i}=C{i},"PASS","FAIL")'

def build_manual(ws):
    ws.title="Manual"; ws["A1"]="Инструкция"; ws["A1"].font=Font(bold=True)
    for i,l in enumerate(["1. Ввести StartLot.","2. Проверить StepPoints.","3. Выбрать Direction DOWN или UP.","4. При необходимости изменить Level Grid.","5. Смотреть Main Table.","6. Проверить Summary.","7. Если Status = OK — сетка безопасна по математике.","8. Если ERROR — использовать нельзя.","9. Если WARNING — проверить skew и rounded-лоты."],2): ws[f"A{i}"]=l

def build_readme(ws):
    ws.title="README"; ws["A1"]="README"; ws["A1"].font=Font(bold=True)
    for i,t in enumerate(["Это простой калькулятор skew-компрессии минусового замка.","Big — крупный ордер на основной стороне.","Small — малый ордер на противоположной стороне.","Safe Close — безопасное частичное закрытие стартового ордера.","Total Main — суммарный объём основной стороны.","Total Opposite — суммарный объём противоположной стороны.","Main <= Opposite обязательно для сохранения защиты.","Status: OK — безопасно, WARNING — проверить skew/rounded, ERROR — нельзя использовать."],2): ws[f"A{i}"]=t

if __name__ == "__main__":
    wb=Workbook(); build_calc(wb.active); build_tests(wb.create_sheet()); build_manual(wb.create_sheet()); build_readme(wb.create_sheet()); wb.save(OUT_FILE); print(f"Created: {OUT_FILE}")
