from pathlib import Path
from openpyxl import load_workbook

f = Path(__file__).resolve().parent / 'MinusLock_Simple_Skew_Compression_Calculator.xlsx'

ERROR_TOKENS = {"#NAME?", "#ИМЯ?", "#VALUE!", "#ЗНАЧ!", "#REF!", "#ССЫЛКА!", "#DIV/0!", "#Н/Д", "#N/A"}
RUS_SHEETS = ['Калькулятор', 'РИСК_АНАЛИЗ', 'Тесты', 'Руководство', 'Описание']


def die(m):
    print('VALIDATION FAILED:', m)
    raise SystemExit(1)


def ok(c, m):
    if not c:
        die(m)


def has_bad_sheet_ref(formula: str) -> bool:
    if not isinstance(formula, str) or not formula.startswith('='):
        return False
    for sh in RUS_SHEETS:
        if f'={sh}!' in formula or f'+{sh}!' in formula or f'-{sh}!' in formula or f'({sh}!' in formula:
            return True
    return False


wb = load_workbook(f, data_only=False)
wb_vals = load_workbook(f, data_only=True)

for s in RUS_SHEETS:
    ok(s in wb.sheetnames, f'нет листа {s}')

c = wb['Калькулятор']
r = wb['РИСК_АНАЛИЗ']
t = wb['Тесты']
cv = wb_vals['Калькулятор']
rv = wb_vals['РИСК_АНАЛИЗ']
tv = wb_vals['Тесты']

# 1) no formula errors/tokens and no bad unquoted russian references
for ws in wb.worksheets:
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            v = cell.value
            if isinstance(v, str):
                ok(v not in ERROR_TOKENS, f'{ws.title}!{cell.coordinate} содержит {v}')
                ok(not has_bad_sheet_ref(v), f'{ws.title}!{cell.coordinate} ссылка без кавычек: {v}')

# 2) expected formulas
ok(c['T30'].value == '=Q30+R30', 'формула T30')
ok(c['U30'].value == '=100+S30', 'формула U30')
ok(c['V30'].value == '=U30-T30', 'формула V30')
ok(c['R18'].value == '=Q18/$K$2*100', 'формула нагрузка')
ok(c['T18'].value == '=O18*$K$6*$K$7', 'формула просадки')
ok(c['X18'].value == '=IF(Q18=0,0,V18/Q18*100)', 'формула margin level')

# 3) risk/tests sheet integrity
ok(r['A2'].value == 'Уровень', 'заголовок риск')
ok(len(r._charts) >= 5, 'нет графиков риск-анализа')

# 4) data_only key values must be present and match baseline
expected = {
    'B44': 165, 'B45': 175, 'B46': 10,
    'B48': 1.65, 'B49': 1.75, 'B50': 0.10,
    'B51': 'OK', 'B73': 37.4, 'B72': 3740, 'B74': 750, 'B70': 'WARNING'
}
for cell, val in expected.items():
    got = cv[cell].value
    ok(got is not None, f'data_only пусто {cell}')
    if isinstance(val, (int, float)):
        ok(abs(float(got) - float(val)) < 1e-6, f'{cell}: ожидалось {val}, получено {got}')
    else:
        ok(str(got) == val, f'{cell}: ожидалось {val}, получено {got}')

# 5) risk block data_only no errors/empty level rows
for rr in range(3, 8):
    for cc in 'ABCDEFG':
        v = rv[f'{cc}{rr}'].value
        ok(v is not None, f'РИСК_АНАЛИЗ пусто {cc}{rr}')
        ok(str(v) not in ERROR_TOKENS, f'РИСК_АНАЛИЗ ошибка {cc}{rr}={v}')

# 6) tests must be PASS in data_only
for rr in range(2, 30):
    if tv[f'A{rr}'].value:
        res = tv[f'D{rr}'].value
        ok(res == 'PASS', f'Тесты!D{rr} не PASS ({res})')

# docs checks
m = Path(__file__).resolve().parent / 'MANUAL_RU.md'
rd = Path(__file__).resolve().parent / 'README.md'
ok(m.exists(), 'нет MANUAL_RU.md')
ok(rd.exists(), 'нет README.md')

print('ALL TESTS PASSED')
