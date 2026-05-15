# MinusLock Percent Grid Calculator V3

Adaptive recovery/risk engine for minus-lock compression systems.

## Features
1. Percent-grid recovery engine
2. Risk-safe rounding
3. Adaptive skew
4. Adaptive ATR step
5. Monte Carlo scenarios
6. Margin control
7. Recovery map
8. Stress tests
9. Risk dashboard
10. Survival analysis

## Project structure
```text
MinusLock_Percent_Grid_Calculator/
│
├── MinusLock_Percent_Grid_Calculator.xlsx
├── create_percent_grid_excel.py
├── validate_percent_grid_calculator.py
├── PERCENT_GRID_VALIDATION_REPORT_RU.md
├── PERCENT_GRID_VALIDATION_REPORT_V2_RU.md
├── PERCENT_GRID_VALIDATION_REPORT_V3_RU.md
├── README.md
└── requirements.txt
```

## Run
```bash
pip install -r requirements.txt
python create_percent_grid_excel.py
python validate_percent_grid_calculator.py
```
