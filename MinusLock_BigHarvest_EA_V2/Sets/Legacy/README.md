# Legacy set files

Existing set files that use `BigRatio`, `SmallRatio`, `CloseBigOnSmall`, and `RemainBigOnSmall` are legacy single-Big geometry inputs. Stage 1 adds the split-geometry parameters and validation while preserving those files in their original locations for compatibility. Do not load a legacy `.set` with `UseSplitBigGeometry=true` unless it has been migrated to `Sets/SplitGeometry/`.
