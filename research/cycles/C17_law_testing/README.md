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
| H-C17-2 | *(bold)* For anchored magmas the instance z = 0 of any law decides the law. | Inventor | **refuted** (18 laws); true for associativity, and for left-distributivity up to N = 10 |
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
| EXP-C17-01 | 90 instances, n = 32 … 512: exact tests always correct; exhaustive/Light probe ratio 23–614 (left-zero bands 1.7); random triples (n²/16 samples) wrong on 27 of 30 near-associative inputs; RS(40) never wrong |
| EXP-C17-02 | anchor instance decides 333 of 382 laws (N ≤ 5), insufficient for 18, undecided 31; LD wrap-around instance has solutions only at N = 2, 4, 8 (N ≤ 10) |

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
