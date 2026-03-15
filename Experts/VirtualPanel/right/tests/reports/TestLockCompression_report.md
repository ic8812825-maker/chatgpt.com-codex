# TestLockCompression

- **Test description:** Greedy Delta Matching should not increase |delta|.
- **Timestamp:** 2026-03-15T21:59:40.210335Z

## Input parameters
- `buy`: `[0.4, 0.2, 0.1]`
- `sell`: `[0.3, 0.2]`

## Execution result
- **status:** PASS

## Metrics
- `delta_before`: `0.20000000000000007`
- `delta_after`: `0.20000000000000004`
- `levels_before`: `5`
- `levels_after`: `5`

## Conclusion
Greedy matching preserves/non-increases absolute delta.
