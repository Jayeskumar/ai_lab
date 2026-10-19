# Cycle C15 — Magma cellular automata: light cones, streaming width and fast-forwarding

**Branch:** E (local-rule dynamics over invented algebras) · **Status:** complete
**Experiments:** EXP-C15-01 … EXP-C15-05 · **Claims:** CLM-C15-01 … CLM-C15-18
**Proofs:** `proofs/paper/C15.md` (Theorems 1–6), `proofs/lean/Infinity/C15_MagmaCA.lean`
(`ca_comm_binomial`, `ca_step_shift`; standard axioms only) · **Module:** `systems/magma_ca.py`

## Step 1 — Hypotheses

Question: *a binary operation is also a cellular automaton, c′ᵢ = cᵢ * cᵢ₊₁. How hard is
it to predict, and when can it be fast-forwarded?* Complexity of the t-step map F_t is
measured by its *streaming width* λ(t): the number of distinct residual functions a
left-to-right (or right-to-left, whichever is smaller) reader must distinguish.

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C15-0 | The 16 two-element automata are the elementary rules 17m; XOR has 2^popcount(t) essential cells. | Explorer | **confirmed** (calibration) |
| H-C15-1 | *(bold)* λ(t) is bounded or geometric — no intermediate growth. | Inventor | **refuted** — the fuse magma has λ(t) = Θ(t) (proved) |
| H-C15-2 | *(bold)* Bounded width ⇔ semigroup, affine, or a light cone of ≤ 2 cells. | Inventor | **refuted** — 685 bounded-width classes outside these |
| H-C15-3 | Surjective ⇔ permutive (order ≤ 3). | Explorer | **confirmed** (exhaustive); fails at order 4; rediscovery (Kari–Salo–Törmä) |
| H-C15-4 | *(bold, from the cycle brief)* Fast-forwardable ⇔ bounded width. | Inventor | **refuted** — fuse: linear width, O(L) fast-forward |
| H-C15-5 | *(bold)* Cycle detection fast-forwards most automata; long cycles only for geometric width. | Application Researcher | first part holds, second **refuted** (affine quasigroups) |
| H-C15-6 | The exact fast-forwards beat simulation > 100× at L = 1024, t = 10⁵ and lose for small t. | Application Researcher | **refuted** on the > 100× clause (commutative-semigroup method 62–100×); the small-t clause is partly true — timed the same way on both sides, affine and fuse lose for t ≲ 20–70 (the first version said they never lose; Skeptic review) |

## Step 2 — Definitions

Magma automaton c′ᵢ = cᵢ * cᵢ₊₁ on cyclic rows (length L) or one-sided rows; t-step
local map F_t; essential cells of F_t; forward/backward ordered-BDD widths and the
streaming width λ(t) = min of the two (invariant under isomorphism and mirror image);
surjectivity/injectivity on bi-infinite rows (pair-graph criterion); permutive tables
(all rows or all columns permutations); nilpotent automata (F_t constant).

## Step 3 — Falsification design

