# ALE_GEOMETRY_REPORT

## 1) Volume convergence / boundedness

- Arithmetic boundedness: **PASS** (no numeric divergence in tested runs).
- Economic boundedness at deep tails: **PARTIAL** (required deposit grows sharply for large depth / trend).

## 2) Average price behavior

- Weighted behavior reacts to added depth and does not remain frozen.
- Under large `k` and deep expansion, average-price improvement exists but with rising margin burden.

## 3) Tail effectiveness (critical)

Question: does each new tail position reduce risk meaningfully?
- Moderate regime: often yes.
- Adversarial regime: can become weak/expensive; marginal risk benefit degrades.

## 4) Key geometry conclusion

Geometry construction is algorithmically stable, but tail economic efficiency is configuration-dependent and can degrade in stressed regimes.
