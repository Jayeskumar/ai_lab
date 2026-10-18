# Cycle C07 — Arithmetic from the minimal excludant

**Branch:** B–D (invented operations defined by exclusion relations) · **Status:** complete
**Experiments:** EXP-C07-01 … EXP-C07-03 · **Claims:** CLM-C07-01 … CLM-C07-08
**Proofs:** `proofs/paper/C07.md` (Theorems 1–3) · **Module:** `systems/mex.py`

## Step 1 — Hypotheses

Question: *what arithmetic do we get if an operation is defined only by what it
must avoid?* f(a, b) is the least value not produced by a prescribed set of
earlier entries (the mex). Conway's nim-sum and nim-product are of this form;
we vary the set of "options".

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C07-1 | *(bold)* Apart from trivial operations only nim-sum and nim-product are associative. | Inventor | **refuted** — ordinary addition and min are mex operations too |
| H-C07-2 | *(bold)* Commutative mex operations are closed on [0, 2^(2^m)), like the nimbers. | Inventor | **refuted** (30 of 34) |
| H-C07-3 | 0 is absorbing or an identity, and diagonals are known sequences. | Explorer | first part **proved**; second **refuted** (88 unmatched sequences) |
| H-C07-4 | *(bold)* Every row is eventually additively periodic (as for Wythoff's game). | Explorer | **refuted** — proved for the Jacobsthal row |
| H-C07-5 | Row 2 of D[x⊕y] swaps Jacobsthal blocks. | Explorer | **proved** |

## Step 2 — Definitions

Spec (L, R, D): options f(a′, b) for a′ < a (L), f(a, b′) for b′ < b (R), and
for a′ < a, b′ < b the XOR of any subset (mask in D) of x = f(a′, b),
y = f(a, b′), z = f(a′, b′). 2 · 2 · 2⁷ = 512 specs.

## Step 3 — Falsification design

Associativity is refuted by a single triple; closure by a single value;
additive periodicity by a row whose deviation from b is unbounded. Tables were
cross-checked against a plain-set implementation before any census.

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C07-01 | 512 specs → 134 operations on [0, 64)², 34 commutative, **11 associative**: 0, a, b, a[b>0], b[a>0], min, +, ⊕, ⊗ (nim), zero-absorbing shifts of ⊕ and + |
| EXP-C07-02 | 0 absorbing or identity in all 34 commutative operations; no closed forms for the chaotic ones; 88 row/diagonal sequences not in the OEIS |
| EXP-C07-03 | 222 of 670 rows additively periodic; Jacobsthal block swap verified for b < 2¹⁵ by an independent algorithm |

A bug (a loop variable shadowing the column count in the new rectangular table
mode) was caught by a sanity check before it affected any recorded result.

## Step 6 — Analysis

* Exclusion produces familiar arithmetic: + is the mex of "decrease either or
  both", min of "decrease both", ⊕ of "decrease one", ⊗ of Conway's corner moves.
  Nothing else in the family is associative (468 specs refuted by explicit
  triples; 33 further specs agree with the 11 formulas on the tested window).
* Most commutative mex operations are chaotic (quadratic growth, no closed
  forms, unknown sequences) — but not structureless: the second row of
  D[x⊕y] is an exact self-similar involution built from Jacobsthal numbers.

## Step 7 — Proofs and counterexamples

Written: Theorem 1 (formulas of the 11 associative operations), Theorem 2
(identity/absorbing 0), Theorem 3 (the Jacobsthal row, with a proof that it is
not additively periodic). Counterexamples: a + b, min (H-C07-1);
f(2, 3) = 4 for D[x⊕y] (H-C07-2); the Jacobsthal row (H-C07-4).

## Step 8 — Comparison with existing mathematics (Historian)

* Nim-sum and nim-product: J. H. Conway, *On Numbers and Games* (1976);
  OEIS A051775, [A006042](https://oeis.org/A006042). **REDISCOVERY.**
* a + b and min(a, b) as Grundy values: rank functions of product posets;
  folklore in combinatorial game theory. **REDISCOVERY** (in substance).
* Additive periodicity is a theorem for Wythoff's game (Dress–Flammenkamp–Pink
  1999; Landman 2002); our family shows it is not the rule for mex operations.
* The Jacobsthal row: no OEIS match for the row, |g(b) − b| or g(b) ⊕ b; no
  mex recursion of this form found on the web (closest: Multiplicative Modular
  Nim, [arXiv:2507.08830](https://arxiv.org/abs/2507.08830), a different
  recursion). **POTENTIALLY NOVEL** (small).

## Step 9 — Applications

None claimed. The census is a source of explicit permutations and
self-similar sequences; no practical use was tested.

## Step 10 — Documentation

`record.yaml` (8 claims, journal). Textbook: Chapter 14, "Arithmetic from the
minimal excludant" (Volume 5).

## Next directions

1. Structure of rows a ≥ 3 of D[x⊕y].
2. Prove the 33 remaining associative-looking specs equal their formulas.
3. Which mex tables are automatic sequences (Walnut-style proofs)?
4. OEIS submissions (human decision).
