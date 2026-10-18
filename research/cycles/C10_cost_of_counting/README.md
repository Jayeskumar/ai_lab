# Cycle C10 — The cost of counting across representations

**Branch:** C (alternative representations) with an algorithmic angle · **Status:** complete
**Experiments:** EXP-C10-01 … EXP-C10-04 · **Claims:** CLM-C10-01 … CLM-C10-07
**Proofs:** `proofs/paper/C10.md`

## Step 1 — Hypotheses

How expensive is the *successor* operation in each representation of
quantity? Cost = number of digit positions that change at n → n+1.

| ID | Hypothesis | Outcome |
|---|---|---|
| H-C10-0 (Inventor, bold) | Zeckendorf, being sparse, counts more cheaply than binary | **refuted**: both average exactly 2 |
| H-C10-1 | Exchange systems fire 1/(m − Σb) times per increment | proved |
| H-C10-2 | Single-offset exchange rules cost 1 + 1/(m − q) | proved |
| H-C10-3 | Multi-offset rules have well-defined average costs | measured; open |

## Steps 2–5 — Definitions, design, execution

Representations: base b, Gray code, factorial base, Zeckendorf, negabinary,
balanced ternary, skew binary (`systems/counting_cost.py`), and the 31
terminating carry rules of C02 via an incremental counter validated against
full stabilisation.

| Experiment | Outcome |
|---|---|
| EXP-C10-01 | n < 10⁶: binary 1.999988, ternary 1.4999935, decimal 1.1111051, Gray 1.0, factorial 1.7182767 (e − 1 = 1.7182818), Zeckendorf 1.999992, negabinary 1.999997, balanced ternary 1.5000005, skew binary 1.4999955 with worst case 2 |
| EXP-C10-02 | Zeckendorf block totals: recurrence = brute force for m ≤ 24; T_m/G_m = 1.9993 (m = 20), 1.99999992 (m = 40) → 2; D_m = 2G_m − T_m = ⌈m/2⌉ + 2 |
| EXP-C10-03 | 31 carry rules: max deviation of average firings from 1/(m − B) is 5.7·10⁻⁴; single-offset rules match 1 + 1/(m − q) within 2.7·10⁻⁴; multi-offset rules show excess costs 0.296 … 0.831 |
| EXP-C10-04 | T_m is OEIS A215005 (same recurrence); the per-step Zeckendorf cost sequence is not in the OEIS |

## Step 6 — Analysis

* Positional systems with a constant radix pattern have average cost
  determined by digit frequencies (b/(b−1), e − 1).
* Zeckendorf counting is exactly as expensive as binary on average (2), but
  its worst case is smaller (≈ m/2 + 1 at G_m vs m + 1 at 2^m).
* For exchange systems, *firings* are governed by the token balance m − Σb
  alone (abelian property), but *digit changes* depend on how firings overlap.
* Skew binary and Gray code show the classical trade-offs: Gray has optimal
  cost 1 at every step; skew binary has worst case 2 with average 1.5.

## Step 7 — Proofs

Theorems 1–4 in `proofs/paper/C10.md` (written); H-C10-0 refuted by Theorem 2.

## Step 8 — Literature

Amortised analysis of binary counters (textbook, e.g. Cormen et al.); Gray
codes; skew binary numbers with O(1) worst-case increments (Myers 1983;
Okasaki's random-access lists); odometers and carry statistics of
numeration systems (Grabner, Liardet, Tichy). T_m is OEIS A215005. The
constants of Theorems 1–2 are **rediscoveries**; the exchange-system results
(Theorems 3–4) follow directly from C02 and are probably folklore for rational
bases; not assessed further.

## Step 9 — Applications (Application Researcher)

Counters are a data-structure primitive (binomial heaps ≈ binary counters,
Fibonacci heaps, skew binary random-access lists). The measured costs give a
menu: Gray code (1, 1) when only the change matters (rotary encoders),
skew binary (1.5 average, 2 worst) for persistent structures, Zeckendorf
(2 average, ≈ log_φ(n)/2 worst). No representation from the invented exchange
systems improves on these classical choices; recorded as a negative result.

## Step 10 — Documentation

`record.yaml`; textbook Volume 4 chapter "The cost of counting".

## Next directions

1. Compute the multi-offset constants exactly (invariant measure of the digit process).
2. Worst-case/average Pareto front over all exchange rules.