Every hypothesis named its refuting object: a magma with sub-geometric unbounded width
(H-C15-1), a bounded-width magma outside the three classes (H-C15-2), a surjective
non-permutive table (H-C15-3), a fast-forwardable automaton with unbounded width
(H-C15-4), a bounded-width class with long cycles (H-C15-5), a speedup below 100× or a
fast-forward losing at small t (H-C15-6). The pair-graph decisions are exact; all
fast-forwards are compared with direct simulation.

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C15-01 | order 2: rules 17m; XOR = Gould's sequence; all widths ≤ 3; surjective rules 51, 85, 102, 153, 170, 204 |
| EXP-C15-02 | order 3, 1734 classes: widths bounded 808 / linear 104 / geometric 300 / irregular 522 (t ≤ 9); 43 surjective = permutive; 7 reversible; 34 nilpotent |
| EXP-C15-03 | 99/99 fast-forwards exact; affine ×1800–2500 and fuse ×4000 at t = 10⁵ (L = 1024; single runs — the Skeptic's re-run gave ×1459–2262 and ×1363); commutative semigroups ×62–100, slower near t = 10³ |
| EXP-C15-04 | cycle detection: 1590/1734 rows (L = 32) repeat within 5000 steps; affine quasigroups and many geometric classes do not |
| EXP-C15-05 | fuse λ(t) = t + 2 to t = 12; Laver tables: bounded light cones; order-4 band surjective but not permutive; OEIS checks |

Timings are indicative (shared, loaded machine) and are stored under `timings`, which
the result hash ignores. The container restarted once during the cycle; all five
results were reproduced with the final code (identical result hashes for E01/E02).

## Step 6 — Analysis

* **Structure gives bounded width, but bounded width is much more common than
  structure.** Commutative semigroups (width ≤ |S|) and affine magmas (width ≤ |A|)
  are bounded, as proved (non-commutative semigroups need not be: for the group S₃
  the width grows 6, 6, 6, 36, 72, 216, 1296 for t = 0…6 — Skeptic review); yet 685 bounded-width order-3 automata have none of the known structures,
  including a reversible automaton whose light cone uses every cell.
* **Width can grow linearly.** The fuse magma (0 burnt, 1 burning, 2 intact) turns the
  light cone into a counter: a cell burns 2 steps after its right neighbour, so F_t
  compares t with twice the length of a run of fuses. The width is Θ(t); 104 order-3
  classes look linear.
* **Width is not predictability.** The same burn times compute any future row in
  O(L) time, so a CA can have unbounded streaming width and still be trivially
  fast-forwardable; conversely bounded width does not give short cycles (the affine
  quasigroups mod 3 have long ones).

## Step 7 — Proofs and counterexamples

Lean: `ca_comm_binomial`, `ca_step_shift`. Written: Theorems 1–6 of
`proofs/paper/C15.md` (semigroup light cones; affine fast-forward; exponent arithmetic;
the fuse magma; surjective ⇔ permutive for order ≤ 3 with the order-4 band; order 2 =
rules 17m). Counterexamples: the fuse magma (H-C15-1, H-C15-4), the reversible
automaton [[0,0,2],[2,2,0],[1,1,1]] (H-C15-2), x + y mod 3 (H-C15-5), the
commutative-semigroup benchmark (H-C15-6).

## Step 8 — Comparison with existing mathematics (Historian)

* Automata given by a binary operation: J. Pedersen, *Cellular automata as algebraic
  systems*, Complex Systems 6 (1992) 237–250 ([abstract](https://www.complex-systems.com/abstracts/v06_i03_a03/));
  C. Moore, A. Drisko, *Algebraic properties of the block transformation on cellular
  automata* (SFI WP 95-09-080; [record](https://ideas.repec.org/p/wop/safiwp/95-09-080.html));
  C. Moore, *Quasi-linear cellular automata* ([adap-org/9701001](https://arxiv.org/abs/adap-org/9701001));
  C. Moore, T. Pnin, *Predicting non-linear cellular automata quickly by decomposing
  them into linear ones* ([patt-sol/9701008](https://arxiv.org/abs/patt-sol/9701008)) —
  nilpotent/solvable group rules predicted in log depth. **REDISCOVERY** of the framework.
* Linear/affine CA and their fast-forward: Martin, Odlyzko, Wolfram, Comm. Math. Phys.
  93 (1984). **REDISCOVERY.**
* Surjective two-neighbour CA on prime alphabets are permutive: J. Kari, V. Salo,
  I. Törmä (2013) ([record](https://research.utu.fi/converis/portal/detail/Publication/3119276),
  [notes](https://villesalo.com/notes/STNCAoPANotes.html)); Hedlund (1969). **REDISCOVERY**
  (our exhaustive check confirms it for n = 2, 3; the order-4 band shows why primality matters).
* Computational irreducibility and coarse-graining: Wolfram; Israeli and Goldenfeld
  ([nlin/0309047](https://arxiv.org/abs/nlin/0309047)). No notion of streaming width of
  t-step rules or analysis of the fuse rule was found. **POTENTIALLY NOVEL** (small).
* OEIS: essential cells of x + y mod 3 = A006047 (Pascal's triangle mod 3); the
  surjective-table counts 1, 6, 420 match only A273820 (an lcm sequence), a three-term
  coincidence; the geometric width sequence of [[0,1,2],[2,0,0],[1,2,0]] has no match.

**Batch 1.1 update (2026-10-19, [Historian audit](../../../reviews/historian_C11_C20.md)).** Streaming width is
essentially the one-way communication complexity of the t-step rule used by Dürr, Rapaport and Theyssier,
*Cellular automata and communication complexity*, Theoret. Comput. Sci. 322 (2004) 355–368
([arXiv:cs/0210008](https://arxiv.org/abs/cs/0210008)), who classify the elementary automata experimentally and
give explicit linear-complexity rules (132, 23) and a three-state Θ(n²) automaton — so the refutations of H-C15-1
and H-C15-4 were already exemplified there. Only the fuse magma and the order-3 census are new; CLM-C15-04, -07,
-15 keep POTENTIALLY NOVEL with low confidence.

## Step 9 — Applications

Exact fast-forwarding of affine and fuse automata gives the state at t = 10⁹ in
milliseconds (about three orders of magnitude faster than simulation at t = 10⁵,
L = 1024; slower for t below about 20–70);
exponent arithmetic for commutative semigroups pays off only for t ≫ L; cycle detection
is generic but fails exactly where cycles are long. No claim beyond these measured
baselines is made.

## Step 10 — Documentation

`record.yaml` (18 claims, journal). Textbook: Chapter 17, "Magma automata and
fast-forwarding" (Volume 7).

## Next directions

1. Characterise bounded streaming width (685 unexplained order-3 classes).
2. Prove or refute CLM-C15-18 (bounded width ⇒ polylog-time fast-forward); fast-forward
   non-commutative semigroups via the popcount word.
3. Prove an exponential lower bound for one "geometric" order-3 automaton.
4. Light cones of Laver tables in general.
