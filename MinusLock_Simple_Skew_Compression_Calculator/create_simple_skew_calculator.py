from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = Path(__file__).resolve().parent / "MinusLock_Simple_Skew_Compression_Calculator.xlsx"

def head(ws,c,t):
    ws[c]=t; ws[c].font=Font(bold=True); ws[c].fill=PatternFill('solid',fgColor='D9E1F2')

def build_calc(ws):
    ws.title='Calculator'
    head(ws,'A1','PARAMETERS')
    params=[('StartLot',1.0),('StepPoints',100),('MaxLevels',5),('LotStep',0.01),('Direction','DOWN'),('UseRounding',True)]
    for i,(k,v) in enumerate(params,2): ws[f'A{i}']=k; ws[f'B{i}']=v
    ws['A8']='BigRoundMode';ws['B8']='DOWN';ws['A9']='SmallRoundMode';ws['B9']='UP';ws['A10']='CloseRoundMode';ws['B10']='SAFE';ws['A11']='PointValue';ws['B11']=1;ws['A12']='Spread';ws['B12']=0;ws['A13']='Commission';ws['B13']=0

    head(ws,'A16','LEVEL GRID')
    for c,h in enumerate(['Level','Big %','Small %','TargetSkew %','ManualClose %'],1): ws.cell(17,c,h).font=Font(bold=True)
    grid=[(1,90,30,0,''),(2,30,15,15,''),(3,20,15,10,''),(4,10,10,10,''),(5,5,5,10,'')]
    for r,row in enumerate(grid,18):
        for c,v in enumerate(row,1): ws.cell(r,c,v)

    def table(sr,label):
        head(ws,f'A{sr}',label)
        cols=['Level','Big %','Small %','TargetSkew %','ManualClose %','Big Lot Raw','Big Lot Rounded','Small Lot Raw','Small Lot Rounded','Start Before %','Total Main Before %','Total Opp After %','Auto Close %','Final Close %','Close Lot Raw','Close Lot Rounded','Start After %','Sum Big %','Sum Small %','Total Main %','Total Opp %','Skew %','Rounded Total Main Lot','Rounded Total Opp Lot','Rounded Skew Lot','Status']
        for c,h in enumerate(cols,1): ws.cell(sr+1,c,h).font=Font(bold=True)
        for idx,r in enumerate(range(sr+2,sr+7),1):
            lvl=17+idx; prev=r-1
            ws[f'A{r}']=f'=A{lvl}'; ws[f'B{r}']=f'=B{lvl}'; ws[f'C{r}']=f'=C{lvl}'; ws[f'D{r}']=f'=D{lvl}'; ws[f'E{r}']=f'=IF(E{lvl}="","",E{lvl})'
            ws[f'F{r}']=f'=$B$2*B{r}/100'; ws[f'G{r}']=f'=IF($B$7,FLOOR(F{r},$B$5),F{r})'; ws[f'H{r}']=f'=$B$2*C{r}/100'; ws[f'I{r}']=f'=IF($B$7,CEILING(H{r},$B$5),H{r})'
            ws[f'J{r}']='=100' if idx==1 else f'=Q{prev}'
            ws[f'R{r}']=f'=SUM($B${sr+2}:B{r})'; ws[f'S{r}']=f'=SUM($C${sr+2}:C{r})'
            ws[f'K{r}']=f'=J{r}+R{r}'; ws[f'L{r}']=f'=100+S{r}'
            ws[f'M{r}']=f'=MIN(J{r},MAX(0,K{r}-L{r}+D{r}))'; ws[f'N{r}']=f'=MIN(J{r},IF(E{r}="",M{r},E{r}))'
            ws[f'O{r}']=f'=$B$2*N{r}/100'; ws[f'P{r}']=f'=MIN($B$2*J{r}/100,IF($B$7,CEILING(O{r},$B$5),O{r}))'
            ws[f'Q{r}']=f'=J{r}-N{r}'; ws[f'T{r}']=f'=Q{r}+R{r}'; ws[f'U{r}']=f'=100+S{r}'; ws[f'V{r}']=f'=U{r}-T{r}'
            ws[f'W{r}']=f'=$B$2*Q{r}/100+SUM($G${sr+2}:G{r})'; ws[f'X{r}']=f'=$B$2+SUM($I${sr+2}:I{r})'; ws[f'Y{r}']=f'=X{r}-W{r}'
            ws[f'Z{r}']=(f'=IF(OR($B$2<=0,$B$5<=0,$B$4<1,NOT(OR($B$6="DOWN",$B$6="UP"))),"ERROR",IF(B{r}<C{r},"ERROR",IF(AND(E{r}<>"",E{r}>J{r}),"ERROR",IF(T{r}>U{r},"ERROR",IF(W{r}>X{r},"ERROR",IF(AND(B{r}>0,G{r}=0),"ERROR",IF(AND(C{r}>0,I{r}=0),"ERROR",IF(AND(D{r}>0,ROUND(Y{r},6)<ROUND($B$2*D{r}/100,6)),"WARNING","OK"))))))))')

    table(24,'DOWN CALCULATION'); table(33,'UP CALCULATION')
    head(ws,'A42','SUMMARY')
    sums=[('Selected Direction','=B6'),('Final Total Main %','=IF(B6="DOWN",T30,T39)'),('Final Total Opposite %','=IF(B6="DOWN",U30,U39)'),('Final Skew %','=IF(B6="DOWN",V30,V39)'),('Final Start Remaining %','=IF(B6="DOWN",Q30,Q39)'),('Final Rounded Main Lot','=IF(B6="DOWN",W30,W39)'),('Final Rounded Opp Lot','=IF(B6="DOWN",X30,X39)'),('Final Rounded Skew Lot','=IF(B6="DOWN",Y30,Y39)'),('Final Rounded Status','=IF(B6="DOWN",Z30,Z39)'),('Final System Status','=IF(B6="DOWN",IF(COUNTIF(Z26:Z30,"ERROR")>0,"ERROR",IF(COUNTIF(Z26:Z30,"WARNING")>0,"WARNING","OK")),IF(COUNTIF(Z35:Z39,"ERROR")>0,"ERROR",IF(COUNTIF(Z35:Z39,"WARNING")>0,"WARNING","OK")))')]
    for i,(k,f) in enumerate(sums,43): ws[f'A{i}']=k; ws[f'B{i}']=f

    head(ws,'A55','HUMAN-READABLE LEVEL SUMMARY')
    hh=['Level','Direction','Action Big','Big %','Big Lot','Action Small','Small %','Small Lot','Close Action','Close %','Close Lot','Start Remaining %','Start Remaining Lot','Total Main %','Total Opposite %','Skew %','Rounded Main Lot','Rounded Opp Lot','Rounded Skew Lot','Status','Human Comment']
    for c,h in enumerate(hh,1): ws.cell(56,c,h).font=Font(bold=True)
    for r in range(57,62):
        lvl=r-56; d=25+lvl; u=34+lvl
        ws[f'A{r}']=lvl; ws[f'B{r}']='=$B$6'; ws[f'C{r}']='=IF($B$6="DOWN","Open Big BUY","Open Big SELL")'; ws[f'D{r}']=f'=IF($B$6="DOWN",B{d},B{u})'; ws[f'E{r}']=f'=IF($B$6="DOWN",G{d},G{u})'
        ws[f'F{r}']='=IF($B$6="DOWN","Open Small SELL","Open Small BUY")'; ws[f'G{r}']=f'=IF($B$6="DOWN",C{d},C{u})'; ws[f'H{r}']=f'=IF($B$6="DOWN",I{d},I{u})'
        ws[f'I{r}']='=IF($B$6="DOWN","Close Start BUY","Close Start SELL")'; ws[f'J{r}']=f'=IF($B$6="DOWN",N{d},N{u})'; ws[f'K{r}']=f'=IF($B$6="DOWN",P{d},P{u})'; ws[f'L{r}']=f'=IF($B$6="DOWN",Q{d},Q{u})'
        ws[f'M{r}']=f'=$B$2*L{r}/100'; ws[f'N{r}']=f'=IF($B$6="DOWN",T{d},T{u})'; ws[f'O{r}']=f'=IF($B$6="DOWN",U{d},U{u})'; ws[f'P{r}']=f'=IF($B$6="DOWN",V{d},V{u})'
        ws[f'Q{r}']=f'=IF($B$6="DOWN",W{d},W{u})'; ws[f'R{r}']=f'=IF($B$6="DOWN",X{d},X{u})'; ws[f'S{r}']=f'=IF($B$6="DOWN",Y{d},Y{u})'; ws[f'T{r}']=f'=IF($B$6="DOWN",Z{d},Z{u})'
        ws[f'U{r}']=f'="Level "&A{r}&": "&IF($B$6="DOWN","price goes DOWN. ","price goes UP. ")&C{r}&" "&ROUND(E{r},2)&" lot, "&F{r}&" "&ROUND(H{r},2)&" lot, "&I{r}&" "&ROUND(K{r},2)&" lot. Start remains "&ROUND(M{r},2)&" lot. Total Main = "&N{r}&"%, Total Opposite = "&O{r}&"%, Skew = "&P{r}&"%, Status = "&T{r}&"."'

