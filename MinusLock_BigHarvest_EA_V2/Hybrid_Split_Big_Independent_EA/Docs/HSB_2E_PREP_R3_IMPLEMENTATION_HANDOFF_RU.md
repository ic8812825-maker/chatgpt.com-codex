# HSB.2E-PREP-R3 — административный implementation handoff

Этот документ не разрешает production implementation. Для каждого блока baseline определяется отдельным административным заданием; broker dispatch и real trading запрещены.

| № | Блок | Owner group | Reference | Formula/scenario | Vectors/tests | Dependencies | Acceptance | Dispatch/real |
|---:|---|---|---|---|---|---|---|---|
| 1 | типы и immutable inputs | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F001/SC01 | G/B/N001; T465 | previous blocks | reference vectors + invariants | NO/NO |
| 2 | identity/ownership | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F002/SC02 | G/B/N002; T466 | previous blocks | reference vectors + invariants | NO/NO |
| 3 | broker snapshot | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F003/SC03 | G/B/N003; T467 | previous blocks | reference vectors + invariants | NO/NO |
| 4 | price/volume normalization | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F004/SC04 | G/B/N004; T468 | previous blocks | reference vectors + invariants | NO/NO |
| 5 | money evaluator | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F005/SC05 | G/B/N005; T469 | previous blocks | reference vectors + invariants | NO/NO |
| 6 | geometry | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F006/SC06 | G/B/N006; T470 | previous blocks | reference vectors + invariants | NO/NO |
| 7 | RecoveryPL | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F007/SC07 | G/B/N007; T471 | previous blocks | reference vectors + invariants | NO/NO |
| 8 | Reserve | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F008/SC08 | G/B/N008; T472 | previous blocks | reference vectors + invariants | NO/NO |
| 9 | partial Far | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F009/SC09 | G/B/N009; T473 | previous blocks | reference vectors + invariants | NO/NO |
| 10 | final close gates | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F010/SC10 | G/B/N010; T474 | previous blocks | reference vectors + invariants | NO/NO |
| 11 | Big scenario | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F011/SC11 | G/B/N011; T475 | previous blocks | reference vectors + invariants | NO/NO |
| 12 | Small scenario | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F012/SC12 | G/B/N012; T476 | previous blocks | reference vectors + invariants | NO/NO |
| 13 | NewFar | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F013/SC13 | G/B/N013; T477 | previous blocks | reference vectors + invariants | NO/NO |
| 14 | Future Small | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F014/SC14 | G/B/N014; T478 | previous blocks | reference vectors + invariants | NO/NO |
| 15 | Catch-Up | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F015/SC15 | G/B/N015; T479 | previous blocks | reference vectors + invariants | NO/NO |
| 16 | transaction coordinator | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F016/SC16 | G/B/N016; T480 | previous blocks | reference vectors + invariants | NO/NO |
| 17 | persistence | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F017/SC01 | G/B/N017; T481 | previous blocks | reference vectors + invariants | NO/NO |
| 18 | restart/reconciliation | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F018/SC02 | G/B/N018; T482 | previous blocks | reference vectors + invariants | NO/NO |
| 19 | FSM orchestration | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F019/SC03 | G/B/N019; T483 | previous blocks | reference vectors + invariants | NO/NO |
| 20 | broker request builder | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F020/SC04 | G/B/N020; T484 | previous blocks | reference vectors + invariants | NO/NO |
| 21 | broker dispatch — последний отдельный этап | `Include/` projected owner | `Tests/Reference/hsb_2e_reference_model.py` | F021/SC05 | G/B/N021; T485 | previous blocks | reference vectors + invariants | NO/NO |
