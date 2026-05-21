from pathlib import Path
from openpyxl import load_workbook

f=Path(__file__).resolve().parent/'MinusLock_Simple_Skew_Compression_Calculator.xlsx'

def die(m):
 print('VALIDATION FAILED:',m); raise SystemExit(1)

def chk(c,m):
 if not c: die(m)

wb=load_workbook(f,data_only=False)

from pathlib import Path as _P
manual=_P(__file__).resolve().parent/'MANUAL_RU.md'
readme=_P(__file__).resolve().parent/'README.md'
chk(manual.exists(),'MANUAL_RU.md missing')
chk(readme.exists(),'README.md missing')
mt=manual.read_text(encoding='utf-8')
rt=readme.read_text(encoding='utf-8')
chk('MANUAL_RU.md' in rt,'README missing MANUAL_RU.md link')
for key in ['PARAMETERS','LEVEL GRID','DOWN CALCULATION','UP CALCULATION','SUMMARY','HUMAN-READABLE LEVEL SUMMARY','StartLot = 1','StartLot = 2','StartLot = 5']:
 chk(key in mt,f'MANUAL missing section: {key}')

c=wb['Calculator']; h=wb['HumanSummary']; t=wb['Tests']
for s in ['Calculator','HumanSummary','Tests','Manual','README']:
 chk(s in wb.sheetnames,f'missing {s}')
# core formulas present
for cell in ['Q26','T26','U26','V26','Q30','T30','U30','V30','Q35','T35','U35','V35','Q39','T39','U39','V39']:
 chk(c[cell].value is not None,f'empty {cell}')
# exact formulas for first row
chk(c['Q26'].value=='=J26-N26','Q26 formula')
chk(c['T26'].value=='=Q26+R26','T26 formula')
chk(c['U26'].value=='=100+S26','U26 formula')
chk(c['V26'].value=='=U26-T26','V26 formula')
# summary
chk(c['B44'].value=='=IF(B6="DOWN",T30,T39)','summary main formula')
chk(c['B45'].value=='=IF(B6="DOWN",U30,U39)','summary opp formula')
chk(c['B46'].value=='=IF(B6="DOWN",V30,V39)','summary skew formula')
# human references
chk(c['N57'].value=='=IF($B$6="DOWN",T26,T35)','human total main ref')
chk(c['O57'].value=='=IF($B$6="DOWN",U26,U35)','human total opp ref')
chk(c['P57'].value=='=IF($B$6="DOWN",V26,V35)','human skew ref')
chk(isinstance(c['U57'].value,str) and 'Total Main = ' in c['U57'].value and '#NAME' not in c['U57'].value and '#ИМЯ' not in c['U57'].value,'human comment formula')
# tests include critical
names=[t[f'A{i}'].value for i in range(2,t.max_row+1)]
for n in ['Down Q26','Down T30','Up T39','Human L1 Total Main','Human Comment contains Total Main = 130']:
 chk(n in names,f'missing test {n}')
print('ALL TESTS PASSED')