def build_human(ws):
    ws.title='HumanSummary'; head(ws,'A1','ИТОГОВЫЙ ЧЕЛОВЕЧЕСКИЙ РАСЧЁТ ВСЕХ УРОВНЕЙ')
    for c,h in enumerate(['Level','Direction','Action Big','Big %','Big Lot','Action Small','Small %','Small Lot','Close Action','Close %','Close Lot','Start Remaining %','Start Remaining Lot','Total Main %','Total Opposite %','Skew %','Rounded Main Lot','Rounded Opp Lot','Rounded Skew Lot','Status','Human Comment'],1): ws.cell(2,c,h).font=Font(bold=True)
    for r in range(3,8):
        src=r+54
        for col in 'ABCDEFGHIJKLMNOPQRSTU': ws[f'{col}{r}']=f'=Calculator!{col}{src}'
    head(ws,'A10','HUMAN TOTALS')
    totals=[('Sum Big Lots','=SUM(E3:E7)'),('Sum Small Lots','=SUM(H3:H7)'),('Sum Close Lots','=SUM(K3:K7)'),('Final Start Remaining Lot','=M7'),('Final Total Main %','=N7'),('Final Total Opposite %','=O7'),('Final Skew %','=P7'),('Final Rounded Main Lot','=Q7'),('Final Rounded Opp Lot','=R7'),('Final Rounded Skew Lot','=S7'),('Final Status','=T7')]
    for i,(k,v) in enumerate(totals,11): ws[f'A{i}']=k; ws[f'B{i}']=v

