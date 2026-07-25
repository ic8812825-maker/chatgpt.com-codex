# Hybrid Split Big — Catch-Up Outcome Truth Table

**Status:** NORMATIVE, Stage 1.2. Economic outcome, calculation validity, routing and gate pass are independent dimensions.

## Outcome classes

| Outcome | Class | Calculation valid | Meaning |
|---|---|---:|---|
| CONTINUE | CONTINUE | yes | Valid next sequential level exists. |
| FINITE_PASS | SUCCESS | yes | Base and Worst both prove finite coverage/recovery. |
| FINAL_CLOSE_PREVIEW_REQUIRED | ROUTE | yes | Partial budget can cover full Far loss; external projected Final Close gate must decide. |
| TERMINAL_MIN_VOLUME | TERMINAL | yes | No broker-valid continuation basket. |
| NO_FINITE_LEVEL | REJECT | yes | Evaluated bound has no finite level. |
| REJECT_* | REJECT | yes | Economic/config/gate rejection. |
| ERROR_* | ERROR | no | Calculation or internal contract failure. |

## Base/Worst aggregation

| Base | Worst | Aggregate | Continue |
|---|---|---|---:|
| CONTINUE | CONTINUE | CONTINUE | yes |
| FINITE_PASS | FINITE_PASS | FINITE_PASS | no |
| FINITE_PASS | CONTINUE | CONTINUE | yes |
| CONTINUE | FINITE_PASS | CONTINUE | yes |
| FINAL_ROUTE | FINAL_ROUTE | FINAL_ROUTE | no |
| FINAL_ROUTE | CONTINUE | CONTINUE if both next states valid; otherwise REJECT_DIVERGENCE | conditional |
| CONTINUE | FINAL_ROUTE | CONTINUE if both next states valid; otherwise REJECT_DIVERGENCE | conditional |
| FINITE_PASS | FINAL_ROUTE | REJECT_DIVERGENCE | no |
| FINAL_ROUTE | FINITE_PASS | REJECT_DIVERGENCE | no |
| TERMINAL | any non-error | TERMINAL | no |
| any non-error | TERMINAL | TERMINAL | no |
| REJECT | any non-error/non-terminal | REJECT | no |
| any non-error/non-terminal | REJECT | REJECT | no |
| ERROR | any | ERROR | no |
| any | ERROR | ERROR | no |

Priority is `ERROR > TERMINAL > REJECT > agreed ROUTE > agreed SUCCESS > CONTINUE`. Mixed route/continue is CONTINUE only when both branches produced a valid next state. ReasonCode is stable machine data; Reason is explanatory text.
