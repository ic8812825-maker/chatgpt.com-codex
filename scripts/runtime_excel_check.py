from openpyxl import load_workbook
from copy import copy

SRC='recovery_lock_cascade_next_step.xlsx'
TMP='reports/tests/recovery_lock_runtime_case.xlsx'

wb=load_workbook(SRC)
# set test values
s=wb['Settings']
s['B11']=0
s['B12']=20
s['B13']=0
s['B14']=0
s['B19']='FULL_CYCLE'
# next section test inputs
tr=wb['TailRecovery_UP']
tr['B14']=0.14
tr['B15']=2
# basket close test inputs (override computed cells for runtime case)
bs=wb['BasketSummary']
bs['B3']=-12
bs['B4']=18
# close lot guard
tr['B6']='NO'
tr['B7']=100
tr['B5']=400

wb.save(TMP)
# open with data_only
wb2=load_workbook(TMP,data_only=True)
out={
 'tail_ticket_up': wb2['Scenario_UP']['B222'].value,
 'next_big': wb2['TailRecovery_UP']['B16'].value,
 'next_small': wb2['TailRecovery_UP']['B17'].value,
 'can_open_section_up': wb2['SectionCalculator_UP']['B14'].value,
 'cost_k21': wb2['SectionCalculator_UP']['K21'].value,
 'can_close_basket_up': wb2['BasketSummary']['B10'].value,
 'close_raw': wb2['TailRecovery_UP']['B8'].value,
 'close_final': wb2['TailRecovery_UP']['B10'].value,
 'close_allowed': wb2['TailRecovery_UP']['B11'].value,
}
print(out)
