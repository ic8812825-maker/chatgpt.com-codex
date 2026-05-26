# MinusLock_Self_Compressing_Recovery_Calculator

Новый отдельный проект Excel-калькулятора самосжимающегося разруливания замка.

## Главное отличие от старого калькулятора
Старый подход считал уровни от фиксированного `StartLot`. Новый подход пересчитывает базу на каждом уровне:
- `NearStart(n+1) = NearStart(n) - Big + Small`
- В raw-логике это эквивалентно `NearStart(n+1) = NearStart(n) × 50%`.

## Модель 90/40/30
- `Big Raw = NearStart × 90%`
- `Small Raw = NearStart × 40%`
- `Max Close Far = NearStart × 30%`
- `Actual Close Far` зависит от `CloseMode`:
  - `THEORETICAL`: `MIN(MaxCloseFar, FarRemainingBefore)`
  - `SAFE_PROFIT_BUDGET`: `MIN(MaxCloseFar, CloseByProfitBudget, FarRemainingBefore)`

## Запуск
```bash
pip install -r requirements.txt
python create_self_compressing_calculator.py
python validate_self_compressing_calculator.py
python smoke_check_self_compressing_excel.py
```

## Excel
Откройте файл `MinusLock_Self_Compressing_Recovery_Calculator.xlsx`.
Листы:
- `Калькулятор`
- `РИСК_АНАЛИЗ`
- `Тесты`
- `Руководство`
- `Описание`

## Что проверяется
- фактический `Actual Close Far Lot` в режиме `THEORETICAL` равен 30% от `NearStart`;
- StartLot-сценарии 1/2/5;
- риск-блок не пустой;
- нет Excel-ошибок.
