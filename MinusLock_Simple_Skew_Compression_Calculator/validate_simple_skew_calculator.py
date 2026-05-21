from pathlib import Path
from openpyxl import load_workbook

f=Path(__file__).resolve().parent/'MinusLock_Simple_Skew_Compression_Calculator.xlsx'

def die(m): print('VALIDATION FAILED:',m); raise SystemExit(1)
def ok(c,m):
    if not c: die(m)

wb=load_workbook(f,data_only=False)
for s in ['Калькулятор','РИСК_АНАЛИЗ','Тесты','Руководство','Описание']:
    ok(s in wb.sheetnames,f'нет листа {s}')
c=wb['Калькулятор']; r=wb['РИСК_АНАЛИЗ']; t=wb['Тесты']
for cell in ['Q26','T26','U26','V26','Q30','T30','U30','V30','J18','K18','L18','N18','R18','U18','V18']:
    ok(c[cell].value is not None,f'пусто {cell}')
ok(c['T30'].value=='=Q30+R30','формула T30')
ok(c['U30'].value=='=100+S30','формула U30')
ok(c['V30'].value=='=U30-T30','формула V30')
ok(c['L18'].value=='=K18/$E$2*100','формула нагрузка')
ok(c['N18'].value=='=I18*$E$6*$E$7','формула просадки')
ok(c['R18'].value=='=IF(K18=0,0,P18/K18*100)','формула margin level')
ok('Уровень'==r['A2'].value,'заголовок риск')
ok(len(r._charts)>=5,'нет графиков')
# docs checks
m=Path(__file__).resolve().parent/'MANUAL_RU.md'; rd=Path(__file__).resolve().parent/'README.md'
ok(m.exists(),'нет MANUAL_RU.md'); ok(rd.exists(),'нет README.md')
mt=m.read_text(encoding='utf-8'); rt=rd.read_text(encoding='utf-8')
for key in ['ПАРАМЕТРЫ','СЕТКА УРОВНЕЙ','DOWN','UP','SUMMARY','HUMAN','StartLot = 1','StartLot = 2','StartLot = 5']:
    ok(key in mt,f'в мануале нет {key}')
ok('MANUAL_RU.md' in rt,'README без ссылки на MANUAL_RU.md')
print('ALL TESTS PASSED')
