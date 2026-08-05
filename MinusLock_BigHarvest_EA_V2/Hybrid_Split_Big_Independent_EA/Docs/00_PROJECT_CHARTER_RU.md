# Устав проекта Hybrid Split Big

Версия 1.0. Статус: нормативный.

## Назначение и область

Документ устанавливает неизменяемые границы поколения 1. Система является самостоятельным MQL5-проектом и реализует только Hybrid Split Big.

## Требования

- `HSBI-GEN-010`: единственный торговый runtime — `HYBRID_SPLIT_BIG_ONLY`.
- `HSBI-GEN-011`: Legacy Big, Legacy Small, отдельный Split Big, generic Big/Small и Legacy ReverseSmall запрещены.
- `HSBI-GEN-012`: `DUAL_TAIL` и два активных Far запрещены.
- `HSBI-GEN-013`: единственные основные роли — INITIAL_BUY, INITIAL_SELL, INITIAL_PLUS, FAR, BIG_CORE, BIG_TREND, SMALL_BASE, NEW_FAR.
- `HSBI-GEN-014`: NEW_FAR является переходной меткой; после commit нового цикла роль становится FAR.
- `HSBI-GEN-015`: MQL5 является production-языком; Python не является production-oracle.
- `HSBI-GEN-016`: старые StateMachine, TradeEngine и include не подключаются.
- `HSBI-GEN-017`: реальная торговля запрещена до всех production gates и отдельного решения пользователя.
- `HSBI-GEN-018`: исполняемый код запрещён на HSB.0.

## Preconditions / Postconditions

Preconditions: проект находится внутри разрешённого корня и ветки `work`. Postconditions: любой проектный артефакт обязан соответствовать Hybrid-only и иметь Requirement IDs.

## Запрещённые состояния и error route

Обнаружение Legacy role, второго Far, альтернативной Final Close authority или зависимости на старый include означает `DOCUMENT_CONFLICT`, блокирует HSB.1 и требует исправления документации.

## Restart, owner, тесты

Restart semantics для устава — документ перечитывается как неизменный контракт. Будущий MQL5 owner: `Core/RuntimeMode` и compile-time dependency guards. Тесты: поиск запрещённых include, runtime flags и ролей. Открытые числовые политики не входят в устав и фиксируются в реестре решений.