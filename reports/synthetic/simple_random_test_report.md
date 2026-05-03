# Simple Random Synthetic Test Report

## 1. Test Info
Version: v2.0
Date: 2026-05-02
Bars: 450
Seed: 42
Initial Price: 1.1

## 3. Summary Metrics
- OPEN BUY: 0
- OPEN SELL: 2
- PARTIAL_CLOSE: 2
- FULL_CLOSE: 0
- Max Total Lot: 0.22
- Max Exposure: 0.06
- Initial Locked Volume: 0.20
- Final Locked Volume: 0.22
- Realized PnL: 0.28
- Floating PnL: -15.43
- Total PnL: -15.15

## 4. Down phase table (bars 121-220)
| bar | close | z | v | regime | state | q | beta | ev | buy_signal_raw | regime_ok | ev_ok | risk_ok | projected_exposure_ok | final_entry_allowed | block_reason_exact |
|---:|---:|---:|---:|---|---|---:|---:|---:|---|---|---|---|---|---|---|
| 121 | 1.10104 | -0.19947229551452011 | 1.2830060934325647 | NEUTRAL | FLOW | 0.0054986807387863 | 0.6601055408970959 | 0.4228485488126665 | False | True | True | False | True | False | BLOCK_WEAK_Z |
| 122 | 1.10059 | -1.741754385965356 | 1.3305322128850132 | NEUTRAL | FLOW | 0.00935438596491339 | 0.3516491228069287 | 0.7193522807018398 | True | True | True | False | False | False | BLOCK_EXPOSURE |
| 123 | 1.10014 | -3.076028368795314 | 1.3853409314205731 | NEUTRAL | FLOW | 0.01 | 0.29999999999999993 | 0.769 | True | True | True | False | True | False | BLOCK_EXPOSURE |
| 124 | 1.09969 | -4.262921348314954 | 1.435020960980228 | NEUTRAL | FLOW | 0.01 | 0.29999999999999993 | 0.769 | True | True | True | False | True | False | BLOCK_EXPOSURE |
| 125 | 1.09924 | -5.198490566038288 | 1.5183346065698402 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 126 | 1.09879 | -6.073545816733637 | 1.5699274455841588 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 127 | 1.09834 | -6.721564245809858 | 1.6497695852534342 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 128 | 1.09789 | -7.325352112676113 | 1.727178738672995 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 129 | 1.09744 | -7.850751252087152 | 1.7924471841522644 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 130 | 1.09699 | -8.335350318471903 | 1.8376543571135788 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 131 | 1.09654 | -8.666927710843906 | 1.923299733518619 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 132 | 1.09609 | -8.88880681818262 | 2.003414911781344 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 133 | 1.09564 | -9.298622589532393 | 2.052122788173372 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 134 | 1.09519 | -9.492808398950098 | 2.1286105369014776 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 135 | 1.09474 | -10.050065189048464 | 2.1047143405960087 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 136 | 1.09429 | -10.590246433203708 | 2.0765998707175313 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 137 | 1.09384 | -11.184363636363953 | 2.0484171322160143 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 138 | 1.09339 | -11.850642201835479 | 2.0058888479940564 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 139 | 1.09294 | -12.360261437909184 | 1.9906323185010888 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 140 | 1.09249 | -12.911192660551073 | 1.9548063127689403 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 141 | 1.09204 | -13.532592592593517 | 1.9176136363635594 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 142 | 1.09159 | -13.828563968668545 | 1.9064211050273545 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 143 | 1.09114 | -14.3089150326801 | 1.8927210648720478 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 144 | 1.09069 | -14.850315789474022 | 1.8584633442558702 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 145 | 1.09024 | -15.279157894736397 | 1.839570121508478 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 146 | 1.08979 | -15.521770833333397 | 1.826744683887546 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 147 | 1.08934 | -15.867272727272972 | 1.809210526315774 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 148 | 1.08889 | -16.317493472584943 | 1.779905195650167 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 149 | 1.08844 | -16.86287978863912 | 1.7358404035771906 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 150 | 1.08799 | -17.34247669773617 | 1.7002490378085102 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 151 | 1.08754 | -17.6173173970778 | 1.6913746630728435 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 152 | 1.08709 | -17.778708827403776 | 1.6784608580275284 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 153 | 1.08664 | -18.161430463574643 | 1.6502010841057557 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 154 | 1.08619 | -18.525858854858978 | 1.6250486865453273 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 155 | 1.08574 | -18.58255599472859 | 1.6270794031899751 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 156 | 1.08529 | -19.038133333331764 | 1.596288098076036 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 157 | 1.08484 | -19.207925531913684 | 1.584492203961316 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 158 | 1.08439 | -19.430359520638376 | 1.5662148070907873 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 159 | 1.08394 | -19.591436170212397 | 1.5497485780232896 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |
| 160 | 1.08349 | -19.8079466666658 | 1.5253823625122687 | VOLATILE | FLOW | 0.0 | 0.29999999999999993 | 0.0 | True | False | False | False | False | False | BLOCK_VOLATILE |

Down phase diagnosis:
- Bars with Z < -1.5: 65
- Bars blocked by EV: 0
- Bars blocked by VOLATILE: 43
- Bars blocked by exposure: 53
- Bars blocked by projected exposure: 0
- Bars where BUY should have opened: 0
- Actual OPEN BUY: 0

## 8. Conclusion
FAIL

This synthetic test does not validate profitability.
It validates only mechanics, risk gates, recommendation logic, and reporting pipeline.
