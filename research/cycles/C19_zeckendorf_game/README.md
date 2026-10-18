# Cycle C19 — The longest Zeckendorf game

**Branch:** C–D (a representation of quantities played as a game) · **Status:** complete
**Experiments:** EXP-C19-01 … EXP-C19-04 · **Claims:** CLM-C19-01 … CLM-C19-14
**Proofs:** `proofs/paper/C19.md` (Theorems 1, 2, 4, Corollary 3, Proposition 6, Conjecture 5),
`proofs/lean/Infinity/C19_Zeckendorf.lean` (12 theorems, standard axioms only) · **Module:** `systems/zeckendorf_game.py`

## Step 1 — Hypotheses

Question (open problem left by cycle C02): *how long can the Zeckendorf game
on n last?* The Fibonacci exchange system of C02 is the two-player Zeckendorf
game of Baird-Smith, Epstein, Flynt and Miller. Before experimenting, the
Historian read the literature: the shortest game has n − Z(n) moves
(Baird-Smith et al.); the split-first strategy produces a longest game and the
bound B(n) = Σ (F_{i+2} − i − 2) δ_i holds with equality iff n = F_k − 1
(Cusenza et al., Fib. Quart. 2022); a closed form for other inputs is stated to
be open (Cheigh et al., CANT VI, 2025).

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C19-0 | The split-first strategy attains L(n) for all n ≤ 150 (independent check of the published theorem). | Explorer | **confirmed** by exhaustive search |
| H-C19-A | Every game has length B(n) − Σ (i − 1) MC_i. | Formal Verifier | **proved** (potential; Lean core) |
| H-C19-B | Split moves alone always end at the lazy representation. | Explorer | **proved** |
| H-C19-F | D(F at level j) = ⌊j²/4⌋. | Explorer | **proved** (given the published strategy theorem) |
| H-C19-1 | *(bold)* D is additive up to consecutive-pair corrections. | Inventor | **refuted** (n = 12) |
| H-C19-2 | The top summand's effect depends only on the two highest levels. | Inventor | **refuted** |
| H-C19-3 | *(bold)* D is additive over lazy runs. | Inventor | **refuted** (inconsistent linear system) |
| H-C19-4 | *(bold)* L(n + 1) = L(n) + (longest game from Zeck(n) + F_1). | Inventor | **refuted** (n = 3) |
| H-C19-R | An explicit two-sequence recursion gives D(n) for all n. | Explorer | **supported** in and out of sample; no proof |

## Step 2 — Definitions

Levels 0, 1, 2, … carry F_1 = 1, F_2 = 2, F_3 = 3, F_4 = 5, …. Moves: combines
C1 (F_1 + F_1 → F_2) and C_i (F_{i−1} + F_i → F_{i+1}); splits S2
(2F_2 → F_1 + F_3) and S_i (2F_i → F_{i−2} + F_{i+1}). L(n) is the longest game,
B(n) the bound of Cusenza et al., D(n) = B(n) − L(n) the *deficit*. The *lazy*
representation of n uses distinct F_i without two consecutive missing indices
below the largest.

## Step 3 — Falsification design

The published strategy theorem was re-tested by an exhaustive search that
assumes no strategy. Every hypothesis about D was confronted with all n below
30000; the final recursion, inferred from that range, was then tested on 6,272
numbers it had not seen (up to 2·10^7). Additive models were refuted either by
explicit counterexamples or by an exact rank test of the corresponding linear
system.

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C19-01 | exact L(n) for n ≤ 150 (≤ 910,775 positions); earlier values n ≤ 60 reproduced; split-first strategy optimal for all n ≤ 150; B(n) attained exactly at 1, 2, 4, 7, 12, 20, 33, 54, 88, 143; positions = Fibonacci partitions (A003107) |
| EXP-C19-02 | identity |G| = B(n) − Σ(i−1)MC_i: 0 violations (greedy n < 1500, 1500 random games); split phase ends at the lazy representation for all n < 5000, independent of firing order; H-C19-4 fails for 288/300 |
| EXP-C19-03 | D(F) = ⌊j²/4⌋ for j ≤ 33; two-summand law for 276 pairs; H-C19-1, -2, -3 refuted; recursion matches all n < 30000; D(n) ≤ ⌊j²/4⌋, L strictly increasing |
| EXP-C19-04 | recursion vs simulation on 6,272 out-of-sample n: 0 mismatches; L(10^7) in 9·10^-5 s vs 8.3 s; L, D, L(F_k), ρ not in the OEIS |

Process notes: a first version of EXP-C19-02 was stopped (a quadratic
simulation up to n = 20000) and rescaled; a first run of EXP-C19-04 crashed at
its last step because the Fibonacci table ended near 5·10^19 — fixed and re-run.

