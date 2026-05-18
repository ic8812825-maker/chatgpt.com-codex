from pathlib import Path
from openpyxl import load_workbook

WB = Path('MinusLock_Percent_Grid_Calculator.xlsx')
RPT = Path('PERCENT_GRID_VALIDATION_REPORT_V3_RU.md')


def ok(flag):
    return 'OK' if flag else 'ERROR'


def main():
    wb = load_workbook(WB)
    must = ['Settings','DownTrend','UpTrend','Summary','Checks','Manual','MarketModel','AdaptiveEngine','MarginControl','MonteCarlo','EquityModel','RecoveryMap','StressTest','RiskDashboard']
    sheets_ok = all(s in wb.sheetnames for s in must)

    s = wb['Settings']; mm = wb['MarketModel']; ae = wb['AdaptiveEngine']; mc = wb['MarginControl']; rd = wb['RiskDashboard']; sm = wb['Summary']

    settings_v3_ok = all(s[f'B{i}'].value is not None for i in range(11,19))
    dynamic_step_ok = mm['B16'].value == '=B3*B4'
    adaptive_formulas_ok = isinstance(ae['B17'].value, str) and 'EXP' in ae['B17'].value
    rounded_cols_ok = all(wb['DownTrend'][c+'1'].value is not None for c in ['AD','AE','AF','AG','AH','AI','AJ'])
    margin_formulas_ok = mc['B12'].value == '=B9*B5' and mc['B13'].value == '=B8/B3*100'
    risk_score_ok = isinstance(rd['B4'].value, str) and 'MIN(100' in rd['B4'].value
    adaptive_stop_ok = isinstance(rd['B8'].value, str) and 'STOP NEW LEVELS' in rd['B8'].value

    monte_rows_ok = wb['MonteCarlo'].max_row >= 10
    recovery_rows_ok = wb['RecoveryMap'].max_row >= 9
    stress_rows_ok = wb['StressTest'].max_row >= 10
    charts_ok = len(sm._charts) >= 10
    aj_down_ok = isinstance(wb['DownTrend']['AJ3'].value, str) and '"WARNING"' in wb['DownTrend']['AJ3'].value and 'J3>0' in wb['DownTrend']['AJ3'].value
    aj_up_ok = isinstance(wb['UpTrend']['AJ3'].value, str) and 'J3>0' in wb['UpTrend']['AJ3'].value
    summary_formula = sm['B15'].value if isinstance(sm['B15'].value, str) else ""
    summary_switch_ok = isinstance(sm['B5'].value, str) and 'Settings!$B$10' in sm['B5'].value and isinstance(sm['B15'].value,str) and 'Settings!$B$10' in sm['B15'].value and isinstance(sm['B16'].value,str) and 'Settings!$B$10' in sm['B16'].value
    summary_universal_error_ok = ('LEFT(IF(Settings!$B$10=' in summary_formula and '),5)="ERROR"' in summary_formula and '),7)="WARNING"' in summary_formula and 'Rounding broke protection balance' not in summary_formula)

    report = f'''# PERCENT_GRID_VALIDATION_REPORT_V3_RU

## 1. Adaptive formulas
- AdaptiveEngine formulas: **{ok(adaptive_formulas_ok)}**.

## 2. Dynamic step
- MarketModel!B16 = ATR × Multiplier: **{ok(dynamic_step_ok)}**.

## 3. Monte Carlo outputs
- MonteCarlo scenarios table present: **{ok(monte_rows_ok)}**.

## 4. Margin calculations
- RequiredMargin/MarginLoad formulas present: **{ok(margin_formulas_ok)}**.

## 5. Recovery calculations
- RecoveryMap rows present: **{ok(recovery_rows_ok)}**.

## 6. Risk score
- RiskDashboard risk score formula present: **{ok(risk_score_ok)}**.

## 7. Adaptive skew
- AdaptiveEngine dynamic skew column present: **{ok(ae['D17'].value is not None)}**.

## 8. Adaptive level stop
- RiskDashboard adaptive stop formula present: **{ok(adaptive_stop_ok)}**.

## 9. Stress tests
- StressTest scenario table present: **{ok(stress_rows_ok)}**.

## 10. Rounded risk logic
- Rounded total columns AD:AJ present: **{ok(rounded_cols_ok)}**.
- DownTrend AJ3 baseline condition fix (J>0 gate): **{ok(aj_down_ok)}**.
- UpTrend AJ3 baseline condition fix (J>0 gate): **{ok(aj_up_ok)}**.

## 11. Summary direction-switch
- Summary uses IF(Settings!Direction...) for final fields/statuses: **{ok(summary_switch_ok)}**.
- Final Summary Status universal ERROR/WARNING handling: **{ok(summary_universal_error_ok)}**.

## 12. Dashboard integrity
- Required V3 sheets exist: **{ok(sheets_ok)}**.
- Summary charts count >= 10: **{ok(charts_ok)}** (found: {len(sm._charts)}).
- V3 settings block present (B11:B18): **{ok(settings_v3_ok)}**.

## Итоговый вердикт
**{ok(all([sheets_ok, settings_v3_ok, dynamic_step_ok, adaptive_formulas_ok, rounded_cols_ok, margin_formulas_ok, risk_score_ok, adaptive_stop_ok, monte_rows_ok, recovery_rows_ok, stress_rows_ok, charts_ok, aj_down_ok, aj_up_ok, summary_switch_ok, summary_universal_error_ok]))}**
'''

    RPT.write_text(report, encoding='utf-8')
    print(report)


if __name__ == '__main__':
    main()
