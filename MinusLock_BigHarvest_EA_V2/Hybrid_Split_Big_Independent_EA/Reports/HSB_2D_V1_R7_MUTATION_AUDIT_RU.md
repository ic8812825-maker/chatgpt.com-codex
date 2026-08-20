# Mutation audit HSB.2D-V1-R7

Каталог M001–M185 непрерывен, все записи required. Runner вычисляет required set из каталога и требует равенства required/executed/caught. Итог: 185/185 CAUGHT, survived/invalid/not-applied/wrong/infrastructure sets пусты. M166 (`< || >` + ранний unauthorized NO_OP) завершил verifier с nonzero exit, S028 присутствовал в actual failures, manifest остался PASS.
