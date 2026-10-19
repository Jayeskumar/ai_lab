# Cycle C06 — Successor-anchored magmas: spectra of composition laws

**Branch:** B (invented operations) · **Status:** complete
**Experiments:** EXP-C06-01 … EXP-C06-04 · **Claims:** CLM-C06-01 … CLM-C06-12
**Proofs:** `proofs/lean/Infinity/C06_Laver.lean` (12 theorems, standard axioms only),
`proofs/paper/C06.md` (Theorems 1–8) · **Modules:** `systems/laver.py`, `systems/magma.py`

## Step 1 — Hypotheses

Question: *anchor one invented binary operation to the successor, x ⋆ 0 = x + 1
(mod N), and impose a single composition law. For which sizes N does a model
exist, and how many are there?*

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C06-1 | Left-distributivity + anchor has exactly one model for N ∈ {1, 2, 4, 8} and none for other N ≤ 10. | Explorer | **confirmed** (SAT, independent of Laver's recursion); published theorem (Laver, Drápal) |
| H-C06-2 | *(bold)* Restricted spectra are special to left-distributivity: every other law of the family has spectrum {1} or all N. | Inventor | **refuted** — 21 other laws have restricted spectra |
| H-C06-3 | *(bold)* Apart from LD, every anchored spectrum equals the "affine spectrum" (models x ⋆ y = x + a y + 1). | Explorer | **refuted** — 6 laws have non-affine models; but it holds for 20 of the 22 restricted laws (N ≤ 9) |
| H-C06-4 | (xy)z = x(y(zz)): models ↔ roots of a² + a ≡ 1 (mod N). | Formal Verifier | **proved**; counts confirmed to N = 12 |
| H-C06-5 | (xy)z = x((yz)z): one model for odd N, none for even N. | Formal Verifier | **proved (Lean)**; confirmed to N = 12 |

## Step 2 — Definitions

A *successor-anchored magma* of size N is a binary operation on ℤ/N with
x ⋆ 0 = x + 1. Its *spectrum* for a law is the set of N admitting a model.
An anchored isomorphism must fix 0 and commute with x ↦ x ⋆ 0, so it is the
identity: model counts are counts of tables. The *affine* tables are
x ⋆ y = x + a·y + 1.

## Step 3 — Falsification design

Each hypothesis named its refuting object in advance: an LD model at a
non-power of two or two LD models at one size (H-C06-1); any non-LD law with a
spectrum strictly between {1} and {1, …, 6} (H-C06-2); a law whose SAT
spectrum differs from its affine spectrum (H-C06-3); a model count differing
from the root count (H-C06-4/5). SAT enumerations are complete (no UNKNOWN
instance occurred).

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C06-01 | Laver's recursion gives LD tables exactly at N = 1, 2, 4, …, 64 (N ≤ 64); A_n LD-verified for n ≤ 12; row-0 periods = OEIS A098820 |
| EXP-C06-02 | exact anchored model counts for 12 laws: LD 1 at N = 1, 2, 4, 8 only; associativity, RD, (xy)z = (xy)(xz), x(yx) = xy: 1 for every N; right-permutable N^(N−1); left-permutable 1, 2, 9, 94, 1486 (A058156); x(xy) = xy 1, 2, 24, ≥ 2000 |
| EXP-C06-03 | 382 laws x(yz) = t, (xy)z = t (t with 3–4 leaves): 77 all N, 283 only N = 1, **22 restricted** — {1,2}: 10, {1,3}: 7, {1,5}: 2, odd: 2, {1,2,4,8}: LD |
| EXP-C06-04 | affine analysis: 20 of 22 restricted laws have only affine models (N ≤ 9); 6 laws have non-affine models; golden law counts = root counts for N ≤ 12 (2 models at N = 11); odd law one model at every odd N ≤ 11 |

The first run of EXP-C06-02 was stopped after 27 minutes: it computed an
unused isomorphism reduction (8! permutations per table). The fix (count
tables directly, justified in Step 2) brought it to 53 s.

## Step 6 — Analysis

* The anchor turns a law into **arithmetic**. Substituting z = 0 makes the law
  talk about the successor: for (xy)z = x((yz)z) it gives x ⋆ (y + 2) =
  x ⋆ y + 1, so going once around ℤ/N forces N to be odd; for
  (xy)z = x(y(zz)) it gives x ⋆ (y ⋆ 1) = x ⋆ y + 1, which forces a
  "translation table" and then the golden congruence a² + a ≡ 1.
* Spectra observed so far: all N, {1}, finite sets {1, 2} and {1, 3}, the odd
  numbers, the moduli where the golden ratio exists (A089270), and the powers
  of two (Laver). Only the last one comes from non-affine models.
* Two "permutable" laws give classical counting problems: right-permutable
  magmas are x + c(y) (N^(N−1)), and left-permutable magmas are commutative
  monoids in disguise (A058156) — the centraliser argument of Theorem 7.

## Step 7 — Proofs and counterexamples

Lean: `anchored_assoc_unique`, `anchored_rd_unique`, `odd_law_even_impossible`,
`odd_law_formula`, `odd_law_model`, `centralizer_eq`, `comp_eq`, `id_eq`,
`leftPerm_assoc`, `leftPerm_comm`, `leftPerm_one_mul`, `leftPerm_mul_one`,
plus the finite checks `laver3_anchored`, `laver3_left_distributive`,
`no_anchored_ld_three`. Written: Theorems 1–8 of `proofs/paper/C06.md` (Theorem 8: spectra are closed
under coprime products, so a spectrum is never the set of primes).
Counterexamples: (xy)z = x((yz)z), (xy)z = x(y(zz)), x(yz) = ((zx)x)y
(H-C06-2); x(yz) = y(x(yz)), x(yz) = y((yx)z) (H-C06-3).

## Step 8 — Comparison with existing mathematics (Historian)

* LD + anchor: Laver's theorem — for every N a unique operation with
  p ⋆ 1 = p + 1 (mod N) and p ⋆ (q + 1) = (p ⋆ q) ⋆ (p + 1) for q < N (the
  recursion without its wrap-around instance) exists, and it is
  left-distributive iff N is a power of 2 (Laver; elementary proof by Drápal;
  Dehornoy, *Braids and Self-Distributivity*, 2000, Ch. X; Dehornoy,
  [arXiv:1711.09792](https://arxiv.org/pdf/1711.09792); Biane,
  [arXiv:1810.00548](https://arxiv.org/pdf/1810.00548); [Wikipedia: Laver table](https://en.wikipedia.org/wiki/Laver_table)). **REDISCOVERY.**
* Golden spectrum: OEIS [A089270](https://oeis.org/A089270) (moduli where
  x² ≡ x + 1 is solvable) and [A087781](https://oeis.org/A087781) (number of
  roots); the number theory is classical. The magma correspondence was not
  found. **POTENTIALLY NOVEL** (small).
* Left-permutable groupoids appear in the groupoid-identity literature (e.g.
  Stanovský; Weber 2009); the bijection with commutative monoids is the
  regular-representation idea and the count is OEIS A058156; no statement
  for anchored magmas found. **POTENTIALLY NOVEL** (small, likely folklore in
  spirit).
* Odd law, right-permutable count: elementary; no prior statement found.

**Batch 1.1 update (2026-10-19, [Historian audit](../../../reviews/historian_C11_C20.md)).** Biane's arXiv v1
(cited above) states the recursion for all q, which is false already at N = 3; the refereed version
([Sém. Lothar. Combin. 80 (2019) B80c](https://www.mat.univie.ac.at/~slc/wpapers/s80biane.pdf), §2.1 and
footnote 1) restricts it to q < N, the correction this lab made in C17. CLM-C06-01 states the published theorem
and is now PROVEN (literature); see also Aguilera–Iannella, [arXiv:2610.06106](https://arxiv.org/abs/2610.06106).

## Step 9 — Applications

None claimed. The construction gives a compact way to generate finite
algebraic structures with prescribed arithmetic constraints on their size
(e.g. a one-law "certificate" that N is odd or that 5 is a square modulo N);
we found no practical use and did not benchmark anything.

## Step 10 — Documentation

`record.yaml` (12 claims, journal). Textbook: Chapter 7, "Anchored operations
and arithmetic spectra" (Volume 2).

## Next directions

1. Prove the finite spectra {1, 2} and {1, 3} (CLM-C06-10).
2. Which sets of integers are anchored spectra of one law? They are closed under
   coprime products (Theorem 8); are they always closed under divisors?
3. Are there non-LD laws with Laver-like (non-affine, power-of-two) spectra?
4. Formalise the golden-law correspondence in Lean.
