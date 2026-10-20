# Cycle C17 — Deciding laws of finite magmas

**Branch:** B (algorithms) · **Status:** complete
**Experiments:** EXP-C17-01, EXP-C17-02 · **Claims:** CLM-C17-01 … CLM-C17-07
**Proofs:** `proofs/paper/C17.md` · **Module:** `systems/law_testing.py`

## Step 1 — Hypotheses

Question (Phase 5 — measurable improvements against baselines): *can
structural facts discovered by the lab make it cheaper to decide whether a
finite operation table satisfies a law than the exhaustive check of all n³
triples?*

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C17-1 | *(bold)* Light's generator test beats the exhaustive check by a factor ≥ n/10 on every input family. | Application Researcher | **refuted** (left-zero bands: 1.7×) |
| H-C17-2 | *(bold)* For anchored magmas the instance z = 0 of any law decides the law. | Inventor | **refuted** (43 laws; first reported as 18 — a counting bug); true for associativity, and for left-distributivity up to N = 4096 |
| H-C17-3 | The Rajagopalan–Schulman test with 40 rounds never errs on the benchmark. | Explorer | supported (0 errors in 90 instances) |

## Step 2 — Definitions

Cost = probes (table look-ups), exact and machine-independent; times are
secondary (the machine was shared with other jobs). Baselines: exhaustive
vectorised check, random triples.

## Step 3 — Falsification design

Input families include each method's worst case: left-zero bands (no small
generating set), single-entry corruptions of associative tables (only ≈ 4n
bad triples among n³), random magmas.

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C17-01 | 90 instances, n = 32 … 512: exact tests always correct; certification (associative inputs) — exhaustive/Light probe ratio 23–614, left-zero bands 1.7; refutation — an exhaustive check stopping at the first violation needs 4 probes on random magmas and 0.15–1.1× Light's probes on corruptions; random triples (n²/16 samples) wrong on 27 of 30 near-associative inputs; RS(40) never wrong |
| EXP-C17-02 | anchor instance decides 339 of 382 laws (N ≤ 5), insufficient for 43, undecided 0; LD wrap-around instance has solutions only at N = 2, 4, 8 (N ≤ 10) |
| EXP-C17-03 | forced anchored tables (uniqueness proved for every N): the full LD anchor instance has a model exactly at the powers of 2, for every N ≤ 4096 (the Skeptic's C program agrees); at the powers of 2 up to 512 the forced table is the Laver table and left-distributive |

> **Correction (2026-10-18, after the Skeptic's review).** The first version
> of EXP-C17-01 charged the exhaustive check a whole 64-row slab as soon as the
> slab contained a violation, so its "gains" of 23–77 on corrupted and random
> inputs measured the slab size; with correct accounting the exhaustive check
> wins on non-associative inputs, and the gains concern certification only.
> EXP-C17-02 had a classification bug (laws with a capped enumeration at one N
> were counted as undecided although a violation had been found at another N):
> the correct count is 339 / 43 / 0, not 333 / 18 / 31.

## Step 6 — Analysis

* Confirming associativity is the expensive case for the exhaustive check;
  rejecting is usually cheap because a violation appears early.
* Light's test is a large practical gain whenever a small generating set
  exists — always for anchored magmas (one generator) — and useless for
  left-zero bands.
* Sampling random triples is unreliable precisely on near-misses; the
  algebraic randomised test is not.

## Step 7 — Proofs and counterexamples

Written: Light's test (Theorem 1), the anchored criterion (Corollary 2), the
one-sidedness of the randomised test (Theorem 3). Counterexamples: left-zero
band (H-C17-1), x(yz) = y(y(xz)) and 17 further laws (H-C17-2).

## Step 8 — Comparison with existing mathematics (Historian)

Light's test: Clifford–Preston, *The Algebraic Theory of Semigroups* I, §1.2.
Randomised test: Rajagopalan and Schulman, SIAM J. Comput. 29 (2000).
**REDISCOVERY** for both; the anchored criterion is a small corollary of the
lab's C06 Theorem 1. During this cycle the lab found that its own C06
paraphrase of Laver's theorem was imprecise (the recursion holds for q < N
only); the C06 record was corrected.

**Batch 1.1 update (2026-10-19, [Historian audit](../../../reviews/historian_C11_C20.md)).** The anchor-instance
question is answered in the literature for every N. Uniqueness is Dehornoy's Lemma X.1.2 (also Biane, SLC 80
(2019) §2.1); the full instance fails for every N that is not a power of 2 (Biane's footnote 1, credited to
A. Lewandowski; Aguilera–Iannella, [arXiv:2610.06106](https://arxiv.org/abs/2610.06106), Prop. 2.5 with Dehornoy's
Lemma X.1.7 and Prop. X.1.6). The forcing argument, the existence of the forced table and the reduction to the
wrap-around equations are now Lean-checked for every N (proofs/lean/Infinity/C17_ForcedTable.lean), so
CLM-C17-05 (N ≤ 4096) is PROVEN (computer-assisted) and a REDISCOVERY. The all-N statement is CLM-C17-08
(REDISCOVERY): the Historian sketched a direct proof by row periods, and the Skeptic's review of batch 1.1
([skeptic_batch1.1.md](../../../reviews/skeptic_batch1.1.md) §1) completed it and machine-checked it in Lean
(proofs/lean/Infinity/C17_RowPeriod.lean: the equivalence for every N, from Laver's theorem as the only
hypothesis), so CLM-C17-08 is PROVEN (Theorem 5 of proofs/paper/C17.md). This answers next direction 1.

## Step 9 — Applications

When a table must be certified associative (e.g. checking a finite model found
by a SAT solver), computing a small generating set first and running Light's
test is 235–340× faster than the exhaustive check at n = 512 in our runs; for
anchored tables a single identity suffices. No gain on left-zero bands.

## Step 10 — Documentation

`record.yaml` (7 claims). Textbook: Chapter 19 (Volume 7).

## Next directions

1. Prove the LD anchor-instance characterisation for all N.
2. Light-type reductions for other laws.
3. Compare with optimised C implementations and model checkers.