## Step 6 — Analysis

* **Longest = fewest weighted combines.** Every game satisfies
  |G| = B(n) − Σ_{i≥2}(i − 1)MC_i; the problem is to minimise the weighted
  number of consecutive combines.
* **Two phases.** The longest (split-first) game first splits until every level
  holds at most one chip — and always arrives at the *lazy* Fibonacci
  representation — and only then normalises to Zeckendorf form. All of the
  deficit is created in the second phase.
* **Fibonacci inputs.** For n = F_k the second phase is a single carry cascade
  C_j, C_{j−2}, …, whose weights add up to the quarter-square ⌊(k−1)²/4⌋.
* **General n.** Lower summands save combines in a way that depends on the
  parity of the gaps: the saving of the top summand depends only on the rest m
  and on the parity of the top level, and is computed by two auxiliary
  sequences ρ₀, ρ₁ with a self-similar block structure.
* L(n)/n → φ² (known); numerically (φ²n − L(n))/(log_φ n)² ∈ [0.34, 0.38].

## Step 7 — Proofs and counterexamples

Written (proofs/paper/C19.md): Theorem 1 (length identity), Theorem 2 (lazy
split phase), Corollary 3 (a short proof of Cusenza et al.'s Theorem 1.4),
Theorem 4 (L(F_k) = F_{k+2} − k − 2 − ⌊(k − 1)²/4⌋), Proposition 6 (all
Fibonacci partitions are reachable). Lean: the potential changes of all move
types and their sum over any move list (`length_identity`), and the weight
sums behind Theorem 4. Counterexamples: n = 12 (H-C19-1), levels (4, 2)
(H-C19-2), the rank test 46 < 47 (H-C19-3), n = 3 (H-C19-4).

## Step 8 — Comparison with existing mathematics (Historian)

* P. Baird-Smith, A. Epstein, K. Flynt, S. J. Miller, *The Zeckendorf game*,
  CANT 2017–18, Springer Proc. Math. Stat. 297 (2020) 25–38,
  [arXiv:1809.04881](https://arxiv.org/abs/1809.04881) — termination, shortest
  game, Player 2 wins; longest games n ≤ 49 (Fig. 4).
* R. Li et al., *Deterministic Zeckendorf games*,
  [arXiv:2006.16457](https://arxiv.org/abs/2006.16457) — bound
  3n − 3Z(n) − IZ(n) + 1; Split Smallest.
* A. Cusenza et al., *Bounds on Zeckendorf games*, Fibonacci Quart. 60 (2022),
  [arXiv:2009.09510](https://arxiv.org/abs/2009.09510) — the split-first
  strategy is longest (Thm 1.2), the bound B(n) (Thm 1.3), equality iff
  n = F_k − 1 (Thm 1.4). **Our Theorem 1 is implicit there; Corollary 3 reproves
  their Theorem 1.4.**
* J. Cheigh et al., *Towards the Gaussianity of random Zeckendorf games*,
  CANT VI, Springer 2025, doi:10.1007/978-3-031-65064-2_4
  ([arXiv:2210.11038](https://arxiv.org/abs/2210.11038)) — every length between
  shortest and longest occurs; "finding a convenient closed form for the length
  of the longest game for non-Fibonacci input N remains open".
* Variants not studied here: *Black Hole Zeckendorf games*
  ([arXiv:2409.10981](https://arxiv.org/abs/2409.10981)), *The ordered
  Zeckendorf game* ([arXiv:2508.20222](https://arxiv.org/abs/2508.20222)).
* Lazy representations: J. L. Brown (1965). No link between them and the game
  was found. OEIS: L(n), D(n), L(F_k), ρ₀, ρ₁ absent; the position counts are
  A003107.

Verdicts: identity and Corollary 3 REDISCOVERY; lazy split phase, L(F_k) and
the recursion POTENTIALLY NOVEL (small; the recursion unproven).

## Step 9 — Applications

The recursion (if true) computes L(n) with O(log² n) operations, against
Θ(n) moves for playing the published strategy: at n = 10^7 about 9·10^-5 s
against 8.3 s (CLM-C19-14; correctness conditional on CLM-C19-05). No other
application is claimed.

## Step 10 — Documentation

`record.yaml` (14 claims, journal). Textbook: Chapter 16, "The longest
Zeckendorf game" (Volume 5).

## Next directions

1. Prove the recursion (analyse the normalisation phase from the lazy
   representation).
2. Prove D(n) ≤ ⌊j²/4⌋ and strict monotonicity of L.
3. Extend the lazy-phase theorem and the Fibonacci-input formula to the
   generalised Zeckendorf games.
4. OEIS submissions (human decision).