def build_tests(ws):
    ws.title='Tests'; ws['A1']='Test'; ws['B1']='Actual'; ws['C1']='Expected'; ws['D1']='Result'
    for c in 'ABCD': ws[f'{c}1'].font=Font(bold=True)
    rows=[('Down Q26','=Calculator!Q26',40),('Down T26','=Calculator!T26',130),('Down U26','=Calculator!U26',130),('Down V26','=Calculator!V26',0),('Down Q30','=Calculator!Q30',10),('Down T30','=Calculator!T30',165),('Down U30','=Calculator!U30',175),('Down V30','=Calculator!V30',10),('Up Q35','=Calculator!Q35',40),('Up T35','=Calculator!T35',130),('Up U35','=Calculator!U35',130),('Up V35','=Calculator!V35',0),('Up Q39','=Calculator!Q39',10),('Up T39','=Calculator!T39',165),('Up U39','=Calculator!U39',175),('Up V39','=Calculator!V39',10),('Summary Main','=Calculator!B44',165),('Summary Opp','=Calculator!B45',175),('Summary Skew','=Calculator!B46',10),('Human L1 Start Remaining Lot','=HumanSummary!M3',0.40),('Human L1 Total Main','=HumanSummary!N3',130),('Human L1 Total Opp','=HumanSummary!O3',130),('Human Sum Big','=HumanSummary!B11',1.55)]
    i=2
    for n,a,e in rows:
        ws[f'A{i}']=n; ws[f'B{i}']=a; ws[f'C{i}']=e; ws[f'D{i}']=f'=IF(ABS(B{i}-C{i})<0.000001,"PASS","FAIL")'; i+=1
    ws[f'A{i}']='Human Comment contains Total Main = 130'; ws[f'B{i}']='=IF(ISNUMBER(SEARCH("Total Main = 130",HumanSummary!U3)),"PASS","FAIL")'; ws[f'C{i}']='PASS'; ws[f'D{i}']=f'=IF(B{i}=C{i},"PASS","FAIL")'

def build_text(ws,name): ws.title=name; ws['A1']=name; ws['A1'].font=Font(bold=True)

if __name__=='__main__':
    wb=Workbook(); build_calc(wb.active); build_human(wb.create_sheet()); build_tests(wb.create_sheet()); build_text(wb.create_sheet(),'Manual'); build_text(wb.create_sheet(),'README'); wb.save(OUT); print(f'Created: {OUT}')
