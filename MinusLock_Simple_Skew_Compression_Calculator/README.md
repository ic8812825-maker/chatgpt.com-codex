# MinusLock Simple Skew Compression Calculator

Простой Excel-калькулятор skew-компрессии минусового замка.

## Состав
- `MinusLock_Simple_Skew_Compression_Calculator.xlsx`
- `create_simple_skew_calculator.py`
- `validate_simple_skew_calculator.py`
- `requirements.txt`

## Что это
Калькулятор проверяет:
- SAFE CLOSE
- TOTAL MAIN <= TOTAL OPPOSITE
- ROUNDED LOT SAFETY
- START REMAINING
- SKEW

## Термины
- **Big**: крупный ордер на основной стороне.
- **Small**: малый ордер на противоположной стороне.
- **Safe Close**: безопасное частичное закрытие стартового ордера с контролем баланса.
- **Total Main**: сумма объема основной стороны.
- **Total Opposite**: сумма объема противоположной стороны.

## Статусы
- `OK`: условия соблюдены.
- `WARNING`: проверьте целевой skew/rounded-логику.
- `ERROR`: математика/безопасность нарушена.

## Запуск
```bash
pip install -r MinusLock_Simple_Skew_Compression_Calculator/requirements.txt -q
python MinusLock_Simple_Skew_Compression_Calculator/create_simple_skew_calculator.py
python MinusLock_Simple_Skew_Compression_Calculator/validate_simple_skew_calculator.py
```
