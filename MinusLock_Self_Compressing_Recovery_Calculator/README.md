# MinusLock Self-Compressing Recovery Calculator

Новый отдельный калькулятор: **MinusLock_Self_Compressing_Recovery_Calculator**.

Отличие от старого проекта: база каждого уровня самосжимается (`NearStart -> 50%`), а не считается от постоянного `StartLot`.

## Запуск
```bash
pip install -r requirements.txt
python create_self_compressing_calculator.py
python validate_self_compressing_calculator.py
python smoke_check_self_compressing_excel.py
```

Откройте `MinusLock_Self_Compressing_Recovery_Calculator.xlsx` в Excel.

## Что означает 90/40/30
- Big = 90% от NearStart
- Small = 40% от NearStart
- Close Far max = 30% от NearStart
- Следующий NearStart: `NearStart - Big + Small` (теоретически 50%)
