# Cycle C08 — Circle multiplications on recurrence numeration systems

**Branch:** C (alternative representations) / B (invented operations) · **Status:** complete
**Experiments:** EXP-C08-01 … EXP-C08-05 · **Claims:** CLM-C08-01 … CLM-C08-06
**Proofs:** `proofs/paper/C08.md`; Theorem 1 machine-checked in `proofs/lean/Infinity/C08_Knuth.lean`

## Step 1 — Hypotheses

An *invented operation on representations*: take the digit strings of a and b
in a greedy numeration system with base sequence G and **convolve the digit
positions**: a ∘_s b = Σ d_i(a) d_j(b) G_{i+j+s}. For G = Fibonacci and s = 2
this is Knuth's "circle" multiplication, famous for being associative although
no algebraic reason is visible. Question: *which (G, s) give associative
operations, and why?*

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C08-1 | Knuth's product is an isolated miracle. | Inventor (devil's advocate) | refuted |
| H-C08-2 | Non-Pisot base sequences are never associative. | Explorer | supported (10/10) |
| H-C08-3 | Pisot base sequences become associative for large shifts. | Explorer | supported (rediscovery of Grabner–Pethő–Tichy–Woeginger 1994) |
| H-C08-4 | Non-monotone shift sets need a negative conjugate root. | Explorer, after a surprise | supported (30/30 vs 10/60) |

## Step 2 — Definitions

Base sequences, greedy expansions, circle products with shift s, minimal
recurrences (Berlekamp–Massey), Pisot classification, associative-shift sets:
`systems/circle.py`, `proofs/paper/C08.md`.

## Step 3 — Falsification design

Exhaustive associativity checks on cubes [1,N]³, random triples up to 10⁶
(10⁹ for Knuth's product), shifts up to 20; a family of 90 quadratic Pisot
sequences split by the sign of the conjugate root to test H-C08-4; an
external validation of the implementation against the OEIS.

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C08-01 | 46 sequences × 6 shifts on [1,22]³: associativity is common at larger shifts; fails at every shift for several families |
| EXP-C08-02 | minimal recurrences: 5 geometric (always associative), 31 Pisot, 10 non-Pisot. **No non-Pisot sequence has an associative shift ≤ 8**; most Pisot sequences become associative above a threshold |
| EXP-C08-03 | Knuth (s = 2): no failure on 20,000 triples up to 10⁹. Thresholds: Fibonacci s ≥ 2, (2,2)-recurrence s ≥ 5, (3,3) with G₁ = 5 s ≥ 10, G_{k+1}=G_k+G_{k−2} s ≥ 10, 4-bonacci s ≥ 7; G_{k+1}=G_k+G_{k−3} (|β| ≈ 0.94) none up to 20. Non-monotone sets confirmed on inputs up to 10⁶: 1,3,4,7,11 → {2} ∪ [4,8]; 1,4,5,9,14 → {4} ∪ [6,8] |
| EXP-C08-04 | 90 quadratic Pisot sequences: **all 30 with β > 0 have upward-closed shift sets; the 10 non-monotone ones all have β < 0** |
| EXP-C08-05 | Our table of Knuth's product equals OEIS A101330 (implementation validated against the literature) |

## Step 6 — Analysis

The data are explained by one picture (Arnoux's idea, generalised): map n to
ν(n) = Σ d_i α^i in the number field of the recurrence. The circle product is
the α-coordinate of α^s ν(a)ν(b). It is associative when α^s ν(a)ν(b) is
again a *greedy* ν — which holds when its conjugate coordinates
β^s ν_β(a)ν_β(b) land in the "window" of conjugates of greedy expansions.

* |β| < 1 (Pisot): the factor β^s shrinks, so large shifts work.
* |β| ≥ 1: the factor never shrinks — no shift works (H-C08-2).
* β < 0: β^s alternates in sign and the window is asymmetric about 0
  (Fibonacci window (−ψ², −ψ) = (−0.382, 0.618)), so an odd shift can push the
  product out while the next even shift brings it back (H-C08-4).
* The threshold grows as |β| → 1 (|β| ≈ 0.94 needs s > 20).

## Step 7 — Proofs and counterexamples

* **Theorem 1** (CLM-C08-01): every shifted Knuth product ∘_t (t ≥ 0, i.e.
  s ≥ 2) is associative; s = 0, 1 fail with explicit counterexamples.
  **Machine-checked in Lean 4 + Mathlib** (`circ_assoc`, `circ_comm`, `key`,
  `window`; standard axioms only).
* H-C08-1 refuted by Theorem 1 itself (s = 3 is another associative product).
* H-C08-2, H-C08-4: conjectures with the heuristic mechanism above.

## Step 8 — Comparison with existing mathematics (Historian)

* Knuth, "Fibonacci multiplication", Appl. Math. Lett. 1 (1988); Arnoux,
  "Some remarks about Fibonacci multiplication", Appl. Math. Lett. 2 (1989).
* **Grabner, Pethő, Tichy, Woeginger, "Associativity of recurrence
  multiplication", Appl. Math. Lett. 7 (1994)**: associativity for linear
  recurrences with dominant-root conditions and canonical initial values when
  a parameter is chosen large enough — H-C08-3 is a **rediscovery**.
* Math. Slovaca 50 (2000), "Generalization of the Fibonacci multiplication"
  (length-2 recurrences and Tribonacci).
* OEIS A101330 (Knuth's table), A101646 (a non-associative variant noted by
  Grabner et al.).
* Not found in one search: the "never associative" statement for non-Pisot
  sequences and the sign-of-β explanation of non-monotone thresholds
  (provisionally potentially novel, low confidence; flagged for audit).

## Step 9 — Applications

An associative circle product on a numeration system defines a commutative
semigroup structure computable digit-wise (no carries inside the product
until re-normalisation); this gives a "digit-convolution" multiplication with
a twisted embedding into an algebraic number field. We see no practical
computational advantage over integer multiplication (re-normalisation costs
dominate); the value is structural. Cycle C09 studies the arithmetic
(irreducibles, factorisation) of the circle semigroups.

## Step 10 — Documentation

`record.yaml`; textbook: Volume 4 ("Alternative representations of
quantities"), chapter "Multiplying digit positions".

## Next directions

1. Formalise the sharper asymmetric window (needed by C09) in Lean.
2. Prove H-C08-2 (non-Pisot ⇒ never associative).
3. Prove H-C08-4 by computing the windows (Rauzy-type fractals for cubic cases).
4. C09: irreducibles and unique factorisation in (ℕ, ∘).
