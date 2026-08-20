# R6 mutation audit

M001–M150 сохранены required. M151–M165 покрывают NO_OP bypass для decision/restart/barrier guards, неправильные S037 status/reason, double negation, Boolean comparison и unknown condition. Каталог непрерывен, runner сравнивает required/executed/caught sets.
